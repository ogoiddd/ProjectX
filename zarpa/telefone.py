"""Validação de telefones portugueses (sem dependências externas).

O MillionVerifier só verifica emails, por isso os números são validados pelo
formato do Plano Nacional de Numeração: 9 dígitos, com prefixo 2 (fixo),
91/92/93/96 (móvel), 30 (VoIP) ou 70x/80x (números especiais).
"""

from __future__ import annotations

import re


def normalizar(numero: str | None) -> str | None:
    """Devolve os 9 dígitos nacionais, ou ``None`` se não for um número PT."""
    if not numero:
        return None
    d = re.sub(r"\D", "", numero)
    if d.startswith("00351"):
        d = d[5:]
    elif d.startswith("351") and len(d) == 12:
        d = d[3:]
    return d if len(d) == 9 else None


def tipo(numero: str | None) -> str | None:
    n = normalizar(numero)
    if not n:
        return None
    if n[0] == "2":
        return "fixo"
    if n[:2] in ("91", "92", "93", "96"):
        return "movel"
    if n[:2] == "30":
        return "voip"
    if n[:2] in ("70", "80"):
        return "especial"
    return None


def formatar(numero: str | None) -> str | None:
    n = normalizar(numero)
    return f"+351 {n[:3]} {n[3:6]} {n[6:]}" if n else None


def validar_lead(lead: dict) -> None:
    for t in lead["telefones"]:
        t["tipo"] = tipo(t["numero"])
        t["valido"] = t["tipo"] is not None
        if t["valido"]:
            t["numero"] = formatar(t["numero"])
