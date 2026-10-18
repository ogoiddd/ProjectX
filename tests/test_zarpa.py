"""Testes do pipeline de leads da Zarpa (sem rede: as APIs são simuladas)."""

import csv
import json

import pytest

from zarpa import auditoria, config, funil, juntar, legal, modelo, smartlead, telefone, verificar
from zarpa.cli import main
from zarpa.fontes import aiark, csv_import, gmaps


@pytest.fixture
def pasta(tmp_path, monkeypatch):
    """Isola campanhas, supressão, oposição e cache numa pasta temporária."""
    monkeypatch.setattr(config, "PASTA_CAMPANHAS", tmp_path / "campanhas")
    monkeypatch.setattr(legal, "SUPRESSAO", tmp_path / "supressao.csv")
    monkeypatch.setattr(legal, "OPOSICAO", tmp_path / "oposicao.csv")
    monkeypatch.setattr(smartlead, "SUPRESSAO", tmp_path / "supressao.csv")
    monkeypatch.setattr(verificar, "CACHE", tmp_path / "cache.json")
    monkeypatch.setenv("MILLIONVERIFIER_API_KEY", "teste")
    monkeypatch.setenv("SMARTLEAD_API_KEY", "teste")
    return tmp_path


def lead(nome="Clínica Sorriso Lda", cidade="Faro", **kw):
    l = modelo.novo_lead(nome, cidade, "teste", subnicho="dentaria")
    l.update(kw)
    return l


# --------------------------------------------------------------------------- #
# Telefones e domínios
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("numero,esperado,tipo", [
    ("+351 289 123 456", "289123456", "fixo"),
    ("00351 912345678", "912345678", "movel"),
    ("96 123 45 67", "961234567", "movel"),
    ("123", None, None),
    ("+44 20 7946 0958", None, None),
])
def test_telefone(numero, esperado, tipo):
    assert telefone.normalizar(numero) == esperado
    assert telefone.tipo(numero) == tipo


def test_dominio_e_redes():
    assert modelo.dominio("https://www.Clinica.pt/contactos") == "clinica.pt"
    assert modelo.dominio("clinica.pt") == "clinica.pt"
    assert modelo.dominio("https://facebook.com/clinica") is None
    assert modelo.e_rede_social("https://www.instagram.com/x")


# --------------------------------------------------------------------------- #
# Fontes
# --------------------------------------------------------------------------- #
FICHA = {
    "name": "Clínica Dentária Sol", "city": "Loulé", "full_address": "Rua A, Loulé",
    "postal_code": "8100-000", "site": "https://www.facebook.com/clinicasol",
    "phone": "+351 289 000 111", "rating": 4.8, "reviews": 212, "place_id": "abc",
    "business_status": "OPERATIONAL", "email_1": "geral@clinicasol.pt",
}


def test_gmaps_ficha_para_lead():
    l = gmaps.para_lead(FICHA, "dentaria")
    assert l["site"] is None and l["redes"]["facebook"].endswith("clinicasol")
    assert l["google"]["avaliacoes"] == 212
    assert l["emails"][0]["publicado_pela_empresa"] is True
    assert l["telefones"][0]["numero"] == "+351 289 000 111"


def test_gmaps_ignora_fechadas_e_achata():
    assert gmaps.para_lead({**FICHA, "business_status": "CLOSED_PERMANENTLY"}, "dentaria") is None
    assert len(gmaps.achatar([[FICHA, FICHA], [FICHA]])) == 3
    assert gmaps.montar_pesquisas("dentaria", ["Faro"]) == [
        "clínica dentária, Faro, Portugal", "dentista, Faro, Portugal"]


def test_aiark_emails_e_lead():
    linhas = [{"state": "DONE", "input": {"firstname": "Ana", "lastname": "Costa", "domain": "sol.pt"},
               "output": [{"address": "ana@sol.pt", "status": "VALID"},
                          {"address": "x@sol.pt", "status": "INVALID"}]}]
    mapa = aiark.emails_por_pessoa(linhas)
    pessoa = {"profile": {"first_name": "Ana", "last_name": "Costa", "title": "Diretora Clínica"},
              "company": {"summary": {"name": "Sol Dental Lda"}, "link": {"website": "https://sol.pt"}},
              "location": {"city": "Faro"}}
    l = aiark.para_lead(pessoa, mapa, "dentaria")
    assert l["nome"] == "Sol Dental Lda"
    assert [e["endereco"] for e in l["emails"]] == ["ana@sol.pt"]
    assert l["emails"][0]["publicado_pela_empresa"] is False
    assert l["decisor"]["primeiro_nome"] == "Ana"


def test_aiark_pesquisa_paginada(monkeypatch):
    monkeypatch.setenv("AIARK_API_KEY", "t")
    paginas = iter([{"content": [{}] * 100, "trackId": "t1", "last": False},
                    {"content": [{}] * 20, "trackId": "t2", "last": True}])
    monkeypatch.setattr(aiark.http, "pedido", lambda *a, **k: next(paginas))
    monkeypatch.setattr(aiark.time, "sleep", lambda s: None)
    res = aiark.pesquisar({}, maximo=500)
    assert [t for _, t in res] == ["t1", "t2"]


def test_csv_import(tmp_path):
    p = tmp_path / "getleads.csv"
    p.write_text("Company Name,City,Website,Email,Phone,First Name,Last Name,Title\n"
                 "Fisio Mar Lda,Lagos,fisiomar.pt,joao@fisiomar.pt,912345678,João,Reis,Sócio-gerente\n")
    [l] = csv_import.importar(p, "getleads", "fisioterapia")
    assert l["site"] == "fisiomar.pt"
    assert l["decisor"]["nome"] == "João Reis"
    assert l["fontes"] == ["csv:getleads"]


# --------------------------------------------------------------------------- #
# Juntar
# --------------------------------------------------------------------------- #
def test_juntar_por_dominio_telefone_e_nome():
    a = lead(site="https://sorriso.pt")
    b = lead("Sorriso Clínica Dentária", "Faro")  # mesmo nome sem palavras vazias
    c = lead("Outra coisa", "Faro", site="sorriso.pt")
    modelo.adicionar_email(c, "geral@sorriso.pt", "x", True)
    d = lead("Sem relação", "Tavira")
    res = juntar.juntar([a, b, c, d])
    assert len(res) == 2
    assert res[0]["emails"][0]["endereco"] == "geral@sorriso.pt"


def test_juntar_lead_que_liga_dois():
    a = lead("A", "Faro", site="a.pt")
    b = lead("B", "Faro")
    modelo.adicionar_telefone(b, "289 000 000", "x")
    c = lead("C", "Faro", site="a.pt")
    modelo.adicionar_telefone(c, "+351289000000", "x")
    d = lead("B", "Faro")  # deve cair no mesmo grupo de b, já fundido com a
    assert len(juntar.juntar([a, b, c, d])) == 1


# --------------------------------------------------------------------------- #
# Verificar
# --------------------------------------------------------------------------- #
def test_verificar_usa_cache(pasta, monkeypatch):
    chamadas = []

    def falso(servico, metodo, url, **kw):
        chamadas.append(kw["params"]["email"])
        return {"result": "ok", "quality": "good", "error": ""}

    monkeypatch.setattr(verificar.http, "pedido", falso)
    l = lead()
    modelo.adicionar_email(l, "geral@sorriso.pt", "x", True)
    modelo.adicionar_telefone(l, "289000000", "x")
    assert verificar.verificar([l], pausa=0) == {"ok": 1}
    l["emails"][0]["mv_resultado"] = None
    verificar.verificar([l], pausa=0)
    assert chamadas == ["geral@sorriso.pt"]  # a 2.ª vez veio da cache
    assert l["telefones"][0] == {"numero": "+351 289 000 000", "fonte": "x", "tipo": "fixo", "valido": True}


# --------------------------------------------------------------------------- #
# Legal
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("nome,esperado", [
    ("Clínica Sorriso, Lda", "sociedade"),
    ("Fisio Mar Unipessoal Lda.", "sociedade"),
    ("Vet Sul S.A.", "sociedade"),
    ("Dra. Marta Silva", "provavel_eni"),
    ("Clínica Sorriso", "desconhecido"),
    ("Clínica Santo Amaro", "desconhecido"),
])
def test_tipo_entidade(nome, esperado):
    assert legal.tipo_entidade(lead(nome)) == esperado


def _email(l, endereco, publicado, mv="ok"):
    modelo.adicionar_email(l, endereco, "x", publicado)
    l["emails"][-1]["mv_resultado"] = mv


def test_escolher_email():
    l = lead(site="https://sorriso.pt")
    _email(l, "dono.pessoal@gmail.com", False)          # gmail não publicado: proibido
    _email(l, "geral@sorriso.pt", True)
    _email(l, "ana.costa@sorriso.pt", False)            # nominativo no domínio: preferido
    _email(l, "outro@outrodominio.pt", False)           # outro domínio, não publicado: proibido
    assert legal.escolher_email(l)["endereco"] == "ana.costa@sorriso.pt"
    l["emails"][2]["mv_resultado"] = "catch_all"
    assert legal.escolher_email(l)["endereco"] == "geral@sorriso.pt"
    assert legal.escolher_email(l, aceitar_catch_all=True)["endereco"] == "geral@sorriso.pt"


def test_gmail_publicado_e_permitido():
    l = lead()
    _email(l, "clinicasorriso@gmail.com", True)
    assert legal.escolher_email(l)["endereco"] == "clinicasorriso@gmail.com"


def test_filtrar(pasta):
    ok = lead(site="sorriso.pt")
    _email(ok, "geral@sorriso.pt", True)
    eni = lead("Dra. Marta Silva", site="marta.pt")
    _email(eni, "geral@marta.pt", True)
    oposta = lead("Vet Sul Lda", site="vetsul.pt")
    _email(oposta, "geral@vetsul.pt", True)
    contagem = legal.filtrar([ok, eni, oposta], oposicao={"vetsul.pt"}, supressao=set())
    assert ok["legal"]["elegivel"] and ok["email_envio"] == "geral@sorriso.pt"
    assert eni["legal"]["motivos"] == ["entidade:provavel_eni"]
    assert oposta["legal"]["motivos"] == ["lista_oposicao"]
    assert contagem["elegivel"] == 1


def test_suprimir_e_ler(pasta):
    legal.suprimir("Ana@Sorriso.pt", "SAIR", "2026-10-18")
    assert "ana@sorriso.pt" in legal.ler_lista(legal.SUPRESSAO)


# --------------------------------------------------------------------------- #
# Auditoria
# --------------------------------------------------------------------------- #
HTML_BOM = ('<html><head><title>Clínica</title><meta name="viewport" content="width=device-width">'
            '</head><body><a href="/marcar">Marcar consulta</a> © 2026</body></html>')
HTML_FRACO = '<html><head><title>Clínica</title></head><body>Copyright 2017</body></html>'


def test_analisar_html():
    s = auditoria.analisar_html(HTML_FRACO, "http://clinica.pt", ano_atual=2026)
    assert s == {"url_final": "http://clinica.pt", "https": False, "viewport": False, "marcacao": False,
                 "ano_copyright": 2017, "desatualizado": True, "titulo": "Clínica", "gerador": None}
    assert auditoria.analisar_html(HTML_BOM, "https://c.pt", 2026)["marcacao"]


class Resposta:
    def __init__(self, html, url, estado=200):
        self.text, self.url, self.status_code, self.ok = html, url, estado, estado < 400


def test_auditar(monkeypatch):
    monkeypatch.setattr(auditoria.requests, "get", lambda url, **k: Resposta(HTML_FRACO, "http://clinica.pt"))
    l = lead(site="clinica.pt", google={"nota": 4.8, "avaliacoes": 212})
    auditoria.auditar(l, ano_atual=2026)
    assert l["icp"] == {"situacao": "site_fraco", "elegivel": True}
    assert set(l["auditoria"]["problemas"]) == {"sem_https", "sem_viewport", "sem_marcacao", "desatualizado"}
    assert "Google: 4.8 em 212 avaliações" in l["auditoria"]["evidencias"]

    monkeypatch.setattr(auditoria.requests, "get", lambda url, **k: Resposta(HTML_BOM, "https://c.pt"))
    bom = lead(site="c.pt")
    auditoria.auditar(bom, ano_atual=2026)
    assert bom["icp"] == {"situacao": "site_bom", "elegivel": False}

    sem = lead(redes={"facebook": "https://facebook.com/x"})
    auditoria.auditar(sem)
    assert sem["icp"]["situacao"] == "so_redes"


# --------------------------------------------------------------------------- #
# Smartlead
# --------------------------------------------------------------------------- #
def pronto(nome="Clínica Sorriso Lda", **kw):
    l = lead(nome, site="sorriso.pt", google={"nota": 4.8, "avaliacoes": 212},
             legal={"elegivel": True, "motivos": []}, icp={"situacao": "site_fraco", "elegivel": True},
             email_envio="geral@sorriso.pt", icebreaker="Vi que o botão 'website' leva ao Facebook.", **kw)
    _email(l, "geral@sorriso.pt", True)
    l["emails"][0]["fonte"] = "gmaps:site"
    return l


def test_variante_estavel_e_equilibrada():
    assert smartlead.variante("x", "c") == smartlead.variante("x", "c")
    vs = [smartlead.variante(f"lead-{i}", "c") for i in range(400)]
    assert 150 < vs.count("A") < 250


def test_linha_envio_sem_adivinhar_titulo():
    l = pronto(decisor={"nome": "Marta Silva", "primeiro_nome": None})
    linha = smartlead.linha_envio(l, "c")
    assert linha["saudacao"] == "Bom dia, Marta"
    assert linha["nota"] == "4,8" and linha["especialidade"] == "dentista"
    assert linha["fonte_contacto"] == "no vosso site"
    assert smartlead.linha_envio(pronto(), "c")["saudacao"] == "Bom dia"


@pytest.mark.parametrize("nome,esperado", [
    ("Clínica Sorriso, Lda.", "Clínica Sorriso"),
    ("Fisio Mar Unipessoal Lda", "Fisio Mar"),
    ("Vet Sul S.A.", "Vet Sul"),
    ("Clínica Santo Amaro", "Clínica Santo Amaro"),
])
def test_nome_comercial(nome, esperado):
    assert smartlead.nome_comercial(nome) == esperado


def test_prontos_exige_icebreaker():
    sem = pronto()
    sem["icebreaker"] = None
    assert smartlead.prontos([pronto(), sem]) == [pronto()]


def test_exportar_e_enviar_ensaio(pasta):
    p = smartlead.exportar([pronto()], "c1")
    linhas = list(csv.DictReader(open(p, encoding="utf-8")))
    assert linhas[0]["email"] == "geral@sorriso.pt"
    r = smartlead.enviar("c1", 123)
    assert r["ensaio"] and r["leads"] == 1
    corpo = json.loads(open(r["ficheiro"]).read())[0]
    assert corpo["lead_list"][0]["custom_fields"]["clinica"] == "Clínica Sorriso"
    assert corpo["settings"]["ignore_unsubscribe_list"] is False


def test_classificar():
    cats = {1: "Interested", 2: "Not Interested", 3: "Do Not Contact"}
    item = lambda st, cat, email="a@b.pt", unsub=False: {
        "status": st, "lead_category_id": cat, "lead": {"email": email, "is_unsubscribed": unsub}}
    assert smartlead.classificar(item("STARTED", None), cats, set(), set()) == []
    assert smartlead.classificar(item("COMPLETED", 1), cats, set(), {"a@b.pt"}) == ["enviado", "resposta_positiva"]
    assert smartlead.classificar(item("COMPLETED", 3), cats, set(), set()) == ["enviado", "opt_out"]
    assert smartlead.classificar(item("INPROGRESS", None), cats, {"a@b.pt"}, set()) == ["enviado", "bounce"]
    assert smartlead.classificar(item("COMPLETED", None), cats, set(), {"a@b.pt"}) == ["enviado", "resposta_neutra"]


def test_sincronizar(pasta, monkeypatch):
    smartlead.exportar([pronto()], "c1")
    smartlead.registar_evento("c1", pronto()["id"], "venda", "1490")

    def falso(servico, metodo, url, **kw):
        if url.endswith("fetch-categories"):
            return [{"id": 3, "name": "Do Not Contact"}]
        if kw["params"].get("emailStatus") or kw["params"]["offset"]:
            return {"data": []}
        return {"data": [{"status": "COMPLETED", "lead_category_id": 3,
                          "lead": {"email": "geral@sorriso.pt", "is_unsubscribed": False}}]}

    monkeypatch.setattr(smartlead.http, "pedido", falso)
    p = smartlead.sincronizar("c1", 123)
    eventos = [l["evento"] for l in csv.DictReader(open(p, encoding="utf-8"))]
    assert eventos == ["enviado", "opt_out", "venda"]
    assert "geral@sorriso.pt" in legal.ler_lista(legal.SUPRESSAO)
    smartlead.sincronizar("c1", 123)  # 2.ª sincronização não duplica a supressão
    assert open(legal.SUPRESSAO).read().count("geral@sorriso.pt") == 1


# --------------------------------------------------------------------------- #
# Funil
# --------------------------------------------------------------------------- #
def eventos(variante, n_env, n_bounce, n_pos, n_reun=0, vendas=()):
    ev = []
    for i in range(n_env):
        lid = f"{variante}{i}"
        ev.append({"lead_id": lid, "variante": variante, "evento": "enviado", "valor": ""})
        if i < n_bounce:
            ev.append({"lead_id": lid, "variante": variante, "evento": "bounce", "valor": ""})
        elif i < n_bounce + n_pos:
            ev.append({"lead_id": lid, "variante": variante, "evento": "resposta_positiva", "valor": ""})
            if i < n_bounce + n_reun:
                ev.append({"lead_id": lid, "variante": variante, "evento": "reuniao_marcada", "valor": ""})
    for i, v in enumerate(vendas):
        ev.append({"lead_id": f"{variante}{n_bounce + i}", "variante": variante, "evento": "venda", "valor": v})
    return ev


def test_funil_contas():
    c = funil.contar(eventos("A", 100, 2, 4, 2, vendas=["1490"]))
    assert c["A"]["entregues"] == 98 and c["total"]["receita"] == 1490
    t = funil.taxas(c["A"])
    assert t["resposta_positiva"] == pytest.approx(4 / 98)
    assert t["reuniao_marcada"] == pytest.approx(0.5)
    assert t["receita_por_100"] == pytest.approx(1490 / 98 * 100)


def test_estrangulamento():
    t = funil.taxas(funil.contar(eventos("A", 200, 2, 10, 1))["A"])  # marca só 10%
    assert funil.estrangulamento(t) == "reuniao_marcada"


def test_relatorio_cli(pasta):
    pasta_c = config.pasta_campanha("c1")
    with open(pasta_c / "resultados.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["lead_id", "campanha", "variante", "data", "evento", "valor"])
        w.writeheader()
        for e in eventos("A", 50, 1, 1) + eventos("B", 50, 0, 3):
            w.writerow({**e, "campanha": "c1", "data": "2026-11-01"})
    assert main(["funil", "--campanha", "c1"]) == 0
    texto = (pasta_c / "funil.md").read_text()
    assert "| resposta_positiva |" in texto and "Ainda sem amostra" in texto


# --------------------------------------------------------------------------- #
# Fluxo completo pela CLI (com APIs simuladas)
# --------------------------------------------------------------------------- #
def test_fluxo_cli(pasta, monkeypatch, tmp_path):
    p = tmp_path / "leads.csv"
    p.write_text("Company Name,City,Website,Email\n"
                 "Clínica Sorriso Lda,Faro,sorriso.pt,geral@sorriso.pt\n"
                 "Dra. Marta Silva,Faro,marta.pt,geral@marta.pt\n")
    monkeypatch.setattr(verificar.http, "pedido", lambda *a, **k: {"result": "ok", "quality": "good", "error": ""})
    monkeypatch.setattr(auditoria.requests, "get", lambda url, **k: Resposta(HTML_FRACO, "http://" + url.split("//")[1]))
    c = ["--campanha", "piloto"]
    main(["importar-csv", *c, "--ficheiro", str(p), "--fonte", "getleads", "--subnicho", "dentaria",
          "--emails-publicados"])
    for cmd in ("juntar", "verificar", "filtrar", "auditar"):
        main([cmd, *c])
    leads = modelo.carregar("piloto")
    assert [l["legal"]["elegivel"] for l in leads] == [True, False]
    leads[0]["icebreaker"] = "Abri o site da Clínica Sorriso no telemóvel e não há onde marcar consulta."
    modelo.gravar("piloto", leads)
    main(["exportar", *c])
    assert len(smartlead.ler_envio("piloto")) == 1
    main(["enviar", *c, "--id-smartlead", "1"])  # ensaio: não toca na API
    assert (config.pasta_campanha("piloto") / "ensaio-smartlead-1.json").exists()
