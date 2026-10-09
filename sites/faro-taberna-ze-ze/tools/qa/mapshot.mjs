import { chromium, devices } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
for (const [n, o] of [['mob', devices['iPhone 13']], ['desk', { viewport: { width: 1440, height: 900 } }]]) {
  const p = await (await b.newContext({ ...o, locale: 'pt-PT', reducedMotion: 'reduce' })).newPage();
  await p.goto('http://127.0.0.1:8791/', { waitUntil: 'networkidle' });
  await p.locator('.map').screenshot({ path: `${process.argv[2]}/${n}-map.png` });
}
await b.close();
