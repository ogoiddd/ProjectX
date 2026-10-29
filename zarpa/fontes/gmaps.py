"""Google Maps via Outscraper (https://outscraper.com).

É a fonte principal para as clínicas **sem site**, que as bases B2B quase não
têm. Cada pesquisa ("clínica dentária, Faro, Portugal") devolve as fichas do
Google: nome, morada, telefone, site, nota, nº de avaliações e link de
marcação. Com ``enrichment=domains_service`` a Outscraper visita o site e
junta emails e redes sociais (campos ``email_1``, ``email_2``, ...).

Chave em ``OUTSCRAPER_API_KEY``.
"""

from __future__ import annotations

import re
import time
from typing import Any, Iterable

from .. import http
from ..config import chave
from ..modelo import adicionar_email, adicionar_telefone, dominio, e_rede_social, novo_lead

BASE = "https://api.app.outscraper.com"
PAUSA = 5  # segundos entre consultas ao pedido assíncrono
ESPERA_MAX = 60 * 60

# Pesquisas por sub-nicho (o termo que as pessoas usam no Google).
PESQUISAS = {
    "dentaria": ["clínica dentária", "dentista"],
    "fisioterapia": ["clínica de fisioterapia", "fisioterapeuta"],
    "estetica": ["clínica de estética", "medicina estética"],
    "veterinaria": ["clínica veterinária", "veterinário"],
}


def montar_pesquisas(subnicho: str, cidades: Iterable[str]) -> list[str]:
    termos = PESQUISAS.get(subnicho, [subnicho])
    return [f"{t}, {c}, Portugal" for c in cidades for t in termos]


def pesquisar(pesquisas: list[str], limite: int = 100, enriquecer: bool = True) -> list[dict]:
    """Corre as pesquisas e devolve a lista plana de fichas (dicts crus)."""
    cab = {"X-API-KEY": chave("outscraper")}
    corpo = {
        "query": pesquisas,
        "language": "pt",
        "region": "PT",
        "organizationsPerQueryLimit": limite,
        "dropDuplicates": True,
        "async": True,
        "enrichment": ["domains_service"] if enriquecer else "",
    }
    pedido = http.pedido("outscraper", "POST", f"{BASE}/google-maps-search", headers=cab, json=corpo)
    resultado = _esperar(pedido["id"], cab)
    return achatar(resultado.get("data", []))


def _esperar(id_pedido: str, cab: dict) -> dict:
    inicio = time.monotonic()
    while time.monotonic() - inicio < ESPERA_MAX:
        r = http.pedido("outscraper", "GET", f"{BASE}/requests/{id_pedido}", headers=cab)
        if r.get("status") != "Pending":
            return r
        time.sleep(PAUSA)
    raise TimeoutError(f"Outscraper: o pedido {id_pedido} não terminou numa hora.")


def achatar(dados: Any) -> list[dict]:
    """A resposta vem como uma lista por pesquisa. Junta tudo numa lista."""
    fichas: list[dict] = []
    for item in dados or []:
        if isinstance(item, list):
            fichas.extend(x for x in item if isinstance(x, dict))
        elif isinstance(item, dict):
            fichas.append(item)
    return fichas


def para_lead(ficha: dict, subnicho: str) -> dict | None:
    """Converte uma ficha da Outscraper num lead. Ignora negócios fechados."""
    nome = ficha.get("name")
    if not nome or ficha.get("business_status") in ("CLOSED_PERMANENTLY", "CLOSED_TEMPORARILY"):
        return None
    site = ficha.get("site") or None
    lead = novo_lead(
        nome, ficha.get("city"), "gmaps",
        subnicho=subnicho,
        morada=ficha.get("full_address"),
        codigo_postal=ficha.get("postal_code"),
        site=None if e_rede_social(site) else site,
    )
    lead["google"] = {
        "place_id": ficha.get("place_id"),
        "nota": ficha.get("rating"),
        "avaliacoes": ficha.get("reviews"),
        "link": ficha.get("location_link"),
        "marcacao_link": ficha.get("booking_appointment_link"),
        "categoria": ficha.get("category") or ficha.get("type"),
        "verificado": ficha.get("verified"),
    }
    if e_rede_social(site):
        lead["redes"][_rede(site)] = site
    for k in ("facebook", "instagram"):
        if ficha.get(k):
            lead["redes"][k] = ficha[k]
    adicionar_telefone(lead, ficha.get("phone"), "gmaps")
    for k in sorted(ficha):
        if re.fullmatch(r"phone_\d+", k):
            adicionar_telefone(lead, ficha[k], "gmaps:site")
    # Emails encontrados no site da própria clínica contam como publicados por ela.
    dom = dominio(lead["site"])
    for k in sorted(ficha):
        if re.fullmatch(r"email_\d+", k) and ficha[k]:
            no_dominio = bool(dom) and ficha[k].lower().endswith("@" + dom)
            adicionar_email(lead, ficha[k], "gmaps:site", publicado_pela_empresa=True)
            if ficha.get(f"{k}_full_name") and no_dominio and not lead["decisor"]:
                lead["decisor"] = {
                    "nome": ficha[f"{k}_full_name"],
                    "cargo": ficha.get(f"{k}_title"),
                    "fonte": "gmaps:site",
                }
    return lead


def _rede(url: str) -> str:
    return "instagram" if "instagram" in url else "facebook" if "fb" in url or "facebook" in url else "outra"
