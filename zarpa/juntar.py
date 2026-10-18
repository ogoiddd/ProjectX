"""Junta os leads das várias fontes e remove duplicados.

Dois leads são o mesmo negócio se partilharem o domínio do site, um telefone
ou o par nome + cidade (normalizados).
"""

from __future__ import annotations

from .modelo import dominio, slug
from .telefone import normalizar as normalizar_telefone

PALAVRAS_VAZIAS = {"clinica", "dentaria", "medica", "centro", "lda", "unipessoal", "sa", "de", "do", "da", "e"}


def _chave_nome(lead: dict) -> str:
    palavras = [p for p in slug(lead["nome"]).split("-") if p not in PALAVRAS_VAZIAS]
    return "-".join(palavras) + "|" + slug(lead.get("cidade") or "")


def chaves(lead: dict) -> set[str]:
    k = {"nome:" + _chave_nome(lead)}
    if dominio(lead.get("site")):
        k.add("dom:" + dominio(lead["site"]))
    for t in lead["telefones"]:
        n = normalizar_telefone(t["numero"])
        if n:
            k.add("tel:" + n)
    return k


def fundir(a: dict, b: dict) -> dict:
    """Junta ``b`` em ``a`` (``a`` ganha nos campos já preenchidos)."""
    for k, v in b.items():
        if k in ("emails", "telefones", "fontes", "redes"):
            continue
        if a.get(k) in (None, "", "desconhecido") and v not in (None, ""):
            a[k] = v
    if b.get("google") and not a.get("google"):
        a["google"] = b["google"]
    a["redes"] = {**b.get("redes", {}), **a.get("redes", {})}
    a["fontes"] = sorted(set(a["fontes"]) | set(b["fontes"]))
    vistos = {e["endereco"] for e in a["emails"]}
    for e in b["emails"]:
        if e["endereco"] in vistos:
            ea = next(x for x in a["emails"] if x["endereco"] == e["endereco"])
            ea["publicado_pela_empresa"] = ea["publicado_pela_empresa"] or e["publicado_pela_empresa"]
        else:
            a["emails"].append(e)
    tels = {normalizar_telefone(t["numero"]) for t in a["telefones"]}
    a["telefones"] += [t for t in b["telefones"] if normalizar_telefone(t["numero"]) not in tels]
    return a


def juntar(leads: list[dict]) -> list[dict]:
    """Funde os duplicados mantendo a ordem da primeira ocorrência."""
    resultado: list[dict] = []
    indice: dict[str, int] = {}
    for lead in leads:
        ks = chaves(lead)
        destinos = sorted({indice[k] for k in ks if k in indice})
        if not destinos:
            resultado.append(lead)
            pos = len(resultado) - 1
        else:
            pos = destinos[0]
            fundir(resultado[pos], lead)
            for outro in destinos[1:]:  # o lead novo ligou dois que já existiam
                fundir(resultado[pos], resultado[outro])
                resultado[outro] = None  # type: ignore[call-overload]
                for k, i in indice.items():
                    if i == outro:
                        indice[k] = pos
        for k in chaves(resultado[pos]):
            indice[k] = pos
    finais = [l for l in resultado if l is not None]
    usados: set[str] = set()
    for l in finais:  # ids únicos
        base, n = l["id"], 2
        while l["id"] in usados:
            l["id"] = f"{base}-{n}"
            n += 1
        usados.add(l["id"])
    return finais


def ja_contactados(leads: list[dict], emails_antigos: set[str]) -> list[dict]:
    """Tira os leads cujo email já esteve noutra campanha."""
    return [l for l in leads if not any(e["endereco"] in emails_antigos for e in l["emails"])]


def emails_de(leads: list[dict]) -> set[str]:
    return {e["endereco"] for l in leads for e in l["emails"]}

