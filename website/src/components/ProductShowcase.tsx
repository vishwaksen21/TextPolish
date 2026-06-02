"use client";

import React from "react";
import { motion } from "framer-motion";
import { Shield, Sparkles, Sliders } from "lucide-react";

export default function ProductShowcase() {
  const ease = [0.16, 1, 0.3, 1] as const;

  return (
    <section className="py-16 md:py-24 bg-white overflow-hidden">
      <div className="max-w-[1200px] mx-auto px-6">

        {/* Minimalist Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.6, ease }}
          className="text-center max-w-[600px] mx-auto mb-20"
        >
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="h-[1px] w-8 bg-[#7C3AED]"></div>
            <h2 className="text-sm font-semibold text-[#7C3AED] uppercase tracking-widest">
              Native Experience
            </h2>
            <div className="h-[1px] w-8 bg-[#7C3AED]"></div>
          </div>
          <h3 className="text-4xl md:text-5xl font-extrabold text-neutral-900 tracking-tight leading-[1.1] mb-6">
            Feels like it belongs <br className="hidden sm:block" />
            on your Mac.
          </h3>
          <p className="text-lg text-neutral-500 font-medium leading-relaxed">
            Take a closer look at the actual product layout, designed to blend seamlessly with macOS Sonoma & Sequoia.
          </p>
        </motion.div>

        {/* Premium Asymmetric Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8">

          {/* FEATURE 1: Menu Bar (Full Width, Dark Mode Card) */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.7, ease }}
            className="md:col-span-2 bg-[#0E0E11] rounded-[32px] p-6 md:p-12 lg:p-16 flex flex-col md:flex-row items-center gap-6 md:gap-12 overflow-hidden relative group"
          >
            {/* Subtle background glow */}
            <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-[#7C3AED]/20 blur-[120px] rounded-full pointer-events-none translate-x-1/3 -translate-y-1/3 transition-transform duration-700 group-hover:scale-110" />

            <div className="w-full md:w-1/2 space-y-6 relative z-10">
              <div className="w-12 h-12 rounded-2xl bg-white/10 flex items-center justify-center backdrop-blur-md border border-white/10">
                <Sliders className="w-6 h-6 text-[#7C3AED]" />
              </div>
              <h4 className="text-3xl lg:text-4xl font-bold text-white tracking-tight">
                Zero-Intrusion <br /> Menu Bar Experience
              </h4>
              <p className="text-lg text-neutral-400 font-medium leading-relaxed max-w-[400px]">
                Avelyn operates entirely in the background, living in your macOS Menu Bar. Trigger it with a keystroke, adjust settings in two clicks, and keep your screen 100% focused on your actual work.
              </p>
            </div>

            <div className="w-full md:w-1/2 relative flex justify-center md:justify-end mt-8 md:mt-0">
              <img
                src="/screenshots/media__1779910881149.png"
                alt="Menu Bar Operation"
                className="w-full max-w-[450px] object-contain drop-shadow-[0_30px_60px_rgba(0,0,0,0.5)] transition-transform duration-700 group-hover:scale-105 select-none"
              />
            </div>
          </motion.div>

          {/* FEATURE 2: Setup Wizard (Half Width, Light Card) */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.7, delay: 0.1, ease }}
            className="bg-[#F5F5F7] rounded-[32px] p-6 md:p-12 flex flex-col overflow-hidden relative group"
          >
            <div className="space-y-5 relative z-10 mb-12">
              <div className="w-12 h-12 rounded-2xl bg-white flex items-center justify-center border border-neutral-200/60 shadow-sm">
                <Sparkles className="w-6 h-6 text-[#7C3AED]" />
              </div>
              <h4 className="text-2xl lg:text-3xl font-bold text-neutral-900 tracking-tight">
                First-Run <br /> Setup Wizard
              </h4>
              <p className="text-base text-neutral-500 font-medium leading-relaxed">
                Getting started with local offline AI should be simple. A premium, step-by-step setup wizard guides you perfectly through model selection and global hotkey preferences.
              </p>
            </div>

            {/* Image bleeds off the bottom */}
            <div className="mt-auto relative flex justify-center -mb-8 md:-mb-12">
              <img
                src="/screenshots/media__1780175716131.png"
                alt="Onboarding Wizard"
                className="w-full max-w-[380px] object-cover rounded-t-2xl drop-shadow-2xl border border-neutral-200/50 transition-transform duration-700 group-hover:-translate-y-3 select-none"
              />
            </div>
          </motion.div>

          {/* FEATURE 3: Permissions (Half Width, Light Card) */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.7, delay: 0.2, ease }}
            className="bg-[#F5F5F7] rounded-[32px] p-6 md:p-12 flex flex-col overflow-hidden relative group"
          >
            <div className="space-y-5 relative z-10 mb-12">
              <div className="w-12 h-12 rounded-2xl bg-white flex items-center justify-center border border-neutral-200/60 shadow-sm">
                <Shield className="w-6 h-6 text-[#7C3AED]" />
              </div>
              <h4 className="text-2xl lg:text-3xl font-bold text-neutral-900 tracking-tight">
                Self-Healing <br /> Permission Assistant
              </h4>
              <p className="text-base text-neutral-500 font-medium leading-relaxed">
                No more troubleshooting terminal commands. Avelyn features a native helper to assist you with macOS Accessibility and Input permissions so global paste events function securely.
              </p>
            </div>

            {/* Image bleeds off the bottom */}
            <div className="mt-auto relative flex justify-center -mb-8 md:-mb-12">
              <img
                src="/screenshots/media__1780177499012.png"
                alt="Security & Permissions"
                className="w-full max-w-[380px] object-cover rounded-t-2xl drop-shadow-2xl border border-neutral-200/50 transition-transform duration-700 group-hover:-translate-y-3 select-none"
              />
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  );
}