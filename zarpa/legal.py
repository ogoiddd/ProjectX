"""Filtro legal: quem pode receber cold email e para que endereço.

Regras (ver ``vendas/email/plano.md`` §1):

- Só **sociedades** (Lda, Unipessoal Lda, SA). Pessoas singulares, incluindo
  os profissionais em nome individual, precisam de consentimento prévio
  (Lei 41/2004, art. 13.º-A) e ficam para o canal telefone.
- Fora quem está na **lista de oposição** ou na nossa **supressão**.
- O email tem de estar verificado (``ok``) e ser **do domínio da clínica**
  ou **publicado pela própria clínica** (site ou ficha Google). Emails
  gratuitos (gmail, sapo...) só se forem o contacto publicado.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

from .config import EMAIL_GENERICO, EMAIL_GRATUITO, OPOSICAO, SUPRESSAO
from .modelo import dominio
from .verificar import APROVADO, ARRISCADO

SOCIEDADE = re.compile(r"\b(lda|limitada|unipessoal|s\.?\s?a\.?|sociedade|s\.?a\.?r\.?l)\b\.?", re.I)
TITULO_PESSOAL = re.compile(r"^\s*(dr|dra|drª|doutor|doutora|prof)\.?\s", re.I)


def tipo_entidade(lead: dict) -> str:
    """``sociedade`` se a denominação o mostrar; ``provavel_eni`` se for o nome de uma pessoa."""
    if lead.get("tipo_entidade") in ("sociedade", "eni"):
        return lead["tipo_entidade"]  # confirmado à mão ou pelo agente
    texto = " ".join(filter(None, [lead.get("denominacao_social"), lead.get("nome")]))
    if SOCIEDADE.search(texto):
        return "sociedade"
    if TITULO_PESSOAL.search(lead.get("nome") or ""):
        return "provavel_eni"
    return "desconhecido"


def ler_lista(caminho: Path) -> set[str]:
    """Lê todos os valores (emails, domínios, NIFs) de um CSV, em minúsculas."""
    if not caminho.exists():
        return set()
    valores = set()
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        for linha in csv.reader(f):
            for v in linha:
                v = v.strip().lower()
                if v and v not in ("email", "dominio", "nif", "motivo", "data"):
                    valores.add(v)
    return valores


def na_lista(lead: dict, lista: set[str]) -> bool:
    alvos = {e["endereco"] for e in lead["emails"]}
    alvos |= {e["endereco"].split("@")[1] for e in lead["emails"]}
    if dominio(lead.get("site")):
        alvos.add(dominio(lead["site"]))
    if lead.get("nif"):
        alvos.add(re.sub(r"\D", "", lead["nif"]))
    return bool(alvos & lista)


def e_generico(endereco: str) -> bool:
    local = endereco.split("@")[0]
    return any(local == p or local.startswith(p + ".") or local.startswith(p + "_") for p in EMAIL_GENERICO)


def email_permitido(e: dict, dom_empresa: str | None, aceitar_catch_all: bool) -> bool:
    estados = APROVADO | (ARRISCADO if aceitar_catch_all else set())
    if e.get("mv_resultado") not in estados:
        return False
    dom_email = e["endereco"].split("@")[1]
    if dom_email in EMAIL_GRATUITO:
        return bool(e["publicado_pela_empresa"])
    return dom_email == dom_empresa or bool(e["publicado_pela_empresa"])


def escolher_email(lead: dict, aceitar_catch_all: bool = False) -> dict | None:
    """O melhor endereço permitido: o do decisor no domínio da clínica, senão um genérico."""
    dom = dominio(lead.get("site"))
    permitidos = [e for e in lead["emails"] if email_permitido(e, dom, aceitar_catch_all)]
    if not permitidos:
        return None
    nominativos = [e for e in permitidos if not e_generico(e["endereco"])
                   and e["endereco"].split("@")[1] == dom]
    ordem = nominativos + [e for e in permitidos if e not in nominativos]
    return sorted(ordem, key=lambda e: e["mv_resultado"] != "ok")[0]


def filtrar(leads: list[dict], aceitar_catch_all: bool = False,
            oposicao: set[str] | None = None, supressao: set[str] | None = None) -> dict[str, int]:
    """Marca ``lead["legal"]`` e ``lead["email_envio"]``. Devolve a contagem de motivos."""
    oposicao = ler_lista(OPOSICAO) if oposicao is None else oposicao
    supressao = ler_lista(SUPRESSAO) if supressao is None else supressao
    contagem: dict[str, int] = {}
    for lead in leads:
        motivos = []
        lead["tipo_entidade"] = tipo_entidade(lead)
        if lead["tipo_entidade"] != "sociedade":
            motivos.append(f"entidade:{lead['tipo_entidade']}")
        if na_lista(lead, oposicao):
            motivos.append("lista_oposicao")
        if na_lista(lead, supressao):
            motivos.append("supressao")
        escolhido = escolher_email(lead, aceitar_catch_all)
        if not escolhido:
            motivos.append("sem_email_permitido")
        lead["email_envio"] = escolhido["endereco"] if escolhido else None
        lead["legal"] = {"elegivel": not motivos, "motivos": motivos}
        for m in motivos or ["elegivel"]:
            contagem[m] = contagem.get(m, 0) + 1
    return contagem


def suprimir(endereco: str, motivo: str, data: str) -> None:
    """Acrescenta um email à supressão global (SAIR, pedido de não contacto...)."""
    novo = not SUPRESSAO.exists()
    with open(SUPRESSAO, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if novo:
            w.writerow(["email", "motivo", "data"])
        w.writerow([endereco.lower(), motivo, data])
