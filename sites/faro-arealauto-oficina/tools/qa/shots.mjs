// node shots.mjs [baseUrl]  → qa/*.png (desktop + mobile, primeiro ecrã + página inteira)
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const qa = path.resolve(here, '../../qa');
const base = process.argv[2] || 'http://127.0.0.1:8611/';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
const errors = [];
for (const [name, vp, mobile] of [['desktop', { width: 1440, height: 900 }, false], ['mobile', { width: 390, height: 844 }, true]]) {
  const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: mobile ? 2 : 1, isMobile: mobile, hasTouch: mobile, locale: 'pt-PT', timezoneId: 'Europe/Lisbon' });
  const p = await ctx.newPage();
  p.on('pageerror', (e) => errors.push(name + ': ' + e.message));
  p.on('console', (m) => m.type() === 'error' && errors.push(name + ' console: ' + m.text()));
  await p.goto(base, { waitUntil: 'networkidle' });
  await p.addStyleTag({ content: 'html{scroll-behavior:auto!important}' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(1800);
  await p.screenshot({ path: `${qa}/${name}-first.png` });
  // percorrer a página para disparar observers
  const h = await p.evaluate(() => document.body.scrollHeight);
  for (let y = 0; y < h; y += vp.height / 2) { await p.evaluate((y) => scrollTo(0, y), y); await p.waitForTimeout(120); }
  await p.waitForTimeout(2600);
  await p.evaluate(() => scrollTo(0, 0));
  await p.screenshot({ path: `${qa}/${name}-full.png`, fullPage: true });
  // estado da folha preenchida
  await p.fill('#f-nome', 'Maria Exemplo'); await p.fill('#f-tel', '912 345 678'); await p.fill('#f-mat', '12ab34');
  await p.fill('#f-carro', 'Renault Clio, 2015'); await p.check('input[value="Travões"]', { force: true });
  await p.fill('#f-desc', 'Chia ao travar de manhã.');
  await p.locator('#folha').scrollIntoViewIfNeeded(); await p.waitForTimeout(400);
  await p.locator('#folha').screenshot({ path: `${qa}/${name}-folha.png` });
  await ctx.close();
}
await b.close();
console.log(errors.length ? errors.join('\n') : 'no errors');
