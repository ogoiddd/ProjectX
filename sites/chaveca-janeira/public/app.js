(() => {
  const doc = document.documentElement;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');

  /* ---------- Language (PT default, EN toggle) ---------- */
  const EN = {
    'skip': 'Skip to content',
    'nav.services': 'Services', 'nav.reviews': 'Reviews', 'nav.hours': 'Hours', 'nav.location': 'Location',
    'hero.eyebrow': 'Euromaster network · Faro',
    'hero.t1': 'Tyres and', 'hero.t2': 'quick servicing', 'hero.t3': 'in Faro.',
    'hero.lede': 'We change, repair and align tyres and look after your car’s routine maintenance: oil, filters, brakes and battery. You’ll find us on Estrada da Senhora da Saúde, in Faro.',
    'cta.call': 'Call 289 887 200', 'cta.directions': 'Get directions',
    'hero.rating': 'Google: 4.5 from 407 reviews',
    'about.kicker': 'The workshop', 'about.title': 'Tyres in the Algarve since 1957.',
    'about.p0': 'Chaveca & Janeira was founded in 1957 in São Brás de Alportel by Sebastião de Sousa Chaveca and Joaquim Guerreiro Janeira to retread lorry tyres. It is still a family business.',
    'about.p1': 'At the Faro workshop, besides changing your tyres, you’ll find quick mechanical services for cars and light vehicles: oil changes, batteries, brakes and more.',
    'about.p2': 'We work with top-quality parts and the leading tyre brands. Whether it’s a puncture halfway through a trip or routine maintenance, call ahead or drop by.',
    'facts.company.k': 'Company', 'facts.network.k': 'Network', 'facts.network.v': 'Euromaster',
    'facts.vehicles.k': 'Vehicles', 'facts.vehicles.v': 'Cars and light vehicles',
    'facts.access.k': 'Access', 'facts.access.v': 'Wheelchair-accessible entrance and parking',
    'services.kicker': 'Workshop services', 'services.title': '14 services, from tyres to brakes.',
    'svc.tyres': 'Tyres', 'svc.mech': 'Quick servicing',
    'svc.change': 'Tyre change', 'svc.change.d': 'From the leading brands, for your car.',
    'svc.repair': 'Puncture repair', 'svc.repair.d': 'We check the damage and tell you whether it can be repaired or the tyre needs replacing.',
    'svc.rotate': 'Tyre rotation', 'svc.rotate.d': 'Swapping tyres between axles for more even wear.',
    'svc.align': 'Wheel alignment', 'svc.align.d': 'So the car tracks straight and the tyres last longer.',
    'svc.n2': 'Nitrogen tyre inflation',
    'svc.warranty': 'Master Garantia', 'svc.warranty.d': 'Tyre warranty against damage for the life of the tyre, with no mileage limit, valid at any Euromaster centre.',
    'svc.oil': 'Oil change', 'svc.filters': 'Car filters', 'svc.brakes': 'Brake system', 'svc.brakes.d': 'Brake pads and a check of the whole system.',
    'svc.shocks': 'Shock absorbers', 'svc.ac': 'Air conditioning', 'svc.battery': 'Battery', 'svc.wipers': 'Wiper blades', 'svc.aro': 'Official service (ARO)',
    'reviews.title': 'What customers write',
    'cap.facade': 'Estrada da Senhora da Saúde 58, Faro', 'cap.911': 'Wheel alignment at the workshop', 'cap.workshop': 'Inside the workshop',
    'img.facade': 'The workshop front on Estrada da Senhora da Saúde, with the blue, yellow and green Euromaster fascia and signs for quick servicing, tyres, alignment and air conditioning',
    'img.911': 'White Porsche 911 on the alignment lift with the aligner targets fitted to the wheels',
    'img.workshop': 'Inside the workshop: iron roof trusses, red wheel aligners and tyre changers, and the yellow work-zone line',
    'img.rs6': 'Audi RS 6 on the alignment lift with its headlights on',
    'reviews.note': '4.5 from 407 reviews on Google. Three of them, copied exactly as written:',
    'reviews.all': 'Read all reviews on Google Maps',
    'hours.kicker': 'Opening hours', 'hours.title': 'Open Monday to Saturday.', 'hours.caption': 'Opening hours',
    'd.mon': 'Monday', 'd.tue': 'Tuesday', 'd.wed': 'Wednesday', 'd.thu': 'Thursday', 'd.fri': 'Friday', 'd.sat': 'Saturday', 'd.sun': 'Sunday', 'd.closed': 'Closed',
    'where.kicker': 'Location', 'where.cta': 'Open directions in Google Maps',
    'where.note': 'Between Avenida Calouste Gulbenkian and the Fórum roundabout.',
    'foot.name': 'Workshop', 'foot.addr': 'Address', 'foot.hours': 'Hours', 'foot.phone': 'Phone',
    'foot.hours.v': 'Mon–Fri 9:00–19:00<br>Sat 9:00–13:00 · Sun closed',
    'foot.link': 'Page on euromaster.pt', 'foot.legal': 'Legal information and privacy', 'foot.complaints': 'Complaints book (Livro de Reclamações)',
    'foot.ral': 'In the event of a dispute, consumers may turn to CIMAAL, the Algarve consumer arbitration centre (<a href="https://www.consumoalgarve.pt" target="_blank" rel="noopener">www.consumoalgarve.pt</a>). More information on the Portal do Consumidor, <a href="https://www.consumidor.gov.pt" target="_blank" rel="noopener">www.consumidor.gov.pt</a>.',
    'dock': 'Call', 'menu': 'Menu', 'dock.dir': 'Directions', 'openbar.more': 'See hours', 'dock.label': 'Quick actions', 'jump.label': 'Shortcuts',
    'svc.book': 'Call to book', 'svc.n2.d': 'Nitrogen escapes more slowly than air, so tyre pressure stays stable for longer.',
    'svc.oil.d': 'Engine oil change following your car’s maintenance schedule.', 'svc.filters.d': 'Checking and replacing your car’s filters.',
    'svc.shocks.d': 'Checking and replacing shock absorbers.', 'svc.battery.d': 'Battery testing and replacement.',
    'svc.wipers.d': 'Replacing wiper blades so you can see clearly in the rain.', 'svc.ac.d': 'Air conditioning check and recharge.',
    'svc.aro.d': 'Servicing your car to the manufacturer’s maintenance schedule.',
    'where.copy': 'Copy address', 'where.vcard': 'Save contact', 'copied': 'Address copied', 'foot.top': 'Back to top'
  };
  const PT = {};
  $$('[data-i18n]').forEach(el => { PT[el.dataset.i18n] = el.innerHTML; });
  $$('[data-i18n-alt]').forEach(el => { PT[el.dataset.i18nAlt] = el.alt; });
  $$('[data-i18n-aria]').forEach(el => { PT[el.dataset.i18nAria] = el.getAttribute('aria-label'); });
  let lang = 'pt';
  try { if (localStorage.getItem('lang') === 'en') lang = 'en'; } catch {}
  const t = (k) => (lang === 'en' ? EN : PT)[k];
  function applyLang() {
    doc.lang = lang === 'en' ? 'en' : 'pt-PT';
    $$('[data-i18n]').forEach(el => { const v = t(el.dataset.i18n); if (v != null) el.innerHTML = v; });
    $$('[data-i18n-alt]').forEach(el => { const v = t(el.dataset.i18nAlt); if (v != null) el.alt = v; });
    $$('[data-i18n-aria]').forEach(el => { const v = t(el.dataset.i18nAria); if (v != null) el.setAttribute('aria-label', v); });
    const b = $('#lang');
    b.textContent = lang === 'en' ? 'PT' : 'EN';
    b.setAttribute('aria-label', lang === 'en' ? 'Mudar para português' : 'Switch to English');
    updateStatus();
  }
  $('#lang').addEventListener('click', () => {
    lang = lang === 'en' ? 'pt' : 'en';
    try { localStorage.setItem('lang', lang); } catch {}
    applyLang();
  });

  /* ---------- Mobile menu ---------- */
  const menuBtn = $('#menuBtn'), menu = $('#menu');
  function setMenu(open) {
    menu.hidden = !open; menuBtn.setAttribute('aria-expanded', String(open));
    $('.bar').classList.toggle('open', open);
  }
  menuBtn.addEventListener('click', () => setMenu(menu.hidden));
  menu.addEventListener('click', e => { if (e.target.closest('a')) setMenu(false); });
  addEventListener('keydown', e => { if (e.key === 'Escape' && !menu.hidden) { setMenu(false); menuBtn.focus(); } });
  matchMedia('(min-width: 900px)').addEventListener('change', e => { if (e.matches) setMenu(false); });

  /* ---------- Open now (Europe/Lisbon) ---------- */
  const HOURS = { 1: [9, 19], 2: [9, 19], 3: [9, 19], 4: [9, 19], 5: [9, 19], 6: [9, 13] };
  function lisbonNow() {
    const p = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Lisbon', weekday: 'short', hour: 'numeric', minute: 'numeric', hourCycle: 'h23' }).formatToParts(new Date());
    const g = (k) => p.find(x => x.type === k).value;
    const day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(g('weekday'));
    return { day, mins: +g('hour') * 60 + +g('minute') };
  }
  function updateStatus() {
    const { day, mins } = lisbonNow();
    const h = HOURS[day];
    const open = h && mins >= h[0] * 60 && mins < h[1] * 60;
    const en = lang === 'en';
    let msg;
    if (open) msg = en ? `Open now · closes at ${h[1]}:00` : `Aberto agora · fecha às ${h[1]}:00`;
    else {
      let d = day, first = true;
      for (let i = 0; i < 8; i++) {
        const hh = HOURS[d];
        if (hh && (!first || mins < hh[0] * 60)) break;
        d = (d + 1) % 7; first = false;
      }
      const names = en ? ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'] : ['domingo', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado'];
      const when = d === day ? (en ? 'today' : 'hoje') : d === (day + 1) % 7 ? (en ? 'tomorrow' : 'amanhã') : names[d];
      msg = en ? `Closed · opens ${when} at 9:00` : `Fechado · abre ${when} às 9:00`;
    }
    const s = $('#status'); if (s) s.textContent = msg;
    // hours heading: live countdown while open
    const head = $('#openNow');
    if (head) {
      if (open) {
        const left = h[1] * 60 - mins, hh = Math.floor(left / 60), mm = left % 60;
        const dur = (hh ? `${hh} h ` : '') + `${mm} min`;
        head.textContent = en ? `Open now. Closes in ${dur}.` : `Aberto agora. Fecha daqui a ${dur}.`;
      } else head.textContent = msg.replace(/ · (\w)/, (_, c) => '. ' + c.toUpperCase()) + '.';
    }
    $('.dot')?.classList.toggle('closed', !open);
    $('#openbar')?.classList.toggle('closed', !open);
    $$('.hours-table tr').forEach(tr => {
      const today = +tr.dataset.day === day;
      tr.classList.toggle('today', today);
      if (today) tr.querySelector('th').dataset.today = open ? (en ? 'Open now' : 'Aberto agora') : (en ? 'Today' : 'Hoje');
    });
  }
  setInterval(updateStatus, 60000);

  /* ---------- Parallax: transform-only, rAF-batched, 3 depths in the hero ---------- */
  const layers = $$('[data-depth]').map(el => ({ el, d: parseFloat(el.dataset.depth), fade: el.hasAttribute('data-fade') }));
  const inner = $$('[data-depth-inner]').map(el => ({ el, d: parseFloat(el.dataset.depthInner), box: el.parentElement }));
  const rollers = $$('[data-roll]').map(el => ({ el, d: parseFloat(el.dataset.roll), box: el.parentElement }));
  const bar = $('.bar'), dock = $('.dock'), hero = $('.hero');
  let ticking = false, vh = innerHeight, lastY = scrollY;
  function frame() {
    ticking = false;
    const y = scrollY;
    bar.classList.toggle('scrolled', y > vh * 0.7);
    // header hides while scrolling down, comes back when scrolling up or near the top
    const dy = y - lastY;
    if (y < 10) bar.classList.remove('hide');
    else if (dy > 4 && menu.hidden) bar.classList.add('hide');
    else if (dy < -4) bar.classList.remove('hide');
    lastY = y;
    dock.classList.toggle('show', y > vh * 0.6);
    if (reduce.matches) return;
    const heroH = hero.offsetHeight;
    for (const l of layers) {
      if (y < heroH * 1.2) {
        l.el.style.transform = `translate3d(0, ${(y * l.d).toFixed(1)}px, 0)`;
        if (l.fade) l.el.style.opacity = Math.max(0, 1 - y / (heroH * 0.75)).toFixed(3);
      }
    }
    for (const l of inner) {
      const r = l.box.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) continue;
      const p = (r.top + r.height / 2 - vh / 2) / vh; // -1..1 around centre
      l.el.style.transform = `translate3d(0, ${(p * l.d * r.height * -1).toFixed(1)}px, 0)`;
    }
    for (const l of rollers) {
      const r = l.box.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) continue;
      l.el.style.transform = `translate3d(${((r.top - vh) * l.d).toFixed(1)}px, 0, 0)`;
    }
  }
  const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(frame); } };
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', () => { vh = innerHeight; onScroll(); }, { passive: true });
  reduce.addEventListener('change', () => {
    if (reduce.matches) { $$('[data-depth],[data-depth-inner],[data-roll]').forEach(el => { el.style.transform = ''; el.style.opacity = ''; }); }
    else onScroll();
  });

  /* ---------- Jump links: smooth scroll to the section, clear of the header ---------- */
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href^="#"]');
    if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey) return;
    const id = a.getAttribute('href').slice(1);
    const target = id === 'topo' ? document.body : document.getElementById(id);
    if (!target) return;
    e.preventDefault();
    const top = id === 'topo' ? 0 : target.getBoundingClientRect().top + scrollY;
    // going down the header slides away; going up it comes back and covers ~90px
    const offset = top > scrollY ? 20 : bar.offsetHeight + 20;
    scrollTo({ top: Math.max(0, top - offset), behavior: reduce.matches ? 'auto' : 'smooth' });
    history.replaceState(null, '', id === 'topo' ? location.pathname : '#' + id);
    if (id !== 'topo') { target.setAttribute('tabindex', '-1'); target.focus({ preventScroll: true }); }
  });

  /* ---------- Current section in the nav ---------- */
  const spyLinks = $$('.nav a, .menu a[href^="#"]');
  const wide = matchMedia('(min-width: 900px)');
  const spy = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (!en.isIntersecting) return;
      // on wide screens hours and location sit side by side, so they light up together
      const ids = wide.matches && ['horario', 'local'].includes(en.target.id) ? ['horario', 'local'] : [en.target.id];
      spyLinks.forEach(l => {
        if (ids.includes(l.getAttribute('href').slice(1))) l.setAttribute('aria-current', 'true');
        else l.removeAttribute('aria-current');
      });
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  ['servicos', 'opinioes', 'horario', 'local'].forEach(id => { const el = document.getElementById(id); if (el) spy.observe(el); });

  /* ---------- Copy address ---------- */
  const toastEl = $('#toast'); let toastT;
  function toast(msg) { toastEl.textContent = msg; toastEl.classList.add('show'); clearTimeout(toastT); toastT = setTimeout(() => toastEl.classList.remove('show'), 2200); }
  $('#copyAddr')?.addEventListener('click', async () => {
    const addr = 'Estrada da Senhora da Saúde 58, 8000-500 Faro';
    try { await navigator.clipboard.writeText(addr); }
    catch { const ta = Object.assign(document.createElement('textarea'), { value: addr }); document.body.append(ta); ta.select(); document.execCommand('copy'); ta.remove(); }
    toast(lang === 'en' ? 'Address copied' : 'Morada copiada');
  });

  applyLang();
  frame();
  requestAnimationFrame(() => document.body.classList.add('loaded'));
})();
