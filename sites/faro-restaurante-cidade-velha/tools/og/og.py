"""Writes og.html (1200x630 share card) and icon.html; render.mjs screenshots them to public/assets."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from art import hero_svg, CAL, WINE, TOWER
og = f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/styles.css"><style>
body{{margin:0;width:1200px;height:630px;background:var(--cal);overflow:hidden;display:grid;grid-template-columns:1fr 360px;gap:60px;padding:0 70px;box-sizing:border-box;align-items:center}}
h1{{font:500 104px/.9 var(--serif);font-variation-settings:"opsz" 30;margin:26px 0 26px;letter-spacing:-.02em}} h1 em{{color:var(--tinto);display:block}}
p{{margin:0;font:400 26px/1.35 var(--sans);color:var(--tinta-2)}} .c{{color:var(--ocre);margin-top:30px}}
.a svg{{width:360px;height:auto;display:block}}
</style></head><body><div><p class="caps c" style="font-size:18px">R. Domingos Guieiro 19 · Largo da Sé · Faro</p>
<h1>Cidade Velha <em>aos pés da Sé.</em></h1><p>Cozinha portuguesa e algarvia na Vila Adentro.<br>Seg–Sáb 11:00–22:00 · 289 827 145</p></div><div class="a">{hero_svg("", "og")}</div></body></html>'''
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "og.html"), "w").write(og)
icon = f'''<!doctype html><html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="512" height="512"><rect width="64" height="64" fill="{CAL}"/><rect x="4.5" y="4.5" width="55" height="55" fill="none" stroke="{WINE}" stroke-width="1.5"/><g transform="translate(18.5 9) scale(.56)" fill="{WINE}">{TOWER}</g></svg></body></html>'''
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.html"), "w").write(icon)
