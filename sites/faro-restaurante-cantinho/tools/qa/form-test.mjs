// Fills the booking form and checks the generated WhatsApp URL. Usage: node form-test.mjs [baseUrl]
import { chromium, devices } from 'playwright';
const base = process.argv[2] || 'http://127.0.0.1:8790';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const ctx = await b.newContext({ ...devices['iPhone 13'], timezoneId: 'Europe/Lisbon' });
const p = await ctx.newPage();
let hit = null;
await ctx.route(/wa\.me/, r => { hit = r.request().url(); r.fulfill({ body: 'ok' }); });
await p.goto(base + '/');
await p.fill('#r-nome', 'Ana Teste');
await p.click('[data-pax="1"]'); await p.click('[data-pax="1"]');
await p.check('input[name=onde][value=esplanada]', { force: true });
await p.fill('#r-data', '2026-10-11'); // a Sunday
console.log('sunday error:', await p.textContent('#r-data-err'));
await p.fill('#r-data', '2026-10-13');
console.log('ticket:', await p.textContent('[data-ticket]'));
await p.click('button[data-via=wa]');
await p.waitForTimeout(800);
console.log('wa url:', hit && decodeURIComponent(hit));
await b.close();
