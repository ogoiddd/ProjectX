"""Web app minimalista para usar a ferramenta a partir de qualquer dispositivo.

Construída apenas com a biblioteca-padrão (``http.server``) — sem frameworks,
por isso corre em qualquer sítio onde haja Python + ``requests``, incluindo
serviços gratuitos (Render, Railway, Fly.io) e até no iPhone (a-Shell).

Abre uma página com um formulário; ao submeter, corre o pipeline e mostra a
tabela de valor, com um botão para descarregar o CSV.

Executar localmente:

    export ODDS_API_KEY=xxxxxxxx
    python -m odds_value.web            # abre em http://localhost:8000

Variáveis de ambiente:
- ``ODDS_API_KEY``  — chave do The Odds API (obrigatória p/ dados ao vivo).
- ``PORT``          — porta HTTP (Render/Railway definem-na automaticamente).
- ``HOST``          — interface (por omissão 0.0.0.0).
"""

from __future__ import annotations

import html
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

from .fetch import MissingApiKey
from .pipeline import analyze_games, load_games, values_to_csv
from .value import ValueSelection

# Ficheiro de exemplo, para permitir uma demo sem chave de API.
_SAMPLE = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                       "examples", "the_odds_api_sample.json")

_PAGE_CSS = """
:root { color-scheme: light dark; }
* { box-sizing: border-box; }
body { font-family: -apple-system, system-ui, Segoe UI, Roboto, sans-serif;
       margin: 0; padding: 1rem; max-width: 1000px; margin: 0 auto;
       line-height: 1.45; }
h1 { font-size: 1.35rem; margin: .2rem 0 1rem; }
form { display: grid; gap: .7rem; background: rgba(127,127,127,.08);
       padding: 1rem; border-radius: 12px; }
label { display: grid; gap: .25rem; font-size: .85rem; font-weight: 600; }
input, select { padding: .6rem; font-size: 1rem; border-radius: 8px;
                border: 1px solid rgba(127,127,127,.4); background: transparent;
                color: inherit; width: 100%; }
.row { display: grid; grid-template-columns: 1fr 1fr; gap: .7rem; }
button { padding: .8rem; font-size: 1rem; font-weight: 700; border: 0;
         border-radius: 10px; background: #2563eb; color: #fff; cursor: pointer; }
button.secondary { background: rgba(127,127,127,.25); color: inherit; }
.actions { display: flex; gap: .6rem; flex-wrap: wrap; }
.actions a { text-decoration: none; }
table { width: 100%; border-collapse: collapse; margin-top: 1rem;
        font-size: .82rem; }
th, td { text-align: left; padding: .5rem .4rem;
         border-bottom: 1px solid rgba(127,127,127,.25); }
th { font-size: .7rem; text-transform: uppercase; letter-spacing: .03em;
     opacity: .7; }
.ev { font-weight: 700; color: #16a34a; white-space: nowrap; }
.num { text-align: right; font-variant-numeric: tabular-nums; }
.warn { font-size: .78rem; color: #b45309; }
.outlier td { background: rgba(234,179,8,.12); }
.summary { margin-top: 1rem; padding: .8rem 1rem; border-radius: 10px;
           background: rgba(37,99,235,.1); font-weight: 600; }
.muted { opacity: .7; font-size: .85rem; }
.tablewrap { overflow-x: auto; }
.disclaimer { margin-top: 1.5rem; font-size: .78rem; opacity: .65; }
"""

_SPORTS = [
    ("soccer_epl", "Inglaterra — Premier League"),
    ("soccer_spain_la_liga", "Espanha — La Liga"),
    ("soccer_italy_serie_a", "Itália — Serie A"),
    ("soccer_germany_bundesliga", "Alemanha — Bundesliga"),
    ("soccer_france_ligue_one", "França — Ligue 1"),
    ("soccer_portugal_primeira_liga", "Portugal — Primeira Liga"),
    ("soccer_uefa_champs_league", "UEFA Champions League"),
    ("soccer_uefa_europa_league", "UEFA Europa League"),
    ("soccer_conmebol_copa_libertadores", "CONMEBOL Libertadores"),
]


def _esc(s: object) -> str:
    return html.escape(str(s))


def _form_page(params: dict[str, str], message: str = "") -> str:
    sport = params.get("sport", "soccer_epl")
    regions = params.get("regions", "eu,uk")
    markets = params.get("markets", "h2h,totals")
    method = params.get("method", "shin")
    ev = params.get("ev", "2")
    demo = params.get("demo", "")
    books = params.get("books", "")

    sport_opts = "".join(
        f'<option value="{_esc(k)}"{" selected" if k == sport else ""}>{_esc(v)}</option>'
        for k, v in _SPORTS
    )
    msg_html = f'<p class="warn">{_esc(message)}</p>' if message else ""
    return f"""<!doctype html>
<html lang="pt"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Valor em odds de futebol</title>
<style>{_PAGE_CSS}</style>
</head><body>
<h1>⚽ Análise de valor em odds</h1>
{msg_html}
<form method="get" action="/analyze">
  <label>Competição
    <select name="sport">{sport_opts}</select>
  </label>
  <div class="row">
    <label>Mercados
      <input name="markets" value="{_esc(markets)}" placeholder="h2h,totals,btts">
    </label>
    <label>Regiões
      <input name="regions" value="{_esc(regions)}" placeholder="eu,uk,us,au">
    </label>
  </div>
  <div class="row">
    <label>Método de devig
      <select name="method">
        <option value="shin"{" selected" if method == "shin" else ""}>Shin (1993)</option>
        <option value="proportional"{" selected" if method == "proportional" else ""}>Proporcional</option>
      </select>
    </label>
    <label>EV mínimo (%)
      <input name="ev" type="number" step="0.5" value="{_esc(ev)}">
    </label>
  </div>
  <label>Casas onde posso apostar <span class="muted">(opcional, separadas por vírgula)</span>
    <input name="books" value="{_esc(books)}" placeholder="bet365,betfair,unibet">
  </label>
  <label class="muted">
    <input type="checkbox" name="demo" value="1"{" checked" if demo else ""}
           style="width:auto;display:inline;margin-right:.4rem">
    Usar dados de exemplo (sem chave de API)
  </label>
  <button type="submit">Procurar valor</button>
</form>
<p class="muted">Precisas da variável de ambiente <code>ODDS_API_KEY</code> para dados ao vivo.
Sem chave, ativa a demo acima.</p>
</body></html>"""


_COLSPAN = 10


def _values_table(values) -> str:
    if not values:
        return '<p class="muted">Nenhuma seleção com EV acima do limite.</p>'
    rows = "".join(_result_row(v) for v in values)
    return f"""<div class="tablewrap"><table>
<thead><tr>
<th>Jogo</th><th>Mercado</th><th>Seleção</th>
<th class="num">Melhor</th><th>Casa</th>
<th class="num">Mediana</th><th class="num">Desvio</th>
<th class="num">Prob. cons.</th><th class="num">EV%</th><th>Confirma</th>
</tr></thead><tbody>{rows}</tbody></table></div>"""


def _results_page(params: dict[str, str], report) -> str:
    method = params.get("method", "shin")
    ev = params.get("ev", "2")
    csv_params = urlencode({**params})
    actionable = report.actionable
    outliers = sum(1 for v in actionable if v.is_outlier)
    only_one = sum(1 for v in actionable if len(v.flagged_by) == 1)

    if report.has_whitelist:
        sections = (
            '<h2 style="font-size:1.05rem;margin:1rem 0 .3rem">✅ Acionável '
            '<span class="muted">— casas onde podes apostar</span></h2>'
            + _values_table(actionable)
            + '<h2 style="font-size:1.05rem;margin:1.4rem 0 .3rem">🔎 Referência '
            '<span class="muted">— valor noutras casas, só para calibrar o consenso</span></h2>'
            + _values_table(report.reference)
        )
    else:
        sections = _values_table(actionable)

    notes = []
    if outliers:
        notes.append(f"{outliers} outlier(s)")
    if only_one:
        notes.append(f"{only_one} confirmada(s) por só 1 método")
    ref_note = f", {len(report.reference)} de referência" if report.has_whitelist else ""
    note = (" · " + " · ".join(notes)) if notes else ""

    return f"""<!doctype html>
<html lang="pt"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Resultados — valor em odds</title>
<style>{_PAGE_CSS}</style>
</head><body>
<h1>⚽ Resultados</h1>
<div class="actions">
  <a href="/"><button class="secondary" type="button">◀ Nova pesquisa</button></a>
  <a href="/analyze.csv?{_esc(csv_params)}"><button type="button">⬇ Descarregar CSV</button></a>
</div>
{sections}
{_bookmaker_stats_html(report)}
<div class="summary">
  {len(actionable)} seleções acionáveis com EV positivo{_esc(ref_note)} de
  {report.markets_analyzed} mercados analisados
  ({report.markets_discarded_few_books} descartados por poucas casas;
  devig: {_esc(method)}, limite: +{_esc(ev)}%){_esc(note)}.
</div>
<p class="disclaimer">O consenso é uma estimativa, não a verdade. Uma odd muito acima
do resto pode ser valor genuíno ou erro/informação em falta. "Confirma" mostra se
os dois métodos de devig (Shin e proporcional) concordam — sinais de um só método
são menos robustos. Isto não é aconselhamento de apostas — joga de forma responsável.</p>
</body></html>"""


def _result_row(v: ValueSelection) -> str:
    cls = ' class="outlier"' if v.is_outlier else ""
    warns = ""
    if v.warnings:
        warns = (
            f'<tr><td colspan="{_COLSPAN}" class="warn">⚠ '
            + " · ".join(_esc(w) for w in v.warnings)
            + "</td></tr>"
        )
    agree_cls = "" if len(v.flagged_by) == len(("shin", "proportional")) else ' class="warn"'
    return f"""<tr{cls}>
<td>{_esc(v.game)}</td><td>{_esc(v.market)}</td><td>{_esc(v.selection)}</td>
<td class="num">{v.best_odds:.2f}</td><td>{_esc(v.best_book)}</td>
<td class="num">{v.median_odds:.2f}</td><td class="num">{v.odds_dispersion:.2f}</td>
<td class="num">{v.consensus_prob * 100:.1f}%</td>
<td class="num ev">{v.ev_pct:+.1f}%</td>
<td{agree_cls}>{_esc(v.agreement)}</td>
</tr>{warns}"""


def _bookmaker_stats_html(report) -> str:
    """(4) Tabela: quantas vezes cada casa deu a melhor odd."""
    counts = report.best_book_counts
    if not counts:
        return ""
    total = report.selections_evaluated
    rows = ""
    for book, count in counts.most_common():
        share = count / total * 100 if total else 0.0
        flag = ' class="warn"' if share >= 40 and total >= 5 else ""
        note = " ⚠ possível outlier sistemático" if flag else ""
        rows += (f'<tr><td>{_esc(book)}</td><td class="num">{count}</td>'
                 f'<td class="num"{flag}>{share:.1f}%{_esc(note)}</td></tr>')
    return f"""<h2 style="font-size:1rem;margin:1.2rem 0 .3rem">Melhor odd por casa
<span class="muted">(em {total} seleções)</span></h2>
<div class="tablewrap"><table>
<thead><tr><th>Casa</th><th class="num">Nº</th><th class="num">%</th></tr></thead>
<tbody>{rows}</tbody></table></div>"""


def _run(params: dict[str, str]):
    """Corre o pipeline a partir dos parâmetros do formulário."""
    demo = bool(params.get("demo"))
    try:
        ev_threshold = float(params.get("ev", "2")) / 100.0
    except ValueError:
        ev_threshold = 0.02
    method = params.get("method", "shin")
    if method not in ("shin", "proportional"):
        method = "shin"

    games = load_games(
        from_json=_SAMPLE if demo else None,
        sport=params.get("sport", "soccer_epl"),
        regions=params.get("regions", "eu,uk"),
        markets=params.get("markets", "h2h,totals"),
    )
    return analyze_games(
        games, method=method, ev_threshold=ev_threshold,
        whitelist=params.get("books") or None,
    )


class Handler(BaseHTTPRequestHandler):
    server_version = "OddsValue/0.1"

    def _send(self, body: str, ctype: str = "text/html; charset=utf-8",
              status: int = 200, extra_headers: dict[str, str] | None = None) -> None:
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(payload)))
        for k, val in (extra_headers or {}).items():
            self.send_header(k, val)
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:  # noqa: N802 (nome imposto pela stdlib)
        parsed = urlparse(self.path)
        params = {k: v[0] for k, v in parse_qs(parsed.query).items()}

        if parsed.path in ("/", "/index.html"):
            self._send(_form_page(params))
            return

        if parsed.path == "/health":
            self._send("ok", ctype="text/plain; charset=utf-8")
            return

        if parsed.path in ("/analyze", "/analyze.csv"):
            try:
                report = _run(params)
            except MissingApiKey:
                self._send(_form_page(
                    params,
                    "Falta a chave ODDS_API_KEY. Define-a no servidor ou ativa a demo.",
                ))
                return
            except Exception as exc:  # rede/parse/etc. — mostra ao utilizador
                self._send(_form_page(params, f"Erro ao obter/analisar odds: {exc}"))
                return

            if parsed.path == "/analyze.csv":
                self._send(
                    values_to_csv(report.values),
                    ctype="text/csv; charset=utf-8",
                    extra_headers={
                        "Content-Disposition": 'attachment; filename="valor.csv"'
                    },
                )
            else:
                self._send(_results_page(params, report))
            return

        self._send("404", status=404, ctype="text/plain; charset=utf-8")

    def log_message(self, fmt: str, *args) -> None:  # silencia o log ruidoso
        return


def main() -> int:
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"A servir em http://{host}:{port}  (Ctrl+C para parar)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nA encerrar.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
