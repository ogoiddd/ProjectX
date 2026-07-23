"""Cálculo do tamanho das ordens copiadas e aplicação dos limites de risco."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .config import Config
from .data_api import Trade


@dataclass
class CopyDecision:
    """Resultado da decisão de copiar (ou não) um trade."""

    should_copy: bool
    reason: str
    # Para BUY: montante em USDC a gastar. Para SELL: nº de shares a vender.
    amount: float = 0.0
    is_buy: bool = True


def _passes_filters(trade: Trade, cfg: Config) -> Optional[str]:
    """Devolve um motivo de rejeição, ou None se passar todos os filtros."""
    cid = trade.condition_id.lower()
    if cfg.allowed_condition_ids and cid not in cfg.allowed_condition_ids:
        return "mercado não está na allowlist"
    if cid in cfg.blocked_condition_ids:
        return "mercado está na blocklist"
    return None


def decide_buy(trade: Trade, cfg: Config, remaining_daily: float) -> CopyDecision:
    """Decide como copiar uma COMPRA do alvo."""
    reason = _passes_filters(trade, cfg)
    if reason:
        return CopyDecision(False, reason)

    if trade.usdc_value < cfg.min_trade_usdc:
        return CopyDecision(
            False,
            f"abaixo do mínimo ({trade.usdc_value:.2f} < {cfg.min_trade_usdc} USDC)",
        )

    # Tamanho base conforme a estratégia.
    if cfg.sizing_strategy == "fixed":
        amount = cfg.fixed_size_usdc
    else:  # proportional
        amount = trade.usdc_value * cfg.copy_ratio

    # Teto por ordem.
    if amount > cfg.max_position_usdc:
        amount = cfg.max_position_usdc

    # Teto diário.
    if amount > remaining_daily:
        if remaining_daily <= 0:
            return CopyDecision(False, "orçamento diário esgotado")
        amount = remaining_daily

    # A Polymarket exige ordens minimamente significativas.
    if amount < 1.0:
        return CopyDecision(
            False, f"montante calculado demasiado pequeno ({amount:.2f} USDC)"
        )

    return CopyDecision(
        True, f"comprar ~{amount:.2f} USDC", amount=round(amount, 2), is_buy=True
    )


def decide_sell(
    trade: Trade, cfg: Config, our_shares: float
) -> CopyDecision:
    """Decide como copiar uma VENDA do alvo, dado quanto detemos do token."""
    if cfg.sell_mode == "ignore":
        return CopyDecision(False, "SELL_MODE=ignore")

    reason = _passes_filters(trade, cfg)
    if reason:
        return CopyDecision(False, reason)

    if our_shares <= 0:
        return CopyDecision(False, "não temos posição neste token")

    if cfg.sell_mode == "exit_full":
        shares = our_shares
    else:  # proportional — vende a mesma fração, limitada ao que temos
        shares = min(our_shares, trade.size * cfg.copy_ratio)

    if shares <= 0:
        return CopyDecision(False, "nada a vender após cálculo")

    return CopyDecision(
        True, f"vender {shares:.2f} shares", amount=round(shares, 2), is_buy=False
    )
