"use client";
import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";

const items = [
  "Brand Identity",
  "★",
  "Web Design",
  "★",
  "Motion & Animation",
  "★",
  "UI/UX Strategy",
  "★",
  "Creative Direction",
  "★",
  "Development",
  "★",
  "Brand Identity",
  "★",
  "Web Design",
  "★",
  "Motion & Animation",
  "★",
  "UI/UX Strategy",
  "★",
  "Creative Direction",
  "★",
  "Development",
  "★",
];

export default function Marquee() {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start end", "end start"] });
  const x = useTransform(scrollYProgress, [0, 1], ["0%", "-15%"]);

  return (
    <div ref={ref} className="relative overflow-hidden py-6 border-y" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
      <motion.div className="marquee-track flex items-center gap-10 text-3xl md:text-4xl font-black tracking-tighter opacity-90" style={{ x }}>
        {[...items, ...items].map((item, i) => (
          <span
            key={i}
            style={{ color: item === "★" ? "var(--accent)" : "inherit" }}
          >
            {item}
          </span>
        ))}
      </motion.div>
    </div>
  );
}
