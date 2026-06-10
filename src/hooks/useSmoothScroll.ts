"use client";
import { useEffect } from "react";

export function useSmoothScroll() {
  useEffect(() => {
    let lenis: import("lenis").default | null = null;

    async function init() {
      const { default: Lenis } = await import("lenis");
      lenis = new Lenis({
        duration: 1.4,
        easing: (t: number) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        smoothWheel: true,
      });

      const raf = (time: number) => {
        lenis?.raf(time);
        requestAnimationFrame(raf);
      };
      requestAnimationFrame(raf);
    }

    init();
    return () => { lenis?.destroy(); };
  }, []);
}
