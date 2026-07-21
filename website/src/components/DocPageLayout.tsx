"use client";

import React from "react";
import Link from "next/link";
import { ArrowLeft, ArrowRight, BookOpen, Clock, Tag } from "lucide-react";
import Breadcrumbs, { BreadcrumbItem } from "./Breadcrumbs";
import RelatedLinks, { LinkItem } from "./RelatedLinks";
import { getFlatDocList } from "@/data/docsNavigation";

interface DocPageLayoutProps {
  categoryTitle: string;
  categorySlug: string;
  itemSlug: string;
  title: string;
  description: string;
  children: React.ReactNode;
  relatedDocs?: LinkItem[];
  relatedFeatures?: LinkItem[];
}

export default function DocPageLayout({
  categoryTitle,
  categorySlug,
  itemSlug,
  title,
  description,
  children,
  relatedDocs = [],
  relatedFeatures = [],
}: DocPageLayoutProps) {
  const flat = getFlatDocList();
  const currentIndex = flat.findIndex(
    (f) => f.categorySlug === categorySlug && f.item.slug === itemSlug
  );

  const prevDoc = currentIndex > 0 ? flat[currentIndex - 1] : null;
  const nextDoc = currentIndex < flat.length - 1 ? flat[currentIndex + 1] : null;

  const breadcrumbItems: BreadcrumbItem[] = [
    { label: "Documentation", href: "/docs" },
    { label: categoryTitle, href: `/docs#${categorySlug}` },
    { label: title },
  ];

  return (
    <article className="max-w-4xl mx-auto px-4 py-8 md:py-12">
      <Breadcrumbs items={breadcrumbItems} />

      {/* Header */}
      <header className="mb-8 border-b border-neutral-200 pb-8">
        <div className="inline-flex items-center space-x-2 text-xs font-semibold uppercase tracking-wider text-[#7C3AED] bg-purple-50 px-3 py-1 rounded-full border border-purple-100 mb-3">
          <BookOpen className="w-3.5 h-3.5" />
          <span>{categoryTitle}</span>
        </div>
        <h1 className="text-3xl md:text-4xl font-extrabold text-neutral-900 tracking-tight mb-3">
          {title}
        </h1>
        <p className="text-lg text-neutral-600 leading-relaxed max-w-3xl">
          {description}
        </p>
      </header>

      {/* Body Content */}
      <div className="prose prose-purple max-w-none prose-headings:font-bold prose-headings:text-neutral-900 prose-p:text-neutral-700 prose-p:leading-relaxed prose-li:text-neutral-700 prose-code:text-[#7C3AED] prose-code:bg-purple-50 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:font-mono text-neutral-800 space-y-6">
        {children}
      </div>

      {/* Related Internal Links */}
      <RelatedLinks docs={relatedDocs} features={relatedFeatures} />

      {/* Next / Previous Article Pagination */}
      <nav aria-label="Article navigation" className="mt-12 pt-8 border-t border-neutral-200 grid grid-cols-1 md:grid-cols-2 gap-4">
        {prevDoc ? (
          <Link
            href={`/docs/${prevDoc.categorySlug}/${prevDoc.item.slug}`}
            className="group p-4 rounded-xl border border-neutral-200 hover:border-[#7C3AED]/40 hover:bg-purple-50/20 transition-all flex items-center space-x-3 text-left"
          >
            <ArrowLeft className="w-5 h-5 text-neutral-400 group-hover:text-[#7C3AED] group-hover:-translate-x-1 transition-all flex-shrink-0" />
            <div>
              <span className="text-xs text-neutral-500 uppercase tracking-wider block">Previous</span>
              <span className="text-sm font-bold text-neutral-900 group-hover:text-[#7C3AED] transition-colors line-clamp-1">
                {prevDoc.item.title}
              </span>
            </div>
          </Link>
        ) : (
          <div />
        )}

        {nextDoc ? (
          <Link
            href={`/docs/${nextDoc.categorySlug}/${nextDoc.item.slug}`}
            className="group p-4 rounded-xl border border-neutral-200 hover:border-[#7C3AED]/40 hover:bg-purple-50/20 transition-all flex items-center justify-between space-x-3 text-right md:col-start-2"
          >
            <div>
              <span className="text-xs text-neutral-500 uppercase tracking-wider block">Next</span>
              <span className="text-sm font-bold text-neutral-900 group-hover:text-[#7C3AED] transition-colors line-clamp-1">
                {nextDoc.item.title}
              </span>
            </div>
            <ArrowRight className="w-5 h-5 text-neutral-400 group-hover:text-[#7C3AED] group-hover:translate-x-1 transition-all flex-shrink-0" />
          </Link>
        ) : null}
      </nav>
    </article>
  );
}
