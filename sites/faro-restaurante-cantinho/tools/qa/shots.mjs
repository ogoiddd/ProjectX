// Screenshots desktop + mobile (PT/EN, day/night sky). Usage: node shots.mjs <outdir> [baseUrl]
import { chromium, devices } from 'playwright';
const out = process.argv[2] || '.';
const base = process.argv[3] || 'http://127.0.0.1:8790';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--proxy-bypass-list=127.0.0.1;localhost'] });
const runs = [
  ['desk', { viewport: { width: 1440, height: 900 } }, '/', ''],
  ['desk-night', { viewport: { width: 1440, height: 900 } }, '/', '?ceu=night'],
  ['mob', devices['iPhone 13'], '/', ''],
  ['mob-en', devices['iPhone 13'], '/en/', '?ceu=dusk'],
];
for (const [name, opts, path, q] of runs) {
  const ctx = await b.newContext({ ...opts, timezoneId: 'Europe/Lisbon' });
  const p = await ctx.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text()));
  p.on('response', r => r.status() >= 400 && errs.push(r.status() + ' ' + r.url()));
  await p.goto(base + path + q, { waitUntil: 'networkidle' });
  await p.waitForTimeout(800);
  await p.screenshot({ path: `${out}/${name}-hero.png` });
  if (!name.includes('night')) {
    // scroll through so scroll-driven animations settle, then full page
    const h = await p.evaluate(() => document.body.scrollHeight);
    for (let y = 0; y < h; y += 500) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(60); }
    await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(300);
    await p.screenshot({ path: `${out}/${name}-full.png`, fullPage: true });
  }
  console.log(name, 'errors:', errs);
  await ctx.close();
}
await b.close();
