import { chromium, devices } from 'playwright';
const [url, out] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--proxy-server=' + process.env.HTTPS_PROXY, '--proxy-bypass-list=127.0.0.1;localhost'] });
for (const [n, d] of [['desk-2000x1127', { viewport: { width: 2000, height: 1127 } }], ['desk-1440', { viewport: { width: 1440, height: 900 } }], ['laptop-1280x720', { viewport: { width: 1280, height: 720 } }], ['iphone', devices['iPhone 15 Pro']], ['se', devices['iPhone SE']]]) {
  const p = await (await b.newContext(d)).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(url); await p.waitForTimeout(1200);
  const r = await p.evaluate(() => { const ob = document.querySelector('#openbar').getBoundingClientRect(), h1 = document.querySelector('.hero h1').getBoundingClientRect(), bar = document.querySelector('.bar').getBoundingClientRect(); return { strip: [Math.round(ob.top), Math.round(ob.bottom)], h1Top: Math.round(h1.top), overlap: h1.top < ob.bottom, text: document.querySelector('#openbar').innerText, pauseBtn: !!document.querySelector('#motionToggle') }; });
  console.log(n, JSON.stringify(r), errs);
  await p.screenshot({ path: `${out}/${n}.png` });
}
await b.close();
