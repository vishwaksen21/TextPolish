"use client";

import React from "react";
import Image from "next/image";
import { motion, useReducedMotion } from "framer-motion";
import { Sparkles, PlayCircle, Command } from "lucide-react";

export default function Hero() {
  const shouldReduceMotion = useReducedMotion();

  const fadeUp = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 },
  };

  const scrollToBeta = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    document.getElementById("beta")?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section className="relative overflow-hidden bg-[#FAFAFA] pt-36 pb-12 sm:pt-40 md:pt-44 lg:pt-48 lg:pb-16">
      {/* Subtle background glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-[1000px] h-[500px] bg-[#7C3AED]/5 blur-[120px] rounded-full pointer-events-none" />

      <div className="mx-auto max-w-[1200px] px-6 relative z-10">
        <div className="grid lg:grid-cols-[0.9fr_1.1fr] gap-10 lg:gap-16 items-center">

          {/* LEFT: Copy & CTAs */}
          <div className="max-w-[560px]">
            {/* Premium Badge */}
            <motion.div
              initial={shouldReduceMotion ? false : "hidden"}
              animate={shouldReduceMotion ? undefined : "visible"}
              variants={fadeUp}
              transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
              className="inline-flex items-center gap-2.5 rounded-full bg-white border border-[#7C3AED]/20 px-3 py-1.5 shadow-sm mb-8"
            >
              <div className="flex items-center justify-center w-5 h-5 rounded-full bg-[#7C3AED]/10">
                <Sparkles className="w-3 h-3 text-[#7C3AED]" />
              </div>
              <span className="text-xs font-bold text-[#7C3AED] tracking-wide uppercase pr-1">
                Local AI • Zero Cloud
              </span>
            </motion.div>

            {/* Headline */}
            <motion.h1
              initial={shouldReduceMotion ? false : "hidden"}
              animate={shouldReduceMotion ? undefined : "visible"}
              variants={fadeUp}
              transition={{ duration: 0.6, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
              className="text-4xl sm:text-6xl lg:text-[72px] font-extrabold text-neutral-900 tracking-tight leading-[1.05]"
            >
              Select text. <br />
              Improve it <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#7C3AED] to-[#a06af9]">instantly.</span>
            </motion.h1>

            {/* Subheadline */}
            <motion.p
              initial={shouldReduceMotion ? false : "hidden"}
              animate={shouldReduceMotion ? undefined : "visible"}
              variants={fadeUp}
              transition={{ duration: 0.6, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
              className="mt-6 text-lg sm:text-xl font-medium leading-relaxed text-neutral-500 max-w-[480px]"
            >
              Avelyn lives in your menu bar. Highlight anywhere, hit your shortcut, and let local AI rewrite, refine, and perfect your text.
            </motion.p>

            {/* Buttons */}
            <motion.div
              initial={shouldReduceMotion ? false : "hidden"}
              animate={shouldReduceMotion ? undefined : "visible"}
              variants={fadeUp}
              transition={{ duration: 0.6, delay: 0.3, ease: [0.16, 1, 0.3, 1] }}
              className="mt-10 flex flex-col sm:flex-row gap-4"
            >
              {/* UPDATED: Early Beta Access Button */}
              <a
                href="#beta"
                onClick={scrollToBeta}
                className="group flex items-center justify-center gap-2 rounded-full bg-[#0E0E11] px-8 py-4 text-sm font-semibold text-white shadow-xl shadow-black/10 transition-all hover:bg-neutral-800 hover:scale-[1.02] active:scale-[0.98]"
              >
                <Sparkles className="w-4 h-4 text-neutral-300 group-hover:text-white transition-colors" />
                Early Beta Access
              </a>

              <a
                href="#how-it-works"
                className="group flex items-center justify-center gap-2 rounded-full border border-neutral-200 bg-white px-8 py-4 text-sm font-semibold text-neutral-900 shadow-sm transition-all hover:bg-neutral-50 hover:border-neutral-300 hover:scale-[1.02] active:scale-[0.98]"
              >
                <PlayCircle className="w-4 h-4 text-neutral-400 group-hover:text-[#7C3AED] transition-colors" />
                Watch Demo
              </a>
            </motion.div>

            {/* Keyboard shortcut hint */}
            <motion.div
              initial={shouldReduceMotion ? false : { opacity: 0 }}
              animate={shouldReduceMotion ? undefined : { opacity: 1 }}
              transition={{ delay: 0.6, duration: 0.8 }}
              className="mt-8 flex items-center gap-2 text-sm text-neutral-400 font-medium"
            >
              Press
              <kbd className="flex items-center gap-1 font-sans bg-white border border-neutral-200 shadow-sm rounded px-2 py-1 text-xs text-neutral-600">
                <Command className="w-3 h-3" /> Shift E
              </kbd>
              to trigger anywhere.
            </motion.div>
          </div>

          {/* RIGHT: Visual Presentation */}
          <motion.div
            initial={shouldReduceMotion ? false : { opacity: 0, x: 40, scale: 0.95 }}
            animate={shouldReduceMotion ? undefined : { opacity: 1, x: 0, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
            className="relative"
          >
            {/* Image Ambient Glow */}
            <div className="absolute inset-0 -z-10 bg-[#7C3AED]/20 blur-[80px] rounded-full scale-90" />

            {/* Premium macOS Window Frame */}
            <div className="rounded-[24px] border border-neutral-200/60 bg-white/50 p-2 shadow-2xl shadow-[#7C3AED]/10 backdrop-blur-xl">
              <div className="overflow-hidden rounded-[16px] bg-white border border-neutral-100 shadow-sm">

                {/* macOS Title Bar */}
                <div className="flex items-center gap-2 px-4 py-3 bg-neutral-50 border-b border-neutral-100">
                  <div className="w-3 h-3 rounded-full bg-[#FF5F56] border border-[#E0443E]" />
                  <div className="w-3 h-3 rounded-full bg-[#FFBD2E] border border-[#DEA123]" />
                  <div className="w-3 h-3 rounded-full bg-[#27C93F] border border-[#1AAB29]" />
                </div>

                {/* EXACT Original Image Implementation */}
                <Image
                  src="/images/hero_image.png"
                  alt="Avelyn Settings"
                  width={2048}
                  height={2048}
                  priority
                  className="w-full max-h-[520px] object-cover object-top"
                />
              </div>
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  );
}