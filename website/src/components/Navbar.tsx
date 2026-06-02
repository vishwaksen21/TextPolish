"use client";

import React from "react";
import Image from "next/image";

export default function Navbar() {
  const navLinks = [
    { name: "Features", href: "#features" },
    { name: "How It Works", href: "#how-it-works" },
    { name: "FAQ", href: "#faq" },
  ];

  return (
    <header className="w-full border-b border-neutral-200/60 bg-white">
      <div className="mx-auto max-w-[1120px] px-6 h-16 flex items-center justify-between">
        <a
          href="#"
          className="flex items-center gap-2.5 select-none"
          aria-label="Avelyn"
        >
          <Image src="/logo.png" alt="Avelyn" width={32} height={32} className="h-8 w-8" />
          <span className="text-[15px] sm:text-base font-semibold tracking-tight text-neutral-950">
            Avelyn
          </span>
        </a>

        <nav className="hidden md:flex items-center gap-8">
          {navLinks.map((link) => (
            <a
              key={link.name}
              href={link.href}
              className="text-sm font-medium text-neutral-600 hover:text-neutral-900 transition-colors"
            >
              {link.name}
            </a>
          ))}
        </nav>

        <a
          href="https://github.com/vishwaksen21/Avelyn/releases"
          className="inline-flex items-center justify-center rounded-full bg-neutral-900 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-neutral-800 active:scale-[0.99] transition"
        >
          Download for macOS
        </a>
      </div>
    </header>
  );
}
