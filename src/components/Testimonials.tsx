"use client";
import { useState, useRef } from "react";
import { motion, AnimatePresence, useInView } from "framer-motion";

const testimonials = [
  {
    quote: "FORMA didn't just build us a website — they built us a presence. Our leads tripled in the first month.",
    author: "Sarah K.",
    role: "CEO, Nocturn",
    accent: "#c8ff00",
  },
  {
    quote: "The animations are insane. Every person who visits our site messages us asking who built it. That's the ROI.",
    author: "Marcus T.",
    role: "Founder, Vela",
    accent: "#ff3c00",
  },
  {
    quote: "We came with a vague brief and they turned it into a 10-year brand platform. Genuinely changed how we see ourselves.",
    author: "Priya M.",
    role: "CMO, Stratum",
    accent: "#9b5de5",
  },
];

export default function Testimonials() {
  const [idx, setIdx] = useState(0);
  const ref = useRef<HTMLElement>(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });
  const cur = testimonials[idx];

  return (
    <section ref={ref} className="px-6 md:px-12 py-24 md:py-36 border-t overflow-hidden" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
      <motion.p
        className="section-label mb-16"
        initial={{ opacity: 0, y: 20 }}
        animate={inView ? { opacity: 1, y: 0 } : {}}
      >
        What clients say
      </motion.p>

      <div className="relative min-h-[260px] flex flex-col justify-between">
        <AnimatePresence mode="wait">
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          >
            <blockquote
              className="text-[clamp(1.4rem,3.5vw,2.8rem)] font-black tracking-tight leading-tight max-w-4xl mb-10"
            >
              &ldquo;{cur.quote}&rdquo;
            </blockquote>
            <div className="flex items-center gap-4">
              <div
                className="w-10 h-10 rounded-full flex items-center justify-center text-sm font-black"
                style={{ background: cur.accent, color: "#080808" }}
              >
                {cur.author[0]}
              </div>
              <div>
                <p className="font-semibold text-sm">{cur.author}</p>
                <p className="text-xs opacity-40">{cur.role}</p>
              </div>
            </div>
          </motion.div>
        </AnimatePresence>

        {/* Controls */}
        <div className="flex items-center gap-4 mt-12">
          {testimonials.map((_, i) => (
            <button
              key={i}
              onClick={() => setIdx(i)}
              className="transition-all duration-300"
              style={{
                width: i === idx ? "2rem" : "0.5rem",
                height: "0.5rem",
                borderRadius: "99px",
                background: i === idx ? "var(--accent)" : "rgba(255,255,255,0.2)",
              }}
              aria-label={`Testimonial ${i + 1}`}
            />
          ))}
          <div className="flex gap-2 ml-auto">
            <button
              onClick={() => setIdx((idx - 1 + testimonials.length) % testimonials.length)}
              className="w-10 h-10 rounded-full border flex items-center justify-center text-sm hover:border-white transition-colors"
              style={{ borderColor: "rgba(255,255,255,0.15)" }}
            >
              ←
            </button>
            <button
              onClick={() => setIdx((idx + 1) % testimonials.length)}
              className="w-10 h-10 rounded-full border flex items-center justify-center text-sm hover:border-white transition-colors"
              style={{ borderColor: "rgba(255,255,255,0.15)" }}
            >
              →
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
