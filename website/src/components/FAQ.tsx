"use client";

import React, { useState } from "react";
import { ChevronDown } from "lucide-react";
import { motion, AnimatePresence, useReducedMotion } from "framer-motion";

export default function FAQ() {
  const shouldReduceMotion = useReducedMotion();
  const ease = [0.16, 1, 0.3, 1] as const;

  const faqs = [
    {
      q: "Does it work offline?",
      a: "Yes, 100%. When configured with Ollama (Local Offline), Avelyn performs all LLM calculations locally on your CPU or GPU without requiring any active internet connection.",
    },
    {
      q: "Does it require Ollama?",
      a: "Avelyn defaults to Ollama for privacy-first, offline execution. However, you can easily configure alternative standard API providers (like Gemini or OpenAI) inside the settings panel if you prefer not to host model binaries locally.",
    },
    {
      q: "Is my data private?",
      a: "Absolutely. Avelyn only captures clipboard content when you trigger the global shortcut Ctrl+Shift+E, holds it in local memory during enhancement, and immediately restores your original clipboard history afterwards. No logs of your text are written to disk or sent to the cloud.",
    },
    {
      q: "Which local models are supported?",
      a: "Avelyn supports any model available on Ollama! The default recommended model is 'gemma3:4b' (a lightweight, blazing-fast model that starts in less than 1.5s), but you can easily use llama3, mistral, or codegemma by inputting the model name in Settings.",
    },
    {
      q: "Does it work everywhere on macOS?",
      a: "Yes. Once you grant standard Accessibility permissions (required to simulate standard copy/paste events) and Input Monitoring (required to detect the global hotkey), Avelyn works system-wide in any editable text field—including Safari, Chrome, Slack, VS Code, Word, and textareas.",
    },
  ];

  const [openIdx, setOpenIdx] = useState<number | null>(null);

  return (
    <section id="faq" className="py-20 bg-white border-b border-neutral-100/60">
      <div className="max-w-[720px] mx-auto px-6">
        {/* Section Header */}
        <motion.div
          initial={shouldReduceMotion ? false : { opacity: 0, y: 10 }}
          whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
          viewport={shouldReduceMotion ? undefined : { once: true, amount: 0.4 }}
          transition={{ duration: 0.55, ease }}
          className="text-center space-y-3 mb-16"
        >
          <h2 className="text-xs font-bold text-[#7C3AED] uppercase tracking-widest">FAQ</h2>
          <p className="text-2xl sm:text-3xl font-extrabold text-[#0E0E11] tracking-tight">
            Frequently Asked Questions
          </p>
        </motion.div>

        {/* Accordions */}
        <motion.div
          initial={shouldReduceMotion ? false : { opacity: 0, y: 10 }}
          whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
          viewport={shouldReduceMotion ? undefined : { once: true, amount: 0.2 }}
          transition={{ duration: 0.6, delay: 0.05, ease }}
          className="space-y-4 text-left"
        >
          {faqs.map((faq, idx) => {
            const isOpen = openIdx === idx;
            return (
              <div
                key={idx}
                className="bg-white border border-neutral-200/50 hover:border-neutral-200 rounded-2xl overflow-hidden transition-all duration-200"
              >
                <button
                  onClick={() => setOpenIdx(isOpen ? null : idx)}
                  className="w-full flex items-center justify-between p-5 text-left font-bold text-sm text-[#0E0E11] focus:outline-none cursor-pointer select-none"
                >
                  <span>{faq.q}</span>
                  <ChevronDown
                    className={`w-4 h-4 text-neutral-400 transition-transform duration-200 ${
                      isOpen ? "rotate-180 text-[#7C3AED]" : ""
                    }`}
                  />
                </button>

                <AnimatePresence initial={false}>
                  {isOpen && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: shouldReduceMotion ? 0 : 0.25, ease }}
                    >
                      <div className="px-5 pb-5 pt-0 text-xs sm:text-sm text-neutral-500 font-medium leading-relaxed border-t border-neutral-100/40">
                        {faq.a}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            );
          })}
        </motion.div>
      </div>
    </section>
  );
}
