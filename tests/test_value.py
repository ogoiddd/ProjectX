"""Testes da deteção de valor (EV, outliers, contexto)."""

import pytest

from odds_value.devig import BookQuote
from odds_value.value import (
    ContextFlags,
    analyze_market,
    expected_value,
    rank_by_value,
)


def test_expected_value():
    # odd 2.0 numa prob 0.55 => EV +10%.
    assert expected_value(2.0, 0.55) == pytest.approx(0.10)


def test_no_value_when_odds_match_consensus():
    quotes = [
        BookQuote("pinnacle", [2.0, 2.0]),
        BookQuote("bet365", [2.0, 2.0]),
    ]
    res = analyze_market("A vs B", "1X2", ["A", "B"], quotes)
    assert res == []


def test_value_detected_for_outlier_book():
    # Uma casa oferece 2.60 numa seleção que o consenso avalia ~0.5 (justa 2.0).
    quotes = [
        BookQuote("pinnacle", [2.0, 2.0]),
        BookQuote("bet365", [2.0, 2.0]),
        BookQuote("softbook", [2.60, 1.55]),
    ]
    res = analyze_market("A vs B", "1X2", ["A", "B"], quotes, method="proportional")
    found = [v for v in res if v.selection == "A"]
    assert found and found[0].ev > 0
    assert found[0].best_book == "softbook"
    assert found[0].is_outlier


def test_combined_market_warning_propagates():
    quotes = [
        BookQuote("pinnacle", [2.5, 2.5, 3.0]),
        BookQuote("bet365", [2.5, 2.5, 3.0]),
        BookQuote("softbook", [3.2, 2.3, 2.9]),  # outlier em X gera EV positivo
    ]
    ctx = ContextFlags(combined_market=True)
    res = analyze_market("A vs B", "Resultado+Golos", ["X", "Y", "Z"], quotes, context=ctx)
    assert any("combinado" in w.lower() for v in res for w in v.warnings)


def test_rank_by_value_orders_desc():
    quotes = [
        BookQuote("pinnacle", [2.0, 2.0]),
        BookQuote("soft", [2.40, 1.70]),
    ]
    res = analyze_market("A vs B", "1X2", ["A", "B"], quotes, method="proportional")
    ranked = rank_by_value(res)
    assert ranked == sorted(ranked, key=lambda v: v.ev, reverse=True)
