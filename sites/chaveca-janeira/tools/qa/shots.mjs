import { chromium, devices } from 'playwright';
const out = process.argv[2] || '.';
const url = process.argv[3] || 'http://127.0.0.1:8765/';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--proxy-server=' + process.env.HTTPS_PROXY, '--proxy-bypass-list=127.0.0.1;localhost'] });
for (const [name, opts] of [['desk', { viewport: { width: 1440, height: 900 } }], ['mob', devices['iPhone 13']]]) {
  const ctx = await b.newContext(opts); const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('response', r => r.status() >= 400 && errs.push(r.status() + ' ' + r.url()));
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
  await p.screenshot({ path: `${out}/${name}-hero.png` });
  await p.screenshot({ path: `${out}/${name}-full.png`, fullPage: true });
  console.log(name, 'errors:', errs);
  await ctx.close();
}
await b.close();
