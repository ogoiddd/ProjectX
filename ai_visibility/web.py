"""Web app minimalista para correr a auditoria a partir do browser/telemóvel.

Só stdlib + ``requests`` (mesmo padrão da :mod:`odds_value.web`). Um formulário
com um campo (URL do negócio) e a escolha de provider (auto/openai/mock); ao
submeter, corre a auditoria e mostra o relatório inline com botões para
descarregar o directory page ou os dados brutos.

Executar:
    python -m ai_visibility.web        # http://localhost:8000
"""

from __future__ import annotations

import html
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

from .audit import run_audit


_FORM_CSS = """
:root { color-scheme: light dark; }
* { box-sizing: border-box; }
body { font-family: -apple-system, system-ui, Segoe UI, Roboto, sans-serif;
       margin: 0; padding: 1rem; max-width: 640px; margin: 0 auto;
       line-height: 1.5; }
h1 { font-size: 1.35rem; margin: .3rem 0 1rem; }
form { display: grid; gap: .8rem; padding: 1rem; border-radius: 12px;
       background: rgba(127,127,127,.08); }
label { display: grid; gap: .3rem; font-size: .85rem; font-weight: 600; }
input, select { padding: .7rem; font-size: 1rem; border-radius: 8px;
                border: 1px solid rgba(127,127,127,.35); background: transparent;
                color: inherit; }
button { padding: .8rem; font-size: 1rem; font-weight: 700; border: 0;
         border-radius: 10px; background: #2563eb; color: #fff; cursor: pointer; }
.hint { font-size: .82rem; opacity: .75; }
.warn { color: #b45309; margin: .4rem 0; }
"""


def _esc(x: object) -> str:
    return html.escape(str(x))


def _form(params: dict[str, str], msg: str = "") -> str:
    url = params.get("url", "")
    provider = params.get("provider", "auto")
    n_q = params.get("n", "10")
    msg_html = f'<p class="warn">{_esc(msg)}</p>' if msg else ""
    key_hint = ("OpenAI: variável OPENAI_API_KEY presente." if os.environ.get("OPENAI_API_KEY")
                else "OpenAI: sem OPENAI_API_KEY — usa 'mock' para demo.")
    return f"""<!doctype html>
<html lang="pt"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Visibility Auditor</title>
<style>{_FORM_CSS}</style>
</head><body>
<h1>🤖 AI Visibility Auditor</h1>
{msg_html}
<form method="get" action="/audit">
  <label>URL do negócio
    <input name="url" type="url" required
           placeholder="https://kellyroofing.com" value="{_esc(url)}">
  </label>
  <label>Provider
    <select name="provider">
      <option value="auto"{" selected" if provider == "auto" else ""}>Auto (OpenAI se disponível)</option>
      <option value="openai"{" selected" if provider == "openai" else ""}>OpenAI (ChatGPT)</option>
      <option value="mock"{" selected" if provider == "mock" else ""}>Mock (demo, sem chave)</option>
    </select>
  </label>
  <label>Nº de queries
    <input name="n" type="number" min="3" max="20" value="{_esc(n_q)}">
  </label>
  <button type="submit">Correr auditoria</button>
</form>
<p class="hint">{_esc(key_hint)}</p>
</body></html>"""


class Handler(BaseHTTPRequestHandler):
    server_version = "AIVisibility/0.1"

    def _send(self, body: str, ctype: str = "text/html; charset=utf-8",
              status: int = 200, extra: dict[str, str] | None = None) -> None:
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(payload)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:  # noqa: N802 (imposto pela stdlib)
        parsed = urlparse(self.path)
        params = {k: v[0] for k, v in parse_qs(parsed.query).items()}

        if parsed.path in ("/", "/index.html"):
            self._send(_form(params))
            return

        if parsed.path == "/health":
            self._send("ok", ctype="text/plain; charset=utf-8")
            return

        if parsed.path in ("/audit", "/audit/report", "/audit/directory", "/audit/data"):
            url = params.get("url", "").strip()
            if not url:
                self._send(_form(params, "Insere um URL."))
                return
            try:
                audit = run_audit(
                    url,
                    n_queries=int(params.get("n", 10) or 10),
                    provider=params.get("provider", "auto"),
                )
            except Exception as exc:  # noqa: BLE001
                self._send(_form(params, f"Erro na auditoria: {exc}"))
                return

            if parsed.path == "/audit/directory":
                self._send(audit.directory_html)
                return
            if parsed.path == "/audit/data":
                self._send(
                    json.dumps(audit.as_dict(), indent=2, ensure_ascii=False),
                    ctype="application/json; charset=utf-8",
                    extra={"Content-Disposition": 'attachment; filename="audit.json"'},
                )
                return

            # /audit ou /audit/report — mostra o relatório com uma barra de ações no topo
            actions = f"""<div style="position:sticky;top:0;background:#111;color:#fff;
padding:.6rem 1rem;display:flex;gap:.7rem;align-items:center;z-index:99">
<a href="/" style="color:#93c5fd;text-decoration:none">◀ Nova auditoria</a>
<a href="/audit/directory?{urlencode(params)}" style="color:#a7f3d0;text-decoration:none">Ver directory page</a>
<a href="/audit/data?{urlencode(params)}" style="color:#fcd34d;text-decoration:none">⬇ Dados (JSON)</a>
<span style="margin-left:auto;font-size:.8rem;opacity:.7">Cmd/Ctrl+P para imprimir → PDF</span>
</div>"""
            self._send(actions + audit.report_html)
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
