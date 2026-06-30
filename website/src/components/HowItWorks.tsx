"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MousePointerClick, Keyboard, Layers, Wand2, Cpu, RefreshCw } from "lucide-react";

export default function HowItWorks() {
  const [activeStep, setActiveStep] = useState(0);

  const steps = [
    {
      tabTitle: "Highlight",
      icon: <MousePointerClick className="w-4 h-4" />,
      title: "Highlight Any Text Block",
      desc: "Select the text you want to rewrite or enhance. Works natively across Safari, Chrome, Slack, Notion, Word, and VS Code without any extensions.",
      screenshot: "/images/step1.png",
      alt: "Avelyn text highlight step",
    },
    {
      tabTitle: "Shortcut",
      icon: <Keyboard className="w-4 h-4" />,
      title: "Trigger the Global Hotkey",
      desc: "Hit your customizable global hotkey (defaults to Ctrl+Shift+E). Avelyn instantly captures the highlighted text into secure memory without losing app focus.",
      screenshot: "/screenshots/step2_shortcut.png",
      alt: "Avelyn keyboard trigger step",
    },
    {
      tabTitle: "Palette",
      icon: <Layers className="w-4 h-4" />,
      title: "Command Palette Appears",
      desc: "A floating, glassmorphic palette snaps perfectly to your cursor location, instantly ready to take your instructions via fuzzy search.",
      screenshot: "/images/step3.png",
      alt: "Avelyn Command Palette appearing",
    },
    {
      tabTitle: "Action",
      icon: <Wand2 className="w-4 h-4" />,
      title: "Choose Your AI Action",
      desc: "Select Smart Assist, Fix Grammar, Improve Writing, or simply type your own custom inline prompt directly into the interface.",
      screenshot: "/images/step4.png",
      alt: "Selecting AI action in Command Palette",
    },
    {
      tabTitle: "Enhance",
      icon: <Cpu className="w-4 h-4" />,
      title: "Hybrid Inference",
      desc: "Watch the text stream back token-by-token, computed locally on your machine or routed securely to high-speed cloud providers. Supports instant cancel controls.",
      screenshot: "/images/step5.png",
      alt: "Avelyn real-time streaming text enhancement popup",
    },
    {
      tabTitle: "Replace",
      icon: <RefreshCw className="w-4 h-4" />,
      title: "Auto-Replace In-Place",
      desc: "Press Enter to seamlessly swap the original text with the polished version. Your original clipboard history remains completely intact.",
      screenshot: "/images/step6.png",
      alt: "Avelyn automatically pasting polished text back in place",
    },
  ];

  return (
    <section id="how-it-works" className="pt-12 pb-16 md:pt-20 md:pb-32 bg-[#FAFAFA] overflow-hidden">
      <div className="max-w-[1200px] mx-auto px-6">

        {/* Section Header */}
        <div className="text-center max-w-[600px] mx-auto mb-10">
          <span className="text-xs font-bold text-[#7C3AED] uppercase tracking-widest mb-3 block">
            Product Walkthrough
          </span>
          <h2 className="text-3xl md:text-4xl font-extrabold text-neutral-900 tracking-tight">
            See the Workflow in Action
          </h2>
        </div>

        {/* Premium Horizontal "Sliding Pill" Navigation */}
        <div className="w-full flex overflow-x-auto scrollbar-none pb-4 md:pb-0 mb-12 justify-start md:justify-center px-4 md:px-0">
          <div className="flex items-center shrink-0 min-w-max p-1.5 bg-neutral-200/50 rounded-full border border-neutral-200/60 shadow-inner">
            {steps.map((step, idx) => {
              const isActive = activeStep === idx;
              return (
                <button
                  key={step.tabTitle}
                  onClick={() => setActiveStep(idx)}
                  className="relative flex items-center gap-1.5 sm:gap-2 px-4 sm:px-5 py-2.5 rounded-full text-xs sm:text-sm font-semibold transition-colors duration-300 outline-none select-none shrink-0"
                >
                  {/* Sliding Background Magic (Framer Motion) */}
                  {isActive && (
                    <motion.div
                      layoutId="activeTab"
                      className="absolute inset-0 bg-white rounded-full shadow-sm border border-neutral-200/50"
                      transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                    />
                  )}

                  {/* Tab Content */}
                  <div className={`relative z-10 flex items-center gap-1.5 sm:gap-2 ${isActive ? "text-[#7C3AED]" : "text-neutral-500 hover:text-neutral-700"
                    }`}>
                    {step.icon}
                    <span>{step.tabTitle}</span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Dynamic Content Area (Text + Tighter Image Container) */}
        <div className="flex flex-col items-center max-w-[850px] mx-auto">

          {/* Dynamic Text with fixed min-height to prevent layout shift */}
          <div className="text-center min-h-[140px] md:min-h-[120px] w-full max-w-[650px] mb-8 flex flex-col justify-end">
            <AnimatePresence mode="wait">
              <motion.div
                key={activeStep}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.3 }}
              >
                <h3 className="text-2xl md:text-3xl font-bold text-neutral-900 mb-4 tracking-tight">
                  <span className="text-neutral-300 mr-2">0{activeStep + 1}.</span>
                  {steps[activeStep].title}
                </h3>
                <p className="text-sm md:text-base text-neutral-500 font-medium leading-relaxed">
                  {steps[activeStep].desc}
                </p>
              </motion.div>
            </AnimatePresence>
          </div>

          {/* Expansive macOS App Showcase */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
            className="w-full relative"
          >
            {/* Ambient Background Glow */}
            <div className="absolute inset-0 bg-[#7C3AED]/10 blur-[100px] rounded-[3rem] scale-90 -z-10" />

            <div className="rounded-[24px] border border-neutral-200/80 bg-white/40 p-2 sm:p-3 shadow-2xl shadow-neutral-900/5 backdrop-blur-xl transition-all">
              <div className="overflow-hidden rounded-[16px] bg-[#F5F5F7] border border-neutral-200/50 flex flex-col aspect-video sm:aspect-[16/10] md:aspect-[16/9]">

                {/* macOS Titlebar */}
                <div className="h-10 bg-white/80 backdrop-blur-md border-b border-neutral-200/60 flex items-center px-4 relative z-20 shrink-0">
                  <div className="flex gap-1.5">
                    <div className="w-2.5 h-2.5 rounded-full bg-[#FF5F56] border border-[#E0443E]/20" />
                    <div className="w-2.5 h-2.5 rounded-full bg-[#FFBD2E] border border-[#DEA123]/20" />
                    <div className="w-2.5 h-2.5 rounded-full bg-[#27C93F] border border-[#1AAB29]/20" />
                  </div>
                </div>

                {/* Crossfading High-Res Image Area (Padding removed to enlarge image) */}
                <div className="relative flex-1 flex items-center justify-center overflow-hidden">
                  <AnimatePresence mode="wait">
                    <motion.div
                      key={activeStep}
                      initial={{ opacity: 0, scale: 0.98 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 1.02 }}
                      transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
                      className="absolute inset-0 flex items-center justify-center p-0 sm:p-2"
                    >
                      {/* Using standard img tag inside motion.div to prevent Next.js image errors */}
                      {/* eslint-disable-next-line @next/next/no-img-element */}
                      <img
                        src={steps[activeStep].screenshot}
                        alt={steps[activeStep].alt}
                        className="w-full h-full object-contain drop-shadow-xl select-none"
                      />
                    </motion.div>
                  </AnimatePresence>
                </div>

              </div>
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  );
}