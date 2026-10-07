import { chromium, devices } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--proxy-server=' + process.env.HTTPS_PROXY, '--proxy-bypass-list=127.0.0.1;localhost'] });
for (const [n, o] of [['m', devices['Pixel 7']], ['d', { viewport: { width: 1440, height: 900 } }]]) {
  const p = await (await b.newContext(o)).newPage();
  await p.goto(process.argv[2]); await p.waitForTimeout(800);
  for (const id of ['#opinioes', '#contacto', '#servicos']) {
    await p.evaluate(s => document.querySelector(s).scrollIntoView(), id); await p.waitForTimeout(1500);
    await p.screenshot({ path: `${process.argv[3]}/${n}-${id.slice(1)}.png` });
  }
}
await b.close();
