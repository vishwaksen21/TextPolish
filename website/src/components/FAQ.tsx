"use client";

import React, { useState } from "react";
import { Plus } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function FAQ() {
  const ease = [0.16, 1, 0.3, 1] as const;

  const faqs = [
    {
      q: "Does it work offline?",
      a: "Yes, 100%. When configured with Local Ollama, Avelyn performs all LLM calculations locally on your CPU or GPU without requiring an internet connection. It is ideal for air-gapped systems or secure environments.",
    },
    {
      q: "How does the hybrid multi-provider architecture work?",
      a: "Avelyn supports Local Ollama, Avelyn Cloud (powered by OpenRouter), and Custom API endpoints. You can run in Single Provider mode, configure specific Route Overrides per task group (Smart Router), or use Auto Provider mode which dynamically switches between local privacy and cloud horsepower depending on text length and task classification.",
    },
    {
      q: "Are my API keys secure?",
      a: "Absolutely. All API keys are stored strictly in local configuration files on your machine. Within the settings UI, keys are masked with secure password bullet points to prevent over-the-shoulder leaks. Avelyn has zero cloud analytics or telemetry trackers, guaranteeing complete data sovereignty.",
    },
    {
      q: "Can I cancel a running generation?",
      a: "Yes. Avelyn provides immediate generation cancellation. If a model is taking too long or you change your mind mid-prompt, you can click cancel to halt the stream instantly, saving local CPU/GPU cycles and API tokens.",
    },
    {
      q: "Which models are supported?",
      a: "For local execution, you can run Gemma 3, Llama 3, Mistral, or custom Modelfiles via Ollama. For cloud execution, you can use GPT-4o Mini, Claude 3.5 Haiku, Gemini 2.5 Flash, and other models. Custom APIs allow you to connect LM Studio, vLLM, or any OpenAI-compatible endpoint.",
    },
    {
      q: "Does it work everywhere on macOS?",
      a: "Yes. Once you grant standard macOS Accessibility permissions (required to simulate standard copy/paste events) and Input Monitoring (required to detect the global hotkey), Avelyn works system-wide in any editable text field—including Safari, Chrome, Slack, VS Code, Word, and textareas.",
    },
  ];

  const [openIdx, setOpenIdx] = useState<number | null>(0); // Default to first item open

  return (
    <section id="faq" className="py-16 md:py-24 lg:py-32 bg-[#F5F5F7]">
      <div className="max-w-[1200px] mx-auto px-6">

        {/* Centered Minimalist Header */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.6, ease }}
          className="text-center mb-16"
        >
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="h-[1px] w-6 bg-[#7C3AED]"></div>
            <span className="text-sm font-semibold text-[#7C3AED] uppercase tracking-widest">
              FAQ
            </span>
            <div className="h-[1px] w-6 bg-[#7C3AED]"></div>
          </div>
          <h2 className="text-4xl md:text-5xl font-extrabold text-neutral-900 tracking-tight leading-tight mb-6">
            Frequently Asked <br className="hidden sm:block" />
            Questions
          </h2>
        </motion.div>

        {/* Floating Island Accordions */}
        <div className="max-w-[840px] mx-auto space-y-4">
          {faqs.map((faq, idx) => {
            const isOpen = openIdx === idx;
            return (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.1 }}
                transition={{ duration: 0.5, delay: idx * 0.05, ease }}
                className={`relative bg-white rounded-[24px] transition-all duration-500 overflow-hidden ${isOpen
                    ? "shadow-lg shadow-[#7C3AED]/5 border border-[#7C3AED]/20"
                    : "shadow-sm hover:shadow-md border border-neutral-200/60"
                  }`}
              >
                <button
                  onClick={() => setOpenIdx(isOpen ? null : idx)}
                  className="w-full flex items-center justify-between p-6 md:p-8 text-left focus:outline-none group"
                >
                  <span className={`text-lg md:text-xl font-bold tracking-tight transition-colors duration-300 pr-6 ${isOpen ? "text-neutral-900" : "text-neutral-700 group-hover:text-neutral-900"
                    }`}>
                    {faq.q}
                  </span>

                  {/* Premium Morphing Icon */}
                  <div className={`shrink-0 flex items-center justify-center w-10 h-10 rounded-full transition-all duration-500 ${isOpen
                      ? "bg-[#EDE9FE] text-[#7C3AED] rotate-45"
                      : "bg-neutral-50 text-neutral-400 group-hover:bg-neutral-100 group-hover:text-neutral-600"
                    }`}>
                    <Plus className="w-5 h-5 transition-transform duration-500" />
                  </div>
                </button>

                <AnimatePresence initial={false}>
                  {isOpen && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.4, ease }}
                    >
                      <div className="px-6 md:px-8 pb-8 pt-0">
                        <div className="w-full h-px bg-neutral-100 mb-6" />
                        <p className="text-base md:text-lg text-neutral-500 font-medium leading-relaxed">
                          {faq.a}
                        </p>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            );
          })}
        </div>

      </div>
    </section>
  );
}