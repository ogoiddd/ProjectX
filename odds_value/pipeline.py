"""Pipeline partilhado: recolha → parsing → análise de valor.

Usado tanto pela CLI (:mod:`odds_value.cli`) como pela web app
(:mod:`odds_value.web`), para não duplicar lógica.
"""

from __future__ import annotations

import csv
import io
import json
from typing import Any, Sequence

from .fetch import GameOdds, fetch_odds_the_odds_api, parse_the_odds_api
from .value import (
    DEFAULT_EV_THRESHOLD,
    ContextFlags,
    ValueSelection,
    analyze_market,
    rank_by_value,
)


def analyze_games(
    games: Sequence[GameOdds],
    method: str = "shin",
    ev_threshold: float = DEFAULT_EV_THRESHOLD,
) -> tuple[list[ValueSelection], int]:
    """Corre a análise de valor sobre todos os jogos.

    Devolve ``(valores_ordenados_por_ev, nº_mercados_analisados)``.
    """
    all_values: list[ValueSelection] = []
    markets_analyzed = 0
    for g in games:
        for mkt in g.markets:
            markets_analyzed += 1
            ctx = ContextFlags(
                second_leg_knockout=g.context.second_leg_knockout,
                high_altitude=g.context.high_altitude,
                special_conditions=g.context.special_conditions,
                combined_market="+" in mkt.market or "&" in mkt.market,
            )
            all_values.extend(
                analyze_market(
                    game=g.game,
                    market=mkt.market,
                    selections=mkt.selections,
                    quotes=mkt.quotes,
                    context=ctx,
                    method=method,
                    ev_threshold=ev_threshold,
                )
            )
    return rank_by_value(all_values), markets_analyzed


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
    "jogo", "mercado", "selecao", "melhor_odd", "casa",
    "prob_consenso", "odd_justa", "ev_pct", "n_casas",
    "dispersao_odds", "outlier", "avisos",
]


def _csv_row(v: ValueSelection) -> list[Any]:
    return [
        v.game, v.market, v.selection, f"{v.best_odds:.4f}", v.best_book,
        f"{v.consensus_prob:.4f}", f"{v.fair_odds:.4f}", f"{v.ev_pct:.2f}",
        v.n_books, f"{v.odds_dispersion:.4f}", int(v.is_outlier),
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
