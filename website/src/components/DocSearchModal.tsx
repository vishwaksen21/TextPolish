"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { Search, X, BookOpen, Layers, HelpCircle, ArrowRight } from "lucide-react";
import { getFlatDocList } from "@/data/docsNavigation";
import { faqDatabase } from "@/data/faqDatabase";

interface DocSearchModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function DocSearchModal({ isOpen, onClose }: DocSearchModalProps) {
  const [query, setQuery] = useState("");
  const flatDocs = getFlatDocList();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        if (isOpen) onClose();
        else setQuery("");
      }
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const filteredDocs = flatDocs.filter(
    (d) =>
      d.item.title.toLowerCase().includes(query.toLowerCase()) ||
      (d.item.description && d.item.description.toLowerCase().includes(query.toLowerCase())) ||
      d.category.toLowerCase().includes(query.toLowerCase())
  );

  const filteredFaqs = faqDatabase
    .filter(
      (f) =>
        f.question.toLowerCase().includes(query.toLowerCase()) ||
        f.answer.toLowerCase().includes(query.toLowerCase())
    )
    .slice(0, 5);

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-16 px-4 bg-black/60 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-2xl bg-white rounded-2xl shadow-2xl border border-neutral-200 overflow-hidden flex flex-col max-h-[80vh]">
        {/* Search Header */}
        <div className="flex items-center px-4 py-3 border-b border-neutral-100 bg-neutral-50/50">
          <Search className="w-5 h-5 text-neutral-400 mr-3 flex-shrink-0" />
          <input
            type="text"
            placeholder="Search documentation, features, FAQs..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-transparent text-neutral-900 placeholder-neutral-400 focus:outline-none text-base"
            autoFocus
          />
          <button
            onClick={onClose}
            className="p-1 rounded-lg hover:bg-neutral-200 text-neutral-500 transition-colors ml-2"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Search Results */}
        <div className="overflow-y-auto p-4 space-y-6 flex-1">
          {/* Docs Section */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-400 mb-3 px-2 flex items-center">
              <BookOpen className="w-3.5 h-3.5 mr-1.5" />
              Documentation Articles ({filteredDocs.length})
            </h4>
            {filteredDocs.length === 0 ? (
              <p className="text-sm text-neutral-500 px-2 py-1">No matching documentation pages.</p>
            ) : (
              <div className="space-y-1">
                {filteredDocs.slice(0, 8).map((d, idx) => (
                  <Link
                    key={idx}
                    href={`/docs/${d.categorySlug}/${d.item.slug}`}
                    onClick={onClose}
                    className="flex items-center justify-between p-2.5 rounded-xl hover:bg-purple-50/80 transition-colors group"
                  >
                    <div>
                      <div className="text-xs font-semibold text-[#7C3AED]">{d.category}</div>
                      <div className="text-sm font-bold text-neutral-900 group-hover:text-[#7C3AED] transition-colors">
                        {d.item.title}
                      </div>
                      {d.item.description && (
                        <div className="text-xs text-neutral-500 line-clamp-1">{d.item.description}</div>
                      )}
                    </div>
                    <ArrowRight className="w-4 h-4 text-neutral-400 group-hover:text-[#7C3AED] group-hover:translate-x-1 transition-all flex-shrink-0" />
                  </Link>
                ))}
              </div>
            )}
          </div>

          {/* FAQs Section */}
          {filteredFaqs.length > 0 && (
            <div className="pt-4 border-t border-neutral-100">
              <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-400 mb-3 px-2 flex items-center">
                <HelpCircle className="w-3.5 h-3.5 mr-1.5" />
                Matching FAQs ({filteredFaqs.length})
              </h4>
              <div className="space-y-2">
                {filteredFaqs.map((faq) => (
                  <div key={faq.id} className="p-3 rounded-xl bg-neutral-50 border border-neutral-100">
                    <div className="text-xs font-bold text-neutral-900">{faq.question}</div>
                    <div className="text-xs text-neutral-600 mt-1 line-clamp-2">{faq.answer}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-4 py-2.5 bg-neutral-50 border-t border-neutral-100 flex items-center justify-between text-xs text-neutral-400">
          <span>Search documentation across 50+ topics</span>
          <span className="flex items-center gap-1">
            <kbd className="px-1.5 py-0.5 rounded bg-neutral-200 text-neutral-700 font-mono text-[10px]">ESC</kbd> to close
          </span>
        </div>
      </div>
    </div>
  );
}
