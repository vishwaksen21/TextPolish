import React from "react";
import Link from "next/link";
import { ArrowRight, BookOpen, Layers, Scale } from "lucide-react";

export interface LinkItem {
  title: string;
  href: string;
  description?: string;
  category?: string;
}

interface RelatedLinksProps {
  title?: string;
  docs?: LinkItem[];
  features?: LinkItem[];
  comparisons?: LinkItem[];
}

export default function RelatedLinks({
  title = "Related Resources & Documentation",
  docs = [],
  features = [],
  comparisons = [],
}: RelatedLinksProps) {
  const hasLinks = docs.length > 0 || features.length > 0 || comparisons.length > 0;
  if (!hasLinks) return null;

  return (
    <section className="mt-12 pt-8 border-t border-neutral-200" aria-label="Related links">
      <h3 className="text-xl font-bold text-neutral-900 mb-6 flex items-center">
        <span>{title}</span>
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {docs.map((doc, idx) => (
          <Link
            key={`doc-${idx}`}
            href={doc.href}
            className="group p-4 rounded-xl border border-neutral-200/80 bg-white hover:border-[#7C3AED]/40 hover:shadow-md transition-all flex items-start space-x-3"
          >
            <div className="p-2 rounded-lg bg-purple-50 text-[#7C3AED] group-hover:bg-[#7C3AED] group-hover:text-white transition-colors">
              <BookOpen className="w-4 h-4" />
            </div>
            <div className="flex-1 min-w-0">
              <span className="text-xs font-semibold text-[#7C3AED] uppercase tracking-wider block mb-0.5">Documentation</span>
              <h4 className="text-sm font-semibold text-neutral-900 group-hover:text-[#7C3AED] transition-colors truncate">
                {doc.title}
              </h4>
              {doc.description && (
                <p className="text-xs text-neutral-500 mt-1 line-clamp-1">{doc.description}</p>
              )}
            </div>
            <ArrowRight className="w-4 h-4 text-neutral-400 group-hover:translate-x-1 transition-transform self-center" />
          </Link>
        ))}

        {features.map((feat, idx) => (
          <Link
            key={`feat-${idx}`}
            href={feat.href}
            className="group p-4 rounded-xl border border-neutral-200/80 bg-white hover:border-[#7C3AED]/40 hover:shadow-md transition-all flex items-start space-x-3"
          >
            <div className="p-2 rounded-lg bg-blue-50 text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition-colors">
              <Layers className="w-4 h-4" />
            </div>
            <div className="flex-1 min-w-0">
              <span className="text-xs font-semibold text-blue-600 uppercase tracking-wider block mb-0.5">Feature</span>
              <h4 className="text-sm font-semibold text-neutral-900 group-hover:text-blue-600 transition-colors truncate">
                {feat.title}
              </h4>
              {feat.description && (
                <p className="text-xs text-neutral-500 mt-1 line-clamp-1">{feat.description}</p>
              )}
            </div>
            <ArrowRight className="w-4 h-4 text-neutral-400 group-hover:translate-x-1 transition-transform self-center" />
          </Link>
        ))}

        {comparisons.map((comp, idx) => (
          <Link
            key={`comp-${idx}`}
            href={comp.href}
            className="group p-4 rounded-xl border border-neutral-200/80 bg-white hover:border-[#7C3AED]/40 hover:shadow-md transition-all flex items-start space-x-3"
          >
            <div className="p-2 rounded-lg bg-emerald-50 text-emerald-600 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
              <Scale className="w-4 h-4" />
            </div>
            <div className="flex-1 min-w-0">
              <span className="text-xs font-semibold text-emerald-600 uppercase tracking-wider block mb-0.5">Comparison</span>
              <h4 className="text-sm font-semibold text-neutral-900 group-hover:text-emerald-600 transition-colors truncate">
                {comp.title}
              </h4>
              {comp.description && (
                <p className="text-xs text-neutral-500 mt-1 line-clamp-1">{comp.description}</p>
              )}
            </div>
            <ArrowRight className="w-4 h-4 text-neutral-400 group-hover:translate-x-1 transition-transform self-center" />
          </Link>
        ))}
      </div>
    </section>
  );
}
