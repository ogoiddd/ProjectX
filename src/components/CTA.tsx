"use client";
import { useRef, useState } from "react";
import { motion, useInView } from "framer-motion";

export default function CTA() {
  const ref = useRef<HTMLElement>(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });
  const [hovered, setHovered] = useState(false);

  return (
    <section
      ref={ref}
      id="contact"
      className="noise relative px-6 md:px-12 py-28 md:py-48 overflow-hidden border-t"
      style={{ borderColor: "rgba(255,255,255,0.06)" }}
    >
      {/* Background pulse */}
      <motion.div
        className="absolute inset-0 pointer-events-none"
        animate={{
          background: hovered
            ? "radial-gradient(circle at 50% 50%, rgba(200,255,0,0.08) 0%, transparent 60%)"
            : "radial-gradient(circle at 50% 50%, rgba(200,255,0,0.02) 0%, transparent 60%)",
        }}
        transition={{ duration: 0.5 }}
      />

      <div className="relative z-10 text-center max-w-5xl mx-auto">
        <motion.p
          className="section-label mb-8 block"
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
        >
          Ready to start?
        </motion.p>

        <motion.h2
          className="text-[clamp(3rem,9vw,8rem)] font-black tracking-tighter leading-[0.9] mb-12"
          initial={{ opacity: 0, y: 60 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ delay: 0.1, duration: 0.9, ease: [0.16, 1, 0.3, 1] }}
          onMouseEnter={() => setHovered(true)}
          onMouseLeave={() => setHovered(false)}
        >
          Let&apos;s build
          <br />
          <span style={{ color: "var(--accent)" }}>something</span>
          <br />
          legendary.
        </motion.h2>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ delay: 0.3, duration: 0.7 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4"
        >
          <a
            href="mailto:hello@forma.studio"
            className="magnetic-btn px-10 py-5 font-black text-sm tracking-widest uppercase rounded-full"
            style={{ background: "var(--accent)", color: "#080808" }}
            data-cursor
          >
            Start a Project
          </a>
          <a
            href="mailto:hello@forma.studio"
            className="text-sm opacity-50 hover:opacity-100 transition-opacity tracking-widest uppercase"
          >
            hello@forma.studio
          </a>
        </motion.div>
      </div>
    </section>
  );
}
