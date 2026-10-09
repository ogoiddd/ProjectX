/* Arealauto · comportamento do site (sem dependências) */
(() => {
  "use strict";

  // ---------- configuração (confirmar com o cliente) ----------
  const CONFIG = {
    phone: "+351289882080",
    // [CONFIRMAR COM CLIENTE] número de telemóvel com WhatsApp da oficina, só dígitos com indicativo (ex.: "3519XXXXXXXX").
    // Enquanto for null, o WhatsApp abre com a mensagem pronta e o cliente escolhe o contacto.
    whatsapp: null,
    email: "arealauto@iol.pt", // [CONFIRMAR] email listado no diretório autonews.pt
    founded: { y: 1996, m: 6, d: 14 },
    // minutos desde a meia-noite; 1 = segunda … 5 = sexta
    hours: { 1: [[510, 750], [840, 1080]], 2: [[510, 750], [840, 1080]], 3: [[510, 750], [840, 1080]], 4: [[510, 750], [840, 1080]], 5: [[510, 750], [840, 1080]] },
  };

  const DAYS = ["domingo", "segunda", "terça", "quarta", "quinta", "sexta", "sábado"];
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const pad = (n) => String(n).padStart(2, "0");
  const hhmm = (m) => `${pad(Math.floor(m / 60))}:${pad(m % 60)}`;

  // ---------- hora de Lisboa ----------
  const fmt = new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Lisbon", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", hourCycle: "h23", weekday: "short" });
  function lisbonNow() {
    const p = Object.fromEntries(fmt.formatToParts(new Date()).map((x) => [x.type, x.value]));
    const y = +p.year, mo = +p.month, d = +p.day;
    const dow = new Date(Date.UTC(y, mo - 1, d)).getUTCDay();
    return { y, mo, d, dow, min: +p.hour * 60 + +p.minute };
  }

  // ---------- feriados (nacionais + 7 set., dia de Faro) ----------
  function easter(y) {
    const a = y % 19, b = Math.floor(y / 100), c = y % 100, d = Math.floor(b / 4), e = b % 4,
      f = Math.floor((b + 8) / 25), g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30,
      i = Math.floor(c / 4), k = c % 4, l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451),
      month = Math.floor((h + l - 7 * m + 114) / 31), day = ((h + l - 7 * m + 114) % 31) + 1;
    return Date.UTC(y, month - 1, day);
  }
  const holidayCache = {};
  function holidays(y) {
    if (holidayCache[y]) return holidayCache[y];
    const key = (t) => new Date(t).toISOString().slice(5, 10);
    const e = easter(y), D = 864e5;
    const fixed = ["01-01", "04-25", "05-01", "06-10", "08-15", "09-07", "10-05", "11-01", "12-01", "12-08", "12-25"];
    return (holidayCache[y] = new Set([...fixed, key(e - 2 * D), key(e), key(e + 60 * D)]));
  }
  const isHoliday = (y, mo, d) => holidays(y).has(`${pad(mo)}-${pad(d)}`);

  function addDays(y, mo, d, n) {
    const t = new Date(Date.UTC(y, mo - 1, d + n));
    return { y: t.getUTCFullYear(), mo: t.getUTCMonth() + 1, d: t.getUTCDate(), dow: t.getUTCDay() };
  }
  function slotsFor(day) { return isHoliday(day.y, day.mo, day.d) ? [] : CONFIG.hours[day.dow] || []; }

  function nextOpening(now) {
    for (let i = 0; i < 14; i++) {
      const day = addDays(now.y, now.mo, now.d, i);
      for (const [o] of slotsFor(day)) {
        if (i > 0 || o > now.min) return { i, day, o };
      }
    }
    return null;
  }

  function whenLabel(n) {
    if (!n) return "";
    if (n.i === 0) return `hoje às ${hhmm(n.o)}`;
    if (n.i === 1) return `amanhã às ${hhmm(n.o)}`;
    return `${DAYS[n.day.dow]} às ${hhmm(n.o)}`;
  }

  function status() {
    const now = lisbonNow();
    const today = { y: now.y, mo: now.mo, d: now.d, dow: now.dow };
    const holiday = isHoliday(now.y, now.mo, now.d);
    const slots = slotsFor(today);
    const nxt = nextOpening(now);
    for (const [o, c] of slots) {
      if (now.min >= o && now.min < c) {
        const left = c - now.min;
        const lunch = c === 750;
        if (left <= 30) return { state: "soon", text: `Aberto · ${lunch ? "fecha para almoço" : "fecha"} às ${hhmm(c)}`, short: `Até ${hhmm(c)}`, stamp: "ABERTO", now };
        return { state: "open", text: `Aberto agora · ${lunch ? "até às 12:30, reabre às 14:00" : "até às 18:00"}`, short: "Aberto", stamp: "ABERTO", now };
      }
    }
    if (slots.length && now.min >= 750 && now.min < 840) return { state: "lunch", text: "Pausa de almoço · reabre às 14:00", short: "Almoço", stamp: "ALMOÇO", now };
    if (holiday) return { state: "holiday", text: `Feriado · abre ${whenLabel(nxt)}`, short: "Feriado", stamp: "FERIADO", now };
    return { state: "closed", text: `Fechado · abre ${whenLabel(nxt)}`, short: "Fechado", stamp: "FECHADO", now };
  }

  function paintStatus() {
    const s = status();
    $$("[data-status]").forEach((el) => (el.dataset.state = s.state));
    $$("[data-status-text]").forEach((el) => (el.textContent = s.text));
    $$("[data-status-short]").forEach((el) => (el.textContent = s.short));
    const stamp = $("[data-status-stamp]");
    if (stamp) { stamp.textContent = s.stamp; stamp.classList.toggle("is-open", s.state === "open" || s.state === "soon"); }
    const today = $("[data-today]");
    if (today) today.textContent = `${DAYS[s.now.dow]}, ${pad(s.now.d)}.${pad(s.now.mo)}`;
    $$(".week tr[data-dow]").forEach((tr) => tr.classList.toggle("is-today", +tr.dataset.dow === s.now.dow));
    return s.now;
  }
  const now0 = paintStatus();
  setInterval(paintStatus, 30_000);

  // ---------- anos de casa ----------
  const f = CONFIG.founded;
  const years = now0.y - f.y - (now0.mo < f.m || (now0.mo === f.m && now0.d < f.d) ? 1 : 0);
  $$("[data-years]").forEach((el) => (el.textContent = years));
  $$("[data-this-year]").forEach((el) => (el.textContent = now0.y));

  // ---------- conta-quilómetros 1996 → ano atual ----------
  const odo = $("[data-odo]");
  if (odo) {
    const target = String(now0.y).padStart(4, "0").split("");
    const digits = $$(".odo-d", odo);
    digits.forEach((el, i) => {
      const from = +el.dataset.from, to = +target[i];
      // fita: de "from" até "to"; os dígitos que mudam dão uma volta extra, o último (vermelho) dá duas
      const k = (to - from + 10) % 10;
      const total = k + (i === digits.length - 1 ? 20 : k ? 10 : 0);
      const seq = [...Array(total + 1)].map((_, j) => (from + j) % 10);
      const strip = document.createElement("span");
      strip.className = "odo-strip";
      strip.innerHTML = seq.map((x) => `<span>${x}</span>`).join("");
      el.append(strip);
      el.dataset.steps = seq.length - 1;
    });
    const roll = () => digits.forEach((el, i) => {
      const strip = $(".odo-strip", el);
      strip.style.transitionDelay = `${(digits.length - 1 - i) * 0.12}s`;
      strip.style.transform = `translateY(${-1.1 * +el.dataset.steps}em)`;
    });
    if (reduced || !("IntersectionObserver" in window)) {
      digits.forEach((el) => { const s = $(".odo-strip", el); s.style.transition = "none"; });
      roll();
    } else {
      const io = new IntersectionObserver((es) => { if (es.some((e) => e.isIntersecting)) { roll(); io.disconnect(); } }, { threshold: 0.6 });
      io.observe(odo);
    }
  }

  // ---------- quadro de ferramentas ↔ lista de serviços ----------
  const tools = $$(".tool");
  const rows = $$(".sv");
  function pick(id, scroll) {
    tools.forEach((t) => t.setAttribute("aria-pressed", String(t.dataset.sv === id)));
    rows.forEach((r) => r.classList.toggle("is-on", r.dataset.sv === id));
    if (scroll && matchMedia("(max-width: 59.99rem)").matches) {
      $(`#sv-${id}`)?.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "center" });
    }
  }
  tools.forEach((t) => t.addEventListener("click", () => pick(t.dataset.sv, true)));
  rows.forEach((r) => r.addEventListener("pointerenter", (e) => { if (e.pointerType === "mouse") pick(r.dataset.sv, false); }));

  // ---------- folha de obra ----------
  const form = $("#job-form");
  if (!form) return;
  // Sem JS o formulário usa a validação nativa e o fallback mailto: do HTML; com JS validamos nós.
  form.noValidate = true;
  const preview = $("[data-preview]");
  const live = $("[data-live]");
  const refEl = $("[data-ref]");
  const ref = `FO-${String(now0.y).slice(2)}${pad(now0.mo)}${pad(now0.d)}-${Math.random().toString(36).slice(2, 6).toUpperCase()}`;
  if (refEl) refEl.textContent = `N.º ${ref}`;

  // próximos 10 dias úteis
  const sel = $("#f-dia");
  for (let i = 1, n = 0; n < 10 && i < 30; i++) {
    const d = addDays(now0.y, now0.mo, now0.d, i);
    if (!slotsFor(d).length) continue;
    const label = `${DAYS[d.dow][0].toUpperCase()}${DAYS[d.dow].slice(1)}, ${pad(d.d)}/${pad(d.mo)}`;
    sel.add(new Option(label, label));
    n++;
  }

  // matrícula: AA-00-AA / 00-AA-00 / 00-00-AA
  const plate = $("#f-mat");
  plate.addEventListener("input", () => {
    const raw = plate.value.toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 6);
    plate.value = raw.replace(/(.{2})(?=.)/g, "$1-");
  });

  function build() {
    const v = (n) => (form.elements[n]?.value || "").trim();
    const motivos = $$('input[name="motivo"]:checked', form).map((i) => i.value);
    const lines = [
      "Olá Arealauto,",
      "",
      `Folha de obra ${ref}`,
      `Nome: ${v("nome") || "—"}`,
      `Telemóvel: ${v("tel") || "—"}`,
    ];
    if (v("matricula")) lines.push(`Matrícula: ${v("matricula")}`);
    if (v("carro")) lines.push(`Carro: ${v("carro")}`);
    if (motivos.length) lines.push(`Preciso de: ${motivos.join(", ")}`);
    if (v("descricao")) lines.push("", v("descricao"));
    lines.push("", `Dá-me jeito: ${v("dia") || "qualquer dia útil"}, de ${form.elements.periodo.value}.`, "", "Obrigado.");
    return lines.join("\n");
  }
  const render = () => { preview.textContent = build(); };
  form.addEventListener("input", render);
  form.addEventListener("change", render);
  render();

  function validate() {
    let first = null;
    [["f-nome", "e-nome", (x) => x.length >= 2], ["f-tel", "e-tel", (x) => x.replace(/\D/g, "").length >= 9]].forEach(([id, err, ok]) => {
      const el = $("#" + id), bad = !ok(el.value.trim());
      el.setAttribute("aria-invalid", String(bad));
      $("#" + err).hidden = !bad;
      if (bad && !first) first = el;
    });
    if (first) { first.focus(); live.textContent = "Faltam dados na folha de obra."; return false; }
    return true;
  }

  // limpar o erro assim que o campo fica válido
  [["f-nome", "e-nome", 2], ["f-tel", "e-tel", 9]].forEach(([id, err, min]) => {
    const el = $("#" + id);
    el.addEventListener("input", () => {
      const val = id === "f-tel" ? el.value.replace(/\D/g, "") : el.value.trim();
      if (el.getAttribute("aria-invalid") === "true" && val.length >= min) { el.setAttribute("aria-invalid", "false"); $("#" + err).hidden = true; }
    });
  });

  let via = "whatsapp";
  $$("[data-via]", form).forEach((b) => b.addEventListener("click", () => (via = b.dataset.via)));

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (e.submitter?.dataset.via) via = e.submitter.dataset.via;
    if (!validate()) return;
    const text = build();
    const done = () => {
      $(".carbon").classList.add("is-ready");
      $(".carbon-title").textContent = "Pronta a enviar. Confirme na app que abriu.";
    };
    if (document.startViewTransition && !reduced) document.startViewTransition(done); else done();
    const url = via === "email"
      ? `mailto:${CONFIG.email}?subject=${encodeURIComponent(`Folha de obra ${ref}`)}&body=${encodeURIComponent(text)}`
      : `https://wa.me/${CONFIG.whatsapp || ""}?text=${encodeURIComponent(text)}`;
    live.textContent = via === "email" ? "A abrir o email com a mensagem." : "A abrir o WhatsApp com a mensagem.";
    if (via === "email") location.href = url; else window.open(url, "_blank", "noopener");
  });

  $("[data-copy]").addEventListener("click", async () => {
    try { await navigator.clipboard.writeText(build()); live.textContent = "Texto copiado."; $("[data-copy]").textContent = "Copiado"; }
    catch { live.textContent = "Não foi possível copiar. Selecione o texto da cópia."; }
  });
})();
