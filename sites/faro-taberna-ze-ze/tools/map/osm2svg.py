"""Draw the streets around Taberna Zé-Zé from an OpenStreetMap JSON extract into an inline SVG.
Usage: python3 osm2svg.py osm.json out.svg   (data © OpenStreetMap contributors, ODbL)
Extract: https://api.openstreetmap.org/api/0.6/map.json?bbox=-7.9400,37.0172,-7.9280,37.0240"""
import json, math, sys

LAT0, LON0 = 37.020463, -7.9338388      # pin from the restaurant's own DISH/Makro page (matches Google)
W, H = 960, 720
SCALE = 2.1                              # px per metre
CX, CY = W * 0.46, H * 0.52

d = json.load(open(sys.argv[1]))
nodes = {e['id']: (e['lat'], e['lon']) for e in d['elements'] if e['type'] == 'node'}
mx = 111320 * math.cos(math.radians(LAT0))
def xy(lat, lon):
    return (CX + (lon - LON0) * mx * SCALE, CY - (lat - LAT0) * 110540 * SCALE)

def inview(pts, m=60):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return not (max(xs) < -m or min(xs) > W + m or max(ys) < -m or min(ys) > H + m)

def path(ids, close=False):
    pts = [xy(*nodes[i]) for i in ids if i in nodes]
    if len(pts) < 2 or not inview(pts): return ''
    return 'M' + 'L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + ('Z' if close else '')

ROAD = {'primary': 'r1', 'secondary': 'r1', 'tertiary': 'r2', 'unclassified': 'r3', 'residential': 'r3',
        'living_street': 'r3', 'pedestrian': 'r4', 'service': 'r4', 'footway': 'r5'}
groups = {k: [] for k in ['b', 'church', 'green', 'r1', 'r2', 'r3', 'r4', 'r5']}
labels, centroids = {}, {}
for e in d['elements']:
    if e['type'] != 'way': continue
    t = e.get('tags', {})
    if t.get('amenity') == 'place_of_worship' or t.get('building') in ('church', 'chapel'):
        p = path(e['nodes'], True)
        if p:
            groups['church'].append(p)
            pts = [xy(*nodes[i]) for i in e['nodes'] if i in nodes]
            centroids[t.get('name', '')] = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
    elif 'building' in t:
        p = path(e['nodes'], True)
        if p: groups['b'].append(p)
    elif t.get('leisure') in ('garden', 'park') or t.get('landuse') == 'grass':
        p = path(e['nodes'], True)
        if p: groups['green'].append(p)
    elif t.get('highway') in ROAD:
        p = path(e['nodes'], t.get('area') == 'yes')
        if p:
            groups[ROAD[t['highway']]].append(p)
            if t.get('name'): labels.setdefault(t['name'], []).append(e['nodes'])

def longest(name):
    best, bl = None, 0
    for ids in labels.get(name, []):
        pts = [xy(*nodes[i]) for i in ids if i in nodes]
        pts = [p for p in pts if 40 < p[0] < W - 40 and 40 < p[1] < H - 40]
        L = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
        if L > bl: best, bl = pts, L
    if not best: return None, 0
    if best[0][0] > best[-1][0]: best = best[::-1]
    return 'M' + 'L'.join(f'{x:.0f} {y:.0f}' for x, y in best), bl

out = [f'<svg class="map-svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="map-t"><title id="map-t" data-i18n="map.title">Mapa das ruas à volta da Taberna Zé-Zé, na Travessa do Alportel, junto ao Largo do Carmo e à Igreja do Carmo, em Faro</title>']
out.append('<rect class="m-bg" width="100%" height="100%"/>')
out.append('<g class="m-green">' + ''.join(f'<path d="{p}"/>' for p in groups['green']) + '</g>')
for k in ['r1', 'r2', 'r3', 'r4']:
    out.append(f'<path class="m-cas m-{k}" d="' + ''.join(groups[k]) + '"/>')
for k in ['r5', 'r4', 'r3', 'r2', 'r1']:
    out.append(f'<path class="m-{k}" d="' + ''.join(groups[k]) + '"/>')
out.append('<g class="m-b">' + ''.join(f'<path d="{p}"/>' for p in groups['b']) + '</g>')
out.append('<g class="m-church">' + ''.join(f'<path d="{p}"/>' for p in groups['church']) + '</g>')
defs, texts = [], []
for i, (name, label) in enumerate([('Rua do Alportel', 'Rua do Alportel'), 
                                   ('Rua Aboim Ascensão', 'R. Aboim Ascensão'), ('Rua General Teófilo da Trindade', 'R. Gen. Teófilo da Trindade'),
                                   ('Rua Brito Cabreira', 'R. Brito Cabreira'), ('Rua da Freira', 'R. da Freira'),
                                   ('Rua Frei Lourenço Santa Maria', 'R. Frei Lourenço Sta. Maria')]):
    p, L = longest(name)
    if p and L > len(label) * 10:
        defs.append(f'<path id="st{i}" d="{p}"/>')
        texts.append(f'<text class="m-lbl"><textPath href="#st{i}" startOffset="50%" text-anchor="middle">{label}</textPath></text>')
out.append('<defs>' + ''.join(defs) + '</defs>' + ''.join(texts))
if 'Igreja do Carmo' in centroids:
    x, y = centroids['Igreja do Carmo']
    out.append(f'<text class="m-poi" x="{x:.0f}" y="{y + 50:.0f}" text-anchor="middle"><tspan x="{x:.0f}">Igreja do Carmo</tspan><tspan class="m-poi-sub" x="{x:.0f}" dy="18">e Capela dos Ossos</tspan></text>')
sp = [xy(*nodes[i]) for ids in labels.get('Praça Silva Porto', []) for i in ids if i in nodes]
if sp:
    out.append(f'<text class="m-poi" x="{sum(p[0] for p in sp)/len(sp):.0f}" y="{sum(p[1] for p in sp)/len(sp):.0f}" text-anchor="middle">Pç. Silva Porto</text>')
out.append(f'<g class="m-pin" transform="translate({CX:.0f} {CY:.0f})"><circle class="m-pulse" r="22"/><circle r="11"/><text x="0" y="-46" text-anchor="middle">Taberna Zé-Zé</text><text class="m-pin-sub" x="0" y="-26" text-anchor="middle">Tv. do Alportel 15</text></g>')
out.append(f'<text class="m-attr" x="{W - 14}" y="{H - 14}" text-anchor="end">© OpenStreetMap</text></svg>')
svg = ''.join(out)
open(sys.argv[2], 'w').write(svg)
print(len(svg), {k: len(v) for k, v in groups.items()}, list(centroids))
