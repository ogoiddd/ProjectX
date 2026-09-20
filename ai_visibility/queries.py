"""Geração das queries de comprador que a auditoria testa contra o LLM.

Não usa AI para as gerar — usa templates por categoria + a localização
detetada no site. Motivo: é determinístico, gratuito, e reproduzível entre
auditorias (fundamental para o cliente confiar no relatório e para nós
compararmos scores antes/depois da correção).

Se a categoria não for reconhecida, cai para um conjunto genérico.
"""

from __future__ import annotations

from dataclasses import dataclass

from .fetch import BusinessProfile


@dataclass(frozen=True)
class BuyerQuery:
    """Uma query de comprador a testar contra o LLM."""

    text: str            # a query "como se fosse um utilizador"
    intent: str          # "discovery" | "comparison" | "trust" | "local"


# Perguntas por *intent* — o {cat} e {loc} são preenchidos por formato.
_TEMPLATES: dict[str, list[str]] = {
    "discovery": [
        "Best {cat} in {loc}",
        "Top rated {cat} companies near {loc}",
        "Who are the leading {cat}s serving {loc}",
    ],
    "comparison": [
        "Compare the best {cat} companies in {loc}",
        "What is the most reliable {cat} in {loc} for a homeowner",
    ],
    "trust": [
        "{cat} in {loc} with the best reviews",
        "Recommended {cat} in {loc} with a good reputation",
    ],
    "local": [
        "{cat} near me in {loc}",
        "Family owned {cat} in {loc}",
        "Licensed and insured {cat} in {loc}",
    ],
}

# Fallback quando não sabemos a categoria.
_GENERIC = [
    ("Top small businesses in {loc}", "discovery"),
    ("Best local service providers in {loc}", "discovery"),
    ("Highly rated companies in {loc}", "trust"),
    ("Recommended local businesses in {loc}", "trust"),
    ("Trusted service providers near {loc}", "local"),
]


def format_location(profile: BusinessProfile) -> str:
    """Devolve uma localização legível para as queries.

    Preferência: "City, ST" → "City" → "the {country}" → "the local area".
    """
    if profile.city and profile.state:
        return f"{profile.city}, {profile.state}"
    if profile.city:
        return profile.city
    if profile.state:
        return profile.state
    if profile.country:
        return f"the {profile.country}"
    return "the local area"


def generate_queries(profile: BusinessProfile, n: int = 10) -> list[BuyerQuery]:
    """Devolve até ``n`` queries determinísticas para testar contra o LLM.

    Distribuição alvo: 3 discovery, 2 comparison, 2 trust, 3 local.
    Se a categoria for genérica, usa o fallback puro.
    """
    loc = format_location(profile)
    cat = profile.category or "local business"

    if cat == "local business":
        queries = [
            BuyerQuery(text=t.format(loc=loc), intent=intent)
            for t, intent in _GENERIC
        ]
    else:
        target_per_intent = {"discovery": 3, "comparison": 2, "trust": 2, "local": 3}
        queries = []
        for intent, k in target_per_intent.items():
            for tmpl in _TEMPLATES[intent][:k]:
                queries.append(BuyerQuery(text=tmpl.format(cat=cat, loc=loc), intent=intent))

    # deduplicar preservando ordem (case-insensitive)
    seen: set[str] = set()
    unique: list[BuyerQuery] = []
    for q in queries:
        key = q.text.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(q)
        if len(unique) >= n:
            break
    return unique
