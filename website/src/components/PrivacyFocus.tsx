"use client";

import React from "react";
import { Shield, EyeOff, ServerCrash, Cpu } from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";

export default function PrivacyFocus() {
  const shouldReduceMotion = useReducedMotion();
  const ease = [0.16, 1, 0.3, 1] as const;

  const highlights = [
    {
      icon: <EyeOff className="w-5 h-5 text-emerald-600" />,
      title: "No Telemetry or Logs",
      desc: "Your selected text and clipboard history never touch external databases, trackers, or telemetry pipelines. Complete digital anonymity.",
    },
    {
      icon: <ServerCrash className="w-5 h-5 text-emerald-600" />,
      title: "100% Offline Capable",
      desc: "Run inference entirely offline without active internet connections or Wi-Fi configurations. Essential for high-security workplace policies.",
    },
    {
      icon: <Cpu className="w-5 h-5 text-emerald-600" />,
      title: "Local GPU Acceleration",
      desc: "Runs locally utilizing Apple Silicon Unified Memory or Windows Nvidia RTX cores via Ollama. Blazing-fast generation without server wait times.",
    },
  ];

  return (
    <section id="privacy" className="py-20 bg-emerald-50/20 border-b border-neutral-100/60">
      <div className="max-w-[1100px] mx-auto px-6">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          {/* Left Side: Editorial Trust Statement */}
          <motion.div
            initial={shouldReduceMotion ? false : { opacity: 0, x: -12 }}
            whileInView={shouldReduceMotion ? undefined : { opacity: 1, x: 0 }}
            viewport={shouldReduceMotion ? undefined : { once: true, amount: 0.35 }}
            transition={{ duration: 0.6, ease }}
            className="lg:col-span-5 text-left space-y-6"
          >
            <div className="inline-flex">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100/60 border border-emerald-200/50 text-[11px] font-bold text-emerald-700 select-none uppercase tracking-wide">
                <Shield className="w-3.5 h-3.5 fill-current" /> Privacy Shield
              </span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-[#0E0E11] tracking-tight leading-[1.1]">
              Your data stays <br />
              <span className="text-emerald-600">on your machine.</span>
            </h2>
            <p className="text-xs sm:text-sm text-neutral-500 font-medium leading-relaxed max-w-[380px]">
              Modern AI tools depend on cloud pipelines that log, inspect, and train on your private thoughts. Avelyn turns this model on its head by compiling intelligence locally.
            </p>
          </motion.div>

          {/* Right Side: Features Grid */}
          <div className="lg:col-span-7 space-y-6">
            {highlights.map((item, idx) => (
              <motion.div
                key={item.title}
                initial={shouldReduceMotion ? false : { opacity: 0, y: 10 }}
                whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
                viewport={shouldReduceMotion ? undefined : { once: true, amount: 0.25 }}
                transition={{ duration: 0.55, delay: idx * 0.06, ease }}
                className="bg-white border border-neutral-200/40 rounded-2xl p-6 shadow-[0_1px_2px_rgba(0,0,0,0.01)] hover:shadow-md transition-all duration-300 flex flex-col sm:flex-row gap-4 items-start text-left"
              >
                <div className="w-10 h-10 rounded-xl bg-emerald-50 flex items-center justify-center shrink-0">
                  {item.icon}
                </div>
                <div className="space-y-1.5">
                  <h3 className="text-sm font-bold text-[#0E0E11]">{item.title}</h3>
                  <p className="text-xs text-neutral-500 font-medium leading-relaxed">
                    {item.desc}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
