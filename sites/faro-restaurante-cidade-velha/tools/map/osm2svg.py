"""Draw Vila Adentro (Faro old town) around Restaurante Cidade Velha from an OpenStreetMap extract.
Usage: python3 osm2svg.py osm.json out.svg      (data (c) OpenStreetMap contributors, ODbL)

Outputs an <svg> fragment with: buildings, streets, the old town walls, the Sé (highlighted),
the two gates (Arco da Vila, Arco do Repouso), and the shortest walking routes from each
gate to the restaurant (computed on the OSM street graph). Prints route lengths in metres.
Labels are emitted with data-i18n keys so the page can translate them.
"""
import heapq, json, math, sys

REST = (37.0135551, -7.9345962)            # OSM node "Restaurante Cidade Velha"
LAT0, LON0 = 37.01385, -7.93410            # view centre
W, H = 960, 720
SCALE = 2.05                               # px per metre

d = json.load(open(sys.argv[1]))
nodes = {e['id']: (e['lat'], e['lon']) for e in d['elements'] if e['type'] == 'node'}
ways = {e['id']: e for e in d['elements'] if e['type'] == 'way'}
mx = 111320 * math.cos(math.radians(LAT0))
def xy(lat, lon):
    return (W / 2 + (lon - LON0) * mx * SCALE, H / 2 - (lat - LAT0) * 110540 * SCALE)
def metres(a, b):
    return math.hypot((a[1] - b[1]) * mx, (a[0] - b[0]) * 110540)

def path(ids, close=False):
    pts = [xy(*nodes[i]) for i in ids if i in nodes]
    if len(pts) < 2: return ''
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    if max(xs) < -60 or min(xs) > W + 60 or max(ys) < -60 or min(ys) > H + 60: return ''
    return 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + ('Z' if close else '')

WALK = {'primary', 'secondary', 'tertiary', 'unclassified', 'residential', 'living_street', 'service', 'pedestrian', 'footway', 'steps', 'path'}
groups = {k: [] for k in ['b', 'major', 'minor', 'foot', 'wall', 'se', 'civic']}
graph = {}
for e in ways.values():
    t = e.get('tags', {})
    ids = e['nodes']
    if t.get('barrier') == 'city_wall' or t.get('historic') == 'citywalls':
        p = path(ids); p and groups['wall'].append(p)
    if t.get('name') == 'Igreja da Sé' and 'building' in t or t.get('amenity') == 'place_of_worship' and t.get('building') == 'cathedral':
        p = path(ids, True); p and groups['se'].append(p); continue
    if t.get('name') in ('Paço Episcopal', 'Câmara Municipal de Faro', 'Igreja da Sé tower', 'Museu e Igreja da Misericórdia'):
        p = path(ids, True); p and groups['civic'].append(p); continue
    if 'building' in t:
        p = path(ids, True); p and groups['b'].append(p)
    hw = t.get('highway')
    if hw in WALK:
        p = path(ids)
        if p:
            groups['major' if hw in ('primary', 'secondary', 'tertiary') else 'foot' if hw in ('footway', 'steps', 'path') else 'minor'].append(p)
        for a, b in zip(ids, ids[1:]):
            if a in nodes and b in nodes:
                w = metres(nodes[a], nodes[b])
                graph.setdefault(a, []).append((b, w)); graph.setdefault(b, []).append((a, w))
# relation-based buildings (multipolygons), e.g. Arco do Repouso
for e in d['elements']:
    if e['type'] == 'relation' and 'building' in e.get('tags', {}):
        for m in e['members']:
            if m['type'] == 'way' and m['ref'] in ways and m['role'] == 'outer':
                p = path(ways[m['ref']]['nodes'], True); p and groups['civic'].append(p)

def nearest(pt):
    return min(graph, key=lambda n: metres(nodes[n], pt))
def route(src, dst):
    s, t = nearest(src), nearest(dst)
    dist, prev, pq = {s: 0}, {}, [(0, s)]
    while pq:
        dd, u = heapq.heappop(pq)
        if u == t: break
        if dd > dist[u]: continue
        for v, w in graph[u]:
            if dd + w < dist.get(v, 1e18):
                dist[v] = dd + w; prev[v] = u; heapq.heappush(pq, (dd + w, v))
    seq = [t]
    while seq[-1] != s: seq.append(prev[seq[-1]])
    seq.reverse()
    pts = [xy(*nodes[i]) for i in seq] + [xy(*dst)]
    return 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts), dist[t] + metres(nodes[t], dst)

ARCO_VILA = (37.014800, -7.934895)     # outer mouth of the Arco da Vila passage
ARCO_REP = (37.013470, -7.933010)      # outer mouth of the Arco do Repouso passage
r1, l1 = route(ARCO_VILA, REST)
r2, l2 = route(ARCO_REP, REST)
print(f'Arco da Vila -> restaurante: {l1:.0f} m ; Arco do Repouso -> restaurante: {l2:.0f} m', file=sys.stderr)

def centroid(name):
    for e in ways.values():
        if e.get('tags', {}).get('name') == name and 'building' in e.get('tags', {}):
            pts = [xy(*nodes[i]) for i in e['nodes'] if i in nodes]
            return sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)

o = [f'<svg class="map-svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="map-title map-desc" preserveAspectRatio="xMidYMid slice">',
     '<title id="map-title" data-i18n="map.title">Mapa da Vila Adentro com o caminho até ao Restaurante Cidade Velha</title>',
     f'<desc id="map-desc" data-i18n="map.desc">Do Arco da Vila são cerca de {round(l1, -1):.0f} metros a pé pela Rua do Município até ao Largo da Sé.</desc>']
o.append('<g class="m-b">' + ''.join(f'<path d="{p}"/>' for p in groups['b']) + '</g>')
o.append('<g class="m-civic">' + ''.join(f'<path d="{p}"/>' for p in groups['civic']) + '</g>')
o.append('<path class="m-major" d="' + ''.join(groups['major']) + '"/>')
o.append('<path class="m-minor" d="' + ''.join(groups['minor']) + '"/>')
o.append('<path class="m-foot" d="' + ''.join(groups['foot']) + '"/>')
o.append('<path class="m-wall" d="' + ''.join(groups['wall']) + '"/>')
o.append('<g class="m-se">' + ''.join(f'<path d="{p}"/>' for p in groups['se']) + '</g>')
o.append(f'<path class="m-route m-route-2" pathLength="1" d="{r2}"/>')
o.append(f'<path class="m-route m-route-1" pathLength="1" d="{r1}"/>')
sx, sy = centroid('Igreja da Sé')
o.append(f'<text class="m-lbl m-lbl-se" x="{sx:.0f}" y="{sy + 6:.0f}" text-anchor="middle" data-i18n="map.se">Sé</text>')
lp = [xy(*nodes[i]) for e in ways.values() if e.get('tags', {}).get('name') == 'Largo da Sé' and 'highway' in e.get('tags', {}) for i in e['nodes'] if i in nodes]
lx = sum(p[0] for p in lp) / len(lp); ly = sum(p[1] for p in lp) / len(lp)
o.append(f'<text class="m-lbl m-lbl-largo" x="{lx - 34:.0f}" y="{ly + 4:.0f}" text-anchor="end" data-i18n="map.largo">Largo da Sé</text>')
# street names along the walking routes
def longest(name):
    best, bl = None, 0
    for e in ways.values():
        t = e.get('tags', {})
        if t.get('name') != name or 'highway' not in t: continue
        pts = [xy(*nodes[i]) for i in e['nodes'] if i in nodes]
        L = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
        if L > bl: best, bl = pts, L
    if best and best[0][0] > best[-1][0]: best = best[::-1]
    return best, bl
defs, texts = [], []
def leg_to_rest(name):
    """The way of `name` that ends at the restaurant, as a straight, left-to-right baseline (reads on the route)."""
    rx_, ry_ = xy(*REST)
    cands = [e for e in ways.values() if e.get('tags', {}).get('name') == name and 'highway' in e.get('tags', {})
             and sum(math.dist(xy(*nodes[a]), xy(*nodes[b])) for a, b in zip(e['nodes'], e['nodes'][1:]) if a in nodes and b in nodes) > 60]
    near = [e for e in cands if min(math.dist(xy(*nodes[i]), (rx_, ry_)) for i in e['nodes'] if i in nodes) < 40]
    best = max(near, key=lambda e: math.dist(xy(*nodes[e['nodes'][0]]), xy(*nodes[e['nodes'][-1]])))
    pts = [xy(*nodes[i]) for i in best['nodes'] if i in nodes]
    pts = [pts[0], pts[-1]] if pts[0][0] < pts[-1][0] else [pts[-1], pts[0]]
    return pts, math.dist(*pts)
for i, (name, label) in enumerate([('Rua do Município', 'R. do Município'), ('Rua Domingos Guieiro', 'R. Domingos Guieiro'), ('Rua do Repouso', 'R. do Repouso')]):
    pts, L = leg_to_rest(name) if name == 'Rua Domingos Guieiro' else longest(name)
    if pts and L > len(label) * 7.5:
        defs.append(f'<path id="st{i}" d="M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + '"/>')
        texts.append(f'<text class="m-st" dy="-7"><textPath href="#st{i}" startOffset="50%" text-anchor="middle">{label}</textPath></text>')
o.append('<defs>' + ''.join(defs) + '</defs>' + ''.join(texts))
ax, ay = xy(*ARCO_VILA)
o.append(f'<g class="m-gate" transform="translate({ax:.0f} {ay:.0f})"><circle r="7"/><text x="14" y="-10" data-i18n="map.arcovila">Arco da Vila</text></g>')
bx, by = xy(*ARCO_REP)
o.append(f'<g class="m-gate m-gate-2" transform="translate({bx:.0f} {by:.0f})"><circle r="7"/><text x="12" y="26" data-i18n="map.arcorepouso">Arco do Repouso</text></g>')
rx, ry = xy(*REST)
o.append(f'<g class="m-pin" transform="translate({rx:.0f} {ry:.0f})"><circle class="m-pin-pulse" r="16"/><circle r="9"/><text x="18" y="5">Cidade Velha</text></g>')
o.append(f'<text class="m-attr" x="{W - 14}" y="{H - 14}" text-anchor="end">© OpenStreetMap</text></svg>')
svg = ''.join(o)
open(sys.argv[2], 'w').write(svg)
print(len(svg), {k: len(v) for k, v in groups.items()}, f'{l1:.0f} {l2:.0f}')
