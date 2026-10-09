#!/usr/bin/env python3
"""Draw the Arealauto location map (ink-on-sand style) from OpenStreetMap tiles.

Data (c) OpenStreetMap contributors, ODbL. Usage:
  python3 -I osm2svg.py out.svg t1.json t2.json ...
Tiles come from https://api.openstreetmap.org/api/0.6/map.json?bbox=... (see README).
"""
import json, math, sys

W, H = 800, 640
LON0, LON1 = -7.9440, -7.8860
LAT0, LAT1 = 37.0090, 37.0500
PIN = (37.040886, -7.896193)  # Google Maps pin "Arealauto" (place id ChIJkREmmcmsGg0R28XofdkM01o)
KX = W / (LON1 - LON0)
KY = H / (LAT1 - LAT0)


def xy(lat, lon):
    return ((lon - LON0) * KX, (LAT1 - lat) * KY)


def simplify(pts, eps=1.2):
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    norm = math.hypot(dx, dy) or 1e-9
    dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        x0, y0 = pts[i]
        d = abs(dy * x0 - dx * y0 + x2 * y1 - y2 * x1) / norm
        if d > dmax:
            dmax, idx = d, i
    if dmax > eps:
        return simplify(pts[: idx + 1], eps)[:-1] + simplify(pts[idx:], eps)
    return [pts[0], pts[-1]]


def path(pts):
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def inside(p, m=40):
    return -m <= p[0] <= W + m and -m <= p[1] <= H + m


nodes, ways = {}, {}
for f in sys.argv[2:]:
    for e in json.load(open(f))["elements"]:
        if e["type"] == "node":
            nodes[e["id"]] = (e["lat"], e["lon"])
        elif e["type"] == "way" and e.get("tags"):
            ways[e["id"]] = e

CLASS = {
    "primary": "r1", "primary_link": "r1", "trunk": "r1", "trunk_link": "r1",
    "secondary": "r2", "secondary_link": "r2", "tertiary": "r2", "tertiary_link": "r2",
    "unclassified": "r3", "residential": "r4", "living_street": "r4",
}
groups = {"r1": [], "r2": [], "r3": [], "r4": [], "rail": []}
for w in ways.values():
    t = w["tags"]
    cls = CLASS.get(t.get("highway"))
    if t.get("railway") == "rail":
        cls = "rail"
    if not cls:
        continue
    pts = [xy(*nodes[n]) for n in w["nodes"] if n in nodes]
    if len(pts) < 2 or not any(inside(p) for p in pts):
        continue
    groups[cls].append(path(simplify(pts, 0.9 if cls in ("r1", "r2") else 1.4)))

px, py = xy(*PIN)
faro = xy(37.0162944, -7.935182)
out = [
    f'<svg class="map-svg" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
    'aria-labelledby="map-t map-d" preserveAspectRatio="xMidYMid slice">',
    '<title id="map-t">Mapa: do centro de Faro ao Areal Gordo</title>',
    '<desc id="map-d">A oficina fica no Sítio do Brejo, Areal Gordo, a nordeste do centro de Faro, '
    'entre a EN 2 e a EN 125.</desc>',
]
for cls in ("r4", "r3", "rail", "r2", "r1"):
    if groups[cls]:
        pl = ' pathLength="1000"' if cls in ("r1", "r2") else ""
        out.append(f'<path class="m-{cls}"{pl} d="{"".join(groups[cls])}"/>')
labels = [
    (faro, "FARO · CENTRO", "m-lbl m-lbl--big"),
    (xy(37.034625, -7.9026032), "Areal Gordo", "m-lbl"),
    (xy(37.0410139, -7.8937948), "Brejo", "m-lbl"),
    (xy(37.0435102, -7.8950232), "Pão Branco", "m-lbl m-lbl--s"),
    (xy(37.0272078, -7.9081607), "Rio Seco", "m-lbl m-lbl--s"),
    (xy(37.043446, -7.9301763), "Campina", "m-lbl m-lbl--s"),
]
labels += [
    ((560, 352), "EN 125", "m-ref"),
    ((150, 236), "EN 2", "m-ref"),
]
for (x, y), txt, cls in labels:
    out.append(f'<text class="{cls}" x="{x:.0f}" y="{y:.0f}">{txt}</text>')
out.append(f'<circle class="m-faro" cx="{faro[0]:.1f}" cy="{faro[1]:.1f}" r="5"/>')
out.append(
    f'<g class="m-pin" transform="translate({px:.1f} {py:.1f})">'
    '<circle class="m-pin-ring" r="26"/><circle class="m-pin-dot" r="8"/>'
    '<text class="m-pin-lbl" x="-14" y="-38" text-anchor="end">AREALAUTO</text>'
    '<path class="m-pin-lead" d="M-10 -32 L-4 -12"/></g>'
)
out.append('<text class="m-attr" x="790" y="630" text-anchor="end">© OpenStreetMap contributors</text>')
out.append("</svg>")
svg = "\n".join(out)
if sys.argv[1].endswith(".html"):  # inject into the page placeholder
    page = open(sys.argv[1]).read()
    import re
    page = re.sub(r"<!--MAP-->|<svg class=\"map-svg\".*?</svg>", lambda m: svg, page, count=1, flags=re.S)
    open(sys.argv[1], "w").write(page)
else:
    open(sys.argv[1], "w").write(svg)
print("pin", round(px), round(py), "faro", [round(v) for v in faro], "bytes", sum(map(len, out)))
