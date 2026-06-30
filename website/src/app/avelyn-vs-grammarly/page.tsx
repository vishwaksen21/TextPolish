import React from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import InteractiveComparison from "@/components/InteractiveComparison";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Avelyn vs Grammarly — Offline Grammarly Alternative for Privacy",
  description: "Compare Avelyn vs Grammarly. Learn why Avelyn is the leading Grammarly alternative for privacy, operating system-wide on macOS with local models and zero keylogging.",
  alternates: {
    canonical: "/avelyn-vs-grammarly",
  },
};

export default function AvelynVsGrammarlyPage() {

  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "Why is Avelyn an optimal Grammarly alternative for privacy?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Avelyn functions as a secure Grammarly alternative for privacy because it processes all text re-writes locally on your macOS hardware. Unlike Grammarly, which acts as a background cloud logger sending key inputs to external databases, Avelyn runs 100% offline using Ollama, preventing data scanning."
        }
      },
      {
        "@type": "Question",
        "name": "Does Avelyn monitor my keyboard in the background?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "No. Avelyn is only active when you highlight text and explicitly press the custom global hotkey. It does not monitor, index, or record background keystrokes, ensuring absolute privacy for system-wide document editing."
        }
      },
      {
        "@type": "Question",
        "name": "Can Avelyn edit code and markdown files?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes. While Grammarly is restricted to simple prose and grammar templates, Avelyn supports open weights models like Llama 3 and CodeGemma. This lets you execute custom prompts to translate code, format markdown tables, or debug scripts system-wide."
        }
      }
    ]
  };

  const breadcrumbJsonLd = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": "https://avelyn.software"
      },
      {
        "@type": "ListItem",
        "position": 2,
        "name": "Avelyn vs Grammarly",
        "item": "https://avelyn.software/avelyn-vs-grammarly"
      }
    ]
  };

  return (
    <div className="flex-1 flex flex-col min-h-screen bg-white">
      <Navbar />

      <main className="flex-grow pt-32 pb-16">
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbJsonLd) }}
        />

        {/* Header Hero */}
        <section className="relative overflow-hidden bg-[#FAFAFA] py-16 border-b border-neutral-100">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-[800px] h-[300px] bg-[#7C3AED]/5 blur-[100px] rounded-full pointer-events-none" />
          
          <div className="mx-auto max-w-[1200px] px-6 text-center">
            <div className="inline-flex items-center gap-2 rounded-full bg-white border border-[#7C3AED]/20 px-3 py-1 mb-6 shadow-sm">
              <span className="text-[10px] font-bold text-[#7C3AED] uppercase tracking-widest">
                Product Comparisons
              </span>
            </div>
            <h1 className="text-4xl sm:text-5xl font-extrabold text-neutral-900 tracking-tight leading-tight max-w-3xl mx-auto mb-6">
              Avelyn vs Grammarly: Offline Grammarly Alternative for Privacy
            </h1>
            <p className="text-lg font-medium leading-relaxed text-neutral-500 max-w-xl mx-auto">
              Discover why thousands of developers and professionals prefer local AI rewriting models over cloud proofreaders that read all document drafts.
            </p>
          </div>
        </section>

        {/* Content Section (SEO Keyword Expansion) */}
        <section className="py-16 max-w-[1000px] mx-auto px-6 leading-relaxed text-neutral-600 font-medium">
          <div className="space-y-12">
            
            {/* Subsection 1 */}
            <div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
                The Security Risks of Real-Time Cloud Proofreaders
              </h2>
              <p className="mb-4">
                Cloud-based grammar checkers function as continuous keyloggers. They hook into your browser viewports and desktop active panels, sending every typed sentence to remote servers. This introduces a major security risk for software developers handling trade secrets, medical professionals editing patient logs under HIPAA compliance, and legal teams drafting confidential briefs.
              </p>
              <p className="mb-4">
                Avelyn solves this privacy vulnerability by providing a 100% offline **Grammarly alternative privacy** utility for macOS. It does not monitor your typing in the background. It remains dormant until you highlight text and press your shortcut trigger, keeping your intellectual property safe.
              </p>
              <p>
                This zero-keylogging design protects sensitive databases, client details, and credentials. Unlike cloud checkers that catalog typing speed, style, and vocabulary in background logs, Avelyn processes raw text on-demand within local sandbox memory structures, which is fully compliant with enterprise security standards.
              </p>
            </div>

            {/* Subsection 2 */}
            <div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
                System-wide Integration vs Floating Widget Bloatware
              </h2>
              <p className="mb-4">
                Grammarly relies on invasive browser extensions and floating desktop widgets. These overlays block code editors, clutter your screen, and introduce rendering lag. 
              </p>
              <p>
                This local editor features a clean menu bar design that stays completely out of the way. Triggered via custom shortcuts, it displays a command palette that matches your system. Once your command is selected, the assistant updates your text directly. Learn how this works on our <a href="/what-is-avelyn" className="text-[#7C3AED] hover:underline font-bold">What is Avelyn page</a> or read about the local setup steps on the <a href="/avelyn-ai" className="text-[#7C3AED] hover:underline font-bold">Avelyn AI page</a>.
              </p>
            </div>

            {/* Subsection 3 */}
            <div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
                Compliance-Ready Local Models
              </h2>
              <p className="mb-4">
                Because this assistant runs locally without remote database logs, it fits easily into strict security policies. By running open models on your unified memory, you can proofread, translate, and reformat code completely offline.
              </p>
              <p className="mb-4">
                For comparisons with other popular AI assistants, check the <a href="/avelyn-vs-chatgpt" className="text-[#7C3AED] hover:underline font-bold">Avelyn vs ChatGPT guide</a> or read our product philosophy in the <a href="/about-avelyn" className="text-[#7C3AED] hover:underline font-bold">About Avelyn page</a>.
              </p>
              <p>
                This compliance-first design allows engineering teams to refine code blocks or check documentation without triggering security alarms. Many financial groups block cloud keyloggers, but approve sandboxed local workflows since they pose zero outbound risk.
              </p>
            </div>

            {/* Subsection 4 */}
            <div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
                Flexible System Prompts vs Fixed Grammar Rules
              </h2>
              <p className="mb-4">
                Traditional cloud tools are confined to checking grammar patterns, correcting syntax, or adjusting tone based on hardcoded structures. You cannot easily ask them to convert an paragraph into a Markdown table, rewrite a paragraph in JSON, or explain a complex coding algorithm.
              </p>
              <p className="mb-4">
                By using local LLM inference engines, the menu bar assistant allows you to run any prompt you write. You can write custom rewrite templates to translate text into foreign languages, format logs, draft replies, or outline complex concepts. You gain a versatile writing tool, rather than a simple grammar checker.
              </p>
              <p>
                This level of customization makes local offline assistants particularly useful for developers and technical writers. Rather than simply highlighting misspelled words, you can highlight a block of code and ask the assistant to write a docstring, refactor variable names, or outline system behavior in clear markdown. A cloud checker would flag these programming syntax structures as grammar errors, whereas a local language model interprets and adapts to your technical context perfectly. This powerful local capability ensures that your writing workflow remains highly flexible, extremely private, and entirely adapted to modern engineering and development patterns.
              </p>
            </div>

          </div>
        </section>

        {/* Comparison Details */}
        <section className="py-16 md:py-24 max-w-[1000px] mx-auto px-6 border-t border-neutral-100">
          <h2 className="text-3xl font-extrabold text-neutral-900 tracking-tight mb-8 text-center">
            Detailed Comparison Table
          </h2>

          <InteractiveComparison competitor="Grammarly" />

          <div className="space-y-10 mt-12">
            <div>
              <h3 className="text-2xl font-bold text-neutral-900 mb-4 tracking-tight">The Core Difference: Local Privacy & Flexibility</h3>
              <p className="text-neutral-500 leading-relaxed font-medium">
                Cloud-based proofreading assistants monitor every keystroke in the background, raising concerns for organizations handling proprietary code, corporate strategies, or sensitive user data. Avelyn runs of its language model processing locally and offline by default using Ollama, offering complete data privacy. Additionally, you are not locked into standard grammar checks; you can customize prompts on the fly to write professional emails, summarize articles, format markdown tables, or explain complex scripts, with the option to leverage secure cloud providers when extra reasoning power is required.
              </p>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
