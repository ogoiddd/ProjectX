// zarpa.pt: maquete ao vivo no topo, rota de 14 dias e pedido de maquete.
(() => {
  'use strict';

  // Contactos para onde vão os pedidos. WhatsApp vazio = botão escondido.
  const CONTACTO = {
    email: 'diogo@zarpa.pt',   // [CONFIRMAR] caixa do Diogo em zarpa.pt
    whatsapp: '',              // [CONFIRMAR] ex.: '3519XXXXXXXX'
  };

  const ESP = {
    dentaria: { nome: 'Medicina dentária', servicos: ['Implantes', 'Ortodontia', 'Higiene oral', 'Branqueamento'] },
    fisioterapia: { nome: 'Fisioterapia', servicos: ['Coluna e ombro', 'Lesões no desporto', 'Pós-cirurgia', 'Pilates clínico'] },
    estetica: { nome: 'Estética', servicos: ['Rosto', 'Depilação a laser', 'Corpo', 'Massagem'] },
    veterinaria: { nome: 'Clínica veterinária', servicos: ['Consultas', 'Vacinação', 'Cirurgia', 'Urgências'] },
  };

  const $ = (s, el = document) => el.querySelector(s);
  const tidy = (s) => s.replace(/\s+/g, ' ').trim();

  /* ---------- maquete ao vivo ---------- */
  const phone = $('#phone');
  const tNome = $('#t-nome');
  const tCidade = $('#t-cidade');
  const espAtual = () => ($('input[name="esp"]:checked') || {}).value || 'dentaria';

  function iniciais(nome) {
    const palavras = nome.split(' ').filter((p) => p.length > 2 || /^[A-ZÁÉÍÓÚ]/.test(p));
    const letras = (palavras.length ? palavras : nome.split(' ')).slice(0, 2).map((p) => p[0]);
    return letras.join('').toUpperCase() || 'A';
  }

  // Horário de exemplo: seg–sex 9h–19h, sáb 9h–13h, hora de Lisboa.
  function horario() {
    const agora = new Date(new Date().toLocaleString('en-US', { timeZone: 'Europe/Lisbon' }));
    const d = agora.getDay();
    const h = agora.getHours() + agora.getMinutes() / 60;
    const fecho = d === 6 ? 13 : 19;
    if (d >= 1 && d <= 6 && h >= 9 && h < fecho) return [true, `Aberto agora, até às ${fecho}:00`];
    if (d >= 1 && d <= 6 && h < 9) return [false, 'Abre hoje às 9:00'];
    if (d >= 1 && d <= 5) return [false, 'Abre amanhã às 9:00'];
    return [false, 'Abre segunda às 9:00'];
  }

  function render() {
    if (!phone) return;
    const nome = tidy(tNome.value) || 'A sua clínica';
    const cidade = tidy(tCidade.value) || 'Faro';
    const esp = espAtual();
    phone.dataset.esp = esp;
    $('#m-nome').textContent = nome;
    $('#m-nome-top').textContent = nome;
    $('#m-ini').textContent = iniciais(nome);
    $('#m-sub').textContent = `${ESP[esp].nome} em ${cidade}`;
    $('#m-servicos').replaceChildren(...ESP[esp].servicos.map((s) => {
      const li = document.createElement('li');
      li.textContent = s;
      return li;
    }));
  }

  if (phone) {
    const [aberto, texto] = horario();
    $('#m-aberto').textContent = texto;
    phone.classList.toggle('fechado', !aberto);
    $('#try').addEventListener('input', render);
    $('#try').addEventListener('change', render);
    render();
  }

  /* ---------- do topo para o pedido ---------- */
  const form = $('#form');
  $('#try')?.addEventListener('submit', (e) => {
    e.preventDefault();
    $('#f-nome').value = tidy(tNome.value);
    $('#f-cidade').value = tidy(tCidade.value);
    $('#f-esp').value = espAtual();
    const alvo = $('#f-nome').value ? ($('#f-cidade').value ? $('#f-contacto') : $('#f-cidade')) : $('#f-nome');
    $('#pedir').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
    setTimeout(() => alvo.focus({ preventScroll: true }), 450);
  });

  /* ---------- rota de 14 dias ---------- */
  const sec = $('#como');
  const route = $('#route');
  const lista = $('.steps');
  const steps = [...document.querySelectorAll('.step')];
  let pedido = false;

  function rota() {
    pedido = false;
    // 0 quando os passos entram a 90% do ecrã, 1 quando o último passo sobe a 60%.
    const r = lista.getBoundingClientRect();
    const vh = innerHeight;
    const p = Math.min(1, Math.max(0, (vh * 0.9 - r.top) / Math.max(1, r.height + vh * 0.3)));
    route.style.setProperty('--p', p.toFixed(4));
    const dia = p * 14;
    steps.forEach((s) => s.classList.toggle('on', dia >= Number(s.dataset.day) - 0.01));
  }

  if (sec && route) {
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
      route.style.setProperty('--p', '1');
      steps.forEach((s) => s.classList.add('on'));
    } else {
      const pedir = () => { if (!pedido) { pedido = true; requestAnimationFrame(rota); } };
      addEventListener('scroll', pedir, { passive: true });
      addEventListener('resize', pedir);
      rota();
    }
  }

  /* ---------- pedido de maquete ---------- */
  if (!form) return;
  const err = $('#f-err');
  const wa = $('#f-wa');
  const ESP_NOME = { dentaria: 'dentária', fisioterapia: 'fisioterapia', estetica: 'estética', veterinaria: 'veterinária', outra: 'outra' };

  function mensagem() {
    const v = (id) => tidy($(id).value);
    const linhas = [
      'Bom dia, Diogo.',
      '',
      `Gostava de ver a maquete do site da ${v('#f-nome')}, em ${v('#f-cidade')} (${ESP_NOME[$('#f-esp').value]}).`,
    ];
    if (v('#f-link')) linhas.push(`Site atual ou ficha do Google: ${v('#f-link')}`);
    linhas.push(`Contacto para a maquete: ${v('#f-contacto')}`);
    linhas.push('', 'Obrigado,', v('#f-pessoa') || '');
    return linhas.join('\n').trim();
  }

  function valido() {
    const faltam = [];
    for (const [id, nome] of [['#f-nome', 'o nome da clínica'], ['#f-cidade', 'a cidade'], ['#f-contacto', 'um email ou telefone']]) {
      const el = $(id);
      const vazio = !tidy(el.value);
      el.setAttribute('aria-invalid', vazio ? 'true' : 'false');
      if (vazio) faltam.push(nome);
    }
    if (faltam.length) {
      const lista = faltam.length > 1 ? `${faltam.slice(0, -1).join(', ')} e ${faltam.at(-1)}` : faltam[0];
      err.textContent = `Falta ${lista}.`;
      err.hidden = false;
      $(`[aria-invalid="true"]`, form).focus();
      return false;
    }
    err.hidden = true;
    return true;
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!valido()) return;
    const assunto = `Maquete: ${tidy($('#f-nome').value)}`;
    location.href = `mailto:${CONTACTO.email}?subject=${encodeURIComponent(assunto)}&body=${encodeURIComponent(mensagem())}`;
  });

  if (CONTACTO.whatsapp) {
    wa.hidden = false;
    wa.target = '_blank';
    wa.rel = 'noopener';
    wa.addEventListener('click', (e) => {
      if (!valido()) { e.preventDefault(); return; }
      wa.href = `https://wa.me/${CONTACTO.whatsapp}?text=${encodeURIComponent(mensagem())}`;
    });
  }

  form.addEventListener('input', (e) => {
    if (e.target.getAttribute('aria-invalid') === 'true' && tidy(e.target.value)) e.target.setAttribute('aria-invalid', 'false');
  });
})();
