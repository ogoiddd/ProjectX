"use client";
import { useRef } from "react";
import { motion, useScroll, useTransform, useInView } from "framer-motion";

const projects = [
  {
    title: "Nocturn",
    category: "Brand + Web",
    year: "2024",
    color: "#c8ff00",
    desc: "A luxury nightlife brand that needed to feel exclusive online.",
    bg: "linear-gradient(135deg, #0a0a0a 0%, #1a1500 100%)",
  },
  {
    title: "Vela",
    category: "E-commerce",
    year: "2024",
    color: "#ff3c00",
    desc: "Sustainable furniture with a 3D product explorer and AR try-on.",
    bg: "linear-gradient(135deg, #0a0a0a 0%, #1a0500 100%)",
  },
  {
    title: "Stratum",
    category: "SaaS Dashboard",
    year: "2025",
    color: "#9b5de5",
    desc: "Data-heavy analytics product made beautiful and intuitive.",
    bg: "linear-gradient(135deg, #0a0a0a 0%, #0d0515 100%)",
  },
  {
    title: "Cascade",
    category: "Motion + Identity",
    year: "2025",
    color: "#00f5d4",
    desc: "A financial platform that had to feel trustworthy and modern.",
    bg: "linear-gradient(135deg, #0a0a0a 0%, #001510 100%)",
  },
];

function ProjectCard({ project, index }: { project: typeof projects[0]; index: number }) {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "-100px" });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 80 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.9, ease: [0.16, 1, 0.3, 1], delay: index * 0.06 }}
      className="group relative overflow-hidden rounded-2xl cursor-none"
      style={{ background: project.bg, border: "1px solid rgba(255,255,255,0.06)" }}
      data-cursor
    >
      {/* Aspect ratio placeholder */}
      <div className="aspect-[4/3] relative flex flex-col justify-end p-8">
        {/* Animated color blob */}
        <div
          className="absolute top-1/4 left-1/4 w-48 h-48 rounded-full blur-[80px] opacity-20 group-hover:opacity-40 transition-opacity duration-700"
          style={{ background: project.color }}
        />

        {/* Big title watermark */}
        <div
          className="absolute top-6 right-6 text-[5rem] font-black leading-none opacity-[0.06] select-none"
          style={{ color: project.color }}
        >
          {project.title[0]}
        </div>

        {/* Hover reveal overlay */}
        <motion.div
          className="absolute inset-0"
          style={{ background: `${project.color}08` }}
          initial={{ opacity: 0 }}
          whileHover={{ opacity: 1 }}
          transition={{ duration: 0.3 }}
        />

        {/* Content */}
        <div className="relative z-10">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-mono opacity-40">{project.category}</span>
            <span className="text-xs font-mono opacity-30">{project.year}</span>
          </div>
          <h3 className="text-3xl md:text-4xl font-black tracking-tight mb-2">{project.title}</h3>
          <p className="text-sm opacity-40 max-w-xs">{project.desc}</p>
        </div>

        {/* Arrow */}
        <motion.div
          className="absolute top-6 left-8 w-10 h-10 rounded-full flex items-center justify-center border"
          style={{ borderColor: project.color, color: project.color }}
          initial={{ scale: 0, opacity: 0 }}
          whileHover={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.25 }}
        >
          ↗
        </motion.div>
      </div>
    </motion.div>
  );
}

export default function Work() {
  const sectionRef = useRef<HTMLElement>(null);
  const inView = useInView(sectionRef, { once: true, margin: "-80px" });

  return (
    <section ref={sectionRef} id="work" className="px-6 md:px-12 py-24 md:py-36 border-t" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-4">
        <div>
          <motion.p
            className="section-label mb-4"
            initial={{ opacity: 0, y: 20 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
          >
            Selected work
          </motion.p>
          <motion.h2
            className="text-[clamp(2.5rem,6vw,5rem)] font-black tracking-tighter leading-tight"
            initial={{ opacity: 0, y: 30 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ delay: 0.1, duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          >
            The proof is in <br className="hidden md:block" />
            the portfolio.
          </motion.h2>
        </div>
        <motion.a
          href="#contact"
          initial={{ opacity: 0 }}
          animate={inView ? { opacity: 1 } : {}}
          transition={{ delay: 0.3 }}
          className="text-sm opacity-50 hover:opacity-100 transition-opacity flex items-center gap-2 shrink-0"
        >
          See all projects <span>→</span>
        </motion.a>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        {projects.map((p, i) => (
          <ProjectCard key={p.title} project={p} index={i} />
        ))}
      </div>
    </section>
  );
}
