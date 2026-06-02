"use client";

import React, { useState } from "react";
import Image from "next/image";
import { motion, AnimatePresence } from "framer-motion";
import { Download, Menu, X } from "lucide-react";

export default function Navbar() {
  const [hoveredLink, setHoveredLink] = useState<string | null>(null);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navLinks = [
    { name: "Features", href: "#features" },
    { name: "How It Works", href: "#how-it-works" },
    { name: "FAQ", href: "#faq" },
  ];

  return (
    <div className="fixed top-0 inset-x-0 z-50 flex justify-center mt-6 px-4 pointer-events-none">
      <motion.header
        initial={{ y: -40, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        className={`pointer-events-auto flex flex-col px-5 sm:px-6 py-2.5 w-full max-w-[1200px] bg-white/60 backdrop-blur-2xl border border-neutral-200/60 shadow-[0_8px_30px_rgb(0,0,0,0.06)] transition-all duration-300 ${
          isMobileMenuOpen ? "rounded-[24px] pb-6" : "rounded-full"
        }`}
      >
        {/* TOP ROW: Logo and standard controls */}
        <div className="w-full flex items-center justify-between">
          {/* LEFT: Logo (Increased Size) */}
          <a
            href="#"
            className="group flex items-center gap-3 select-none outline-none"
            aria-label="Avelyn"
          >
            <div className="relative flex items-center justify-center transition-transform duration-300 group-hover:scale-105 group-active:scale-95">
              <Image
                src="/logo.png"
                alt="Avelyn Logo"
                width={32}
                height={32}
                className="h-8 w-8 object-contain"
              />
            </div>
            <span className="text-base font-bold tracking-tight text-neutral-900">
              Avelyn
            </span>
          </a>

          {/* RIGHT: Desktop Nav links, CTA and Mobile Toggle */}
          <div className="flex items-center gap-3">
            {/* CENTER: Liquid Hover Navigation (Desktop only) */}
            <nav
              className="hidden md:flex items-center gap-1.5"
              onMouseLeave={() => setHoveredLink(null)}
            >
              {navLinks.map((link) => (
                <a
                  key={link.name}
                  href={link.href}
                  onMouseEnter={() => setHoveredLink(link.name)}
                  className="relative px-5 py-2 text-[13px] font-semibold text-neutral-500 hover:text-neutral-900 transition-colors duration-200 outline-none select-none"
                >
                  {hoveredLink === link.name && (
                    <motion.div
                      layoutId="nav-hover-pill"
                      className="absolute inset-0 bg-black/5 rounded-full -z-10"
                      transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                    />
                  )}
                  {link.name}
                </a>
              ))}
            </nav>

            {/* CTA */}
            <div className="flex items-center">
              <a
                href="https://github.com/vishwaksen21/Avelyn/releases"
                className="group flex items-center gap-1.5 rounded-full bg-[#0E0E11] pl-5 pr-6 py-2.5 text-[13px] font-semibold text-white shadow-sm shadow-black/10 transition-all duration-300 hover:bg-neutral-800 hover:shadow-md hover:scale-[1.02] active:scale-[0.98] outline-none"
              >
                <Download className="w-3.5 h-3.5 text-neutral-400 group-hover:text-white transition-colors" />
                <span className="hidden xs:inline">Download</span>
                <span className="inline xs:hidden">App</span>
              </a>
            </div>

            {/* Hamburger Toggle button */}
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="flex md:hidden p-2 rounded-full hover:bg-black/5 text-neutral-600 hover:text-neutral-900 transition-all active:scale-95 outline-none select-none"
              aria-label="Toggle Menu"
            >
              {isMobileMenuOpen ? (
                <X className="w-4.5 h-4.5" />
              ) : (
                <Menu className="w-4.5 h-4.5" />
              )}
            </button>
          </div>
        </div>

        {/* MOBILE NAVIGATION DRAWER */}
        <AnimatePresence>
          {isMobileMenuOpen && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
              className="md:hidden overflow-hidden w-full flex flex-col mt-4 border-t border-neutral-200/40 pt-4 gap-1.5"
            >
              {navLinks.map((link) => (
                <a
                  key={link.name}
                  href={link.href}
                  onClick={() => setIsMobileMenuOpen(false)}
                  className="px-4 py-2.5 text-sm font-semibold text-neutral-500 hover:text-neutral-900 hover:bg-black/5 rounded-xl transition-all duration-200"
                >
                  {link.name}
                </a>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </motion.header>
    </div>
  );
}