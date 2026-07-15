---
tags: [trading, bot, setup]
---

# Forex Bot — Deployment Checklist

Strategy: SMA 20/100 long/short, 5 majors, news blackout, 2×ATR stops.
Backtested edge ≈ zero over 21 years. This deploys infrastructure,
not income. Not financial advice.

## Phase 1 — Machine
- [ ] Ubuntu VPS (~$5/mo) or Raspberry Pi, always on
- [ ] `sudo apt install python3-pip && pip install requests pandas numpy`
- [ ] Copy `live_trader.py` to `/home/you/bot/`

## Phase 2 — Broker (OANDA)
- [ ] Practice account → API token + account ID
- [ ] Live account → KYC → fund ONLY affordable-loss money
- [ ] Live API token + account ID (kept aside until Phase 7)

## Phase 3 — Sizing
- [ ] UNITS=1000 × 5 pairs ≈ $5,200 notional
- [ ] Fund ≥ $2,000 (≈2.6× leverage) or halve UNITS per $1,000
- [ ] Per-trade stop risk ≈ $15–20/pair at default size

## Phase 4 — Verify (practice keys)
- [ ] `python3 live_trader.py --selftest` — offline logic OK
- [ ] `python3 live_trader.py` — dry run, no orders
- [ ] `python3 live_trader.py --execute` — order + stop visible in
      OANDA web UI, journal file written

## Phase 5 — Obsidian journal
- [ ] Local bot: `OBSIDIAN_VAULT=/path/inside/your/vault`
- [ ] VPS bot: Syncthing on VPS + device → sync journal folder
      into vault
- [ ] Confirm entries appear on phone

## Phase 6 — Automation
- [ ] `timedatectl set-timezone UTC`
- [ ] `crontab -e`:
      `15 22 * * 1-5 cd /home/you/bot && OANDA_API_KEY=xxx OANDA_ACCOUNT_ID=yyy OBSIDIAN_VAULT=/home/you/sync/journal python3 live_trader.py --execute >> trader.log 2>&1`
- [ ] Heartbeat rule: no journal note on a weekday → read trader.log

## Phase 7 — Gate to live money
- [ ] ≥ 3 months on practice
- [ ] Journal review: slippage vs backtest, news blocks firing,
      fills sane
- [ ] Decision point. If proceeding: live token, `OANDA_ENV=live`,
      add `--i-accept-live-risk`, half size for 2 weeks
- [ ] Kill switch: `crontab -r` stops the bot; stops remain live
      server-side at OANDA

## Monthly review (with Claude)
- [ ] Paste journal entries into chat for analysis
- [ ] Re-run the live signal board via FMP
- [ ] Compare running P&L vs backtest expectation (≈ 0)
