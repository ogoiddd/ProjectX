// Usage: node render.mjs <outDir> [frames=1] [view=hero] [w] [h] [startFrame]
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { extname, join } from 'node:path';
const [out = 'frames', frames = '1', view = 'hero', w = '2560', h = '1440', start = '0', fps = '30', loop = '10'] = process.argv.slice(2);
const types = { '.html': 'text/html', '.js': 'text/javascript' };
const srv = createServer(async (q, r) => { let body; const f = join(process.cwd(), decodeURIComponent(q.url.split('?')[0])); try { body = await readFile(f); } catch { r.writeHead(404); return r.end(); } r.writeHead(200, { 'content-type': types[extname(f)] || 'application/octet-stream' }); r.end(body); }).listen(0);
const port = srv.address().port;
await mkdir(out, { recursive: true });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const p = await b.newPage({ viewport: { width: +w, height: +h } });
p.on('console', m => console.log('page:', m.text())); p.on('pageerror', e => console.log('ERR', e.message));
await p.goto(`http://localhost:${port}/scene.html?w=${w}&h=${h}&view=${view}&loop=${loop}`, { waitUntil: 'domcontentloaded', timeout: 120000 });
await p.waitForFunction('window.ready === true', null, { timeout: 120000 });
const t0 = Date.now();
for (let i = +start; i < +start + +frames; i++) {
  await p.evaluate(t => window.renderAt(t), i / +fps);
  const d = await p.evaluate(() => window.grab());
  await writeFile(`${out}/f${String(i).padStart(4, '0')}.png`, Buffer.from(d.split(',')[1], 'base64'));
  if (i % 10 === 0) console.log('frame', i, ((Date.now() - t0) / 1000).toFixed(1) + 's');
}
await b.close(); srv.close();
