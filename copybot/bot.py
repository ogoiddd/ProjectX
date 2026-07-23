"""Loop principal do bot: deteta trades dos alvos e copia-os."""

from __future__ import annotations

import signal
import time

from .clob import ClobExecutor
from .config import Config
from .data_api import DataAPI, Trade
from .logger import get_logger
from .sizing import decide_buy, decide_sell
from .state import State

log = get_logger("bot")


class CopyBot:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.data = DataAPI(cfg.data_api_host)
        self.executor = ClobExecutor(cfg)
        self.state = State(cfg.state_file)
        self._running = True

    def stop(self, *_):
        log.info("Sinal de paragem recebido — a terminar após o ciclo atual…")
        self._running = False

    # -- ciclo de deteção ---------------------------------------------------

    def _collect_new_trades(self):
        """Junta trades novos (ainda não vistos) de todos os alvos, por ordem cronológica."""
        new_trades = []
        for wallet in self.cfg.target_wallets:
            for trade in self.data.get_user_trades(wallet, limit=100):
                if not trade.tx_hash or trade.side not in ("BUY", "SELL"):
                    continue
                if self.state.has_seen(trade.key):
                    continue
                new_trades.append(trade)
        new_trades.sort(key=lambda t: t.timestamp)
        return new_trades

    def _bootstrap(self) -> None:
        """
        No primeiro arranque marca todos os trades atuais como vistos SEM copiar,
        para não copiar retroativamente o histórico inteiro do alvo.
        """
        count = 0
        for wallet in self.cfg.target_wallets:
            for trade in self.data.get_user_trades(wallet, limit=100):
                self.state.mark_seen(trade.key)
                count += 1
        self.state.bootstrapped = True
        self.state.save()
        log.info(
            "Bootstrap concluído: %d trades históricos marcados como vistos "
            "(não serão copiados). A partir de agora só copio trades NOVOS.",
            count,
        )

    # -- cópia de um trade --------------------------------------------------

    def _handle_trade(self, trade: Trade) -> None:
        who = trade.proxy_wallet[:8]
        log.info("Trade novo de %s…: %s", who, trade.describe())

        if trade.side == "BUY":
            remaining = self.state.remaining_daily_budget(self.cfg.max_daily_usdc)
            decision = decide_buy(trade, self.cfg, remaining)
            if not decision.should_copy:
                log.info("  ↳ ignorado: %s", decision.reason)
                return
            log.info("  ↳ a copiar: %s", decision.reason)
            resp = self.executor.market_buy(trade.asset, decision.amount)
            if resp is not None:
                self.state.record_spend(decision.amount)

        else:  # SELL
            our_shares = 0.0
            if self.cfg.sell_mode != "ignore":
                pos = self.data.get_position(self.cfg.funder_address, trade.asset)
                our_shares = pos.size if pos else 0.0
            decision = decide_sell(trade, self.cfg, our_shares)
            if not decision.should_copy:
                log.info("  ↳ ignorado: %s", decision.reason)
                return
            log.info("  ↳ a copiar: %s", decision.reason)
            self.executor.market_sell(trade.asset, decision.amount)

    # -- loop ---------------------------------------------------------------

    def run(self) -> None:
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

        log.info("%s", self.cfg.summary())
        if self.cfg.dry_run:
            log.warning(
                "MODO DRY-RUN: nenhuma ordem real será enviada. "
                "Muda DRY_RUN=false no .env quando estiveres pronto."
            )

        # Autentica cedo (falha rápido se as credenciais estiverem erradas).
        self.executor.preflight()

        if not self.state.bootstrapped:
            log.info("Primeiro arranque — a fazer bootstrap do histórico…")
            self._bootstrap()

        log.info("Bot a correr. Ctrl+C para parar.")
        while self._running:
            try:
                new_trades = self._collect_new_trades()
                if new_trades:
                    log.info("%d trade(s) novo(s) detetado(s).", len(new_trades))
                for trade in new_trades:
                    self._handle_trade(trade)
                    self.state.mark_seen(trade.key)
                    self.state.save()
            except Exception as exc:  # noqa: BLE001 — o loop nunca deve morrer
                log.exception("Erro no ciclo principal: %s", exc)

            # Espera fraccionada para reagir depressa ao Ctrl+C.
            for _ in range(self.cfg.poll_interval_seconds):
                if not self._running:
                    break
                time.sleep(1)

        self.state.save()
        log.info("Bot terminado. Estado guardado.")
