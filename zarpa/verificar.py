"""Verificação de emails no MillionVerifier (https://millionverifier.com).

``GET https://api.millionverifier.com/api/v3/?api=KEY&email=...&timeout=20``
devolve ``result``: ``ok``, ``catch_all``, ``unknown``, ``disposable``,
``invalid`` ou ``error``. Só ``ok`` segue para envio. ``catch_all`` pode ir
num lote à parte, pequeno, se for pedido explicitamente.

As respostas ficam em cache (``vendas/email/cache-millionverifier.json``,
fora do git) para nunca se pagar duas vezes o mesmo email.
"""

from __future__ import annotations

import json
import time
from datetime import date

from . import http
from .config import PASTA_EMAIL, chave
from .telefone import validar_lead

URL = "https://api.millionverifier.com/api/v3/"
URL_CREDITOS = "https://api.millionverifier.com/api/v3/credits"
CACHE = PASTA_EMAIL / "cache-millionverifier.json"
VALIDADE_DIAS = 30  # um resultado com mais de 30 dias volta a ser verificado

APROVADO = {"ok"}
ARRISCADO = {"catch_all"}


def _cache() -> dict:
    return json.loads(CACHE.read_text()) if CACHE.exists() else {}


def creditos() -> int | None:
    r = http.pedido("millionverifier", "GET", URL_CREDITOS, params={"api": chave("millionverifier")})
    return (r or {}).get("credits")


def verificar_email(endereco: str, cache: dict) -> dict:
    hoje = date.today()
    em_cache = cache.get(endereco)
    if em_cache and (hoje - date.fromisoformat(em_cache["data"])).days <= VALIDADE_DIAS:
        return em_cache
    r = http.pedido("millionverifier", "GET", URL, timeout=70,
                    params={"api": chave("millionverifier"), "email": endereco, "timeout": 20})
    if r.get("error"):
        raise http.ErroApi("millionverifier", 200, r["error"])
    res = {"resultado": r.get("result"), "qualidade": r.get("quality"),
           "subresultado": r.get("subresult"), "role": r.get("role"),
           "free": r.get("free"), "data": hoje.isoformat()}
    cache[endereco] = res
    return res


def verificar(leads: list[dict], pausa: float = 0.1) -> dict[str, int]:
    """Verifica todos os emails e telefones dos leads. Devolve a contagem por resultado."""
    cache = _cache()
    contagem: dict[str, int] = {}
    try:
        for lead in leads:
            validar_lead(lead)
            for e in lead["emails"]:
                if e.get("mv_resultado") in APROVADO | ARRISCADO | {"invalid", "disposable"}:
                    contagem[e["mv_resultado"]] = contagem.get(e["mv_resultado"], 0) + 1
                    continue
                res = verificar_email(e["endereco"], cache)
                e["mv_resultado"], e["mv_qualidade"] = res["resultado"], res["qualidade"]
                contagem[res["resultado"]] = contagem.get(res["resultado"], 0) + 1
                time.sleep(pausa)
    finally:
        CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1))
    return contagem
