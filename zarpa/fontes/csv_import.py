"""Importa leads de um CSV exportado de qualquer ferramenta (Get Leads, ...).

As colunas são reconhecidas pelo nome, em português ou inglês. Para um CSV
com nomes estranhos, passa-se um mapa ``{"coluna_do_csv": "campo"}``.
"""

from __future__ import annotations

import csv
import unicodedata
from pathlib import Path

from ..modelo import adicionar_email, adicionar_telefone, e_rede_social, novo_lead

# campo interno -> nomes de coluna aceites (normalizados: minúsculas, sem acentos)
SINONIMOS = {
    "nome": ["company", "company name", "company_name", "business name", "name", "nome", "empresa", "clinica"],
    "cidade": ["city", "cidade", "localidade", "location"],
    "morada": ["address", "full_address", "morada", "endereco"],
    "site": ["website", "site", "domain", "company website", "url"],
    "email": ["email", "e-mail", "email address", "work email", "company email"],
    "telefone": ["phone", "telefone", "phone number", "company phone", "mobile", "telemovel"],
    "decisor_nome": ["full name", "contact name", "person name", "decisor"],
    "decisor_primeiro": ["first name", "first_name", "primeiro nome"],
    "decisor_apelido": ["last name", "last_name", "apelido"],
    "decisor_cargo": ["title", "job title", "cargo", "position"],
    "linkedin": ["linkedin", "linkedin url", "person linkedin url"],
    "nif": ["nif", "nipc", "vat"],
    "denominacao_social": ["denominacao social", "legal name", "razao social"],
}


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return " ".join(s.lower().replace("_", " ").split())


def detetar_colunas(cabecalho: list[str], mapa: dict[str, str] | None = None) -> dict[str, str]:
    """Devolve ``{campo: coluna_do_csv}``."""
    res: dict[str, str] = {}
    norm = {_norm(c): c for c in cabecalho}
    for campo, nomes in SINONIMOS.items():
        for n in nomes:
            if _norm(n) in norm:
                res[campo] = norm[_norm(n)]
                break
    for coluna, campo in (mapa or {}).items():
        res[campo] = coluna
    return res


def importar(caminho: str | Path, fonte: str, subnicho: str,
             mapa: dict[str, str] | None = None, emails_publicados: bool = False) -> list[dict]:
    """Lê o CSV e devolve leads.

    ``emails_publicados=True`` só se a ferramenta tirou os emails do site ou da
    ficha da própria clínica (e não de um "email finder").
    """
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        leitor = csv.DictReader(f)
        col = detetar_colunas(leitor.fieldnames or [], mapa)
        if "nome" not in col:
            raise ValueError(f"Não encontrei a coluna do nome da empresa em {caminho}.")
        leads = []
        for linha in leitor:
            v = lambda campo: (linha.get(col[campo]) or "").strip() or None if campo in col else None
            if not v("nome"):
                continue
            site = v("site")
            lead = novo_lead(v("nome"), v("cidade"), f"csv:{fonte}", subnicho=subnicho,
                             morada=v("morada"), nif=v("nif"),
                             denominacao_social=v("denominacao_social"),
                             site=None if e_rede_social(site) else site)
            adicionar_email(lead, v("email"), f"csv:{fonte}", publicado_pela_empresa=emails_publicados)
            adicionar_telefone(lead, v("telefone"), f"csv:{fonte}")
            nome_decisor = v("decisor_nome") or " ".join(filter(None, [v("decisor_primeiro"), v("decisor_apelido")]))
            if nome_decisor:
                lead["decisor"] = {"nome": nome_decisor, "primeiro_nome": v("decisor_primeiro"),
                                   "cargo": v("decisor_cargo"), "fonte": f"csv:{fonte}",
                                   "linkedin": v("linkedin")}
            leads.append(lead)
        return leads
