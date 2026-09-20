"""Cálculo do Score de Visibilidade em AI /100.

Composto por três dimensões (pesos escolhidos para replicar o formato mostrado
no vídeo — Presence 45, Content Depth 30, Structured Data 25):

- **Presence (45 pts)** — % de queries em que o negócio é mencionado, ponderado
  por *intent* (discovery > local > trust > comparison).
- **Content Depth (30 pts)** — o site tem substância para o LLM ler? (comprimento,
  headings, FAQ, presença de palavras-chave da categoria).
- **Structured Data (25 pts)** — JSON-LD, LocalBusiness/FAQPage schema, OG tags,
  NAP (Name/Address/Phone) — quanto mais estruturado, mais o LLM confia.

Cada dimensão devolve subpontuação 0–1; multiplicamos pelo peso para o total.

Também derivamos *recommendations* — a lista concreta que vai ao relatório e
que sustenta o pitch ("aqui está o que temos de arranjar").
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .fetch import BusinessProfile
from .llm_check import QueryResult

WEIGHT_PRESENCE = 45
WEIGHT_CONTENT = 30
WEIGHT_STRUCTURED = 25

# ponderação por intent na dimensão de Presence
_INTENT_WEIGHTS = {"discovery": 1.2, "local": 1.1, "trust": 1.0, "comparison": 0.8}


@dataclass
class ScoreBreakdown:
    """Resultado final da pontuação, pronto a render em HTML/PDF."""

    total: int                           # 0–100
    tier: str                            # "Invisible" | "Emerging" | "Growing" | "Established" | "Dominant"

    presence: int                        # 0–45
    presence_ratio: float                # 0–1
    presence_notes: list[str] = field(default_factory=list)

    content_depth: int = 0               # 0–30
    content_notes: list[str] = field(default_factory=list)

    structured_data: int = 0             # 0–25
    structured_notes: list[str] = field(default_factory=list)

    recommendations: list[dict[str, str]] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


def _tier(total: int) -> str:
    if total >= 85:
        return "Dominant"
    if total >= 65:
        return "Established"
    if total >= 45:
        return "Growing"
    if total >= 25:
        return "Emerging"
    return "Invisible"


def _score_presence(results: list[QueryResult]) -> tuple[int, float, list[str]]:
    ok = [r for r in results if not r.error]
    if not ok:
        return 0, 0.0, ["A auditoria não conseguiu correr contra o LLM."]

    weighted_num = 0.0
    weighted_den = 0.0
    per_intent: dict[str, list[bool]] = {}
    for r in ok:
        w = _INTENT_WEIGHTS.get(r.query.intent, 1.0)
        weighted_den += w
        if r.business_mentioned:
            weighted_num += w
        per_intent.setdefault(r.query.intent, []).append(r.business_mentioned)

    ratio = weighted_num / weighted_den if weighted_den else 0.0
    pts = round(ratio * WEIGHT_PRESENCE)

    notes: list[str] = []
    hits = sum(1 for r in ok if r.business_mentioned)
    notes.append(f"Mencionado em {hits}/{len(ok)} queries testadas.")
    for intent, hits_list in per_intent.items():
        h = sum(hits_list)
        notes.append(f"— {intent}: {h}/{len(hits_list)}.")
    if hits == 0:
        notes.append(
            "O LLM não referiu o negócio em nenhuma pergunta — invisibilidade total."
        )
    return pts, ratio, notes


def _score_content(profile: BusinessProfile) -> tuple[int, list[str]]:
    if not profile.ok:
        return 0, [f"Não consegui ler o site ({profile.error or 'erro'})."]

    notes: list[str] = []
    score = 0.0

    # 12 pts por comprimento de texto (saturado aos 6k chars)
    tl = profile.text_length
    length_pts = min(1.0, tl / 6000.0) * 12
    score += length_pts
    if tl < 1500:
        notes.append(f"Texto visível muito curto ({tl} chars) — LLMs precisam de substância para citar.")
    elif tl < 4000:
        notes.append(f"Texto moderado ({tl} chars) — mais conteúdo por página ajudaria.")
    else:
        notes.append(f"Bom volume de texto ({tl} chars).")

    # 6 pts pelos headings (saturado aos 12)
    hn = len(profile.headings)
    headings_pts = min(1.0, hn / 12.0) * 6
    score += headings_pts
    if hn < 4:
        notes.append(f"Poucos headings ({hn}) — usar H1/H2/H3 estrutura a página para o AI.")

    # 6 pts se tiver FAQ / Q&A textual
    if profile.has_faq:
        score += 6
        notes.append("Boa: já existe uma secção com FAQ / Q&A.")
    else:
        notes.append("Não detetei FAQ — perde muita visibilidade para queries do tipo pergunta.")

    # 6 pts se tiver keywords da própria categoria a aparecerem no conteúdo
    n_keys = sum(profile.keywords_hits.values())
    keys_pts = min(1.0, n_keys / 15.0) * 6
    score += keys_pts
    if n_keys < 3:
        notes.append("Poucas menções às palavras-chave da categoria — dilui o sinal.")

    return round(score), notes


def _score_structured(profile: BusinessProfile) -> tuple[int, list[str]]:
    if not profile.ok:
        return 0, ["Sem análise estrutural: falha ao obter o site."]

    notes: list[str] = []
    score = 0.0

    if profile.json_ld_types:
        score += 10
        notes.append(f"JSON-LD encontrado: {', '.join(sorted(set(profile.json_ld_types))) or '?'}.")
    else:
        notes.append("Sem JSON-LD — os assistentes AI dependem muito deste sinal.")

    if profile.has_localbusiness_schema:
        score += 6
        notes.append("LocalBusiness schema presente — muito bom para AI local.")
    else:
        notes.append("Sem schema LocalBusiness (ou derivado) — recomendado para negócio local.")

    if profile.has_faqpage_schema:
        score += 4
        notes.append("FAQPage schema presente.")
    else:
        notes.append("Sem FAQPage schema — grande oportunidade para responder às perguntas do comprador em formato máquina.")

    if profile.og_title and profile.og_description:
        score += 2
        notes.append("Open Graph completo.")
    else:
        notes.append("Open Graph incompleto (og:title/og:description).")

    if profile.phone and (profile.city or profile.state):
        score += 3
        notes.append("NAP básico detetado (telefone + localização).")
    else:
        notes.append("NAP (nome / morada / telefone) não é evidente ao AI.")

    return round(score), notes


def _recommendations(
    profile: BusinessProfile,
    presence_ratio: float,
    top_competitors: list[tuple[str, int]],
) -> list[dict[str, str]]:
    recs: list[dict[str, str]] = []
    if presence_ratio < 0.5:
        recs.append({
            "title": "Publicar uma Directory Page AI-friendly",
            "why": (
                "O negócio quase não aparece em respostas de AI. Precisamos de uma página"
                " pública com todo o contexto que os LLMs procuram (nome, morada,"
                " serviços, Q&A, avaliações) marcada com JSON-LD LocalBusiness + FAQPage."
            ),
            "impact": "Alto",
        })
    if not profile.has_faqpage_schema or not profile.has_faq:
        recs.append({
            "title": "Adicionar FAQ com FAQPage JSON-LD",
            "why": (
                "As perguntas frequentes (preço, área de serviço, licenciamento, tempo de"
                " resposta) são exatamente as *strings* que os LLMs vão citar. Sem elas,"
                " o negócio não é elegível para essas queries."
            ),
            "impact": "Alto",
        })
    if not profile.has_localbusiness_schema:
        recs.append({
            "title": "Marcar LocalBusiness JSON-LD",
            "why": (
                "Nome, morada, telefone, horário, geo e área servida em JSON-LD são o"
                " sinal mais forte para o LLM associar o negócio a uma localização."
            ),
            "impact": "Alto",
        })
    if profile.text_length < 4000:
        recs.append({
            "title": "Expandir conteúdo de serviço",
            "why": (
                "Menos de 4k caracteres visíveis dão pouco texto para o LLM extrair. Uma"
                " página de serviços com 800–1200 palavras por categoria muda o jogo."
            ),
            "impact": "Médio",
        })
    if not profile.og_title or not profile.og_description:
        recs.append({
            "title": "Completar meta tags (Open Graph + description)",
            "why": (
                "Alguns crawlers de AI e agregadores usam a descrição OG para gerar o"
                " snippet. Sem ela, o LLM inventa ou salta o resultado."
            ),
            "impact": "Baixo",
        })
    if top_competitors:
        names = ", ".join(n for n, _ in top_competitors[:3])
        recs.append({
            "title": "Análise competitiva focada",
            "why": (
                f"O AI está a recomendar em vez do negócio: {names}. Estudar os sinais"
                " que eles têm (schema, reviews estruturadas, backlinks locais) e replicar."
            ),
            "impact": "Médio",
        })
    return recs


def compute_score(
    profile: BusinessProfile,
    results: list[QueryResult],
    top_competitors: list[tuple[str, int]] | None = None,
) -> ScoreBreakdown:
    """Combina Presence + Content + Structured num Score /100."""
    presence_pts, presence_ratio, presence_notes = _score_presence(results)
    content_pts, content_notes = _score_content(profile)
    structured_pts, structured_notes = _score_structured(profile)

    total = min(100, presence_pts + content_pts + structured_pts)
    recs = _recommendations(profile, presence_ratio, top_competitors or [])

    return ScoreBreakdown(
        total=total,
        tier=_tier(total),
        presence=presence_pts,
        presence_ratio=presence_ratio,
        presence_notes=presence_notes,
        content_depth=content_pts,
        content_notes=content_notes,
        structured_data=structured_pts,
        structured_notes=structured_notes,
        recommendations=recs,
    )
