"use client";
import { useRef, useState } from "react";
import { motion, useInView } from "framer-motion";

const services = [
  {
    num: "01",
    title: "Brand Identity",
    desc: "Logos, color systems, typography, and motion guidelines that make your brand immediately recognizable and lasting.",
    tags: ["Strategy", "Visual ID", "Guidelines"],
  },
  {
    num: "02",
    title: "Interactive Web",
    desc: "Custom-built websites with scroll-stopping interactions, 3D elements, and micro-animations that convert.",
    tags: ["Next.js", "GSAP", "Three.js"],
  },
  {
    num: "03",
    title: "Motion Design",
    desc: "Video, UI animations, and immersive experiences that communicate your story without a single word.",
    tags: ["After Effects", "Rive", "Lottie"],
  },
  {
    num: "04",
    title: "Creative Direction",
    desc: "We take the wheel — strategy, concept, copywriting, design, and dev. All under one roof.",
    tags: ["Full-service", "Strategy", "Content"],
  },
];

function TiltCard({ service, index, inView }: { service: typeof services[0]; index: number; inView: boolean }) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [tilt, setTilt] = useState({ x: 0, y: 0 });
  const [hovered, setHovered] = useState(false);

  const handleMove = (e: React.MouseEvent) => {
    const card = cardRef.current!;
    const rect = card.getBoundingClientRect();
    const cx = (e.clientX - rect.left) / rect.width  - 0.5;
    const cy = (e.clientY - rect.top)  / rect.height - 0.5;
    setTilt({ x: cy * -12, y: cx * 12 });
  };

  return (
    <motion.div
      ref={cardRef}
      initial={{ opacity: 0, y: 60 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ delay: index * 0.12, duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
      onMouseMove={handleMove}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => { setTilt({ x: 0, y: 0 }); setHovered(false); }}
      data-cursor
      style={{
        transform: `perspective(800px) rotateX(${tilt.x}deg) rotateY(${tilt.y}deg)`,
        transition: hovered ? "transform 0.1s" : "transform 0.6s cubic-bezier(0.16,1,0.3,1)",
        background: hovered ? "rgba(200,255,0,0.04)" : "rgba(255,255,255,0.02)",
        borderColor: hovered ? "rgba(200,255,0,0.2)" : "rgba(255,255,255,0.07)",
      }}
      className="border rounded-xl p-8 flex flex-col gap-6 cursor-none"
    >
      <div className="flex items-start justify-between">
        <span className="text-xs font-mono opacity-30">{service.num}</span>
        <motion.span
          animate={{ rotate: hovered ? 45 : 0 }}
          transition={{ duration: 0.3 }}
          className="text-xl opacity-20"
        >
          ↗
        </motion.span>
      </div>
      <div>
        <h3 className="text-2xl md:text-3xl font-black tracking-tight mb-3">{service.title}</h3>
        <p className="text-sm opacity-50 leading-relaxed">{service.desc}</p>
      </div>
      <div className="flex flex-wrap gap-2 mt-auto">
        {service.tags.map(t => (
          <span key={t} className="text-xs px-3 py-1 rounded-full font-mono" style={{ background: "rgba(255,255,255,0.05)", color: "rgba(255,255,255,0.4)" }}>
            {t}
          </span>
        ))}
      </div>
    </motion.div>
  );
}

export default function Services() {
  const ref = useRef<HTMLElement>(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });

  return (
    <section ref={ref} id="services" className="px-6 md:px-12 py-24 md:py-36">
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-6">
        <div>
          <p className="section-label mb-4">What we do</p>
          <h2 className="text-[clamp(2.5rem,6vw,5rem)] font-black tracking-tighter leading-tight">
            Craft, not templates.
          </h2>
        </div>
        <p className="text-sm opacity-40 max-w-xs leading-relaxed">
          Every project is designed from scratch — no themes, no drag-and-drop, no excuses.
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        {services.map((s, i) => (
          <TiltCard key={s.num} service={s} index={i} inView={inView} />
        ))}
      </div>
    </section>
  );
}
