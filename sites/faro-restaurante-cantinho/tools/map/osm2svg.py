"""Draw Vila Adentro (Faro old town) around the Arco do Repouso as a small, hand-set SVG.

Usage:  python3 osm2svg.py osm-vila-adentro.json map.svg
Data:   © OpenStreetMap contributors, ODbL.  Extract:
        https://api.openstreetmap.org/api/0.6/map.json?bbox=-7.9380,37.0105,-7.9290,37.0170
The output is pasted (by tools/build.py) into the #onde section of the page.
"""
import json, math, sys

LAT0, LON0 = 37.01372, -7.93380      # view centre (between Sé and Arco do Repouso)
PIN = (37.0134441, -7.9332883)        # OSM node 4832258784 "Cantinho"
W, H = 1000, 760
SCALE = 1.95                          # px per metre
CX, CY = W / 2, H / 2

d = json.load(open(sys.argv[1]))
E = {(e['type'], e['id']): e for e in d['elements']}
nodes = {e['id']: (e['lat'], e['lon']) for e in d['elements'] if e['type'] == 'node'}
mx = 111320 * math.cos(math.radians(LAT0))


def xy(lat, lon):
    return (CX + (lon - LON0) * mx * SCALE, CY - (lat - LAT0) * 110540 * SCALE)


def path(ids, close=False):
    pts = [xy(*nodes[i]) for i in ids if i in nodes]
    if len(pts) < 2:
        return ''
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    if max(xs) < -60 or min(xs) > W + 60 or max(ys) < -60 or min(ys) > H + 60:
        return ''
    s = 'M' + 'L'.join(f'{x:.0f} {y:.0f}' for x, y in pts)
    return s + ('Z' if close else '')


ROAD = {'primary': 'r1', 'secondary': 'r1', 'tertiary': 'r1', 'tertiary_link': 'r1',
        'residential': 'r2', 'living_street': 'r2', 'unclassified': 'r2',
        'pedestrian': 'r3', 'service': 'r3', 'footway': 'r4', 'steps': 'r4', 'path': 'r4'}
G = {k: [] for k in ['b', 'g', 'r1', 'r2', 'r3', 'r4', 'wall', 'coast', 'rail', 'park', 'church']}
for e in d['elements']:
    if e['type'] != 'way':
        continue
    t = e.get('tags', {})
    if t.get('barrier') == 'city_wall':
        p = path(e['nodes'], e['nodes'][0] == e['nodes'][-1]); p and G['wall'].append(p)
    elif t.get('building') == 'cathedral' or t.get('historic') == 'tower':
        p = path(e['nodes'], True); p and G['church'].append(p)
    elif 'building' in t:
        p = path(e['nodes'], True); p and G['b'].append(p)
    elif t.get('highway') in ROAD:
        p = path(e['nodes']); p and G[ROAD[t['highway']]].append(p)
    elif t.get('natural') == 'coastline':
        p = path(e['nodes']); p and G['coast'].append(p)
    elif t.get('railway') == 'rail':
        p = path(e['nodes']); p and G['rail'].append(p)
    elif t.get('amenity') == 'parking' and e['id'] == 90463207:
        p = path(e['nodes'], True); p and G['park'].append(p)
    elif t.get('leisure') in ('garden', 'park') or t.get('landuse') in ('grass', 'village_green'):
        p = path(e['nodes'], True); p and G['g'].append(p)


def label(text, lat, lon, cls, rot=0, anchor='middle'):
    x, y = xy(lat, lon)
    r = f' transform="rotate({rot} {x:.0f} {y:.0f})"' if rot else ''
    return f'<text class="{cls}" x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}"{r}>{text}</text>'


px, py = xy(*PIN)
ax, ay = xy(37.0135507, -7.9330258)       # Arco do Repouso outer ring
vx, vy = xy(37.01465, -7.93485)           # Arco da Vila
sx, sy = xy(37.01329, -7.93494)           # Sé tower
lsx, lsy = xy(37.01230, -7.93236)         # Largo de São Francisco (parking polygon centroid)

out = [f'<svg class="map-svg" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="map-t map-d">',
       '<title id="map-t">{{ Mapa da Vila Adentro, Faro || Map of Faro old town }}</title>',
       '<desc id="map-d">{{ O Cantinho fica na Rua do Repouso, n.º 6, junto ao Arco do Repouso, na muralha a nascente da Vila Adentro. A Sé e o Arco da Vila ficam a poucos minutos a pé; o Largo de São Francisco fica do outro lado do arco. || Cantinho is at Rua do Repouso 6, by the Arco do Repouso gate on the east side of the old town wall. The cathedral and the Arco da Vila are a few minutes on foot; Largo de São Francisco is just outside the arch. }}</desc>',
       '<defs><pattern id="hatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><line x1="0" y1="0" x2="0" y2="9" class="hatch"/></pattern></defs>',
       f'<rect class="land" x="0" y="0" width="{W}" height="{H}"/>']
# land is the area NE of the coastline: we fake it by a light paper rect and let the coastline line read as the edge
for cp in G['coast']:
    pts = cp[1:].split('L')
    x0, y0 = map(float, pts[0].split()); x1, y1 = map(float, pts[-1].split())
    out.append(f'<path class="water" fill="url(#hatch)" d="{cp}L-80 {max(y1, y0, H)+80}L-80 -80L{x0:.0f} -80Z"/>')
out.append(f'<g class="g">' + ''.join(f'<path d="{p}"/>' for p in G['g']) + '</g>')
out.append(f'<g class="park">' + ''.join(f'<path d="{p}"/>' for p in G['park']) + '</g>')
for k in ['r1', 'r2', 'r3', 'r4']:
    out.append(f'<g class="{k}">' + ''.join(f'<path d="{p}"/>' for p in G[k]) + '</g>')
out.append('<g class="rail">' + ''.join(f'<path d="{p}"/>' for p in G['rail']) + '</g>')
out.append('<g class="b">' + ''.join(f'<path d="{p}"/>' for p in G['b']) + '</g>')
out.append('<g class="church">' + ''.join(f'<path d="{p}"/>' for p in G['church']) + '</g>')
out.append('<g class="coast">' + ''.join(f'<path d="{p}"/>' for p in G['coast']) + '</g>')
out.append('<g class="wall">' + ''.join(f'<path pathLength="1" d="{p}"/>' for p in G['wall']) + '</g>')
out.append('<g class="labels" aria-hidden="true">')
out.append(label('VILA ADENTRO', 37.01430, -7.93530, 'l-area'))
out.append(label('Ria Formosa', 37.01180, -7.93700, 'l-water'))
out.append(label('Largo da Sé', 37.01318, -7.93395, 'l-st'))
out.append(label('Largo de São Francisco', 37.01205, -7.93236, 'l-st'))
out.append(label('Sé', 37.01300, -7.93500, 'l-poi'))
out.append(label('Arco da Vila', 37.01495, -7.93485, 'l-poi'))
out.append(label('muralha', 37.01262, -7.93450, 'l-wall', 20))
out.append('</g>')
# markers
out.append(f'<g class="m-gate"><circle cx="{vx:.0f}" cy="{vy:.0f}" r="7"/></g>')
out.append(f'<g class="m-park" aria-hidden="true"><rect x="{lsx-13:.0f}" y="{lsy-40:.0f}" width="26" height="26" rx="4"/><text x="{lsx:.0f}" y="{lsy-21:.0f}" text-anchor="middle">P</text></g>')
out.append(f'<g class="m-arch"><path d="M{ax-11:.0f} {ay+22:.0f}v-14a11 11 0 0 1 22 0v14" /></g>')
out.append(label('Arco do Repouso', 37.01372, -7.93268, 'l-poi l-arch', 0, 'start'))
out.append(f'<g class="pin" transform="translate({px:.0f} {py:.0f})"><circle class="pulse" r="18"/><path d="M0 0c-14-18-22-26-22-38a22 22 0 0 1 44 0c0 12-8 20-22 38z"/><circle cy="-38" r="8" class="pin-dot"/></g>')
out.append(f'<text class="l-pin" x="{px-26:.0f}" y="{py-48:.0f}" text-anchor="end">Cantinho</text>')
out.append(f'<text class="l-pin2" x="{px-26:.0f}" y="{py-26:.0f}" text-anchor="end">R. do Repouso, 6</text>')
out.append('</svg>')
open(sys.argv[2], 'w').write('\n'.join(out))
print('pin', round(px), round(py), 'arch', round(ax), round(ay), 'vila', round(vx), round(vy), 'sé', round(sx), round(sy))
