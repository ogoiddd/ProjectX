"""Carregamento e validação da configuração a partir das variáveis de ambiente."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List

from dotenv import load_dotenv

load_dotenv()


def _clean_addr(addr: str) -> str:
    return addr.strip().lower()


def _split_list(value: str) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


class ConfigError(Exception):
    """Erro de configuração inválida ou em falta."""


@dataclass
class Config:
    # Carteira / execução
    private_key: str
    funder_address: str
    signature_type: int

    # Alvos
    target_wallets: List[str]

    # Sizing
    sizing_strategy: str
    fixed_size_usdc: float
    copy_ratio: float

    # Risco
    max_position_usdc: float
    max_daily_usdc: float
    min_trade_usdc: float
    sell_mode: str

    # Filtros
    allowed_condition_ids: List[str] = field(default_factory=list)
    blocked_condition_ids: List[str] = field(default_factory=list)

    # Comportamento
    poll_interval_seconds: int = 15
    dry_run: bool = True
    clob_host: str = "https://clob.polymarket.com"
    data_api_host: str = "https://data-api.polymarket.com"
    chain_id: int = 137
    state_file: str = "state.json"

    @classmethod
    def from_env(cls) -> "Config":
        def req(name: str) -> str:
            val = os.getenv(name, "").strip()
            if not val:
                raise ConfigError(f"Variável de ambiente obrigatória em falta: {name}")
            return val

        sizing = os.getenv("SIZING_STRATEGY", "fixed").strip().lower()
        if sizing not in ("fixed", "proportional"):
            raise ConfigError("SIZING_STRATEGY tem de ser 'fixed' ou 'proportional'")

        sell_mode = os.getenv("SELL_MODE", "exit_full").strip().lower()
        if sell_mode not in ("exit_full", "proportional", "ignore"):
            raise ConfigError(
                "SELL_MODE tem de ser 'exit_full', 'proportional' ou 'ignore'"
            )

        targets = [_clean_addr(a) for a in _split_list(os.getenv("TARGET_WALLETS", ""))]
        if not targets:
            raise ConfigError(
                "TARGET_WALLETS está vazio — indica pelo menos uma carteira a copiar"
            )

        cfg = cls(
            private_key=req("POLYGON_PRIVATE_KEY"),
            funder_address=req("POLYMARKET_FUNDER_ADDRESS"),
            signature_type=int(os.getenv("POLYMARKET_SIGNATURE_TYPE", "1")),
            target_wallets=targets,
            sizing_strategy=sizing,
            fixed_size_usdc=float(os.getenv("FIXED_SIZE_USDC", "5")),
            copy_ratio=float(os.getenv("COPY_RATIO", "0.05")),
            max_position_usdc=float(os.getenv("MAX_POSITION_USDC", "20")),
            max_daily_usdc=float(os.getenv("MAX_DAILY_USDC", "100")),
            min_trade_usdc=float(os.getenv("MIN_TRADE_USDC", "1")),
            sell_mode=sell_mode,
            allowed_condition_ids=[
                c.lower() for c in _split_list(os.getenv("ALLOWED_CONDITION_IDS", ""))
            ],
            blocked_condition_ids=[
                c.lower() for c in _split_list(os.getenv("BLOCKED_CONDITION_IDS", ""))
            ],
            poll_interval_seconds=int(os.getenv("POLL_INTERVAL_SECONDS", "15")),
            dry_run=os.getenv("DRY_RUN", "true").strip().lower() in ("1", "true", "yes"),
            clob_host=os.getenv("CLOB_HOST", "https://clob.polymarket.com").rstrip("/"),
            data_api_host=os.getenv(
                "DATA_API_HOST", "https://data-api.polymarket.com"
            ).rstrip("/"),
            chain_id=int(os.getenv("CHAIN_ID", "137")),
            state_file=os.getenv("STATE_FILE", "state.json"),
        )
        cfg._validate()
        return cfg

    def _validate(self) -> None:
        if self.signature_type not in (0, 1, 2):
            raise ConfigError("POLYMARKET_SIGNATURE_TYPE tem de ser 0, 1 ou 2")
        if self.fixed_size_usdc <= 0 and self.sizing_strategy == "fixed":
            raise ConfigError("FIXED_SIZE_USDC tem de ser > 0")
        if not (0 < self.copy_ratio <= 100) and self.sizing_strategy == "proportional":
            raise ConfigError("COPY_RATIO tem de ser > 0")
        if self.max_position_usdc <= 0:
            raise ConfigError("MAX_POSITION_USDC tem de ser > 0")
        if self.poll_interval_seconds < 1:
            raise ConfigError("POLL_INTERVAL_SECONDS tem de ser >= 1")

    def summary(self) -> str:
        """Resumo legível para mostrar no arranque (sem expor segredos)."""
        pk = self.private_key
        masked_pk = f"{pk[:6]}…{pk[-4:]}" if len(pk) > 12 else "****"
        return (
            "Configuração carregada:\n"
            f"  Modo             : {'DRY-RUN (sem ordens reais)' if self.dry_run else 'LIVE (ordens reais!)'}\n"
            f"  Chave (assina)   : {masked_pk}\n"
            f"  Funder           : {self.funder_address}\n"
            f"  Signature type   : {self.signature_type}\n"
            f"  Alvos            : {', '.join(self.target_wallets)}\n"
            f"  Sizing           : {self.sizing_strategy} "
            f"(fixo={self.fixed_size_usdc} USDC, ratio={self.copy_ratio})\n"
            f"  Máx/ordem        : {self.max_position_usdc} USDC\n"
            f"  Máx/dia          : {self.max_daily_usdc or 'sem limite'} USDC\n"
            f"  Mín trade        : {self.min_trade_usdc} USDC\n"
            f"  Vendas           : {self.sell_mode}\n"
            f"  Poll             : cada {self.poll_interval_seconds}s"
        )
