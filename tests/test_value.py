"""Testes da deteção de valor (EV, filtros, comparação de métodos, stats)."""

import pytest

from odds_value.devig import BookQuote
from odds_value.pipeline import analyze_games, values_to_csv
from odds_value.value import (
    ContextFlags,
    analyze_market,
    book_in_whitelist,
    expected_value,
    normalize_whitelist,
    rank_by_value,
)
from odds_value.fetch import GameOdds, MarketOdds


def _books(rows):
    """Ajuda: lista de (nome, [odds]) -> lista de BookQuote."""
    return [BookQuote(name, odds) for name, odds in rows]


def test_expected_value():
    # odd 2.0 numa prob 0.55 => EV +10%.
    assert expected_value(2.0, 0.55) == pytest.approx(0.10)


def test_no_value_when_odds_match_consensus():
    quotes = _books([
        ("pinnacle", [2.0, 2.0]), ("bet365", [2.0, 2.0]), ("williamhill", [2.0, 2.0]),
        ("unibet", [2.0, 2.0]), ("betfair_ex_eu", [2.0, 2.0]),
    ])
    res = analyze_market("A vs B", "1X2", ["A", "B"], quotes)
    assert res.values == []
    assert res.n_books == 5
    assert not res.discarded_few_books


def test_value_detected_for_outlier_book():
    quotes = _books([
        ("pinnacle", [2.0, 2.0]), ("bet365", [2.0, 2.0]), ("williamhill", [2.0, 2.0]),
        ("unibet", [2.0, 2.0]), ("softbook", [2.60, 1.55]),
    ])
    res = analyze_market("A vs B", "1X2", ["A", "B"], quotes, method="proportional")
    found = [v for v in res.values if v.selection == "A"]
    assert found and found[0].ev > 0
    assert found[0].best_book == "softbook"
    assert found[0].is_outlier


# --- (3) descartar mercados com menos de 5 casas -------------------------- #
def test_market_discarded_with_few_books():
    quotes = _books([("pinnacle", [2.6, 2.0]), ("bet365", [2.0, 2.0])])
    res = analyze_market("A vs B", "1X2", ["A", "B"], quotes)
    assert res.discarded_few_books
    assert res.values == []


def test_min_books_configurable():
    quotes = _books([("pinnacle", [2.6, 2.0]), ("bet365", [2.0, 2.0])])
    res = analyze_market("A vs B", "1X2", ["A", "B"], quotes, min_books=2,
                         method="proportional")
    assert not res.discarded_few_books


# --- (1) filtrar seleções com prob de consenso < 10% ---------------------- #
def test_low_probability_selection_is_filtered():
    # Azarão extremo (odd ~26 => prob ~3.8%): abaixo de 10%, deve ser ignorado
    # mesmo que a melhor odd sugira EV positivo.
    quotes = _books([
        ("pinnacle", [1.05, 26.0]), ("bet365", [1.05, 25.0]),
        ("williamhill", [1.05, 27.0]), ("unibet", [1.05, 24.0]),
        ("softbook", [1.05, 40.0]),   # outlier no azarão
    ])
    res = analyze_market("A vs B", "1X2", ["Favorito", "Azarao"], quotes,
                         method="proportional")
    assert all(v.selection != "Azarao" for v in res.values)


def test_low_prob_still_counted_in_best_books():
    # A seleção filtrada continua a contar para a estatística por casa.
    quotes = _books([
        ("pinnacle", [1.05, 26.0]), ("bet365", [1.05, 25.0]),
        ("williamhill", [1.05, 27.0]), ("unibet", [1.05, 24.0]),
        ("softbook", [1.05, 40.0]),
    ])
    res = analyze_market("A vs B", "1X2", ["Favorito", "Azarao"], quotes)
    # duas seleções => dois registos de melhor-casa
    assert len(res.best_books) == 2
    assert "softbook" in res.best_books   # melhor odd no azarão


# --- (2) comparação Shin vs proporcional ---------------------------------- #
def test_flagged_by_records_both_methods():
    quotes = _books([
        ("pinnacle", [2.0, 2.0]), ("bet365", [2.0, 2.0]), ("williamhill", [2.0, 2.0]),
        ("unibet", [2.0, 2.0]), ("softbook", [2.60, 1.55]),
    ])
    res = analyze_market("A vs B", "1X2", ["A", "B"], quotes)
    v = next(v for v in res.values if v.selection == "A")
    assert set(v.flagged_by) <= {"shin", "proportional"}
    assert v.ev_shin != 0.0 and v.ev_proportional != 0.0
    if len(v.flagged_by) == 1:
        assert "menos robusto" in " ".join(v.warnings).lower()
        assert v.agreement.startswith("só")
    else:
        assert v.agreement == "ambos"


# --- (5) mediana e desvio ------------------------------------------------- #
def test_median_and_dispersion_present():
    quotes = _books([
        ("a", [2.0, 2.0]), ("b", [2.1, 1.95]), ("c", [1.9, 2.05]),
        ("d", [2.0, 2.0]), ("e", [2.60, 1.55]),
    ])
    res = analyze_market("A vs B", "1X2", ["A", "B"], quotes, method="proportional")
    v = next(v for v in res.values if v.selection == "A")
    assert v.median_odds == pytest.approx(2.0)      # mediana de [2.0,2.1,1.9,2.0,2.6]
    assert v.best_odds == 2.60
    assert v.odds_dispersion > 0


def test_combined_market_warning_propagates():
    quotes = _books([
        ("pinnacle", [2.5, 2.5, 3.0]), ("bet365", [2.5, 2.5, 3.0]),
        ("williamhill", [2.5, 2.5, 3.0]), ("unibet", [2.5, 2.5, 3.0]),
        ("softbook", [3.2, 2.3, 2.9]),
    ])
    ctx = ContextFlags(combined_market=True)
    res = analyze_market("A vs B", "Resultado+Golos", ["X", "Y", "Z"], quotes, context=ctx)
    assert any("combinado" in w.lower() for v in res.values for w in v.warnings)


def test_rank_by_value_orders_desc():
    quotes = _books([
        ("pinnacle", [2.0, 2.0]), ("bet365", [2.0, 2.0]), ("williamhill", [2.0, 2.0]),
        ("unibet", [2.0, 2.0]), ("soft", [2.40, 1.70]),
    ])
    res = analyze_market("A vs B", "1X2", ["A", "B"], quotes, method="proportional")
    ranked = rank_by_value(res.values)
    assert ranked == sorted(ranked, key=lambda v: v.best_ev, reverse=True)


# --- (4) estatística por casa via pipeline -------------------------------- #
def _game_with(market, selections, rows):
    return GameOdds(
        game="A vs B", home="A", away="B", commence_time="",
        markets=[MarketOdds(market=market, selections=selections, quotes=_books(rows))],
    )


def test_pipeline_best_book_counts_and_discards():
    good = _game_with("1X2", ["A", "B"], [
        ("pinnacle", [2.0, 2.0]), ("bet365", [2.0, 2.0]), ("williamhill", [2.0, 2.0]),
        ("unibet", [2.0, 2.0]), ("softbook", [2.60, 1.55]),
    ])
    fewbooks = _game_with("1X2", ["A", "B"], [
        ("pinnacle", [2.6, 2.0]), ("bet365", [2.0, 2.0]),
    ])
    report = analyze_games([good, fewbooks], method="proportional")
    assert report.markets_analyzed == 1
    assert report.markets_discarded_few_books == 1
    # softbook dá a melhor odd na seleção A; conta para a estatística.
    assert report.best_book_counts["softbook"] >= 1
    assert report.selections_evaluated == 2


# --- whitelist: acionável vs referência ----------------------------------- #
def test_normalize_whitelist():
    assert normalize_whitelist(None) is None
    assert normalize_whitelist("") is None
    assert normalize_whitelist("bet365, betfair") == {"bet365", "betfair"}
    assert normalize_whitelist(["Bet365", " Unibet "]) == {"bet365", "unibet"}


def test_book_in_whitelist_tolerant_match():
    wl = normalize_whitelist("betfair,bet365")
    assert book_in_whitelist("betfair_ex_eu", wl)   # inclusão parcial
    assert book_in_whitelist("bet365", wl)
    assert not book_in_whitelist("pinnacle", wl)
    # sem whitelist, tudo passa
    assert book_in_whitelist("qualquer", None)


def test_no_whitelist_all_actionable():
    quotes = _books([
        ("pinnacle", [2.0, 2.0]), ("bet365", [2.0, 2.0]), ("williamhill", [2.0, 2.0]),
        ("unibet", [2.0, 2.0]), ("softbook", [2.60, 1.55]),
    ])
    res = analyze_market("A vs B", "1X2", ["A", "B"], quotes, method="proportional")
    assert all(v.section == "actionable" for v in res.values)


def test_whitelist_splits_actionable_and_reference():
    # softbook (não-whitelist) dá a melhor odd em A; bet365 (whitelist) também
    # tem valor mas menor. Deve haver acionável (bet365) e referência (softbook).
    quotes = _books([
        ("pinnacle", [2.0, 2.0]), ("williamhill", [2.0, 2.0]), ("unibet", [2.0, 2.0]),
        ("bet365", [2.35, 1.75]),      # whitelist, com algum valor em A
        ("softbook", [2.70, 1.55]),    # fora da whitelist, ainda mais valor em A
    ])
    res = analyze_market("A vs B", "1X2", ["A", "B"], quotes,
                         method="proportional", whitelist="bet365,betfair")
    a_action = [v for v in res.values if v.selection == "A" and v.section == "actionable"]
    a_ref = [v for v in res.values if v.selection == "A" and v.section == "reference"]
    assert a_action and a_action[0].best_book == "bet365"
    assert a_ref and a_ref[0].best_book == "softbook"
    # a odd de referência é melhor do que a acionável (valor que não consigo apanhar)
    assert a_ref[0].best_odds > a_action[0].best_odds


def test_whitelist_no_actionable_when_value_only_outside():
    # Só softbook (fora da whitelist) tem valor; a whitelist não deve acionar nada.
    quotes = _books([
        ("pinnacle", [2.0, 2.0]), ("williamhill", [2.0, 2.0]), ("unibet", [2.0, 2.0]),
        ("bet365", [1.80, 1.80]),      # whitelist, odds curtas: sem valor em lado nenhum
        ("softbook", [2.60, 1.55]),    # fora da whitelist, com valor em A
    ])
    res = analyze_market("A vs B", "1X2", ["A", "B"], quotes,
                         method="proportional", whitelist="bet365")
    assert not [v for v in res.values if v.section == "actionable"]
    assert [v for v in res.values if v.section == "reference"]


def test_whitelist_consensus_uses_all_books():
    # O consenso não muda com a whitelist (usa sempre todas as casas): a
    # prob_consenso da seleção A é igual com e sem whitelist.
    quotes = _books([
        ("pinnacle", [2.0, 2.0]), ("williamhill", [2.0, 2.0]), ("unibet", [2.0, 2.0]),
        ("bet365", [2.35, 1.75]), ("softbook", [2.70, 1.55]),
    ])
    without = analyze_market("A vs B", "1X2", ["A", "B"], quotes, method="proportional")
    withwl = analyze_market("A vs B", "1X2", ["A", "B"], quotes,
                            method="proportional", whitelist="bet365")
    pa_without = next(v for v in without.values if v.selection == "A").consensus_prob
    pa_with = next(v for v in withwl.values
                   if v.selection == "A" and v.section == "actionable").consensus_prob
    assert pa_without == pytest.approx(pa_with)


def test_pipeline_report_actionable_reference_split():
    good = _game_with("1X2", ["A", "B"], [
        ("pinnacle", [2.0, 2.0]), ("williamhill", [2.0, 2.0]), ("unibet", [2.0, 2.0]),
        ("bet365", [2.35, 1.75]), ("softbook", [2.70, 1.55]),
    ])
    report = analyze_games([good], method="proportional", whitelist="bet365")
    assert report.has_whitelist
    assert any(v.best_book == "bet365" for v in report.actionable)
    assert any(v.best_book == "softbook" for v in report.reference)
    assert report.n_value == len(report.actionable)


def test_pipeline_csv_has_new_columns():
    good = _game_with("1X2", ["A", "B"], [
        ("pinnacle", [2.0, 2.0]), ("bet365", [2.0, 2.0]), ("williamhill", [2.0, 2.0]),
        ("unibet", [2.0, 2.0]), ("softbook", [2.60, 1.55]),
    ])
    report = analyze_games([good], method="proportional")
    csv = values_to_csv(report.values)
    header = csv.splitlines()[0]
    for col in ("seccao", "odd_mediana", "ev_shin_pct", "ev_prop_pct", "metodos_confirmam"):
        assert col in header
