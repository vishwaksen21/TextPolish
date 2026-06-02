"use client";

import React from "react";
import {
  Fingerprint,
  Zap,
  BrainCircuit,
  Feather,
  WandSparkles,
  CheckCheck,
  AppWindow
} from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";

export default function FeaturesBento() {
  const shouldReduceMotion = useReducedMotion();
  const ease = [0.16, 1, 0.3, 1] as const;

  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1, delayChildren: 0.2 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { duration: 0.6, ease } },
  };

  return (
    <section id="features" className="py-16 md:py-24 bg-[#FAFAFA]">
      <div className="max-w-[1200px] mx-auto px-6">

        {/* Minimalist Section Header */}
        <motion.div
          initial={shouldReduceMotion ? false : { opacity: 0, y: 15 }}
          whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
          viewport={shouldReduceMotion ? undefined : { once: true, amount: 0.3 }}
          transition={{ duration: 0.6, ease }}
          className="mb-10 md:mb-20"
        >
          <div className="flex items-center gap-3 mb-4">
            <div className="h-[1px] w-8 bg-[#7C3AED]"></div>
            <h2 className="text-sm font-semibold text-[#7C3AED] uppercase tracking-widest">
              The Arsenal
            </h2>
          </div>
          <p className="text-4xl md:text-5xl font-extrabold text-neutral-900 tracking-tight leading-[1.1]">
            Everything you need. <br className="hidden sm:block" />
            <span className="text-neutral-400">Nothing you don't.</span>
          </p>
        </motion.div>

        {/* Bento Grid Layout */}
        <motion.div
          variants={shouldReduceMotion ? undefined : containerVariants}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, amount: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-4 grid-rows-[auto] gap-6"
        >
          {/* Hero Card: Privacy & Local AI (Spans 2 columns, 2 rows) */}
          <motion.div
            variants={itemVariants}
            className="md:col-span-2 md:row-span-2 bg-[#7C3AED] rounded-[2rem] p-8 md:p-10 flex flex-col justify-between relative overflow-hidden group shadow-xl shadow-[#7C3AED]/10"
          >
            {/* Subtle background decoration */}
            <div className="absolute -bottom-24 -right-24 w-80 h-80 bg-white opacity-5 rounded-full blur-3xl group-hover:scale-110 transition-transform duration-700"></div>

            <div className="w-14 h-14 bg-white/20 backdrop-blur-md rounded-2xl flex items-center justify-center mb-16 shadow-inner ring-1 ring-white/30">
              <Fingerprint className="w-7 h-7 text-white" />
            </div>

            <div className="relative z-10">
              <h3 className="text-2xl md:text-3xl font-bold text-white mb-3 tracking-tight">
                Absolute Privacy. <br /> 100% Local AI.
              </h3>
              <p className="text-white/80 font-medium leading-relaxed text-sm md:text-base max-w-sm">
                Your data never leaves your physical memory. Harness Llama 3, Gemma, or Mistral natively via Ollama with zero cloud processing and zero telemetry.
              </p>
            </div>
          </motion.div>

          {/* Wide Card: Global Shortcut */}
          <motion.div
            variants={itemVariants}
            className="md:col-span-2 bg-white border border-neutral-200/60 rounded-[2rem] p-8 hover:shadow-lg hover:shadow-neutral-200/40 transition-all duration-300"
          >
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-xl font-bold text-neutral-900 mb-2">Lightning Fast</h3>
                <p className="text-neutral-500 text-sm font-medium leading-relaxed max-w-[260px]">
                  Highlight any text, anywhere. Hit <kbd className="bg-neutral-100 text-neutral-700 px-2 py-1 rounded-md text-xs border border-neutral-200 mx-1">Ctrl+Shift+E</kbd> and Avelyn replaces it instantly.
                </p>
              </div>
              <div className="w-12 h-12 bg-[#EDE9FE]/50 rounded-2xl flex items-center justify-center ring-1 ring-[#7C3AED]/10">
                <Zap className="w-6 h-6 text-[#7C3AED]" />
              </div>
            </div>
          </motion.div>

          {/* Square Card: Smart Assist */}
          <motion.div
            variants={itemVariants}
            className="bg-white border border-neutral-200/60 rounded-[2rem] p-8 flex flex-col hover:border-[#7C3AED]/30 transition-all duration-300"
          >
            <BrainCircuit className="w-7 h-7 text-[#7C3AED] mb-6" />
            <h3 className="text-lg font-bold text-neutral-900 mb-2">Context Aware</h3>
            <p className="text-neutral-500 text-sm font-medium leading-relaxed">
              Automatically detects your tone and intent to generate structural adjustments that feel human.
            </p>
          </motion.div>

          {/* Square Card: Elevate Writing */}
          <motion.div
            variants={itemVariants}
            className="bg-white border border-neutral-200/60 rounded-[2rem] p-8 flex flex-col hover:border-[#7C3AED]/30 transition-all duration-300"
          >
            <Feather className="w-7 h-7 text-[#7C3AED] mb-6" />
            <h3 className="text-lg font-bold text-neutral-900 mb-2">Polished Prose</h3>
            <p className="text-neutral-500 text-sm font-medium leading-relaxed">
              Fix awkward phrasing, upgrade your vocabulary, and tighten sentences for maximum impact.
            </p>
          </motion.div>

          {/* Wide Card: Universal Support */}
          <motion.div
            variants={itemVariants}
            className="md:col-span-2 bg-white border border-neutral-200/60 rounded-[2rem] p-8 flex flex-col md:flex-row md:items-center gap-6 hover:shadow-lg hover:shadow-neutral-200/40 transition-all duration-300"
          >
            <div className="w-12 h-12 shrink-0 bg-[#EDE9FE]/50 rounded-2xl flex items-center justify-center ring-1 ring-[#7C3AED]/10">
              <AppWindow className="w-6 h-6 text-[#7C3AED]" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-neutral-900 mb-2">Universal Integration</h3>
              <p className="text-neutral-500 text-sm font-medium leading-relaxed">
                Functions flawlessly across VS Code, Chrome, Word, Slack, Notion, and literally any editable text interface system-wide.
              </p>
            </div>
          </motion.div>

          {/* Square Card: Prompt Engineering */}
          <motion.div
            variants={itemVariants}
            className="bg-white border border-neutral-200/60 rounded-[2rem] p-8 flex flex-col hover:border-[#7C3AED]/30 transition-all duration-300"
          >
            <WandSparkles className="w-7 h-7 text-[#7C3AED] mb-6" />
            <h3 className="text-lg font-bold text-neutral-900 mb-2">Auto-Prompts</h3>
            <p className="text-neutral-500 text-sm font-medium leading-relaxed">
              Transform basic instructions into highly optimized prompt structures instantly.
            </p>
          </motion.div>

          {/* Square Card: Grammar */}
          <motion.div
            variants={itemVariants}
            className="bg-white border border-neutral-200/60 rounded-[2rem] p-8 flex flex-col hover:border-[#7C3AED]/30 transition-all duration-300"
          >
            <CheckCheck className="w-7 h-7 text-[#7C3AED] mb-6" />
            <h3 className="text-lg font-bold text-neutral-900 mb-2">Silent Fixes</h3>
            <p className="text-neutral-500 text-sm font-medium leading-relaxed">
              Correct spelling, fix complex syntax, and enforce formatting rules in the background.
            </p>
          </motion.div>

        </motion.div>
      </div>
    </section>
  );
}