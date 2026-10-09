// Per-section screenshots. Usage: node sections.mjs <outdir> [baseUrl]
import { chromium, devices } from 'playwright';
const out = process.argv[2] || '.'; const base = process.argv[3] || 'http://127.0.0.1:8790';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
for (const [name, opts, path] of [['desk', { viewport: { width: 1440, height: 900 } }, '/'], ['mob', devices['iPhone 13'], '/en/']]) {
  const ctx = await b.newContext({ ...opts, timezoneId: 'Europe/Lisbon' }); const p = await ctx.newPage();
  await p.goto(base + path, { waitUntil: 'networkidle' });
  for (const s of ['.hero', '.casa', '.ementa', '.vozes', '.reservar', '.onde', '.foot']) {
    const el = p.locator(s).first(); await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(400);
    await el.screenshot({ path: `${out}/${name}-sec-${s.slice(1)}.png` });
  }
  await ctx.close();
}
await b.close();
