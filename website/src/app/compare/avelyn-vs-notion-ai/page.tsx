import { Metadata } from "next";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Breadcrumbs from "@/components/Breadcrumbs";
import SchemaMarkup from "@/components/SchemaMarkup";
import InteractiveComparison from "@/components/InteractiveComparison";

export const metadata: Metadata = {
  title: "Avelyn vs Notion AI (2026 Comparison) — System-Wide vs Single App",
  description: "Compare Avelyn and Notion AI. Learn why system-wide text enhancement across Mail, Xcode, Slack, and Safari beats single-app AI.",
  alternates: { canonical: "https://avelyn.software/compare/avelyn-vs-notion-ai" },
};

export default function AvelynVsNotionAIPage() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "Avelyn vs Notion AI Comparison",
    "url": "https://avelyn.software/compare/avelyn-vs-[#notion-ai]"
  };

  const breadcrumbs = [
    { label: "Comparisons", href: "/compare" },
    { label: "Avelyn vs Notion AI" }
  ];

  return (
    <div className="flex flex-col min-h-screen bg-white">
      <SchemaMarkup schema={schema} />
      <Navbar />

      <main className="flex-1 pt-32 pb-20 max-w-[1200px] w-full mx-auto px-6 space-y-12">
        <Breadcrumbs items={breadcrumbs} />

        <header className="text-center max-w-3xl mx-auto space-y-4">
          <span className="inline-flex items-center px-3.5 py-1 rounded-full text-xs font-semibold bg-purple-50 text-[#7C3AED] border border-purple-100 uppercase tracking-wider">
            Detailed Benchmark
          </span>
          <h1 className="text-4xl md:text-5xl font-extrabold text-neutral-900 tracking-tight">
            Avelyn vs Notion AI
          </h1>
          <p className="text-lg text-neutral-600 leading-relaxed">
            Enhance text in Notion, Slack, Xcode, Apple Notes, and Mail without paying $10/mo single-app add-ons.
          </p>
        </header>

        <InteractiveComparison competitor="Notion AI" />
      </main>

      <Footer />
    </div>
  );
}
