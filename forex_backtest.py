#!/usr/bin/env python3
"""forex_backtest.py — research bench: SMA 20/100 trend backtest on Fed H.10 data.

REBUILD NOTICE: reconstruction of the lost research script described in
CLAUDE.md. Re-runs the 21-year, five-major, 2 bps-cost backtest behind the
project's headline finding (edge ~ zero). Research only — production needs
nothing but live_trader.py.

Data: Federal Reserve H.10 daily noon rates via FRED CSV (no API key).
Strategy: identical to live_trader.py — long when SMA20 > SMA100, short
otherwise, always in the market once history allows.
Costs: 2 bps (0.0002) one-way per unit of position change; a flip
(long -> short) is two one-way trades.

Usage: python3 forex_backtest.py [--years 21] [--fast 20] [--slow 100]
"""

import argparse
import datetime as dt
import io
import os

import numpy as np
import pandas as pd
import requests

# FRED series are already quoted in each pair's trading convention.
SERIES = {
    "EUR_USD": "DEXUSEU",
    "GBP_USD": "DEXUSUK",
    "USD_JPY": "DEXJPUS",
    "USD_CHF": "DEXSZUS",
    "AUD_USD": "DEXUSAL",
}
COST_ONE_WAY = 0.0002  # 2 bps per unit of position change
TRADING_DAYS = 252
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".fred_cache")


def fetch_series(series_id):
    cache = os.path.join(CACHE_DIR, f"{series_id}.csv")
    if os.path.exists(cache) and (
        dt.datetime.now().timestamp() - os.path.getmtime(cache) < 86400
    ):
        text = open(cache, encoding="utf-8").read()
    else:
        r = requests.get(
            "https://fred.stlouisfed.org/graph/fredgraph.csv",
            params={"id": series_id}, timeout=60,
        )
        r.raise_for_status()
        text = r.text
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(cache, "w", encoding="utf-8") as f:
            f.write(text)
    df = pd.read_csv(io.StringIO(text), na_values=".", parse_dates=[0])
    df.columns = ["date", "price"]
    return df.dropna().set_index("date")["price"]


def backtest_pair(price, fast, slow):
    """Daily always-in SMA crossover; returns (net daily returns, positions)."""
    pos = np.where(price.rolling(fast).mean() > price.rolling(slow).mean(), 1.0, -1.0)
    pos = pd.Series(pos, index=price.index)
    pos[price.rolling(slow).mean().isna()] = 0.0  # flat until history exists
    ret = pos.shift(1) * price.pct_change()
    cost = COST_ONE_WAY * pos.diff().abs()
    return (ret - cost).fillna(0.0), pos


def stats(net, pos):
    equity = (1 + net).cumprod()
    years = len(net) / TRADING_DAYS
    cagr = equity.iloc[-1] ** (1 / years) - 1
    sharpe = net.mean() / net.std() * np.sqrt(TRADING_DAYS) if net.std() > 0 else 0.0
    max_dd = (equity / equity.cummax() - 1).min()

    # Trades = segments between position changes (always-in system).
    change_points = pos.ne(pos.shift()).cumsum()
    trade_rets = (1 + net).groupby(change_points).prod() - 1
    trade_rets = trade_rets[pos.groupby(change_points).first() != 0]
    wins = trade_rets[trade_rets > 0]
    losses = trade_rets[trade_rets <= 0]
    win_rate = len(wins) / len(trade_rets) if len(trade_rets) else float("nan")
    profit_factor = (
        wins.sum() / abs(losses.sum()) if len(losses) and losses.sum() != 0
        else float("inf")
    )
    return {
        "CAGR %": 100 * cagr,
        "Sharpe": sharpe,
        "MaxDD %": 100 * max_dd,
        "Trades": len(trade_rets),
        "Win %": 100 * win_rate,
        "ProfitFactor": profit_factor,
        "TotalRet %": 100 * (equity.iloc[-1] - 1),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--years", type=int, default=21)
    ap.add_argument("--fast", type=int, default=20)
    ap.add_argument("--slow", type=int, default=100)
    args = ap.parse_args()

    end = dt.date.today()
    start = end - dt.timedelta(days=int(args.years * 365.25))
    print(f"SMA {args.fast}/{args.slow} long/short | {start} .. {end} | "
          f"costs {COST_ONE_WAY * 1e4:.0f} bps one-way\n")

    rows = {}
    for pair, sid in SERIES.items():
        price = fetch_series(sid)
        price = price[(price.index.date >= start)]
        net, pos = backtest_pair(price, args.fast, args.slow)
        rows[pair] = stats(net, pos)

    table = pd.DataFrame(rows).T
    avg = table.mean(numeric_only=True)
    avg.name = "AVERAGE"
    table = pd.concat([table, avg.to_frame().T])
    with pd.option_context("display.float_format", "{:0.2f}".format,
                           "display.width", 120):
        print(table)
    print("\nReminder (CLAUDE.md): edge ~ zero is the expected result. Do not "
          "re-optimize parameters; out-of-sample that made things worse.")


if __name__ == "__main__":
    main()
