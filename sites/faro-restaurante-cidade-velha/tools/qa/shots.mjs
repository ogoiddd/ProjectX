// Screenshots desktop + mobile for each language. Usage: node shots.mjs http://localhost:8411 ../../qa
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PW || "playwright");
const [base = "http://localhost:8411", out = "../../qa"] = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" + (process.env.PWB || "") });
const errors = [];
for (const [name, vp, mobile] of [["desktop", { width: 1440, height: 900 }, false], ["mobile", { width: 390, height: 844 }, true]]) {
  const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: mobile ? 2 : 1, isMobile: mobile, hasTouch: mobile, locale: "pt-PT", timezoneId: "Europe/Lisbon" });
  for (const lang of (process.env.LANGS || "pt,en").split(",")) {
    const page = await ctx.newPage();
    page.on("console", (m) => m.type() === "error" && errors.push(`${lang}/${name}: ${m.text()}`));
    page.on("pageerror", (e) => errors.push(`${lang}/${name}: ${e.message}`));
    await page.goto(base + (lang === "pt" ? "/" : `/${lang}/`), { waitUntil: "networkidle" });
    await page.waitForTimeout(1200);
    await page.screenshot({ path: `${out}/${lang}-${name}-fold.png` });
    // scroll through to trigger observers, then full page
    await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } window.scrollTo(0, 0); });
    await page.waitForTimeout(1800);
    await page.screenshot({ path: `${out}/${lang}-${name}-full.png`, fullPage: true });
    await page.close();
  }
  await ctx.close();
}
await browser.close();
console.log(errors.length ? errors.join("\n") : "no console errors");
