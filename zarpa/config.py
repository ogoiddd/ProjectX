"""Caminhos, chaves e constantes partilhadas."""

from __future__ import annotations

import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA_EMAIL = RAIZ / "vendas" / "email"
PASTA_CAMPANHAS = PASTA_EMAIL / "campanhas"
SUPRESSAO = PASTA_EMAIL / "supressao.csv"
OPOSICAO = PASTA_EMAIL / "lista-oposicao.csv"

# Nome da variável de ambiente de cada serviço.
CHAVES = {
    "outscraper": "OUTSCRAPER_API_KEY",
    "aiark": "AIARK_API_KEY",
    "millionverifier": "MILLIONVERIFIER_API_KEY",
    "smartlead": "SMARTLEAD_API_KEY",
    "pagespeed": "PAGESPEED_API_KEY",  # opcional
}

# Domínios de email gratuitos: um endereço destes só é usado se for o
# contacto publicado pela própria clínica (ficha Google ou site).
EMAIL_GRATUITO = {
    "gmail.com", "hotmail.com", "hotmail.pt", "outlook.com", "outlook.pt",
    "live.com", "live.com.pt", "yahoo.com", "yahoo.com.br", "sapo.pt",
    "iol.pt", "clix.pt", "netcabo.pt", "icloud.com", "me.com", "msn.com",
    "mail.telepac.pt", "gmx.com", "protonmail.com", "proton.me",
}

# Prefixos de emails genéricos (não nominativos).
EMAIL_GENERICO = (
    "geral", "info", "informacoes", "contacto", "contactos", "contact",
    "clinica", "recepcao", "rececao", "secretaria", "marcacoes", "marcacao",
    "consultas", "atendimento", "admin", "office", "hello", "ola", "reservas",
)


class ChaveEmFalta(RuntimeError):
    """Levantada quando a variável de ambiente com a chave não existe."""


def chave(servico: str, obrigatoria: bool = True) -> str | None:
    """Lê a chave do ``servico`` do ambiente."""
    nome = CHAVES[servico]
    valor = os.environ.get(nome)
    if not valor and obrigatoria:
        raise ChaveEmFalta(f"Falta a variável de ambiente {nome}.")
    return valor


def pasta_campanha(campanha: str) -> Path:
    pasta = PASTA_CAMPANHAS / campanha
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta
