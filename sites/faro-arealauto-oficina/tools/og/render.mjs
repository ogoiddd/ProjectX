// node render.mjs  → public/assets/og.jpg + ícones PNG
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.resolve(here, '../../public/assets');
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
await p.goto('file://' + path.join(here, 'og.html')); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
await p.screenshot({ path: path.join(out, 'og.jpg'), type: 'jpeg', quality: 82 });
for (const [n, s] of [['favicon-32.png', 32], ['apple-touch-icon.png', 180], ['icon-192.png', 192], ['icon-512.png', 512]]) {
  await p.setViewportSize({ width: s, height: s });
  await p.goto('file://' + path.join(out, 'favicon.svg'));
  await p.waitForTimeout(150);
  await p.screenshot({ path: path.join(out, n), omitBackground: true });
}
await b.close();
