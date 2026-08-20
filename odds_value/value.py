"""Deteção de valor: EV%, dispersão entre casas e filtros de contexto.

O fluxo é: para cada mercado de um jogo,
1. calcular a probabilidade de consenso (:mod:`odds_value.devig`);
2. comparar a melhor odd de cada seleção com essa probabilidade;
3. sinalizar EV positivo, medir a dispersão entre casas e anexar avisos de
   contexto (segunda mão de eliminatória, altitude, mercados combinados...).
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from typing import Sequence

from .devig import BookQuote, consensus

# Limite mínimo de EV para sinalizar uma seleção como valor (+2%).
DEFAULT_EV_THRESHOLD = 0.02

# Acima deste desvio relativo ao consenso, a melhor odd é "outlier":
# pode ser valor genuíno ou um erro/linha desatualizada da casa.
OUTLIER_ODDS_RATIO = 0.15  # 15% acima da odd justa


@dataclass
class ContextFlags:
    """Contexto do jogo/mercado que ajuda a filtrar falsos positivos."""

    second_leg_knockout: bool = False   # 2ª mão de eliminatória
    high_altitude: bool = False         # > 2000 m
    special_conditions: str = ""        # texto livre (clima, relvado, etc.)
    combined_market: bool = False       # ex.: resultado+golos (margem 20-30%)

    def warnings(self) -> list[str]:
        w: list[str] = []
        if self.second_leg_knockout:
            w.append(
                "2ª mão de eliminatória: o favorito pode não precisar de vencer "
                "(vantagem da 1ª mão), o que distorce mercados de resultado."
            )
        if self.high_altitude:
            w.append("Altitude relevante (>2000 m): pode afetar desempenho/golos.")
        if self.special_conditions:
            w.append(f"Condições especiais: {self.special_conditions}.")
        if self.combined_market:
            w.append(
                "Mercado combinado (ex.: resultado+golos): margem tipicamente "
                "20-30%, muito acima de mercados simples — consenso menos fiável."
            )
        return w


@dataclass
class ValueSelection:
    """Uma seleção avaliada, com a melhor odd e o seu EV."""

    game: str
    market: str
    selection: str
    best_odds: float
    best_book: str
    consensus_prob: float
    fair_odds: float
    ev: float                       # EV fracionário (0.03 = +3%)
    n_books: int
    odds_dispersion: float          # desvio-padrão das odds entre casas
    is_outlier: bool                # melhor odd muito acima do resto
    warnings: list[str] = field(default_factory=list)

    @property
    def ev_pct(self) -> float:
        return self.ev * 100.0

    @property
    def has_value(self) -> bool:
        return self.ev >= DEFAULT_EV_THRESHOLD


def expected_value(odds: float, prob: float) -> float:
    """EV fracionário: ``(odd * prob) - 1``. +0.05 = +5% de valor esperado."""
    return odds * prob - 1.0


def analyze_market(
    game: str,
    market: str,
    selections: Sequence[str],
    quotes: Sequence[BookQuote],
    context: ContextFlags | None = None,
    method: str = "shin",
    ev_threshold: float = DEFAULT_EV_THRESHOLD,
) -> list[ValueSelection]:
    """Avalia todas as seleções de um mercado e devolve as com EV >= limite.

    ``quotes`` são as odds de cada casa para as ``selections`` (mesma ordem).
    """
    context = context or ContextFlags()
    con = consensus(quotes, method=method)
    warnings = context.warnings()

    results: list[ValueSelection] = []
    for i, sel in enumerate(selections):
        col = [q.odds[i] for q in quotes]           # odds desta seleção em todas as casas
        best_idx = max(range(len(col)), key=lambda k: col[k])
        best_odds = col[best_idx]
        best_book = quotes[best_idx].bookmaker

        prob = con.probabilities[i]
        fair = con.fair_odds[i]
        ev = expected_value(best_odds, prob)

        dispersion = statistics.pstdev(col) if len(col) > 1 else 0.0
        # Outlier: melhor odd muito acima da odd justa de consenso.
        is_outlier = fair > 0 and (best_odds / fair - 1.0) >= OUTLIER_ODDS_RATIO

        sel_warnings = list(warnings)
        if is_outlier:
            sel_warnings.append(
                f"Melhor odd ({best_odds:.2f}) está {best_odds / fair - 1.0:+.0%} "
                f"acima da odd justa ({fair:.2f}): pode ser valor OU erro/"
                "informação em falta na casa. Confirmar antes de apostar."
            )

        if ev >= ev_threshold:
            results.append(
                ValueSelection(
                    game=game,
                    market=market,
                    selection=sel,
                    best_odds=best_odds,
                    best_book=best_book,
                    consensus_prob=prob,
                    fair_odds=fair,
                    ev=ev,
                    n_books=con.n_books,
                    odds_dispersion=dispersion,
                    is_outlier=is_outlier,
                    warnings=sel_warnings,
                )
            )
    return results


def rank_by_value(selections: Sequence[ValueSelection]) -> list[ValueSelection]:
    """Ordena por magnitude de EV (maior primeiro)."""
    return sorted(selections, key=lambda s: s.ev, reverse=True)
