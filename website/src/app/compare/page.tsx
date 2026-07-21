import { Metadata } from "next";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SchemaMarkup from "@/components/SchemaMarkup";
import { comparisonsData } from "@/data/comparisonsData";
import { ArrowRight, Scale, CheckCircle2, XCircle } from "lucide-react";

export const metadata: Metadata = {
  title: "Avelyn Comparisons — How Avelyn Compares to ChatGPT, Grammarly, Gemini & Claude",
  description: "Detailed feature, privacy, pricing, and latency comparisons between Avelyn and ChatGPT, Grammarly, Google Gemini, Claude 3.5, Copilot, and Notion AI.",
  alternates: { canonical: "https://avelyn.software/compare" },
};

export default function ComparisonHubPage() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "Avelyn Product Comparisons Hub",
    "url": "https://avelyn.software/compare"
  };

  const competitors = Object.values(comparisonsData);

  return (
    <div className="flex flex-col min-h-screen bg-white">
      <SchemaMarkup schema={schema} />
      <Navbar />

      <main className="flex-1 pt-32 pb-20 max-w-[1200px] w-full mx-auto px-6">
        <header className="mb-12 text-center max-w-3xl mx-auto space-y-4">
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-purple-50 text-[#7C3AED] border border-purple-100 uppercase tracking-wider">
            Architectural Comparison
          </span>
          <h1 className="text-4xl md:text-5xl font-extrabold text-neutral-900 tracking-tight leading-tight">
            How Avelyn Compares to <br />
            <span className="bg-gradient-to-r from-[#7C3AED] via-purple-600 to-indigo-600 bg-clip-text text-transparent">
              Popular AI Tools
            </span>
          </h1>
          <p className="text-lg text-neutral-600 leading-relaxed">
            See how system-wide macOS hotkey automation, local offline processing, and zero telemetry stack up against browser web chats and cloud subscription tools.
          </p>
        </header>

        <section className="grid grid-cols-1 md:grid-cols-2 gap-8" aria-label="Competitor Comparisons">
          {competitors.map((comp) => (
            <div
              key={comp.slug}
              className="rounded-3xl border border-neutral-200/80 bg-white p-8 shadow-sm hover:shadow-xl transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className="inline-flex items-center space-x-2 text-xs font-bold text-[#7C3AED] uppercase tracking-wider bg-purple-50 px-3 py-1 rounded-full border border-purple-100">
                    <Scale className="w-3.5 h-3.5" />
                    <span>Avelyn vs {comp.name}</span>
                  </div>
                </div>

                <h3 className="text-2xl font-bold text-neutral-900 mb-2">
                  {comp.headline}
                </h3>
                <p className="text-sm text-neutral-600 leading-relaxed mb-6">
                  {comp.description}
                </p>

                <div className="space-y-2 mb-6">
                  <div className="text-xs font-bold uppercase tracking-wider text-neutral-400">Pricing Comparison</div>
                  <div className="text-xs text-neutral-700 font-semibold bg-neutral-50 p-3 rounded-xl border border-neutral-100">
                    <div><span className="text-[#7C3AED] font-bold">Avelyn:</span> {comp.pricingComparison.avelyn}</div>
                    <div className="mt-1"><span className="text-neutral-500 font-bold">{comp.name}:</span> {comp.pricingComparison.competitor}</div>
                  </div>
                </div>
              </div>

              <Link
                href={`/compare/${comp.slug}`}
                className="inline-flex items-center justify-center space-x-2 w-full py-3 rounded-xl bg-[#0E0E11] text-white text-sm font-bold hover:bg-neutral-800 transition-colors"
              >
                <span>Read Full Comparison</span>
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          ))}
        </section>
      </main>

      <Footer />
    </div>
  );
}
