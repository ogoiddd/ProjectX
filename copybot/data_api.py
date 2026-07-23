"""Cliente da Data API da Polymarket (deteção de trades e posições).

A Data API é pública (sem autenticação). Documentação:
https://docs.polymarket.com/api-reference/core/get-trades-for-a-user-or-markets
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import requests

from .logger import get_logger

log = get_logger("data_api")


@dataclass
class Trade:
    """Um trade individual devolvido pela Data API."""

    proxy_wallet: str  # carteira do trader
    side: str  # BUY ou SELL
    asset: str  # token_id (ERC-1155) — é o que a CLOB precisa
    condition_id: str  # id do mercado
    size: float  # nº de shares
    price: float  # preço por share (0..1)
    timestamp: int  # unix seconds
    tx_hash: str
    outcome: str  # ex.: "Yes"/"No"
    outcome_index: int
    title: str
    slug: str

    @property
    def usdc_value(self) -> float:
        """Valor aproximado do trade em USDC (shares * preço)."""
        return self.size * self.price

    @property
    def key(self) -> str:
        """Chave única para deduplicação."""
        return f"{self.tx_hash}:{self.asset}:{self.side}:{self.timestamp}"

    def describe(self) -> str:
        return (
            f"{self.side} {self.size:.2f} '{self.outcome}' @ {self.price:.3f} "
            f"(~{self.usdc_value:.2f} USDC) — {self.title[:60]}"
        )

    @classmethod
    def from_json(cls, d: dict) -> Optional["Trade"]:
        try:
            return cls(
                proxy_wallet=str(d.get("proxyWallet", "")).lower(),
                side=str(d.get("side", "")).upper(),
                asset=str(d.get("asset", "")),
                condition_id=str(d.get("conditionId", "")).lower(),
                size=float(d.get("size", 0) or 0),
                price=float(d.get("price", 0) or 0),
                timestamp=int(d.get("timestamp", 0) or 0),
                tx_hash=str(d.get("transactionHash", "")),
                outcome=str(d.get("outcome", "")),
                outcome_index=int(d.get("outcomeIndex", 0) or 0),
                title=str(d.get("title", "")),
                slug=str(d.get("slug", "")),
            )
        except (ValueError, TypeError) as exc:  # pragma: no cover
            log.warning("Trade ignorado (JSON inválido): %s (%s)", d, exc)
            return None


@dataclass
class Position:
    """Uma posição atual (holdings) de uma carteira."""

    asset: str  # token_id
    condition_id: str
    size: float  # shares detidas
    avg_price: float
    title: str

    @classmethod
    def from_json(cls, d: dict) -> Optional["Position"]:
        try:
            return cls(
                asset=str(d.get("asset", "")),
                condition_id=str(d.get("conditionId", "")).lower(),
                size=float(d.get("size", 0) or 0),
                avg_price=float(d.get("avgPrice", 0) or 0),
                title=str(d.get("title", "")),
            )
        except (ValueError, TypeError):  # pragma: no cover
            return None


class DataAPI:
    def __init__(self, host: str, timeout: int = 15):
        self.host = host.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "polymarket-copybot/1.0"})

    def get_user_trades(self, wallet: str, limit: int = 100) -> List[Trade]:
        """Trades mais recentes de uma carteira (taker), do mais recente ao mais antigo."""
        url = f"{self.host}/trades"
        params = {"user": wallet, "limit": limit, "takerOnly": "true"}
        try:
            resp = self.session.get(url, params=params, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as exc:
            log.error("Falha ao obter trades de %s: %s", wallet, exc)
            return []
        except ValueError:
            log.error("Resposta não-JSON ao obter trades de %s", wallet)
            return []

        if not isinstance(data, list):
            log.warning("Resposta inesperada da Data API: %s", type(data))
            return []

        trades = [t for t in (Trade.from_json(d) for d in data) if t is not None]
        # Ordena por timestamp crescente para processar por ordem cronológica.
        trades.sort(key=lambda t: t.timestamp)
        return trades

    def get_position(self, wallet: str, asset: str) -> Optional[Position]:
        """Posição atual de uma carteira num token específico (ou None se não tiver)."""
        url = f"{self.host}/positions"
        params = {"user": wallet}
        try:
            resp = self.session.get(url, params=params, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
        except (requests.RequestException, ValueError) as exc:
            log.error("Falha ao obter posições de %s: %s", wallet, exc)
            return None

        if not isinstance(data, list):
            return None

        for d in data:
            pos = Position.from_json(d)
            if pos and pos.asset == asset and pos.size > 0:
                return pos
        return None
