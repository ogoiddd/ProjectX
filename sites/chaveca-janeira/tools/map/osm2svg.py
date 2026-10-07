"""Render the streets around the workshop from an OpenStreetMap JSON extract into a small SVG.
Usage: python3 osm2svg.py osm.json out.svg   (data © OpenStreetMap contributors, ODbL)"""
import json, math, sys

LAT0, LON0 = 37.02378, -7.93935          # workshop (Google Maps pin)
W, H = 960, 640                           # viewBox, 1 unit ≈ 1 m * SCALE
SCALE = 0.95                              # px per metre
CX, CY = W * 0.5, H * 0.5

d = json.load(open(sys.argv[1]))
nodes = {e['id']: (e['lat'], e['lon']) for e in d['elements'] if e['type'] == 'node'}
mx = 111320 * math.cos(math.radians(LAT0))
def xy(lat, lon):
    return (CX + (lon - LON0) * mx * SCALE, CY - (lat - LAT0) * 110540 * SCALE)

def path(ids, close=False):
    pts = [xy(*nodes[i]) for i in ids if i in nodes]
    if len(pts) < 2: return ''
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    if max(xs) < -40 or min(xs) > W + 40 or max(ys) < -40 or min(ys) > H + 40: return ''
    s = 'M' + 'L'.join(f'{x:.0f} {y:.0f}' for x, y in pts)
    return s + ('Z' if close else '')

ROAD = {'primary': 'r1', 'primary_link': 'r1', 'secondary': 'r2', 'tertiary': 'r2', 'unclassified': 'r3', 'residential': 'r3', 'living_street': 'r3', 'service': 'r4', 'pedestrian': 'r4'}
groups = {k: [] for k in ['b', 'r1', 'r2', 'r3', 'r4', 'rail']}
labels = {}
for e in d['elements']:
    if e['type'] != 'way': continue
    t = e.get('tags', {})
    if 'building' in t:
        p = path(e['nodes'], True)
        if p: groups['b'].append(p)
    elif t.get('highway') in ROAD:
        p = path(e['nodes'])
        if p:
            groups[ROAD[t['highway']]].append(p)
            n = t.get('name')
            if n: labels.setdefault(n, []).append(e['nodes'])
    elif t.get('railway') == 'rail':
        p = path(e['nodes'])
        if p: groups['rail'].append(p)

def longest(name):
    best, bl = None, 0
    for ids in labels.get(name, []):
        pts = [xy(*nodes[i]) for i in ids if i in nodes]
        pts = [p for p in pts if 30 < p[0] < W - 30 and 30 < p[1] < H - 30]
        L = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
        if L > bl: best, bl = pts, L
    if not best: return None, 0
    if best[0][0] > best[-1][0]: best = best[::-1]          # read left → right
    return 'M' + 'L'.join(f'{x:.0f} {y:.0f}' for x, y in best), bl

out = [f'<svg class="map-svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="map-t"><title id="map-t">Mapa das ruas à volta da oficina, na Estrada da Senhora da Saúde, perto da Rotunda do Fórum, em Faro</title>']
out.append('<g class="m-b">' + ''.join(f'<path d="{p}"/>' for p in groups['b']) + '</g>')
out.append('<path class="m-rail" d="' + ''.join(groups['rail']) + '"/>')
for k in ['r4', 'r3', 'r2', 'r1']:
    out.append(f'<path class="m-{k}" d="' + ''.join(groups[k]) + '"/>')
defs, texts = [], []
for i, (name, label) in enumerate([('Estrada da Senhora da Saúde', 'Estr. da Sra. da Saúde'), ('Avenida Calouste Gulbenkian', 'Av. Calouste Gulbenkian'), ('Rua Aboim Ascensão', 'R. Aboim Ascensão'), ('Avenida Heróis da Pátria', 'Av. Heróis da Pátria')]):
    p, L = longest(name)
    if p and L > len(label) * 9:
        defs.append(f'<path id="st{i}" d="{p}"/>')
        texts.append(f'<text class="m-lbl{" m-lbl-main" if i == 0 else ""}"><textPath href="#st{i}" startOffset="{"78%" if i == 0 else "50%"}" text-anchor="middle">{label}</textPath></text>')
out.append('<defs>' + ''.join(defs) + '</defs>' + ''.join(texts))
# landmark: the Fórum roundabout (label at its centroid)
rp = [xy(*nodes[i]) for ids in labels.get('Rotunda do Fórum', []) for i in ids if i in nodes]
if rp:
    rx = sum(p[0] for p in rp) / len(rp); ry = sum(p[1] for p in rp) / len(rp)
    out.append(f'<text class="m-lbl m-poi" x="{rx:.0f}" y="{ry + 48:.0f}" text-anchor="middle">Rotunda do Fórum</text>')
# the workshop
out.append(f'<g class="m-pin" transform="translate({CX:.0f} {CY:.0f})"><rect x="-9" y="-9" width="18" height="18"/><text x="16" y="-14">Chaveca &amp; Janeira</text></g>')
out.append(f'<text class="m-attr" x="{W - 12}" y="{H - 12}" text-anchor="end">© OpenStreetMap</text></svg>')
svg = ''.join(out)
open(sys.argv[2], 'w').write(svg)
print(len(svg), {k: len(v) for k, v in groups.items()}, list(labels)[:3])
