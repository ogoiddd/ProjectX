(() => {
  const doc = document.documentElement;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const PHONE = '351938735167';
  const ADDRESS = 'Taberna Zé-Zé, Travessa do Alportel 15, 8000-448 Faro';

  /* Opening hours (minutes since midnight, Europe/Lisbon). Source: Google listing. [CONFIRMAR COM CLIENTE] */
  const HOURS = { 1: [1080, 1380], 2: [1080, 1380], 3: [1080, 1380], 4: [1080, 1380], 5: [1080, 1380], 6: [1080, 1380] };
  /* Times offered in the table request (UI choice, not a house rule). [CONFIRMAR COM CLIENTE] */
  const SLOTS = ['18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00'];

  /* ---------- i18n ---------- */
  const EN = {
    'skip': 'Skip to content',
    'nav.menu': 'Menu', 'nav.house': 'The house', 'nav.reviews': 'Reviews', 'nav.where': 'Where &amp; when',
    'call.aria': 'Call 938 735 167',
    'hero.eyebrow': 'Family-run taberna · Largo do Carmo, Faro',
    'hero.t1': 'The cataplana', 'hero.t2': 'opens at your table.',
    'hero.lede': 'Ria Formosa seafood in cataplanas and rice pots for two, on Travessa do Alportel in central Faro. The room is small and fills up, especially in summer: ask for a table before you come.',
    'hero.rating': '963 reviews on Google',
    'book.title': 'Ask for a table', 'book.sub': 'Pick, and the message writes itself. Send it by WhatsApp or SMS; the house confirms.',
    'book.people': 'People', 'book.people.aria': 'Number of people', 'book.minus': 'One person fewer', 'book.plus': 'One more person',
    'book.day': 'Day', 'book.time': 'Time', 'book.name': 'Name', 'book.name.ph': 'e.g. Anna Smith…',
    'book.note': 'Note', 'book.opt': '(optional)', 'book.note.ph': 'High chair, allergies, a quiet corner…',
    'book.preview': 'Your message', 'book.wa': 'Send by WhatsApp', 'book.sms': 'By SMS', 'book.call': 'Call',
    'book.fine': 'This site stores and sends nothing: the message only leaves when you send it from your phone. Taberna Zé-Zé uses your name, contact and whatever you write (including allergies, if you mention them) only to handle this booking. On WhatsApp, Meta’s terms also apply. <a href="/privacy">Privacy policy</a>. Your table is only booked once the house replies.',
    'book.todo': 'does 938 735 167 use WhatsApp? Which booking times are accepted?',
    'menu.kicker': 'Menu', 'menu.title': 'From the Ria Formosa into the cataplana.',
    'menu.lede': 'Cataplanas and rice dishes are for two and come to the table in the pot. The seafood rice is served with fried bread on the side.',
    'menu.jump': 'Menu sections',
    'menu.c1': 'Cataplanas', 'menu.c2': 'Rice', 'menu.c3': 'Small plates', 'menu.c4': 'Meat',
    'menu.allergens': '<strong>Allergens:</strong> the cataplanas and rice dishes contain crustaceans and molluscs. The ingredient lists are not the full information on the 14 allergens (EU Reg. 1169/2011), which is available at the restaurant: ask the staff or mention allergies in your table request.',
    'menu.prices': 'Prices at the restaurant, VAT included.',
    'd.noprice': 'price to be confirmed',
    'menu.todo': 'current prices and menu. Dishes taken from the house’s DISH page and from Google reviews.',
    'menu.c1.long': 'Sea and Ria Formosa cataplanas', 'menu.c2.long': 'Seafood rice', 'menu.c3.long': 'Small plates guests rave about', 'menu.c4.long': 'If you’d rather have meat',
    'd.for2': 'for 2', 'd.add': 'Add to my table request', 'd.added': 'Added to the request',
    'd.c1': 'Ria Formosa seafood cataplana with lobster', 'd.c1.i': 'lobster, clams, prawns, cockles, crab claws, mussels in the shell, langoustine, razor clams, tomato, coriander, garlic, onion and pepper',
    'd.c2': 'Ria Formosa seafood cataplana', 'd.c2.i': 'clams, prawns, cockles, crab claws, mussels in the shell, langoustine, razor clams, tomato, coriander, garlic, onion and pepper',
    'd.c3': 'Razor clam cataplana', 'd.c3.i': 'razor clams, potato, clams, prawns, tomato, coriander, garlic, onion, pepper and cockles',
    'd.c4': 'Oyster cataplana, “the pearl of the Ria Formosa”', 'd.c4.i': 'oysters, razor clams, cockles, clams, prawns, tomato, coriander, garlic, onion, pepper and potato',
    'd.a1': 'Seafood rice, Taberna style', 'd.a1.i': 'clams, prawns, razor clams, crab claws, cockles, mussels in the shell, rice, tomato, coriander, garlic, onion and pepper',
    'd.a2': 'Lobster rice', 'd.a2.i': 'lobster, clams, prawns, cockles, mussels, rice, tomato, coriander, garlic, onion and pepper',
    'd.a3': 'Razor clam rice', 'd.a3.i': 'razor clams, rice, tomato, coriander, garlic, onion and pepper',
    'd.p1': 'Razor clams Bulhão Pato (garlic, coriander, olive oil)', 'd.p2': 'Clams', 'd.p3': 'Fried baby squid', 'd.p4': 'Squid and prawn bean stew',
    'd.m1': 'Black Angus T-bone steak, 500&nbsp;g',
    'house.kicker': 'The house', 'house.title': 'A small room, a few steps from the Carmo church.',
    'house.p1': 'Taberna Zé-Zé is a family-run place on Travessa do Alportel, right by Largo do Carmo. From the door to the Carmo church and its Bone Chapel (Capela dos Ossos) it’s about 70 metres.',
    'house.p2': 'Dinner is the thing here: Ria Formosa shellfish, cataplanas and rice in the pot, small plates to share. The room is small, so in summer walk-ins may have to wait.',
    'house.f1.k': 'Service', 'house.f1.v': 'Dinner, Monday to Saturday',
    'house.f2.k': 'Also', 'house.f2.v': 'Takeaway and private events <span class="todo-inline">[CONFIRMAR]</span>',
    'house.f3.k': 'Room', 'house.f3.v': 'Air conditioning <span class="todo-inline">[CONFIRMAR]</span>',
    'house.f4.k': 'Payment', 'house.f4.v': 'Cash and debit card <span class="todo-inline">[CONFIRMAR]</span>',
    'ph.1': 'The cataplana opening at the table, steam and all', 'ph.2': 'The door on Travessa do Alportel, early evening', 'ph.3': 'The room, full, at dinner',
    'rev.kicker': 'Google reviews', 'rev.of': 'from 963 reviews', 'rev.note': 'Quoted exactly as written, in Portuguese, with our translation.', 'rev.all': 'Read them all on Google Maps',
    'rev.tr1': '“We tried the razor clams Bulhão Pato and they were divine. The seafood rice, what a delight, it comes with fried bread on the side that leaves you wanting more. Really good.”',
    'rev.tr2': '“It’s the first time I’ve given full marks. But this place deserves it.”',
    'rev.tr3': '“Highlights were the clams and the fried baby squid: fresh, tasty and spot on.”',
    'rev.tr4': '“Taberna do Zé-Zé, in Faro, is without a doubt the best traditional restaurant in the city.”',
    'rev.tr5': '“Authentic small plates, with fresh ingredients and home-cooked flavour standing out. Lots of traditional fish dishes!”',
    'where.kicker': 'Where &amp; when', 'where.title': 'Travessa do Alportel, 15.', 'where.near': 'by Largo do Carmo, central Faro',
    'hours.caption': 'Opening hours', 'hours.todo': 'hours from Google. The house’s DISH page also lists lunch (12:00–15:00) and closing at 01:00.',
    'd.mon': 'Monday', 'd.tue': 'Tuesday', 'd.wed': 'Wednesday', 'd.thu': 'Thursday', 'd.fri': 'Friday', 'd.sat': 'Saturday', 'd.sun': 'Sunday', 'd.closed': 'Closed',
    'where.dir': 'Get directions', 'where.copy': 'Copy address', 'copied': 'Address copied',
    'where.cap': 'On foot: right by Largo do Carmo, 2 minutes from Praça Silva Porto.',
    'map.title': 'Map of the streets around Taberna Zé-Zé on Travessa do Alportel, by Largo do Carmo and the Carmo church in Faro',
    'foot.addr': 'Address', 'foot.hours': 'Hours', 'foot.hours.v': 'Mon–Sat 18:00–23:00<br>Closed on Sundays', 'foot.more': 'Also on', 'foot.legal': 'Legal',
    'foot.complaints': 'Electronic complaints book (Livro de Reclamações)', 'foot.privlink': 'Privacy policy', 'foot.privhref': '/privacy',
    'foot.ral': 'For consumer disputes, consumers may turn to CIMAAL, the Algarve consumer dispute mediation and arbitration centre (<a href="https://www.consumoalgarve.pt" target="_blank" rel="noopener">consumoalgarve.pt</a>, +351 289 823 135). More information at <a href="https://www.consumidor.gov.pt" target="_blank" rel="noopener">consumidor.gov.pt</a>.',
    'foot.privacy': 'This site uses no cookies, no visitor tracking and stores no personal data. Map © OpenStreetMap.', 'foot.top': 'Back to top',
    'dock.label': 'Quick actions', 'dock.book': 'Ask for a table', 'dock.call': 'Call', 'dock.dir': 'Directions'
  };
  const PT = {};
  $$('[data-i18n]').forEach(el => { PT[el.dataset.i18n] = el.innerHTML; });
  $$('[data-i18n-aria]').forEach(el => { PT[el.dataset.i18nAria] = el.getAttribute('aria-label'); });
  $$('[data-i18n-ph]').forEach(el => { PT[el.dataset.i18nPh] = el.placeholder; });
  $$('[data-i18n-href]').forEach(el => { PT[el.dataset.i18nHref] = el.getAttribute('href'); });
  PT['d.added'] = 'Junto ao pedido de mesa';
  PT['copied'] = 'Morada copiada';

  let lang = 'pt';
  const q = /[?&]lang=(pt|en)\b/.exec(location.search);
  try {
    const saved = q ? q[1] : localStorage.getItem('lang');
    if (saved === 'en' || saved === 'pt') lang = saved;
    else if (!/^pt\b/i.test(navigator.language || 'pt')) lang = 'en';
  } catch { if (q) lang = q[1]; }
  const canon = $('link[rel="canonical"]'), canonBase = canon && canon.href.split('?')[0];
  const t = (k) => (lang === 'en' ? EN : PT)[k] ?? PT[k];

  function applyLang() {
    doc.lang = lang === 'en' ? 'en' : 'pt-PT';
    $$('[data-i18n]').forEach(el => { const v = t(el.dataset.i18n); if (v != null) el.innerHTML = v; });
    $$('[data-i18n-aria]').forEach(el => { const v = t(el.dataset.i18nAria); if (v != null) el.setAttribute('aria-label', v); });
    $$('[data-i18n-ph]').forEach(el => { const v = t(el.dataset.i18nPh); if (v != null) el.placeholder = v; });
    $$('[data-i18n-href]').forEach(el => { const v = t(el.dataset.i18nHref); if (v != null) el.setAttribute('href', v); });
    if (canon) canon.href = canonBase + (lang === 'en' ? '?lang=en' : '');
    $$('.q-tr').forEach(el => { el.hidden = lang !== 'en'; });
    $$('.add').forEach(b => { b.firstElementChild.textContent = t(b.getAttribute('aria-pressed') === 'true' ? 'd.added' : 'd.add'); });
    const b = $('#lang');
    b.innerHTML = lang === 'en' ? 'PT<span class="sr" lang="pt-PT"> · Mudar para português</span>' : 'EN<span class="sr" lang="en"> · Switch to English</span>';
    renderDays(); updateStatus(); markToday(); renderMessage();
  }
  $('#lang').addEventListener('click', () => {
    lang = lang === 'en' ? 'pt' : 'en';
    try { localStorage.setItem('lang', lang); } catch {}
    try { const u = new URL(location.href); u.searchParams.delete('lang'); if (lang === 'en') u.searchParams.set('lang', 'en'); history.replaceState(null, '', u); } catch {}
    if (document.startViewTransition && !matchMedia('(prefers-reduced-motion: reduce)').matches) document.startViewTransition(applyLang);
    else applyLang();
  });

  /* ---------- Lisbon clock ---------- */
  function lisbon(date = new Date()) {
    const p = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Lisbon', year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', hourCycle: 'h23' }).formatToParts(date);
    const g = (k) => +p.find(x => x.type === k).value;
    const y = g('year'), m = g('month'), d = g('day');
    return { y, m, d, day: new Date(Date.UTC(y, m - 1, d)).getUTCDay(), mins: g('hour') * 60 + g('minute') };
  }
  const hhmm = (m) => `${String(Math.floor(m / 60) % 24).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`;
  const DAYS = { pt: ['domingo', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado'], en: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'] };
  const DAYS_SHORT = { pt: ['dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sáb'], en: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'] };

  /* ---------- Open now ---------- */
  function updateStatus() {
    const { day, mins } = lisbon();
    const h = HOURS[day], en = lang === 'en';
    const box = $('#status'), out = $('#statusText');
    const open = h && mins >= h[0] && mins < h[1];
    let msg;
    if (open) {
      const left = h[1] - mins;
      msg = left <= 45
        ? (en ? `Open · kitchen closing soon (${hhmm(h[1])})` : `Aberto · fecha às ${hhmm(h[1])}, falta pouco`)
        : (en ? `Open now · until ${hhmm(h[1])}` : `Aberto agora · até às ${hhmm(h[1])}`);
    } else {
      let d = day, i = 0;
      if (!(h && mins < h[0])) { do { d = (d + 1) % 7; i++; } while (!HOURS[d] && i < 8); }
      const when = i === 0 ? (en ? 'today' : 'hoje') : i === 1 ? (en ? 'tomorrow' : 'amanhã') : (en ? 'on ' + DAYS.en[d] : DAYS.pt[d]);
      msg = en ? `Closed now · opens ${when} at ${hhmm(HOURS[d][0])}` : `Fechado agora · abre ${when} às ${hhmm(HOURS[d][0])}`;
    }
    box.classList.toggle('is-open', !!open); box.classList.toggle('is-closed', !open);
    out.textContent = msg;
  }
  function markToday() {
    const { day } = lisbon();
    $$('#hoursBody tr').forEach(tr => {
      const on = +tr.dataset.d === day;
      tr.classList.toggle('today', on);
      if (on) tr.querySelector('th').dataset.today = lang === 'en' ? 'today' : 'hoje';
    });
  }

  /* ---------- Table request ---------- */
  const form = $('#book'), daysBox = $('#days'), timesBox = $('#times');
  const people = $('#people'), nameI = $('#name'), noteI = $('#note');
  const wanted = new Set();
  let selDay = null, selTime = '20:00';

  function dayList() {
    const now = lisbon(), list = [];
    for (let i = 0; i < 10; i++) {
      const dt = new Date(Date.UTC(now.y, now.m - 1, now.d + i));
      const wd = dt.getUTCDay();
      const openSlots = HOURS[wd] ? SLOTS.filter(s => i > 0 || toMin(s) >= now.mins + 30) : [];
      list.push({ i, wd, d: dt.getUTCDate(), m: dt.getUTCMonth() + 1, key: dt.toISOString().slice(0, 10), closed: !HOURS[wd], full: HOURS[wd] && !openSlots.length });
    }
    return list;
  }
  const toMin = (s) => +s.slice(0, 2) * 60 + +s.slice(3);
  function dayLabel(x) {
    const en = lang === 'en';
    if (x.i === 0) return en ? 'Today' : 'Hoje';
    if (x.i === 1) return en ? 'Tomorrow' : 'Amanhã';
    const s = DAYS_SHORT[lang === 'en' ? 'en' : 'pt'][x.wd];
    return s.charAt(0).toUpperCase() + s.slice(1);
  }
  function renderDays() {
    const list = dayList();
    if (!selDay || !list.find(x => x.key === selDay && !x.closed && !x.full)) selDay = (list.find(x => !x.closed && !x.full) || list[0]).key;
    daysBox.setAttribute('aria-label', lang === 'en' ? 'Day' : 'Dia');
    daysBox.innerHTML = list.map(x => {
      const sub = x.closed ? (lang === 'en' ? 'closed' : 'fechado') : `${x.d}/${x.m}`;
      return `<label class="chip"><input type="radio" name="day" value="${x.key}"${x.key === selDay ? ' checked' : ''}${x.closed || x.full ? ' disabled' : ''}><span>${dayLabel(x)}<small>${sub}</small></span></label>`;
    }).join('');
    renderTimes();
  }
  function renderTimes() {
    const list = dayList(), x = list.find(y => y.key === selDay);
    const now = lisbon();
    const ok = (s) => x && !x.closed && (x.i > 0 || toMin(s) >= now.mins + 30);
    if (!ok(selTime)) selTime = SLOTS.find(ok) || null;
    timesBox.innerHTML = SLOTS.map(s => `<label class="chip"><input type="radio" name="time" value="${s}"${s === selTime ? ' checked' : ''}${ok(s) ? '' : ' disabled'}><span>${s}</span></label>`).join('');
    const hint = $('#timeHint');
    hint.textContent = x && x.i === 0 && SLOTS.some(s => !ok(s))
      ? (lang === 'en' ? 'Earlier times today have passed. For tonight at short notice, calling is quickest.' : 'As horas mais cedo de hoje já passaram. Para hoje em cima da hora, ligar é mais rápido.')
      : '';
    renderMessage();
  }
  form.addEventListener('submit', e => e.preventDefault());
  daysBox.addEventListener('change', e => { selDay = e.target.value; renderTimes(); bumpTicket(); });
  timesBox.addEventListener('change', e => { selTime = e.target.value; renderMessage(); });
  $$('.step').forEach(b => b.addEventListener('click', () => {
    const v = Math.min(20, Math.max(1, (+people.value || 2) + +b.dataset.step));
    people.value = v; renderMessage();
  }));
  [people, nameI, noteI].forEach(el => el.addEventListener('input', renderMessage));
  people.addEventListener('change', () => { people.value = Math.min(20, Math.max(1, Math.round(+people.value) || 2)); renderMessage(); });

  function buildMessage() {
    const n = Math.min(20, Math.max(1, Math.round(+people.value) || 2));
    const x = dayList().find(y => y.key === selDay);
    const date = x ? `${x.d}/${x.m}` : '';
    const name = nameI.value.trim(), note = noteI.value.trim();
    const dishes = [...wanted];
    const L = [];
    if (lang === 'en') {
      L.push('Hello! I’d like to ask for a table at Taberna Zé-Zé. (Pedido de mesa)');
      L.push(`• ${n} ${n === 1 ? 'person' : 'people'} (${n} ${n === 1 ? 'pessoa' : 'pessoas'})`);
      if (x) L.push(`• ${DAYS.en[x.wd]} ${date} (${DAYS.pt[x.wd]}), ${selTime || '—'}`);
      if (name) L.push(`• Name / Nome: ${name}`);
      if (dishes.length) L.push(`• We’d like / Gostávamos de: ${dishes.join(', ')}`);
      if (note) L.push(`• Note / Nota: ${note}`);
      L.push('Thank you! / Obrigado!');
    } else {
      L.push('Olá! Queria pedir mesa na Taberna Zé-Zé.');
      L.push(`• ${n} ${n === 1 ? 'pessoa' : 'pessoas'}`);
      if (x) L.push(`• ${x.i === 0 ? 'Hoje, ' : x.i === 1 ? 'Amanhã, ' : ''}${DAYS.pt[x.wd]} ${date}, às ${selTime || '—'}`);
      if (name) L.push(`• Nome: ${name}`);
      if (dishes.length) L.push(`• Gostávamos de: ${dishes.join(', ')}`);
      if (note) L.push(`• Nota: ${note}`);
      L.push('Obrigado!');
    }
    return L.join('\n');
  }
  function renderMessage() {
    if (!form) return;
    const msg = buildMessage();
    $('#preview').textContent = msg;
    const enc = encodeURIComponent(msg);
    $('#sendWa').href = `https://wa.me/${PHONE}?text=${enc}`;
    $('#sendSms').href = `sms:+${PHONE}?&body=${enc}`;
  }
  function bumpTicket() {
    const x = dayList().find(y => y.key === selDay);
    if (x) $('#ticketNo').textContent = `${String(x.d).padStart(2, '0')}·${String(x.m).padStart(2, '0')}`;
  }

  /* menu -> request */
  const comanda = $('#mesa');
  $$('.add').forEach(b => {
    b.setAttribute('aria-pressed', 'false');
    b.addEventListener('click', () => {
      const d = b.dataset.dish, on = !wanted.has(d);
      on ? wanted.add(d) : wanted.delete(d);
      b.setAttribute('aria-pressed', String(on));
      b.firstElementChild.textContent = t(on ? 'd.added' : 'd.add');
      renderMessage();
      comanda.classList.remove('bump'); void comanda.offsetWidth; comanda.classList.add('bump');
    });
  });

  /* copy address */
  $('#copyAddr').addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(ADDRESS); $('#copied').textContent = t('copied'); setTimeout(() => { $('#copied').textContent = ''; }, 2500); } catch {}
  });

  applyLang(); bumpTicket();
  doc.classList.remove('i18n-wait');
  setInterval(() => { updateStatus(); markToday(); }, 60000);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) { updateStatus(); renderTimes(); } });
})();
