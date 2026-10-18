"""QuickEnrich (https://quickenrich.io): empresas e decisores com email/telemóvel.

API em ``https://app.quickenrich.io`` com ``Authorization: Bearer <chave>``
(chave em ``QUICKENRICH_API_KEY``). Dois usos no pipeline:

1. **Descobrir clínicas** (``procurar_empresas``):
   ``POST /api/companies/company-finder`` com filtros ``{"campo": {"include": [...],
   "exclude": [...]}}``. Devolve site, telefone e ``home_page_email`` (o email
   que a clínica publica no próprio site). 1 crédito por empresa.
2. **Encontrar o decisor** de leads que já temos (``enriquecer``):
   - com o nome do decisor: ``GET /api/employees/search`` (nome + domínio);
   - sem nome: ``GET /api/employees/dataset-search`` (domínio + cargos),
     1 crédito por contacto devolvido com email ou telefone.

Os emails encontrados aqui seguem para o MillionVerifier como os outros.
"""

from __future__ import annotations

import json
import time

from .. import http
from ..config import PASTA_EMAIL, chave
from ..legal import e_generico
from ..modelo import adicionar_email, adicionar_telefone, dominio, novo_lead

BASE = "https://app.quickenrich.io"
POR_PAGINA = 100

# Cargos de quem decide numa clínica (português e inglês, como aparecem no LinkedIn).
CARGOS = ["sócio-gerente", "socio gerente", "gerente", "diretor clínico", "diretora clínica",
          "proprietário", "proprietária", "fundador", "fundadora", "owner", "founder",
          "co-founder", "ceo", "managing partner", "medical director", "clinical director"]


def _cab() -> dict:
    return {"Authorization": f"Bearer {chave('quickenrich')}", "Accept": "application/json"}


def carregar_filtros(subnicho: str) -> dict:
    p = PASTA_EMAIL / "filtros" / f"quickenrich-{subnicho}.json"
    if not p.exists():
        p = PASTA_EMAIL / "filtros" / "quickenrich-clinicas.json"
    return json.loads(p.read_text())


# --------------------------------------------------------------------------- #
# 1. Descobrir clínicas
# --------------------------------------------------------------------------- #
def procurar_empresas(filtros: dict, maximo: int) -> list[dict]:
    empresas: list[dict] = []
    pagina = 1
    while len(empresas) < maximo:
        corpo = {**filtros, "page": pagina, "per_page": min(POR_PAGINA, maximo - len(empresas))}
        r = http.pedido("quickenrich", "POST", f"{BASE}/api/companies/company-finder",
                        headers=_cab(), json=corpo)
        dados = (r or {}).get("data") or []
        empresas += dados
        meta = (r or {}).get("meta") or {}
        if not dados or pagina >= (meta.get("last_page") or pagina):
            break
        pagina += 1
        time.sleep(0.5)  # limite: 120 pedidos/min
    return empresas[:maximo]


def empresa_para_lead(e: dict, subnicho: str) -> dict | None:
    if not e.get("company_name"):
        return None
    lead = novo_lead(e["company_name"], e.get("city"), "quickenrich",
                     subnicho=subnicho, site=e.get("url"))
    # O email da página inicial é publicado pela própria clínica.
    adicionar_email(lead, e.get("home_page_email"), "quickenrich:site", publicado_pela_empresa=True)
    adicionar_telefone(lead, e.get("phone"), "quickenrich")
    if e.get("linkedin_url"):
        lead["redes"]["linkedin"] = e["linkedin_url"]
    return lead


# --------------------------------------------------------------------------- #
# 2. Encontrar o decisor
# --------------------------------------------------------------------------- #
def precisa_decisor(lead: dict) -> bool:
    """Tem domínio próprio e ainda não tem um email nominativo nesse domínio."""
    dom = dominio(lead.get("site"))
    if not dom:
        return False
    return not any(e["endereco"].endswith("@" + dom) and not e_generico(e["endereco"])
                   for e in lead["emails"])


def _contacto_para_lead(lead: dict, c: dict) -> bool:
    """Junta um contacto devolvido pela API ao lead. Devolve True se trouxe email ou telefone."""
    if not (c.get("email") or c.get("employee_phone")):
        return False
    adicionar_email(lead, c.get("email"), "quickenrich", publicado_pela_empresa=False)
    adicionar_telefone(lead, c.get("employee_phone"), "quickenrich")
    if not (lead.get("decisor") or {}).get("nome"):
        nome = " ".join(filter(None, [c.get("first_name"), c.get("last_name")]))
        lead["decisor"] = {"nome": nome or None, "primeiro_nome": c.get("first_name"),
                           "cargo": c.get("title"), "fonte": "quickenrich",
                           "linkedin": c.get("employee_linkedin")}
    if "quickenrich" not in lead["fontes"]:
        lead["fontes"].append("quickenrich")
    return True


def enriquecer(leads: list[dict], max_creditos: int, cargos: list[str] | None = None) -> dict:
    """Procura o decisor de cada lead com domínio. Para ao atingir ``max_creditos``."""
    gastos, encontrados, restantes = 0, 0, None
    for lead in leads:
        if gastos >= max_creditos:
            break
        if not precisa_decisor(lead):
            continue
        dom = dominio(lead["site"])
        d = lead.get("decisor") or {}
        partes = (d.get("nome") or "").split()
        if len(partes) >= 2:
            params = {"company_url": dom, "first_name": partes[0], "last_name": partes[-1]}
            r = http.pedido("quickenrich", "GET", f"{BASE}/api/employees/search", headers=_cab(), params=params)
            dados = (r or {}).get("data")
            contactos = [dados] if isinstance(dados, dict) else (dados or [])
        else:
            params = {"company_url": dom, "title": ",".join(cargos or CARGOS), "has_email": "true"}
            r = http.pedido("quickenrich", "GET", f"{BASE}/api/employees/dataset-search",
                            headers=_cab(), params=params)
            contactos = (r or {}).get("data") or []
        meta = (r or {}).get("meta") or {}
        gastos += meta.get("credits_used") or 0
        restantes = meta.get("remaining_credits", restantes)
        if any([_contacto_para_lead(lead, c) for c in contactos[:3]]):
            encontrados += 1
        time.sleep(0.1)
    return {"leads_enriquecidos": encontrados, "creditos_gastos": gastos, "creditos_restantes": restantes}
