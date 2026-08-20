"""Remoção de margem (overround) e cálculo da linha de consenso.

Este módulo é puramente numérico — não depende de rede nem de I/O — para
poder ser testado de forma isolada e determinística.

Definições
----------
- odd decimal ``o``: pagamento total por unidade apostada (inclui o stake).
- probabilidade implícita ``p = 1 / o``: inclui a margem da casa.
- booksum / overround ``B = sum(p_i)``: para um mercado equilibrado B > 1;
  o excesso ``B - 1`` é a margem bruta da casa.

Dois métodos de "devig" (remoção de margem) são implementados e comparáveis:

1. **Normalização proporcional** — assume que a margem está distribuída
   proporcionalmente à probabilidade de cada seleção. Simples e robusto,
   mas enviesa contra os favoritos (subestima favoritos, sobrestima
   azarões) porque na prática as casas carregam mais margem nos azarões
   (favourite-longshot bias).

2. **Método de Shin (1993)** — modela a margem como resultado de uma fração
   ``z`` de apostadores informados ("insider trading"). Corrige parte do
   favourite-longshot bias e costuma aproximar-se melhor das probabilidades
   verdadeiras, sobretudo em mercados de 2-3 seleções.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


# --------------------------------------------------------------------------- #
# Utilidades básicas
# --------------------------------------------------------------------------- #
def implied_probabilities(odds: Sequence[float]) -> list[float]:
    """Converte odds decimais em probabilidades implícitas (com margem)."""
    _validate_odds(odds)
    return [1.0 / o for o in odds]


def booksum(odds: Sequence[float]) -> float:
    """Soma das probabilidades implícitas (overround). >1 num mercado normal."""
    return sum(implied_probabilities(odds))


def margin(odds: Sequence[float]) -> float:
    """Margem bruta da casa: ``booksum - 1`` (ex.: 0.05 = 5%)."""
    return booksum(odds) - 1.0


def _validate_odds(odds: Sequence[float]) -> None:
    if len(odds) < 2:
        raise ValueError("Um mercado precisa de pelo menos 2 seleções.")
    for o in odds:
        if o is None or o <= 1.0:
            raise ValueError(f"Odd decimal inválida: {o!r} (tem de ser > 1.0).")


# --------------------------------------------------------------------------- #
# Método 1: normalização proporcional
# --------------------------------------------------------------------------- #
def devig_proportional(odds: Sequence[float]) -> list[float]:
    """Remove a margem escalando as probabilidades implícitas para somarem 1.

    ``fair_i = p_i / sum(p)``. As probabilidades resultantes somam
    exatamente 1 (a menos de erro de vírgula flutuante).
    """
    probs = implied_probabilities(odds)
    total = sum(probs)
    return [p / total for p in probs]


# --------------------------------------------------------------------------- #
# Método 2: Shin (1993)
# --------------------------------------------------------------------------- #
def _shin_probabilities(probs: Sequence[float], z: float) -> list[float]:
    """Probabilidades de Shin para um dado ``z`` (não necessariamente somam 1)."""
    b = sum(probs)
    out = []
    for p in probs:
        # pi = (sqrt(z^2 + 4(1-z) * p^2 / B) - z) / (2(1-z))
        root = (z * z + 4.0 * (1.0 - z) * (p * p) / b) ** 0.5
        out.append((root - z) / (2.0 * (1.0 - z)))
    return out


def solve_shin_z(odds: Sequence[float], tol: float = 1e-10, max_iter: int = 200) -> float:
    """Resolve, por bisseção, o ``z`` tal que as probabilidades de Shin somam 1.

    ``z`` é a fração estimada de dinheiro informado. Em ``z = 0`` a soma das
    probabilidades de Shin vale ``sqrt(booksum) >= 1``; aumentar ``z`` baixa
    a soma monotonicamente, pelo que existe uma raiz única em [0, 1).
    """
    probs = implied_probabilities(odds)

    def sum_at(z: float) -> float:
        return sum(_shin_probabilities(probs, z))

    lo, hi = 0.0, 0.9999
    # Se nem sequer há margem (booksum <= 1), z = 0 é a resposta.
    if sum_at(lo) <= 1.0 + tol:
        return 0.0
    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        s = sum_at(mid)
        if abs(s - 1.0) < tol:
            return mid
        # soma decresce com z: se soma>1, precisamos de mais z
        if s > 1.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def devig_shin(odds: Sequence[float]) -> list[float]:
    """Remove a margem pelo método de Shin. As probabilidades somam ~1."""
    z = solve_shin_z(odds)
    probs = implied_probabilities(odds)
    fair = _shin_probabilities(probs, z)
    # Renormaliza para blindar contra erro numérico residual do solver.
    total = sum(fair)
    return [f / total for f in fair]


def devig(odds: Sequence[float], method: str = "proportional") -> list[float]:
    """Interface única de devig. ``method`` em {"proportional", "shin"}."""
    if method == "proportional":
        return devig_proportional(odds)
    if method == "shin":
        return devig_shin(odds)
    raise ValueError(f"Método de devig desconhecido: {method!r}")


# --------------------------------------------------------------------------- #
# Consenso entre casas
# --------------------------------------------------------------------------- #
# Casas consideradas "afiadas" (margens baixas, limites altos). A odd destas
# casas é a referência de mercado mais fiável, por isso recebe mais peso.
SHARP_BOOKS: dict[str, float] = {
    "pinnacle": 3.0,
    "betfair_ex_eu": 2.0,   # exchange (back)
    "betfair_ex_uk": 2.0,
    "matchbook": 1.6,
    "smarkets": 1.6,
}
DEFAULT_SHARP_WEIGHT = 1.0


@dataclass
class BookQuote:
    """Odds de uma casa para um conjunto de seleções (mesma ordem em todo o mercado)."""

    bookmaker: str          # chave da casa (ex.: "pinnacle")
    odds: list[float]       # odds decimais, uma por seleção


@dataclass
class ConsensusResult:
    """Resultado do consenso para um mercado."""

    probabilities: list[float]   # probabilidade de consenso por seleção (soma 1)
    fair_odds: list[float]       # odd justa = 1 / prob de consenso
    n_books: int                 # nº de casas usadas
    method: str                  # método de devig aplicado


def bookmaker_weight(bookmaker: str, book_margin: float) -> float:
    """Peso de uma casa no consenso.

    Combina dois sinais:
    - reputação de casa afiada (Pinnacle & exchanges pesam mais);
    - margem observada — quanto menor a margem, mais afiada a linha, logo
      mais peso (peso ∝ 1 / (1 + margem)).
    """
    sharp = SHARP_BOOKS.get(bookmaker.lower(), DEFAULT_SHARP_WEIGHT)
    # margem pode ser ligeiramente negativa em exchanges; protege o denominador.
    margin_factor = 1.0 / (1.0 + max(book_margin, 0.0))
    return sharp * margin_factor


def consensus(
    quotes: Sequence[BookQuote],
    method: str = "shin",
) -> ConsensusResult:
    """Linha de consenso: média ponderada das probabilidades sem margem.

    Cada casa é primeiro "devigada" com ``method``; depois faz-se a média
    ponderada por :func:`bookmaker_weight`. O resultado é renormalizado para
    somar 1 e convertido em odds justas.
    """
    if not quotes:
        raise ValueError("Sem cotações para calcular consenso.")

    n_sel = len(quotes[0].odds)
    if any(len(q.odds) != n_sel for q in quotes):
        raise ValueError("Todas as casas têm de cotar o mesmo nº de seleções.")

    acc = [0.0] * n_sel
    weight_total = 0.0
    for q in quotes:
        fair = devig(q.odds, method=method)
        w = bookmaker_weight(q.bookmaker, margin(q.odds))
        for i, p in enumerate(fair):
            acc[i] += w * p
        weight_total += w

    probs = [a / weight_total for a in acc]
    # Renormaliza (a média ponderada de vetores que somam 1 já soma 1, mas
    # protege contra acumulação de erro).
    total = sum(probs)
    probs = [p / total for p in probs]
    fair_odds = [1.0 / p if p > 0 else float("inf") for p in probs]
    return ConsensusResult(
        probabilities=probs,
        fair_odds=fair_odds,
        n_books=len(quotes),
        method=method,
    )
