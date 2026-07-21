import { Metadata } from "next";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Breadcrumbs from "@/components/Breadcrumbs";
import SchemaMarkup from "@/components/SchemaMarkup";
import InteractiveComparison from "@/components/InteractiveComparison";

export const metadata: Metadata = {
  title: "Avelyn vs Microsoft Copilot (2026 Comparison) — Local Privacy vs Cloud Suite",
  description: "Detailed comparison between Avelyn and Microsoft Copilot. Discover why Avelyn's zero telemetry and local Ollama engine outperform Copilot for Mac users.",
  alternates: { canonical: "https://avelyn.software/compare/avelyn-vs-copilot" },
};

export default function AvelynVsCopilotPage() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "Avelyn vs Microsoft Copilot Comparison",
    "url": "https://avelyn.software/compare/avelyn-vs-copilot"
  };

  const breadcrumbs = [
    { label: "Comparisons", href: "/compare" },
    { label: "Avelyn vs Microsoft Copilot" }
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
            Avelyn vs Microsoft Copilot
          </h1>
          <p className="text-lg text-neutral-600 leading-relaxed">
            Local offline AI execution, system-wide Mac hotkeys, and zero subscription fees.
          </p>
        </header>

        <InteractiveComparison competitor="Copilot" />
      </main>

      <Footer />
    </div>
  );
}
