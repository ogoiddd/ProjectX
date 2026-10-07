// Mobile audit: tap targets, tiny text, overflow, per-device screenshots.
// Usage: node mobile-audit.mjs <url> <outDir>
import { chromium, devices } from 'playwright';
const [url, out] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--autoplay-policy=no-user-gesture-required', '--proxy-server=' + process.env.HTTPS_PROXY, '--proxy-bypass-list=127.0.0.1;localhost'] });
const DEV = {
  'se-375': devices['iPhone SE'], 'android-360': { ...devices['Galaxy S9+'], viewport: { width: 360, height: 740 } },
  'iphone13-390': devices['iPhone 13'], 'pixel7-412': devices['Pixel 7'],
  'landscape-844': devices['iPhone 13 landscape'], 'ipad-810': devices['iPad (gen 7)'],
};
for (const [name, d] of Object.entries(DEV)) {
  const ctx = await b.newContext({ ...d, locale: 'pt-PT' }); const p = await ctx.newPage();
  await p.goto(url, { waitUntil: 'load' }); await p.waitForTimeout(1500);
  await p.screenshot({ path: `${out}/${name}-0.png` });
  const r = await p.evaluate(() => {
    const vis = e => { const s = getComputedStyle(e), b = e.getBoundingClientRect(); return s.visibility !== 'hidden' && s.display !== 'none' && b.width > 0 && b.height > 0 && !e.closest('[aria-hidden="true"]'); };
    const small = [...document.querySelectorAll('a, button')].filter(vis).map(e => { const b = e.getBoundingClientRect(); return { t: (e.innerText || e.getAttribute('aria-label') || '').trim().slice(0, 40), w: Math.round(b.width), h: Math.round(b.height) }; }).filter(x => x.h < 44 || x.w < 44);
    const tiny = []; const seen = new Set();
    document.querySelectorAll('body *').forEach(e => { if (!vis(e) || e.closest('svg')) return; const txt = [...e.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).map(n => n.textContent.trim()).join(' '); if (!txt) return; const fs = parseFloat(getComputedStyle(e).fontSize); if (fs < 12 && !seen.has(txt)) { seen.add(txt); tiny.push(fs + 'px: ' + txt.slice(0, 40)); } });
    const wide = [...document.querySelectorAll('body *')].filter(e => { const b = e.getBoundingClientRect(); return vis(e) && b.right > innerWidth + 1 && !e.closest('.sidewall-wrap,.fascia,.hero-media,.track'); }).map(e => e.className || e.tagName).slice(0, 8);
    const mapLbl = document.querySelector('.m-lbl'); const mapPx = mapLbl ? Math.round(mapLbl.getBoundingClientRect().height) : null;
    return { vw: innerWidth, vh: innerHeight, docW: document.documentElement.scrollWidth, small, tiny, wide, mapLabelPx: mapPx, nav: !!document.querySelector('.nav a') && getComputedStyle(document.querySelector('.nav')).display !== 'none' };
  });
  console.log('==', name, JSON.stringify(r));
  let i = 1; for (const sel of ['.about', '#servicos', '.band', '#opinioes', '#horario', '#local', '#contacto']) { await p.evaluate(s => { const e = document.querySelector(s); scrollTo(0, e.getBoundingClientRect().top + scrollY - 60); }, sel); await p.waitForTimeout(500); await p.screenshot({ path: `${out}/${name}-${i++}.png` }); }
  await ctx.close();
}
await b.close();
