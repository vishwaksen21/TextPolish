"use client";

import React from "react";
import { motion, useReducedMotion } from "framer-motion";
import { Shield, Sparkles, Sliders } from "lucide-react";

export default function ProductShowcase() {
  const shouldReduceMotion = useReducedMotion();
  const ease = [0.16, 1, 0.3, 1] as const;

  const cards = [
    {
      badge: "Onboarding Wizard",
      title: "First-Run Setup Wizard",
      desc: "Getting started with local offline AI should be simple. Avelyn walks you through a premium, step-by-step setup wizard that guides you through model selection and global hotkey preferences.",
      screenshot: "/screenshots/media__1780175716131.png",
      span: "lg:col-span-6",
      icon: <Sparkles className="w-4 h-4 text-[#7C3AED]" />
    },
    {
      badge: "Security & Permissions",
      title: "Self-Healing Permission Assistant",
      desc: "No more troubleshooting terminal commands. Avelyn features a native helper to assist you with macOS Accessibility and Input Monitoring permissions so global paste events function securely and smoothly.",
      screenshot: "/screenshots/media__1780177499012.png",
      span: "lg:col-span-6",
      icon: <Shield className="w-4 h-4 text-[#7C3AED]" />
    },
    {
      badge: "Sleek Menu Bar Operation",
      title: "Zero-Intrusion Menu Bar Experience",
      desc: "Avelyn operates entirely in the background, living in your system tray / macOS Menu Bar. Trigger it with a keystroke, change quick-settings in two clicks, and keep your screen 100% focused on your actual work.",
      screenshot: "/screenshots/media__1779910881149.png",
      span: "lg:col-span-12",
      icon: <Sliders className="w-4 h-4 text-[#7C3AED]" />,
      isHorizontal: true
    }
  ];

  return (
    <section className="py-20 bg-neutral-50/50 border-b border-neutral-100/60 text-neutral-800">
      <div className="max-w-[1100px] mx-auto px-6">
        {/* Section Header */}
        <motion.div
          initial={shouldReduceMotion ? false : { opacity: 0, y: 10 }}
          whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
          viewport={shouldReduceMotion ? undefined : { once: true, amount: 0.3 }}
          transition={{ duration: 0.55, ease }}
          className="text-center max-w-[600px] mx-auto space-y-4 mb-16"
        >
          <span className="text-xs font-bold text-[#7C3AED] uppercase tracking-widest bg-[#EDE9FE]/50 px-3.5 py-1 rounded-full border border-[#EDE9FE]">
            Premium Design
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-[#0E0E11] tracking-tight">
            Designed to Feel Native
          </h2>
          <p className="text-sm text-neutral-500 font-medium leading-relaxed">
            Take a closer look at the actual product layout, designed to blend seamlessly with macOS Sonoma & Sequoia.
          </p>
        </motion.div>

        {/* Dynamic Product Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {cards.map((card, idx) => (
            <motion.div
              key={card.title}
              initial={shouldReduceMotion ? false : { opacity: 0, y: 14 }}
              whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
              viewport={shouldReduceMotion ? undefined : { once: true, amount: 0.2 }}
              transition={{ duration: 0.6, delay: idx * 0.06, ease }}
              className={`${card.span} bg-white border border-neutral-200/50 rounded-2xl p-6 md:p-8 flex flex-col justify-between shadow-[0_1px_3px_rgba(0,0,0,0.01)] hover:shadow-lg hover:shadow-neutral-200/25 hover:border-neutral-300 transition-all duration-300 group`}
            >
              {/* Card Meta & Header */}
              <div className="space-y-4 text-left">
                <div className="flex items-center gap-2">
                  <div className="w-7 h-7 rounded-lg bg-[#EDE9FE]/50 border border-[#EDE9FE] flex items-center justify-center">
                    {card.icon}
                  </div>
                  <span className="text-[10px] font-bold text-neutral-400 uppercase tracking-widest">
                    {card.badge}
                  </span>
                </div>

                <div className="space-y-2">
                  <h3 className="text-xl font-extrabold text-[#0E0E11] tracking-tight">
                    {card.title}
                  </h3>
                  <p className="text-xs sm:text-sm text-neutral-500 font-medium leading-relaxed max-w-[500px]">
                    {card.desc}
                  </p>
                </div>
              </div>

              {/* Real App Screenshot displaying native container style */}
              <div className="mt-8 overflow-hidden rounded-xl border border-neutral-200/60 bg-[#F5F5F7] p-2 select-none">
                <div className="bg-white rounded-lg overflow-hidden border border-neutral-200/30 shadow-inner flex items-center justify-center">
                  <img
                    src={card.screenshot}
                    alt={card.title}
                    className={`w-full object-cover select-none pointer-events-none transition-transform duration-500 group-hover:scale-[1.01] ${
                      card.isHorizontal ? "max-h-[140px] md:max-h-[180px] object-contain p-2" : "h-auto"
                    }`}
                  />
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
