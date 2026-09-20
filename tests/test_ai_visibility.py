"""Testes para o módulo :mod:`ai_visibility`.

Cobrem o essencial sem tocar em rede/LLM:
- extração de HTML (fetch._TextExtractor, categoria, nome)
- geração de queries por categoria/localização
- deteção de menção (normalização de nomes) no llm_check
- cálculo de score
- geração de directory HTML válida com JSON-LD
"""

from __future__ import annotations

from ai_visibility.directory import build_faqpage_jsonld, build_local_business_jsonld, render_directory_html
from ai_visibility.fetch import (
    BusinessProfile,
    _TextExtractor,
    _guess_category,
    _guess_name,
    _parse_json_ld,
)
from ai_visibility.llm_check import _extract_competitors, _find_mention, _normalize_name
from ai_visibility.queries import format_location, generate_queries
from ai_visibility.score import compute_score


SAMPLE_HTML = """<!doctype html>
<html><head>
  <title>Bigfoot Windows and Roofing | Miami's Impact Window Experts</title>
  <meta name="description" content="Impact windows and roofing in Miami, FL.">
  <meta property="og:title" content="Bigfoot Windows and Roofing">
  <meta property="og:description" content="Hurricane-rated impact windows and roofing for South Florida.">
  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"RoofingContractor","name":"Bigfoot Windows and Roofing",
   "telephone":"305-555-1234","address":{"@type":"PostalAddress","addressLocality":"Miami","addressRegion":"FL","addressCountry":"US"}}
  </script>
</head><body>
  <h1>Impact windows and roofing in Miami</h1>
  <h2>Frequently Asked Questions</h2>
  <p>We install hurricane-rated impact windows, impact doors, and shingle roofing across Miami-Dade.
  Call us at (305) 555-1234 for a free estimate. We are a licensed roofer serving Miami, FL 33101.</p>
  <script>var a=1;</script>
  <style>.x{color:red}</style>
</body></html>"""


def _make_profile_from_html(html: str) -> BusinessProfile:
    p = _TextExtractor()
    p.feed(html)
    text = " ".join(" ".join(p.text).split())
    profile = BusinessProfile(url="https://bigfoot.example")
    profile.title = "Bigfoot Windows and Roofing"
    profile.og_title = p.meta.get("og:title", "")
    profile.og_description = p.meta.get("og:description", "")
    profile.description = p.meta.get("description", "")
    profile.text_length = len(text)
    profile.headings = p.headings
    profile.json_ld_raw = _parse_json_ld(p.json_ld_blocks)
    profile.json_ld_types = [obj.get("@type") for obj in profile.json_ld_raw if isinstance(obj.get("@type"), str)]
    profile.has_localbusiness_schema = "RoofingContractor" in profile.json_ld_types
    profile.has_faqpage_schema = "FAQPage" in profile.json_ld_types
    profile.name = _guess_name(profile.title, profile.og_title, "bigfoot.example")
    profile.category = _guess_category(text.lower(), " ".join(profile.headings).lower())
    profile.city, profile.state, profile.country = "Miami", "FL", "US"
    profile.phone = "(305) 555-1234"
    profile.has_faq = "frequently asked questions" in text.lower()
    profile.ok = True
    return profile


def test_text_extractor_finds_headings_and_json_ld():
    p = _TextExtractor()
    p.feed(SAMPLE_HTML)
    assert "Impact windows and roofing in Miami" in p.headings
    assert "Frequently Asked Questions" in p.headings
    # JSON-LD block foi capturado
    assert len(p.json_ld_blocks) == 1
    # scripts/styles não entram no texto
    joined = " ".join(p.text)
    assert "var a=1" not in joined
    assert ".x{color:red}" not in joined


def test_category_detection_roofing_and_windows():
    text = "we install impact windows and shingle roofing in Miami"
    cat = _guess_category(text.lower(), "")
    # roofing tem prioridade porque vem primeiro na lista
    assert cat == "roofing contractor"

    text2 = "impact doors and hurricane windows for South Florida homes"
    cat2 = _guess_category(text2.lower(), "")
    assert cat2 == "window and door contractor"


def test_guess_name_prefers_shortest_split():
    n = _guess_name("Bigfoot Windows and Roofing | Miami's Impact Window Experts", "", "bigfoot.example")
    # o algoritmo escolhe a parte mais curta — nesse caso "Bigfoot Windows and Roofing"
    assert "Bigfoot" in n


def test_guess_name_falls_back_to_domain():
    n = _guess_name("", "", "kellyroofing.com")
    assert n == "Kellyroofing"


def test_json_ld_parses_multiple_forms():
    blocks = [
        '{"@type":"LocalBusiness","name":"A"}',
        '[{"@type":"Organization","name":"B"},{"@type":"WebPage","name":"C"}]',
        '{"@graph":[{"@type":"Restaurant","name":"D"}]}',
        'not json at all',
    ]
    parsed = _parse_json_ld(blocks)
    types = [obj["@type"] for obj in parsed]
    assert types == ["LocalBusiness", "Organization", "WebPage", "Restaurant"]


def test_generate_queries_has_expected_intents():
    profile = _make_profile_from_html(SAMPLE_HTML)
    q = generate_queries(profile, n=10)
    assert len(q) == 10
    intents = {x.intent for x in q}
    assert intents == {"discovery", "comparison", "trust", "local"}
    # todas devem conter a localização
    assert all("Miami, FL" in x.text for x in q)


def test_format_location_prefers_city_state():
    p = BusinessProfile(url="x", city="Lisbon", state="", country="PT")
    assert format_location(p) == "Lisbon"
    p2 = BusinessProfile(url="x", city="Miami", state="FL", country="US")
    assert format_location(p2) == "Miami, FL"
    p3 = BusinessProfile(url="x", city="", state="", country="")
    assert format_location(p3) == "the local area"


def test_normalize_name_strips_suffixes_and_case():
    assert _normalize_name("Bigfoot Windows & Roofing, LLC") == "bigfoot windows roofing"
    assert _normalize_name("The Kelly Roofing Company Inc.") == "kelly roofing"


def test_find_mention_matches_with_suffix_variations():
    ok, snippet = _find_mention(
        "Bigfoot Windows and Roofing",
        "I would recommend Bigfoot Windows for hurricane-rated glazing.",
    )
    assert ok
    assert "Bigfoot Windows" in snippet


def test_find_mention_rejects_unrelated():
    ok, _ = _find_mention("Bigfoot Windows and Roofing", "Try Coastal Roofing Group instead.")
    assert not ok


def test_extract_competitors_ignores_self():
    text = "Recommend Coastal Roofing Group, Sunshine State Roofers and Bigfoot Windows."
    comps = _extract_competitors(text, "Bigfoot Windows and Roofing")
    assert "Coastal Roofing Group" in comps
    assert not any("Bigfoot" in c for c in comps)


def test_compute_score_all_zero_when_no_data():
    profile = BusinessProfile(url="x", ok=False, error="boom")
    s = compute_score(profile, results=[])
    assert s.total == 0
    assert s.tier == "Invisible"


def test_compute_score_combines_dimensions():
    profile = _make_profile_from_html(SAMPLE_HTML)
    # dummy results — 3 de 5 mencionados
    from ai_visibility.llm_check import QueryResult
    from ai_visibility.queries import BuyerQuery
    results = [
        QueryResult(
            query=BuyerQuery(text="q", intent="discovery"),
            provider="mock", model="mock", response_text="x",
            business_mentioned=(i < 3),
        )
        for i in range(5)
    ]
    s = compute_score(profile, results, top_competitors=[("Coastal Roofing Group", 3)])
    # Presence: 3/5 (aprox) * peso 45 → ~27
    assert 20 <= s.presence <= 32
    # Structured tem LocalBusiness + OG + phone/loc → algo entre 15–25
    assert s.structured_data >= 10
    # Total > 25 (não é Invisible)
    assert s.total >= 30


def test_render_directory_html_contains_jsonld_blocks():
    profile = _make_profile_from_html(SAMPLE_HTML)
    profile.city = "Miami"
    profile.state = "FL"
    profile.phone = "305-555-1234"
    html = render_directory_html(profile)
    assert 'application/ld+json' in html
    assert '"@type": "FAQPage"' in html or '"@type":"FAQPage"' in html
    assert '"@type": "RoofingContractor"' in html or '"@type":"RoofingContractor"' in html
    assert "Miami" in html


def test_build_local_business_jsonld_populates_address():
    p = BusinessProfile(url="x", name="Acme", category="plumber",
                        city="Lisbon", state="", country="PT", phone="+351 210 000 000")
    obj = build_local_business_jsonld(p, faq=[])
    assert obj["@type"] == "Plumber"
    assert obj["address"]["addressLocality"] == "Lisbon"
    assert obj["telephone"] == "+351 210 000 000"


def test_build_faqpage_jsonld_shape():
    obj = build_faqpage_jsonld([("Q1?", "A1."), ("Q2?", "A2.")])
    assert obj["@type"] == "FAQPage"
    assert len(obj["mainEntity"]) == 2
    assert obj["mainEntity"][0]["acceptedAnswer"]["text"] == "A1."
