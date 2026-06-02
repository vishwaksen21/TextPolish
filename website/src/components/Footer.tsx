"use client";

import React from "react";
import { Mail, Shield } from "lucide-react";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  const footerLinks = [
    {
      title: "Product",
      links: [
        { name: "Download macOS", href: "https://github.com/vishwaksen21/Avelyn/releases" },
        { name: "Setup Wizard", href: "#how-it-works" },
        { name: "Changelog", href: "https://github.com/vishwaksen21/Avelyn/releases" },
        { name: "Beta Program", href: "#" }
      ]
    },
    {
      title: "Resources",
      links: [
        { name: "Documentation", href: "https://github.com/vishwaksen21/Avelyn/blob/main/README.md" },
        { name: "GitHub Repository", href: "https://github.com/vishwaksen21/Avelyn" },
        { name: "Local LLM Guide", href: "https://github.com/vishwaksen21/Avelyn#ollama-offline--local" },
        { name: "Ollama Models", href: "https://ollama.com/library" }
      ]
    },
    {
      title: "Company",
      links: [
        { name: "Contact Support", href: "mailto:support@avelyn.app" },
        { name: "Privacy Policy", href: "#privacy" },
        { name: "MIT License", href: "https://github.com/vishwaksen21/Avelyn/blob/main/LICENSE" },
        { name: "System Status", href: "#" }
      ]
    }
  ];

  return (
    <footer className="bg-white border-t border-neutral-100/80 pt-20 pb-12 text-neutral-500 text-xs text-left">
      <div className="max-w-[1100px] mx-auto px-6">
        {/* Top Section: Brand info + Multi-column Links */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-10 md:gap-8 pb-16 border-b border-neutral-100">
          {/* Brand Signature */}
          <div className="md:col-span-4 flex flex-col space-y-4">
            <div className="flex items-center gap-3 select-none">
              <img src="/logo.png" alt="Avelyn Logo" className="h-8 w-auto" />
              <span className="font-bold text-[19px] text-[#0E0E11] tracking-tight">Avelyn</span>
            </div>
            <p className="text-xs text-neutral-400 font-semibold leading-relaxed max-w-[260px]">
              Writing assistant for macOS and Windows. 100% offline, privacy-first local GPU-accelerated text enhancement.
            </p>
            {/* Social badges */}
            <div className="flex items-center gap-3.5 pt-1 text-neutral-400">
              <a
                href="https://github.com/vishwaksen21/Avelyn"
                className="hover:text-[#0E0E11] transition-colors"
                aria-label="Avelyn GitHub"
              >
                <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
              </a>
              <a
                href="mailto:support@avelyn.app"
                className="hover:text-[#0E0E11] transition-colors"
                aria-label="Avelyn Support"
              >
                <Mail className="w-4 h-4" />
              </a>
            </div>
          </div>

          {/* Dynamic Columns */}
          <div className="md:col-span-8 grid grid-cols-2 sm:grid-cols-3 gap-8">
            {footerLinks.map((column) => (
              <div key={column.title} className="flex flex-col space-y-4">
                <h4 className="text-[11px] font-bold text-[#0E0E11] uppercase tracking-widest">
                  {column.title}
                </h4>
                <ul className="flex flex-col space-y-2.5">
                  {column.links.map((link) => (
                    <li key={link.name}>
                      <a
                        href={link.href}
                        className="text-xs font-semibold text-neutral-400 hover:text-[#0E0E11] transition-colors"
                      >
                        {link.name}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        {/* Bottom Section: Legal disclaimer, Privacy shield note, and Copyright */}
        <div className="pt-10 flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2 text-[10px] text-neutral-400 font-bold bg-[#EDE9FE]/20 border border-[#EDE9FE]/55 px-3 py-1 rounded-full select-none uppercase tracking-wide">
            <Shield className="w-3.5 h-3.5 text-[#7C3AED]" />
            <span>Fully Compliant local sandbox</span>
          </div>

          {/* Copyright block */}
          <div className="text-xs text-neutral-400 font-medium select-none">
            &copy; {currentYear} Avelyn. Handcrafted for maximum privacy.
          </div>
        </div>
      </div>
    </footer>
  );
}
