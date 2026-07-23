"""Execução de ordens via CLOB API da Polymarket (py-clob-client).

Encapsula a criação/assinatura/submissão de ordens de mercado.
"""

from __future__ import annotations

from typing import Optional

from .config import Config
from .logger import get_logger

log = get_logger("clob")


class ClobExecutor:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self._client = None  # inicialização preguiçosa (só em modo LIVE)

    # -- inicialização ------------------------------------------------------

    def _ensure_client(self):
        """Cria e autentica o ClobClient na primeira utilização real."""
        if self._client is not None:
            return self._client

        # Import tardio: em DRY_RUN nem sequer precisamos da dependência.
        from py_clob_client.client import ClobClient

        client = ClobClient(
            self.cfg.clob_host,
            key=self.cfg.private_key,
            chain_id=self.cfg.chain_id,
            signature_type=self.cfg.signature_type,
            funder=self.cfg.funder_address,
        )
        # Deriva/cria as credenciais de API (L2) a partir da chave.
        client.set_api_creds(client.create_or_derive_api_creds())
        self._client = client
        log.info("Cliente CLOB autenticado (host=%s)", self.cfg.clob_host)
        return self._client

    def preflight(self) -> None:
        """Verifica que conseguimos autenticar antes de começar (só LIVE)."""
        if self.cfg.dry_run:
            log.info("DRY-RUN ativo — a saltar autenticação CLOB.")
            return
        self._ensure_client()

    # -- ordens -------------------------------------------------------------

    def market_buy(self, token_id: str, amount_usdc: float) -> Optional[dict]:
        """Compra a mercado (FOK): gasta ~amount_usdc no token."""
        if self.cfg.dry_run:
            log.info(
                "[DRY-RUN] COMPRARIA token=%s por %.2f USDC", token_id, amount_usdc
            )
            return {"dry_run": True, "side": "BUY", "amount": amount_usdc}

        from py_clob_client.clob_types import MarketOrderArgs, OrderType
        from py_clob_client.order_builder.constants import BUY

        try:
            client = self._ensure_client()
            order = client.create_market_order(
                MarketOrderArgs(
                    token_id=token_id,
                    amount=amount_usdc,  # em USDC para o lado BUY
                    side=BUY,
                    order_type=OrderType.FOK,
                )
            )
            resp = client.post_order(order, OrderType.FOK)
            log.info("Ordem BUY submetida: %s", resp)
            return resp
        except Exception as exc:  # noqa: BLE001 — queremos continuar vivos
            log.error("Falha na COMPRA de %s: %s", token_id, exc)
            return None

    def market_sell(self, token_id: str, shares: float) -> Optional[dict]:
        """Venda a mercado (FOK): vende `shares` do token."""
        if self.cfg.dry_run:
            log.info("[DRY-RUN] VENDERIA %.2f shares do token=%s", shares, token_id)
            return {"dry_run": True, "side": "SELL", "shares": shares}

        from py_clob_client.clob_types import MarketOrderArgs, OrderType
        from py_clob_client.order_builder.constants import SELL

        try:
            client = self._ensure_client()
            order = client.create_market_order(
                MarketOrderArgs(
                    token_id=token_id,
                    amount=shares,  # em shares para o lado SELL
                    side=SELL,
                    order_type=OrderType.FOK,
                )
            )
            resp = client.post_order(order, OrderType.FOK)
            log.info("Ordem SELL submetida: %s", resp)
            return resp
        except Exception as exc:  # noqa: BLE001
            log.error("Falha na VENDA de %s: %s", token_id, exc)
            return None
