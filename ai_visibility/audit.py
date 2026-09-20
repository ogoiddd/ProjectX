"""Orquestração: URL → fetch → queries → LLM → score → relatório + directory."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .directory import render_directory_html
from .fetch import BusinessProfile, fetch_business
from .llm_check import QueryResult, results_summary, run_queries
from .queries import format_location, generate_queries
from .report import render_report_html
from .score import ScoreBreakdown, compute_score


@dataclass
class AuditResult:
    """Tudo o que uma auditoria produz — pronto para render ou persistência."""

    profile: BusinessProfile
    queries_run: int
    results: list[QueryResult]
    summary: dict[str, Any]
    score: ScoreBreakdown
    report_html: str
    directory_html: str
    provider: str
    model: str
    extras: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "profile": self.profile.as_dict(),
            "queries_run": self.queries_run,
            "summary": self.summary,
            "score": self.score.as_dict(),
            "provider": self.provider,
            "model": self.model,
            "results": [
                {
                    "query": r.query.text,
                    "intent": r.query.intent,
                    "mentioned": r.business_mentioned,
                    "competitors": r.competitors_mentioned,
                    "snippet": r.mention_snippet,
                    "latency_ms": r.latency_ms,
                    "error": r.error,
                }
                for r in self.results
            ],
        }


def run_audit(
    url: str,
    *,
    n_queries: int = 10,
    provider: str = "auto",
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
    delay_seconds: float = 0.0,
) -> AuditResult:
    """Corre a auditoria completa e devolve :class:`AuditResult`."""
    profile = fetch_business(url)
    queries = generate_queries(profile, n=n_queries)

    location = format_location(profile)
    results = run_queries(
        queries,
        business_name=profile.name,
        category=profile.category,
        location=location,
        provider=provider,
        model=model,
        api_key=api_key,
        delay_seconds=delay_seconds,
    )
    summary = results_summary(results)
    score = compute_score(profile, results, top_competitors=summary["top_competitors"])

    directory_html = render_directory_html(profile)
    report_html = render_report_html(profile, results, score)

    used_provider = results[0].provider if results else provider
    used_model = results[0].model if results else model
    return AuditResult(
        profile=profile,
        queries_run=len(queries),
        results=results,
        summary=summary,
        score=score,
        report_html=report_html,
        directory_html=directory_html,
        provider=used_provider,
        model=used_model,
    )


def write_outputs(audit: AuditResult, out_dir: str | os.PathLike[str]) -> dict[str, str]:
    """Escreve os artefactos da auditoria em disco. Devolve o caminho de cada um."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    slug = _slug(audit.profile.name) or "business"

    report_path = out / f"{slug}-ai-visibility-report.html"
    directory_path = out / f"{slug}-directory.html"
    json_path = out / f"{slug}-audit.json"

    report_path.write_text(audit.report_html, encoding="utf-8")
    directory_path.write_text(audit.directory_html, encoding="utf-8")
    json_path.write_text(json.dumps(audit.as_dict(), indent=2, ensure_ascii=False),
                         encoding="utf-8")

    return {
        "report_html": str(report_path),
        "directory_html": str(directory_path),
        "audit_json": str(json_path),
    }


def _slug(name: str) -> str:
    import re
    s = re.sub(r"[^\w\s-]", "", name.lower())
    s = re.sub(r"[\s_-]+", "-", s).strip("-")
    return s[:60]
