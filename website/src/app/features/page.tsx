import { Metadata } from "next";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SchemaMarkup from "@/components/SchemaMarkup";
import { Sparkles, ArrowRight, Zap, Shield, Globe, Code, FileText, CheckCircle, Mail, MessageSquare, Layers } from "lucide-react";

export const metadata: Metadata = {
  title: "Avelyn Features — System-Wide AI Writing, Coding & Privacy Suite",
  description: "Explore Avelyn's complete feature suite: Prompt Enhancement, Grammar Correction, AI Email Writing, Coding Assistant, Translation, and Local Offline AI.",
  alternates: { canonical: "https://avelyn.software/features" },
};

const featureCards = [
  { slug: "prompt-enhancer", title: "Prompt Enhancer", desc: "Turn vague 3-word notes into structured LLM prompts." },
  { slug: "grammar-checker", title: "Grammar Checker AI", desc: "Neural grammar, syntax, and punctuation fixing." },
  { slug: "email-writer", title: "AI Email Writer", desc: "Draft executive emails from bullet points in Mail or Outlook." },
  { slug: "ai-rewriter", title: "AI Text Rewriter", desc: "Paraphrase, rephrase, expand, or condense text." },
  { slug: "ai-summarizer", title: "AI Text Summarizer", desc: "Condense long articles and PDFs into executive bullet points." },
  { slug: "translation", title: "AI Translation Tool", desc: "Instant translation across 50+ languages system-wide." },
  { slug: "coding-assistant", title: "AI Coding Assistant", desc: "Refactor, explain, and debug code snippets inside any IDE." },
  { slug: "local-ai", title: "Local Offline AI Engine", desc: "100% offline LLMs via Ollama with zero cloud telemetry." },
  { slug: "cloud-ai", title: "Cloud AI Engine", desc: "Connect Google Gemini Flash and OpenRouter API keys." },
  { slug: "mac-ai-assistant", title: "Mac AI Assistant", desc: "Native macOS menu bar integration and double-tap hotkeys." },
  { slug: "ai-writing-assistant", title: "AI Writing Assistant", desc: "Executive tone shifting and report drafting." },
];

export default function FeaturesHubPage() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Avelyn Feature Suite",
    "operatingSystem": "macOS",
    "url": "https://avelyn.software/features"
  };

  return (
    <div className="flex flex-col min-h-screen bg-white">
      <SchemaMarkup schema={schema} />
      <Navbar />

      <main className="flex-1 pt-32 pb-20 max-w-[1200px] w-full mx-auto px-6">
        <header className="mb-12 text-center max-w-3xl mx-auto space-y-4">
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-purple-50 text-[#7C3AED] border border-purple-100 uppercase tracking-wider">
            Comprehensive Capabilities
          </span>
          <h1 className="text-4xl md:text-5xl font-extrabold text-neutral-900 tracking-tight leading-tight">
            System-Wide AI Features for <br />
            <span className="bg-gradient-to-r from-[#7C3AED] via-purple-600 to-indigo-600 bg-clip-text text-transparent">
              macOS Power Users
            </span>
          </h1>
          <p className="text-lg text-neutral-600 leading-relaxed">
            Refine writing, generate code, translate languages, and enhance prompts everywhere you type on Mac.
          </p>
        </header>

        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" aria-label="Feature Cards">
          {featureCards.map((feat) => (
            <Link
              key={feat.slug}
              href={`/features/${feat.slug}`}
              className="group p-6 rounded-2xl border border-neutral-200/80 bg-white hover:border-[#7C3AED]/40 hover:shadow-xl transition-all flex flex-col justify-between"
            >
              <div>
                <div className="p-3 rounded-xl bg-purple-50 text-[#7C3AED] w-fit mb-4 group-hover:bg-[#7C3AED] group-hover:text-white transition-colors">
                  <Layers className="w-5 h-5" />
                </div>
                <h3 className="text-xl font-bold text-neutral-900 group-hover:text-[#7C3AED] transition-colors mb-2">
                  {feat.title}
                </h3>
                <p className="text-sm text-neutral-600 leading-relaxed">
                  {feat.desc}
                </p>
              </div>

              <div className="pt-6 mt-4 border-t border-neutral-100 flex items-center text-xs font-bold text-[#7C3AED]">
                <span>Explore {feat.title}</span>
                <ArrowRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
              </div>
            </Link>
          ))}
        </section>
      </main>

      <Footer />
    </div>
  );
}
