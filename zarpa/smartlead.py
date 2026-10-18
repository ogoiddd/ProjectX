"""Exportação para o Smartlead e sincronização dos resultados.

API: ``https://server.smartlead.ai/api/v1`` com ``?api_key=`` (chave em
``SMARTLEAD_API_KEY``).

- ``POST /campaigns/{id}/leads``: até 400 leads por pedido, com
  ``custom_fields`` (os ``{{campos}}`` dos emails).
- ``GET /campaigns/{id}/leads``: estado e categoria de cada lead.
- ``GET /leads/fetch-categories``: nomes das categorias (Interested, ...).

``enviar`` corre em modo de ensaio por omissão: grava o que seria enviado e
não toca no Smartlead. Só envia com ``ensaio=False`` (``--a-serio`` na CLI),
depois de aprovares o ``envio.csv``.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from datetime import date
from pathlib import Path

from . import http
from .config import SUPRESSAO, chave, pasta_campanha
from .legal import ler_lista, suprimir

BASE = "https://server.smartlead.ai/api/v1"
POR_PEDIDO = 400

FONTE_TEXTO = {
    "gmaps": "na vossa ficha do Google",
    "gmaps:site": "no vosso site",
    "aiark": "numa base de dados profissional (AI Ark)",
    "quickenrich:site": "no vosso site",
    "quickenrich": "numa base de dados profissional (QuickEnrich)",
}

COLUNAS = ["lead_id", "email", "variante", "saudacao", "primeiro_nome", "clinica", "cidade",
           "especialidade", "icebreaker", "icebreaker_fonte", "concorrente", "n_avaliacoes",
           "nota", "fonte_contacto", "telefone", "site", "precisa_maquete"]

# Termo de pesquisa por sub-nicho (o que vai em "{{especialidade}} {{cidade}}").
ESPECIALIDADE = {"dentaria": "dentista", "fisioterapia": "fisioterapia",
                 "estetica": "clínica de estética", "veterinaria": "veterinário"}

POSITIVAS = {"interested", "meeting request", "information request"}
NEGATIVAS = {"not interested", "wrong person"}
NAO_CONTACTAR = {"do not contact"}


def variante(lead_id: str, campanha: str) -> str:
    """A ou B, estável e aleatória (hash do id + campanha)."""
    return "AB"[hashlib.sha256(f"{campanha}:{lead_id}".encode()).digest()[0] % 2]


SUFIXO_LEGAL = re.compile(r"[\s,]*\b(unipessoal\s+)?(lda|limitada|s\.?\s?a)\b\.?\s*$", re.I)


def nome_comercial(nome: str) -> str:
    """``Clínica Sorriso, Lda.`` -> ``Clínica Sorriso`` (o email fala da clínica, não da firma)."""
    return SUFIXO_LEGAL.sub("", nome).strip() or nome


def fonte_contacto(lead: dict) -> str:
    e = next((x for x in lead["emails"] if x["endereco"] == lead["email_envio"]), None)
    f = (e or {}).get("fonte", "")
    if f in FONTE_TEXTO:
        return FONTE_TEXTO[f]
    if f.startswith("csv:"):
        return f"numa base de dados profissional ({f[4:]})"
    return "numa fonte pública"


def linha_envio(lead: dict, campanha: str) -> dict:
    d = lead.get("decisor") or {}
    primeiro = d.get("primeiro_nome") or ((d.get("nome") or "").split() or [None])[0]
    g = lead.get("google") or {}
    var = lead.get("variante") or variante(lead["id"], campanha)
    tel = next((t["numero"] for t in lead["telefones"] if t.get("valido")), None)
    return {
        "lead_id": lead["id"],
        "email": lead["email_envio"],
        "variante": var,
        # Nunca se adivinha "Dr."/"Dra." a partir do nome; o agente pode pôr a
        # saudação à mão se a clínica usar o título publicamente.
        "saudacao": lead.get("saudacao") or (f"Bom dia, {primeiro}" if primeiro else "Bom dia"),
        "primeiro_nome": primeiro or "",
        "clinica": nome_comercial(lead["nome"]),
        "cidade": lead.get("cidade") or "",
        "especialidade": ESPECIALIDADE.get(lead.get("subnicho") or "", lead.get("subnicho") or ""),
        "icebreaker": lead.get("icebreaker") or "",
        "icebreaker_fonte": lead.get("icebreaker_fonte") or "",
        "concorrente": lead.get("concorrente") or "",
        "n_avaliacoes": g.get("avaliacoes") or "",
        "nota": str(g.get("nota") or "").replace(".", ","),
        "fonte_contacto": fonte_contacto(lead),
        "telefone": tel or "",
        "site": lead.get("site") or "",
        "precisa_maquete": "sim" if var == "A" else "não",
    }


def prontos(leads: list[dict]) -> list[dict]:
    """Leads que podem seguir: legal ✔, ICP ✔, email escolhido e icebreaker escrito."""
    return [l for l in leads
            if (l.get("legal") or {}).get("elegivel") and (l.get("icp") or {}).get("elegivel")
            and l.get("email_envio") and l.get("icebreaker")]


def exportar(leads: list[dict], campanha: str) -> Path:
    p = pasta_campanha(campanha) / "envio.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS)
        w.writeheader()
        for l in prontos(leads):
            w.writerow(linha_envio(l, campanha))
    return p


def ler_envio(campanha: str) -> list[dict]:
    with open(pasta_campanha(campanha) / "envio.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def para_smartlead(linha: dict) -> dict:
    campos = {k: str(v) for k, v in linha.items() if k not in ("email",)}
    return {
        "email": linha["email"],
        "first_name": linha["primeiro_nome"],
        "company_name": linha["clinica"],
        "website": linha["site"],
        "location": linha["cidade"],
        "phone_number": linha["telefone"],
        "custom_fields": campos,
    }


def enviar(campanha: str, id_campanha_smartlead: int, variante_filtro: str | None = None,
           ensaio: bool = True) -> dict:
    """Envia o ``envio.csv`` (já aprovado) para a campanha do Smartlead."""
    linhas = [l for l in ler_envio(campanha) if not variante_filtro or l["variante"] == variante_filtro]
    lotes = [linhas[i:i + POR_PEDIDO] for i in range(0, len(linhas), POR_PEDIDO)]
    corpos = [{"lead_list": [para_smartlead(l) for l in lote],
               "settings": {"ignore_global_block_list": False, "ignore_unsubscribe_list": False,
                            "ignore_duplicate_leads_in_other_campaign": False,
                            "ignore_community_bounce_list": False}} for lote in lotes]
    if ensaio:
        p = pasta_campanha(campanha) / f"ensaio-smartlead-{id_campanha_smartlead}.json"
        p.write_text(json.dumps(corpos, ensure_ascii=False, indent=1))
        return {"ensaio": True, "leads": len(linhas), "ficheiro": str(p)}
    total = {"added_count": 0, "skipped_count": 0, "skipped_leads": []}
    for corpo in corpos:
        r = http.pedido("smartlead", "POST", f"{BASE}/campaigns/{id_campanha_smartlead}/leads",
                        params={"api_key": chave("smartlead")}, json=corpo)
        total["added_count"] += r.get("added_count") or 0
        total["skipped_count"] += r.get("skipped_count") or 0
        total["skipped_leads"] += r.get("skipped_leads") or []
    return total


# --------------------------------------------------------------------------- #
# Resultados
# --------------------------------------------------------------------------- #
def _leads_campanha(id_campanha: int, **filtros) -> list[dict]:
    todos, offset = [], 0
    while True:
        r = http.pedido("smartlead", "GET", f"{BASE}/campaigns/{id_campanha}/leads",
                        params={"api_key": chave("smartlead"), "offset": offset, "limit": 100, **filtros})
        dados = r.get("data") or []
        todos += dados
        if len(dados) < 100:
            return todos
        offset += 100


def categorias() -> dict[int, str]:
    r = http.pedido("smartlead", "GET", f"{BASE}/leads/fetch-categories",
                    params={"api_key": chave("smartlead")})
    itens = r if isinstance(r, list) else (r or {}).get("data", [])
    return {c["id"]: c["name"] for c in itens}


def classificar(item: dict, cats: dict[int, str], bounced: set[str], replied: set[str]) -> list[str]:
    """Eventos de um lead do Smartlead (função pura)."""
    email = (item.get("lead") or {}).get("email", "").lower()
    eventos = []
    if item.get("status") not in (None, "STARTED"):
        eventos.append("enviado")
    if email in bounced:
        eventos.append("bounce")
    cat = (cats.get(item.get("lead_category_id")) or "").strip().lower()
    if (item.get("lead") or {}).get("is_unsubscribed") or cat in NAO_CONTACTAR:
        eventos.append("opt_out")
    elif cat in POSITIVAS:
        eventos.append("resposta_positiva")
    elif cat in NEGATIVAS:
        eventos.append("resposta_negativa")
    elif email in replied:
        eventos.append("resposta_neutra")
    return eventos


def sincronizar(campanha: str, id_campanha_smartlead: int) -> Path:
    """Reescreve ``resultados.csv`` = eventos do Smartlead + ``eventos-manuais.csv``."""
    pasta = pasta_campanha(campanha)
    envio = {l["email"].lower(): l for l in ler_envio(campanha)}
    cats = categorias()
    bounced = {(i.get("lead") or {}).get("email", "").lower()
               for i in _leads_campanha(id_campanha_smartlead, emailStatus="bounced")}
    replied = {(i.get("lead") or {}).get("email", "").lower()
               for i in _leads_campanha(id_campanha_smartlead, emailStatus="replied")}
    hoje = date.today().isoformat()
    ja_suprimidos = ler_lista(SUPRESSAO)
    linhas = []
    for item in _leads_campanha(id_campanha_smartlead):
        email = (item.get("lead") or {}).get("email", "").lower()
        base = envio.get(email, {})
        for ev in classificar(item, cats, bounced, replied):
            linhas.append({"lead_id": base.get("lead_id", email), "campanha": campanha,
                           "variante": base.get("variante", ""), "data": hoje, "evento": ev, "valor": ""})
            if ev == "opt_out" and email not in ja_suprimidos:
                suprimir(email, "smartlead:" + ev, hoje)
                ja_suprimidos.add(email)
    manuais = pasta / "eventos-manuais.csv"
    if manuais.exists():
        with open(manuais, newline="", encoding="utf-8") as f:
            linhas += list(csv.DictReader(f))
    p = pasta / "resultados.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["lead_id", "campanha", "variante", "data", "evento", "valor"])
        w.writeheader()
        w.writerows(linhas)
    return p


EVENTOS_MANUAIS = {"reuniao_marcada", "reuniao_feita", "proposta", "venda", "perdido"}


def registar_evento(campanha: str, lead_id: str, evento: str, valor: str = "") -> Path:
    """O Diogo regista o que acontece fora do email (reuniões, propostas, vendas)."""
    if evento not in EVENTOS_MANUAIS:
        raise ValueError(f"Evento desconhecido: {evento}. Usar um de {sorted(EVENTOS_MANUAIS)}.")
    envio = {l["lead_id"]: l for l in ler_envio(campanha)}
    p = pasta_campanha(campanha) / "eventos-manuais.csv"
    novo = not p.exists()
    with open(p, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["lead_id", "campanha", "variante", "data", "evento", "valor"])
        if novo:
            w.writeheader()
        w.writerow({"lead_id": lead_id, "campanha": campanha,
                    "variante": envio.get(lead_id, {}).get("variante", ""),
                    "data": date.today().isoformat(), "evento": evento, "valor": valor})
    return p
