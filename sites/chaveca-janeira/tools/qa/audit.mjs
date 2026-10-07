import { chromium, devices } from 'playwright';
const [url, out] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--proxy-server=' + process.env.HTTPS_PROXY] });
for (const [n, o] of [['desk', { viewport: { width: 1440, height: 900 } }], ['mob', devices['Pixel 7']]]) {
  const ctx = await b.newContext({ ...o, locale: 'pt-PT' }); const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push('JS: ' + e.message)); p.on('response', r => r.status() >= 400 && errs.push(r.status() + ' ' + r.url().slice(0, 140)));
  let bytes = 0, reqs = 0; p.on('response', async r => { reqs++; const l = +(r.headers()['content-length'] || 0); bytes += l; });
  const t0 = Date.now(); await p.goto(url, { waitUntil: 'load', timeout: 90000 }); const tl = Date.now() - t0;
  await p.waitForTimeout(4000);
  await p.screenshot({ path: `${out}/${n}-top.png` });
  const info = await p.evaluate(() => {
    const q = s => document.querySelector(s);
    const imgs = [...document.images];
    return {
      title: document.title, desc: q('meta[name=description]')?.content, canonical: q('link[rel=canonical]')?.href, lang: document.documentElement.lang,
      ogImage: q('meta[property="og:image"]')?.content, h1: [...document.querySelectorAll('h1')].map(h => h.innerText.trim()), h2: [...document.querySelectorAll('h2')].map(h => h.innerText.trim()).slice(0, 25),
      tel: [...document.querySelectorAll('a[href^="tel:"]')].map(a => a.getAttribute('href')).slice(0, 10),
      imgsNoAlt: imgs.filter(i => !i.hasAttribute('alt') || !i.alt.trim()).length, imgs: imgs.length,
      jsonld: [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => s.textContent.slice(0, 200)),
      docW: document.documentElement.scrollWidth, vw: innerWidth, height: document.body.scrollHeight,
      fonts: [...new Set([...document.querySelectorAll('h1,h2,p,a,button')].slice(0, 200).map(e => getComputedStyle(e).fontFamily))].slice(0, 6),
      emoji: (document.body.innerText.match(/\p{Extended_Pictographic}/gu) || []).length,
      emdash: (document.body.innerText.match(/—/g) || []).length,
      text: document.body.innerText.slice(0, 5000)
    };
  });
  console.log('=====', n, 'load ms', tl, 'requests', reqs);
  console.log(JSON.stringify({ ...info, text: undefined }, null, 1));
  console.log('ERRORS', errs.slice(0, 25));
  if (n === 'desk') console.log('TEXT\n' + info.text);
  await p.screenshot({ path: `${out}/${n}-full.png`, fullPage: true });
  await ctx.close();
}
await b.close();
