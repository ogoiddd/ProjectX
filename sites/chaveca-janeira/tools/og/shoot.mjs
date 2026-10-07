import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
const A = '../../public/assets/';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY } });
const shot = async (file, w, h, out, type = 'png') => {
  const p = await b.newPage({ viewport: { width: w, height: h } });
  await p.goto(pathToFileURL(file).href, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: A + out, type, quality: type === 'jpeg' ? 86 : undefined, omitBackground: type === 'png' });
  await p.close();
};
await shot('og.html', 1200, 630, 'og.jpg', 'jpeg');
await shot('icon.html', 180, 180, 'apple-touch-icon.png');
await shot('icon.html', 32, 32, 'favicon-32.png');
await shot('icon.html', 512, 512, 'icon-512.png');
await shot('icon.html', 192, 192, 'icon-192.png');
await b.close();
