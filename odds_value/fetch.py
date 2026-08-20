"""Recolha de dados de fontes públicas e legítimas.

Fontes suportadas
-----------------
- **The Odds API** (https://the-odds-api.com): agrega odds de dezenas de
  casas por mercado (1X2/h2h, totals, BTTS). Tier gratuito. A chave é lida
  da variável de ambiente ``ODDS_API_KEY``.
- **API-Football** (https://www.api-football.com): forma recente, golos
  marcados/sofridos e resultados de eliminatórias. Chave em
  ``API_FOOTBALL_KEY``.

NENHUMA função aqui faz scraping de sites de casas de apostas. Só se usam as
APIs públicas oficiais, dentro dos seus termos de uso.

As respostas cruas são convertidas em estruturas :class:`GameOdds` /
:class:`MarketOdds` prontas para o pipeline de valor.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

import requests

from .devig import BookQuote
from .value import ContextFlags

ODDS_API_BASE = "https://api.the-odds-api.com/v4"
API_FOOTBALL_BASE = "https://v3.football.api-sports.io"

# Mapa The Odds API -> mercado interno. h2h = 1X2, totals = mais/menos golos.
MARKET_MAP = {
    "h2h": "1X2",
    "totals": "Totals (O/U)",
    "btts": "BTTS",
}

# Estádios/cidades acima de ~2000 m onde a altitude é fator relevante.
# (chave em minúsculas; usada para heurística de contexto)
HIGH_ALTITUDE_VENUES = {
    "la paz": 3640,
    "el alto": 4150,
    "potosi": 4067,
    "oruro": 3706,
    "cochabamba": 2558,
    "quito": 2850,
    "bogota": 2640,
    "cusco": 3399,
    "toluca": 2660,
    "pachuca": 2432,
    "puebla": 2135,
    "mexico city": 2240,
    "addis ababa": 2355,
}


class MissingApiKey(RuntimeError):
    """Levantada quando a variável de ambiente com a chave não existe."""


def _require_key(env_var: str) -> str:
    key = os.environ.get(env_var)
    if not key:
        raise MissingApiKey(
            f"Variável de ambiente {env_var} não definida. "
            f"Define-a com a tua chave de API (ver README)."
        )
    return key


@dataclass
class MarketOdds:
    """Odds de todas as casas para um mercado de um jogo."""

    market: str                 # nome interno do mercado (ex.: "1X2")
    selections: list[str]       # nomes das seleções, em ordem estável
    quotes: list[BookQuote]     # odds por casa, alinhadas com selections


@dataclass
class GameOdds:
    """Um jogo com todos os seus mercados e o contexto associado."""

    game: str                   # "Casa vs Fora"
    home: str
    away: str
    commence_time: str
    markets: list[MarketOdds] = field(default_factory=list)
    context: ContextFlags = field(default_factory=ContextFlags)


# --------------------------------------------------------------------------- #
# The Odds API
# --------------------------------------------------------------------------- #
def fetch_odds_the_odds_api(
    sport: str = "soccer_epl",
    regions: str = "eu,uk",
    markets: str = "h2h,totals",
    odds_format: str = "decimal",
    session: requests.Session | None = None,
    timeout: float = 20.0,
) -> list[dict[str, Any]]:
    """Chama o endpoint de odds do The Odds API e devolve o JSON cru.

    ``sport`` usa as chaves da API (ex.: ``soccer_epl``, ``soccer_uefa_champs_league``).
    Consulta ``/sports`` para a lista completa. ``markets`` aceita
    ``h2h,totals,btts`` conforme o desporto.
    """
    key = _require_key("ODDS_API_KEY")
    sess = session or requests.Session()
    url = f"{ODDS_API_BASE}/sports/{sport}/odds"
    params = {
        "apiKey": key,
        "regions": regions,
        "markets": markets,
        "oddsFormat": odds_format,
        "dateFormat": "iso",
    }
    resp = sess.get(url, params=params, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def parse_the_odds_api(raw_games: list[dict[str, Any]]) -> list[GameOdds]:
    """Converte o JSON do The Odds API em :class:`GameOdds`.

    Para cada mercado, alinha as odds de todas as casas na mesma ordem de
    seleções (a ordem é fixada pela primeira casa vista).
    """
    games: list[GameOdds] = []
    for g in raw_games:
        home = g.get("home_team", "")
        away = g.get("away_team", "")
        game_label = f"{home} vs {away}"

        # market_key -> (selections_order, {book: {selection: odd}})
        markets: dict[str, tuple[list[str], dict[str, dict[str, float]]]] = {}
        for book in g.get("bookmakers", []):
            book_key = book.get("key", "unknown")
            for mkt in book.get("markets", []):
                mkey = mkt.get("key")
                if mkey not in MARKET_MAP:
                    continue
                order, books = markets.setdefault(mkey, ([], {}))
                per_book: dict[str, float] = {}
                for outcome in mkt.get("outcomes", []):
                    name = _outcome_name(outcome, home, away)
                    price = outcome.get("price")
                    if price is None:
                        continue
                    per_book[name] = float(price)
                    if name not in order:
                        order.append(name)
                if per_book:
                    books[book_key] = per_book

        game = GameOdds(
            game=game_label,
            home=home,
            away=away,
            commence_time=g.get("commence_time", ""),
            context=infer_context(home, away),
        )
        for mkey, (order, books) in markets.items():
            quotes: list[BookQuote] = []
            for book_key, per_book in books.items():
                # só usa casas que cotaram TODAS as seleções (odds alinhadas)
                if all(sel in per_book for sel in order):
                    quotes.append(
                        BookQuote(bookmaker=book_key, odds=[per_book[s] for s in order])
                    )
            if len(quotes) >= 2 and len(order) >= 2:
                game.markets.append(
                    MarketOdds(market=MARKET_MAP[mkey], selections=order, quotes=quotes)
                )
        if game.markets:
            games.append(game)
    return games


def _outcome_name(outcome: dict[str, Any], home: str, away: str) -> str:
    """Normaliza o nome de uma seleção (inclui a linha em totals)."""
    name = outcome.get("name", "")
    point = outcome.get("point")
    if point is not None:
        return f"{name} {point}"
    return name


# --------------------------------------------------------------------------- #
# API-Football (complemento: forma, golos, eliminatórias)
# --------------------------------------------------------------------------- #
def fetch_team_form_api_football(
    team_id: int,
    last: int = 5,
    session: requests.Session | None = None,
    timeout: float = 20.0,
) -> dict[str, Any]:
    """Últimos ``last`` jogos de uma equipa (forma, golos marcados/sofridos)."""
    key = _require_key("API_FOOTBALL_KEY")
    sess = session or requests.Session()
    url = f"{API_FOOTBALL_BASE}/fixtures"
    params = {"team": team_id, "last": last}
    headers = {"x-apisports-key": key}
    resp = sess.get(url, params=params, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def summarize_form(api_football_fixtures: dict[str, Any], team_id: int) -> dict[str, float]:
    """Resume forma recente a partir da resposta de /fixtures da API-Football."""
    goals_for = goals_against = played = wins = 0
    for fx in api_football_fixtures.get("response", []):
        teams = fx.get("teams", {})
        goals = fx.get("goals", {})
        is_home = teams.get("home", {}).get("id") == team_id
        gf = goals.get("home") if is_home else goals.get("away")
        ga = goals.get("away") if is_home else goals.get("home")
        if gf is None or ga is None:
            continue
        played += 1
        goals_for += gf
        goals_against += ga
        if gf > ga:
            wins += 1
    if played == 0:
        return {"played": 0, "gf_avg": 0.0, "ga_avg": 0.0, "win_rate": 0.0}
    return {
        "played": played,
        "gf_avg": goals_for / played,
        "ga_avg": goals_against / played,
        "win_rate": wins / played,
    }


# --------------------------------------------------------------------------- #
# Heurísticas de contexto
# --------------------------------------------------------------------------- #
def infer_context(
    home: str,
    away: str,
    venue: str | None = None,
    is_second_leg: bool = False,
    special_conditions: str = "",
) -> ContextFlags:
    """Deriva flags de contexto a partir de metadados disponíveis.

    A deteção de altitude usa o nome do clube/cidade da equipa da casa ou o
    ``venue`` explícito. A 2ª mão de eliminatória tem de ser passada
    explicitamente (``is_second_leg``) porque o The Odds API não a expõe.
    """
    haystack = f"{home} {venue or ''}".lower()
    high_alt = any(city in haystack for city in HIGH_ALTITUDE_VENUES)
    return ContextFlags(
        second_leg_knockout=is_second_leg,
        high_altitude=high_alt,
        special_conditions=special_conditions,
    )
