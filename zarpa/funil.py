"""Funil de conversão a partir do ``resultados.csv``.

Calcula as taxas por variante, compara com as metas do plano (§5) e aponta a
etapa com o maior desvio, que é onde o próximo teste deve atacar.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from .config import pasta_campanha

# etapa -> (numerador, denominador, meta, alerta, maior_e_melhor)
METAS = {
    "bounce": ("bounce", "enviado", 0.02, 0.03, False),
    "resposta": ("respostas", "entregues", 0.06, 0.03, True),
    "resposta_positiva": ("resposta_positiva", "entregues", 0.03, 0.015, True),
    "opt_out": ("opt_out", "entregues", 0.02, 0.03, False),
    "reuniao_marcada": ("reuniao_marcada", "resposta_positiva", 0.50, 0.35, True),
    "comparencia": ("reuniao_feita", "reuniao_marcada", 0.75, 0.60, True),
    "venda": ("venda", "reuniao_feita", 0.25, 0.15, True),
}
META_RECEITA_100 = 300
MINIMO_POR_VARIANTE = 150
# Uma etapa só conta para o estrangulamento com pelo menos 5 casos na base:
# 0 de 1 reuniões feitas é ruído (ou a reunião ainda não aconteceu).
MINIMO_DENOMINADOR = 5


def ler(caminho: Path) -> list[dict]:
    with open(caminho, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def contar(eventos: list[dict]) -> dict[str, dict]:
    """Contagens por variante (e ``total``): um lead conta uma vez por evento."""
    leads: dict[str, dict[str, set]] = defaultdict(lambda: defaultdict(set))
    receita: dict[str, float] = defaultdict(float)
    for e in eventos:
        for v in (e.get("variante") or "?", "total"):
            leads[v][e["evento"]].add(e["lead_id"])
            if e["evento"] == "venda" and e.get("valor"):
                receita[v] += float(str(e["valor"]).replace(",", "."))
    res = {}
    for v, ev in leads.items():
        c = {k: len(s) for k, s in ev.items()}
        c["entregues"] = c.get("enviado", 0) - c.get("bounce", 0)
        c["respostas"] = sum(c.get(k, 0) for k in ("resposta_positiva", "resposta_negativa",
                                                   "resposta_neutra", "opt_out"))
        c["receita"] = receita[v]
        res[v] = c
    return res


def taxas(c: dict) -> dict[str, float | None]:
    t = {}
    for etapa, (num, den, *_resto) in METAS.items():
        t[etapa] = c.get(num, 0) / c[den] if c.get(den) else None
        t[f"{etapa}_base"] = c.get(den, 0)
    t["receita_por_100"] = c["receita"] / c["entregues"] * 100 if c.get("entregues") else None
    return t


def estrangulamento(t: dict) -> str | None:
    """A etapa com o maior desvio negativo face à meta (relativo)."""
    pior, desvio_pior = None, 0.0
    for etapa, (_n, _d, meta, _alerta, maior) in METAS.items():
        valor = t.get(etapa)
        if valor is None or t.get(f"{etapa}_base", 0) < MINIMO_DENOMINADOR:
            continue
        desvio = (meta - valor) / meta if maior else (valor - meta) / meta
        if desvio > desvio_pior:
            pior, desvio_pior = etapa, desvio
    return pior


def _pct(x: float | None) -> str:
    return "—" if x is None else f"{x * 100:.1f}%"


def relatorio(campanha: str) -> str:
    c = contar(ler(pasta_campanha(campanha) / "resultados.csv"))
    variantes = sorted(v for v in c if v != "total") + ["total"]
    linhas = [f"# Funil · {campanha}", "",
              "| Etapa | Meta | " + " | ".join(variantes) + " |",
              "|---|---|" + "---|" * len(variantes)]
    linhas.append("| Entregues | ≥ 150 por variante | " +
                  " | ".join(str(c[v].get("entregues", 0)) for v in variantes) + " |")
    tx = {v: taxas(c[v]) for v in variantes}
    for etapa, (_n, _d, meta, alerta, maior) in METAS.items():
        cel = []
        for v in variantes:
            x = tx[v][etapa]
            mau = x is not None and ((x < alerta) if maior else (x > alerta))
            cel.append(_pct(x) + (" ⚠️" if mau else ""))
        sinal = "≥" if maior else "<"
        linhas.append(f"| {etapa} | {sinal} {meta * 100:g}% | " + " | ".join(cel) + " |")
    linhas.append(f"| **receita por 100 entregues** | ≥ {META_RECEITA_100} | " + " | ".join(
        "—" if tx[v]["receita_por_100"] is None else f"{tx[v]['receita_por_100']:.0f}" for v in variantes) + " |")
    pior = estrangulamento(tx["total"])
    linhas += ["", f"**Estrangulamento:** {pior or 'nenhum abaixo da meta'}."]
    poucos = [v for v in variantes if v != "total" and c[v].get("entregues", 0) < MINIMO_POR_VARIANTE]
    if poucos:
        linhas.append(f"**Ainda sem amostra para decidir:** variante(s) {', '.join(poucos)} "
                      f"com menos de {MINIMO_POR_VARIANTE} entregues.")
    return "\n".join(linhas) + "\n"
