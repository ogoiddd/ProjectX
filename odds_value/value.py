"""Deteção de valor: EV%, dispersão entre casas e filtros de contexto.

O fluxo é: para cada mercado de um jogo,
1. calcular a probabilidade de consenso (:mod:`odds_value.devig`) com AMBOS os
   métodos de devig (Shin e proporcional);
2. comparar a melhor odd de cada seleção com essa probabilidade;
3. sinalizar EV positivo, medir a dispersão entre casas e anexar avisos de
   contexto (segunda mão de eliminatória, altitude, mercados combinados...).

Filtros de fiabilidade aplicados:
- **Poucas casas** — mercados com menos de ``min_books`` (5 por omissão) são
  descartados: o consenso é frágil.
- **Cauda de baixa probabilidade** — seleções com prob. de consenso abaixo de
  ``min_prob`` (10% por omissão) são ignoradas: o devig é menos fiável nos
  extremos e o EV fica muito sensível a erros de vírgula.
- **Concordância entre métodos** — o sinal é comparado sob Shin e proporcional;
  sinais que só aparecem num dos métodos são marcados como menos robustos.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from typing import Sequence

from .devig import BookQuote, consensus

# Limite mínimo de EV para sinalizar uma seleção como valor (+2%).
DEFAULT_EV_THRESHOLD = 0.02

# Nº mínimo de casas para um mercado ser considerado (abaixo disto, descarta-se).
MIN_BOOKS = 5

# Probabilidade de consenso mínima; abaixo disto o devig é pouco fiável.
MIN_CONSENSUS_PROB = 0.10

# Acima deste desvio relativo ao consenso, a melhor odd é "outlier":
# pode ser valor genuíno ou um erro/linha desatualizada da casa.
OUTLIER_ODDS_RATIO = 0.15  # 15% acima da odd justa

METHODS = ("shin", "proportional")
_METHOD_LABEL = {"shin": "Shin", "proportional": "Proporcional"}


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
    """Uma seleção avaliada, com a melhor odd, a mediana e o seu EV.

    O EV é calculado sob os dois métodos de devig. ``ev`` é o do método
    primário (o escolhido pelo utilizador); ``ev_shin`` / ``ev_proportional``
    permitem a comparação lado a lado, e ``flagged_by`` diz que métodos
    ultrapassam o limite de EV.
    """

    game: str
    market: str
    selection: str
    best_odds: float
    best_book: str
    median_odds: float              # odd mediana entre TODAS as casas
    consensus_prob: float           # prob. de consenso do método primário
    fair_odds: float                # odd justa do método primário
    ev: float                       # EV fracionário do método primário
    ev_shin: float
    ev_proportional: float
    flagged_by: list[str]           # métodos com EV >= limite (subconjunto de METHODS)
    n_books: int
    odds_dispersion: float          # desvio-padrão das odds entre casas
    is_outlier: bool                # melhor odd muito acima do resto
    section: str = "actionable"     # "actionable" (whitelist) ou "reference"
    warnings: list[str] = field(default_factory=list)

    @property
    def ev_pct(self) -> float:
        return self.ev * 100.0

    @property
    def is_actionable(self) -> bool:
        return self.section == "actionable"

    @property
    def best_ev(self) -> float:
        """Maior EV entre os dois métodos (usado para ordenar/sinalizar)."""
        return max(self.ev_shin, self.ev_proportional)

    @property
    def agreement(self) -> str:
        """Rótulo de concordância: 'ambos', 'só Shin' ou 'só Proporcional'."""
        if len(self.flagged_by) == len(METHODS):
            return "ambos"
        if len(self.flagged_by) == 1:
            return f"só {_METHOD_LABEL[self.flagged_by[0]]}"
        return "nenhum"

    @property
    def has_value(self) -> bool:
        return bool(self.flagged_by)


def expected_value(odds: float, prob: float) -> float:
    """EV fracionário: ``(odd * prob) - 1``. +0.05 = +5% de valor esperado."""
    return odds * prob - 1.0


@dataclass
class MarketResult:
    """Resultado da análise de um mercado.

    - ``values``: seleções com valor (EV >= limite em pelo menos um método).
    - ``best_books``: a casa com a melhor odd em CADA seleção (mesmo sem valor
      e mesmo nas seleções filtradas), para estatística de outliers por casa.
    - ``discarded_few_books``: True se o mercado foi descartado por ter poucas
      casas (< ``min_books``).
    """

    game: str
    market: str
    n_books: int
    values: list[ValueSelection] = field(default_factory=list)
    best_books: list[str] = field(default_factory=list)
    discarded_few_books: bool = False


def normalize_whitelist(books: Sequence[str] | str | None) -> set[str] | None:
    """Normaliza a whitelist de casas. Devolve ``None`` se não houver whitelist.

    Aceita uma string separada por vírgulas ou uma sequência de nomes.
    """
    if books is None:
        return None
    if isinstance(books, str):
        books = books.split(",")
    tokens = {b.strip().lower() for b in books if b and b.strip()}
    return tokens or None


def book_in_whitelist(bookmaker: str, whitelist: set[str] | None) -> bool:
    """True se ``bookmaker`` corresponde à whitelist (ou se não há whitelist).

    A correspondência é tolerante: ``betfair`` casa com ``betfair_ex_eu`` e
    vice-versa (comparação por inclusão, sem distinção de maiúsculas).
    """
    if not whitelist:
        return True
    b = bookmaker.lower()
    return any(t == b or t in b or b in t for t in whitelist)


def analyze_market(
    game: str,
    market: str,
    selections: Sequence[str],
    quotes: Sequence[BookQuote],
    context: ContextFlags | None = None,
    method: str = "shin",
    ev_threshold: float = DEFAULT_EV_THRESHOLD,
    min_books: int = MIN_BOOKS,
    min_prob: float = MIN_CONSENSUS_PROB,
    whitelist: Sequence[str] | str | None = None,
) -> MarketResult:
    """Avalia todas as seleções de um mercado.

    ``quotes`` são as odds de cada casa para as ``selections`` (mesma ordem).
    ``method`` é o método primário (o que preenche as colunas principais);
    o outro é sempre calculado para comparação.

    ``whitelist``: casas onde o utilizador pode apostar. TODAS as casas entram
    no consenso, mas só as da whitelist geram sinais "acionáveis"; o valor
    encontrado nas restantes é marcado como "referência" (útil só para calibrar
    o consenso). Sem whitelist, tudo é considerado acionável.
    """
    context = context or ContextFlags()
    n_books = len(quotes)

    # (3) Descarta mercados com poucas casas — consenso pouco fiável.
    if n_books < min_books:
        return MarketResult(
            game=game, market=market, n_books=n_books, discarded_few_books=True,
        )

    if method not in METHODS:
        method = "shin"
    alt = "proportional" if method == "shin" else "shin"
    wl = normalize_whitelist(whitelist)

    # Consenso usa SEMPRE todas as casas (mais dados = melhor estimativa).
    con = {m: consensus(quotes, method=m) for m in METHODS}
    con_primary = con[method]
    warnings = context.warnings()

    result = MarketResult(game=game, market=market, n_books=n_books)
    for i, sel in enumerate(selections):
        pairs = [(q.bookmaker, q.odds[i]) for q in quotes]   # (casa, odd) todas
        col = [o for _, o in pairs]
        overall_best = max(pairs, key=lambda p: p[1])

        # (4) Estatística por casa usa a melhor odd global (independente da whitelist).
        result.best_books.append(overall_best[0])

        prob = con_primary.probabilities[i]
        fair = con_primary.fair_odds[i]

        # (1) Filtra a cauda de baixa probabilidade (devig pouco fiável).
        if prob < min_prob:
            continue

        median_odds = statistics.median(col)
        dispersion = statistics.pstdev(col) if len(col) > 1 else 0.0

        def _make(book: str, odds: float, section: str) -> ValueSelection | None:
            ev_by_method = {
                m: expected_value(odds, con[m].probabilities[i]) for m in METHODS
            }
            flagged_by = [m for m in METHODS if ev_by_method[m] >= ev_threshold]
            if not flagged_by:
                return None

            is_outlier = fair > 0 and (odds / fair - 1.0) >= OUTLIER_ODDS_RATIO
            sel_warnings = list(warnings)
            if is_outlier:
                sel_warnings.append(
                    f"Melhor odd ({odds:.2f}) está {odds / fair - 1.0:+.0%} acima da "
                    f"odd justa ({fair:.2f}): pode ser valor OU erro/informação em "
                    "falta na casa. Confirmar antes de apostar."
                )
            # (2) Sinal confirmado por um só método é menos robusto.
            if len(flagged_by) == 1:
                only = _METHOD_LABEL[flagged_by[0]]
                other = _METHOD_LABEL[alt if flagged_by[0] == method else method]
                sel_warnings.append(
                    f"Sinal só confirmado pelo método {only}; o método {other} não o "
                    "marca como valor — menos robusto."
                )
            return ValueSelection(
                game=game, market=market, selection=sel,
                best_odds=odds, best_book=book, median_odds=median_odds,
                consensus_prob=prob, fair_odds=fair,
                ev=ev_by_method[method], ev_shin=ev_by_method["shin"],
                ev_proportional=ev_by_method["proportional"], flagged_by=flagged_by,
                n_books=n_books, odds_dispersion=dispersion, is_outlier=is_outlier,
                section=section, warnings=sel_warnings,
            )

        # Melhor odd DENTRO da whitelist (acionável) e FORA dela (referência).
        wl_pairs = [(b, o) for b, o in pairs if book_in_whitelist(b, wl)]
        rest_pairs = [(b, o) for b, o in pairs if not book_in_whitelist(b, wl)]

        if wl_pairs:
            b, o = max(wl_pairs, key=lambda p: p[1])
            vs = _make(b, o, "actionable")
            if vs:
                result.values.append(vs)
        # Só há secção "referência" quando existe whitelist a definir "as outras".
        if wl and rest_pairs:
            b, o = max(rest_pairs, key=lambda p: p[1])
            vs = _make(b, o, "reference")
            if vs:
                result.values.append(vs)
    return result


def rank_by_value(selections: Sequence[ValueSelection]) -> list[ValueSelection]:
    """Ordena por magnitude de EV (maior primeiro), pelo melhor dos dois métodos."""
    return sorted(selections, key=lambda s: s.best_ev, reverse=True)
