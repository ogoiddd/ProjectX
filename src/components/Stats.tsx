"use client";
import { useEffect, useRef, useState } from "react";
import { motion, useInView } from "framer-motion";

const stats = [
  { value: 120, suffix: "+", label: "Projects delivered" },
  { value: 98,  suffix: "%", label: "Client satisfaction" },
  { value: 7,   suffix: "×", label: "Avg. conversion lift" },
  { value: 12,  suffix: "y", label: "Years in the craft" },
];

function Counter({ value, suffix }: { value: number; suffix: string }) {
  const [count, setCount] = useState(0);
  const ref = useRef<HTMLSpanElement>(null);
  const inView = useInView(ref, { once: true, margin: "-100px" });

  useEffect(() => {
    if (!inView) return;
    const duration = 1800;
    const start = Date.now();
    const tick = () => {
      const elapsed = Date.now() - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setCount(Math.round(eased * value));
      if (progress < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }, [inView, value]);

  return (
    <span ref={ref} className="counter-num">
      {count}{suffix}
    </span>
  );
}

export default function Stats() {
  const sectionRef = useRef<HTMLElement>(null);
  const inView = useInView(sectionRef, { once: true, margin: "-80px" });

  return (
    <section ref={sectionRef} id="about" className="px-6 md:px-12 py-24 md:py-36 border-b" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
      <motion.p
        className="section-label mb-16"
        initial={{ opacity: 0, y: 20 }}
        animate={inView ? { opacity: 1, y: 0 } : {}}
        transition={{ duration: 0.6 }}
      >
        By the numbers
      </motion.p>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-4">
        {stats.map((s, i) => (
          <motion.div
            key={s.label}
            initial={{ opacity: 0, y: 40 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ delay: i * 0.1, duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
          >
            <div
              className="text-[clamp(3rem,6vw,5.5rem)] font-black leading-none tracking-tighter mb-3"
              style={{ color: i % 2 === 1 ? "var(--accent)" : "var(--fg)" }}
            >
              <Counter value={s.value} suffix={s.suffix} />
            </div>
            <p className="text-sm opacity-40 leading-snug max-w-[12ch]">{s.label}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
