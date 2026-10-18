// node shots.mjs [baseUrl]  → qa/*.png (desktop + mobile) e og.png
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const qa = path.resolve(here, '../../qa');
const base = process.argv[2] || 'http://127.0.0.1:8622/';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
const errors = [];

const og = await b.newPage({ viewport: { width: 1200, height: 630 } });
await og.goto('file://' + path.resolve(here, '../og/og.html'));
await og.evaluate(() => document.fonts.ready);
await og.screenshot({ path: path.resolve(here, '../../public/assets/og.png') });
await og.close();

for (const [name, vp, mobile] of [['desktop', { width: 1440, height: 900 }, false], ['mobile', { width: 390, height: 844 }, true]]) {
  const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: mobile ? 2 : 1, isMobile: mobile, hasTouch: mobile, locale: 'pt-PT', timezoneId: 'Europe/Lisbon' });
  const p = await ctx.newPage();
  p.on('pageerror', (e) => errors.push(name + ': ' + e.message));
  p.on('console', (m) => m.type() === 'error' && errors.push(name + ' console: ' + m.text()));
  await p.goto(base, { waitUntil: 'networkidle' });
  await p.addStyleTag({ content: 'html{scroll-behavior:auto!important}' });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: `${qa}/${name}-first.png` });
  // maquete ao vivo preenchida
  await p.fill('#t-nome', 'Clínica Dentária do Mar');
  await p.fill('#t-cidade', 'Loulé');
  await p.click('label:has(input[value="fisioterapia"])');
  await p.waitForTimeout(500);
  await p.screenshot({ path: `${qa}/${name}-maquete.png` });
  // a meio da rota
  await p.evaluate(() => { const s = document.querySelector('#como'); scrollTo(0, s.offsetTop - innerHeight * 0.2 + s.offsetHeight * 0.35); });
  await p.waitForTimeout(400);
  await p.screenshot({ path: `${qa}/${name}-rota.png` });
  const h = await p.evaluate(() => document.body.scrollHeight);
  for (let y = 0; y < h; y += vp.height / 2) { await p.evaluate((y) => scrollTo(0, y), y); await p.waitForTimeout(80); }
  await p.waitForTimeout(600);
  await p.evaluate(() => scrollTo(0, 0));
  await p.screenshot({ path: `${qa}/${name}-full.png`, fullPage: true });
  // pedir esta maquete → formulário preenchido
  await p.click('#try button[type=submit]');
  await p.waitForTimeout(900);
  const vals = await p.evaluate(() => [document.activeElement.id, document.querySelector('#f-nome').value, document.querySelector('#f-cidade').value, document.querySelector('#f-esp').value]);
  if (vals.join('|') !== 'f-contacto|Clínica Dentária do Mar|Loulé|fisioterapia') errors.push(name + ' prefill: ' + vals.join('|'));
  await p.click('#form button[type=submit]');
  const err = await p.textContent('#f-err');
  if (err !== 'Falta um email ou telefone.') errors.push(name + ' validação: ' + err);
  await p.screenshot({ path: `${qa}/${name}-pedir.png` });
  const sw = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
  if (sw > 0) errors.push(name + ' horizontal overflow ' + sw);
  await ctx.close();
}
await b.close();
console.log(errors.length ? errors.join('\n') : 'no errors');
