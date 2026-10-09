// node render.mjs http://localhost:8411  -> public/assets/og.jpg + icons
import { createRequire } from "node:module"; import { readFileSync } from "node:fs";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PW || "playwright");
const base = process.argv[2] || "http://localhost:8411", out = new URL("../../public/assets/", import.meta.url).pathname;
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
await p.goto(base + "/robots.txt");
await p.setContent(readFileSync(new URL("og.html", import.meta.url), "utf8"), { waitUntil: "networkidle" });
await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: out + "og.jpg", type: "jpeg", quality: 86 });
await p.setContent(readFileSync(new URL("icon.html", import.meta.url), "utf8"));
for (const s of [512, 192, 180, 32]) { await p.setViewportSize({ width: s, height: s }); await p.evaluate((s) => { const v = document.querySelector("svg"); v.setAttribute("width", s); v.setAttribute("height", s); }, s);
  await p.screenshot({ path: out + (s === 180 ? "apple-touch-icon.png" : s === 32 ? "favicon-32.png" : `icon-${s}.png`) }); }
await b.close(); console.log("ok");
