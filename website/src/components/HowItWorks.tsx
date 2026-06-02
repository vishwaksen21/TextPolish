"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MousePointerClick, Keyboard, Wand2, Cpu, RefreshCw, Layers } from "lucide-react";

export default function HowItWorks() {
  const [activeStep, setActiveStep] = useState(0);

  const steps = [
    {
      num: "01",
      icon: <MousePointerClick className="w-5 h-5" />,
      tabTitle: "Highlight",
      title: "Highlight Any Text Block",
      desc: "Simply select the text you want to rewrite, enhance, or explain. It works system-wide in any macOS application.",
      bullets: [
        "Works in Safari, Chrome, Slack, Notion, Word, and textareas.",
        "Compatible with raw code blocks inside VS Code and terminals.",
        "No extensions required — native system-wide integration."
      ],
      screenshot: "/images/step1.png",
      alt: "Avelyn text highlight step"
    },
    {
      num: "02",
      icon: <Keyboard className="w-5 h-5" />,
      tabTitle: "Shortcut",
      title: "Trigger the Global Hotkey",
      desc: "Press your customizable global hotkey (defaults to Ctrl+Shift+E). Avelyn instantly captures the highlighted text into secure memory.",
      bullets: [
        "Zero-latency background clipboard capture mechanics.",
        "Customizable triggers (e.g., Command+Shift+K) via Settings.",
        "App focus stays 100% stable without background interruption."
      ],
      screenshot: "/screenshots/step2_shortcut.png",
      alt: "Avelyn keyboard trigger step"
    },
    {
      num: "03",
      icon: <Layers className="w-5 h-5" />,
      tabTitle: "Palette",
      title: "Command Palette Appears",
      desc: "A floating, glassmorphic Raycast-grade Command Palette instantly snaps to your cursor location on top of your active application.",
      bullets: [
        "Elegant frosted glass backing with a premium drop shadow.",
        "Fuzzy search filters instantly through multiple AI actions.",
        "Clean, system-native keyboard-navigable interface."
      ],
      screenshot: "/images/step3.png",
      alt: "Avelyn Command Palette appearing"
    },
    {
      num: "04",
      icon: <Wand2 className="w-5 h-5" />,
      tabTitle: "Action",
      title: "Choose Your AI Action",
      desc: "Fuzzy search or arrow down to choose an action. Choose from Smart Assist, Improve Writing, Fix Grammar, or write custom prompts.",
      bullets: [
        "Improve Prompt turns raw notes into high-fidelity prompt templates.",
        "Explain Code analyzes and documents highlighted code lines.",
        "Write custom rules inline for highly specific instructions."
      ],
      screenshot: "/images/step4.png",
      alt: "Selecting AI action in Command Palette"
    },
    {
      num: "05",
      icon: <Cpu className="w-5 h-5" />,
      tabTitle: "Enhance",
      title: "Watch AI Enhance in Real-Time",
      desc: "Avelyn runs local offline inference (via Ollama) or secure cloud inference. Watch the improved text stream token-by-token.",
      bullets: [
        "Local inference with llama3, gemma3, or mistral models.",
        "Token-by-token streaming popup lets you preview changes instantly.",
        "Works 100% offline with zero cloud telemetry or data leaks."
      ],
      screenshot: "/images/step5.png",
      alt: "Avelyn real-time streaming text enhancement popup"
    },
    {
      num: "06",
      icon: <RefreshCw className="w-5 h-5" />,
      tabTitle: "Replace",
      title: "Auto-Replace In-Place",
      desc: "Press Enter to accept. Avelyn automatically pastes the polished text back, replacing your original selection.",
      bullets: [
        "Seamless in-place text swap with zero manual copy-pasting.",
        "Press Escape anytime to undo and restore original text instantly.",
        "Original clipboard history is fully restored after replacement."
      ],
      screenshot: "/images/step6.png",
      alt: "Avelyn automatically pasting polished text back in place"
    }
  ];

  return (
    <section id="how-it-works" className="py-20 lg:py-28 bg-white border-b border-neutral-100/60 overflow-hidden text-neutral-800">
      <div className="max-w-[1100px] mx-auto px-6">
        {/* Section Header */}
        <div className="text-center max-w-[600px] mx-auto space-y-4 mb-16">
          <span className="text-xs font-bold text-[#7C3AED] uppercase tracking-widest bg-[#EDE9FE]/50 px-3.5 py-1 rounded-full border border-[#EDE9FE]">
            Product Walkthrough
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-[#0E0E11] tracking-tight">
            See the Actual Product Workflow
          </h2>
          <p className="text-sm text-neutral-500 font-medium leading-relaxed">
            Understand exactly how Avelyn enhances your prose system-wide in seconds. Real screens, real speed, no abstract mockups.
          </p>
        </div>

        {/* Premium Frosted Segmented Control Bar */}
        <div className="flex justify-start md:justify-center overflow-x-auto pb-4 md:pb-0 mb-12 scrollbar-none">
          <div className="flex bg-[#F5F5F7] p-1.5 rounded-2xl border border-neutral-200/60 shrink-0">
            {steps.map((step, idx) => {
              const isActive = activeStep === idx;
              return (
                <button
                  key={step.tabTitle}
                  onClick={() => setActiveStep(idx)}
                  className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-bold transition-all duration-200 cursor-pointer select-none whitespace-nowrap ${
                    isActive
                      ? "bg-white text-[#7C3AED] shadow-sm"
                      : "text-neutral-500 hover:text-[#0E0E11]"
                  }`}
                >
                  <span className={`transition-colors ${isActive ? "text-[#7C3AED]" : "text-neutral-400"}`}>
                    {step.icon}
                  </span>
                  <span>{step.tabTitle}</span>
                  <span className={`text-[10px] ml-0.5 px-1.5 py-0.5 rounded-full ${
                    isActive ? "bg-[#EDE9FE] text-[#7C3AED]" : "bg-neutral-200/50 text-neutral-500"
                  }`}>
                    {step.num}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* 2-Column Content Section */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center min-h-[480px]">
          {/* Left Column: Product Storytelling */}
          <div className="lg:col-span-5 flex flex-col justify-center space-y-6 text-left">
            <AnimatePresence mode="wait">
              <motion.div
                key={activeStep}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 10 }}
                transition={{ duration: 0.35, ease: "easeOut" }}
                className="space-y-6"
              >
                {/* Step counter */}
                <div className="text-sm font-bold text-[#7C3AED] uppercase tracking-widest flex items-center gap-2">
                  <span>Step {steps[activeStep].num}</span>
                  <span className="w-8 h-[1px] bg-[#7C3AED]/40"></span>
                </div>

                {/* Title */}
                <h3 className="text-2xl sm:text-3xl font-extrabold text-[#0E0E11] tracking-tight leading-tight">
                  {steps[activeStep].title}
                </h3>

                {/* Description */}
                <p className="text-sm sm:text-base text-neutral-500 font-medium leading-relaxed">
                  {steps[activeStep].desc}
                </p>

                {/* Bullets */}
                <ul className="space-y-3.5 pt-2 border-t border-neutral-100">
                  {steps[activeStep].bullets.map((bullet, bIdx) => (
                    <li key={bIdx} className="flex gap-2.5 items-start text-xs sm:text-sm text-neutral-600 font-medium">
                      <span className="text-[#7C3AED] mt-1 text-[10px]">✦</span>
                      <span>{bullet}</span>
                    </li>
                  ))}
                </ul>
              </motion.div>
            </AnimatePresence>
          </div>

          {/* Right Column: High-Resolution App Screenshot in macOS Frame */}
          <div className="lg:col-span-7 flex justify-center lg:justify-end items-center">
            <AnimatePresence mode="wait">
              <motion.div
                key={activeStep}
                initial={{ opacity: 0, scale: 0.97, y: 10 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.97, y: -10 }}
                transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
                className="w-full max-w-[560px]"
              >
                {/* Premium macOS Window Frame Wrapper */}
                <div className="bg-white rounded-2xl border border-neutral-200/80 shadow-[0_24px_50px_-12px_rgba(14,14,17,0.12)] hover:shadow-[0_32px_60px_-16px_rgba(14,14,17,0.16)] overflow-hidden transition-all duration-300">
                  {/* macOS Titlebar */}
                  <div className="h-10 bg-neutral-50/80 border-b border-neutral-200/60 flex items-center px-4 relative select-none">
                    {/* Traffic Lights */}
                    <div className="flex gap-1.5 z-10">
                      <div className="w-3 h-3 rounded-full bg-[#FF5F56] border border-[#E0443E]"></div>
                      <div className="w-3 h-3 rounded-full bg-[#FFBD2E] border border-[#DEA123]"></div>
                      <div className="w-3 h-3 rounded-full bg-[#27C93F] border border-[#1AAB29]"></div>
                    </div>
                    {/* Window title */}
                    <div className="absolute inset-0 flex items-center justify-center text-[10px] font-bold text-neutral-400 uppercase tracking-wider">
                      Avelyn Workflow Demo — Step {steps[activeStep].num}
                    </div>
                  </div>

                  {/* Real screenshot body */}
                  <div className="bg-neutral-50 flex items-center justify-center overflow-hidden aspect-[4/3] md:aspect-[1.45] relative">
                    <img
                      src={steps[activeStep].screenshot}
                      alt={steps[activeStep].alt}
                      className="w-full h-full object-contain p-2 select-none pointer-events-none"
                    />
                  </div>
                </div>
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </div>
    </section>
  );
}
