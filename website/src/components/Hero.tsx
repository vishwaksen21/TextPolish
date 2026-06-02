"use client";

import React from "react";
import Image from "next/image";
import { motion, useReducedMotion } from "framer-motion";

export default function Hero() {
  const shouldReduceMotion = useReducedMotion();

  const fadeUp = {
    hidden: { opacity: 0, y: 12 },
    visible: { opacity: 1, y: 0 },
  };

  return (
    <section className="relative overflow-hidden bg-white">
      <div className="mx-auto max-w-[1280px] px-6 py-12 lg:py-16">
        <div className="grid min-h-[650px] items-center gap-12 lg:grid-cols-[0.85fr_1.15fr]">

          {/* LEFT */}
          <div className="max-w-[540px]">
            <motion.div
              initial={shouldReduceMotion ? false : "hidden"}
              animate={shouldReduceMotion ? undefined : "visible"}
              variants={fadeUp}
              transition={{
                duration: 0.5,
                ease: [0.16, 1, 0.3, 1],
              }}
              className="inline-flex items-center gap-2 rounded-full bg-violet-50 px-4 py-2"
            >
              <Image
                src="/logo.png"
                alt="Avelyn"
                width={18}
                height={18}
                className="h-[18px] w-[18px]"
              />

              <span className="text-sm font-medium text-violet-700">
                Local AI. Private. Offline.
              </span>
            </motion.div>

            <motion.h1
              initial={shouldReduceMotion ? false : "hidden"}
              animate={shouldReduceMotion ? undefined : "visible"}
              variants={fadeUp}
              transition={{
                duration: 0.6,
                delay: 0.05,
                ease: [0.16, 1, 0.3, 1],
              }}
              className="mt-6 text-[48px] leading-[0.95] font-semibold tracking-[-0.04em] text-neutral-950 sm:text-[58px] lg:text-[68px]"
            >
              Select text.
              <br />
              Improve it instantly.
            </motion.h1>

            <motion.p
              initial={shouldReduceMotion ? false : "hidden"}
              animate={shouldReduceMotion ? undefined : "visible"}
              variants={fadeUp}
              transition={{
                duration: 0.6,
                delay: 0.12,
                ease: [0.16, 1, 0.3, 1],
              }}
              className="mt-6 text-lg leading-relaxed text-neutral-600"
            >
              Avelyn lives in your menu bar and helps you rewrite,
              refine, and improve text anywhere on macOS using local AI.
            </motion.p>

            <motion.div
              initial={shouldReduceMotion ? false : "hidden"}
              animate={shouldReduceMotion ? undefined : "visible"}
              variants={fadeUp}
              transition={{
                duration: 0.6,
                delay: 0.18,
                ease: [0.16, 1, 0.3, 1],
              }}
              className="mt-8 flex flex-wrap gap-4"
            >
              <a
                href="https://github.com/vishwaksen21/Avelyn/releases"
                className="inline-flex items-center justify-center rounded-full bg-neutral-950 px-7 py-4 text-base font-semibold text-white transition hover:bg-neutral-800"
              >
                Download for macOS
              </a>

              <a
                href="#how-it-works"
                className="inline-flex items-center justify-center rounded-full border border-neutral-200 bg-white px-7 py-4 text-base font-semibold text-neutral-900 transition hover:bg-neutral-50"
              >
                Watch Demo
              </a>
            </motion.div>

            <motion.div
              initial={shouldReduceMotion ? false : { opacity: 0 }}
              animate={shouldReduceMotion ? undefined : { opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="mt-10 flex items-center gap-3 text-sm font-medium text-neutral-500"
            >
              <span>Private</span>
              <span>•</span>
              <span>Offline</span>
              <span>•</span>
              <span>Local AI</span>
            </motion.div>
          </div>

          {/* RIGHT */}
          <motion.div
            initial={
              shouldReduceMotion
                ? false
                : {
                    opacity: 0,
                    x: 40,
                    scale: 0.98,
                  }
            }
            animate={
              shouldReduceMotion
                ? undefined
                : {
                    opacity: 1,
                    x: 0,
                    scale: 1,
                  }
            }
            transition={{
              duration: 0.8,
              delay: 0.1,
              ease: [0.16, 1, 0.3, 1],
            }}
            className="relative"
          >
            {/* Glow */}
            <div className="absolute inset-0 -z-10 flex items-center justify-center">
              <div className="h-[420px] w-[420px] rounded-full bg-violet-300/20 blur-3xl" />
            </div>

            <div className="overflow-hidden rounded-[28px] border border-neutral-200 bg-white shadow-[0_40px_80px_-30px_rgba(0,0,0,0.18)]">
  <Image
    src="/images/hero_image.png"
    alt="Avelyn Settings"
    width={2048}
    height={2048}
    priority
    className="w-full max-h-[520px] object-cover object-top"
  />
</div>
          </motion.div>

        </div>
      </div>
    </section>
  );
}
