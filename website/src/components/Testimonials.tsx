"use client";

import React, { useState } from "react";
import { Mail, Check } from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";

export default function Testimonials() {
  const shouldReduceMotion = useReducedMotion();
  const ease = [0.16, 1, 0.3, 1] as const;

  const [email, setEmail] = useState("");
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email.trim()) {
      setIsSubmitted(true);
      setEmail("");
    }
  };

  return (
    <section className="py-20 bg-neutral-50/40 border-b border-neutral-100/60">
      <div className="max-w-[1100px] mx-auto px-6">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          {/* Left Side: Join the Beta Callout */}
          <motion.div
            initial={shouldReduceMotion ? false : { opacity: 0, y: 12 }}
            whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
            viewport={shouldReduceMotion ? undefined : { once: true, amount: 0.35 }}
            transition={{ duration: 0.6, ease }}
            className="lg:col-span-6 text-left space-y-5"
          >
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#EDE9FE]/50 border border-[#EDE9FE] text-[10px] font-bold text-[#7C3AED] select-none uppercase tracking-wide">
              Early Access
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-[#0E0E11] tracking-tight leading-[1.1]">
              Join the Avelyn <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#7C3AED] to-[#A78BFA]">
                Private Beta.
              </span>
            </h2>
            <p className="text-xs sm:text-sm text-neutral-500 font-medium leading-relaxed max-w-[420px]">
              We are currently running a limited-enrollment private beta to polish offline performance and Sonoma window focus mechanics. Drop your email to request access.
            </p>

            <form onSubmit={handleSubmit} className="flex gap-2 max-w-[400px]">
              {isSubmitted ? (
                <div className="flex items-center gap-2 bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-semibold px-4 py-3 rounded-xl w-full">
                  <Check className="w-4 h-4 shrink-0" />
                  <span>Thank you! We&apos;ve added you to the waitlist.</span>
                </div>
              ) : (
                <>
                  <div className="relative flex-1">
                    <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-neutral-400" />
                    <input
                      type="email"
                      required
                      placeholder="name@email.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="w-full bg-white border border-neutral-200 focus:border-[#7C3AED] rounded-xl pl-10 pr-4 py-3 text-xs sm:text-sm text-neutral-800 font-semibold focus:outline-none transition-colors"
                    />
                  </div>
                  <button
                    type="submit"
                    className="bg-[#0E0E11] hover:bg-neutral-800 text-white text-xs font-bold px-5 py-3 rounded-xl shadow-md transition-all active:scale-[0.98] cursor-pointer shrink-0"
                  >
                    Request Access
                  </button>
                </>
              )}
            </form>
          </motion.div>

          {/* Right Side: Status/Feedback Blocks */}
          <div className="lg:col-span-6 grid grid-cols-1 sm:grid-cols-2 gap-4 text-left">
            <motion.div
              initial={shouldReduceMotion ? false : { opacity: 0, y: 10 }}
              whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
              viewport={shouldReduceMotion ? undefined : { once: true, amount: 0.25 }}
              transition={{ duration: 0.6, delay: 0.06, ease }}
              className="bg-white border border-neutral-200/50 rounded-2xl p-6 space-y-3"
            >
              <span className="text-xs font-bold text-neutral-400 uppercase tracking-wider">Beta Status</span>
              <div className="h-[1px] bg-neutral-100"></div>
              <div className="space-y-1">
                <h4 className="text-xs font-bold text-[#0E0E11]">Version 1.0.0-beta4</h4>
                <p className="text-[11px] text-neutral-400 font-semibold">Sonoma focus stability patches added.</p>
              </div>
            </motion.div>

            <motion.div
              initial={shouldReduceMotion ? false : { opacity: 0, y: 10 }}
              whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
              viewport={shouldReduceMotion ? undefined : { once: true, amount: 0.25 }}
              transition={{ duration: 0.6, delay: 0.12, ease }}
              className="bg-white border border-neutral-200/50 rounded-2xl p-6 space-y-3"
            >
              <span className="text-xs font-bold text-neutral-400 uppercase tracking-wider">Next Release</span>
              <div className="h-[1px] bg-neutral-100"></div>
              <div className="space-y-1">
                <h4 className="text-xs font-bold text-[#0E0E11]">Version 1.1.0-RC1</h4>
                <p className="text-[11px] text-neutral-400 font-semibold">Streaming speed increase by ~25%.</p>
              </div>
            </motion.div>

            <motion.div
              initial={shouldReduceMotion ? false : { opacity: 0, y: 10 }}
              whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
              viewport={shouldReduceMotion ? undefined : { once: true, amount: 0.25 }}
              transition={{ duration: 0.6, delay: 0.18, ease }}
              className="bg-white border border-neutral-200/50 rounded-2xl p-6 space-y-3 sm:col-span-2"
            >
              <span className="text-xs font-bold text-neutral-400 uppercase tracking-wider">Early Tester Feedback</span>
              <div className="h-[1px] bg-neutral-100"></div>
              <p className="text-xs text-neutral-500 italic font-medium leading-relaxed">
                &ldquo;Having a local, offline assistant that lives inside the clipboard stack completely replaces web dashboards for me. The latency on Apple Silicon is extremely impressive.&rdquo;
              </p>
            </motion.div>
          </div>
        </div>
      </div>
    </section>
  );
}
