"use client";

import React from "react";
import Link from "next/link";
import { Mail, Shield, ArrowUpRight, BookOpen, Layers, Scale, Lock, HelpCircle } from "lucide-react";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  const footerColumns = [
    {
      title: "Documentation",
      links: [
        { name: "Docs Overview", href: "/docs" },
        { name: "Getting Started", href: "/docs/getting-started/installation" },
        { name: "AI Providers Guide", href: "/docs/providers/gemini-integration" },
        { name: "Local Ollama Setup", href: "/docs/providers/ollama-integration" },
        { name: "Troubleshooting", href: "/docs/troubleshooting/ollama-connection-issues" },
      ]
    },
    {
      title: "Features & Tools",
      links: [
        { name: "Prompt Enhancer", href: "/features/prompt-enhancer" },
        { name: "Grammar Checker", href: "/features/grammar-checker" },
        { name: "AI Email Writer", href: "/features/email-writer" },
        { name: "AI Code Assistant", href: "/features/coding-assistant" },
        { name: "Local AI Engine", href: "/features/local-ai" },
      ]
    },
    {
      title: "Comparisons",
      links: [
        { name: "vs. ChatGPT", href: "/compare/avelyn-vs-chatgpt" },
        { name: "vs. Grammarly", href: "/compare/avelyn-vs-grammarly" },
        { name: "vs. Google Gemini", href: "/compare/avelyn-vs-gemini" },
        { name: "vs. Claude 3.5", href: "/compare/avelyn-vs-claude" },
        { name: "vs. Notion AI", href: "/compare/avelyn-vs-notion-ai" },
      ]
    },
    {
      title: "Trust & Governance",
      links: [
        { name: "About Avelyn", href: "/trust/about" },
        { name: "Privacy Policy", href: "/trust/privacy" },
        { name: "Security & Keys", href: "/trust/security" },
        { name: "Product Roadmap", href: "/trust/roadmap" },
        { name: "Central FAQ", href: "/faq" },
      ]
    }
  ];

  return (
    <footer className="relative bg-[#FAFAFA] pt-12 md:pt-24 overflow-hidden border-t border-neutral-200/60 block w-full">

      {/* Subtle Ambient Glow */}
      <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-full max-w-[800px] h-[300px] bg-[#7C3AED]/10 blur-[120px] rounded-t-full pointer-events-none" />

      <div className="max-w-[1200px] mx-auto px-4 sm:px-6 relative z-10 flex flex-col">

        {/* --- TOP SECTION: CTA & Links --- */}
        <div className="flex flex-col lg:flex-row justify-between gap-10 lg:gap-16 mb-12 md:mb-16">

          {/* Left: Final Call to Action */}
          <div className="flex flex-col items-start max-w-sm">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white border border-neutral-200/60 shadow-sm mb-5">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              <span className="text-[10px] font-bold text-neutral-600 uppercase tracking-widest">
                System Operational · v2.1
              </span>
            </div>

            <p className="text-2xl sm:text-3xl md:text-4xl font-extrabold text-neutral-900 tracking-tight leading-[1.15] mb-5">
              Write better. <br />
              <span className="text-neutral-400">Never compromise privacy.</span>
            </p>

            <Link
              href="/#beta"
              className="group inline-flex items-center justify-center gap-2 rounded-full bg-[#0E0E11] px-6 py-3.5 text-sm font-semibold text-white shadow-xl shadow-black/10 transition-all hover:bg-neutral-800 hover:scale-[1.02] active:scale-[0.98]"
            >
              Early Beta Access
              <ArrowUpRight className="w-4 h-4 text-neutral-400 group-hover:text-white transition-colors" />
            </Link>
          </div>

          {/* Right: Clean Columns */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-8 md:gap-12 w-full lg:w-auto">
            {footerColumns.map((column) => (
              <div key={column.title} className="flex flex-col">
                <span className="text-xs font-bold text-neutral-900 uppercase tracking-widest mb-4 block">
                  {column.title}
                </span>
                <ul className="flex flex-col space-y-2.5">
                  {column.links.map((link) => (
                    <li key={link.name}>
                      <Link
                        href={link.href}
                        className="group flex items-center text-xs sm:text-sm font-medium text-neutral-500 hover:text-[#7C3AED] transition-colors duration-300"
                      >
                        {link.name}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        {/* --- MIDDLE SECTION: Typography --- */}
        <div className="w-full flex justify-center items-center overflow-hidden select-none pointer-events-none mb-6">
          <span className="text-[14vw] sm:text-[16vw] lg:text-[180px] font-extrabold text-neutral-900/5 tracking-tighter leading-none">
            AVELYN
          </span>
        </div>

        {/* --- BOTTOM SECTION: Badges & Socials --- */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 py-6 border-t border-neutral-200/60 relative z-20 text-center sm:text-left">

          <div className="flex flex-col sm:flex-row items-center gap-3 sm:gap-6">
            <div className="flex items-center gap-1.5 text-neutral-400">
              <Shield className="w-4 h-4 text-emerald-500 flex-shrink-0" />
              <span className="text-xs font-medium uppercase tracking-wider text-neutral-600">
                100% Local Sandbox & Zero Telemetry
              </span>
            </div>
            <div className="hidden sm:block w-1 h-1 rounded-full bg-neutral-300" />
            <span className="text-xs text-neutral-500 font-medium">
              &copy; {currentYear} Avelyn. All rights reserved.
            </span>
          </div>

          <div className="flex items-center gap-4">
            <Link
              href="/docs"
              className="text-xs font-semibold text-neutral-600 hover:text-[#7C3AED] transition-colors"
            >
              Docs
            </Link>
            <Link
              href="/faq"
              className="text-xs font-semibold text-neutral-600 hover:text-[#7C3AED] transition-colors"
            >
              FAQ
            </Link>
            <a
              href="https://github.com/vishwaksen21/Avelyn"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 rounded-full bg-white border border-neutral-200/60 text-neutral-500 hover:text-neutral-900 transition-all"
              aria-label="GitHub"
            >
              <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
              </svg>
            </a>
          </div>

        </div>
      </div>
    </footer>
  );
}