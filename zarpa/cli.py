"""Linha de comandos: ``python -m zarpa <comando> --campanha <id> ...``.

Ordem normal de uma campanha::

    recolher-gmaps → recolher-aiark → recolher-quickenrich → importar-csv
    → juntar → enriquecer → verificar
    → filtrar → auditar → (agente icebreaker-writer) → exportar
    → (aprovação humana) → enviar --a-serio → sincronizar → funil
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from typing import Sequence

from . import auditoria, funil, juntar, legal, modelo, smartlead, verificar
from .config import PASTA_CAMPANHAS, pasta_campanha
from .fontes import aiark, csv_import, gmaps, quickenrich


def _acrescentar(campanha: str, novos: list[dict]) -> None:
    leads = modelo.carregar(campanha) + novos
    modelo.gravar(campanha, leads)
    print(f"+{len(novos)} leads ({len(leads)} no total, antes de juntar).")


def cmd_recolher_gmaps(a) -> None:
    pesquisas = gmaps.montar_pesquisas(a.subnicho, [c.strip() for c in a.cidades.split(",")])
    fichas = gmaps.pesquisar(pesquisas, limite=a.limite)
    modelo.gravar_bruto(a.campanha, f"gmaps-{a.subnicho}", fichas)
    _acrescentar(a.campanha, [l for f in fichas if (l := gmaps.para_lead(f, a.subnicho))])


def cmd_recolher_aiark(a) -> None:
    filtros = aiark.carregar_filtros(a.subnicho)
    novos, brutos = [], []
    for pessoas, track_id in aiark.pesquisar(filtros, a.maximo):
        linhas = aiark.encontrar_emails(track_id) if track_id else []
        brutos.append({"pessoas": pessoas, "emails": linhas})
        mapa = aiark.emails_por_pessoa(linhas)
        novos += [l for p in pessoas if (l := aiark.para_lead(p, mapa, a.subnicho))]
    modelo.gravar_bruto(a.campanha, f"aiark-{a.subnicho}", brutos)
    _acrescentar(a.campanha, novos)


def cmd_recolher_quickenrich(a) -> None:
    empresas = quickenrich.procurar_empresas(quickenrich.carregar_filtros(a.subnicho), a.maximo)
    modelo.gravar_bruto(a.campanha, f"quickenrich-{a.subnicho}", empresas)
    _acrescentar(a.campanha, [l for e in empresas if (l := quickenrich.empresa_para_lead(e, a.subnicho))])


def cmd_enriquecer(a) -> None:
    leads = modelo.carregar(a.campanha)
    print("QuickEnrich:", quickenrich.enriquecer(leads, a.max_creditos))
    modelo.gravar(a.campanha, leads)


def cmd_importar_csv(a) -> None:
    mapa = json.loads(a.mapa) if a.mapa else None
    _acrescentar(a.campanha, csv_import.importar(a.ficheiro, a.fonte, a.subnicho, mapa, a.emails_publicados))


def cmd_juntar(a) -> None:
    leads = modelo.carregar(a.campanha)
    antes = len(leads)
    leads = juntar.juntar(leads)
    if a.excluir_contactados:
        antigos: set[str] = set()
        for p in PASTA_CAMPANHAS.glob("*/leads.json"):
            if p.parent.name != a.campanha:
                antigos |= juntar.emails_de(json.loads(p.read_text()))
        leads = juntar.ja_contactados(leads, antigos)
    modelo.gravar(a.campanha, leads)
    print(f"{antes} → {len(leads)} leads únicos.")


def cmd_verificar(a) -> None:
    leads = modelo.carregar(a.campanha)
    contagem = verificar.verificar(leads)
    modelo.gravar(a.campanha, leads)
    print("MillionVerifier:", contagem)


def cmd_filtrar(a) -> None:
    leads = modelo.carregar(a.campanha)
    contagem = legal.filtrar(leads, aceitar_catch_all=a.aceitar_catch_all)
    modelo.gravar(a.campanha, leads)
    print("Filtro legal:", contagem)


def cmd_auditar(a) -> None:
    leads = modelo.carregar(a.campanha)
    alvo = [l for l in leads if (l.get("legal") or {}).get("elegivel")] if not a.todos else leads
    for i, l in enumerate(alvo, 1):
        auditoria.auditar(l, com_pagespeed=a.pagespeed)
        print(f"[{i}/{len(alvo)}] {l['nome']}: {l['icp']['situacao']}")
    modelo.gravar(a.campanha, leads)


def cmd_exportar(a) -> None:
    leads = modelo.carregar(a.campanha)
    p = smartlead.exportar(leads, a.campanha)
    print(f"{len(smartlead.prontos(leads))} leads prontos → {p}")
    print("Revê o ficheiro e aprova antes de correr `enviar --a-serio`.")


def cmd_enviar(a) -> None:
    print(smartlead.enviar(a.campanha, a.id_smartlead, a.variante, ensaio=not a.a_serio))


def cmd_sincronizar(a) -> None:
    print(smartlead.sincronizar(a.campanha, a.id_smartlead))


def cmd_evento(a) -> None:
    print(smartlead.registar_evento(a.campanha, a.lead, a.tipo, a.valor or ""))


def cmd_funil(a) -> None:
    texto = funil.relatorio(a.campanha)
    (pasta_campanha(a.campanha) / "funil.md").write_text(texto)
    print(texto)


def cmd_estado(a) -> None:
    leads = modelo.carregar(a.campanha)
    c = Counter()
    for l in leads:
        c["total"] += 1
        c["com email"] += bool(l["emails"])
        c["email verificado ok"] += any(e.get("mv_resultado") == "ok" for e in l["emails"])
        c["legal ✔"] += bool((l.get("legal") or {}).get("elegivel"))
        c["icp ✔ (site fraco/sem site)"] += bool((l.get("icp") or {}).get("elegivel"))
        c["com icebreaker"] += bool(l.get("icebreaker"))
    c["prontos"] = len(smartlead.prontos(leads))
    for k, v in c.items():
        print(f"{k:32} {v}")


def construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="zarpa", description="Pipeline de leads da Zarpa (clínicas).")
    sub = p.add_subparsers(dest="comando", required=True)

    def novo(nome: str, func, ajuda: str) -> argparse.ArgumentParser:
        s = sub.add_parser(nome, help=ajuda)
        s.add_argument("--campanha", required=True, help="ex.: 2026-11-dentarias-algarve")
        s.set_defaults(func=func)
        return s

    s = novo("recolher-gmaps", cmd_recolher_gmaps, "Google Maps via Outscraper")
    s.add_argument("--subnicho", required=True, choices=sorted(gmaps.PESQUISAS))
    s.add_argument("--cidades", required=True, help="lista separada por vírgulas")
    s.add_argument("--limite", type=int, default=100, help="fichas por pesquisa")

    s = novo("recolher-aiark", cmd_recolher_aiark, "Decisores e emails via AI Ark")
    s.add_argument("--subnicho", required=True)
    s.add_argument("--maximo", type=int, default=300)

    s = novo("recolher-quickenrich", cmd_recolher_quickenrich, "Clínicas via QuickEnrich (company finder)")
    s.add_argument("--subnicho", required=True)
    s.add_argument("--maximo", type=int, default=200, help="1 crédito por empresa")

    s = novo("enriquecer", cmd_enriquecer, "Decisor + email/telemóvel via QuickEnrich (depois de juntar)")
    s.add_argument("--max-creditos", type=int, default=200)

    s = novo("importar-csv", cmd_importar_csv, "CSV de outra ferramenta (Get Leads, ...)")
    s.add_argument("--ficheiro", required=True)
    s.add_argument("--fonte", required=True, help="ex.: getleads")
    s.add_argument("--subnicho", required=True)
    s.add_argument("--mapa", help='JSON {"coluna do csv": "campo"}')
    s.add_argument("--emails-publicados", action="store_true",
                   help="os emails foram tirados do site/ficha da própria clínica")

    s = novo("juntar", cmd_juntar, "Juntar fontes e remover duplicados")
    s.add_argument("--excluir-contactados", action="store_true",
                   help="tirar emails que já estiveram noutras campanhas")

    novo("verificar", cmd_verificar, "MillionVerifier + telefones")

    s = novo("filtrar", cmd_filtrar, "Filtro legal e escolha do email")
    s.add_argument("--aceitar-catch-all", action="store_true")

    s = novo("auditar", cmd_auditar, "Visitar sites e recolher evidências")
    s.add_argument("--pagespeed", action="store_true")
    s.add_argument("--todos", action="store_true", help="auditar também os não elegíveis")

    novo("exportar", cmd_exportar, "Gerar envio.csv para aprovação")

    s = novo("enviar", cmd_enviar, "Enviar o envio.csv para o Smartlead")
    s.add_argument("--id-smartlead", type=int, required=True)
    s.add_argument("--variante", choices=["A", "B"], help="só uma variante (cada uma na sua campanha)")
    s.add_argument("--a-serio", action="store_true", help="sem isto é só um ensaio")

    s = novo("sincronizar", cmd_sincronizar, "Trazer resultados do Smartlead")
    s.add_argument("--id-smartlead", type=int, required=True)

    s = novo("evento", cmd_evento, "Registar reunião, proposta ou venda")
    s.add_argument("--lead", required=True)
    s.add_argument("--tipo", required=True, choices=sorted(smartlead.EVENTOS_MANUAIS))
    s.add_argument("--valor", help="valor da venda (ex.: 1490)")

    novo("funil", cmd_funil, "Métricas e estrangulamento")
    novo("estado", cmd_estado, "Quantos leads em cada etapa")
    return p


def main(argv: Sequence[str] | None = None) -> int:
    a = construir_parser().parse_args(argv)
    a.func(a)
    return 0
