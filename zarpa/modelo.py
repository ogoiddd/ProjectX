"""Modelo de lead (dicionário JSON) e leitura/escrita da campanha.

Um lead é um ``dict`` com este formato (os campos ausentes valem ``None``):

.. code-block:: text

    id, nome, denominacao_social, nif, tipo_entidade, subnicho,
    cidade, morada, codigo_postal, site,
    emails:    [{endereco, fonte, publicado_pela_empresa, mv_resultado, mv_qualidade}]
    telefones: [{numero, fonte, tipo, valido}]
    decisor:   {nome, primeiro_nome, cargo, fonte, linkedin}
    google:    {place_id, nota, avaliacoes, link, marcacao_link, estado}
    redes:     {facebook, instagram}
    fontes:    ["gmaps", "aiark", "csv:getleads", ...]
    auditoria, icp, legal, email_envio, icebreaker, icebreaker_fonte, variante
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

from .config import pasta_campanha

REDES = ("facebook.com", "instagram.com", "fb.com", "linktr.ee", "tiktok.com")


def slug(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def dominio(url: str | None) -> str | None:
    """``https://www.Clinica.pt/x`` -> ``clinica.pt``. Redes sociais -> ``None``."""
    if not url:
        return None
    if "://" not in url:
        url = "http://" + url
    host = (urlparse(url).hostname or "").lower()
    host = host.removeprefix("www.")
    if not host or "." not in host or any(host.endswith(r) for r in REDES):
        return None
    return host


def e_rede_social(url: str | None) -> bool:
    if not url:
        return False
    if "://" not in url:
        url = "http://" + url
    host = (urlparse(url).hostname or "").lower()
    return any(host.endswith(r) for r in REDES)


def novo_lead(nome: str, cidade: str | None, fonte: str, **campos: Any) -> dict:
    lead = {
        "id": slug(f"{nome}-{cidade or ''}"),
        "nome": nome.strip(),
        "denominacao_social": None,
        "nif": None,
        "tipo_entidade": "desconhecido",
        "subnicho": None,
        "cidade": cidade,
        "morada": None,
        "codigo_postal": None,
        "site": None,
        "emails": [],
        "telefones": [],
        "decisor": None,
        "google": None,
        "redes": {},
        "fontes": [fonte],
    }
    lead.update({k: v for k, v in campos.items() if v is not None})
    return lead


def adicionar_email(lead: dict, endereco: str | None, fonte: str,
                    publicado_pela_empresa: bool) -> None:
    if not endereco:
        return
    endereco = endereco.strip().lower()
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", endereco):
        return
    for e in lead["emails"]:
        if e["endereco"] == endereco:
            e["publicado_pela_empresa"] = e["publicado_pela_empresa"] or publicado_pela_empresa
            return
    lead["emails"].append({
        "endereco": endereco,
        "fonte": fonte,
        "publicado_pela_empresa": publicado_pela_empresa,
        "mv_resultado": None,
        "mv_qualidade": None,
    })


def adicionar_telefone(lead: dict, numero: str | None, fonte: str) -> None:
    if not numero:
        return
    digitos = re.sub(r"\D", "", numero)
    if any(re.sub(r"\D", "", t["numero"]) == digitos for t in lead["telefones"]):
        return
    lead["telefones"].append({"numero": numero.strip(), "fonte": fonte, "tipo": None, "valido": None})


# --------------------------------------------------------------------------- #
# Ficheiros da campanha
# --------------------------------------------------------------------------- #
def caminho_leads(campanha: str) -> Path:
    return pasta_campanha(campanha) / "leads.json"


def carregar(campanha: str) -> list[dict]:
    p = caminho_leads(campanha)
    return json.loads(p.read_text()) if p.exists() else []


def gravar(campanha: str, leads: Iterable[dict]) -> Path:
    p = caminho_leads(campanha)
    p.write_text(json.dumps(list(leads), ensure_ascii=False, indent=1))
    return p


def gravar_bruto(campanha: str, nome: str, dados: Any) -> Path:
    """Guarda a resposta crua de uma API, para não pagar duas vezes."""
    pasta = pasta_campanha(campanha) / "brutos"
    pasta.mkdir(exist_ok=True)
    p = pasta / f"{nome}.json"
    p.write_text(json.dumps(dados, ensure_ascii=False, indent=1))
    return p
