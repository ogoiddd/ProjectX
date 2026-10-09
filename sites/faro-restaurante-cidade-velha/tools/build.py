# -*- coding: utf-8 -*-
"""Generate the four static language pages (/, /en/, /fr/, /de/), the privacy pages (/privacidade/, /en/privacy/),
the 404 page and the sitemap from one template, then check every inline script against the CSP in public/vercel.json.
The output in public/ is plain HTML/CSS/JS: no build step is needed to deploy it.
Usage: python3 tools/build.py"""
import base64, hashlib, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from i18n import T, DISHES, Q_LANG          # noqa: E402
from art import hero_svg, dom_rodrigo_svg, LOGO, FAVICON, ICONS  # noqa: E402
from legal import L as LEGAL, PRIV_PATH, NOT_FOUND  # noqa: E402

PUB = os.path.join(HERE, "..", "public")
BASE = "https://cidade-velha-faro.vercel.app"
LANGS = ["pt", "en", "fr", "de"]
PATH = {"pt": "/", "en": "/en/", "fr": "/fr/", "de": "/de/"}
TEL = "+351289827145"
WA = "351916008548"            # [CONFIRMAR COM CLIENTE] mobile from Trip.com / allaboutportugal; WhatsApp not confirmed
EMAIL = ""                     # [CONFIRMAR COM CLIENTE] booking email unknown
LAT, LON = 37.0135551, -7.9345962
GMAPS_DIR = f"https://www.google.com/maps/dir/?api=1&destination={LAT},{LON}&travelmode=walking"
GMAPS_PLACE = "https://www.google.com/maps/search/?api=1&query=Restaurante+Cidade+Velha+R.+Domingos+Guieiro+19+Faro"
AMAPS = f"https://maps.apple.com/?daddr={LAT},{LON}&dirflg=w&q=Restaurante%20Cidade%20Velha"
FB = "https://www.facebook.com/restaurantecidadevelha/"
IG = "https://www.instagram.com/restaurantecidadevelha/"
LIVRO = "https://www.livroreclamacoes.pt/Inicio/"
RAL_URL = "https://www.consumoalgarve.pt/"
MAP_SVG = open(os.path.join(HERE, "map", "map.svg"), encoding="utf-8").read()


def tbc(s):
    """[[text]] -> visible placeholder badge."""
    return re.sub(r"\[\[(.+?)\]\]", lambda m: f'<span class="tbc">[{m.group(1)}]</span>', s)


def words(s):
    return " ".join(f'<span class="l">{w}</span>' for w in s.split())


def jsonld(L):
    t = T[L]
    data = {
        "@context": "https://schema.org",
        "@type": "Restaurant",
        "@id": BASE + "/#restaurante",
        "name": "Restaurante Cidade Velha",
        "url": BASE + PATH[L],
        "telephone": TEL,
        "image": BASE + "/assets/og.jpg",
        "description": t["desc"],
        "servesCuisine": ["Portuguese", "Algarvian", "Seafood"],
        "acceptsReservations": True,
        "hasMenu": BASE + PATH[L] + "#carta",
        "address": {"@type": "PostalAddress", "streetAddress": "Rua Domingos Guieiro 19", "postalCode": "8000-311",
                    "addressLocality": "Faro", "addressRegion": "Faro", "addressCountry": "PT"},
        "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LON},
        "hasMap": GMAPS_PLACE,
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                                       "opens": "11:00", "closes": "22:00"}],
        "sameAs": [FB, IG],
        "containedInPlace": {"@type": "TouristAttraction", "name": "Vila Adentro (Cidade Velha de Faro)"},
        "inLanguage": t["html_lang"],
    }
    return json.dumps(data, ensure_ascii=False, indent=1)


def map_svg(L):
    t = T[L]
    keys = {"map.title": t["map_title"], "map.desc": t["map_desc"], "map.se": t["map_se"], "map.largo": t["map_largo"],
            "map.arcovila": t["map_arcovila"], "map.arcorepouso": t["map_arcorepouso"]}
    s = MAP_SVG
    for k, v in keys.items():
        s = re.sub(rf'(data-i18n="{re.escape(k)}">)[^<]*(<)', lambda m: m.group(1) + html.escape(v) + m.group(2), s)
    return s.replace('data-i18n="map.', 'data-k="')


def menu(L):
    t = T[L]
    idx = {"pt": None, "en": 4, "fr": 5, "de": 6}[L]
    out = []
    for course, key in [("start", "c_start"), ("sea", "c_sea"), ("land", "c_land"), ("sweet", "c_sweet")]:
        items = []
        for c, did, pt, ptnote, *tr in DISHES:
            if c != course:
                continue
            sub = ptnote if L == "pt" else tr[idx - 4]
            sub_html = f'<span class="t">{html.escape(sub)}</span>' if sub else ""
            items.append(f'<li><span class="n" lang="pt-PT">{pt}</span><span class="p"><span aria-hidden="true">—&nbsp;€</span><span class="sr-only">{t["price_tbc"]}</span></span>{sub_html}</li>')
        out.append(f'<div class="course"><h3>{t[key]}</h3><ul class="dish">{"".join(items)}</ul></div>')
    return "".join(out)


def hours_rows(L):
    t = T[L]
    rows = []
    for i, d in enumerate(t["days"]):
        v = t["closed"] if i == 6 else "11:00 – 22:00"
        rows.append(f'<tr data-day="{i}" data-today=" · {t["today"]}"><th scope="row">{d}</th><td>{v}</td></tr>')
    return "".join(rows)


def time_options():
    opts = []
    for h in range(12, 22):
        for m in (0, 30):
            if h == 21 and m == 30:
                continue
            opts.append(f'<option>{h:02d}:{m:02d}</option>')
    return "".join(opts)


def page(L):
    t = T[L]
    I = ICONS
    pre = "" if L == "pt" else "../"
    alts = "".join(f'<link rel="alternate" hreflang="{T[x]["html_lang"]}" href="{BASE}{PATH[x]}">' for x in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{BASE}/en/">'
    og_alt = "".join(f'<meta property="og:locale:alternate" content="{T[x]["og_locale"]}">' for x in LANGS if x != L)
    langs = "".join(
        f'<a href="{PATH[x]}" hreflang="{T[x]["html_lang"]}" lang="{T[x]["html_lang"]}" title="{T[x]["name"]}"'
        + (' aria-current="page"' if x == L else "") + f'>{T[x]["label"]}</a>' for x in LANGS)
    eyebrow = "".join(f"<span>{e}</span>" for e in t["eyebrow"])
    tl = "".join(
        f'<li{" class=here" if i == len(t["tl"]) - 1 else ""}><b>{y}</b><span>{x}</span>' + (f"<small>{tbc(s)}</small>" if s else "") + "</li>"
        for i, (y, x, s) in enumerate(t["tl"]))
    niches = "".join(
        f'<figure class="niche"><div class="frame" tabindex="0" role="img" aria-label="{t["photo"]} {n}"><span>{t["photo"]}</span></div>'
        f'<figcaption><b>{i}</b>{n}</figcaption></figure>'
        for i, n in enumerate(t["niches"], 1))
    def quote(q, who):
        ql = Q_LANG[q]
        orig = t["q_orig"].get(ql, "") if ql != t["html_lang"] else ""
        return (f'<blockquote class="quote" lang="{ql}"><p>“{html.escape(q, quote=False)}”</p><footer lang="{t["html_lang"]}">{who}'
                + (f'<span class="orig">{orig}</span>' if orig else "") + "</footer></blockquote>")
    quotes = "".join(quote(q, who) for q, who in t["q"])
    quotes += f'<p class="quote-tbc">{tbc(t["q_tbc"])}</p>'
    tables = "".join(
        f'<label><input type="radio" name="mesa" value="{v}"{" checked" if i == 2 else ""}><span>{lbl}</span></label>'
        for i, (v, lbl) in enumerate(zip(["Mesa cá fora (esplanada)", "Na sala", "Tanto faz"], t["f_t"])))
    s1 = "".join(f"<li>{s}</li>" for s in t["s1"])
    s2 = "".join(f"<li>{s}</li>" for s in t["s2"])
    js_strings = dict(t["js"], days=t["days_short"], lang=L)
    stars = I["star"] * 4 + I["star_part"]
    f_priv = t["f_privacy"].replace("{priv}", PRIV_PATH[L])
    mail_btn = (f'<button class="btn btn-ghost" type="submit" name="via" value="mail">{I["mail"]}{t["f_mail"]}</button>')

    return f'''<!doctype html>
<html lang="{t["html_lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t["title"]}</title>
<meta name="description" content="{html.escape(t["desc"])}">
<link rel="canonical" href="{BASE}{PATH[L]}">
{alts}
<meta name="theme-color" content="#f4eee3">
<meta name="color-scheme" content="light">
<meta name="geo.region" content="PT-08"><meta name="geo.placename" content="Faro"><meta name="geo.position" content="{LAT};{LON}"><meta name="ICBM" content="{LAT}, {LON}">
<meta property="og:type" content="restaurant.restaurant">
<meta property="og:locale" content="{t["og_locale"]}">{og_alt}
<meta property="og:site_name" content="Restaurante Cidade Velha">
<meta property="og:title" content="{html.escape(t["og_title"])}">
<meta property="og:description" content="{html.escape(t["og_desc"])}">
<meta property="og:url" content="{BASE}{PATH[L]}">
<meta property="og:image" content="{BASE}/assets/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html.escape(t["hero_art"])}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" as="font" type="font/woff2" href="/fonts/bodoni-roman.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/fonts/bodoni-italic.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/fonts/jost.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/fonts/marcellus-sc.woff2" crossorigin>
<link rel="stylesheet" href="/styles.css">
<script>document.documentElement.classList.add("js")</script>
<script type="application/ld+json">{jsonld(L)}</script>
</head>
<body>
<a class="skip" href="#main">{t["skip"]}</a>
<header class="top">
 <div class="wrap">
  <a class="brand" href="{PATH[L]}">{LOGO}<span><b>Cidade Velha</b><small>{t["brand_sub"]}</small></span></a>
  <nav class="nav" aria-label="{t["nav_carta"]}, {t["nav_casa"]}…">
   <a href="#carta">{t["nav_carta"]}</a><a href="#casa">{t["nav_casa"]}</a><a href="#reservar">{t["nav_reservar"]}</a><a href="#chegar">{t["nav_chegar"]}</a>
  </nav>
  <nav class="langs" aria-label="{t["lang_label"]}">{langs}</nav>
  <a class="btn btn-small" href="#reservar">{t["btn_reservar"]}</a>
 </div>
</header>

<main id="main">
<section class="hero" aria-labelledby="h1">
 <div class="wrap">
  <div>
   <p class="eyebrow caps">{eyebrow}</p>
   <h1 id="h1">{words(t["h1a"])} <em>{words(t["h1b"])}</em></h1>
   <p class="lede">{t["lede"]}</p>
   <div class="hero-actions">
    <a class="btn" href="#reservar">{I["table"]}{t["btn_reservar"]}{I["arrow"]}</a>
    <a class="btn btn-ghost" href="tel:{TEL}">{I["phone"]}{t["btn_call"]}</a>
    <a class="btn btn-ghost btn-dir" href="#chegar">{I["pin"]}{t["btn_dir"]}</a>
   </div>
   <div class="hero-meta">
    <p class="status m0" data-status role="status"><span class="dot" aria-hidden="true"></span><span data-status-text>{t["status_default"]}</span></p>
    <a href="{GMAPS_PLACE}" rel="noopener">★ {t["rating_line"]}</a>
   </div>
  </div>
  <figure class="estampa m0">
   {hero_svg(t["hero_art"])}
   <span class="photo-tag">{t["photo_hero"]}</span>
   <figcaption><span>{t["hero_cap_l"]}</span><span>{t["hero_cap_r"]}</span></figcaption>
  </figure>
 </div>
</section>

<section class="ribbon" aria-label="{t["f1b"]} · {t["f2b"]} · {t["f3b"]}">
 <div class="wrap">
  <p class="fact"><b>{t["f1b"]}</b><span>{t["f1"]}</span></p>
  <p class="fact"><b>{t["f2b"]}</b><span>{t["f2"]}</span></p>
  <p class="fact"><b>{t["f3b"]}</b><span>{t["f3"]}</span></p>
 </div>
</section>

<section class="sec" id="carta" aria-labelledby="carta-h">
 <div class="wrap">
  <header class="sec-head"><span class="num">I</span><h2 id="carta-h">{t["carta_h"]}</h2><p class="sec-intro">{t["carta_intro"]}</p></header>
  <div class="carta-grid">
   <article class="sheet" aria-labelledby="carta-h">
    <p class="sheet-note"><span>{t["sheet_note"]}</span>{tbc(t["sheet_tbc"])}</p>
    <div class="courses">{menu(L)}</div>
    <p class="diet">{tbc(t["diet"])}</p>
    <p class="diet">{t["vat"]}</p>
    <p class="diet allergens">{tbc(t["allergens"])}</p>
   </article>
   <aside class="aside-dr" aria-labelledby="dr-h">
    <div class="plate">
     {dom_rodrigo_svg(t["dr_art"])}
     <h3 id="dr-h" lang="pt-PT">{t["dr_title"]}</h3>
     <p>{t["dr_text"]}</p>
     <span class="tbc">{t["dr_photo"]}</span>
    </div>
   </aside>
  </div>
 </div>
</section>

<section class="sec dark" id="casa" aria-labelledby="casa-h">
 <div class="wrap">
  <header class="sec-head"><span class="num">II</span><h2 id="casa-h">{t["casa_h"]}</h2><p class="sec-intro">{t["casa_intro"]}</p></header>
  <div class="casa-grid">
   <div>
    <blockquote class="pull" lang="{t["html_lang"]}"><p class="m0">{t["pull"]}</p></blockquote>
    <p class="pull-src">{t["pull_src"]}</p>
    <p>{tbc(t["casa_tbc"])}</p>
   </div>
   <div>
    <h3 class="caps tl-h">{t["tl_h"]}</h3>
    <ol class="timeline">{tl}</ol>
   </div>
  </div>
  <div class="niches" role="region" aria-label="{t["niches_label"]}" tabindex="0">{niches}</div>
  <p class="niches-hint" aria-hidden="true">{t["niches_hint"]}</p>
 </div>
</section>

<section class="sec reviews" aria-labelledby="rev-h">
 <div class="wrap">
  <div>
   <span class="num">III</span>
   <h2 id="rev-h" class="rev-h">{t["rev_h"]}</h2>
   <div class="score"><b>{t["f1b"]}</b><div class="stars" aria-hidden="true">{stars}</div><p>{t["rev_score"]}</p>
   <p class="more"><a href="{GMAPS_PLACE}" rel="noopener">{t["rev_more"]}</a></p></div>
  </div>
  <div class="quotes">{quotes}</div>
 </div>
</section>

<section class="sec reserve" id="reservar" aria-labelledby="res-h">
 <div class="wrap">
  <header class="sec-head"><span class="num">IV</span><h2 id="res-h">{t["res_h"]}</h2><p class="sec-intro">{t["res_intro"]}</p></header>
  <div class="reserve-grid">
   <form id="booking" novalidate data-wa="{WA}" data-email="{EMAIL}" data-tel="{TEL}">
    <div class="field"><label for="f-name">{t["f_name"]}</label><input id="f-name" name="nome" autocomplete="name" required maxlength="80" aria-describedby="e-name"><span class="err" id="e-name" aria-live="polite"></span></div>
    <div class="field half"><label for="f-date">{t["f_date"]}</label><input id="f-date" name="dia" type="date" required aria-describedby="e-date"><span class="err" id="e-date" aria-live="polite"></span></div>
    <div class="field half"><label for="f-time">{t["f_time"]}</label><select id="f-time" name="hora" required aria-describedby="e-time">{time_options()}</select><span class="err" id="e-time" aria-live="polite"></span></div>
    <div class="field half"><label for="f-people">{t["f_people"]}</label>
     <div class="stepper"><button type="button" data-step="-1" aria-label="{t["f_less"]}">−</button><input id="f-people" name="pessoas" type="number" inputmode="numeric" min="1" max="30" value="2"><button type="button" data-step="1" aria-label="{t["f_more"]}">+</button></div></div>
    <div class="field half"><label for="f-phone">{t["f_phone"]}</label><input id="f-phone" name="tel" type="tel" autocomplete="tel" inputmode="tel" maxlength="30"></div>
    <fieldset><legend>{t["f_table"]}</legend><div class="seg">{tables}</div></fieldset>
    <div class="field"><label for="f-notes">{t["f_notes"]}</label><textarea id="f-notes" name="notas" maxlength="300" placeholder="{t["f_notes_ph"]}"></textarea></div>
    <div class="form-actions">
     <button class="btn" type="submit" name="via" value="wa">{I["wa"]}{t["f_wa"]}</button>
     {mail_btn}
    </div>
    <p class="form-status" data-form-status role="status" aria-live="polite" hidden><span data-form-status-text></span> <a data-form-fallback href="#" rel="noopener" hidden>{t["js"]["fallback"]}</a></p>
    <noscript><p class="form-note nojs">{t["nojs"]}</p></noscript>
    <p class="form-note">{t["f_note"]}</p>
    <p class="form-note privacy-note">{f_priv}</p>
    <p class="form-note">{tbc(t["f_tbc"])}</p>
   </form>
   <div class="ticket-wrap">
    <div class="ticket" aria-live="polite">
     <h3><span>{t["ticket_h"]}</span><span>{t["ticket_tag"]}</span></h3>
     <pre lang="pt-PT" data-preview>{t["js"]["empty"]}</pre>
     <p class="hint">{t["ticket_hint"]}</p>
    </div>
    <blockquote class="tip"><p class="m0" lang="en">“{t["tip_q"]}”</p><cite>{t["tip_src"]}</cite></blockquote>
   </div>
  </div>
 </div>
</section>

<section class="sec" id="chegar" aria-labelledby="chegar-h">
 <div class="wrap">
  <header class="sec-head"><span class="num">V</span><h2 id="chegar-h">{t["chegar_h"]}</h2></header>
  <div class="chegar-grid">
   <div>
    <div class="routes" role="group" aria-label="{t["nav_chegar"]}">
     <button type="button" data-route="1" aria-pressed="true">{t["r1"]}</button>
     <button type="button" data-route="2" aria-pressed="false">{t["r2"]}</button>
    </div>
    <div data-steps="1"><p class="walk">{t["walk"]}<small>{t["walk_small"]}</small></p><ol class="steps">{s1}</ol></div>
    <div data-steps="2" hidden><p class="walk">{t["walk2"]}<small>{t["walk2_small"]}</small></p><ol class="steps">{s2}</ol></div>
    <p class="car">{tbc(t["car"])}</p>
    <div class="map-actions">
     <a class="btn" href="{GMAPS_DIR}" rel="noopener">{I["pin"]}{t["gmaps"]}</a>
     <a class="btn btn-ghost" href="{AMAPS}" rel="noopener">{t["amaps"]}</a>
    </div>
   </div>
   <figure class="map" data-route="1">{map_svg(L)}</figure>
  </div>
 </div>
</section>
</main>

<footer class="sec dark" id="contacto" aria-label="{t["h_where"]}">
 <div class="wrap">
  <div class="contact-grid">
   <div>
    <h3>{t["h_hours"]}</h3>
    <p class="status" data-status><span class="dot" aria-hidden="true"></span><span data-status-text>{t["status_default"]}</span></p>
    <table class="hours"><caption class="sr-only">{t["h_hours"]}</caption><tbody>{hours_rows(L)}</tbody></table>
    <p class="hours-note">{tbc(t["hours_tbc"])}</p>
   </div>
   <div>
    <h3>{t["h_where"]}</h3>
    <address>Rua Domingos Guieiro, 19<br>Largo da Sé · Vila Adentro<br>8000-311 Faro</address>
    <p class="mt-dir"><a href="{GMAPS_DIR}" rel="noopener">{t["gmaps"]}</a></p>
   </div>
   <div>
    <h3>{t["h_phone"]}</h3>
    <a class="big-tel" href="tel:{TEL}">289 827 145</a>
    <p class="mobile-note">{t["mobile"]} {tbc(t["mobile_tbc"])}</p>
    <p class="m0"><a href="{FB}" rel="noopener">{t["fb"]}</a> · <a href="{IG}" rel="noopener">{t["ig"]}</a></p>
   </div>
  </div>
  <div class="colophon">
   <p class="word" aria-hidden="true">Cidade <span>Velha</span></p>
   <div class="small">
    <span>© 2026 Restaurante Cidade Velha · R. Domingos Guieiro 19, 8000-311 Faro</span>
    <span>{tbc(t["entity"])}</span>
    <a href="{PRIV_PATH[L]}"{' hreflang="en"' if L in ("fr", "de") else ""}>{t["privacy_link"]}</a>
    <a href="{LIVRO}" rel="noopener">{t["complaints"]}</a>
    <a href="{RAL_URL}" rel="noopener">{t["ral"]}</a>
    <a href="https://www.openstreetmap.org/copyright" rel="noopener">{t["osm"]}</a>
   </div>
  </div>
 </div>
</footer>

<nav class="bar" aria-label="{t["bar_res"]} · {t["bar_call"]} · {t["bar_dir"]}">
 <a href="#reservar">{I["table"]}{t["bar_res"]}</a>
 <a href="tel:{TEL}">{I["phone"]}{t["bar_call"]}</a>
 <a href="{GMAPS_DIR}" rel="noopener">{I["pin"]}{t["bar_dir"]}</a>
</nav>
<script type="application/json" id="i18n">{json.dumps(js_strings, ensure_ascii=False)}</script>
<script src="/app.js" defer></script>
</body>
</html>
'''


def head_common(title, desc, canonical, lang_html, robots=""):
    return f"""<!doctype html>
<html lang="{lang_html}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{robots}{canonical}
<meta name="theme-color" content="#f4eee3">
<meta name="color-scheme" content="light">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preload" as="font" type="font/woff2" href="/fonts/bodoni-roman.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/fonts/jost.woff2" crossorigin>
<link rel="stylesheet" href="/styles.css">
</head>"""


def simple_footer():
    return f"""<footer class="sec dark legal-foot">
 <div class="wrap">
  <p class="m0">Restaurante Cidade Velha · Rua Domingos Guieiro, 19 · 8000-311 Faro · <a href="tel:{TEL}">289 827 145</a></p>
  <p class="m0"><a href="{LIVRO}" rel="noopener">Livro de Reclamações</a> · <a href="{RAL_URL}" rel="noopener">CIMAAL</a> · <a href="https://www.openstreetmap.org/copyright" rel="noopener">© OpenStreetMap</a></p>
 </div>
</footer>"""


def privacy_page(L):
    """Privacy policy + legal information. PT and EN only; FR/DE pages link to the EN version."""
    c = LEGAL[L]
    other = "en" if L == "pt" else "pt"
    canonical = (f'<link rel="canonical" href="{BASE}{PRIV_PATH[L]}">\n'
                 f'<link rel="alternate" hreflang="pt-PT" href="{BASE}{PRIV_PATH["pt"]}">\n'
                 f'<link rel="alternate" hreflang="en" href="{BASE}{PRIV_PATH["en"]}">\n'
                 f'<link rel="alternate" hreflang="x-default" href="{BASE}{PRIV_PATH["en"]}">')
    return head_common(c["title"], c["desc"], canonical, T[L]["html_lang"]) + f"""
<body>
<a class="skip" href="#main">{T[L]["skip"]}</a>
<header class="top">
 <div class="wrap">
  <a class="brand" href="{PATH[L]}">{LOGO}<span><b>Cidade Velha</b><small>{c["back"]}</small></span></a>
  <nav class="langs" aria-label="{T[L]["lang_label"]}"><a href="{PRIV_PATH[other]}" hreflang="{T[other]["html_lang"]}" lang="{T[other]["html_lang"]}">{T[other]["label"]}</a></nav>
 </div>
</header>
<main id="main" class="sec">
 <div class="wrap legal">
  <h1>{c["h1"]}</h1>
  <p class="updated">{c["updated"]}</p>
  {tbc(c["body"])}
  <p><a class="btn" href="{PATH[L]}">{c["back"]}</a></p>
 </div>
</main>
{simple_footer()}
</body>
</html>
"""


def not_found_page():
    blocks = "".join(
        f'<div lang="{lang}" class="lost-lang"><h{1 if i == 0 else 2}>{h}</h{1 if i == 0 else 2}><p>{txt}</p><p><a href="{href}">{lbl}</a></p></div>'
        for i, (lang, h, txt, lbl, href) in enumerate(NOT_FOUND))
    return head_common("Página não encontrada · Page not found · Restaurante Cidade Velha, Faro",
                       "Restaurante Cidade Velha, Faro: página não encontrada.", "", "pt-PT",
                       robots='<meta name="robots" content="noindex">\n') + f"""
<body>
<header class="top">
 <div class="wrap">
  <a class="brand" href="/">{LOGO}<span><b>Cidade Velha</b><small>Restaurante · Largo da Sé</small></span></a>
 </div>
</header>
<main id="main" class="sec">
 <div class="wrap legal lost">
  <p class="caps">404</p>
  {blocks}
  <p><a class="btn" href="tel:{TEL}">289 827 145</a></p>
 </div>
</main>
{simple_footer()}
</body>
</html>
"""


def check_csp():
    """CSP has no 'unsafe-inline': every executable inline <script> must be allowed by hash in public/vercel.json,
    and no inline style attributes / <style> blocks may appear."""
    csp = open(os.path.join(PUB, "vercel.json"), encoding="utf-8").read()
    for root, _, files in os.walk(PUB):
        for f in files:
            if not f.endswith(".html"):
                continue
            path = os.path.join(root, f)
            doc = open(path, encoding="utf-8").read()
            for js in re.findall(r"<script>(.*?)</script>", doc, flags=re.S):
                h = base64.b64encode(hashlib.sha256(js.encode()).digest()).decode()
                assert f"'sha256-{h}'" in csp, f"{path}: add 'sha256-{h}' to script-src in vercel.json"
            assert not re.search(r"\sstyle=|<style", doc), f"{path}: inline style is blocked by the CSP"
            assert not re.search(r"\son[a-z]+=", doc), f"{path}: inline event handler is blocked by the CSP"


def main():
    for L in LANGS:
        d = PUB if L == "pt" else os.path.join(PUB, L)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(L))
    for L in ("pt", "en"):
        d = os.path.join(PUB, PRIV_PATH[L].strip("/"))
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(privacy_page(L))
    open(os.path.join(PUB, "404.html"), "w", encoding="utf-8").write(not_found_page())
    open(os.path.join(PUB, "assets", "favicon.svg"), "w").write(FAVICON)
    urls = []
    for L in LANGS:
        links = "".join(f'<xhtml:link rel="alternate" hreflang="{T[x]["html_lang"]}" href="{BASE}{PATH[x]}"/>' for x in LANGS)
        links += f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/en/"/>'
        urls.append(f"<url><loc>{BASE}{PATH[L]}</loc><lastmod>2026-10-09</lastmod>{links}</url>")
    plinks = (f'<xhtml:link rel="alternate" hreflang="pt-PT" href="{BASE}{PRIV_PATH["pt"]}"/>'
              f'<xhtml:link rel="alternate" hreflang="en" href="{BASE}{PRIV_PATH["en"]}"/>'
              f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{PRIV_PATH["en"]}"/>')
    for L in ("pt", "en"):
        urls.append(f"<url><loc>{BASE}{PRIV_PATH[L]}</loc><lastmod>2026-10-09</lastmod>{plinks}</url>")
    open(os.path.join(PUB, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(urls) + "\n</urlset>\n")
    check_csp()
    print("ok")


if __name__ == "__main__":
    main()
