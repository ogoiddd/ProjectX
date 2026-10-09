import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PW || "playwright");
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await b.newPage({ viewport: { width: 390, height: 844 } });
await p.goto((process.argv[2] || "http://localhost:8411") + "/");
const r = await p.evaluate(() => {
  const W = document.documentElement.clientWidth, out = [];
  document.querySelectorAll("body *").forEach((el) => { const b = el.getBoundingClientRect(); if (b.right > W + 1 && b.width > 0) out.push(el.tagName + "." + el.className.baseVal + el.className + " " + Math.round(b.right)); });
  const route = document.querySelector(".m-route-1");
  return { W, sw: document.documentElement.scrollWidth, over: out.slice(0, 15), d: route.getAttribute("d").slice(0, 120), cs: getComputedStyle(route).strokeDashoffset, bar: getComputedStyle(document.querySelector(".bar")).display };
});
console.log(JSON.stringify(r, null, 1));
await b.close();
