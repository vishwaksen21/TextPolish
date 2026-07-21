"use client";

import React, { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronRight, Search, Menu, X, BookOpen, Home } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import DocSearchModal from "@/components/DocSearchModal";
import { docCategories } from "@/data/docsNavigation";

interface DocsLayoutProps {
  children: React.ReactNode;
}

export default function DocsLayout({ children }: DocsLayoutProps) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [expandedCategories, setExpandedCategories] = useState<string[]>([
    "getting-started",
    "features",
    "providers"
  ]);

  const toggleCategory = (slug: string) => {
    setExpandedCategories((prev) =>
      prev.includes(slug) ? prev.filter((c) => c !== slug) : [...prev, slug]
    );
  };

  return (
    <div className="flex flex-col min-h-screen bg-white">
      <Navbar />

      <div className="pt-28 pb-12 flex-1 max-w-[1400px] w-full mx-auto px-4 sm:px-6">
        {/* Docs Sub-header Search & Quick Jump Bar */}
        <div className="mb-6 flex flex-col sm:flex-row items-center justify-between gap-4 p-4 rounded-2xl bg-neutral-50 border border-neutral-200/80">
          <div className="flex items-center space-x-3 text-sm text-neutral-600">
            <BookOpen className="w-5 h-5 text-[#7C3AED]" />
            <span className="font-bold text-neutral-900">Avelyn Documentation Center</span>
            <span className="hidden sm:inline text-neutral-300">|</span>
            <span className="hidden sm:inline text-xs text-neutral-500">v2.1 Guide & Specs</span>
          </div>

          <button
            onClick={() => setIsSearchOpen(true)}
            className="w-full sm:w-auto flex items-center justify-between px-4 py-2 rounded-xl bg-white border border-neutral-200 text-sm text-neutral-500 hover:text-neutral-900 hover:border-[#7C3AED]/40 shadow-sm transition-all group"
          >
            <span className="flex items-center">
              <Search className="w-4 h-4 mr-2 text-neutral-400 group-hover:text-[#7C3AED] transition-colors" />
              <span>Search docs...</span>
            </span>
            <kbd className="ml-4 px-1.5 py-0.5 text-[10px] font-mono rounded bg-neutral-100 border border-neutral-200 text-neutral-500">
              ⌘K
            </kbd>
          </button>
        </div>

        <div className="flex flex-col md:flex-row gap-8 relative items-start">
          {/* Mobile Sidebar Toggle Button */}
          <button
            className="fixed bottom-6 right-6 md:hidden z-50 p-3.5 rounded-full bg-[#7C3AED] text-white shadow-xl hover:bg-[#6D28D9] transition-all"
            onClick={() => setIsSidebarOpen(true)}
            aria-label="Open documentation sidebar"
          >
            <Menu className="w-6 h-6" />
          </button>

          {/* Sidebar Drawer Overlay for Mobile */}
          <AnimatePresence>
            {isSidebarOpen && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 md:hidden z-40 bg-black/50 backdrop-blur-sm"
                onClick={() => setIsSidebarOpen(false)}
              />
            )}
          </AnimatePresence>

          {/* Docs Sidebar */}
          <aside
            className={`fixed md:sticky top-28 w-72 md:w-72 flex-shrink-0 bg-white border border-neutral-200/80 rounded-2xl p-4 h-[calc(100vh-8rem)] overflow-y-auto z-40 transform transition-transform duration-300 ease-in-out shadow-sm ${
              isSidebarOpen ? "left-4 translate-x-0" : "-translate-x-full md:translate-x-0"
            }`}
            aria-label="Documentation navigation"
          >
            <div className="flex items-center justify-between pb-3 mb-4 border-b border-neutral-100">
              <Link href="/docs" className="text-xs font-bold uppercase tracking-wider text-neutral-400 hover:text-[#7C3AED]">
                All Documentation
              </Link>
              <button onClick={() => setIsSidebarOpen(false)} className="md:hidden p-1 text-neutral-400">
                <X className="w-4 h-4" />
              </button>
            </div>

            <nav className="space-y-4" aria-label="Documentation sidebar">
              {docCategories.map((category) => {
                const isExpanded = expandedCategories.includes(category.slug);
                return (
                  <div key={category.slug} className="space-y-1">
                    <button
                      onClick={() => toggleCategory(category.slug)}
                      className="w-full flex items-center justify-between px-2.5 py-1.5 text-xs font-bold text-neutral-800 uppercase tracking-wider hover:bg-neutral-50 rounded-lg transition-colors text-left"
                      aria-expanded={isExpanded}
                    >
                      <span>{category.title}</span>
                      <motion.div animate={{ rotate: isExpanded ? 90 : 0 }} transition={{ duration: 0.2 }}>
                        <ChevronRight className="w-3.5 h-3.5 text-neutral-400" />
                      </motion.div>
                    </button>

                    <AnimatePresence initial={false}>
                      {isExpanded && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: "auto", opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          transition={{ duration: 0.2 }}
                          className="overflow-hidden pl-2 space-y-0.5 border-l-2 border-purple-100 ml-2 mt-1"
                        >
                          {category.items.map((item) => (
                            <Link
                              key={item.slug}
                              href={`/docs/${category.slug}/${item.slug}`}
                              onClick={() => setIsSidebarOpen(false)}
                              className="block px-3 py-1.5 text-xs font-medium text-neutral-600 hover:text-[#7C3AED] hover:bg-purple-50/60 rounded-md transition-colors"
                            >
                              {item.title}
                            </Link>
                          ))}
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                );
              })}
            </nav>
          </aside>

          {/* Main Docs Content Stream */}
          <main className="flex-1 w-full min-w-0 bg-white rounded-2xl border border-neutral-200/80 p-6 md:p-10 shadow-sm">
            {children}
          </main>
        </div>
      </div>

      <DocSearchModal isOpen={isSearchOpen} onClose={() => setIsSearchOpen(false)} />

      <Footer />
    </div>
  );
}