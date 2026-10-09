"""Build the two static pages (PT at /, EN at /en/) from one template.

    python3 tools/build.py

Template syntax (tools/src/index.html):
    {{ texto em português || English text }}   bilingual copy, kept side by side
    {{name}}                                    variable (see VARS below)
The output in public/ is plain HTML: no build step is needed to deploy.
"""
import json, math, pathlib, random, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'tools' / 'src' / 'index.html'
PRIV = ROOT / 'tools' / 'src' / 'privacidade.html'   # privacy policy: /privacidade/ and /en/privacy/
NOTFOUND = ROOT / 'tools' / 'src' / '404.html'       # one bilingual 404 (Vercel serves /404.html)
MAP = ROOT / 'tools' / 'map' / 'map.svg'
SITE = 'https://cantinho-faro.vercel.app'


# ---------------------------------------------------------------- hero: the arch
def hero_svg():
    rnd = random.Random(1249)              # the year of the legend; deterministic stones
    W, H = 600, 820
    L, R, SPRING, RAD = 160, 440, 400, 205  # opening: x 160..440, springs at y=400
    span = R - L
    apex_y = SPRING - math.sqrt(RAD * RAD - (RAD - span / 2) ** 2)

    def arch_pts(offset=0.0, n=24):
        """points along the pointed arch, pushed outward by `offset`"""
        mid = (L + R) / 2
        cx, cy = L + RAD, SPRING          # centre of the left arc (right arc is its mirror)
        r = RAD + offset
        a0, a1 = math.pi, math.acos((mid - cx) / r)
        left = [(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy - r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
        right = [(2 * mid - x, y) for x, y in reversed(left)]
        return left + right[1:]

    inner = arch_pts(0)
    opening = 'M{:.1f} {}'.format(L, H) + ''.join(f'L{x:.1f} {y:.1f}' for x, y in inner) + f'L{R} {H}Z'

    # ashlar courses
    stones = []
    tones = ['#D6BC97', '#CFB089', '#C8A67D', '#DCC6A4', '#C29E74', '#D2B58E']
    y = 64
    row = 0
    while y < H:
        h = rnd.choice([34, 36, 38, 40])
        x = -rnd.randint(0, 60)
        while x < W:
            w = rnd.randint(52, 118)
            stones.append(f'<rect x="{x+2}" y="{y+2}" width="{w-4}" height="{h-4}" rx="3" fill="{rnd.choice(tones)}"/>')
            x += w
        y += h
        row += 1
    # merlons on top of the wall
    merl = []
    x = 6
    while x < W:
        merl.append(f'<rect x="{x}" y="14" width="44" height="54" rx="3" fill="{rnd.choice(tones)}"/>')
        x += 74
    # voussoirs: wedges between inner and outer arch curves
    outer = arch_pts(58)
    vous = []
    n = len(inner) // 2                      # apex index
    idx = list(range(0, len(inner), 3))
    for a, b in zip(idx, idx[1:]):
        if n - 3 <= a < n + 3:
            continue                          # keystone goes here
        p = [inner[a], inner[b], outer[b], outer[a]]
        vous.append('<path d="M' + 'L'.join(f'{px:.1f} {py:.1f}' for px, py in p) + f'Z" fill="{rnd.choice(tones)}"/>')
    ks = [inner[n - 3], inner[n + 3], (outer[n + 3][0] + 4, outer[n + 3][1] - 14), (outer[n - 3][0] - 4, outer[n - 3][1] - 14)]
    vous.append('<path class="keystone" d="M' + 'L'.join(f'{px:.1f} {py:.1f}' for px, py in ks) + 'Z"/>')

    # stars (only visible at night, controlled by CSS)
    stars = ''.join(f'<circle cx="{rnd.uniform(L+8, R-8):.0f}" cy="{rnd.uniform(apex_y+10, 560):.0f}" r="{rnd.choice([0.9,1.2,1.6])}"/>' for _ in range(46))

    # Vila Adentro rooftops + the Sé bell tower, seen through the arch (free composition)
    roofs = (f'M{L-10} 820V650l40-22 40 22v-30h46v-38l26-18 26 18v58l34-26 38 26v-64h18v-60l22-26 22 26v60h12v84'
             f'l30-20 30 20v-40l26-16 30 16V820Z')
    tower = 'M296 600V452h6v-22h48v22h6v148Zm16-132v-26h10v26Zm18 0v-26h10v26Z M300 430l26-30 26 30Z'
    windows = '<rect class="win" x="236" y="690" width="16" height="24" rx="8"/><rect class="win" x="330" y="676" width="12" height="20" rx="6"/><rect class="win dim" x="388" y="712" width="10" height="16" rx="5"/>'
    stork = '<g class="stork"><path d="M0 0c10-6 22-6 30 0 6-8 18-14 34-12-12 4-20 10-24 16l22 4-24 2c-6 6-14 8-22 6l-14 10 6-12c-6-2-8-8-8-14z"/></g>'

    return f'''<svg class="arch-svg" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false" preserveAspectRatio="xMidYMax slice">
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" class="sky-a"/><stop offset=".7" class="sky-b"/><stop offset="1" class="sky-c"/></linearGradient>
  <radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFB36B" stop-opacity=".9"/><stop offset="1" stop-color="#FFB36B" stop-opacity="0"/></radialGradient>
  <clipPath id="opening"><path d="{opening}"/></clipPath>
  <mask id="wallmask"><rect width="{W}" height="{H}" fill="#fff"/><path d="{opening}" fill="#000"/></mask>
</defs>
<g clip-path="url(#opening)" class="through">
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  <g class="stars">{stars}</g>
  <circle class="orb" cx="380" cy="300" r="20"/>
  {stork}
  <path class="roofs" d="{roofs}"/><path class="roofs tower" d="{tower}"/>
  <ellipse class="lamp" cx="244" cy="702" rx="60" ry="46" fill="url(#glow)"/>
  {windows}
  <path class="reveal" d="{'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in inner)}"/>
</g>
<g class="wall" mask="url(#wallmask)">
  <rect y="60" width="{W}" height="{H}" class="mortar"/>
  {''.join(merl)}
  {''.join(stones)}
  {''.join(vous)}
</g>
<path class="intrados" d="{'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in inner)}"/>
</svg>'''


def render(lang, tpl, mapsvg, path=None):
    i = 0 if lang == 'pt' else 1

    def bi(m):
        parts = m.group(1).split('||')
        return parts[i].strip() if len(parts) == 2 else m.group(0)
    out = re.sub(r'\{\{((?:(?!\}\}).)*?\|\|(?:(?!\}\}).)*?)\}\}', bi, tpl, flags=re.S)
    V = {
        'lang': 'pt-PT' if lang == 'pt' else 'en',
        'root': '/' if lang == 'pt' else '/en/',
        'url': SITE + (path or ('/' if lang == 'pt' else '/en/')),
        'site': SITE,
        'hero_svg': hero_svg(),
        'map_svg': mapsvg,
        'jsonld': jsonld(lang),
    }
    out = out.replace('{{map_svg}}', V['map_svg'])
    for k, v in V.items():
        out = out.replace('{{' + k + '}}', v)
    # second pass for bilingual strings that lived inside the map svg
    out = re.sub(r'\{\{((?:(?!\}\}).)*?\|\|(?:(?!\}\}).)*?)\}\}', bi, out, flags=re.S)
    left = re.findall(r'\{\{[^}]{0,60}', out)
    assert not left, left[:5]
    return out


def jsonld(lang):
    pt = lang == 'pt'
    d = {
        '@context': 'https://schema.org',
        '@type': 'Restaurant',
        '@id': SITE + '/#restaurante',
        'name': 'Cantinho',
        'alternateName': 'Cantinho de Faro',
        'url': SITE + ('/' if pt else '/en/'),
        'inLanguage': 'pt-PT' if pt else 'en',
        'description': ('Tasca de cozinha tradicional portuguesa na cidade velha de Faro, junto ao Arco do Repouso.' if pt
                        else 'Traditional Portuguese cooking in Faro old town, next to the Arco do Repouso gate.'),
        'image': SITE + '/assets/og.jpg',
        'logo': SITE + '/assets/icon-512.png',
        'telephone': '+351911013101',
        'servesCuisine': ['Portuguesa', 'Algarvia'] if pt else ['Portuguese', 'Algarvian'],
        'acceptsReservations': 'True',
        'hasMenu': SITE + ('/#ementa' if pt else '/en/#ementa'),
        'address': {'@type': 'PostalAddress', 'streetAddress': 'Rua do Repouso 6', 'postalCode': '8000-169',
                    'addressLocality': 'Faro', 'addressRegion': 'Faro', 'addressCountry': 'PT'},
        'geo': {'@type': 'GeoCoordinates', 'latitude': 37.0134441, 'longitude': -7.9332883},
        'hasMap': 'https://www.google.com/maps/search/?api=1&query=Cantinho%2C%20R.%20do%20Repouso%206%2C%20Faro',
        'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification',
                                       'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
                                       'opens': '10:30', 'closes': '23:30'}],
        'sameAs': ['https://www.facebook.com/cantinhodefaro', 'https://www.instagram.com/cantinhodefaro/'],
        'containedInPlace': {'@type': 'TouristAttraction', 'name': 'Vila Adentro, Faro'},
    }
    return json.dumps(d, ensure_ascii=False, indent=1)


def main():
    tpl = SRC.read_text()
    mapsvg = MAP.read_text()
    (ROOT / 'public' / 'index.html').write_text(render('pt', tpl, mapsvg))
    (ROOT / 'public' / 'en').mkdir(exist_ok=True)
    (ROOT / 'public' / 'en' / 'index.html').write_text(render('en', tpl, mapsvg))
    priv = PRIV.read_text()
    for lang, path in (('pt', '/privacidade/'), ('en', '/en/privacy/')):
        out = ROOT / 'public' / path.strip('/') / 'index.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(lang, priv, '', path))
    (ROOT / 'public' / '404.html').write_text(NOTFOUND.read_text())
    # CSP has no 'unsafe-inline': every inline <script> must be allowed by hash in public/vercel.json
    import base64, hashlib
    csp = (ROOT / 'public' / 'vercel.json').read_text()
    for page in (ROOT / 'public').rglob('*.html'):
        for js in re.findall(r'<script>(.*?)</script>', page.read_text(), flags=re.S):
            h = base64.b64encode(hashlib.sha256(js.encode()).digest()).decode()
            assert f"'sha256-{h}'" in csp, f'{page}: add sha256-{h} to script-src in vercel.json'
    print('ok')


if __name__ == '__main__':
    main()
