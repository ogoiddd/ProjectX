/* Fábrica da Picanha — interações
   i18n · nav · brasas (canvas) · reveals · contadores ·
   espeto de progresso · marquee · carrossel de cortes · reservas WhatsApp */

(() => {
  "use strict";

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ============ i18n ============ */

  const SUPPORTED = ["pt", "en", "es", "fr"];
  let lang = localStorage.getItem("fdp-lang");
  if (!SUPPORTED.includes(lang)) {
    const nav = (navigator.language || "pt").slice(0, 2).toLowerCase();
    lang = SUPPORTED.includes(nav) ? nav : "pt";
  }

  const t = (key) => (I18N[lang] && I18N[lang][key]) || I18N.pt[key] || key;

  function applyLang(next) {
    lang = next;
    localStorage.setItem("fdp-lang", lang);
    document.documentElement.lang = lang;

    document.querySelectorAll("[data-i18n]").forEach((el) => {
      el.textContent = t(el.dataset.i18n);
    });
    document.querySelectorAll("[data-i18n-ph]").forEach((el) => {
      el.placeholder = t(el.dataset.i18nPh);
    });
    document.querySelectorAll(".lang__btn").forEach((b) => {
      b.classList.toggle("is-active", b.dataset.lang === lang);
    });
  }

  document.querySelectorAll(".lang__btn").forEach((btn) => {
    btn.addEventListener("click", () => applyLang(btn.dataset.lang));
  });

  applyLang(lang);

  /* ============ nav ============ */

  const nav = document.getElementById("nav");
  const burger = document.getElementById("burger");
  const mobileMenu = document.getElementById("mobileMenu");

  function closeMenu() {
    mobileMenu.classList.remove("is-open");
    document.body.classList.remove("menu-open");
    burger.setAttribute("aria-expanded", "false");
  }
  burger.addEventListener("click", () => {
    const open = mobileMenu.classList.toggle("is-open");
    document.body.classList.toggle("menu-open", open);
    burger.setAttribute("aria-expanded", String(open));
  });
  mobileMenu.querySelectorAll("a").forEach((a) => a.addEventListener("click", closeMenu));

  /* ============ brasas no hero ============ */

  const canvas = document.getElementById("embers");
  if (canvas && !reducedMotion) {
    const ctx = canvas.getContext("2d");
    let W, H, embers = [];

    function resize() {
      W = canvas.width = canvas.offsetWidth;
      H = canvas.height = canvas.offsetHeight;
    }
    resize();
    window.addEventListener("resize", resize);

    const COUNT = Math.min(70, Math.floor(window.innerWidth / 18));

    function spawn(e) {
      e.x = Math.random() * W;
      e.y = H + 10 + Math.random() * 40;
      e.r = 0.8 + Math.random() * 2.2;
      e.vy = 0.4 + Math.random() * 1.1;
      e.vx = (Math.random() - 0.5) * 0.35;
      e.life = 0;
      e.max = 250 + Math.random() * 300;
      e.hue = 18 + Math.random() * 22; // laranja → âmbar
      return e;
    }
    for (let i = 0; i < COUNT; i++) {
      const e = spawn({});
      e.y = Math.random() * H; // primeira leva espalhada
      embers.push(e);
    }

    let visible = true;
    new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; }, { threshold: 0 }).observe(canvas);

    (function tick() {
      requestAnimationFrame(tick);
      if (!visible) return;
      ctx.clearRect(0, 0, W, H);
      for (const e of embers) {
        e.life++;
        e.x += e.vx + Math.sin((e.life + e.max) * 0.02) * 0.3;
        e.y -= e.vy;
        if (e.y < -10 || e.life > e.max) spawn(e);
        const fade = Math.max(0, 1 - e.life / e.max) * 0.85;
        ctx.beginPath();
        ctx.arc(e.x, e.y, e.r, 0, Math.PI * 2);
        ctx.fillStyle = `hsla(${e.hue}, 95%, 58%, ${fade})`;
        ctx.shadowColor = "rgba(240,138,29,0.8)";
        ctx.shadowBlur = 8;
        ctx.fill();
        ctx.shadowBlur = 0;
      }
    })();
  }

  /* ============ reveals ============ */

  const revealObs = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) {
        en.target.classList.add("is-in");
        revealObs.unobserve(en.target);
      }
    });
  }, { threshold: 0.18, rootMargin: "0px 0px -40px 0px" });
  document.querySelectorAll(".reveal").forEach((el) => revealObs.observe(el));

  /* ============ contadores ============ */

  const countObs = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      countObs.unobserve(en.target);
      const el = en.target;
      const target = parseFloat(el.dataset.count);
      if (reducedMotion) { el.textContent = target; return; }
      const start = performance.now();
      const DUR = 1400;
      (function step(now) {
        const p = Math.min(1, (now - start) / DUR);
        const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(target * eased);
        if (p < 1) requestAnimationFrame(step);
      })(start);
    });
  }, { threshold: 0.6 });
  document.querySelectorAll("[data-count]").forEach((el) => countObs.observe(el));

  /* ============ efeitos ligados ao scroll (um só listener) ============ */

  const skewerFill = document.querySelector(".skewer__fill");
  const skewerFlame = document.querySelector(".skewer__flame");
  const heroContent = document.querySelector("[data-parallax]");
  const marqueeTrack = document.getElementById("marqueeTrack");
  const cuts = document.querySelector(".cuts");
  const cutsTrack = document.getElementById("cutsTrack");
  const cutsSticky = document.querySelector(".cuts__sticky");
  const isMobile = () => window.matchMedia("(max-width: 800px)").matches;

  let ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      const y = window.scrollY;

      // nav compacta
      nav.classList.toggle("is-scrolled", y > 40);

      if (reducedMotion) return;

      // espeto de progresso
      const total = document.documentElement.scrollHeight - window.innerHeight;
      const p = total > 0 ? y / total : 0;
      if (skewerFill) {
        skewerFill.style.height = (p * 100) + "%";
        skewerFlame.style.top = (p * 100) + "%";
      }

      // parallax do hero
      if (heroContent && y < window.innerHeight * 1.2) {
        heroContent.style.transform = `translateY(${y * 0.28}px)`;
        heroContent.style.opacity = String(Math.max(0, 1 - y / (window.innerHeight * 0.85)));
      }

      // marquee anda com o scroll
      if (marqueeTrack) {
        marqueeTrack.style.transform = `translateX(${-(y * 0.35) % (marqueeTrack.scrollWidth / 2)}px)`;
      }

      // carrossel de cortes: progresso dentro da secção sticky
      if (cuts && cutsTrack && !isMobile()) {
        const rect = cuts.getBoundingClientRect();
        const scrollable = cuts.offsetHeight - window.innerHeight;
        if (rect.top <= 0 && scrollable > 0) {
          const prog = Math.min(1, Math.max(0, -rect.top / scrollable));
          const max = cutsTrack.scrollWidth - cutsSticky.offsetWidth + 2 * 16;
          cutsTrack.style.transform = `translateX(${-prog * Math.max(0, max)}px)`;
        }
      } else if (cutsTrack) {
        cutsTrack.style.transform = "";
      }
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();

  /* ============ localizações → pré-seleciona restaurante ============ */

  const restSelect = document.getElementById("fRest");
  document.querySelectorAll("[data-loc]").forEach((link) => {
    link.addEventListener("click", () => { restSelect.value = link.dataset.loc; });
  });

  /* ============ reservas → WhatsApp ============ */

  const WHATSAPP = "351960307895";
  const form = document.getElementById("bookingForm");
  const dateInput = document.getElementById("fDate");

  // datas passadas indisponíveis
  dateInput.min = new Date().toISOString().split("T")[0];

  form.addEventListener("submit", (ev) => {
    ev.preventDefault();

    const name = document.getElementById("fName").value.trim();
    if (!dateInput.value || !name) {
      alert(t("form.missing"));
      return;
    }

    const locale = { pt: "pt-PT", en: "en-GB", es: "es-ES", fr: "fr-FR" }[lang];
    const dateStr = new Date(dateInput.value + "T12:00:00").toLocaleDateString(locale, {
      weekday: "long", day: "numeric", month: "long", year: "numeric"
    });

    const note = document.getElementById("fNote").value.trim();
    const msg = t("wa.msg")
      .replace("{rest}", restSelect.value)
      .replace("{date}", dateStr)
      .replace("{time}", document.getElementById("fTime").value)
      .replace("{people}", document.getElementById("fPeople").value)
      .replace("{name}", name)
      .replace("{note}", note ? t("wa.note") + note : "");

    window.open(`https://wa.me/${WHATSAPP}?text=${encodeURIComponent(msg)}`, "_blank", "noopener");
  });

  /* ============ ano no rodapé ============ */

  document.getElementById("year").textContent = new Date().getFullYear();
})();
