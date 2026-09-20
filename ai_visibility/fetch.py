"""Recolha e análise do site do negócio.

Extrai título, meta description, headings, texto visível, JSON-LD, tags
Open Graph, indicadores de NAP (Name/Address/Phone) e existência de FAQ.
Tudo só com stdlib (``html.parser``, ``re``, ``json``) + ``requests``.

Não é um scraper agressivo: uma única página (a landing) por omissão, com
User-Agent identificado. Respeita ``robots.txt`` no sentido em que só
descarrega o URL que o utilizador nos dá — não segue links profundos.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urljoin, urlparse

import requests

DEFAULT_UA = (
    "Mozilla/5.0 (compatible; AIVisibilityAuditor/0.1; "
    "+https://github.com/) requests/Python"
)

# Heurística leve para categoria — se aparecerem palavras destas, o negócio é
# categorizado assim. Ordem importa (primeira match ganha).
CATEGORY_KEYWORDS: list[tuple[str, list[str]]] = [
    ("roofing contractor",
     ["roofer", "roofing", "roof repair", "shingle", "tile roof", "flat roof"]),
    ("window and door contractor",
     ["impact window", "hurricane window", "replacement windows", "impact doors"]),
    ("HVAC contractor",
     ["hvac", "air conditioning", "heating and cooling", "ac repair"]),
    ("plumber",
     ["plumber", "plumbing", "leak repair", "water heater"]),
    ("electrician",
     ["electrician", "electrical contractor", "wiring", "panel upgrade"]),
    ("landscaper",
     ["landscap", "lawn care", "irrigation", "sod install"]),
    ("solar installer",
     ["solar panels", "solar installer", "photovoltaic"]),
    ("dentist",
     ["dentist", "dental clinic", "orthodontist", "implants"]),
    ("law firm",
     ["law firm", "attorney", "lawyer", "personal injury"]),
    ("real estate agent",
     ["realtor", "real estate", "homes for sale"]),
    ("restaurant",
     ["menu", "reservation", "restaurant", "chef"]),
    ("gym",
     ["gym", "personal trainer", "fitness studio", "crossfit"]),
]

# Sinais textuais de que existe uma secção de FAQ / Q&A na página.
FAQ_MARKERS = [
    "frequently asked questions", "faq", "perguntas frequentes",
    "common questions", "questions we get",
]

# Regex simples para telefone (US + internacional genérico) e código postal.
PHONE_RE = re.compile(
    r"(?:\+?\d{1,3}[\s.\-]?)?(?:\(\d{2,4}\)[\s.\-]?|\d{2,4}[\s.\-])\d{3,4}[\s.\-]?\d{3,4}"
)
US_ZIP_RE = re.compile(r"\b\d{5}(?:-\d{4})?\b")
STATE_RE = re.compile(
    r"\b(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|"
    r"MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|"
    r"WA|WV|WI|WY|DC)\b"
)


class MissingUrl(ValueError):
    """URL inválido ou vazio."""


@dataclass
class BusinessProfile:
    """Perfil derivado do site do negócio, tudo o que a auditoria precisa."""

    url: str
    fetched_url: str = ""            # URL final após redirects
    status_code: int = 0
    ok: bool = False
    error: str = ""

    title: str = ""
    description: str = ""
    og_title: str = ""
    og_description: str = ""
    og_image: str = ""

    name: str = ""                   # melhor palpite do nome comercial
    category: str = ""               # categoria heurística (ex.: "roofing contractor")
    city: str = ""
    state: str = ""
    country: str = ""
    phone: str = ""

    text_length: int = 0
    headings: list[str] = field(default_factory=list)
    keywords_hits: dict[str, int] = field(default_factory=dict)
    has_faq: bool = False

    json_ld_types: list[str] = field(default_factory=list)
    json_ld_raw: list[dict[str, Any]] = field(default_factory=list)
    has_schema_org_markup: bool = False
    has_localbusiness_schema: bool = False
    has_faqpage_schema: bool = False

    def as_dict(self) -> dict[str, Any]:
        d = self.__dict__.copy()
        # não incluir raw JSON-LD (pode ser grande) no dump principal
        d.pop("json_ld_raw", None)
        return d


class _TextExtractor(HTMLParser):
    """Extrai texto visível, headings, meta e blocos JSON-LD."""

    def __init__(self) -> None:
        super().__init__()
        self.text: list[str] = []
        self.headings: list[str] = []
        self.meta: dict[str, str] = {}          # description, og:*, keywords
        self.json_ld_blocks: list[str] = []

        self._skip_stack: list[str] = []        # dentro de script/style/nav/…
        self._current_heading: str | None = None
        self._current_json_ld: list[str] | None = None
        self._current_tag: str = ""

    _SKIP_TAGS = {"script", "style", "noscript", "template", "svg"}
    _HEAD_TAGS = {"h1", "h2", "h3"}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._current_tag = tag
        adict = {k: (v or "") for k, v in attrs}

        if tag == "meta":
            name = adict.get("name", "").lower()
            prop = adict.get("property", "").lower()
            content = adict.get("content", "").strip()
            if name in {"description", "keywords"}:
                self.meta[name] = content
            elif prop.startswith("og:"):
                self.meta[prop] = content

        if tag == "script" and adict.get("type", "").lower() == "application/ld+json":
            self._current_json_ld = []
            # ainda entra no skip_stack para não meter no texto visível

        if tag in self._SKIP_TAGS:
            self._skip_stack.append(tag)
            return

        if tag in self._HEAD_TAGS:
            self._current_heading = ""

    def handle_endtag(self, tag: str) -> None:
        if tag in self._SKIP_TAGS and self._skip_stack and self._skip_stack[-1] == tag:
            self._skip_stack.pop()

        if tag == "script" and self._current_json_ld is not None:
            self.json_ld_blocks.append("".join(self._current_json_ld))
            self._current_json_ld = None

        if tag in self._HEAD_TAGS and self._current_heading is not None:
            h = " ".join(self._current_heading.split()).strip()
            if h:
                self.headings.append(h)
            self._current_heading = None

    def handle_data(self, data: str) -> None:
        if self._current_json_ld is not None:
            self._current_json_ld.append(data)
            return
        if self._skip_stack:
            return
        if self._current_heading is not None:
            self._current_heading += data
        self.text.append(data)


def _clean_text(chunks: list[str]) -> str:
    joined = " ".join(chunks)
    # colapsar espaços e newlines
    return " ".join(joined.split())


def _parse_json_ld(blocks: list[str]) -> list[dict[str, Any]]:
    """Faz parse tolerante — cada bloco pode conter um objeto ou uma lista."""
    parsed: list[dict[str, Any]] = []
    for raw in blocks:
        raw = raw.strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            # muitos sites têm JSON-LD com trailing commas ou HTML entities; ignora
            continue
        if isinstance(obj, list):
            for item in obj:
                if isinstance(item, dict):
                    parsed.append(item)
        elif isinstance(obj, dict):
            # @graph pode conter vários nós
            graph = obj.get("@graph")
            if isinstance(graph, list):
                for item in graph:
                    if isinstance(item, dict):
                        parsed.append(item)
            else:
                parsed.append(obj)
    return parsed


def _extract_types(json_ld: list[dict[str, Any]]) -> list[str]:
    types: list[str] = []
    for obj in json_ld:
        t = obj.get("@type")
        if isinstance(t, str):
            types.append(t)
        elif isinstance(t, list):
            types.extend(x for x in t if isinstance(x, str))
    return types


def _guess_category(text_lower: str, headings_lower: str) -> str:
    haystack = f"{headings_lower} {text_lower}"
    for cat, keys in CATEGORY_KEYWORDS:
        for k in keys:
            if k in haystack:
                return cat
    return "local business"


def _guess_name(title: str, og_title: str, host: str) -> str:
    """Melhor palpite para o nome comercial.

    A `<title>` costuma vir como "Nome | Slogan" ou "Slogan - Nome". A OG title
    é geralmente mais limpa. Se nenhuma existir, deriva do domínio.
    """
    for candidate in (og_title, title):
        if not candidate:
            continue
        parts = re.split(r"\s+[\|\-–—]\s+", candidate)
        parts = [p.strip() for p in parts if p.strip()]
        if not parts:
            continue
        # heurística: se a última parte é mais curta e não parece slogan, é o nome
        if len(parts) == 1:
            return parts[0]
        parts.sort(key=lambda p: (len(p), p))  # a mais curta primeiro
        return parts[0]
    # do domínio: kellyroofing.com -> "Kellyroofing"
    domain = host.split(":")[0].removeprefix("www.")
    root = domain.split(".")[0]
    return root.replace("-", " ").title() if root else "Business"


def _guess_location(text: str, json_ld: list[dict[str, Any]]) -> tuple[str, str, str]:
    """Devolve (city, state, country) a partir do texto + JSON-LD."""
    city = state = country = ""

    for obj in json_ld:
        addr = obj.get("address")
        if isinstance(addr, dict):
            city = city or str(addr.get("addressLocality", "") or "")
            state = state or str(addr.get("addressRegion", "") or "")
            country = country or str(addr.get("addressCountry", "") or "")
        elif isinstance(addr, list) and addr:
            first = addr[0]
            if isinstance(first, dict):
                city = city or str(first.get("addressLocality", "") or "")
                state = state or str(first.get("addressRegion", "") or "")
                country = country or str(first.get("addressCountry", "") or "")

    if not state:
        m = STATE_RE.search(text)
        if m:
            state = m.group(0)
    if not city and state:
        # tenta apanhar "Cidade, ST"
        m = re.search(rf"([A-Z][a-zA-Z\.\s]{{2,30}}),\s*{state}\b", text)
        if m:
            city = m.group(1).strip()
    if state and not country:
        country = "US"
    return city, state, country


def fetch_business(
    url: str,
    session: requests.Session | None = None,
    timeout: float = 20.0,
    user_agent: str = DEFAULT_UA,
) -> BusinessProfile:
    """Descarrega e analisa a landing page do negócio.

    Nunca lança em caso de erro de rede: devolve um :class:`BusinessProfile`
    com ``ok=False`` e ``error`` preenchido, para o pipeline continuar (com
    score de conteúdo/structured data zerado).
    """
    if not url or not url.strip():
        raise MissingUrl("URL vazio.")
    if "://" not in url:
        url = "https://" + url.strip()

    sess = session or requests.Session()
    profile = BusinessProfile(url=url)

    try:
        resp = sess.get(
            url,
            timeout=timeout,
            headers={"User-Agent": user_agent, "Accept": "text/html,*/*;q=0.8"},
            allow_redirects=True,
        )
        profile.status_code = resp.status_code
        profile.fetched_url = resp.url
        resp.raise_for_status()
        html = resp.text
    except requests.RequestException as exc:
        profile.error = f"fetch failed: {exc}"
        return profile

    parser = _TextExtractor()
    try:
        parser.feed(html)
    except Exception as exc:  # HTMLParser é tolerante mas há PDFs, XML, etc.
        profile.error = f"parse failed: {exc}"
        return profile

    text = _clean_text(parser.text)
    profile.text_length = len(text)
    profile.headings = parser.headings[:30]
    profile.title = parser.meta.get("og:title") or _extract_title(html)
    profile.description = parser.meta.get("description", "")
    profile.og_title = parser.meta.get("og:title", "")
    profile.og_description = parser.meta.get("og:description", "")
    profile.og_image = parser.meta.get("og:image", "")
    if profile.og_image and profile.og_image.startswith("/"):
        profile.og_image = urljoin(profile.fetched_url or url, profile.og_image)

    profile.json_ld_raw = _parse_json_ld(parser.json_ld_blocks)
    profile.json_ld_types = _extract_types(profile.json_ld_raw)
    profile.has_schema_org_markup = bool(profile.json_ld_types) or "schema.org" in html
    profile.has_localbusiness_schema = any(
        t == "LocalBusiness" or (isinstance(t, str) and "Business" in t)
        for t in profile.json_ld_types
    ) or any(
        t in profile.json_ld_types for t in (
            "Restaurant", "Dentist", "Electrician", "Plumber", "HVACBusiness",
            "RoofingContractor", "HomeAndConstructionBusiness", "Store",
            "ProfessionalService",
        )
    )
    profile.has_faqpage_schema = "FAQPage" in profile.json_ld_types

    text_lower = text.lower()
    profile.has_faq = any(m in text_lower for m in FAQ_MARKERS)

    host = urlparse(profile.fetched_url or url).netloc
    profile.name = _guess_name(profile.title, profile.og_title, host)
    profile.category = _guess_category(text_lower, " ".join(h.lower() for h in profile.headings))

    m_phone = PHONE_RE.search(text)
    profile.phone = m_phone.group(0).strip() if m_phone else ""

    city, state, country = _guess_location(text, profile.json_ld_raw)
    profile.city, profile.state, profile.country = city, state, country

    # keywords_hits: contagem crua para reutilização no score
    hits: dict[str, int] = {}
    for _cat, keys in CATEGORY_KEYWORDS:
        for k in keys:
            c = text_lower.count(k)
            if c:
                hits[k] = c
    profile.keywords_hits = hits

    profile.ok = True
    return profile


def _extract_title(html: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if not m:
        return ""
    return " ".join(m.group(1).split())
