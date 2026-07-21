import { Metadata } from "next";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Breadcrumbs from "@/components/Breadcrumbs";
import SchemaMarkup from "@/components/SchemaMarkup";
import InteractiveComparison from "@/components/InteractiveComparison";

export const metadata: Metadata = {
  title: "Avelyn vs Google Gemini (2026 Comparison) — Native Mac vs Web Chat",
  description: "Detailed comparison between Avelyn and Google Gemini. Discover why system-wide hotkeys, local Ollama fallbacks, and zero telemetry beat web apps.",
  alternates: { canonical: "https://avelyn.software/compare/avelyn-vs-gemini" },
};

export default function AvelynVsGeminiPage() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "Avelyn vs Google Gemini Comparison",
    "description": "Comparison of Avelyn macOS assistant vs Google Gemini Web.",
    "url": "https://avelyn.software/compare/avelyn-vs-gemini"
  };

  const breadcrumbs = [
    { label: "Comparisons", href: "/compare" },
    { label: "Avelyn vs Google Gemini" }
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
            Avelyn vs Google Gemini
          </h1>
          <p className="text-lg text-neutral-600 leading-relaxed">
            Use Google Gemini Flash system-wide inside any Mac application while keeping local offline Ollama fallbacks ready.
          </p>
        </header>

        <InteractiveComparison competitor="Gemini" />
      </main>

      <Footer />
    </div>
  );
}
