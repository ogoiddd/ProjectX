// node shoot.mjs  -> renders og.jpg and icon PNGs into ../../public/assets
import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';
const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(here, '../../public/assets');
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
await p.goto('file://' + path.join(here, 'og.html')); await p.waitForTimeout(400);
await p.screenshot({ path: path.join(out, 'og.jpg'), type: 'jpeg', quality: 86 });
for (const [n, s] of [['favicon-32.png', 32], ['apple-touch-icon.png', 180], ['icon-192.png', 192], ['icon-512.png', 512]]) {
  await p.setViewportSize({ width: s, height: s });
  await p.goto('file://' + path.join(here, 'icon.html')); await p.waitForTimeout(150);
  await p.screenshot({ path: path.join(out, n), omitBackground: true });
}
await b.close();
console.log('ok');
