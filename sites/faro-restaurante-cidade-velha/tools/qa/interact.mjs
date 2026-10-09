// Fill the booking form (EN page), check validation + WhatsApp link, status text. node interact.mjs http://localhost:8411
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PW || "playwright");
const base = process.argv[2] || "http://localhost:8411";
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, timezoneId: "Europe/Lisbon" });
const p = await ctx.newPage();
await p.goto(base + "/en/");
console.log("status:", await p.textContent("[data-status-text]"));
await p.click("button[value=wa]");
console.log("empty-name error:", await p.textContent("#e-name"));
await p.fill("#f-name", "Anna Schmidt");
// pick next Sunday -> expect error
const sunday = await p.evaluate(() => { const d = new Date(); d.setDate(d.getDate() + ((7 - d.getDay()) % 7 || 7)); return d.toLocaleDateString("sv"); });
await p.fill("#f-date", sunday); await p.click("button[value=wa]");
console.log("sunday error:", await p.textContent("#e-date"));
const tue = await p.evaluate(() => { const d = new Date(); d.setDate(d.getDate() + ((9 - d.getDay()) % 7 || 7)); return d.toLocaleDateString("sv"); });
await p.fill("#f-date", tue);
await p.click("[data-step='1']"); await p.check("input[name=mesa][value='Esplanada, no Largo']", { force: true });
await p.fill("#f-notes", "Vegetarian, one guest");
const [popup] = await Promise.all([ctx.waitForEvent("page"), p.click("button[value=wa]")]);
console.log("wa url:", decodeURIComponent(popup.url()).slice(0, 400));
console.log("preview:\n" + await p.textContent("[data-preview]"));
await p.locator(".ticket-wrap").screenshot({ path: "../../qa/en-booking-ticket.png" });
await b.close();
