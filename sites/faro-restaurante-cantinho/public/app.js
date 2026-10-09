/* Cantinho · Faro — aberto agora, céu de Faro, galeria, reservas por WhatsApp/SMS. Sem dependências. */
(() => {
  'use strict';
  const EN = document.documentElement.lang === 'en';
  const PHONE = '351911013101';
  const LAT = 37.0134441, LON = -7.9332883;
  // Mon–Sat 10:30–23:30, Sunday closed (Google Business Profile). 0 = Sunday.
  const OPEN = 10 * 60 + 30, CLOSE = 23 * 60 + 30;
  const isOpenDay = d => d !== 0;

  const T = EN ? {
    days: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
    open: c => `Open now · until ${c}`, closing: m => `Open · closes in ${m} min`,
    opensToday: h => `Closed · opens today at ${h}`, opensTomorrow: h => `Closed · opens tomorrow at ${h}`,
    opensOn: (d, h) => `Closed on Sundays · opens ${d} at ${h}`,
    today: 'today', sky: { day: 'Daylight in Faro, right now.', golden: 'Late afternoon light in Faro, right now.', dusk: 'Sunset over Faro, right now.', night: 'Night in Faro, right now.' },
    sundayErr: 'We’re closed on Sundays. Please pick another day.', pastErr: 'Please pick today or a later date.',
    nameErr: 'Please tell us your name.', sent: { wa: 'Opening WhatsApp… If nothing happens, call +351 911 013 101.', sms: 'Opening your messages app… If nothing happens, call +351 911 013 101.' },
    msg: (n, d, h, p, o, x) => `Hello Cantinho! I'd like to book a table for ${p} ${p === 1 ? 'person' : 'people'} on ${d} at ${h}${o ? ` (${o})` : ''}.${x ? `\nNotes: ${x}` : ''}\nName: ${n || '…'}`,
    pick: 'Choose a date…'
  } : {
    days: ['domingo', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado'],
    open: c => `Aberto agora · até às ${c}`, closing: m => `Aberto · fecha daqui a ${m} min`,
    opensToday: h => `Fechado · abre hoje às ${h}`, opensTomorrow: h => `Fechado · abre amanhã às ${h}`,
    opensOn: (d, h) => `Fechado ao domingo · abre ${d} às ${h}`,
    today: 'hoje', sky: { day: 'Dia claro em Faro, agora mesmo.', golden: 'Fim de tarde em Faro, agora mesmo.', dusk: 'Pôr do sol em Faro, agora mesmo.', night: 'Noite em Faro, agora mesmo.' },
    sundayErr: 'Ao domingo estamos fechados. Escolha outro dia.', pastErr: 'Escolha hoje ou um dia a seguir.',
    nameErr: 'Diga-nos o seu nome.', sent: { wa: 'A abrir o WhatsApp… Se nada acontecer, ligue 911 013 101.', sms: 'A abrir as mensagens… Se nada acontecer, ligue 911 013 101.' },
    msg: (n, d, h, p, o, x) => `Olá Cantinho! Queria reservar mesa para ${p} ${p === 1 ? 'pessoa' : 'pessoas'} no dia ${d}, às ${h}${o ? ` (${o})` : ''}.${x ? `\nNotas: ${x}` : ''}\nNome: ${n || '…'}`,
    pick: 'Escolha o dia…'
  };

  const pad = n => String(n).padStart(2, '0');
  const hm = m => `${pad(Math.floor(m / 60))}:${pad(m % 60)}`;

  // Faro wall-clock time, whatever the visitor's timezone
  function faroNow() {
    const parts = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Lisbon', weekday: 'short', hour: '2-digit', minute: '2-digit', year: 'numeric', month: '2-digit', day: '2-digit', hourCycle: 'h23' }).formatToParts(new Date());
    const g = t => parts.find(p => p.type === t).value;
    const wd = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(g('weekday'));
    return { day: wd, min: +g('hour') * 60 + +g('minute'), iso: `${g('year')}-${g('month')}-${g('day')}` };
  }

  /* ---------- aberto agora */
  const statusEl = document.querySelector('[data-status]');
  const statusTx = document.querySelector('[data-status-text]');
  function status() {
    const { day, min } = faroNow();
    let open = false, txt;
    if (isOpenDay(day) && min >= OPEN && min < CLOSE) {
      open = true;
      txt = CLOSE - min <= 45 ? T.closing(CLOSE - min) : T.open(hm(CLOSE));
    } else if (isOpenDay(day) && min < OPEN) txt = T.opensToday(hm(OPEN));
    else if (isOpenDay((day + 1) % 7)) txt = T.opensTomorrow(hm(OPEN));
    else txt = T.opensOn(T.days[(day + 2) % 7], hm(OPEN));
    if (statusEl) { statusEl.dataset.open = open ? '1' : '0'; statusTx.textContent = txt; }
    document.querySelectorAll('[data-hours] tr').forEach(tr => {
      const today = +tr.dataset.d === day;
      tr.classList.toggle('today', today);
      const th = tr.querySelector('th');
      if (today) th.dataset.today = T.today; else delete th.dataset.today;
    });
  }

  /* ---------- the sky inside the arch follows the sun over Faro */
  function sunAltitude(date) {
    const rad = Math.PI / 180;
    const d = date / 864e5 - 10957.5;                 // days since J2000
    const g = (357.529 + 0.98560028 * d) * rad;
    const q = 280.459 + 0.98564736 * d;
    const L = (q + 1.915 * Math.sin(g) + 0.020 * Math.sin(2 * g)) * rad;
    const e = (23.439 - 0.00000036 * d) * rad;
    const dec = Math.asin(Math.sin(e) * Math.sin(L));
    const ra = Math.atan2(Math.cos(e) * Math.sin(L), Math.cos(L));
    const gmst = (18.697374558 + 24.06570982441908 * d) % 24;
    const ha = (gmst * 15 + LON) * rad - ra;
    return Math.asin(Math.sin(LAT * rad) * Math.sin(dec) + Math.cos(LAT * rad) * Math.cos(dec) * Math.cos(ha)) / rad;
  }
  const fig = document.querySelector('.hero-arch');
  const skyTx = document.querySelector('[data-sky-text]');
  function sky() {
    if (!fig) return;
    const forced = new URLSearchParams(location.search).get('ceu');   // ?ceu=night for demos
    const a = sunAltitude(Date.now());
    const s = forced || (a > 14 ? 'day' : a > 3 ? 'golden' : a > -6 ? 'dusk' : 'night');
    fig.dataset.sky = s;
    if (skyTx) skyTx.textContent = T.sky[s] || '';
    const orb = fig.querySelector('.orb');
    if (orb) orb.setAttribute('cy', String(Math.round(s === 'day' ? 250 : s === 'golden' ? 330 : s === 'dusk' ? 420 : 260)));
  }

  status(); sky();
  setInterval(() => { status(); sky(); }, 60000);

  /* ---------- gallery: arrows + drag to scroll */
  const strip = document.querySelector('.strip');
  if (strip) {
    const step = () => (strip.querySelector('li')?.getBoundingClientRect().width || 260) + 18;
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    document.querySelectorAll('[data-strip]').forEach(b => b.addEventListener('click', () =>
      strip.scrollBy({ left: step() * +b.dataset.strip, behavior: reduce ? 'auto' : 'smooth' })));
    strip.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); strip.scrollBy({ left: step() * (e.key === 'ArrowRight' ? 1 : -1), behavior: reduce ? 'auto' : 'smooth' }); }
    });
    let x0 = 0, s0 = 0, down = false, moved = false;
    strip.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; down = true; moved = false; x0 = e.clientX; s0 = strip.scrollLeft; });
    window.addEventListener('pointermove', e => {
      if (!down) return;
      const dx = e.clientX - x0;
      if (Math.abs(dx) > 4) { moved = true; strip.classList.add('drag'); }
      strip.scrollLeft = s0 - dx;
    });
    window.addEventListener('pointerup', () => {
      if (!down) return; down = false;
      if (moved) { strip.classList.remove('drag'); const w = step(); strip.scrollTo({ left: Math.round(strip.scrollLeft / w) * w, behavior: reduce ? 'auto' : 'smooth' }); }
    });
  }

  /* ---------- reservas: compõe a mensagem e abre WhatsApp / SMS */
  const form = document.getElementById('res-form');
  if (!form) return;
  const $ = s => form.querySelector(s);
  const sent = $('[data-sent]'), nameErr = $('#r-nome-err');
  const date = $('#r-data'), time = $('#r-hora'), paxOut = $('#r-pax'), ticket = $('[data-ticket]'), err = $('#r-data-err');
  let pax = 2;

  const today = faroNow().iso;
  date.min = today;
  // half-hour slots inside opening hours (last booking an hour before closing); static in the HTML, rebuilt only if missing
  if (!time.options.length) for (let m = OPEN; m <= CLOSE - 60; m += 30) {
    const o = document.createElement('option'); o.value = o.textContent = hm(m);
    if (m === 20 * 60) o.selected = true;
    time.append(o);
  }
  // default date: next open day
  (function () {
    const d = new Date(today + 'T12:00:00');
    if (d.getDay() === 0) d.setDate(d.getDate() + 1);
    date.value = d.toISOString().slice(0, 10);
  })();

  function fmtDate(v) {
    if (!v) return T.pick;
    const d = new Date(v + 'T12:00:00');
    return new Intl.DateTimeFormat(EN ? 'en-GB' : 'pt-PT', { weekday: 'long', day: 'numeric', month: 'long' }).format(d);
  }
  function check() {
    let msg = '';
    if (date.value) {
      const d = new Date(date.value + 'T12:00:00');
      if (date.value < today) msg = T.pastErr;
      else if (d.getDay() === 0) msg = T.sundayErr;
    }
    err.textContent = msg;
    date.setAttribute('aria-invalid', msg ? 'true' : 'false');
    return !msg;
  }
  function text() {
    const n = $('#r-nome').value.trim();
    const o = (form.querySelector('input[name=onde]:checked') || {}).value;
    const any = o && /tanto|no pref/.test(o);
    return T.msg(n, fmtDate(date.value), time.value, pax, any ? '' : o, $('#r-notas').value.trim());
  }
  function render() { ticket.textContent = text(); }
  form.addEventListener('input', e => {
    check(); render();
    if (e.target.id === 'r-nome' && e.target.value.trim()) { e.target.setAttribute('aria-invalid', 'false'); nameErr.textContent = ''; }
    sent.textContent = '';
  });
  form.addEventListener('change', render);
  form.querySelectorAll('[data-pax]').forEach(b => b.addEventListener('click', () => {
    pax = Math.min(20, Math.max(1, pax + +b.dataset.pax)); paxOut.value = paxOut.textContent = pax; render();
  }));
  form.addEventListener('submit', e => {
    e.preventDefault();
    const name = $('#r-nome');
    sent.textContent = '';
    name.setAttribute('aria-invalid', name.value.trim() ? 'false' : 'true');
    nameErr.textContent = name.value.trim() ? '' : T.nameErr;
    if (!name.value.trim()) { name.focus(); return; }
    if (!date.value) { err.textContent = T.pastErr; date.setAttribute('aria-invalid', 'true'); date.focus(); return; }
    if (!check()) { date.focus(); return; }
    const via = (e.submitter && e.submitter.dataset.via) || 'wa';
    sent.textContent = T.sent[via === 'sms' ? 'sms' : 'wa'];
    const body = encodeURIComponent(text());
    location.href = via === 'sms' ? `sms:+${PHONE}?&body=${body}` : `https://wa.me/${PHONE}?text=${body}`;
  });
  render();
})();
