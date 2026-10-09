/* Restaurante Cidade Velha — small, dependency-free enhancements.
   1. "Aberto agora" from the Lisbon clock   2. booking request -> WhatsApp / email (no backend)
   3. walking-route map                       */
(() => {
  "use strict";
  const S = JSON.parse(document.getElementById("i18n").textContent);
  // Opening hours (Google listing): Mon–Sat 11:00–22:00, Sunday closed. Index 0 = Monday.
  const HOURS = [[660, 1320], [660, 1320], [660, 1320], [660, 1320], [660, 1320], [660, 1320], null];
  const pad = (n) => String(n).padStart(2, "0");
  const hm = (m) => `${pad(Math.floor(m / 60))}:${pad(m % 60)}`;

  function lisbonNow() {
    const p = Object.fromEntries(new Intl.DateTimeFormat("en-GB", {
      timeZone: "Europe/Lisbon", weekday: "short", hour: "2-digit", minute: "2-digit", hourCycle: "h23",
      year: "numeric", month: "2-digit", day: "2-digit"
    }).formatToParts(new Date()).map((x) => [x.type, x.value]));
    const day = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].indexOf(p.weekday);
    return { day, min: +p.hour * 60 + +p.minute, iso: `${p.year}-${p.month}-${p.day}` };
  }

  function status() {
    const n = lisbonNow();
    const h = HOURS[n.day];
    if (h && n.min >= h[0] && n.min < h[1]) return { open: true, text: S.open_until.replace("{t}", hm(h[1])) };
    if (h && n.min < h[0]) return { open: false, text: S.opens_today.replace("{t}", hm(h[0])) };
    for (let i = 1; i <= 7; i++) {
      const d = (n.day + i) % 7;
      if (HOURS[d]) return { open: false, text: S.opens_day.replace("{d}", i === 1 ? S.tomorrow : S.days[d]).replace("{t}", hm(HOURS[d][0])) };
    }
    return { open: false, text: "" };
  }

  function paintStatus() {
    const s = status();
    document.querySelectorAll("[data-status]").forEach((el) => {
      el.dataset.open = s.open;
      el.querySelector("[data-status-text]").textContent = s.text;
    });
    const today = lisbonNow().day;
    document.querySelectorAll(".hours tr").forEach((tr) => tr.classList.toggle("today", +tr.dataset.day === today));
  }
  paintStatus();
  setInterval(paintStatus, 60000);

  /* ---------- booking request ---------- */
  const form = document.getElementById("booking");
  if (form) {
    const $ = (n) => form.elements[n];
    const preview = document.querySelector("[data-preview]");
    const date = $("dia"), time = $("hora"), people = $("pessoas");
    const now = lisbonNow();
    date.min = now.iso;
    // default: today if still bookable, else the next open day
    const addDays = (iso, k) => { const d = new Date(iso + "T12:00:00Z"); d.setUTCDate(d.getUTCDate() + k); return d.toISOString().slice(0, 10); };
    const dow = (iso) => (new Date(iso + "T12:00:00Z").getUTCDay() + 6) % 7;
    let def = now.iso;
    if (!HOURS[now.day] || now.min > 20 * 60 + 30) def = addDays(def, 1);
    while (!HOURS[dow(def)]) def = addDays(def, 1);
    date.value = def;

    function syncTimes() {
      const today = date.value === lisbonNow().iso;
      const cutoff = lisbonNow().min + 30;
      let firstOk = null;
      [...time.options].forEach((o) => {
        const [h, m] = o.value.split(":").map(Number);
        o.disabled = today && h * 60 + m < cutoff;
        if (!o.disabled && !firstOk) firstOk = o;
      });
      if (time.selectedOptions[0]?.disabled && firstOk) firstOk.selected = true;
      if (!time.value || time.selectedOptions[0]?.disabled) { const o20 = [...time.options].find((o) => o.value === "20:00" && !o.disabled); if (o20) o20.selected = true; }
    }
    if (!form.dataset.timeTouched) { const o = [...time.options].find((x) => x.value === "20:00"); if (o) o.selected = true; }
    syncTimes();

    form.querySelectorAll("[data-step]").forEach((b) => b.addEventListener("click", () => {
      const v = Math.min(30, Math.max(1, (+people.value || 1) + +b.dataset.step));
      people.value = v; render();
    }));

    function fmtDate(iso) {
      if (!iso) return "";
      return new Intl.DateTimeFormat("pt-PT", { weekday: "long", day: "numeric", month: "long", timeZone: "UTC" }).format(new Date(iso + "T12:00:00Z"));
    }

    function message() {
      const lines = ["Olá, Cidade Velha! Pedido de reserva:", ""];
      lines.push(`• Nome: ${$("nome").value.trim() || "—"}`);
      lines.push(`• Dia: ${fmtDate(date.value) || "—"}`);
      lines.push(`• Hora: ${time.value || "—"}`);
      lines.push(`• Pessoas: ${people.value || "—"}`);
      lines.push(`• Mesa: ${form.querySelector("[name=mesa]:checked")?.value || "Tanto faz"}`);
      if ($("tel").value.trim()) lines.push(`• Contacto: ${$("tel").value.trim()}`);
      if ($("notas").value.trim()) lines.push(`• Notas: ${$("notas").value.trim()}`);
      lines.push(`• Língua do cliente: ${S.lang_name}`);
      lines.push("", "(pedido enviado a partir do site)");
      return lines.join("\n");
    }
    function render() { preview.textContent = message(); }

    function setErr(input, id, msg) {
      const e = document.getElementById(id);
      e.textContent = msg || "";
      input.setAttribute("aria-invalid", msg ? "true" : "false");
      return !msg;
    }
    function validate() {
      let ok = setErr($("nome"), "e-name", $("nome").value.trim() ? "" : S.err_name);
      let dm = "";
      if (!date.value) dm = S.err_date;
      else if (date.value < lisbonNow().iso) dm = S.err_past;
      else if (!HOURS[dow(date.value)]) dm = S.err_sun;
      ok = setErr(date, "e-date", dm) && ok;
      let tm = "";
      if (!dm) {
        syncTimes();
        if (!time.value || time.selectedOptions[0]?.disabled) tm = [...time.options].some((o) => !o.disabled) ? S.err_time : S.err_late;
      }
      ok = setErr(time, "e-time", tm) && ok;
      return ok;
    }

    form.addEventListener("input", (e) => { if (e.target === date) { syncTimes(); if (date.getAttribute("aria-invalid") === "true") validate(); } render(); });
    time.addEventListener("change", () => { if (time.getAttribute("aria-invalid") === "true") validate(); });
    form.addEventListener("change", render);
    const statusBox = form.querySelector("[data-form-status]");
    const statusText = form.querySelector("[data-form-status-text]");
    const fallback = form.querySelector("[data-form-fallback]");
    function showStatus(text, href, newTab) {
      statusText.textContent = text;           // fixed strings only; user input never reaches innerHTML
      fallback.hidden = !href;
      if (href) fallback.href = href;
      if (newTab) fallback.target = "_blank"; else fallback.removeAttribute("target");
      statusBox.hidden = false;
    }
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!validate()) { statusBox.hidden = true; form.querySelector("[aria-invalid=true]")?.focus(); return; }
      const msg = message();
      const via = e.submitter?.value || "wa";
      if (via === "mail") {
        const subj = `Pedido de reserva · ${fmtDate(date.value)} ${time.value} · ${people.value} pax`;
        const url = `mailto:${form.dataset.email || ""}?subject=${encodeURIComponent(subj)}&body=${encodeURIComponent(msg)}`;
        showStatus(S.sent_mail, url);
        location.href = url;
      } else {
        const url = `https://wa.me/${encodeURIComponent(form.dataset.wa)}?text=${encodeURIComponent(msg)}`;
        showStatus(S.sent_wa, url, true);
        window.open(url, "_blank", "noopener");
      }
    });
    render();
  }

  /* ---------- map: route toggle + draw-on-view ---------- */
  const map = document.querySelector(".map");
  if (map) {
    const btns = document.querySelectorAll(".routes [data-route]");
    btns.forEach((b) => b.addEventListener("click", () => {
      const r = b.dataset.route;
      btns.forEach((x) => x.setAttribute("aria-pressed", x === b));
      document.querySelectorAll("[data-steps]").forEach((s) => (s.hidden = s.dataset.steps !== r));
      map.classList.remove("drawn");
      map.dataset.route = r;
      requestAnimationFrame(() => requestAnimationFrame(() => map.classList.add("drawn")));
    }));
    if ("IntersectionObserver" in window) {
      const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting || e.boundingClientRect.top < 0) { map.classList.add("drawn"); io.disconnect(); } }), { threshold: 0.2 });
      io.observe(map);
    } else map.classList.add("drawn");
  }
})();
