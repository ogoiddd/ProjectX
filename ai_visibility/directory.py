"""Gera a **Directory Page** AI-friendly — o *deliverable* de $600/mês.

É uma página HTML autónoma (imprimível ou publicável em qualquer domínio) que
inclui:

- H1/H2 com nome + categoria + localização (sinais fortes para LLMs);
- Descrição rica dos serviços (blocos por categoria);
- FAQ com 10 perguntas/respostas geradas a partir da categoria detetada;
- JSON-LD ``LocalBusiness`` com NAP, geo, área servida e horário;
- JSON-LD ``FAQPage`` com as mesmas Q&A em formato máquina;
- ``BreadcrumbList`` para contexto de navegação.

Sem framework nem CSS externo — pronta a colar em qualquer site ou a servir
como página independente.
"""

from __future__ import annotations

import html
import json
from typing import Any

from .fetch import BusinessProfile

# Templates de FAQ por categoria — perguntas que compradores reais fazem ao AI.
_FAQ_TEMPLATES: dict[str, list[tuple[str, str]]] = {
    "roofing contractor": [
        ("How much does a new roof cost in {loc}?",
         "In {loc}, a full replacement typically ranges from $9,000 to $25,000 depending on square footage, roofing material (shingle, tile, or metal), and roof pitch. {name} provides itemized estimates after an on-site inspection."),
        ("How long does a roof replacement take?",
         "Most residential replacements are completed in 1–3 days once the crew starts. Weather delays are the main variable in {loc}'s climate."),
        ("Do you handle insurance claims for storm damage?",
         "Yes — {name} works directly with homeowners insurance adjusters, documenting damage and providing the reports required for a claim."),
        ("Are you licensed and insured to do roofing in {loc}?",
         "Yes. {name} carries a state contractor's license, general liability, and workers' compensation. License numbers are available on request."),
        ("What roofing materials do you install?",
         "Asphalt shingle, concrete tile, clay tile, standing-seam metal, and modified bitumen for low-slope sections. {name} matches material to the home's structure and the local wind zone."),
        ("Do you offer financing?",
         "Financing is available through our lending partners with 0% intro APR options for qualifying homeowners."),
        ("How long is the warranty on a new roof?",
         "Materials are covered by the manufacturer (25–50 years depending on the product). {name}'s workmanship warranty is 10 years — transferable to a new owner."),
        ("Can you repair a leak without a full replacement?",
         "Yes. Targeted repairs are usually possible when the underlayment is intact and damage is localized."),
        ("Do you serve areas outside {loc}?",
         "{name} serves {loc} and neighboring communities. Contact us to confirm coverage for your address."),
        ("What's included in a free roof inspection?",
         "A full walk of the roof, attic ventilation check, drip-edge and flashing review, photo documentation, and a written report with recommended actions."),
    ],
    "window and door contractor": [
        ("How much do impact windows cost in {loc}?",
         "In {loc}, impact windows typically cost $900–$1,600 per opening installed. Larger sliders and picture windows run higher. {name} provides written estimates after measurement."),
        ("Are impact windows required in {loc}?",
         "In coastal high-velocity hurricane zones (HVHZ), building codes require impact-rated glazing or approved shutters on all openings. {name} installs code-compliant systems."),
        ("Do impact windows lower insurance premiums?",
         "Yes — most insurers offer a wind-mitigation discount when impact windows are documented via a certified inspection."),
        ("How long does installation take?",
         "Typical whole-home installs run 2–4 days once product arrives; lead times for custom sizes are 6–10 weeks."),
        ("What brands do you install?",
         "{name} installs multiple hurricane-rated brands (PGT, ES Windows, CGI, and others), choosing based on impact rating, energy performance, and homeowner budget."),
        ("Do you offer financing?",
         "Yes — 0% and low-APR plans are available through our lending partners for qualifying homeowners."),
        ("Are you licensed and insured?",
         "Yes. {name} holds the required state contractor licenses plus general liability and workers' compensation."),
        ("Do you handle the permit and inspection?",
         "{name} pulls all required permits and coordinates the municipal inspection at completion."),
        ("What's the warranty?",
         "Manufacturer warranties on glass and frames (10–25 years typical) plus {name}'s installation warranty."),
        ("Can I finance through PACE or My Safe Florida Home in {loc}?",
         "Where available, PACE financing and My Safe Florida Home grants can offset costs. {name} guides eligible homeowners through the application."),
    ],
    "HVAC contractor": [
        ("How much is a new AC system in {loc}?",
         "Full system replacements typically run $6,500–$14,000 depending on tonnage, SEER rating, ducts and installation complexity."),
        ("Are you licensed and insured for HVAC work in {loc}?",
         "Yes, {name} holds the required state HVAC license, EPA 608 refrigerant certification, and full insurance."),
        ("Do you offer emergency repairs?",
         "Yes — {name} runs same-day service for cooling failures in peak season."),
        ("What brands do you install?",
         "Trane, Carrier, Rheem, and Goodman among others; {name} matches system to home load."),
        ("Do you provide maintenance plans?",
         "Yes — twice-yearly checkups keep systems efficient and warranties valid."),
        ("Will a new system lower my electric bill?",
         "Upgrading from a SEER-12 to a SEER-16 system typically saves 20–30% on cooling costs."),
        ("Do you offer financing?",
         "Yes — 0% intro APR options for qualifying homeowners."),
        ("How long does installation take?",
         "Most residential swaps complete in a single day."),
        ("What's the warranty?",
         "Standard 10-year manufacturer parts + {name}'s 2-year labor warranty."),
        ("Do you install heat pumps?",
         "Yes — including cold-climate and ducted mini-split systems."),
    ],
}

_GENERIC_FAQ = [
    ("What areas do you serve?", "{name} serves {loc} and surrounding areas."),
    ("Are you licensed and insured?", "Yes — {name} carries the required licenses and full insurance."),
    ("Do you offer free estimates?", "Yes, {name} provides free written estimates."),
    ("How can I get in touch?", "Call {phone} or reach out through the contact form on our site."),
    ("How long have you been in business?", "{name} has years of local experience serving {loc}."),
    ("Do you offer financing?", "Yes — flexible financing options for qualifying customers."),
    ("What sets you apart from competitors?", "Local ownership, transparent pricing, and a workmanship warranty backed by {name}."),
    ("Do you provide emergency service?", "Yes — same-day availability for urgent issues in {loc}."),
    ("What's your typical turnaround?", "Most projects are scheduled within a few business days."),
    ("What's the warranty on your work?", "Every project comes with a written warranty covering both parts and labor."),
]

_SERVICE_BLOCKS: dict[str, list[tuple[str, str]]] = {
    "roofing contractor": [
        ("Roof replacement",
         "Full tear-off and replacement using shingles, tile, or standing-seam metal — matched to your home and the local wind zone."),
        ("Roof repair",
         "Targeted leak repair, flashing replacement, and storm damage restoration with photo documentation for insurance claims."),
        ("Storm damage & insurance claims",
         "We work directly with your insurer, providing inspection reports and estimates to support your claim."),
        ("Free roof inspection",
         "On-site inspection with attic check and written recommendations — no obligation."),
    ],
    "window and door contractor": [
        ("Impact window installation",
         "Hurricane-rated windows in every configuration — single hung, sliding, casement, picture and architectural shapes."),
        ("Impact doors",
         "Front, French, sliding and pivot doors rated for HVHZ zones."),
        ("Wind mitigation inspections",
         "Documented reports that unlock homeowners insurance discounts."),
        ("Financing & incentives",
         "PACE and My Safe Florida Home eligibility support where available."),
    ],
    "HVAC contractor": [
        ("System installation", "Right-sized systems from leading manufacturers, installed by NATE-certified technicians."),
        ("Emergency repair", "Same-day cooling and heating repair, 7 days a week."),
        ("Maintenance plans", "Twice-yearly service keeps systems efficient and warranties valid."),
        ("Indoor air quality", "Upgrades for filtration, humidity control and duct sealing."),
    ],
}

_GENERIC_SERVICES = [
    ("Consultation", "Free consultation with a written scope and estimate."),
    ("Installation", "Licensed and insured installation by an in-house crew."),
    ("Repair & maintenance", "Emergency and scheduled service for existing customers."),
    ("Warranty support", "Written workmanship warranty backed by {name}."),
]


def _esc(x: Any) -> str:
    return html.escape(str(x))


def _fmt(s: str, ctx: dict[str, str]) -> str:
    for k, v in ctx.items():
        s = s.replace("{" + k + "}", v)
    return s


def _faq_for(category: str) -> list[tuple[str, str]]:
    return _FAQ_TEMPLATES.get(category, _GENERIC_FAQ)


def _services_for(category: str) -> list[tuple[str, str]]:
    return _SERVICE_BLOCKS.get(category, _GENERIC_SERVICES)


def build_local_business_jsonld(profile: BusinessProfile, faq: list[tuple[str, str]]) -> dict[str, Any]:
    """Devolve o JSON-LD LocalBusiness pronto a serializar."""
    type_map = {
        "roofing contractor": "RoofingContractor",
        "window and door contractor": "HomeAndConstructionBusiness",
        "HVAC contractor": "HVACBusiness",
        "plumber": "Plumber",
        "electrician": "Electrician",
        "dentist": "Dentist",
        "law firm": "LegalService",
        "restaurant": "Restaurant",
    }
    biz_type = type_map.get(profile.category, "LocalBusiness")

    addr: dict[str, Any] = {"@type": "PostalAddress"}
    if profile.city:
        addr["addressLocality"] = profile.city
    if profile.state:
        addr["addressRegion"] = profile.state
    if profile.country:
        addr["addressCountry"] = profile.country

    obj: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": biz_type,
        "name": profile.name,
        "url": profile.fetched_url or profile.url,
        "description": (profile.og_description or profile.description
                        or f"{profile.name} — {profile.category} serving {profile.city or profile.state}."),
        "address": addr,
        "areaServed": profile.city or profile.state or "Local area",
    }
    if profile.phone:
        obj["telephone"] = profile.phone
    if profile.og_image:
        obj["image"] = profile.og_image

    return obj


def build_faqpage_jsonld(faq: list[tuple[str, str]]) -> dict[str, Any]:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faq
        ],
    }


def render_directory_html(profile: BusinessProfile) -> str:
    """Devolve o HTML autónomo da directory page."""
    loc = profile.city or profile.state or "your area"
    ctx = {
        "name": profile.name,
        "loc": loc,
        "phone": profile.phone or "our office",
    }
    faq_raw = _faq_for(profile.category)
    faq = [(_fmt(q, ctx), _fmt(a, ctx)) for q, a in faq_raw]
    services = [(t, _fmt(d, ctx)) for t, d in _services_for(profile.category)]

    local_biz_ld = build_local_business_jsonld(profile, faq)
    faqpage_ld = build_faqpage_jsonld(faq)
    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": profile.url},
            {"@type": "ListItem", "position": 2,
             "name": f"{profile.category.title()} in {loc}",
             "item": (profile.url.rstrip("/") + "/directory")},
        ],
    }

    services_html = "".join(
        f"<article><h3>{_esc(t)}</h3><p>{_esc(d)}</p></article>"
        for t, d in services
    )
    faq_html = "".join(
        f"<details><summary>{_esc(q)}</summary><p>{_esc(a)}</p></details>"
        for q, a in faq
    )

    css = """
    :root { color-scheme: light dark; }
    * { box-sizing: border-box; }
    body { font-family: -apple-system, system-ui, Segoe UI, Roboto, sans-serif;
           max-width: 880px; margin: 0 auto; padding: 2rem; line-height: 1.55;
           color: #111; background: #fff; }
    header { padding: 2rem 0; border-bottom: 1px solid #e5e7eb; margin-bottom: 2rem; }
    .breadcrumbs { font-size: .82rem; color: #6b7280; margin-bottom: .8rem; }
    h1 { font-size: 2rem; margin: .2rem 0; letter-spacing: -.01em; }
    .tagline { font-size: 1.05rem; color: #4b5563; margin: .3rem 0 1rem; }
    .cta { display: inline-block; padding: .75rem 1.2rem; border-radius: 10px;
           background: #2563eb; color: #fff; font-weight: 700;
           text-decoration: none; }
    section { margin: 2rem 0; }
    section h2 { font-size: 1.25rem; margin: 0 0 1rem;
                 border-left: 4px solid #2563eb; padding-left: .6rem; }
    .services { display: grid; grid-template-columns: repeat(auto-fit,minmax(260px,1fr));
                gap: 1rem; }
    .services article { padding: 1rem; border: 1px solid #e5e7eb; border-radius: 12px; }
    .services h3 { margin: 0 0 .3rem; font-size: 1rem; }
    details { padding: .8rem 1rem; border-bottom: 1px solid #e5e7eb; }
    details summary { cursor: pointer; font-weight: 600; }
    details p { margin: .5rem 0 0; color: #374151; }
    footer { margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #e5e7eb;
             font-size: .82rem; color: #6b7280; }
    """

    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_esc(profile.name)} — {_esc(profile.category.title())} in {_esc(loc)}</title>
<meta name="description" content="{_esc(profile.name)} — licensed {_esc(profile.category)} serving {_esc(loc)}. Services, FAQ, service area and contact info.">
<script type="application/ld+json">{json.dumps(local_biz_ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faqpage_ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(breadcrumb_ld, ensure_ascii=False)}</script>
<style>{css}</style>
</head><body>
<header>
  <div class="breadcrumbs">Home / {_esc(profile.category.title())} in {_esc(loc)}</div>
  <h1>{_esc(profile.name)} — {_esc(profile.category.title())} in {_esc(loc)}</h1>
  <div class="tagline">Licensed and insured local {_esc(profile.category)}. Serving {_esc(loc)} and nearby communities.</div>
  <a class="cta" href="{_esc(profile.fetched_url or profile.url)}">Get a free estimate</a>
</header>

<section>
  <h2>About {_esc(profile.name)}</h2>
  <p>{_esc(profile.og_description or profile.description or f"{profile.name} is a {profile.category} serving {loc}. We combine local expertise, transparent pricing and a written workmanship warranty on every job.")}</p>
</section>

<section>
  <h2>Services</h2>
  <div class="services">{services_html}</div>
</section>

<section>
  <h2>Service area</h2>
  <p>{_esc(profile.name)} serves {_esc(loc)} and neighboring communities. Contact us to confirm coverage for your address.</p>
</section>

<section>
  <h2>Frequently asked questions</h2>
  {faq_html}
</section>

<footer>
  Contact: {_esc(profile.phone or "see main site")} · {_esc(profile.fetched_url or profile.url)}
  <br>Directory page generated by ai_visibility — machine-readable via JSON-LD LocalBusiness + FAQPage.
</footer>
</body></html>"""
