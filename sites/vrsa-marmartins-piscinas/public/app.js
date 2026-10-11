// Mar Martins · interações da demo. Sem dependências, sem cookies, sem pedidos a terceiros.
(() => {
  'use strict';

  // [CONFIRMAR COM CLIENTE] Preencher quando houver contactos confirmados.
  // wa: número internacional só com dígitos (ex.: '351912345678'); email: endereço.
  const CONTACT = { wa: '', email: '' };

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fmt = (n, d = 1) => n.toLocaleString('pt-PT', { minimumFractionDigits: d, maximumFractionDigits: d });

  /* ---------- antes / depois ---------- */
  const compare = $('[data-compare]');
  if (compare) {
    const before = $('[data-before]', compare);
    const handle = $('[data-handle]', compare);
    const range = $('[data-compare-range]', compare);
    const set = (v) => {
      before.style.clipPath = `inset(0 ${100 - v}% 0 0)`;
      handle.style.left = v + '%';
    };
    range.addEventListener('input', () => set(+range.value));
    set(+range.value);
  }

  /* ---------- simulador ---------- */
  const sim = $('[data-sim]');
  const state = { len: 8, wid: 4, min: 1.2, max: 1.8 };
  if (sim) {
    const inputs = { len: $('#s-len'), wid: $('#s-wid'), min: $('#s-min'), max: $('#s-max') };
    const pool = $('[data-sim-pool]');
    const label = $('[data-sim-label]');
    const grid = $('[data-sim-grid]');
    const W = 400, H = 240, SCALE = 21, TOP = 18;

    // grelha de 1 m
    const NS = 'http://www.w3.org/2000/svg';
    for (let x = W / 2 % SCALE; x < W; x += SCALE) {
      const p = document.createElementNS(NS, 'path'); p.setAttribute('d', `M${x.toFixed(1)} 0V${H}`); grid.append(p);
    }
    for (let y = TOP; y < H; y += SCALE) {
      const p = document.createElementNS(NS, 'path'); p.setAttribute('d', `M0 ${y}H${W}`); grid.append(p);
    }

    const update = (changed) => {
      for (const k in inputs) state[k] = parseFloat(inputs[k].value);
      // a parte funda nunca é mais rasa que a parte rasa
      if (state.max < state.min) {
        if (changed === 'min') { state.max = state.min; inputs.max.value = state.min; }
        else { state.min = state.max; inputs.min.value = state.max; }
      }
      const { len, wid, min, max } = state;
      const avg = (min + max) / 2;
      const vol = len * wid * avg;
      const area = len * wid;
      const perim = 2 * (len + wid);
      const floor = Math.hypot(len, max - min) * wid;
      const lining = floor + wid * (min + max) + len * (min + max);

      $('[data-out="len"]').textContent = fmt(len) + ' m';
      $('[data-out="wid"]').textContent = fmt(wid) + ' m';
      $('[data-out="min"]').textContent = fmt(min) + ' m';
      $('[data-out="max"]').textContent = fmt(max) + ' m';
      $('[data-stat="vol"]').textContent = fmt(vol);
      $('[data-stat="litres"]').textContent = Math.round(vol * 1000).toLocaleString('pt-PT') + ' L';
      $('[data-stat="area"]').textContent = fmt(area);
      $('[data-stat="perim"]').textContent = fmt(perim);
      $('[data-stat="lining"]').textContent = '≈ ' + Math.round(lining);

      const pw = len * SCALE, ph = wid * SCALE;
      pool.setAttribute('x', ((W - pw) / 2).toFixed(1));
      pool.setAttribute('y', (TOP + (H - 40 - TOP - ph) / 2 + 2).toFixed(1));
      pool.setAttribute('width', pw.toFixed(1));
      pool.setAttribute('height', ph.toFixed(1));
      label.textContent = `${fmt(len)} × ${fmt(wid)} m · escala 1 quadrado = 1 m`;

      // o corte do topo acompanha as medidas
      const dims = { len: fmt(len) + ' m', min: fmt(min) + ' m', max: fmt(max) + ' m' };
      $$('[data-dim]').forEach((t) => { t.textContent = dims[t.dataset.dim]; });
    };
    for (const k in inputs) inputs[k].addEventListener('input', () => update(k));
    update();

    $('[data-sim-send]').addEventListener('click', () => {
      const { len, wid, min, max } = state;
      const vol = len * wid * (min + max) / 2;
      $('#q-med').value = `${fmt(len)} × ${fmt(wid)} m, profundidade ${fmt(min)}–${fmt(max)} m (≈ ${fmt(vol)} m³)`;
      const nova = $('input[name="tipo"][value="Piscina nova"]');
      if (nova) nova.checked = true;
      setTimeout(() => $('#q-nome').focus({ preventScroll: true }), reduce ? 0 : 600);
    });
  }

  /* ---------- separadores do processo ---------- */
  const tabs = $('[data-tabs]');
  if (tabs) {
    const btns = $$('[role="tab"]', tabs);
    const select = (b) => {
      btns.forEach((x) => {
        const on = x === b;
        x.setAttribute('aria-selected', on);
        x.tabIndex = on ? 0 : -1;
        $('#' + x.getAttribute('aria-controls')).hidden = !on;
      });
    };
    btns.forEach((b, i) => {
      b.addEventListener('click', () => select(b));
      b.addEventListener('keydown', (e) => {
        const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        const n = btns[(i + d + btns.length) % btns.length];
        select(n); n.focus();
      });
    });
  }

  /* ---------- atalhos dos serviços ---------- */
  $$('[data-pick]').forEach((a) => a.addEventListener('click', () => {
    const r = $(`input[name="tipo"][value="${a.dataset.pick}"]`);
    if (r) r.checked = true;
  }));

  /* ---------- pedido de orçamento ---------- */
  const form = $('[data-quote]');
  if (form) {
    let via = 'wa';
    $$('[data-send]', form).forEach((b) => b.addEventListener('click', () => { via = b.dataset.send; }));

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const f = new FormData(form);
      const nome = (f.get('nome') || '').trim();
      const tel = (f.get('tel') || '').trim();
      const okNome = nome.length > 1;
      const okTel = tel.replace(/\D/g, '').length >= 9;
      $('#q-nome').setAttribute('aria-invalid', !okNome);
      $('#q-tel').setAttribute('aria-invalid', !okTel);
      $('[data-err]').hidden = okNome && okTel;
      if (!okNome || !okTel) { (okNome ? $('#q-tel') : $('#q-nome')).focus(); return; }

      const opt = (k, v) => ((v || '').trim() ? `${k}: ${v.trim()}` : null);
      const lines = [
        'Olá, Mar Martins. Gostava de pedir um orçamento.',
        '',
        `Pedido: ${f.get('tipo')}`,
        opt('Localidade', f.get('loc')),
        opt('Medidas', f.get('medidas')),
        opt('Notas', f.get('msg')),
        '',
        `${nome} · ${tel}`,
      ].filter((l) => l !== null);
      const text = lines.join('\n');

      $('[data-preview]').hidden = false;
      $('[data-preview-text]').textContent = text;

      const url = via === 'wa' && CONTACT.wa
        ? `https://wa.me/${CONTACT.wa}?text=${encodeURIComponent(text)}`
        : via === 'email' && CONTACT.email
          ? `mailto:${CONTACT.email}?subject=${encodeURIComponent('Pedido de orçamento · ' + f.get('tipo'))}&body=${encodeURIComponent(text)}`
          : '';
      $('[data-preview-note]').hidden = !!url;
      if (url) location.href = url;
    });
  }

  /* ---------- botão flutuante ---------- */
  const fab = $('[data-fab]');
  const orc = $('#orcamento');
  const hero = $('.hero');
  if (fab && 'IntersectionObserver' in window) {
    const vis = new Map();
    const io = new IntersectionObserver((es) => {
      es.forEach((e) => vis.set(e.target, e.isIntersecting));
      fab.classList.toggle('is-hidden', [...vis.values()].some(Boolean));
    });
    io.observe(orc); io.observe(hero);
  }

  /* ---------- entrada das secções ---------- */
  if (!reduce && 'IntersectionObserver' in window) {
    const els = $$('.sec-head, .compare, .medir-grid, .tabs, .serv, .zona, .orcamento');
    els.forEach((el) => el.classList.add('reveal'));
    const io = new IntersectionObserver((es) => es.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
    }), { rootMargin: '0px 0px -8% 0px' });
    els.forEach((el) => io.observe(el));
  }
})();
