import React from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "What is Avelyn? Features, Safety, and Offline AI Capabilities",
  description: "Frequently Asked Questions about Avelyn — the system-wide offline AI assistant for macOS. Get answers on data safety, model support, and local sandboxing.",
  alternates: {
    canonical: "/what-is-avelyn",
  },
};

export default function WhatIsAvelynPage() {
  const faqs = [
    {
      q: "What is Avelyn?",
      a: "Avelyn is a privacy-first, local offline AI writing assistant specifically designed for macOS. It integrates system-wide, allowing you to highlight text in any application (like Chrome, Slack, Word, or VS Code), hit a customizable global keyboard shortcut, and refine or rewrite your prose instantly using local AI models."
    },
    {
      q: "Is the application safe to use?",
      a: "Yes, this utility is highly secure. Unlike traditional cloud writing assistants that stream your highlighted inputs to remote servers, the tool operates entirely within a local sandbox on your machine. It only captures your highlighted text when the hotkey is pressed, processes it strictly in local memory, and updates your clipboard with zero external network request logging or telemetry."
    },
    {
      q: "Is it completely offline?",
      a: "Yes. When configured with local offline servers like Ollama, the assistant operates 100% offline. No active internet connection is required to rewrite, format, translate, or proofread your text, making it ideal for air-gapped workstations or sensitive corporate environments."
    },
    {
      q: "Does the macOS assistant use Ollama?",
      a: "The tool defaults to Ollama for local offline LLM model execution. This allows you to host and run open-weights models like Llama 3, Mistral, and Gemma 3 on your Apple Silicon CPU or GPU. Alternatively, if you prefer not to host binaries locally, you can configure cloud API connections inside the Settings panel."
    },
    {
      q: "How does the offline AI assistant function system-wide?",
      a: "The utility uses standard macOS accessibility APIs to copy highlighted text when the global shortcut (Ctrl+Shift+E) is pressed. It displays a minimalist command palette next to your cursor, takes your selected rewrite instruction (Smart Assist, Fix Grammar, or custom prompt), processes the text via local Ollama inference, and pastes the result directly back in place."
    },
    {
      q: "Why is the system different from cloud alternatives?",
      a: "The system is different because it is built from the ground up for zero cloud dependency and complete data sovereignty. Unlike cloud assistants that transmit your keystrokes to third-party databases, this utility runs open LLMs natively on your Apple Silicon hardware, executes edits in-place inside a local sandbox, requires no subscriptions, and functions completely offline."
    },
    {
      q: "What macOS versions are supported?",
      a: "The software supports macOS 13 (Ventura), macOS 14 (Sonoma), and macOS 15 (Sequoia) or newer. It is optimized to run on both Intel-based Macs and Apple Silicon machines (M1, M2, M3, M4 series), though Apple Silicon is highly recommended for faster token generation and lower memory latency during local LLM model execution."
    },
    {
      q: "Can I run fine-tuned or custom model files?",
      a: "Yes. Because the utility integrates directly with Ollama's local api server, you can load any custom Modelfile inside your local library. Once registered in Ollama, your custom fine-tuned model profile will automatically appear in the assistant's model dropdown list."
    },
    {
      q: "Is there any background network tracking?",
      a: "Absolutely not. The application code is built with zero telemetry dependencies. It does not contain analytic tracking scripts, error reporting mechanisms that connect to external endpoints, or remote config fetching. Your texts, keyboard actions, and logs remain strictly on your local SSD."
    }
  ];

  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": faqs.map(faq => ({
      "@type": "Question",
      "name": faq.q,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": faq.a
      }
    }))
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
        "name": "What is Avelyn?",
        "item": "https://avelyn.software/what-is-avelyn"
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

        {/* Hero Area */}
        <section className="relative overflow-hidden bg-[#FAFAFA] py-16 border-b border-neutral-100">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-[800px] h-[300px] bg-[#7C3AED]/5 blur-[100px] rounded-full pointer-events-none" />
          
          <div className="mx-auto max-w-[1200px] px-6 text-center">
            <h1 className="text-4xl sm:text-5xl font-extrabold text-neutral-900 tracking-tight leading-tight mb-4">
              What is Avelyn?
            </h1>
            <p className="text-lg font-medium leading-relaxed text-neutral-500 max-w-xl mx-auto">
              Everything you need to know about the local offline AI assistant: privacy, capabilities, and integrations.
            </p>
          </div>
        </section>

        {/* FAQ/Q&A Body */}
        <section className="py-16 md:py-24 max-w-[840px] mx-auto px-6">
          <div className="space-y-12">
            {faqs.map((faq, idx) => (
              <div key={idx} className="border-b border-neutral-100 pb-10 last:border-none">
                <h2 className="text-2xl font-bold text-neutral-900 mb-4 tracking-tight flex items-start gap-3">
                  <span className="text-[#7C3AED] font-mono">Q.</span>
                  {faq.q}
                </h2>
                <div className="flex gap-3 pl-8 text-neutral-500 font-medium leading-relaxed text-base sm:text-lg">
                  <p>{faq.a}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Security Deep Dive Section (Added for length and SEO authority) */}
        <section className="py-16 max-w-[840px] mx-auto px-6 border-t border-neutral-100 leading-relaxed">
          <h2 className="text-3xl font-extrabold text-neutral-900 tracking-tight mb-6">
            Detailed Security Architecture Overview
          </h2>
          <div className="space-y-6 text-neutral-500 font-medium text-base sm:text-lg">
            <p>
              To fully establish trust, the application uses local macOS sandboxing rules that restrict standard network bindings. Unlike typical macOS writing assistants that maintain active HTTP connections to send text packets to remote cloud queues, this utility enforces static isolation.
            </p>
            <p>
              When a user triggers the global shortcut command palette, the local memory buffer is temporarily filled with the copied text selection. The text block is analyzed locally, processed using CPU or GPU acceleration, and pasted back. The clipboard cache is immediately cleared, preventing data leakage across applications.
            </p>
            <p>
              Additionally, our offline AI assistant on macOS utilizes advanced OS level security permissions. The utility requires Accessibility permissions solely to communicate with open editors via standard UI scripting interfaces. It does not monitor keyboard interrupts in the background when inactive, meaning it never functions as a keylogger. This is a critical distinction for anyone comparing privacy-focused tools to cloud alternatives.
            </p>
            <p>
              The architecture is also fully compatible with corporate VPNs, firewall rules, and air-gapped systems. Since all network requests are blocked by the system-level sandbox, security operations center (SOC) analysts can verify that no outbound traffic packets are generated during editing. This allows immediate onboarding in financial institutes, medical software editing desks, and aerospace development firms.
            </p>
            <p>
              By decoupling local rewriting from the cloud, users can confidently edit proprietary source code, internal spreadsheets, and confidential emails without violating company compliance frameworks or security protocols. To see how this compares to cloud alternatives, view our detailed comparison guides:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-[#7C3AED] font-bold">
              <li>
                Explore the <a href="/avelyn-vs-chatgpt" className="hover:underline">Avelyn vs ChatGPT: Local ChatGPT Alternative Guide</a>.
              </li>
              <li>
                Explore the <a href="/avelyn-vs-grammarly" className="hover:underline">Avelyn vs Grammarly: Privacy-First Grammarly Alternative Guide</a>.
              </li>
              <li>
                Learn about native optimizations in the <a href="/about-avelyn" className="hover:underline">About Avelyn Philosophy Page</a> or review model integrations in the <a href="/avelyn-ai" className="hover:underline">Avelyn AI Integration Page</a>.
              </li>
            </ul>
          </div>
        </section>

        {/* Local AI Callout */}
        <section className="mx-auto max-w-[800px] px-6 text-center py-12 bg-neutral-50 rounded-[32px] border border-neutral-200/50 my-12">
          <h2 className="text-2xl font-extrabold text-neutral-900 tracking-tight mb-4">
            Ready to enhance your writing locally?
          </h2>
          <p className="text-neutral-500 text-sm sm:text-base font-medium mb-8 max-w-lg mx-auto">
            Get started with this privacy-first assistant for macOS and run Llama 3 or Gemma 3 offline today.
          </p>
          <a
            href="/#beta"
            className="inline-flex items-center gap-2 rounded-full bg-[#0E0E11] px-6 py-3.5 text-sm font-semibold text-white shadow-md hover:bg-neutral-800 transition-all"
          >
            Apply for Beta Access
          </a>
        </section>
      </main>

      <Footer />
    </div>
  );
}
