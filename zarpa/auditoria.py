"""Visita o site de cada lead e recolhe evidências para o icebreaker.

Não escreve o icebreaker: isso é trabalho do agente ``icebreaker-writer``,
que lê estas evidências, confirma-as e escreve uma frase com um facto real.

Classificação do ICP (``lead["icp"]["situacao"]``):

- ``sem_site``: nem site nem redes;
- ``so_redes``: o "site" é Facebook/Instagram;
- ``site_fraco``: tem site com pelo menos um problema da lista ``PROBLEMAS``;
- ``site_bom``: nenhum problema encontrado → **fora da campanha**.
"""

from __future__ import annotations

import re
from datetime import date

import requests

from . import http
from .config import chave

AGENTE = "Mozilla/5.0 (compatible; ZarpaAudit/0.1; +https://zarpa.pt)"
PSI = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

MARCACAO = re.compile(
    r"marcar\s+consulta|marca[çc][ãa]o\s+online|marca[çc][õo]es|agendar|agende|agendamento|"
    r"book\s+(an\s+)?appointment|booking|doctoralia|marcar\s+online", re.I)
COPYRIGHT = re.compile(r"(?:©|&copy;|copyright)\s*(?:\d{4}\s*[-–]\s*)?(20\d{2})", re.I)
VIEWPORT = re.compile(r"<meta[^>]+name=[\"']viewport[\"']", re.I)
GERADOR = re.compile(r"<meta[^>]+name=[\"']generator[\"'][^>]+content=[\"']([^\"']+)", re.I)
TITULO = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)

PROBLEMAS = {
    "sem_resposta": "O site não abre",
    "sem_https": "O site não tem HTTPS (o navegador mostra 'não seguro')",
    "sem_viewport": "O site não está adaptado ao telemóvel",
    "sem_marcacao": "Não há forma de marcar consulta online",
    "desatualizado": "O site parece desatualizado (copyright antigo)",
    "lento": "O site é lento no telemóvel (PageSpeed baixo)",
}


def analisar_html(html: str, url_final: str, ano_atual: int | None = None) -> dict:
    """Extrai os sinais do HTML. Função pura (testável sem rede)."""
    ano_atual = ano_atual or date.today().year
    anos = [int(a) for a in COPYRIGHT.findall(html)]
    ano = max(anos) if anos else None
    titulo = TITULO.search(html)
    gerador = GERADOR.search(html)
    return {
        "url_final": url_final,
        "https": url_final.lower().startswith("https://"),
        "viewport": bool(VIEWPORT.search(html)),
        "marcacao": bool(MARCACAO.search(html)),
        "ano_copyright": ano,
        "desatualizado": ano is not None and ano < ano_atual - 2,
        "titulo": re.sub(r"\s+", " ", titulo.group(1)).strip()[:120] if titulo else None,
        "gerador": gerador.group(1)[:60] if gerador else None,
    }


def pagespeed_movel(url: str) -> int | None:
    """Nota de desempenho no telemóvel (0–100). A chave é opcional."""
    params = {"url": url, "strategy": "mobile", "category": "performance"}
    k = chave("pagespeed", obrigatoria=False)
    if k:
        params["key"] = k
    try:
        r = http.pedido("pagespeed", "GET", PSI, params=params, timeout=120)
        return round(r["lighthouseResult"]["categories"]["performance"]["score"] * 100)
    except Exception:
        return None


def auditar(lead: dict, com_pagespeed: bool = False, ano_atual: int | None = None) -> dict:
    site = lead.get("site")
    evid: list[str] = []
    g = lead.get("google") or {}
    if g.get("nota") and g.get("avaliacoes"):
        evid.append(f"Google: {g['nota']} em {g['avaliacoes']} avaliações")
    if g.get("marcacao_link"):
        evid.append(f"A ficha Google tem link de marcação: {g['marcacao_link']}")

    if not site:
        situacao = "so_redes" if lead.get("redes") else "sem_site"
        if situacao == "so_redes":
            evid.append("O 'site' é uma rede social: " + ", ".join(lead["redes"].values()))
        else:
            evid.append("Sem site nem redes sociais encontradas")
        aud = {"site": None, "problemas": [situacao]}
    else:
        url = site if "://" in site else "http://" + site
        try:
            r = requests.get(url, headers={"User-Agent": AGENTE}, timeout=20, allow_redirects=True)
            sinais = analisar_html(r.text if r.ok else "", r.url, ano_atual)
            sinais["estado_http"] = r.status_code
        except requests.RequestException as e:
            sinais = {"url_final": url, "erro": type(e).__name__, "estado_http": None}
        problemas = []
        if not sinais.get("estado_http") or sinais["estado_http"] >= 400:
            problemas.append("sem_resposta")
        else:
            if not sinais["https"]:
                problemas.append("sem_https")
            if not sinais["viewport"]:
                problemas.append("sem_viewport")
            if not sinais["marcacao"] and not g.get("marcacao_link"):
                problemas.append("sem_marcacao")
            if sinais["desatualizado"]:
                problemas.append("desatualizado")
            if com_pagespeed:
                sinais["pagespeed_movel"] = pagespeed_movel(sinais["url_final"])
                if sinais["pagespeed_movel"] is not None and sinais["pagespeed_movel"] < 50:
                    problemas.append("lento")
        situacao = "site_fraco" if problemas else "site_bom"
        evid += [f"{PROBLEMAS[p]} ({sinais.get('url_final')})" for p in problemas]
        if sinais.get("ano_copyright"):
            evid.append(f"Último ano de copyright no site: {sinais['ano_copyright']}")
        if sinais.get("pagespeed_movel") is not None:
            evid.append(f"PageSpeed no telemóvel: {sinais['pagespeed_movel']}/100")
        aud = {"site": site, **sinais, "problemas": problemas}

    lead["auditoria"] = {**aud, "evidencias": evid, "data": date.today().isoformat()}
    lead["icp"] = {"situacao": situacao, "elegivel": situacao != "site_bom"}
    return lead["auditoria"]
