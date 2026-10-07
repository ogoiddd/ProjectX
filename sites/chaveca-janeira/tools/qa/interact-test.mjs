// Checks jump links land on their section (not hidden under the header), services expand, copy works, live hours text.
import { chromium, devices } from 'playwright';
const [url, out] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--proxy-server=' + process.env.HTTPS_PROXY, '--proxy-bypass-list=127.0.0.1;localhost'] });
for (const [n, d] of [['iphone', devices['iPhone 15 Pro']], ['desktop', { viewport: { width: 1440, height: 900 } }]]) {
  const ctx = await b.newContext({ ...d, permissions: ['clipboard-read', 'clipboard-write'] }); const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(url); await p.waitForTimeout(1200);
  const land = async (sel, id) => {
    await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(500);
    if (sel.startsWith('#menu')) { await p.click('#menuBtn'); await p.waitForTimeout(200); }
    await p.click(sel); await p.waitForTimeout(1600);
    return p.evaluate(id => { const t = document.getElementById(id).getBoundingClientRect().top; const bar = document.querySelector('.bar').getBoundingClientRect(); return { top: Math.round(t), barBottom: Math.round(bar.bottom), hidden: t < Math.max(0, bar.bottom) - 2, hash: location.hash, current: document.querySelector(`.nav a[href="#${id}"]`)?.getAttribute('aria-current') }; }, id);
  };
  for (const id of ['servicos', 'horario', 'local', 'opinioes']) console.log(n, 'hero jump →', id, JSON.stringify(await land(`.jump a[href="#${id}"]`, id)));
  if (n === 'iphone') console.log(n, 'menu → local', JSON.stringify(await land('#menu a[href="#local"]', 'local')));
  else console.log(n, 'nav → horario', JSON.stringify(await land('.nav a[href="#horario"]', 'horario')));
  // jump back up from bottom
  await p.evaluate(() => scrollTo(0, document.body.scrollHeight)); await p.waitForTimeout(600);
  await p.click(n === 'iphone' ? '.dock a[href="#horario"]' : '.to-top a').catch(e => console.log('click err', e.message.slice(0, 80))); await p.waitForTimeout(1600);
  console.log(n, n === 'iphone' ? 'dock → horario (from bottom, upward)' : 'to top', JSON.stringify(await p.evaluate(() => ({ y: Math.round(scrollY), horarioTop: Math.round(document.getElementById('horario').getBoundingClientRect().top), barBottom: Math.round(document.querySelector('.bar').getBoundingClientRect().bottom) }))));
  if (n === 'iphone') await p.screenshot({ path: `${out}/iphone-dock-hours.png` });
  // services
  await p.evaluate(() => document.getElementById('servicos').scrollIntoView()); await p.waitForTimeout(400);
  await p.click('details.svc summary >> nth=1'); await p.waitForTimeout(300);
  console.log(n, 'service open', await p.evaluate(() => { const d = document.querySelectorAll('details.svc')[1]; return d.open + ' | ' + d.querySelector('.svc-more p').textContent.slice(0, 50) + ' | ' + d.querySelector('.svc-call').href; }));
  if (n === 'iphone') { await p.evaluate(() => { const d = document.querySelectorAll('details.svc')[1]; scrollTo(0, d.getBoundingClientRect().top + scrollY - 200); }); await p.waitForTimeout(400); await p.screenshot({ path: `${out}/iphone-service-open.png` }); }
  // copy
  await p.evaluate(() => document.getElementById('local').scrollIntoView()); await p.waitForTimeout(300);
  await p.click('#copyAddr'); await p.waitForTimeout(400);
  console.log(n, 'copy', await p.evaluate(() => navigator.clipboard.readText()), '| toast:', await p.textContent('#toast'));
  if (n === 'iphone') { await p.evaluate(() => { const e = document.querySelector('.where-actions'); scrollTo(0, e.getBoundingClientRect().top + scrollY - 420); }); await p.waitForTimeout(300); await p.click('#copyAddr'); await p.waitForTimeout(250); await p.screenshot({ path: `${out}/iphone-location.png` }); }
  console.log(n, 'hours heading:', await p.textContent('#openNow'), '| vcard:', await p.getAttribute('.where-actions a[download]', 'href'), '| errors', errs);
  await ctx.close();
}
await b.close();
