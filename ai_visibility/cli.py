"""CLI para correr a auditoria: ``python -m ai_visibility <url>``.

Exemplo:

    python -m ai_visibility https://kellyroofing.com --out ./reports
    python -m ai_visibility https://kellyroofing.com --provider mock

Produz três ficheiros em ``--out`` (por omissão ``./ai_visibility_out``):
    <slug>-ai-visibility-report.html      # relatório imprimível (PDF via browser)
    <slug>-directory.html                 # directory page a publicar
    <slug>-audit.json                     # dados crus da auditoria
"""

from __future__ import annotations

import argparse
import sys

from .audit import run_audit, write_outputs


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ai_visibility",
        description="Corre uma auditoria de visibilidade em AI para um negócio.",
    )
    p.add_argument("url", help="URL do site do negócio (ex.: https://kellyroofing.com)")
    p.add_argument("--out", default="./ai_visibility_out",
                   help="Directoria de saída (default: ./ai_visibility_out)")
    p.add_argument("--n-queries", type=int, default=10,
                   help="Número de queries a testar (default: 10)")
    p.add_argument("--provider", choices=("auto", "openai", "mock"), default="auto",
                   help="Provider LLM. 'auto' usa OpenAI se OPENAI_API_KEY estiver definida; caso contrário mock.")
    p.add_argument("--model", default="gpt-4o-mini",
                   help="Modelo OpenAI a usar (default: gpt-4o-mini)")
    p.add_argument("--delay", type=float, default=0.0,
                   help="Delay em segundos entre pedidos (rate-limit)")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        audit = run_audit(
            args.url,
            n_queries=args.n_queries,
            provider=args.provider,
            model=args.model,
            delay_seconds=args.delay,
        )
    except Exception as exc:  # noqa: BLE001 — mostrar ao utilizador de forma limpa
        print(f"[erro] {exc}", file=sys.stderr)
        return 2

    paths = write_outputs(audit, args.out)

    b = audit.profile
    s = audit.score
    hits = sum(1 for r in audit.results if r.business_mentioned)
    total = len(audit.results)

    print(f"\n=== {b.name} — {b.category} — {b.city or ''}{',' if b.city and b.state else ''} {b.state or ''}".rstrip())
    print(f"URL analisado: {b.fetched_url or b.url}")
    print(f"Provider: {audit.provider} · Modelo: {audit.model}")
    print()
    print(f"AI Visibility Score: {s.total}/100 ({s.tier})")
    print(f"  Presence:        {s.presence}/45   [{hits}/{total} menções]")
    print(f"  Content Depth:   {s.content_depth}/30")
    print(f"  Structured Data: {s.structured_data}/25")
    print()
    print("Top concorrentes mencionados pelo AI:")
    for name, count in audit.summary["top_competitors"][:5]:
        print(f"  - {name} ({count}x)")
    print()
    print("Ficheiros gerados:")
    for k, v in paths.items():
        print(f"  {k:>16}: {v}")
    if s.recommendations:
        print("\nRecomendações principais:")
        for i, r in enumerate(s.recommendations[:3], 1):
            print(f"  {i}. [{r['impact']}] {r['title']}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
