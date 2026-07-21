"use client";

import React, { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, Menu, X, BookOpen } from "lucide-react";

export default function Navbar() {
  const [hoveredLink, setHoveredLink] = useState<string | null>(null);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navLinks = [
    { name: "Documentation", href: "/docs" },
    { name: "Features", href: "/features" },
    { name: "Compare", href: "/compare" },
    { name: "FAQ", href: "/faq" },
  ];

  return (
    <div className="fixed top-0 inset-x-0 z-50 flex justify-center mt-3 sm:mt-6 px-3 sm:px-4 pointer-events-none">
      <motion.header
        initial={{ y: -40, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        className={`pointer-events-auto flex flex-col px-4 sm:px-6 py-2.5 w-full max-w-[1200px] bg-white/80 backdrop-blur-2xl border border-neutral-200/80 shadow-[0_8px_30px_rgb(0,0,0,0.08)] transition-all duration-300 ${
          isMobileMenuOpen ? "rounded-[24px] pb-6" : "rounded-full"
        }`}
      >
        {/* TOP ROW: Logo and standard controls */}
        <div className="w-full flex items-center justify-between">
          {/* LEFT: Logo */}
          <Link
            href="/"
            className="group flex items-center gap-2.5 select-none outline-none"
            aria-label="Avelyn Home"
          >
            <div className="relative flex items-center justify-center transition-transform duration-300 group-hover:scale-105 group-active:scale-95">
              <Image
                src="/logo.png"
                alt="Avelyn Logo"
                width={32}
                height={32}
                className="h-7 w-7 sm:h-8 sm:w-8 object-contain"
              />
            </div>
            <span className="text-base sm:text-lg font-bold tracking-tight text-neutral-900">
              Avelyn
            </span>
          </Link>

          {/* RIGHT: Desktop Nav links, CTA and Mobile Toggle */}
          <div className="flex items-center gap-2 sm:gap-3">
            {/* CENTER: Liquid Hover Navigation (Desktop only) */}
            <nav
              className="hidden md:flex items-center gap-1"
              onMouseLeave={() => setHoveredLink(null)}
            >
              {navLinks.map((link) => (
                <Link
                  key={link.name}
                  href={link.href}
                  onMouseEnter={() => setHoveredLink(link.name)}
                  className="relative px-4 py-2 text-[13px] font-semibold text-neutral-600 hover:text-neutral-900 transition-colors duration-200 outline-none select-none"
                >
                  {hoveredLink === link.name && (
                    <motion.div
                      layoutId="nav-hover-pill"
                      className="absolute inset-0 bg-black/5 rounded-full -z-10"
                      transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                    />
                  )}
                  {link.name}
                </Link>
              ))}
            </nav>

            {/* CTA */}
            <div className="flex items-center space-x-1.5 sm:space-x-2">
              <Link
                href="/docs"
                className="hidden sm:inline-flex items-center gap-1.5 px-3.5 py-2 text-[13px] font-semibold text-[#7C3AED] hover:bg-purple-50 rounded-full transition-colors"
              >
                <BookOpen className="w-3.5 h-3.5" />
                <span>Docs</span>
              </Link>
              <Link
                href="/#beta"
                className="group flex items-center gap-1.5 rounded-full bg-[#0E0E11] px-3.5 sm:pl-4 sm:pr-5 py-2 sm:py-2.5 text-xs sm:text-[13px] font-semibold text-white shadow-sm shadow-black/10 transition-all duration-300 hover:bg-neutral-800 hover:shadow-md hover:scale-[1.02] active:scale-[0.98] outline-none"
              >
                <Sparkles className="w-3.5 h-3.5 text-neutral-400 group-hover:text-white transition-colors" />
                <span>Beta Access</span>
              </Link>
            </div>

            {/* Hamburger Toggle button */}
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="flex md:hidden p-2 rounded-full hover:bg-black/5 text-neutral-600 hover:text-neutral-900 transition-all active:scale-95 outline-none select-none"
              aria-label="Toggle Menu"
            >
              {isMobileMenuOpen ? (
                <X className="w-5 h-5" />
              ) : (
                <Menu className="w-5 h-5" />
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
              transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
              className="md:hidden overflow-hidden w-full flex flex-col mt-3 border-t border-neutral-200/60 pt-3 gap-1"
            >
              {navLinks.map((link) => (
                <Link
                  key={link.name}
                  href={link.href}
                  onClick={() => setIsMobileMenuOpen(false)}
                  className="px-4 py-3 text-sm font-semibold text-neutral-700 hover:text-[#7C3AED] hover:bg-purple-50/70 rounded-xl transition-all duration-200 flex items-center justify-between"
                >
                  <span>{link.name}</span>
                </Link>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </motion.header>
    </div>
  );
}