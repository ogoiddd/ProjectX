# Chaveca & Janeira — Faro

One-page site for **Euromaster Chaveca & Janeira Faro** (Estr. da Sra. da Saúde 58, 8000-500 Faro · +351 289 887 200).

- `public/` — the deployable static site (no build step): `index.html`, `styles.css`, `app.js`, `assets/`.
- `tools/hero/` — the hero film. `scene.html` is a three.js scene (alloy wheel, sidewall lettering, sunlit roller door); `render.mjs` renders it frame-by-frame in headless Chromium at 2560×1440 / 1440×2560; `encode.sh` turns the frames into the web MP4s and poster frames. Every motion in the scene is periodic over 10 s, so the clip loops without a seam.
- `tools/og/` — OG image and icon renders.
- `tools/qa/` — Playwright screenshot / check scripts.

## Facts used (sources)

All business facts come from the Google Maps listing and the euromaster.pt centre page: address, phone, hours (Mon–Fri 09:00–19:00, Sat 09:00–13:00, Sun closed), rating (4.5 · 407 reviews at time of build), wheelchair-accessible entrance/parking, the 13 listed services, the Master Garantia wording, and the three reviews (quoted verbatim). No prices, awards or history were added.

## Re-render the hero

```bash
cd tools/hero && npm i
node render.mjs /tmp/fh 240 hero 2560 1440 0 24 10
node render.mjs /tmp/fp 240 portrait 1440 2560 0 24 10
./encode.sh /tmp/fh /tmp/fp ../../public/assets
```

## Location map

`tools/map/osm2svg.py` draws the street map from an OpenStreetMap extract (© OpenStreetMap contributors, ODbL):

```bash
curl -o osm.json "https://api.openstreetmap.org/api/0.6/map.json?bbox=-7.9465,37.0190,-7.9322,37.0286"
python3 tools/map/osm2svg.py osm.json map.svg   # paste the <svg> into the #local map card
```
