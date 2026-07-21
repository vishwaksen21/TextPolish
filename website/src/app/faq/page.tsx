"use client";

import React, { useState } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SchemaMarkup from "@/components/SchemaMarkup";
import { FAQ_CATEGORIES, faqDatabase } from "@/data/faqDatabase";
import { Search, ChevronDown, HelpCircle, Sparkles } from "lucide-react";

export default function FAQPage() {
  const [activeCategory, setActiveCategory] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [openItems, setOpenItems] = useState<string[]>(["inst-1", "feat-1", "priv-1"]);

  const toggleItem = (id: string) => {
    setOpenItems((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]
    );
  };

  const filteredFaqs = faqDatabase.filter((item) => {
    const matchesCategory = activeCategory === "all" || item.category === activeCategory;
    const matchesSearch =
      item.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.answer.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": faqDatabase.slice(0, 30).map((f) => ({
      "@type": "Question",
      "name": f.question,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": f.answer
      }
    }))
  };

  return (
    <div className="flex flex-col min-h-screen bg-white">
      <SchemaMarkup schema={faqSchema} />
      <Navbar />

      <main className="flex-1 pt-32 pb-20 max-w-[1200px] w-full mx-auto px-6 space-y-12">
        {/* Header */}
        <header className="text-center max-w-3xl mx-auto space-y-4">
          <span className="inline-flex items-center px-3.5 py-1 rounded-full text-xs font-semibold bg-purple-50 text-[#7C3AED] border border-purple-100 uppercase tracking-wider">
            Comprehensive Knowledgebase
          </span>
          <h1 className="text-4xl md:text-5xl font-extrabold text-neutral-900 tracking-tight leading-tight">
            Frequently Asked Questions <br />
            <span className="bg-gradient-to-r from-[#7C3AED] via-purple-600 to-indigo-600 bg-clip-text text-transparent">
              100+ Detailed Answers
            </span>
          </h1>
          <p className="text-lg text-neutral-600 leading-relaxed">
            Search our comprehensive database covering installation, local Ollama setup, OpenRouter keys, privacy architecture, and macOS troubleshooting.
          </p>

          {/* Search Box */}
          <div className="pt-4 max-w-xl mx-auto">
            <div className="relative flex items-center">
              <Search className="w-5 h-5 text-neutral-400 absolute left-4 pointer-events-none" />
              <input
                type="text"
                placeholder="Search 100+ questions (e.g. Ollama, Gemini, hotkeys, privacy)..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-12 pr-4 py-3.5 rounded-full bg-neutral-50 border border-neutral-200 text-neutral-900 placeholder-neutral-400 focus:outline-none focus:border-[#7C3AED] focus:bg-white transition-all shadow-sm"
              />
            </div>
          </div>
        </header>

        {/* Category Tabs */}
        <section aria-label="FAQ Category Filters">
          <div className="flex items-center gap-2 overflow-x-auto pb-4 scrollbar-none justify-start md:justify-center flex-wrap">
            {FAQ_CATEGORIES.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setActiveCategory(cat.id)}
                className={`px-4 py-2 rounded-full text-xs font-bold transition-all whitespace-nowrap ${
                  activeCategory === cat.id
                    ? "bg-[#7C3AED] text-white shadow-md"
                    : "bg-neutral-100 text-neutral-600 hover:bg-neutral-200"
                }`}
              >
                {cat.label}
              </button>
            ))}
          </div>
        </section>

        {/* FAQ Accordion List */}
        <section className="max-w-4xl mx-auto space-y-4" aria-label="FAQ Accordion">
          <div className="text-xs font-bold uppercase tracking-wider text-neutral-400 mb-2">
            Showing {filteredFaqs.length} Answers
          </div>

          {filteredFaqs.length === 0 ? (
            <div className="text-center py-12 text-neutral-500 bg-neutral-50 rounded-2xl border border-neutral-200">
              No matching questions found for "{searchQuery}". Try searching for another term.
            </div>
          ) : (
            filteredFaqs.map((faq) => {
              const isOpen = openItems.includes(faq.id);
              return (
                <div
                  key={faq.id}
                  className="rounded-2xl border border-neutral-200/80 bg-white overflow-hidden transition-all shadow-sm hover:border-purple-200"
                >
                  <button
                    onClick={() => toggleItem(faq.id)}
                    className="w-full flex items-center justify-between p-6 text-left hover:bg-neutral-50/50 transition-colors"
                    aria-expanded={isOpen}
                  >
                    <span className="text-base md:text-lg font-bold text-neutral-900 pr-4">
                      {faq.question}
                    </span>
                    <ChevronDown
                      className={`w-5 h-5 text-neutral-400 transition-transform duration-200 flex-shrink-0 ${
                        isOpen ? "rotate-180 text-[#7C3AED]" : ""
                      }`}
                    />
                  </button>

                  {isOpen && (
                    <div className="px-6 pb-6 text-sm md:text-base text-neutral-600 leading-relaxed border-t border-neutral-100 pt-4">
                      {faq.answer}
                    </div>
                  )}
                </div>
              );
            })
          )}
        </section>
      </main>

      <Footer />
    </div>
  );
}
