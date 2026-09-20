"""Gera o **relatório HTML** — o *lead magnet* que é enviado por email.

Self-contained (nenhum recurso externo), estilizado para impressão em A4 →
o cliente abre em Safari/Chrome e faz "Print → Save as PDF". Foi desenhado
para se parecer com o exemplo do vídeo: score grande /100, tier em badge,
breakdown por dimensão com barras, recomendações accionáveis e tabela de
queries testadas.
"""

from __future__ import annotations

import html
from datetime import date
from typing import Any

from .fetch import BusinessProfile
from .llm_check import QueryResult
from .score import ScoreBreakdown

_TIER_COLORS = {
    "Invisible": "#dc2626",     # vermelho
    "Emerging": "#ea580c",       # laranja
    "Growing": "#ca8a04",        # âmbar
    "Established": "#16a34a",    # verde
    "Dominant": "#0891b2",       # ciano
}

_CSS = """
:root { color-scheme: light dark; }
* { box-sizing: border-box; }
body { font-family: -apple-system, system-ui, Segoe UI, Roboto, sans-serif;
       margin: 0; padding: 2rem; line-height: 1.5; color: #111;
       background: #fafaf9; }
.page { max-width: 820px; margin: 0 auto; background: #fff;
        padding: 2.5rem; border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,.06); }
h1 { font-size: 1.6rem; margin: 0 0 .3rem; }
.eyebrow { font-size: .72rem; letter-spacing: .12em; text-transform: uppercase;
           color: #6b7280; font-weight: 700; }
.byline { color: #6b7280; font-size: .85rem; margin-bottom: 1.5rem; }
.hero { display: grid; grid-template-columns: 1fr; gap: 1rem;
        padding: 1.5rem; border-radius: 16px; color: #fff;
        background: linear-gradient(135deg,#0f172a 0%,#1e293b 60%,#0b1220 100%);
        margin-bottom: 1.5rem; }
.hero h2 { font-size: 1.25rem; margin: 0 0 .3rem; font-weight: 600; }
.hero .lead { font-size: 1.05rem; color: #cbd5e1; }
.hero .hit { color: #f87171; font-weight: 800; }
.hero .ok  { color: #34d399; font-weight: 800; }
.score-row { display: grid; grid-template-columns: 220px 1fr;
             gap: 1.5rem; align-items: center; margin: 1.5rem 0; }
.score-ring { position: relative; width: 200px; height: 200px; }
.score-ring svg { transform: rotate(-90deg); }
.score-ring .val { position: absolute; inset: 0; display: grid;
                   place-items: center; font-size: 3rem; font-weight: 800;
                   color: #111; letter-spacing: -.02em; }
.tier-badge { display: inline-block; padding: .35rem .75rem;
              border-radius: 999px; font-size: .78rem; font-weight: 700;
              letter-spacing: .04em; text-transform: uppercase; color: #fff; }
.section { margin: 1.75rem 0; }
.section h3 { font-size: 1.05rem; margin: 0 0 .5rem; }
.bar { height: 10px; background: #e5e7eb; border-radius: 999px;
       overflow: hidden; }
.bar > span { display: block; height: 100%;
              background: linear-gradient(90deg,#f97316,#f59e0b,#facc15); }
.dim { display: grid; grid-template-columns: 1fr auto; align-items: center;
       gap: 1rem; padding: .8rem 0; border-top: 1px solid #f1f5f9; }
.dim:first-child { border-top: 0; }
.dim .label { font-weight: 700; color: #111; }
.dim .num { font-variant-numeric: tabular-nums; font-weight: 800;
            color: #111; }
.notes { margin: .5rem 0 .2rem; font-size: .88rem; color: #374151;
         padding-left: 1rem; }
.notes li { margin: .15rem 0; }
.rec { padding: 1rem; border: 1px solid #e5e7eb; border-radius: 12px;
       margin-bottom: .8rem; background: #fafaf9; }
.rec h4 { margin: 0 0 .3rem; font-size: .98rem; }
.rec .why { color: #4b5563; font-size: .9rem; }
.rec .impact { display: inline-block; margin-top: .4rem; padding: .15rem .55rem;
               border-radius: 6px; font-size: .72rem; font-weight: 700;
               text-transform: uppercase; letter-spacing: .05em; }
.rec .impact.Alto  { background: #fee2e2; color: #991b1b; }
.rec .impact.Médio { background: #fef3c7; color: #92400e; }
.rec .impact.Baixo { background: #dcfce7; color: #166534; }
table.q { width: 100%; border-collapse: collapse; margin-top: .6rem;
          font-size: .82rem; }
table.q th, table.q td { text-align: left; padding: .55rem .5rem;
                         border-bottom: 1px solid #f1f5f9; vertical-align: top; }
table.q th { font-size: .68rem; text-transform: uppercase; letter-spacing: .05em;
             color: #6b7280; font-weight: 700; }
table.q .yes { color: #16a34a; font-weight: 800; }
table.q .no  { color: #dc2626; font-weight: 800; }
.footer { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #f1f5f9;
          font-size: .78rem; color: #6b7280; }
.callout { padding: 1rem 1.25rem; border-radius: 12px;
           background: linear-gradient(90deg,#fef3c7,#fef9c3);
           color: #713f12; font-weight: 600; margin: 1rem 0 1.5rem; }
@media print {
  body { background: #fff; padding: 0; }
  .page { box-shadow: none; border-radius: 0; padding: 1rem 1.5rem; }
  @page { size: A4; margin: 12mm; }
}
"""


def _esc(x: Any) -> str:
    return html.escape(str(x))


def _ring_svg(score: int, color: str) -> str:
    """Anel de progresso SVG, mostrando o score."""
    r = 84
    circ = 2 * 3.14159 * r
    filled = circ * (score / 100.0)
    return f"""<svg width="200" height="200" viewBox="0 0 200 200">
  <circle cx="100" cy="100" r="{r}" stroke="#e5e7eb" stroke-width="16" fill="none"/>
  <circle cx="100" cy="100" r="{r}" stroke="{color}" stroke-width="16" fill="none"
    stroke-linecap="round"
    stroke-dasharray="{filled:.1f} {circ - filled:.1f}"/>
</svg>"""


def _hero_line(profile: BusinessProfile, hits: int, total: int) -> str:
    name = _esc(profile.name)
    n = total or 1
    if hits == 0:
        return (
            f"We ran <strong>{name}</strong> through <span class='hit'>{n} live ChatGPT "
            f"searches</span>. It showed up in <span class='hit'>0 of them</span>."
        )
    return (
        f"We ran <strong>{name}</strong> through <span class='ok'>{n} live ChatGPT "
        f"searches</span>. It showed up in <span class='ok'>{hits} of {n}</span>."
    )


def render_report_html(
    profile: BusinessProfile,
    results: list[QueryResult],
    score: ScoreBreakdown,
    *,
    generated_on: str | None = None,
    directory_url: str | None = None,
) -> str:
    """Devolve o HTML self-contained do relatório."""
    generated_on = generated_on or date.today().isoformat()
    total_queries = len(results)
    hits = sum(1 for r in results if r.business_mentioned)
    color = _TIER_COLORS.get(score.tier, "#111")

    # cabeçalho — replica o look do vídeo
    hero = f"""<div class="hero">
  <div class="eyebrow" style="color:#94a3b8">AI Visibility Report · {_esc(profile.category.title())}
     · {_esc(profile.city or profile.state or "")} · {_esc(generated_on)}</div>
  <h2>{_hero_line(profile, hits, total_queries)}</h2>
  <div class="lead">Here's exactly what's holding {_esc(profile.name)} back in AI search — and how to fix it, in plain English.</div>
</div>"""

    # score ring
    ring = f"""<div class="score-row">
  <div class="score-ring">
    {_ring_svg(score.total, color)}
    <div class="val">{score.total}</div>
  </div>
  <div>
    <div class="eyebrow" style="color:#6b7280">AI Visibility Score</div>
    <h3 style="margin:.2rem 0 .6rem;font-size:1.15rem">How often AI recommends {_esc(profile.name)}</h3>
    <span class="tier-badge" style="background:{color}">{_esc(score.tier)}</span>
    <p style="margin:.8rem 0 0; color:#4b5563">Estimado com base em {total_queries} queries reais de comprador
    ({hits} menções · {score.presence_ratio*100:.0f}% presence).</p>
  </div>
</div>"""

    # breakdown por dimensão
    def _dim(label: str, pts: int, out_of: int, notes: list[str]) -> str:
        pct = int(round((pts / out_of) * 100)) if out_of else 0
        notes_html = "".join(f"<li>{_esc(n)}</li>" for n in notes)
        return f"""<div class="dim">
  <div style="flex:1">
    <div class="label">{_esc(label)}</div>
    <div class="bar" style="margin-top:.4rem"><span style="width:{pct}%"></span></div>
    <ul class="notes">{notes_html}</ul>
  </div>
  <div class="num">{pts}<span style="color:#94a3b8;font-weight:400"> / {out_of}</span></div>
</div>"""

    breakdown = "<div class='section'><h3>Visibility breakdown</h3>" + (
        _dim("Presence in AI answers", score.presence, 45, score.presence_notes)
        + _dim("Content depth", score.content_depth, 30, score.content_notes)
        + _dim("Structured data", score.structured_data, 25, score.structured_notes)
    ) + "</div>"

    # recomendações
    rec_html = "".join(
        f"""<div class="rec">
  <h4>{i+1}. {_esc(r['title'])}</h4>
  <div class="why">{_esc(r['why'])}</div>
  <span class="impact {_esc(r['impact'])}">Impact: {_esc(r['impact'])}</span>
</div>"""
        for i, r in enumerate(score.recommendations)
    ) or "<p>Sem recomendações críticas — a visibilidade está saudável.</p>"

    recs = f"""<div class="section">
  <h3>Recommended fixes</h3>
  {rec_html}
</div>"""

    # tabela de queries
    rows = []
    for r in results:
        badge = '<span class="yes">✓</span>' if r.business_mentioned else '<span class="no">✗</span>'
        rows.append(
            f"<tr><td>{_esc(r.query.text)}</td>"
            f"<td>{_esc(r.query.intent)}</td>"
            f"<td>{badge}</td>"
            f"<td style='font-size:.78rem;color:#6b7280'>"
            f"{_esc(', '.join(r.competitors_mentioned[:3]) or '—')}</td></tr>"
        )
    queries_tbl = f"""<div class="section">
  <h3>Queries tested against ChatGPT</h3>
  <table class="q">
    <thead><tr><th>Query</th><th>Intent</th><th>Mentioned?</th><th>Top competitors named</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</div>"""

    callout = ""
    if directory_url:
        callout = f"""<div class="callout">
  Ready-to-publish AI directory page for {_esc(profile.name)} generated
  at <code>{_esc(directory_url)}</code>. Publish it to your domain to close
  the largest gap in one move.
</div>"""

    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Visibility Report — {_esc(profile.name)}</title>
<style>{_CSS}</style>
</head><body>
<div class="page">
  <div class="eyebrow">AI Visibility Report</div>
  <h1>{_esc(profile.name)}</h1>
  <div class="byline">
    {_esc(profile.category.title())} · {_esc(profile.city or "")}{", " if profile.city and profile.state else ""}{_esc(profile.state or "")}
    · Prepared {_esc(generated_on)}
  </div>
  {hero}
  {callout}
  {ring}
  {breakdown}
  {recs}
  {queries_tbl}
  <div class="footer">
    Audit powered by ai_visibility (local run · provider: {_esc(results[0].provider if results else '—')} · model: {_esc(results[0].model if results else '—')}).<br>
    This is a snapshot; AI answers vary over time. Retest 14–30 days after publishing the fixes.
  </div>
</div>
</body></html>"""
