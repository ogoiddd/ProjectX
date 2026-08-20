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
from .pipeline import analyze_games, load_games, values_to_csv
from .value import DEFAULT_EV_THRESHOLD, ValueSelection


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
        "Jogo", "Mercado", "Seleção", "Melhor odd", "Casa",
        "Prob. cons.", "Odd justa", "EV%",
    ]
    rows = []
    for v in values:
        rows.append([
            _clip(v.game, 28),
            _clip(v.market, 14),
            _clip(v.selection, 18),
            f"{v.best_odds:.2f}",
            _clip(v.best_book, 12),
            f"{v.consensus_prob * 100:.1f}%",
            f"{v.fair_odds:.2f}",
            f"{v.ev_pct:+.1f}%",
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

    values, markets_analyzed = analyze_games(games, args.method, args.ev_threshold)
    print_table(values)

    if args.csv:
        write_csv(values, args.csv)
        print(f"\nCSV exportado para: {args.csv}")

    print(
        f"\nResumo: {len(values)} mercados com EV positivo encontrados "
        f"de {markets_analyzed} analisados "
        f"(método de devig: {args.method}, limite EV: {args.ev_threshold * 100:+.1f}%)."
    )
    outliers = sum(1 for v in values if v.is_outlier)
    if outliers:
        print(f"         {outliers} sinalizados como outlier — confirmar antes de apostar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
