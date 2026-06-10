"use client";
import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const links = ["Work", "Services", "About", "Contact"];

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <>
      <header
        className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 md:px-12 py-5 transition-all duration-500"
        style={{
          backdropFilter: scrolled ? "blur(20px)" : "none",
          background: scrolled ? "rgba(8,8,8,0.85)" : "transparent",
          borderBottom: scrolled ? "1px solid rgba(255,255,255,0.06)" : "1px solid transparent",
        }}
      >
        <a href="#" className="text-lg font-black tracking-tighter" style={{ color: "var(--accent)" }}>
          FORMA
        </a>

        <nav className="hidden md:flex gap-8 items-center">
          {links.map((l) => (
            <a
              key={l}
              href={`#${l.toLowerCase()}`}
              className="text-sm tracking-wide opacity-60 hover:opacity-100 transition-opacity duration-200"
            >
              {l}
            </a>
          ))}
        </nav>

        <a
          href="#contact"
          className="magnetic-btn hidden md:flex px-5 py-2.5 text-sm font-semibold border tracking-wide"
          style={{ borderColor: "var(--accent)", color: "var(--accent)" }}
          data-cursor
        >
          Let&apos;s Talk
        </a>

        <button
          className="md:hidden flex flex-col gap-1.5 p-2"
          onClick={() => setOpen(!open)}
          aria-label="Menu"
        >
          <span
            className="block w-6 h-px bg-current transition-all duration-300"
            style={{ transform: open ? "translateY(4px) rotate(45deg)" : "" }}
          />
          <span
            className="block w-4 h-px bg-current transition-all duration-300"
            style={{ opacity: open ? 0 : 1 }}
          />
          <span
            className="block w-6 h-px bg-current transition-all duration-300"
            style={{ transform: open ? "translateY(-4px) rotate(-45deg)" : "" }}
          />
        </button>
      </header>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="fixed inset-0 z-40 flex flex-col justify-center items-center gap-8"
            style={{ background: "var(--bg)" }}
          >
            {links.map((l, i) => (
              <motion.a
                key={l}
                href={`#${l.toLowerCase()}`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.07 }}
                className="text-4xl font-black tracking-tighter"
                onClick={() => setOpen(false)}
              >
                {l}
              </motion.a>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
