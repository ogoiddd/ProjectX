#!/usr/bin/env python3
"""live_trader.py — five-pair SMA trend bot for OANDA v20 (PRACTICE by default).

REBUILD NOTICE: this is a reconstruction to the spec in CLAUDE.md (July 2026);
the originally validated file was lost. It must re-pass the full Phase 4
verification chain in BOT_SETUP_CHECKLIST.md (--selftest -> dry run -> ONE
manual --execute confirmed by a human in the OANDA web UI) before being
placed under cron.

Strategy: SMA 20/100 crossover on daily candles, long AND short, five majors.
Risk: 2xATR(14) server-side stop-loss on every position, total notional
capped at 3x account equity, high-impact-news blackout on new entries.
Journal: one Markdown note per run into $OBSIDIAN_VAULT.

Modes:
    python3 live_trader.py --selftest    offline logic checks, no network
    python3 live_trader.py               dry run: fetch + decide, NO orders
    python3 live_trader.py --execute     place orders (PRACTICE unless the
                                         live gates below are BOTH passed)

Configuration (environment variables only — never files, never argv):
    OANDA_API_KEY      v20 API token                              (required)
    OANDA_ACCOUNT_ID   account id, e.g. 101-004-1234567-001       (required)
    OANDA_ENV          "practice" (default) | "live"
    UNITS              base units per pair (default 1000)
    OBSIDIAN_VAULT     journal directory (default ./journal)

Safety gates — do not remove or weaken (CLAUDE.md hard rules):
    G1  practice is the default environment
    G2  live requires OANDA_ENV=live AND --i-accept-live-risk together
    G3  no order of any kind without --execute
    G4  every entry carries a server-side 2xATR stop-loss
    G5  run aborts if planned total notional > 3x account equity
    G6  news-calendar failure blocks NEW entries (fail closed)
    G7  credentials come from env vars and are never printed or written
"""

import argparse
import datetime as dt
import json
import os
import sys
import tempfile

import numpy as np
import pandas as pd
import requests

PAIRS = ["EUR_USD", "GBP_USD", "USD_JPY", "USD_CHF", "AUD_USD"]
SMA_FAST = 20
SMA_SLOW = 100
ATR_LEN = 14
ATR_STOP_MULT = 2.0
MAX_LEVERAGE = 3.0          # total notional <= 3x equity (gate G5)
NEWS_WINDOW_HOURS = 24      # block new entries if high-impact news this soon
CANDLE_COUNT = SMA_SLOW + ATR_LEN + 10

HOSTS = {
    "practice": "https://api-fxpractice.oanda.com",
    "live": "https://api-fxtrade.oanda.com",
}
NEWS_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"


def log(msg):
    print(f"{dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M:%S}Z {msg}", flush=True)


# ---------------------------------------------------------------- indicators

def sma(closes, n):
    return float(pd.Series(closes).rolling(n).mean().iloc[-1])


def atr(highs, lows, closes, n=ATR_LEN):
    h, l, c = (pd.Series(x, dtype=float) for x in (highs, lows, closes))
    prev_c = c.shift(1)
    tr = pd.concat([h - l, (h - prev_c).abs(), (l - prev_c).abs()], axis=1).max(axis=1)
    return float(tr.rolling(n).mean().iloc[-1])


def signal(closes):
    """+1 long when SMA20 > SMA100, -1 short otherwise. Always positioned."""
    return 1 if sma(closes, SMA_FAST) > sma(closes, SMA_SLOW) else -1


def notional_usd(pair, units, price):
    """Approximate USD notional of a position in `pair` at `price`."""
    base = pair.split("_")[0]
    return abs(units) if base == "USD" else abs(units) * price


# ---------------------------------------------------------------- OANDA API

class Oanda:
    def __init__(self, env, key, account):
        self.base = HOSTS[env]
        self.account = account
        self.s = requests.Session()
        self.s.headers["Authorization"] = f"Bearer {key}"

    def _get(self, path, **params):
        r = self.s.get(self.base + path, params=params, timeout=30)
        r.raise_for_status()
        return r.json()

    def candles(self, pair):
        j = self._get(f"/v3/instruments/{pair}/candles",
                      granularity="D", count=CANDLE_COUNT, price="M")
        rows = [c for c in j["candles"] if c["complete"]]
        return {
            "close": [float(c["mid"]["c"]) for c in rows],
            "high": [float(c["mid"]["h"]) for c in rows],
            "low": [float(c["mid"]["l"]) for c in rows],
        }

    def equity(self):
        return float(self._get(f"/v3/accounts/{self.account}/summary")["account"]["NAV"])

    def open_units(self):
        """{pair: signed units} for currently open positions."""
        j = self._get(f"/v3/accounts/{self.account}/openPositions")
        out = {}
        for p in j["positions"]:
            units = int(p["long"]["units"]) + int(p["short"]["units"])
            if units:
                out[p["instrument"]] = units
        return out

    def market_order(self, pair, units, stop_distance):
        order = {"order": {
            "type": "MARKET",
            "instrument": pair,
            "units": str(units),
            "timeInForce": "FOK",
            "positionFill": "DEFAULT",
            "stopLossOnFill": {"distance": f"{stop_distance:.5f}", "timeInForce": "GTC"},
        }}
        r = self.s.post(f"{self.base}/v3/accounts/{self.account}/orders",
                        json=order, timeout=30)
        r.raise_for_status()
        return r.json()

    def close_position(self, pair, units):
        body = {"longUnits": "ALL"} if units > 0 else {"shortUnits": "ALL"}
        r = self.s.put(f"{self.base}/v3/accounts/{self.account}/positions/{pair}/close",
                       json=body, timeout=30)
        r.raise_for_status()
        return r.json()


# ---------------------------------------------------------------- news filter

def blocked_currencies(now=None, fetch=None):
    """Currencies with high-impact news within NEWS_WINDOW_HOURS.

    Returns (set_of_currencies, ok). On any failure returns (set(), False)
    and the caller must fail closed for NEW entries (gate G6).
    """
    now = now or dt.datetime.now(dt.timezone.utc)
    try:
        if fetch is None:
            r = requests.get(NEWS_URL, timeout=15)
            r.raise_for_status()
            events = r.json()
        else:
            events = fetch()
        blocked = set()
        for ev in events:
            if str(ev.get("impact", "")).lower() != "high":
                continue
            when = dt.datetime.fromisoformat(ev["date"])
            if 0 <= (when - now).total_seconds() <= NEWS_WINDOW_HOURS * 3600:
                blocked.add(ev.get("country", "").upper())
        return blocked, True
    except Exception as e:  # noqa: BLE001 — any failure means fail closed
        log(f"WARNING news calendar unavailable ({type(e).__name__}); "
            f"failing CLOSED: no new entries this run")
        return set(), False


def pair_blocked(pair, blocked, calendar_ok):
    if not calendar_ok:
        return True
    a, b = pair.split("_")
    return a in blocked or b in blocked


# ---------------------------------------------------------------- journaling

def journal_dir():
    return os.environ.get("OBSIDIAN_VAULT", os.path.join(os.getcwd(), "journal"))


def write_journal(rows, equity, mode, path=None):
    path = path or journal_dir()
    os.makedirs(path, exist_ok=True)
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    fname = os.path.join(path, f"{today}-forex-bot.md")
    lines = [
        "---",
        f"date: {today}",
        "tags: [trading, bot, journal]",
        f"mode: {mode}",
        "---",
        "",
        f"# Forex bot run — {today}",
        "",
        f"- Mode: **{mode}**",
        f"- Account equity: {equity if equity is not None else 'n/a'}",
        "",
        "| Pair | Signal | Action | Price | Stop dist | Units |",
        "|------|--------|--------|-------|-----------|-------|",
    ]
    for r in rows:
        lines.append("| {pair} | {signal} | {action} | {price} | {stop} | {units} |"
                     .format(**r))
    lines.append("")
    with open(fname, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return fname


# ---------------------------------------------------------------- live gates

def resolve_env(argv_flag_accept_live):
    """Gates G1+G2: returns 'practice' or 'live', refusing half-armed live."""
    env = os.environ.get("OANDA_ENV", "practice").lower()
    if env not in HOSTS:
        raise SystemExit(f"OANDA_ENV must be 'practice' or 'live', got {env!r}")
    if env == "live" and not argv_flag_accept_live:
        raise SystemExit("REFUSED: OANDA_ENV=live requires --i-accept-live-risk. "
                         "See Phase 7 of BOT_SETUP_CHECKLIST.md.")
    if env != "live" and argv_flag_accept_live:
        raise SystemExit("REFUSED: --i-accept-live-risk given but OANDA_ENV is not "
                         "'live'. Remove the flag or set the env var deliberately.")
    return env


# ---------------------------------------------------------------- main run

def run(execute):
    accept_live = "--i-accept-live-risk" in sys.argv
    env = resolve_env(accept_live)
    key = os.environ.get("OANDA_API_KEY")
    account = os.environ.get("OANDA_ACCOUNT_ID")
    if not key or not account:
        raise SystemExit("Set OANDA_API_KEY and OANDA_ACCOUNT_ID environment "
                         "variables (never write them into files).")
    units_per_pair = int(os.environ.get("UNITS", "1000"))
    mode = "EXECUTE" if execute else "DRY RUN"
    log(f"=== live_trader {mode} | env={env} | units={units_per_pair} ===")
    if env == "live":
        log("*** LIVE ACCOUNT — real money at risk ***")

    api = Oanda(env, key, account)
    equity = api.equity()
    open_pos = api.open_units()
    blocked, calendar_ok = blocked_currencies()
    if calendar_ok and blocked:
        log(f"news blackout currencies (next {NEWS_WINDOW_HOURS}h): {sorted(blocked)}")

    plans, rows = [], []
    for pair in PAIRS:
        d = api.candles(pair)
        if len(d["close"]) < SMA_SLOW + 1:
            log(f"{pair}: insufficient history, skipping")
            continue
        sig = signal(d["close"])
        price = d["close"][-1]
        stop = ATR_STOP_MULT * atr(d["high"], d["low"], d["close"])
        held = open_pos.get(pair, 0)
        target = sig * units_per_pair

        if held and (held > 0) == (sig > 0):
            action = "hold"
        elif held:
            action = "flip-close" if pair_blocked(pair, blocked, calendar_ok) else "flip"
        else:
            action = "news-blocked" if pair_blocked(pair, blocked, calendar_ok) else "open"

        plans.append({"pair": pair, "sig": sig, "held": held, "target": target,
                      "price": price, "stop": stop, "action": action})
        rows.append({"pair": pair, "signal": "LONG" if sig > 0 else "SHORT",
                     "action": action, "price": f"{price:.5f}",
                     "stop": f"{stop:.5f}", "units": target})
        log(f"{pair}: signal={'LONG' if sig > 0 else 'SHORT'} price={price:.5f} "
            f"stop_dist={stop:.5f} held={held} -> {action}")

    planned = sum(notional_usd(p["pair"], units_per_pair, p["price"])
                  for p in plans if p["action"] in ("open", "flip", "hold"))
    log(f"equity={equity:.2f} planned_notional~{planned:.0f} "
        f"cap={MAX_LEVERAGE:.0f}x={MAX_LEVERAGE * equity:.0f}")
    if planned > MAX_LEVERAGE * equity:
        raise SystemExit(f"ABORT (gate G5): planned notional {planned:.0f} exceeds "
                         f"{MAX_LEVERAGE:.0f}x equity {equity:.2f}. Lower UNITS.")

    if not execute:
        log("dry run complete — no orders placed, no journal written")
        return

    for p in plans:
        if p["action"] in ("flip", "flip-close"):
            log(f"{p['pair']}: closing {p['held']} units")
            api.close_position(p["pair"], p["held"])
        if p["action"] in ("open", "flip"):
            log(f"{p['pair']}: market order {p['target']} units, "
                f"stop distance {p['stop']:.5f}")
            api.market_order(p["pair"], p["target"], p["stop"])

    fname = write_journal(rows, equity, f"{mode} ({env})")
    log(f"journal written: {fname}")
    log("run complete")


# ---------------------------------------------------------------- self-test

def selftest():
    failures = []

    def check(name, cond):
        log(f"  {'PASS' if cond else 'FAIL'}  {name}")
        if not cond:
            failures.append(name)

    log("--- selftest (offline) ---")

    up = list(np.linspace(1.0, 2.0, 120))
    down = list(np.linspace(2.0, 1.0, 120))
    check("SMA math", abs(sma([1, 2, 3, 4, 5], 5) - 3.0) < 1e-9)
    check("signal long on uptrend", signal(up) == 1)
    check("signal short on downtrend", signal(down) == -1)

    h = [1.10] * 30
    l = [1.00] * 30
    c = [1.05] * 30
    check("ATR on constant-range series", abs(atr(h, l, c) - 0.10) < 1e-9)

    check("notional USD-base", notional_usd("USD_JPY", 1000, 155.0) == 1000)
    check("notional USD-quote", abs(notional_usd("EUR_USD", 1000, 1.08) - 1080) < 1e-9)
    check("sizing cap trips",
          5 * notional_usd("EUR_USD", 1000, 1.04) > MAX_LEVERAGE * 1500)
    check("sizing cap clears",
          5 * notional_usd("EUR_USD", 1000, 1.04) <= MAX_LEVERAGE * 2000)

    now = dt.datetime(2026, 1, 5, 12, 0, tzinfo=dt.timezone.utc)
    fake = lambda: [  # noqa: E731
        {"impact": "High", "country": "USD",
         "date": (now + dt.timedelta(hours=3)).isoformat()},
        {"impact": "Low", "country": "EUR",
         "date": (now + dt.timedelta(hours=3)).isoformat()},
        {"impact": "High", "country": "GBP",
         "date": (now + dt.timedelta(hours=90)).isoformat()},
    ]
    blocked, ok = blocked_currencies(now=now, fetch=fake)
    check("news filter blocks imminent high-impact", ok and blocked == {"USD"})
    check("news filter blocks pair by currency",
          pair_blocked("EUR_USD", blocked, ok) and not pair_blocked("EUR_GBP", blocked, ok))
    bad_blocked, bad_ok = blocked_currencies(now=now,
                                             fetch=lambda: (_ for _ in ()).throw(IOError()))
    check("news filter fails CLOSED", not bad_ok
          and pair_blocked("EUR_USD", bad_blocked, bad_ok))

    with tempfile.TemporaryDirectory() as td:
        fname = write_journal(
            [{"pair": "EUR_USD", "signal": "LONG", "action": "open",
              "price": "1.08000", "stop": "0.01400", "units": 1000}],
            2000.0, "SELFTEST", path=td)
        content = open(fname, encoding="utf-8").read()
        check("journal file written", os.path.exists(fname))
        check("journal contains trade row", "EUR_USD" in content and "1.08000" in content)

    saved_env, saved_argv = os.environ.get("OANDA_ENV"), sys.argv[:]
    try:
        os.environ["OANDA_ENV"] = "live"
        sys.argv = ["live_trader.py"]
        try:
            resolve_env(argv_flag_accept_live=False)
            check("live gate refuses without flag", False)
        except SystemExit:
            check("live gate refuses without flag", True)
        os.environ["OANDA_ENV"] = "practice"
        try:
            resolve_env(argv_flag_accept_live=True)
            check("live gate refuses flag without env", False)
        except SystemExit:
            check("live gate refuses flag without env", True)
        check("practice resolves by default",
              resolve_env(argv_flag_accept_live=False) == "practice")
    finally:
        sys.argv = saved_argv
        if saved_env is None:
            os.environ.pop("OANDA_ENV", None)
        else:
            os.environ["OANDA_ENV"] = saved_env

    if failures:
        log(f"--- selftest FAILED: {len(failures)} check(s) ---")
        raise SystemExit(1)
    log("--- selftest PASSED: all checks OK ---")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true", help="offline logic checks")
    ap.add_argument("--execute", action="store_true",
                    help="actually place orders (default is dry run)")
    ap.add_argument("--i-accept-live-risk", action="store_true",
                    help="required together with OANDA_ENV=live; see Phase 7")
    args = ap.parse_args()
    if args.selftest:
        selftest()
    else:
        run(execute=args.execute)


if __name__ == "__main__":
    main()
