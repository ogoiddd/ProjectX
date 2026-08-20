"""Ferramenta de análise de valor em odds de futebol.

Módulos:
- :mod:`odds_value.fetch`  — recolha de dados (The Odds API, API-Football).
- :mod:`odds_value.devig`  — remoção de margem e linha de consenso.
- :mod:`odds_value.value`  — EV%, dispersão e filtros de contexto.
- :mod:`odds_value.cli`    — interface de linha de comandos (tabela + CSV).
"""

from .devig import (
    BookQuote,
    consensus,
    devig,
    devig_proportional,
    devig_shin,
    margin,
)
from .value import ContextFlags, ValueSelection, analyze_market, rank_by_value

__all__ = [
    "BookQuote",
    "ContextFlags",
    "ValueSelection",
    "analyze_market",
    "consensus",
    "devig",
    "devig_proportional",
    "devig_shin",
    "margin",
    "rank_by_value",
]

__version__ = "0.1.0"
