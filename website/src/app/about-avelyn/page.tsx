import React from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Shield, Sparkles, Cpu, Award, Lock, EyeOff, Code, FileText } from "lucide-react";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About Avelyn — Privacy-First Local LLM Writing Assistant",
  description: "Learn the philosophy and architecture behind Avelyn. Discover how our system-wide local LLM writing assistant leverages Apple Silicon and Ollama for secure, offline text edits.",
  alternates: {
    canonical: "/about-avelyn",
  },
};

export default function AboutPage() {
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
        "name": "About Avelyn",
        "item": "https://avelyn.software/about-avelyn"
      }
    ]
  };

  return (
    <div className="flex-1 flex flex-col min-h-screen bg-white">
      <Navbar />

      <main className="flex-grow pt-32 pb-16 md:pb-24">
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbJsonLd) }}
        />

        {/* Hero Section */}
        <section className="relative overflow-hidden bg-[#FAFAFA] py-16 md:py-20 border-b border-neutral-100">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-[800px] h-[400px] bg-[#7C3AED]/5 blur-[100px] rounded-full pointer-events-none" />
          
          <div className="mx-auto max-w-[1200px] px-6 text-center">
            <div className="inline-flex items-center gap-2 rounded-full bg-white border border-[#7C3AED]/20 px-3 py-1 mb-6 shadow-sm">
              <span className="text-[10px] font-bold text-[#7C3AED] uppercase tracking-widest">
                Our Story & Philosophy
              </span>
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-neutral-900 tracking-tight leading-tight max-w-4xl mx-auto mb-6">
              About Avelyn — Privacy-First <br className="hidden sm:block" />
              Local LLM Writing Assistant
            </h1>
            <p className="text-lg sm:text-xl font-medium leading-relaxed text-neutral-500 max-w-2xl mx-auto">
              Avelyn was built to bridge the gap between powerful generative AI capabilities and absolute data sovereignty. We believe your thoughts belong to you.
            </p>
          </div>
        </section>

        {/* Brand Strategy / Detailed Story */}
        <section className="py-16 md:py-24 max-w-[1000px] mx-auto px-6 leading-relaxed">
          <div className="space-y-12 text-neutral-600 font-medium text-base sm:text-lg">
            
            {/* Section 1 */}
            <div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
                The Privacy Crisis in Modern Writing Utilities
              </h2>
              <p className="mb-4">
                Almost every mainstream writing assistant runs on centralized cloud models. This means every email draft, code snippet, sensitive project note, and password you highlight is sent across the internet, stored in external databases, and used to train future model parameters. In corporate environments, research laboratories, and personal contexts, this data pipeline presents an unacceptable liability.
              </p>
              <p className="mb-4">
                As organizations enforce strict policies against data leakage, professionals are forced to choose between efficiency and security. Avelyn is engineered as a zero-telemetry alternative. It acts as a dedicated **local LLM writing assistant** that operates system-wide, processing your information entirely within a local sandbox on your machine.
              </p>
              <p>
                Moreover, the bandwidth costs, subscription limitations, and availability bottlenecks of cloud APIs interfere with smooth, native editing pipelines. Security departments often block cloud endpoints, but a sandboxed local tool that handles data solely in system RAM is fully compliant with enterprise security standards.
              </p>
            </div>

            {/* Section 2 */}
            <div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
                Under the Hood: The Local Sandboxed Architecture
              </h2>
              <p className="mb-4">
                Avelyn integrates with native macOS accessibility APIs to intercept highlighted text only when a user triggers the global shortcut (Ctrl+Shift+E). Once activated, the app captures the selection, loads it into local memory, and presents a minimalist command palette right at the cursor position. 
              </p>
              <p className="mb-4">
                Unlike cloud-based tools that stream files to third-party endpoints, Avelyn routes the text directly to a local inference engine running on the host. By utilizing local ports connected to models hosted on your system, it guarantees that no information is sent to external servers. To understand the detailed mechanics, read our answers to common questions in the <a href="/what-is-avelyn" className="text-[#7C3AED] hover:underline font-bold">What is Avelyn FAQ guide</a>.
              </p>
              <p>
                Once inference completes, Avelyn replaces the selection in place. The entire workflow is transparent, lightning-fast, and relies on zero cloud processing.
              </p>
            </div>

            {/* Section 3 */}
            <div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
                Apple Silicon Native Hardware Acceleration
              </h2>
              <p className="mb-4">
                Running LLMs locally has historically been slow and resource-heavy. Avelyn solves this by optimizing compilation for Apple Silicon Unified Memory Architecture (M1, M2, M3, M4 chips). It leverages the Apple Neural Engine and GPU cores to perform prompt processing and token streaming with sub-second latency.
              </p>
              <p className="mb-4">
                By maintaining dynamic model warming in the background, Avelyn ensures that highlighting a block and asking for a rewrite executes in under 1.5 seconds. For details on benchmarking configurations and model specifications, check out the <a href="/avelyn-ai" className="text-[#7C3AED] hover:underline font-bold">Avelyn AI technical guide</a>.
              </p>
            </div>

            {/* Section 4 */}
            <div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
                Strategic Comparisons: How We Stack Up
              </h2>
              <p className="mb-4">
                When compared to cloud alternatives, Avelyn offers a completely different paradigm. Traditional systems operate as destinations, requiring constant copy-pasting and subscriptions. Avelyn runs 100% offline, for free, with unlimited context inputs.
              </p>
              <p>
                To see detailed head-to-head comparisons against mainstream solutions, explore our dedicated research pages:
              </p>
              <ul className="list-disc pl-6 mt-4 space-y-2 text-[#7C3AED] font-bold">
                <li>
                  <a href="/avelyn-vs-chatgpt" className="hover:underline">Avelyn vs ChatGPT: Cloud AI vs Local Privacy Comparison</a>
                </li>
                <li>
                  <a href="/avelyn-vs-grammarly" className="hover:underline">Avelyn vs Grammarly: Keyboard Tracking vs Local Sandbox Proofreading</a>
                </li>
              </ul>
            </div>

            {/* Section 5 */}
            <div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
                Advanced Local Sandbox Architecture Details
              </h2>
              <p className="mb-4">
                Operating inside a local sandbox requires compliance with macOS App Sandbox security rules. The assistant maintains absolute boundary isolation. It does not write temporary files containing highlighted text selections to disk, avoiding data leaks. The temporary text buffer is loaded purely in system RAM. Once the rewrite instruction executes and the output is pasted back, the system memory block is immediately zeroed out.
              </p>
              <p>
                This standard of sandboxing prevents other applications from intercepting the clipboard data or reading the text buffer during LLM processing. This matches the security standard required by enterprises handling classified documentation or proprietary source code.
              </p>
            </div>

            {/* Section 6 */}
            <div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
                A Community-Driven Open Source Core
              </h2>
              <p className="mb-4">
                Our repository is publicly hosted, encouraging peer review, contributions, and community audits. Developers can review the accessibility hooks, shortcut bindings, and local api wrappers to verify that no network requests are sent.
              </p>
              <p>
                In addition to security, an open ecosystem fosters model diversity. As developers build specialized coding helpers or creative writing weights, they can plug them directly into the assistant. This community approach ensures the product remains adaptable to future breakthroughs in language modeling.
              </p>
            </div>

          </div>
        </section>

        {/* Pillars Grid */}
        <section className="py-16 md:py-20 max-w-[1200px] mx-auto px-6 border-t border-neutral-100">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="bg-[#F5F5F7] rounded-[24px] p-6 border border-neutral-200/40">
              <Shield className="w-8 h-8 text-[#7C3AED] mb-4" />
              <h3 className="text-lg font-bold text-neutral-900 mb-2">Zero Cloud Logging</h3>
              <p className="text-neutral-500 text-sm leading-relaxed">
                Your texts never touch cloud gateways, external servers, or proxy log databases.
              </p>
            </div>

            <div className="bg-[#F5F5F7] rounded-[24px] p-6 border border-neutral-200/40">
              <Cpu className="w-8 h-8 text-[#7C3AED] mb-4" />
              <h3 className="text-lg font-bold text-neutral-900 mb-2">Silicon Acceleration</h3>
              <p className="text-neutral-500 text-sm leading-relaxed">
                Optimized for Apple M-series chips, ensuring sub-second inference speeds.
              </p>
            </div>

            <div className="bg-[#F5F5F7] rounded-[24px] p-6 border border-neutral-200/40">
              <Lock className="w-8 h-8 text-[#7C3AED] mb-4" />
              <h3 className="text-lg font-bold text-neutral-900 mb-2">Private Sandbox</h3>
              <p className="text-neutral-500 text-sm leading-relaxed">
                Runs locally on your device within a secured macOS sandbox, protecting code and documentation.
              </p>
            </div>

            <div className="bg-[#F5F5F7] rounded-[24px] p-6 border border-neutral-200/40">
              <Award className="w-8 h-8 text-[#7C3AED] mb-4" />
              <h3 className="text-lg font-bold text-neutral-900 mb-2">Open Weights Models</h3>
              <p className="text-neutral-500 text-sm leading-relaxed">
                Supports Gemma 3, Llama 3, Mistral, and custom fine-tuned weights via Ollama.
              </p>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="mx-auto max-w-[800px] px-6 text-center py-12 bg-neutral-50 rounded-[32px] border border-neutral-200/50 mt-12">
          <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
            Experience Local Offline Writing Assistance
          </h2>
          <p className="text-neutral-500 text-base font-medium mb-8 max-w-lg mx-auto">
            Take part in our private beta program and run your macOS writing workflows with complete digital sovereignty.
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
