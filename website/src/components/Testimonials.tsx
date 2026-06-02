"use client";

import React, { useState } from "react";
import { Mail, Check, ArrowRight, Star, Activity, GitBranch } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function BetaAccess() {
  const ease = [0.16, 1, 0.3, 1] as const;

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (name.trim() && email.trim()) {
      setIsSubmitting(true);

      try {
        const response = await fetch(
          "https://formspree.io/f/xojbgykz",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json",
            },
            body: JSON.stringify({
              name,
              email,
            }),
          }
        );

        if (!response.ok) {
          throw new Error("Submission failed");
        }

        setIsSubmitted(true);
        setName("");
        setEmail("");
      } catch (error) {
        console.error("Error submitting form:", error);
      } finally {
        setIsSubmitting(false);
      }
    }
  };
  return (
    <section id="beta" className="py-16 md:py-24 relative bg-[#FAFAFA] overflow-hidden border-t border-neutral-200/50">

      {/* Subtle background glow */}
      <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-[#7C3AED]/5 blur-[120px] rounded-full pointer-events-none translate-x-1/3 -translate-y-1/3" />

      <div className="max-w-[1200px] mx-auto px-6 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-16 lg:gap-12 items-center">

          {/* LEFT SIDE: Premium Call to Action */}
          <div className="lg:col-span-5 text-left flex flex-col justify-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.3 }}
              transition={{ duration: 0.6, ease }}
            >
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#7C3AED]/10 border border-[#7C3AED]/20 mb-6">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#7C3AED] opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-[#7C3AED]"></span>
                </span>
                <span className="text-[11px] font-bold text-[#7C3AED] uppercase tracking-widest">
                  Private Beta Now Open
                </span>
              </div>

              <h2 className="text-4xl md:text-5xl lg:text-6xl font-extrabold text-neutral-900 tracking-tight leading-[1.05] mb-6">
                Experience the <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#7C3AED] to-[#a06af9]">
                  future of writing.
                </span>
              </h2>

              <p className="text-base text-neutral-500 font-medium leading-relaxed max-w-[420px] mb-10">
                We are running a limited-enrollment private beta to polish offline performance and native macOS window mechanics. Request your access token below.
              </p>

              {/* Spotlight-Style Unified Form */}
              <div className="w-full max-w-[460px]">
                <AnimatePresence mode="wait">
                  {isSubmitted ? (
                    <motion.div
                      key="success"
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      className="flex items-center gap-3 bg-emerald-50 border border-emerald-200/60 text-emerald-700 px-5 py-4 rounded-2xl shadow-sm"
                    >
                      <div className="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center shrink-0">
                        <Check className="w-4 h-4 text-emerald-600" />
                      </div>
                      <div>
                        <div className="text-sm font-bold">You're on the list!</div>
                        <div className="text-xs font-medium opacity-80 mt-0.5">Keep an eye on your inbox for the invite.</div>
                      </div>
                    </motion.div>
                  ) : (
                    <motion.form
                      key="form"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      onSubmit={handleSubmit}
                      className="flex flex-col gap-3"
                    >
                      {/* Name Input */}
                      <div className="relative flex items-center bg-white border border-neutral-200/80 rounded-[20px] p-1.5 shadow-sm hover:shadow-md hover:border-[#7C3AED]/30 transition-all duration-300 focus-within:border-[#7C3AED]/50 focus-within:ring-4 focus-within:ring-[#7C3AED]/10">
                        <input
                          type="text"
                          required
                          placeholder="Your name"
                          value={name}
                          onChange={(e) => setName(e.target.value)}
                          disabled={isSubmitting}
                          className="flex-1 bg-transparent border-none py-3 px-4 text-sm text-neutral-900 font-medium focus:outline-none focus:ring-0 placeholder:text-neutral-400 disabled:opacity-50"
                        />
                      </div>

                      {/* Email Input */}
                      <div className="relative flex items-center bg-white border border-neutral-200/80 rounded-[20px] p-1.5 shadow-sm hover:shadow-md hover:border-[#7C3AED]/30 transition-all duration-300 focus-within:border-[#7C3AED]/50 focus-within:ring-4 focus-within:ring-[#7C3AED]/10">
                        <div className="pl-4 pr-2 text-neutral-400">
                          <Mail className="w-5 h-5" />
                        </div>

                        <input
                          type="email"
                          required
                          placeholder="name@company.com"
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                          disabled={isSubmitting}
                          className="flex-1 bg-transparent border-none py-3 text-sm text-neutral-900 font-medium focus:outline-none focus:ring-0 placeholder:text-neutral-400 disabled:opacity-50"
                        />

                        <button
                          type="submit"
                          disabled={isSubmitting}
                          className="group flex items-center justify-center w-12 h-10 rounded-[14px] bg-[#0E0E11] hover:bg-neutral-800 text-white transition-all active:scale-95 shrink-0 disabled:opacity-50"
                        >
                          {isSubmitting ? (
                            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                          ) : (
                            <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                          )}
                        </button>
                      </div>
                    </motion.form>
                  )}
                </AnimatePresence>
              </div>
            </motion.div>
          </div>

          {/* RIGHT SIDE: macOS-Style Widgets */}
          <div className="lg:col-span-7 grid grid-cols-1 sm:grid-cols-2 gap-5 text-left relative z-10">

            {/* Widget 1: Beta Status */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.6, delay: 0.1, ease }}
              className="bg-white border border-neutral-200/60 rounded-[24px] p-7 shadow-sm hover:shadow-md transition-all duration-300 flex flex-col justify-between"
            >
              <div className="w-10 h-10 rounded-full bg-blue-50 border border-blue-100 flex items-center justify-center mb-6">
                <Activity className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <span className="text-[10px] font-bold text-neutral-400 uppercase tracking-widest mb-1.5 block">
                  Current Build
                </span>
                <h4 className="text-xl font-bold text-neutral-900 tracking-tight mb-2">v1.0.0-beta4</h4>
                <p className="text-sm text-neutral-500 font-medium leading-relaxed">
                  Sonoma & Sequoia window focus stability patches deployed.
                </p>
              </div>
            </motion.div>

            {/* Widget 2: Next Release */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.6, delay: 0.2, ease }}
              className="bg-white border border-neutral-200/60 rounded-[24px] p-7 shadow-sm hover:shadow-md transition-all duration-300 flex flex-col justify-between"
            >
              <div className="w-10 h-10 rounded-full bg-amber-50 border border-amber-100 flex items-center justify-center mb-6">
                <GitBranch className="w-5 h-5 text-amber-600" />
              </div>
              <div>
                <span className="text-[10px] font-bold text-neutral-400 uppercase tracking-widest mb-1.5 block">
                  Next Release
                </span>
                <h4 className="text-xl font-bold text-neutral-900 tracking-tight mb-2">v1.1.0-RC1</h4>
                <p className="text-sm text-neutral-500 font-medium leading-relaxed">
                  Local Ollama token streaming speed increased by ~25%.
                </p>
              </div>
            </motion.div>

            {/* Widget 3: App Store Style Review (Spans 2 columns) */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.6, delay: 0.3, ease }}
              className="bg-[#0E0E11] border border-neutral-800 rounded-[24px] p-8 shadow-xl sm:col-span-2 relative overflow-hidden group"
            >
              {/* Subtle inner glow */}
              <div className="absolute top-0 right-0 w-64 h-64 bg-[#7C3AED]/20 blur-[80px] rounded-full pointer-events-none translate-x-1/2 -translate-y-1/2 group-hover:bg-[#7C3AED]/30 transition-colors duration-700" />

              <div className="relative z-10">
                <div className="flex items-center justify-between mb-6">
                  <span className="text-[10px] font-bold text-neutral-500 uppercase tracking-widest">
                    Early Tester Feedback
                  </span>
                  <div className="flex gap-1">
                    {[...Array(5)].map((_, i) => (
                      <Star key={i} className="w-4 h-4 fill-amber-400 text-amber-400" />
                    ))}
                  </div>
                </div>

                <h4 className="text-2xl font-bold text-white tracking-tight mb-4 leading-snug">
                  "Completely replaces web dashboards for me."
                </h4>

                <p className="text-base text-neutral-400 font-medium leading-relaxed mb-6">
                  Having a local, offline assistant that lives natively inside the macOS clipboard stack is a game-changer. The inference latency on Apple Silicon is extremely impressive.
                </p>

                <div className="flex items-center gap-3 pt-6 border-t border-white/10">
                  <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-xs font-bold text-white">
                    JS
                  </div>
                  <div className="flex flex-col">
                    <span className="text-sm font-bold text-white">Beta User</span>
                    <span className="text-xs font-medium text-neutral-500">macbook m2 air</span>
                  </div>
                </div>
              </div>
            </motion.div>

          </div>
        </div>
      </div>
    </section>
  );
}