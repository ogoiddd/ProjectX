"""AI Ark (https://ai-ark.com): decisores de clínicas com site.

Fluxo da API (``X-TOKEN`` com a chave em ``AIARK_API_KEY``):

1. ``POST /v1/people`` com filtros de empresa (``account``) e de pessoa
   (``contact``). Cada página devolve pessoas **sem email** e um ``trackId``.
2. ``POST /v1/people/email-finder`` com esse ``trackId`` (uso único,
   expira em 6 h) para lançar a procura de emails.
3. ``GET /v1/people/email-finder/{trackId}/inquiries`` até todas as linhas
   estarem ``DONE``. Os emails vêm em ``content[].output[].address``.

Os filtros ficam em ``vendas/email/filtros/aiark-<subnicho>.json`` para se
poderem afinar sem mexer no código.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from .. import http
from ..config import PASTA_EMAIL, chave
from ..modelo import adicionar_email, dominio, novo_lead

BASE = "https://api.ai-ark.com/api/developer-portal"
PAUSA = 10
ESPERA_MAX = 30 * 60
TAMANHO_PAGINA = 100


def _cab() -> dict:
    return {"X-TOKEN": chave("aiark"), "Content-Type": "application/json"}


def carregar_filtros(subnicho: str) -> dict:
    p = PASTA_EMAIL / "filtros" / f"aiark-{subnicho}.json"
    if not p.exists():
        p = PASTA_EMAIL / "filtros" / "aiark-clinicas.json"
    return json.loads(Path(p).read_text())


def pesquisar(filtros: dict, maximo: int) -> list[tuple[list[dict], str]]:
    """Devolve ``[(pessoas, trackId), ...]``, uma entrada por página."""
    paginas = []
    total = 0
    pagina = 0
    while total < maximo:
        corpo = {**filtros, "page": pagina, "size": min(TAMANHO_PAGINA, maximo - total)}
        r = http.pedido("aiark", "POST", f"{BASE}/v1/people", headers=_cab(), json=corpo)
        pessoas = r.get("content") or []
        if not pessoas:
            break
        paginas.append((pessoas, r.get("trackId")))
        total += len(pessoas)
        if r.get("last"):
            break
        pagina += 1
        time.sleep(0.3)  # limite: 5 pedidos/s
    return paginas


def encontrar_emails(track_id: str) -> list[dict]:
    """Lança a procura de emails e espera pelo fim. Devolve as linhas ``content``."""
    http.pedido("aiark", "POST", f"{BASE}/v1/people/email-finder", headers=_cab(),
                json={"trackId": track_id})
    inicio = time.monotonic()
    while time.monotonic() - inicio < ESPERA_MAX:
        linhas = _resultados(track_id)
        if linhas and all(l.get("state") == "DONE" for l in linhas):
            return linhas
        time.sleep(PAUSA)
    raise TimeoutError(f"AI Ark: a procura de emails {track_id} não terminou.")


def _resultados(track_id: str) -> list[dict]:
    linhas, pagina = [], 0
    while True:
        r = http.pedido("aiark", "GET", f"{BASE}/v1/people/email-finder/{track_id}/inquiries",
                        headers=_cab(), params={"page": pagina, "size": 100})
        linhas.extend(r.get("content") or [])
        if r.get("last", True):
            return linhas
        pagina += 1


def _g(d: dict | None, *chaves: str):
    for k in chaves:
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    return d


def emails_por_pessoa(linhas: list[dict]) -> dict[tuple, list[str]]:
    """Mapa ``(nome, apelido, domínio)`` -> emails com estado VALID ou CATCH_ALL."""
    mapa: dict[tuple, list[str]] = {}
    for l in linhas:
        ent = l.get("input") or {}
        k = ((ent.get("firstname") or "").lower(), (ent.get("lastname") or "").lower(),
             (ent.get("domain") or "").lower().removeprefix("www."))
        bons = [o["address"] for o in l.get("output") or []
                if o.get("address") and (o.get("status") or "").upper() in ("VALID", "CATCH_ALL")]
        if bons:
            mapa.setdefault(k, []).extend(bons)
    return mapa


def para_lead(pessoa: dict, emails: dict[tuple, list[str]], subnicho: str) -> dict | None:
    empresa = pessoa.get("company") or {}
    nome_empresa = (_g(empresa, "summary", "name") or empresa.get("name")
                    or _g(pessoa, "profile", "company_name"))
    if not nome_empresa:
        return None
    site = _g(empresa, "link", "website") or _g(empresa, "link", "domain")
    dom = dominio(site)
    lead = novo_lead(nome_empresa, _g(pessoa, "location", "city"), "aiark",
                     subnicho=subnicho, site=site)
    primeiro = _g(pessoa, "profile", "first_name") or ""
    apelido = _g(pessoa, "profile", "last_name") or ""
    lead["decisor"] = {
        "nome": _g(pessoa, "profile", "full_name") or f"{primeiro} {apelido}".strip(),
        "primeiro_nome": primeiro or None,
        "cargo": _g(pessoa, "profile", "title"),
        "fonte": "aiark",
        "linkedin": _g(pessoa, "link", "linkedin"),
    }
    for e in emails.get((primeiro.lower(), apelido.lower(), dom or ""), []):
        # Email nominativo encontrado por ferramenta: não é "publicado pela empresa".
        adicionar_email(lead, e, "aiark", publicado_pela_empresa=False)
    return lead
