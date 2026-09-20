"""Corre queries num LLM e verifica se o negócio é mencionado na resposta.

Suporta:
- **OpenAI ChatGPT** (via API `chat.completions`) — precisa de ``OPENAI_API_KEY``.
- **Mock**                                        — sem chave, resposta gerada
  deterministicamente a partir da categoria + localização; útil para demos
  e para testar o pipeline sem gastar créditos.

A **deteção de menção** é feita em Python (não pedimos ao próprio LLM que
julgue), para ser barata e determinística:
- normalizamos nome (lowercase, sem "the ", sem sufixos LLC/Inc/&…) e vemos
  se aparece como subsequência na resposta;
- variações de espaçamento/pontuação toleradas;
- também extraímos até N nomes de "concorrentes" mencionados na resposta
  (nomes próprios detetados por regex simples), para a recomendação.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import re
import time
from dataclasses import dataclass, field
from typing import Any

import requests

from .queries import BuyerQuery

OPENAI_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_DEFAULT_MODEL = "gpt-4o-mini"

# palavras que separamos do nome comercial antes de comparar
_NAME_STRIP = re.compile(
    r"\b(the|inc\.?|llc|ltd\.?|corp\.?|company|co\.?|group|"
    r"holdings|services|service|solutions|&|and)\b",
    re.IGNORECASE,
)

# extrai "Nomes Próprios Duas ou Três Palavras" para candidatos a concorrentes
_PROPER_NOUN_RE = re.compile(r"\b([A-Z][a-zA-Z&\-]+(?:\s+[A-Z][a-zA-Z&\-]+){1,3})\b")

# palavras que capitalizadas em início de frase não são parte de um nome
# comercial; se a primeira palavra do match for uma destas, é descascada.
_LEADING_STOPWORDS = {
    "the", "a", "an", "recommend", "recommended", "consider", "try",
    "check", "visit", "contact", "call", "email", "look", "search",
    "find", "here", "for", "in", "at", "some", "many", "several",
    "best", "top", "leading", "premier", "great", "good", "reputable",
    "trusted", "licensed", "family", "local", "new", "old",
    "yes", "no", "sure", "however", "although", "meanwhile", "also",
    "and", "but", "or", "so",
}


@dataclass
class QueryResult:
    """Resultado de correr uma :class:`BuyerQuery` no LLM."""

    query: BuyerQuery
    provider: str
    model: str
    response_text: str
    business_mentioned: bool
    competitors_mentioned: list[str] = field(default_factory=list)
    latency_ms: int = 0
    error: str = ""
    # janela de contexto extraída à volta da menção (para o relatório)
    mention_snippet: str = ""


def _normalize_name(name: str) -> str:
    """Prepara um nome comercial para comparação difusa."""
    if not name:
        return ""
    n = _NAME_STRIP.sub(" ", name)
    n = re.sub(r"[^\w\s]", " ", n)
    n = " ".join(n.split()).lower().strip()
    return n


def _find_mention(business_name: str, response_text: str) -> tuple[bool, str]:
    """Devolve (aparece?, snippet de contexto)."""
    norm_name = _normalize_name(business_name)
    if not norm_name:
        return False, ""
    norm_resp = _normalize_name(response_text)
    idx = norm_resp.find(norm_name)
    if idx < 0:
        # tenta com só as 2 primeiras palavras (ex.: "Bigfoot Windows" no lugar
        # de "Bigfoot Windows and Roofing" — o LLM pode encurtar)
        parts = norm_name.split()
        if len(parts) >= 3:
            head = " ".join(parts[:2])
            idx = norm_resp.find(head)
            if idx < 0:
                return False, ""
        else:
            return False, ""
    # snippet no texto original, aproximado
    orig = response_text
    start = max(0, min(len(orig), idx - 60))
    end = min(len(orig), idx + 140)
    snippet = " ".join(orig[start:end].split())
    return True, snippet


def _extract_competitors(response_text: str, exclude_name: str, limit: int = 5) -> list[str]:
    """Nomes próprios (>=2 palavras) mencionados, excluindo o próprio negócio."""
    excl = _normalize_name(exclude_name)
    seen: set[str] = set()
    result: list[str] = []
    for m in _PROPER_NOUN_RE.finditer(response_text):
        name = m.group(1).strip()
        # descasca stopwords no início (ex.: "Recommend Coastal Roofing Group")
        parts = name.split()
        while parts and parts[0].lower() in _LEADING_STOPWORDS:
            parts = parts[1:]
        if len(parts) < 2:
            continue
        name = " ".join(parts)
        norm = _normalize_name(name)
        if not norm or norm in seen:
            continue
        # rejeita cabeçalhos comuns ("United States", "New York City", cidades soltas)
        low = norm.lower()
        if low in {"united states", "new york city", "los angeles",
                   "san francisco", "google maps", "yelp reviews", "better business",
                   "home advisor"}:
            continue
        if excl and (excl in norm or norm in excl):
            continue
        seen.add(norm)
        result.append(name)
        if len(result) >= limit:
            break
    return result


# --------------------------------------------------------------------------- #
# Providers
# --------------------------------------------------------------------------- #
def _call_openai(
    prompt: str,
    model: str,
    api_key: str,
    session: requests.Session,
    timeout: float,
    max_retries: int = 3,
) -> tuple[str, int]:
    """Chama o endpoint chat.completions e devolve (texto, latency_ms).

    Faz retry com backoff exponencial (1s, 2s, 4s) em 429/5xx — respeita o
    header ``Retry-After`` quando presente.
    """
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are ChatGPT answering a real user looking for a local business. "
                    "Respond as you would to a normal user: list 3-7 specific businesses "
                    "by name that best match, with a short reason each. Be concrete — do "
                    "not refuse to name businesses. If you cannot verify, say so briefly."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 500,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    t0 = time.time()
    last_status: int | None = None
    last_body: str = ""
    for attempt in range(max_retries + 1):
        resp = session.post(OPENAI_URL, json=payload, headers=headers, timeout=timeout)
        if resp.status_code < 400:
            latency_ms = int((time.time() - t0) * 1000)
            data = resp.json()
            text = data["choices"][0]["message"]["content"]
            return text, latency_ms

        last_status = resp.status_code
        last_body = (resp.text or "")[:400]
        # não tentar de novo em erros do cliente (excepto 429)
        retryable = resp.status_code == 429 or 500 <= resp.status_code < 600
        if not retryable or attempt == max_retries:
            break
        retry_after = resp.headers.get("Retry-After")
        wait = float(retry_after) if retry_after and retry_after.replace(".", "").isdigit() else (2 ** attempt)
        time.sleep(wait)

    raise RuntimeError(f"OpenAI HTTP {last_status}: {last_body}")


def _mock_response(prompt: str, category: str, location: str, business_name: str) -> str:
    """Resposta determinística sem chamar API — útil para demo/tests.

    A menção do negócio é decidida pelo hash do prompt para dar resultados
    consistentes entre execuções (e para o score não ficar zerado nem 100).
    Por defeito, o mock **não** menciona o negócio (para simular o cenário
    do vídeo: "showed up in 0 of them"). Menciona alguns concorrentes
    fictícios/plausíveis.
    """
    h = int(hashlib.sha256(prompt.encode()).hexdigest(), 16)
    rnd = random.Random(h)
    fake_competitors = [
        f"{location.split(',')[0]} Pro {category.title().split()[0]}s",
        f"Elite {category.title()}s",
        f"{location.split(',')[0]} Premier {category.title().split()[0]} Co.",
        f"Coastal {category.title().split()[0]} Group",
        f"Sunshine State {category.title()}s",
    ]
    rnd.shuffle(fake_competitors)
    picks = fake_competitors[:4]
    include_business = rnd.random() < 0.10  # 10% chance — simula baixa visibilidade
    if include_business:
        picks.insert(rnd.randint(1, 3), business_name)
    lines = [
        f"Here are some well-regarded {category}s in {location} you might consider:",
        "",
    ]
    for i, name in enumerate(picks, 1):
        lines.append(f"{i}. **{name}** — established local {category} with solid reviews.")
    lines.append("")
    lines.append(
        "Recommendation: always verify licensing, insurance, and recent Google reviews "
        "before hiring."
    )
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# API pública
# --------------------------------------------------------------------------- #
def run_queries(
    queries: list[BuyerQuery],
    business_name: str,
    category: str,
    location: str,
    *,
    provider: str = "auto",
    model: str = OPENAI_DEFAULT_MODEL,
    api_key: str | None = None,
    session: requests.Session | None = None,
    timeout: float = 40.0,
    delay_seconds: float = 0.0,
) -> list[QueryResult]:
    """Corre cada query no LLM e devolve os resultados.

    ``provider``:
      - ``"openai"``: força OpenAI (falha se não houver chave).
      - ``"mock"``:   força mock.
      - ``"auto"``:   usa OpenAI se ``OPENAI_API_KEY`` estiver definida,
                      caso contrário mock.
    """
    if provider not in {"openai", "mock", "auto"}:
        raise ValueError(f"provider inválido: {provider}")

    resolved_key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if provider == "auto":
        provider = "openai" if resolved_key else "mock"
    if provider == "openai" and not resolved_key:
        raise RuntimeError(
            "OPENAI_API_KEY não definida. Define-a ou usa provider='mock'."
        )

    sess = session or requests.Session()
    results: list[QueryResult] = []
    for q in queries:
        try:
            if provider == "openai":
                text, latency = _call_openai(q.text, model, resolved_key, sess, timeout)
                used_model = model
            else:
                t0 = time.time()
                text = _mock_response(q.text, category, location, business_name)
                latency = int((time.time() - t0) * 1000)
                used_model = "mock"
            mentioned, snippet = _find_mention(business_name, text)
            competitors = _extract_competitors(text, business_name)
            results.append(QueryResult(
                query=q,
                provider=provider,
                model=used_model,
                response_text=text,
                business_mentioned=mentioned,
                competitors_mentioned=competitors,
                latency_ms=latency,
                mention_snippet=snippet,
            ))
        except requests.RequestException as exc:
            results.append(QueryResult(
                query=q,
                provider=provider,
                model=model,
                response_text="",
                business_mentioned=False,
                error=f"network: {exc}",
            ))
        except RuntimeError as exc:
            # RuntimeError vem do _call_openai com o status HTTP + body
            results.append(QueryResult(
                query=q,
                provider=provider,
                model=model,
                response_text="",
                business_mentioned=False,
                error=str(exc),
            ))
        except Exception as exc:
            results.append(QueryResult(
                query=q,
                provider=provider,
                model=model,
                response_text="",
                business_mentioned=False,
                error=f"error: {exc}",
            ))

        if delay_seconds:
            time.sleep(delay_seconds)

    return results


def results_summary(results: list[QueryResult]) -> dict[str, Any]:
    """Métricas agregadas a partir dos resultados por query."""
    total = len(results)
    ok = [r for r in results if not r.error]
    hits = sum(1 for r in ok if r.business_mentioned)
    by_intent: dict[str, dict[str, int]] = {}
    for r in ok:
        d = by_intent.setdefault(r.query.intent, {"total": 0, "hits": 0})
        d["total"] += 1
        if r.business_mentioned:
            d["hits"] += 1

    all_competitors: dict[str, int] = {}
    for r in ok:
        for c in r.competitors_mentioned:
            all_competitors[c] = all_competitors.get(c, 0) + 1
    top_competitors = sorted(all_competitors.items(), key=lambda kv: -kv[1])[:10]

    return {
        "total_queries": total,
        "successful_queries": len(ok),
        "mention_hits": hits,
        "mention_rate": hits / len(ok) if ok else 0.0,
        "by_intent": by_intent,
        "top_competitors": top_competitors,
    }
