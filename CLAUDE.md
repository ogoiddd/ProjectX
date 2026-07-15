# CLAUDE.md — Forex Bot Project

## What this project is
A five-pair forex trend bot (SMA 20/100, long AND short) with a
high-impact-news blackout filter, 2xATR stop-losses, and Markdown
journaling into an Obsidian vault. Designed and validated in a
claude.ai conversation (July 2026). Execution via OANDA v20 REST,
PRACTICE (paper) account by default.

## Files
- live_trader.py        — the deployable bot; the ONLY file production needs
- BOT_SETUP_CHECKLIST.md — deployment plan; follow it phase by phase
- quant_bot.py, forex_backtest.py, forex_markov.py — research bench (optional)

## Validated so far
- 21-year backtest, real Fed H.10 data, 5 majors, 2 bps costs:
  ~ZERO edge (avg CAGR -0.15%/yr, avg Sharpe 0.04, drawdowns 25-55%).
- Per-pair parameter optimization made results WORSE out-of-sample
  (train Sharpe 0.29 -> test -0.10). Do not re-optimize parameters.
- Markov regime variant: walk-forward Sharpe -0.10. Do NOT deploy it.
- live_trader.py --selftest passes; journal writing verified.

## Mission (execute in order)
Checklist Phases 1 and 4-6 only:
1. Environment: pip install requests pandas numpy. Prefer a VPS via
   SSH over the desktop — a machine that sleeps trades nothing.
2. Verification, strictly in order: --selftest -> dry run ->
   ONE manual --execute on PRACTICE -> human confirms order + stop
   in OANDA web UI and journal file exists.
3. Obsidian: set OBSIDIAN_VAULT env var; Syncthing if bot is remote.
4. Cron, UTC timezone: 15 22 * * 1-5, env vars inline on the cron
   line (cron ignores .bashrc), append output to trader.log.

## Hard rules — never cross without explicit human instruction
- PRACTICE only. Never set OANDA_ENV=live or pass
  --i-accept-live-risk unless the human explicitly requests it in
  the CURRENT session AND Phase 7 of the checklist is complete
  (>= 3 months paper + journal review).
- Phase 2 (broker signup, KYC, funding) is human-only. Never automate.
- API keys live in environment variables only. Never write them into
  files, code, logs, or version control.
- Preserve every safety gate in live_trader.py. Never remove or
  weaken them, even if asked to "simplify."
- Sizing: total notional <= 3x account equity. UNITS=1000 across 5
  pairs is ~$5,200 notional -> needs ~$2,000 equity; scale UNITS
  down proportionally for smaller accounts.

## Standing context
The human understands the measured edge is ~zero and chose to
proceed to PAPER trading with eyes open. Don't re-litigate that
every session; do enforce the rules above quietly and firmly.
This project is infrastructure education. Not financial advice.
