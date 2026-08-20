"""Interface de linha de comandos: tabela em consola, CSV e resumo.

Uso típico:

    export ODDS_API_KEY=xxxxxxxx
    python -m odds_value.cli --sport soccer_epl --markets h2h,totals --csv valor.csv

Sem rede (ex.: demonstração/testes), usa um ficheiro JSON já guardado do
The Odds API:

    python -m odds_value.cli --from-json exemplo.json --method shin
"""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from .devig import devig_proportional, devig_shin, margin
from .pipeline import AnalysisReport, analyze_games, load_games, values_to_csv
from .value import DEFAULT_EV_THRESHOLD, MIN_BOOKS, MIN_CONSENSUS_PROB, ValueSelection


def _clip(text: str, width: int) -> str:
    """Trunca texto ao comprimento máximo, com reticências."""
    text = str(text)
    return text if len(text) <= width else text[: width - 1] + "…"


def print_table(values: Sequence[ValueSelection]) -> None:
    """Imprime a tabela de valor na consola."""
    if not values:
        print("\nNenhum mercado com EV positivo acima do limite.")
        return

    headers = [
        "Jogo", "Mercado", "Seleção", "Melhor odd", "Casa", "Mediana",
        "Desvio", "Prob. cons.", "Odd justa", "EV%", "Shin/Prop", "Confirma",
    ]
    rows = []
    for v in values:
        rows.append([
            _clip(v.game, 26),
            _clip(v.market, 13),
            _clip(v.selection, 16),
            f"{v.best_odds:.2f}",
            _clip(v.best_book, 11),
            f"{v.median_odds:.2f}",
            f"{v.odds_dispersion:.2f}",
            f"{v.consensus_prob * 100:.1f}%",
            f"{v.fair_odds:.2f}",
            f"{v.ev_pct:+.1f}%",
            f"{v.ev_shin * 100:+.1f}/{v.ev_proportional * 100:+.1f}",
            v.agreement,
        ])

    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    print("\n" + line)
    print("-" * len(line))
    for v, row in zip(values, rows):
        print(" | ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)))
        for w in v.warnings:
            print(f"    ⚠ {w}")


def write_csv(values: Sequence[ValueSelection], path: str) -> None:
    """Exporta os resultados para CSV."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(values_to_csv(values))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="odds_value",
        description="Análise de valor em odds de futebol (The Odds API / API-Football).",
    )
    src = p.add_mutually_exclusive_group()
    src.add_argument("--sport", default="soccer_epl",
                     help="Chave do desporto no The Odds API (ex.: soccer_epl).")
    src.add_argument("--from-json", metavar="FICHEIRO",
                     help="Lê a resposta do The Odds API a partir de um JSON local (sem rede).")
    p.add_argument("--regions", default="eu,uk", help="Regiões de casas (eu,uk,us,au).")
    p.add_argument("--markets", default="h2h,totals",
                   help="Mercados a pedir (h2h,totals,btts).")
    p.add_argument("--method", choices=["proportional", "shin"], default="shin",
                   help="Método de remoção de margem para o consenso.")
    p.add_argument("--ev-threshold", type=float, default=DEFAULT_EV_THRESHOLD,
                   help="EV mínimo para sinalizar (fracionário; 0.02 = +2%%).")
    p.add_argument("--min-books", type=int, default=MIN_BOOKS,
                   help="Nº mínimo de casas por mercado (abaixo disto, descarta).")
    p.add_argument("--min-prob", type=float, default=MIN_CONSENSUS_PROB,
                   help="Prob. de consenso mínima por seleção (abaixo, ignora).")
    p.add_argument("--csv", metavar="FICHEIRO", help="Caminho para exportar CSV.")
    p.add_argument("--compare-devig", action="store_true",
                   help="Mostra comparação proporcional vs Shin para o 1º mercado.")
    return p


def _compare_devig_demo(games) -> None:
    """Imprime uma comparação lado-a-lado dos dois métodos de devig."""
    for g in games:
        for mkt in g.markets:
            odds = mkt.quotes[0].odds
            prop = devig_proportional(odds)
            shin = devig_shin(odds)
            print(f"\nComparação devig — {g.game} / {mkt.market} "
                  f"(casa {mkt.quotes[0].bookmaker}, margem {margin(odds) * 100:.2f}%)")
            print(f"  {'Seleção':<20} {'Odd':>7} {'Proporcional':>13} {'Shin':>8}")
            for sel, o, pp, sh in zip(mkt.selections, odds, prop, shin):
                print(f"  {sel[:20]:<20} {o:>7.2f} {pp * 100:>12.2f}% {sh * 100:>7.2f}%")
            return  # só o primeiro mercado


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    games = load_games(
        from_json=args.from_json,
        sport=args.sport,
        regions=args.regions,
        markets=args.markets,
    )

    if not games:
        print("Sem jogos/mercados válidos na resposta.", file=sys.stderr)
        return 1

    if args.compare_devig:
        _compare_devig_demo(games)

    report = analyze_games(
        games,
        method=args.method,
        ev_threshold=args.ev_threshold,
        min_books=args.min_books,
        min_prob=args.min_prob,
    )
    print_table(report.values)
    print_bookmaker_stats(report)

    if args.csv:
        write_csv(report.values, args.csv)
        print(f"\nCSV exportado para: {args.csv}")

    print(
        f"\nResumo: {report.n_value} seleções com EV positivo encontradas "
        f"de {report.markets_analyzed} mercados analisados "
        f"({report.markets_discarded_few_books} descartados por < {args.min_books} casas; "
        f"devig: {args.method}, limite EV: {args.ev_threshold * 100:+.1f}%, "
        f"prob. mín.: {args.min_prob * 100:.0f}%)."
    )
    outliers = sum(1 for v in report.values if v.is_outlier)
    if outliers:
        print(f"         {outliers} sinalizadas como outlier — confirmar antes de apostar.")
    only_one = sum(1 for v in report.values if len(v.flagged_by) == 1)
    if only_one:
        print(f"         {only_one} confirmadas por apenas um método (menos robustas).")
    return 0


def print_bookmaker_stats(report: AnalysisReport) -> None:
    """(4) Estatística: quantas vezes cada casa deu a melhor odd."""
    if not report.best_book_counts:
        return
    total = report.selections_evaluated
    print(f"\nMelhor odd por casa (em {total} seleções avaliadas):")
    for book, count in report.best_book_counts.most_common():
        share = count / total * 100 if total else 0.0
        flag = "  ← aparece muito acima do resto (possível outlier sistemático)" \
            if share >= 40 and total >= 5 else ""
        print(f"  {book:<18} {count:>3}  ({share:4.1f}%){flag}")


if __name__ == "__main__":
    raise SystemExit(main())
