"use client";

import React from "react";
import { Shield, EyeOff, ServerCrash, Cpu } from "lucide-react";
import { motion } from "framer-motion";

export default function PrivacyFocus() {
  const ease = [0.16, 1, 0.3, 1] as const;

  const highlights = [
    {
      icon: <EyeOff className="w-6 h-6 text-emerald-600" />,
      title: "Zero Telemetry",
      desc: "Your selected text and clipboard history never touch external databases, trackers, or telemetry pipelines. Complete digital anonymity.",
    },
    {
      icon: <ServerCrash className="w-6 h-6 text-emerald-600" />,
      title: "100% Offline",
      desc: "Run inference entirely offline without active internet connections. Essential for high-security workplace policies and air-gapped systems.",
    },
    {
      icon: <Cpu className="w-6 h-6 text-emerald-600" />,
      title: "Local Acceleration",
      desc: "Runs strictly locally utilizing Apple Silicon Unified Memory or Windows Nvidia RTX cores. Blazing-fast generation without server wait times.",
    },
  ];

  return (
    <section id="privacy" className="py-16 md:py-24 bg-white relative overflow-hidden">

      {/* Ambient Emerald Background Glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-[1000px] h-[600px] bg-emerald-500/5 blur-[120px] rounded-full pointer-events-none" />

      <div className="max-w-[1200px] mx-auto px-6 relative z-10">

        {/* Cinematic Centered Header */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.6, ease }}
          className="text-center max-w-[700px] mx-auto mb-12 md:mb-20 flex flex-col items-center"
        >
          {/* Large Authoritative Icon */}
          <div className="w-16 h-16 rounded-2xl bg-emerald-50 border border-emerald-100/60 flex items-center justify-center mb-8 shadow-sm">
            <Shield className="w-8 h-8 text-emerald-600 fill-emerald-600/10" />
          </div>

          <h2 className="text-4xl md:text-5xl lg:text-6xl font-extrabold text-neutral-900 tracking-tight leading-[1.05] mb-6">
            Your data stays <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-teal-500">
              strictly on your machine.
            </span>
          </h2>

          <p className="text-lg text-neutral-500 font-medium leading-relaxed max-w-[540px]">
            Modern AI tools depend on cloud pipelines that log, inspect, and train on your private thoughts. Avelyn turns this model on its head by computing everything locally.
          </p>
        </motion.div>

        {/* 3-Column Premium Bento Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
          {highlights.map((item, idx) => (
            <motion.div
              key={item.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.6, delay: idx * 0.1, ease }}
              className="bg-[#F5F5F7] rounded-[32px] p-6 md:p-10 flex flex-col relative overflow-hidden group hover:bg-[#F0F0F3] transition-colors duration-500"
            >
              {/* Subtle hover gradient inside the card */}
              <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/0 to-emerald-500/0 group-hover:to-emerald-500/[0.03] transition-colors duration-500 pointer-events-none" />

              <div className="w-12 h-12 rounded-2xl bg-white flex items-center justify-center border border-neutral-200/60 shadow-sm mb-8 relative z-10 transition-transform duration-500 group-hover:scale-105 group-hover:shadow-md">
                {item.icon}
              </div>

              <div className="relative z-10">
                <h3 className="text-xl font-bold text-neutral-900 mb-3 tracking-tight">
                  {item.title}
                </h3>
                <p className="text-sm sm:text-base text-neutral-500 font-medium leading-relaxed">
                  {item.desc}
                </p>
              </div>
            </motion.div>
          ))}
        </div>

      </div>
    </section>
  );
}