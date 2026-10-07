"""Bundle the site into one self-contained HTML file (fonts, images and a light video inlined) for phone previews.
Usage: python3 build-preview.py <publicDir> <portrait.mp4> <landscape.mp4> <out.html>"""
import base64, re, sys
P, PMP4, LMP4, OUT = sys.argv[1:5]
def uri(path):
    mime = {'webp': 'image/webp', 'svg': 'image/svg+xml', 'woff2': 'font/woff2', 'mp4': 'video/mp4'}[path.rsplit('.', 1)[1]]
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()
html, css, js = (open(f'{P}/{f}').read() for f in ('index.html', 'styles.css', 'app.js'))
for f in ('archivo-latin', 'jetbrains-mono-latin'):
    css = css.replace(f'url(/fonts/{f}.woff2)', 'url(' + uri(f'{P}/fonts/{f}.woff2') + ')')
js = js.replace("return base + ext;", "return base.startsWith('data:') ? base : base + ext;")
blob = "if (src.startsWith('data:')) { fetch(src).then(r => r.blob()).then(bl => { video.src = URL.createObjectURL(bl); video.muted = true; video.play().catch(() => {}); }); return; }\n      "
js = js.replace("      video.src = src;\n    }", "      " + blob + "video.src = src;\n    }")
js = js.replace("const src = pickSource(); video.dataset.current = src; video.src = src; video.muted = true;",
                "const src = pickSource(); video.dataset.current = src; video.muted = true;\n    " + blob + "video.src = src;")
html = re.sub(r'<link rel="(preload|manifest|apple-touch-icon|canonical)"[^>]*>\n?', '', html)
html = re.sub(r'<link rel="icon"[^>]*png"[^>]*>\n?', '', html)
html = html.replace('<link rel="stylesheet" href="/styles.css">', '<style>' + css + '</style>').replace('<script src="/app.js" defer></script>', '<script>' + js + '</script>')
html = re.sub(r'\s(srcset|sizes)="[^"]*"', '', html)
small = {'facade-1600.webp': 'facade-900.webp', 'workshop-1600.webp': 'workshop-900.webp', 'align-911-1100.webp': 'align-911-700.webp', 'hero-poster-1920.webp': 'hero-poster-1280.webp'}
html = re.sub(r'="/assets/([\w.-]+\.(?:webp|svg))"', lambda m: '="' + uri(f'{P}/assets/{small.get(m.group(1), m.group(1))}') + '"', html)
html = html.replace('<source media="(orientation: portrait)">', '<source media="(orientation: portrait)" srcset="' + uri(f'{P}/assets/hero-poster-portrait.webp') + '">').replace('<source>', '')
html = html.replace('data-landscape="/assets/hero-1080" data-landscape-sm="/assets/hero-720" data-portrait="/assets/hero-portrait"',
                    f'data-landscape="{uri(LMP4)}" data-landscape-sm="{uri(LMP4)}" data-portrait="{uri(PMP4)}"')
html = html.replace("'/assets/hero-poster-portrait.webp'", "'" + uri(f'{P}/assets/hero-poster-portrait.webp') + "'").replace("'/assets/hero-poster-1920.webp'", "'" + uri(f'{P}/assets/hero-poster-1280.webp') + "'")
html = html.replace('href="/legal"', 'href="https://chaveca-janeira-faro.vercel.app/legal"').replace('href="/contacto.vcf"', 'href="data:text/vcard;charset=utf-8;base64,' + base64.b64encode(open(f'{P}/contacto.vcf', 'rb').read()).decode() + '"')
assert 'createObjectURL' in html
open(OUT, 'w').write(html)
print(len(html) // 1024, 'KB; unresolved:', re.findall(r'["(\']/(?:assets|fonts)/[^"\')]+', html)[:3])
