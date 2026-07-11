/* Fábrica da Picanha — interações
   i18n · nav + dropdown de idioma · scrollspy · reveals · contadores ·
   parallax · carrossel de cortes · reservas WhatsApp */

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
    document.querySelectorAll("[data-lang-current]").forEach((el) => {
      el.textContent = lang.toUpperCase();
    });
  }

  document.querySelectorAll(".lang__btn").forEach((btn) => {
    btn.addEventListener("click", () => applyLang(btn.dataset.lang));
  });

  applyLang(lang);

  /* ============ dropdown de idioma (desktop) ============ */

  const langDd = document.getElementById("langDd");
  const langBtn = document.getElementById("langBtn");

  if (langDd && langBtn) {
    const setOpen = (open) => {
      langDd.classList.toggle("is-open", open);
      langBtn.setAttribute("aria-expanded", String(open));
    };
    langBtn.addEventListener("click", (ev) => {
      ev.stopPropagation();
      setOpen(!langDd.classList.contains("is-open"));
    });
    langDd.querySelectorAll(".lang__btn").forEach((b) => {
      b.addEventListener("click", () => { setOpen(false); langBtn.focus(); });
    });
    document.addEventListener("click", (ev) => {
      if (!langDd.contains(ev.target)) setOpen(false);
    });
    document.addEventListener("keydown", (ev) => {
      if (ev.key === "Escape" && langDd.classList.contains("is-open")) {
        setOpen(false);
        langBtn.focus();
      }
    });
  }

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

  /* ============ scrollspy: sublinhado cobre no link ativo ============ */

  const spyLinks = Array.from(document.querySelectorAll(".nav__links a"));
  const spySections = spyLinks
    .map((a) => document.querySelector(a.getAttribute("href")))
    .filter(Boolean);

  function updateSpy() {
    const probe = window.scrollY + window.innerHeight * 0.4;
    let current = null;
    spySections.forEach((sec) => {
      if (sec.offsetTop <= probe) current = "#" + sec.id;
    });
    spyLinks.forEach((a) => {
      a.classList.toggle("is-active", a.getAttribute("href") === current);
    });
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

  const heroContent = document.querySelector("[data-parallax]");
  const conceptImg = document.querySelector("[data-parallax-slow]");
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

      // link ativo
      updateSpy();

      if (reducedMotion) return;

      // hero desvanece ao rolar
      if (heroContent && y < window.innerHeight * 1.2) {
        heroContent.style.transform = `translateY(${y * 0.28}px)`;
        heroContent.style.opacity = String(Math.max(0, 1 - y / (window.innerHeight * 0.85)));
      }

      // parallax suave na fotografia do conceito
      if (conceptImg) {
        const rect = conceptImg.getBoundingClientRect();
        const delta = rect.top + rect.height / 2 - window.innerHeight / 2;
        conceptImg.style.transform = `translateY(${(-delta * 0.06).toFixed(1)}px)`;
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
