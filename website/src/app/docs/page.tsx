import { Metadata } from "next";
import Link from "next/link";
import { ArrowRight, Sparkles, Zap, Shield, Globe, Terminal, FileText, CheckCircle, HelpCircle } from "lucide-react";
import SchemaMarkup from "@/components/SchemaMarkup";
import { docCategories } from "@/data/docsNavigation";

export const metadata: Metadata = {
  title: "Avelyn Documentation — User Guides, API Setup & Performance Specs",
  description: "Complete documentation for Avelyn — the privacy-first local AI writing assistant for macOS. Learn installation, feature modes, local Ollama, OpenRouter, Gemini Flash, and security.",
  alternates: {
    canonical: "https://avelyn.software/docs",
  },
  openGraph: {
    title: "Avelyn Documentation — Guides & Technical Specs",
    description: "Learn how to configure local LLMs (Ollama), cloud providers (Gemini, OpenRouter), and system-wide macOS hotkeys with Avelyn.",
    url: "https://avelyn.software/docs",
    type: "website",
  },
};

export default function DocsPage() {
  const docsSchema = {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "name": "Avelyn Documentation Center",
    "headline": "Complete User Guide & Technical Manual for Avelyn macOS AI Assistant",
    "description": "Comprehensive documentation for setting up local Ollama models, cloud APIs, global hotkeys, and privacy rules on macOS.",
    "url": "https://avelyn.software/docs",
    "author": {
      "@type": "Organization",
      "name": "Avelyn Software"
    }
  };

  const breadcrumbSchema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://avelyn.software" },
      { "@type": "ListItem", "position": 2, "name": "Documentation", "item": "https://avelyn.software/docs" }
    ]
  };

  return (
    <>
      <SchemaMarkup schema={[docsSchema, breadcrumbSchema]} />

      <div className="space-y-12">
        {/* Hero Banner */}
        <section className="relative p-8 md:p-12 rounded-3xl bg-gradient-to-br from-neutral-900 via-neutral-950 to-[#120B2E] text-white overflow-hidden shadow-xl">
          <div className="absolute top-0 right-0 w-96 h-96 bg-[#7C3AED]/20 blur-[120px] rounded-full pointer-events-none" />
          
          <div className="relative z-10 max-w-3xl space-y-4">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-xs font-semibold text-purple-300">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Version 2.1 Documentation Center</span>
            </div>
            <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight text-white leading-tight">
              Master System-Wide <br />
              <span className="bg-gradient-to-r from-purple-400 via-pink-300 to-purple-200 bg-clip-text text-transparent">
                Privacy-First AI Refinement
              </span>
            </h1>
            <p className="text-neutral-300 text-base md:text-lg leading-relaxed">
              Explore step-by-step installation guides, provider integration manuals, global hotkey shortcuts, and troubleshooting steps for Avelyn.
            </p>

            <div className="pt-4 flex flex-wrap gap-3">
              <Link
                href="/docs/getting-started/installation"
                className="inline-flex items-center px-5 py-2.5 rounded-full bg-[#7C3AED] text-white text-sm font-semibold hover:bg-[#6D28D9] transition-all shadow-md hover:scale-[1.02]"
              >
                Quick Installation Guide
                <ArrowRight className="w-4 h-4 ml-2" />
              </Link>
              <Link
                href="/docs/providers/ollama-integration"
                className="inline-flex items-center px-5 py-2.5 rounded-full bg-white/10 text-white text-sm font-semibold hover:bg-white/20 transition-all border border-white/10"
              >
                Local Ollama Setup
              </Link>
            </div>
          </div>
        </section>

        {/* Documentation Categories Grid */}
        <section className="space-y-10" aria-label="Documentation Categories">
          <div className="border-b border-neutral-200 pb-4">
            <h2 className="text-2xl font-bold text-neutral-900 tracking-tight">Documentation Categories</h2>
            <p className="text-neutral-600 text-sm mt-1">Select a category below to explore topics, configuration steps, and tutorials.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {docCategories.map((cat) => (
              <div
                key={cat.slug}
                id={cat.slug}
                className="rounded-2xl border border-neutral-200/80 bg-white p-6 shadow-sm hover:border-[#7C3AED]/40 hover:shadow-md transition-all flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center space-x-3 mb-3">
                    <div className="p-2.5 rounded-xl bg-purple-50 text-[#7C3AED]">
                      <Sparkles className="w-5 h-5" />
                    </div>
                    <h3 className="text-xl font-bold text-neutral-900">{cat.title}</h3>
                  </div>

                  <ul className="space-y-2 mb-6">
                    {cat.items.map((item) => (
                      <li key={item.slug}>
                        <Link
                          href={`/docs/${cat.slug}/${item.slug}`}
                          className="group flex items-start justify-between p-2 rounded-lg hover:bg-purple-50/50 transition-colors"
                        >
                          <div>
                            <span className="text-sm font-semibold text-neutral-800 group-hover:text-[#7C3AED] transition-colors block">
                              {item.title}
                            </span>
                            {item.description && (
                              <span className="text-xs text-neutral-500 line-clamp-1">{item.description}</span>
                            )}
                          </div>
                          <ArrowRight className="w-4 h-4 text-neutral-400 group-hover:text-[#7C3AED] group-hover:translate-x-1 transition-all mt-1 flex-shrink-0" />
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Popular Docs Quick Access */}
        <section className="p-8 rounded-2xl bg-neutral-50 border border-neutral-200/80 space-y-4">
          <div className="flex items-center space-x-2 text-sm font-bold text-neutral-900 uppercase tracking-wider">
            <CheckCircle className="w-4 h-4 text-[#7C3AED]" />
            <span>Popular Quick Tutorials</span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <Link
              href="/docs/providers/gemini-integration"
              className="p-4 rounded-xl bg-white border border-neutral-200 hover:border-[#7C3AED] transition-all block"
            >
              <span className="text-xs text-purple-600 font-bold block mb-1">AI Providers</span>
              <span className="text-sm font-bold text-neutral-900 block">Connecting Google Gemini Flash</span>
              <span className="text-xs text-neutral-500 mt-1 block">Free API key setup for instant cloud speed.</span>
            </Link>
            <Link
              href="/docs/getting-started/permissions-setup"
              className="p-4 rounded-xl bg-white border border-neutral-200 hover:border-[#7C3AED] transition-all block"
            >
              <span className="text-xs text-purple-600 font-bold block mb-1">macOS Setup</span>
              <span className="text-sm font-bold text-neutral-900 block">Accessibility & Hotkey Permissions</span>
              <span className="text-xs text-neutral-500 mt-1 block">Granting system replacement rights.</span>
            </Link>
            <Link
              href="/docs/troubleshooting/ollama-connection-issues"
              className="p-4 rounded-xl bg-white border border-neutral-200 hover:border-[#7C3AED] transition-all block"
            >
              <span className="text-xs text-purple-600 font-bold block mb-1">Troubleshooting</span>
              <span className="text-sm font-bold text-neutral-900 block">Fixing Ollama 11434 Port Errors</span>
              <span className="text-xs text-neutral-500 mt-1 block">Resolving daemon connection problems.</span>
            </Link>
          </div>
        </section>
      </div>
    </>
  );
}