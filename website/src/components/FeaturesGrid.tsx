"use client";

import React from "react";
import { Sparkles, PenTool, CheckCircle, FileText, Lock, Keyboard, Cpu, HelpCircle } from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";

export default function FeaturesGrid() {
  const shouldReduceMotion = useReducedMotion();
  const ease = [0.16, 1, 0.3, 1] as const;

  const features = [
    {
      icon: <Sparkles className="w-5 h-5 text-[#7C3AED]" />,
      title: "Smart Assist",
      desc: "Automatically detects intent, tone context, and intent vectors to produce refined structural adjustments instantly.",
    },
    {
      icon: <PenTool className="w-5 h-5 text-[#7C3AED]" />,
      title: "Improve Writing",
      desc: "Polishes abstract phrasing, tightens sentences, and enhances overall vocabulary for high-end professional impact.",
    },
    {
      icon: <FileText className="w-5 h-5 text-[#7C3AED]" />,
      title: "Improve Prompt",
      desc: "Transforms simple instructions into highly engineered prompt formats with zero manual restructuring required.",
    },
    {
      icon: <CheckCircle className="w-5 h-5 text-[#7C3AED]" />,
      title: "Fix Grammar",
      desc: "Corrects spelling mistakes, syntax, and complex structural formatting rules silently in the background.",
    },
    {
      icon: <Lock className="w-5 h-5 text-[#7C3AED]" />,
      title: "Privacy First",
      desc: "All data stays 100% local. Zero network logs are stored, and clipboard text never leaves your physical memory.",
    },
    {
      icon: <Keyboard className="w-5 h-5 text-[#7C3AED]" />,
      title: "Global Shortcut",
      desc: "Simply highlight text anywhere and press Ctrl+Shift+E. Avelyn captures and replaces content instantly.",
    },
    {
      icon: <Cpu className="w-5 h-5 text-[#7C3AED]" />,
      title: "Local AI Engines",
      desc: "Harness local llama3, gemma3, or mistral models directly via Ollama. 100% offline with zero cloud latency.",
    },
    {
      icon: <HelpCircle className="w-5 h-5 text-[#7C3AED]" />,
      title: "Works Everywhere",
      desc: "Works inside VS Code, Safari, Chrome, Word, Slack, Notion, and any editable text interface system-wide.",
    },
  ];

  return (
    <section id="features" className="py-20 bg-neutral-50/50 border-b border-neutral-100/60">
      <div className="max-w-[1100px] mx-auto px-6">
        {/* Section Header */}
        <motion.div
          initial={shouldReduceMotion ? false : { opacity: 0, y: 10 }}
          whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
          viewport={shouldReduceMotion ? undefined : { once: true, amount: 0.3 }}
          transition={{ duration: 0.55, ease }}
          className="text-center max-w-[500px] mx-auto space-y-3 mb-16"
        >
          <h2 className="text-xs font-bold text-[#7C3AED] uppercase tracking-widest">Core Capabilities</h2>
          <p className="text-2xl sm:text-3xl font-extrabold text-[#0E0E11] tracking-tight">
            Designed for high performance. Built for privacy.
          </p>
        </motion.div>

        {/* Feature Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feat, idx) => (
            <motion.div
              key={feat.title}
              initial={shouldReduceMotion ? false : { opacity: 0, y: 10 }}
              whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
              viewport={shouldReduceMotion ? undefined : { once: true, amount: 0.2 }}
              transition={{ duration: 0.55, delay: idx * 0.04, ease }}
              className="bg-white border border-neutral-200/50 hover:border-neutral-200 p-6 rounded-2xl shadow-[0_1px_3px_rgba(0,0,0,0.01)] hover:shadow-lg hover:shadow-neutral-200/20 transition-all duration-300 flex flex-col justify-between text-left"
            >
              <div className="space-y-4">
                <div className="w-10 h-10 rounded-xl bg-[#EDE9FE]/40 flex items-center justify-center">
                  {feat.icon}
                </div>
                <h3 className="text-sm font-bold text-[#0E0E11]">{feat.title}</h3>
                <p className="text-xs text-neutral-500 font-medium leading-relaxed">
                  {feat.desc}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
