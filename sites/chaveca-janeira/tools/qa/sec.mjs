import { chromium, devices } from 'playwright';
const [url, out, ...ids] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--proxy-server=' + process.env.HTTPS_PROXY, '--proxy-bypass-list=127.0.0.1;localhost'] });
for (const [n, o] of [['m', devices['Pixel 7']], ['d', { viewport: { width: 1440, height: 900 } }]]) {
  const p = await (await b.newContext(o)).newPage();
  await p.goto(url); await p.waitForTimeout(1200);
  await p.screenshot({ path: `${out}/${n}-top.png` });
  for (const id of ids) { await p.evaluate(s => { const e = document.querySelector(s); scrollTo(0, e.getBoundingClientRect().top + scrollY - 70); }, id); await p.waitForTimeout(900); await p.screenshot({ path: `${out}/${n}-${id.replace(/\W/g, '')}.png` }); }
}
await b.close();
