"use client";
import { motion } from "framer-motion";

const socials = ["Twitter", "Instagram", "Dribbble", "LinkedIn"];

export default function Footer() {
  return (
    <footer className="px-6 md:px-12 py-12 border-t" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-8">
        <div>
          <span className="text-2xl font-black tracking-tighter" style={{ color: "var(--accent)" }}>
            FORMA
          </span>
          <p className="text-xs opacity-30 mt-1">Digital Experience Studio — Est. 2013</p>
        </div>

        <nav className="flex flex-wrap gap-6">
          {socials.map(s => (
            <a
              key={s}
              href="#"
              className="text-xs opacity-40 hover:opacity-100 transition-opacity tracking-wide"
            >
              {s}
            </a>
          ))}
        </nav>

        <p className="text-xs opacity-20 font-mono">
          © {new Date().getFullYear()} FORMA Studio
        </p>
      </div>
    </footer>
  );
}
