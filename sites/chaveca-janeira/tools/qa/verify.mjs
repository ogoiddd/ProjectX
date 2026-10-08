// Live checks: video, parallax, reduced motion, links, overflow, basic perf timings.
// Usage: node verify.mjs <url> <outDir>
import { chromium, devices } from 'playwright';
const [url, out = '.'] = process.argv.slice(2);
const local = /127\.0\.0\.1|localhost/.test(url);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--autoplay-policy=no-user-gesture-required', '--proxy-server=' + process.env.HTTPS_PROXY, '--proxy-bypass-list=127.0.0.1;localhost'] });
const report = {};
const ok = (k, v) => { report[k] = v; console.log((v && v.pass === false ? '✗ ' : '✓ ') + k, JSON.stringify(v)); };

for (const [name, opts] of [['desktop', { viewport: { width: 1440, height: 900 } }], ['mobile', devices['Pixel 7']]]) {
  const ctx = await b.newContext(opts);
  const p = await ctx.newPage();
  const errors = []; p.on('pageerror', e => errors.push(e.message));
  p.on('response', r => { if (r.status() >= 400) errors.push(r.status() + ' ' + r.url()); });
  const t0 = Date.now();
  await p.goto(url, { waitUntil: 'load' });
  const nav = await p.evaluate(() => { const n = performance.getEntriesByType('navigation')[0]; return { ttfb: Math.round(n.responseStart), dcl: Math.round(n.domContentLoadedEventEnd), load: Math.round(n.loadEventEnd) }; });
  const lcp = await p.evaluate(() => new Promise(res => { new PerformanceObserver(l => { const e = l.getEntries(); res(Math.round(e[e.length - 1].startTime)); }).observe({ type: 'largest-contentful-paint', buffered: true }); setTimeout(() => res(null), 3000); }));
  ok(`${name}: timings`, { ...nav, lcp, wall: Date.now() - t0 });
  await p.waitForTimeout(4000);
  const v = await p.evaluate(() => { const i = document.querySelector('.hero-poster'); return { src: i.currentSrc.split('/').pop(), w: i.naturalWidth, h: i.naturalHeight, video: !!document.querySelector('video') }; });
  ok(`${name}: static hero image`, { ...v, pass: /^hero-/.test(v.src) && !v.video });
  await p.screenshot({ path: `${out}/${name}-live-hero.png` });
  const before = await p.evaluate(() => [...document.querySelectorAll('[data-depth]')].map(e => getComputedStyle(e).transform));
  await p.mouse.wheel(0, 500); await p.waitForTimeout(600);
  const after = await p.evaluate(() => ({ y: scrollY, t: [...document.querySelectorAll('[data-depth]')].map(e => getComputedStyle(e).transform) }));
  const ys = after.t.map(m => { const x = m.match(/matrix\(([^)]+)\)/); return x ? +(+x[1].split(',')[5]).toFixed(1) : 0; });
  ok(`${name}: parallax layers (translateY at scroll ${after.y})`, { ys, distinctDepths: new Set(ys).size, pass: new Set(ys).size >= 3 && before.join() !== after.t.join() });
  const ov = await p.evaluate(() => ({ docW: document.documentElement.scrollWidth, vw: innerWidth }));
  ok(`${name}: no horizontal overflow`, { ...ov, pass: ov.docW <= ov.vw });
  // scroll everything so lazy media + reveals fire, then a full-page shot
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 400) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } scrollTo(0, 0); });
  await p.waitForTimeout(800);
  await p.screenshot({ path: `${out}/${name}-live-full.png`, fullPage: true });
  const links = await p.evaluate(() => ({ tel: [...document.querySelectorAll('a[href^="tel:"]')].map(a => a.getAttribute('href')), maps: [...document.querySelectorAll('a[data-directions]')].map(a => a.href) }));
  ok(`${name}: links`, { tel: [...new Set(links.tel)], telCount: links.tel.length, mapsCount: links.maps.length, maps: [...new Set(links.maps)], pass: links.tel.every(h => h === 'tel:+351289887200') && links.maps.every(h => h.startsWith('https://www.google.com/maps/dir/?api=1&destination=')) });
  ok(`${name}: console/network errors`, { errors, pass: errors.length === 0 });
  await ctx.close();
}

// Reduced motion: no transforms, no autoplay, poster visible
const rctx = await b.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
const rp = await rctx.newPage();
await rp.goto(url, { waitUntil: 'load' }); await rp.waitForTimeout(2500);
await rp.mouse.wheel(0, 600); await rp.waitForTimeout(500);
const r = await rp.evaluate(() => ({ transforms: [...document.querySelectorAll('[data-depth]')].map(e => getComputedStyle(e).transform), video: !!document.querySelector('video') }));
ok('reduced-motion', { ...r, pass: r.transforms.every(t => t === 'none') && !r.video });
await rctx.close();

// Maps link resolves (follow the directions URL)
if (!local) {
  const mctx = await b.newContext(); const mp = await mctx.newPage();
  const resp = await mp.goto('https://www.google.com/maps/dir/?api=1&destination=Euromaster%20Chaveca%20%26%20Janeira%20Faro%2C%20Estr.%20da%20Sra.%20da%20Saude%2058%2C%208000-500%20Faro', { waitUntil: 'domcontentloaded' }).catch(e => ({ status: () => e.message }));
  ok('maps directions URL', { status: resp.status(), final: mp.url().slice(0, 120) });
  await mctx.close();
}
await b.close();
