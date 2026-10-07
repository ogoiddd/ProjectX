import { chromium, devices } from 'playwright';
const [url, out] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--proxy-server=' + process.env.HTTPS_PROXY, '--proxy-bypass-list=127.0.0.1;localhost'] });
for (const [n, d] of [['iphone', devices['iPhone 15 Pro']], ['desktop', { viewport: { width: 1440, height: 900 } }]]) {
  const p = await (await b.newContext(d)).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(url); await p.waitForTimeout(1200);
  const st = async () => p.evaluate(() => { const bar = document.querySelector('.bar'), t = document.querySelector('#motionToggle'); return { y: Math.round(scrollY), barTop: Math.round(bar.getBoundingClientRect().bottom), btnVisible: getComputedStyle(t).visibility }; });
  console.log(n, 'top     ', JSON.stringify(await st()));
  await p.mouse.wheel(0, 300); await p.waitForTimeout(600); console.log(n, 'down 300', JSON.stringify(await st()));
  await p.screenshot({ path: `${out}/${n}-down.png` });
  await p.mouse.wheel(0, 1500); await p.waitForTimeout(600); console.log(n, 'down more', JSON.stringify(await st()));
  await p.mouse.wheel(0, -200); await p.waitForTimeout(600); console.log(n, 'up 200  ', JSON.stringify(await st()));
  await p.screenshot({ path: `${out}/${n}-up.png` });
  await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(600); console.log(n, 'back top', JSON.stringify(await st()), errs);
}
await b.close();
