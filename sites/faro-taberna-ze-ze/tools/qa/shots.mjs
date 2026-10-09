// node shots.mjs <outdir> [url]  — desktop + mobile screenshots, console/HTTP errors
import { chromium, devices } from 'playwright';
const out = process.argv[2] || '.';
const url = process.argv[3] || 'http://127.0.0.1:8791/';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
for (const [name, opts] of [['desk', { viewport: { width: 1440, height: 900 }, locale: 'pt-PT', timezoneId: 'Europe/Lisbon' }], ['mob', { ...devices['iPhone 13'], locale: 'pt-PT', timezoneId: 'Europe/Lisbon' }], ['mob-en', { ...devices['iPhone 13'], locale: 'en-GB' }]]) {
  const ctx = await b.newContext({ ...opts, reducedMotion: process.env.MOTION ? 'no-preference' : 'reduce' }); const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text())); p.on('response', r => r.status() >= 400 && errs.push(r.status() + ' ' + r.url()));
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(2200);
  await p.screenshot({ path: `${out}/${name}-hero.png` });
  // walk the page so view()-timeline reveals settle
  const h = await p.evaluate(() => document.body.scrollHeight);
  for (let y = 0; y < h; y += 500) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(60); }
  await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(300);
  await p.screenshot({ path: `${out}/${name}-full.png`, fullPage: true });
  console.log(name, 'errors:', errs);
  await ctx.close();
}
await b.close();
