// node interact.mjs <outdir> — exercises the table request: stepper, day/time, dish add, EN toggle; checks the WhatsApp link
import { chromium, devices } from 'playwright';
const out = process.argv[2] || '.';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const ctx = await b.newContext({ ...devices['iPhone 13'], locale: 'pt-PT', timezoneId: 'Europe/Lisbon', reducedMotion: 'reduce' });
const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
await p.goto('http://127.0.0.1:8791/', { waitUntil: 'networkidle' });
await p.click('.step[data-step="1"]'); await p.click('.step[data-step="1"]');
const day = p.locator('#days input:not([disabled])').nth(1); await day.check({ force: true });
await p.locator('#times input[value="21:00"]').check({ force: true });
await p.fill('#name', 'Ana Martins'); await p.fill('#note', 'Uma cadeira de bebé');
await p.locator('.add').nth(2).click();
console.log('PT preview:\n' + await p.textContent('#preview'));
console.log('WA:', decodeURIComponent((await p.getAttribute('#sendWa', 'href')).split('text=')[1]).slice(0, 80) + '…');
await p.locator('#mesa').scrollIntoViewIfNeeded(); await p.screenshot({ path: `${out}/mob-comanda-filled.png` });
await p.click('#lang'); await p.waitForTimeout(400);
console.log('EN preview:\n' + await p.textContent('#preview'));
console.log('EN status:', await p.textContent('#statusText'));
await p.evaluate(() => document.querySelector('#onde').scrollIntoView()); await p.waitForTimeout(200);
await p.screenshot({ path: `${out}/mob-map-en.png` });
// keyboard: tab order reaches the WhatsApp button
await p.evaluate(() => scrollTo(0, 0));
let hit = false; for (let i = 0; i < 60 && !hit; i++) { await p.keyboard.press('Tab'); hit = await p.evaluate(() => document.activeElement?.id === 'sendWa'); }
console.log('keyboard reaches WhatsApp button:', hit, 'errors:', errs);
await b.close();
