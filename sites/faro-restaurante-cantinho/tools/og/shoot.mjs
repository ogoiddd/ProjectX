// Renders og.jpg (1200x630) and the PNG icons from the live page's own arch + fonts.
// Usage: node shoot.mjs <public dir> [baseUrl]   (serve public/ on baseUrl first)
import { chromium } from 'playwright';
const pub = process.argv[2]; const base = process.argv[3] || 'http://127.0.0.1:8790';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
await p.goto(base + '/?ceu=dusk', { waitUntil: 'networkidle' });
await p.evaluate(() => {
  const arch = document.querySelector('.hero-arch'); arch.querySelector('figcaption')?.remove();
  document.body.innerHTML = '';
  document.body.style.cssText = 'margin:0;padding:0;background:#1D1916;overflow:hidden';
  const w = document.createElement('div');
  w.style.cssText = 'display:grid;grid-template-columns:1fr 470px;width:1200px;height:630px';
  w.innerHTML = `<div style="padding:70px 0 0 72px;color:#F1E9DC">
    <p style="font:600 22px Newsreader;font-variant-caps:all-small-caps;letter-spacing:.16em;color:#CFB089;margin:0 0 26px">R. do Repouso, 6 · Vila Adentro · Faro</p>
    <p style="font:400 132px/0.9 Gloock;margin:0">Cantinho</p>
    <p style="font:italic 380 44px/1.15 Newsreader;color:#E57A45;margin:26px 0 0;max-width:560px">Diz a lenda que o rei descansou aqui. Hoje, janta-se.</p>
    <p style="font:400 24px Newsreader;color:#C2B5A3;margin:60px 0 0">Seg–Sáb 10:30–23:30 · 911 013 101</p></div>`;
  arch.style.cssText = 'height:630px;min-height:0;margin:0';
  arch.querySelectorAll('svg,g').forEach(e => e.style.animation = 'none');
  w.append(arch); document.body.append(w);
});
await p.waitForTimeout(400);
await p.screenshot({ path: `${pub}/assets/og.jpg`, type: 'jpeg', quality: 86 });
for (const [n, s] of [['icon-512', 512], ['icon-192', 192], ['apple-touch-icon', 180], ['favicon-32', 32]]) {
  const q = await b.newPage({ viewport: { width: s, height: s } });
  await q.goto(base + '/robots.txt');
  await q.setContent(`<style>html,body{margin:0}</style><img src="${base}/assets/icon.svg" width="${s}" height="${s}">`);
  await q.waitForTimeout(150);
  await q.screenshot({ path: `${pub}/assets/${n}.png` }); await q.close();
}
await b.close();
