"use client";
import { useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { gsap } from "gsap";

const WORDS = ["brands", "ideas", "stories", "products", "visions"];

function ScrambleText({ words }: { words: string[] }) {
  const ref = useRef<HTMLSpanElement>(null);
  const CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&";

  useEffect(() => {
    const el = ref.current!;
    let wordIdx = 0;
    let interval: ReturnType<typeof setInterval>;
    let scrambleTimeout: ReturnType<typeof setTimeout>;

    const scramble = (target: string, onDone: () => void) => {
      let frame = 0;
      const total = 18;
      interval = setInterval(() => {
        el.textContent = target
          .split("")
          .map((ch, i) =>
            frame / total > i / target.length
              ? ch
              : CHARS[Math.floor(Math.random() * CHARS.length)]
          )
          .join("");
        frame++;
        if (frame > total + target.length) {
          clearInterval(interval);
          el.textContent = target;
          onDone();
        }
      }, 35);
    };

    const cycle = () => {
      wordIdx = (wordIdx + 1) % words.length;
      scramble(words[wordIdx], () => {
        scrambleTimeout = setTimeout(cycle, 2400);
      });
    };

    el.textContent = words[0];
    scrambleTimeout = setTimeout(cycle, 2400);

    return () => {
      clearInterval(interval);
      clearTimeout(scrambleTimeout);
    };
  }, [words]);

  return (
    <span
      ref={ref}
      className="inline-block font-mono tracking-tight"
      style={{ color: "var(--accent)" }}
    />
  );
}

export default function Hero() {
  const containerRef = useRef<HTMLElement>(null);
  const bgRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleMouse = (e: MouseEvent) => {
      if (!bgRef.current) return;
      const x = (e.clientX / window.innerWidth  - 0.5) * 30;
      const y = (e.clientY / window.innerHeight - 0.5) * 20;
      gsap.to(bgRef.current, {
        x,
        y,
        duration: 2.5,
        ease: "power2.out",
      });
    };

    window.addEventListener("mousemove", handleMouse);
    return () => window.removeEventListener("mousemove", handleMouse);
  }, []);

  const containerVariants = {
    hidden: {},
    visible: { transition: { staggerChildren: 0.12, delayChildren: 0.2 } },
  };

  const lineVariants = {
    hidden:  { y: "110%", opacity: 0 },
    visible: { y: "0%",  opacity: 1, transition: { duration: 0.9, ease: [0.16, 1, 0.3, 1] } },
  };

  return (
    <section
      ref={containerRef}
      id="hero"
      className="noise relative min-h-screen flex flex-col justify-end pb-16 md:pb-24 px-6 md:px-12 overflow-hidden"
    >
      {/* Animated gradient orbs */}
      <div ref={bgRef} className="absolute inset-0 pointer-events-none" style={{ zIndex: 0 }}>
        <motion.div
          className="absolute rounded-full blur-[120px]"
          style={{
            width: "60vw",
            height: "60vw",
            top: "-15%",
            right: "-10%",
            background: "radial-gradient(circle, rgba(200,255,0,0.07) 0%, transparent 70%)",
          }}
          animate={{ scale: [1, 1.08, 1], rotate: [0, 15, 0] }}
          transition={{ duration: 12, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="absolute rounded-full blur-[100px]"
          style={{
            width: "50vw",
            height: "50vw",
            bottom: "-10%",
            left: "-10%",
            background: "radial-gradient(circle, rgba(255,60,0,0.05) 0%, transparent 70%)",
          }}
          animate={{ scale: [1, 1.12, 1], rotate: [0, -20, 0] }}
          transition={{ duration: 14, repeat: Infinity, ease: "easeInOut", delay: 2 }}
        />
      </div>

      {/* Big decorative year */}
      <motion.div
        className="absolute top-28 right-6 md:right-12 text-[11vw] font-black opacity-[0.04] leading-none select-none pointer-events-none"
        initial={{ opacity: 0 }}
        animate={{ opacity: 0.04 }}
        transition={{ delay: 1, duration: 1 }}
      >
        2025
      </motion.div>

      {/* Main heading */}
      <motion.div
        className="relative z-10 max-w-7xl"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <div className="split-line mb-2">
          <motion.span
            variants={lineVariants}
            className="section-label inline-block mb-6"
          >
            Digital Experience Studio
          </motion.span>
        </div>

        <h1 className="text-[clamp(3.2rem,10vw,9rem)] font-black leading-[0.92] tracking-tighter mb-2">
          <div className="split-line">
            <motion.span variants={lineVariants} className="inline-block">
              We make
            </motion.span>
          </div>
          <div className="split-line">
            <motion.span variants={lineVariants} className="inline-block">
              <ScrambleText words={WORDS} />
            </motion.span>
          </div>
          <div className="split-line">
            <motion.span variants={lineVariants} className="inline-block gradient-text">
              unforgettable.
            </motion.span>
          </div>
        </h1>

        <div className="split-line mt-8">
          <motion.p
            variants={lineVariants}
            className="text-base md:text-lg opacity-50 max-w-lg leading-relaxed"
          >
            Scroll-stopping websites that turn visitors into customers and brands
            into cultural landmarks.
          </motion.p>
        </div>

        <motion.div
          variants={lineVariants}
          className="flex flex-wrap gap-4 mt-10 items-center"
        >
          <a
            href="#work"
            className="magnetic-btn px-8 py-4 font-bold text-sm tracking-widest uppercase"
            style={{ background: "var(--accent)", color: "#080808" }}
            data-cursor
          >
            See Our Work
          </a>
          <a
            href="#services"
            className="text-sm tracking-widest uppercase opacity-60 hover:opacity-100 transition-opacity flex items-center gap-2"
          >
            What we do
            <span className="inline-block translate-y-px">↓</span>
          </a>
        </motion.div>
      </motion.div>

      {/* Scroll indicator */}
      <motion.div
        className="absolute bottom-8 left-6 md:left-12 flex items-center gap-3 opacity-40 text-xs tracking-widest uppercase"
        initial={{ opacity: 0 }}
        animate={{ opacity: 0.4 }}
        transition={{ delay: 1.8, duration: 0.8 }}
      >
        <motion.span
          className="inline-block w-6 h-px"
          style={{ background: "var(--fg)" }}
          animate={{ scaleX: [0, 1, 0] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
        />
        Scroll
      </motion.div>

      {/* Grid lines */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.025]"
        style={{
          backgroundImage:
            "linear-gradient(var(--fg) 1px, transparent 1px), linear-gradient(90deg, var(--fg) 1px, transparent 1px)",
          backgroundSize: "80px 80px",
          zIndex: 0,
        }}
      />
    </section>
  );
}
