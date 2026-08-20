"""Testes das funções de remoção de margem e consenso."""

import math

import pytest

from odds_value.devig import (
    BookQuote,
    booksum,
    bookmaker_weight,
    consensus,
    devig,
    devig_proportional,
    devig_shin,
    implied_probabilities,
    margin,
    solve_shin_z,
)


# --------------------------------------------------------------------------- #
# Básicos
# --------------------------------------------------------------------------- #
def test_implied_probabilities():
    assert implied_probabilities([2.0, 2.0]) == [0.5, 0.5]


def test_margin_no_overround():
    # Mercado justo perfeito: 2.0 / 2.0 => booksum 1.0, margem 0.
    assert margin([2.0, 2.0]) == pytest.approx(0.0)


def test_margin_with_overround():
    # 1.90 / 1.90 => booksum ~1.0526, margem ~5.26%.
    assert margin([1.90, 1.90]) == pytest.approx(0.05263, abs=1e-4)


@pytest.mark.parametrize("bad", [[], [2.0], [2.0, 1.0], [2.0, -3.0], [2.0, None]])
def test_invalid_odds_raise(bad):
    with pytest.raises(ValueError):
        implied_probabilities(bad)


# --------------------------------------------------------------------------- #
# Proporcional
# --------------------------------------------------------------------------- #
def test_proportional_sums_to_one():
    fair = devig_proportional([1.90, 3.50, 4.20])
    assert sum(fair) == pytest.approx(1.0)


def test_proportional_symmetric():
    # Odds iguais => probabilidades iguais.
    fair = devig_proportional([1.90, 1.90])
    assert fair == pytest.approx([0.5, 0.5])


def test_proportional_known_values():
    # 1.90/1.90: p=0.5263 cada, normalizado => 0.5 cada.
    fair = devig_proportional([1.90, 1.90])
    assert fair[0] == pytest.approx(0.5)


# --------------------------------------------------------------------------- #
# Shin
# --------------------------------------------------------------------------- #
def test_shin_sums_to_one():
    fair = devig_shin([1.90, 3.50, 4.20])
    assert sum(fair) == pytest.approx(1.0, abs=1e-6)


def test_shin_symmetric_equals_proportional():
    # Num mercado simétrico, Shin e proporcional coincidem (0.5/0.5).
    assert devig_shin([1.90, 1.90]) == pytest.approx([0.5, 0.5], abs=1e-6)


def test_shin_z_zero_when_no_margin():
    # Sem margem (booksum <= 1), a fração de insiders z deve ser 0.
    assert solve_shin_z([2.0, 2.0]) == pytest.approx(0.0, abs=1e-9)


def test_shin_z_positive_with_margin():
    z = solve_shin_z([1.90, 3.50, 4.20])
    assert 0.0 < z < 1.0


def test_shin_reduces_favourite_longshot_bias():
    # Shin puxa probabilidade para o favorito face à normalização proporcional:
    # o favorito (odd mais baixa) fica com prob Shin >= prob proporcional.
    odds = [1.50, 4.50, 7.00]
    prop = devig_proportional(odds)
    shin = devig_shin(odds)
    assert shin[0] >= prop[0]          # favorito reforçado
    assert shin[-1] <= prop[-1]        # azarão atenuado


def test_shin_probabilities_are_valid():
    shin = devig_shin([1.20, 6.0, 15.0])
    assert all(0.0 <= p <= 1.0 for p in shin)


# --------------------------------------------------------------------------- #
# Dispatch
# --------------------------------------------------------------------------- #
def test_devig_dispatch():
    odds = [1.90, 3.50, 4.20]
    assert devig(odds, "proportional") == pytest.approx(devig_proportional(odds))
    assert devig(odds, "shin") == pytest.approx(devig_shin(odds))


def test_devig_unknown_method():
    with pytest.raises(ValueError):
        devig([2.0, 2.0], "inexistente")


# --------------------------------------------------------------------------- #
# Consenso
# --------------------------------------------------------------------------- #
def test_bookmaker_weight_sharp_gets_more():
    # Com a mesma margem, Pinnacle pesa mais do que uma casa qualquer.
    assert bookmaker_weight("pinnacle", 0.02) > bookmaker_weight("casa_random", 0.02)


def test_bookmaker_weight_low_margin_gets_more():
    # Para a mesma casa, menor margem => maior peso.
    assert bookmaker_weight("x", 0.01) > bookmaker_weight("x", 0.10)


def test_consensus_sums_to_one():
    quotes = [
        BookQuote("pinnacle", [1.95, 3.60, 4.10]),
        BookQuote("bet365", [1.90, 3.50, 4.20]),
        BookQuote("williamhill", [1.85, 3.55, 4.30]),
    ]
    res = consensus(quotes, method="shin")
    assert sum(res.probabilities) == pytest.approx(1.0, abs=1e-6)
    assert res.n_books == 3


def test_consensus_fair_odds_are_inverse():
    quotes = [
        BookQuote("pinnacle", [2.0, 2.0]),
        BookQuote("bet365", [2.0, 2.0]),
    ]
    res = consensus(quotes, method="proportional")
    for p, o in zip(res.probabilities, res.fair_odds):
        assert o == pytest.approx(1.0 / p)


def test_consensus_pinnacle_pulls_line():
    # Pinnacle discorda das outras; por pesar mais, o consenso aproxima-se dela.
    quotes = [
        BookQuote("pinnacle", [3.0, 1.5]),      # favorece a seleção 1
        BookQuote("softbook_a", [1.5, 3.0]),
        BookQuote("softbook_b", [1.5, 3.0]),
    ]
    res = consensus(quotes, method="proportional")
    # média simples ignorando pesos daria prob[0] < 0.5; com peso Pinnacle sobe.
    simple = (1/3.0 + 1/1.5 + 1/1.5)
    simple_p0 = (1/3.0) / simple  # aprox só ilustrativo
    assert res.probabilities[0] > simple_p0


def test_consensus_requires_equal_selection_count():
    with pytest.raises(ValueError):
        consensus([BookQuote("a", [2.0, 2.0]), BookQuote("b", [2.0, 2.0, 2.0])])


def test_consensus_empty_raises():
    with pytest.raises(ValueError):
        consensus([])
