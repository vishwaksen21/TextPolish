import { Metadata } from "next";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SchemaMarkup from "@/components/SchemaMarkup";
import { Shield, Sparkles, Heart, Code } from "lucide-react";

export const metadata: Metadata = {
  title: "About Avelyn — Our Privacy-First AI Mission & Story",
  description: "Learn why we built Avelyn: combining local LLMs, cloud APIs, and native macOS automation into a single private workflow tool.",
  alternates: { canonical: "https://avelyn.software/trust/about" },
};

export default function AboutTrustPage() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "AboutPage",
    "name": "About Avelyn",
    "url": "https://avelyn.software/trust/about"
  };

  return (
    <div className="flex flex-col min-h-screen bg-white">
      <SchemaMarkup schema={schema} />
      <Navbar />

      <main className="flex-1 pt-32 pb-20 max-w-4xl w-full mx-auto px-6 space-y-12">
        <header className="space-y-4">
          <span className="inline-flex items-center px-3.5 py-1 rounded-full text-xs font-semibold bg-purple-50 text-[#7C3AED] border border-purple-100 uppercase tracking-wider">
            About Avelyn
          </span>
          <h1 className="text-4xl md:text-5xl font-extrabold text-neutral-900 tracking-tight leading-tight">
            Building Software That Respects <br />
            <span className="bg-gradient-to-r from-[#7C3AED] via-purple-600 to-indigo-600 bg-clip-text text-transparent">
              Your Workspace Privacy
            </span>
          </h1>
          <p className="text-lg text-neutral-600 leading-relaxed">
            Avelyn was created with a straightforward goal: bring fast, system-wide AI text refinement directly to your keyboard cursor without tracking your keystrokes or logging your sensitive drafts.
          </p>
        </header>

        <section className="prose prose-purple max-w-none text-neutral-800 space-y-6">
          <h2>Our Core Philosophy</h2>
          <p>
            We believe desktop tools should operate as extensions of your mind. You shouldn't have to copy text into web browser tabs, navigate through advertisement popups, or worry about third-party web scrapers training on your confidential proposals.
          </p>
          <p>
            By leveraging Apple Silicon Unified Memory and open-source models like Gemma 3 via Ollama, Avelyn turns your Mac into a self-contained AI workstation.
          </p>
        </section>
      </main>

      <Footer />
    </div>
  );
}
