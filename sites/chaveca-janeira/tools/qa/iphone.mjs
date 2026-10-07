import { chromium, devices } from 'playwright';
const [url, out] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--autoplay-policy=no-user-gesture-required'] });
const ctx = await b.newContext({ ...devices['iPhone 15 Pro'] });
const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
await p.goto(url, { waitUntil: 'load' }); await p.waitForTimeout(3500);
const v = await p.evaluate(() => { const v = document.querySelector('#heroVideo'); return { paused: v.paused, w: v.videoWidth, h: v.videoHeight, on: v.classList.contains('on') }; });
console.log('video', JSON.stringify(v), 'errors', errs);
const shots = [['01-inicio', null], ['02-oficina', '.about'], ['03-servicos', '#servicos'], ['04-fotos', '.band'], ['05-opinioes', '#opinioes'], ['06-horario', '#horario'], ['07-localizacao', '#local'], ['08-contacto', '#contacto']];
for (const [n, sel] of shots) {
  if (sel) await p.evaluate(s => { const e = document.querySelector(s); scrollTo(0, e.getBoundingClientRect().top + scrollY - 70); }, sel);
  await p.waitForTimeout(700); await p.screenshot({ path: `${out}/iphone-${n}.png` });
}
await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(400);
await p.click('#menuBtn'); await p.waitForTimeout(300); await p.screenshot({ path: `${out}/iphone-09-menu.png` });
await b.close();
