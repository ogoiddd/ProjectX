"""Pipeline partilhado: recolha → parsing → análise de valor.

Usado tanto pela CLI (:mod:`odds_value.cli`) como pela web app
(:mod:`odds_value.web`), para não duplicar lógica.
"""

from __future__ import annotations

import csv
import io
import json
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Sequence

from .fetch import GameOdds, fetch_odds_the_odds_api, parse_the_odds_api
from .value import (
    DEFAULT_EV_THRESHOLD,
    MIN_BOOKS,
    MIN_CONSENSUS_PROB,
    ContextFlags,
    ValueSelection,
    analyze_market,
    rank_by_value,
)


@dataclass
class AnalysisReport:
    """Resultado agregado da análise de todos os jogos."""

    values: list[ValueSelection] = field(default_factory=list)   # ordenados por EV
    markets_analyzed: int = 0                                     # mercados considerados
    markets_discarded_few_books: int = 0                          # descartados (<min_books)
    best_book_counts: Counter = field(default_factory=Counter)    # casa -> nº de "melhor odd"
    selections_evaluated: int = 0                                 # seleções com melhor-odd

    @property
    def n_value(self) -> int:
        return len(self.values)


def analyze_games(
    games: Sequence[GameOdds],
    method: str = "shin",
    ev_threshold: float = DEFAULT_EV_THRESHOLD,
    min_books: int = MIN_BOOKS,
    min_prob: float = MIN_CONSENSUS_PROB,
) -> AnalysisReport:
    """Corre a análise de valor sobre todos os jogos e agrega estatísticas."""
    report = AnalysisReport()
    for g in games:
        for mkt in g.markets:
            ctx = ContextFlags(
                second_leg_knockout=g.context.second_leg_knockout,
                high_altitude=g.context.high_altitude,
                special_conditions=g.context.special_conditions,
                combined_market="+" in mkt.market or "&" in mkt.market,
            )
            res = analyze_market(
                game=g.game,
                market=mkt.market,
                selections=mkt.selections,
                quotes=mkt.quotes,
                context=ctx,
                method=method,
                ev_threshold=ev_threshold,
                min_books=min_books,
                min_prob=min_prob,
            )
            if res.discarded_few_books:
                report.markets_discarded_few_books += 1
                continue
            report.markets_analyzed += 1
            report.values.extend(res.values)
            # (4) estatística por casa: quem dá a melhor odd, em todas as seleções
            report.best_book_counts.update(res.best_books)
            report.selections_evaluated += len(res.best_books)

    report.values = rank_by_value(report.values)
    return report


def load_games(
    *,
    from_json: str | None = None,
    raw: list[dict[str, Any]] | None = None,
    sport: str = "soccer_epl",
    regions: str = "eu,uk",
    markets: str = "h2h,totals",
) -> list[GameOdds]:
    """Obtém e faz o parsing dos jogos.

    Prioridade: ``raw`` (já em memória) > ``from_json`` (ficheiro local) >
    chamada ao The Odds API.
    """
    if raw is None:
        if from_json:
            with open(from_json, encoding="utf-8") as f:
                raw = json.load(f)
        else:
            raw = fetch_odds_the_odds_api(sport=sport, regions=regions, markets=markets)
    return parse_the_odds_api(raw)


CSV_HEADER = [
    "jogo", "mercado", "selecao", "melhor_odd", "casa", "odd_mediana",
    "prob_consenso", "odd_justa", "ev_pct", "ev_shin_pct", "ev_prop_pct",
    "metodos_confirmam", "n_casas", "dispersao_odds", "outlier", "avisos",
]


def _csv_row(v: ValueSelection) -> list[Any]:
    return [
        v.game, v.market, v.selection, f"{v.best_odds:.4f}", v.best_book,
        f"{v.median_odds:.4f}", f"{v.consensus_prob:.4f}", f"{v.fair_odds:.4f}",
        f"{v.ev_pct:.2f}", f"{v.ev_shin * 100:.2f}", f"{v.ev_proportional * 100:.2f}",
        v.agreement, v.n_books, f"{v.odds_dispersion:.4f}", int(v.is_outlier),
        " | ".join(v.warnings),
    ]


def values_to_csv(values: Sequence[ValueSelection]) -> str:
    """Serializa os resultados para uma string CSV (usada pela web app)."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(CSV_HEADER)
    for v in values:
        writer.writerow(_csv_row(v))
    return buf.getvalue()
