import React from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Cpu, Zap, Eye, Terminal } from "lucide-react";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Avelyn AI — macOS Multi-Provider & API Key Integration Guide",
  description: "Optimize your macOS workflow with Avelyn. Integrate local Ollama engines, OpenRouter API keys, and custom endpoints to route and fall back between offline and cloud models.",
  alternates: {
    canonical: "/avelyn-ai",
  },
};

export default function AvelynAiPage() {
  const models = [
    {
      name: "GPT-4o Mini",
      desc: "Fast, extremely cheap, and highly capable cloud model. Ideal for complex reasoning tasks and large document summarizations.",
      category: "Cloud / Reasoning"
    },
    {
      name: "Claude 3.5 Haiku",
      desc: "Anthropic's low-latency model, famous for coding task completions, technical writing, and structural email updates.",
      category: "Cloud / Writing"
    },
    {
      name: "Gemini 2.5 Flash",
      desc: "Google's ultra-low-latency model. Processes system-wide highlight requests in sub-second speeds.",
      category: "Cloud / Speed"
    },
    {
      name: "Gemma 3 (4B / 9B)",
      desc: "Developed by Google, this lightweight model is the default recommendation for local execution. Optimized for speed and quality in writing edits, executing in less than 1.5 seconds.",
      category: "Local / Default"
    },
    {
      name: "Llama 3 (8B)",
      desc: "Meta's highly popular open weights model. Excellent for general structural updates, semantic rephrasing, and creative copy editing.",
      category: "Local / Prose"
    },
    {
      name: "Mistral (7B)",
      desc: "Known for its rich linguistic ability, it serves as a powerful offline model for translation, formatting, and complex structural grammar checks.",
      category: "Local / Grammar"
    }
  ];

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
        "name": "Avelyn AI",
        "item": "https://avelyn.software/avelyn-ai"
      }
    ]
  };

  return (
    <div className="flex-1 flex flex-col min-h-screen bg-white">
      <Navbar />

      <main className="flex-grow pt-32 pb-16">
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
                Local & Cloud Specs
              </span>
            </div>
            <h1 className="text-4xl sm:text-5xl font-extrabold text-neutral-900 tracking-tight leading-tight max-w-3xl mx-auto mb-6">
              Avelyn AI — macOS Multi-Provider & API Key Integration
            </h1>
            <p className="text-lg font-medium leading-relaxed text-neutral-500 max-w-xl mx-auto">
              Run optimized local language models or securely connect to cloud APIs with seamless routing.
            </p>
          </div>
        </section>

        {/* Technical Setup Overview (SEO Keyword Density Expansion) */}
        <section className="py-16 max-w-[1000px] mx-auto px-6 leading-relaxed">
          <div className="space-y-10 text-neutral-600 font-medium text-base sm:text-lg">
            
            {/* Subsection 1 */}
            <div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
                Configuring Your Local Ollama Assistant on macOS
              </h2>
              <p className="mb-4">
                To run Avelyn as a fully integrated **local Ollama assistant**, you need to ensure the Ollama system daemon is running on your machine. Ollama acts as the backend inference pipeline, packaging open-source model weights (like Meta's Llama 3 or Google's Gemma 3) and exposing a local REST API endpoint on your loopback address.
              </p>
              <p className="mb-4">
                Follow these simple steps to initialize your environment:
              </p>
              <ol className="list-decimal pl-6 mb-4 space-y-2">
                <li>
                  Download Ollama for macOS from the official portal and move it to your `/Applications` directory.
                </li>
                <li>
                  Launch your Terminal app and fetch your preferred model. For instance, run: <code className="bg-neutral-100 text-neutral-800 px-1.5 py-0.5 rounded text-sm font-mono">ollama run gemma3:4b</code>.
                </li>
                <li>
                  Confirm the daemon is listening by visiting <code className="bg-neutral-100 text-neutral-800 px-1.5 py-0.5 rounded text-sm font-mono">http://localhost:11434</code> in your browser.
                </li>
                <li>
                  Open the assistant settings window and choose your active model from the local model profiles list.
                </li>
              </ol>
              <p>
                By linking the menu bar assistant to Ollama, you achieve instant, zero-latency text refinements system-wide. Learn more about the core mechanics on our <a href="/about-avelyn" className="text-[#7C3AED] hover:underline font-bold">About Avelyn Page</a> or review common setups on the <a href="/what-is-avelyn" className="text-[#7C3AED] hover:underline font-bold">What is Avelyn FAQ Page</a>.
              </p>
            </div>

            {/* Subsection 2 */}
            <div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
                Integrating Cloud APIs & OpenRouter Keys
              </h2>
              <p className="mb-4">
                If you prefer not to download and compile large model weights locally, or want to access global frontier models, Avelyn supports direct cloud provider integrations. You can connect your custom API keys for <strong>OpenRouter (Avelyn Cloud)</strong> or standard OpenAI-compatible endpoints.
              </p>
              <p className="mb-4">
                To integrate your cloud API keys:
              </p>
              <ol className="list-decimal pl-6 mb-4 space-y-2">
                <li>
                  Open the <strong>Settings</strong> panel and navigate to the <strong>AI Provider</strong> tab.
                </li>
                <li>
                  Select the <strong>Single Provider</strong> mode or configure overrides inside the <strong>Smart Router</strong>.
                </li>
                <li>
                  Under **Avelyn Cloud**, paste your OpenRouter API Key (prefixed with <code className="bg-neutral-100 text-neutral-800 px-1.5 py-0.5 rounded text-sm font-mono">sk-or-v1-...</code>). Your key will be permanently masked with password bullet points (<code className="bg-neutral-100 text-neutral-800 px-1.5 py-0.5 rounded text-sm font-mono">••••••••</code>) for strict UI privacy.
                </li>
                <li>
                  Choose a model from the list of options, such as <code className="bg-neutral-100 text-neutral-800 px-1.5 py-0.5 rounded text-sm font-mono">openai/gpt-4o-mini</code> or <code className="bg-neutral-100 text-neutral-800 px-1.5 py-0.5 rounded text-sm font-mono">google/gemini-2.5-flash</code>.
                </li>
                <li>
                  To connect custom local endpoints (like LM Studio or vLLM) or raw OpenAI servers, choose the <strong>Custom API</strong> provider option and fill in your base URL, API Key, and target model ID.
                </li>
              </ol>
              <p>
                API keys are stored strictly in local configuration files. Avelyn does not route keys through third-party servers, ensuring complete telemetry privacy.
              </p>
            </div>

            {/* Subsection 3 */}
            <div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
                Apple Silicon Benchmark Logs & Generation Speed
              </h2>
              <p className="mb-4">
                Performance scales directly with your chip's memory bandwidth. Because Apple M-series chips use unified memory, local inference does not suffer from CPU-to-GPU memory transfer overheads. A 4B parameter model like Gemma 3 Warm-boots instantly and generates tokens at speeds exceeding 70 tokens per second.
              </p>
              <p className="mb-4">
                Here is a breakdown of average generation speeds across hardware setups:
              </p>
              <ul className="list-disc pl-6 mb-4 space-y-2">
                <li>
                  <strong>Apple M4 Pro (Unified Memory)</strong>: Gemma 3 (4B) &rarr; ~85 tokens/sec. Llama 3 (8B) &rarr; ~52 tokens/sec.
                </li>
                <li>
                  <strong>Apple M2 Max (Unified Memory)</strong>: Gemma 3 (4B) &rarr; ~68 tokens/sec. Llama 3 (8B) &rarr; ~42 tokens/sec.
                </li>
                <li>
                  <strong>Apple M1 (Standard 8GB)</strong>: Gemma 3 (4B) &rarr; ~35 tokens/sec. Llama 3 (8B) &rarr; ~20 tokens/sec.
                </li>
              </ul>
              <p>
                This hardware-level efficiency matches or exceeds cloud generation latency, without routing text blocks over the internet. Read our comparison write-ups: <a href="/avelyn-vs-chatgpt" className="text-[#7C3AED] hover:underline font-bold">Avelyn vs ChatGPT</a> and <a href="/avelyn-vs-grammarly" className="text-[#7C3AED] hover:underline font-bold">Avelyn vs Grammarly</a>.
              </p>
            </div>

            {/* Subsection 4 */}
            <div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
                Custom System Prompts & Context Length Optimization
              </h2>
              <p className="mb-4">
                The assistant allows you to write custom instructions to adjust the editor's behavior. By passing system prompts, you can instruct the local model to write in specific styles (e.g. academic, professional email, clean markdown format, or translation).
              </p>
              <p className="mb-4">
                To avoid slowing down local performance, we recommend setting a modest context window of 2,048 or 4,096 tokens inside the system settings panel. This allocates sufficient memory for system-wide highlight rewrites without exhausting system RAM or causing chip thermal throttling.
              </p>
              <p>
                Additionally, you can define target formatting instructions (such as "keep formatting exactly intact" or "output raw code block syntax only") in the prompt template. The system parses these instructions alongside user selection, formatting outputs instantly without adding unnecessary tokens to the generation path.
              </p>
            </div>

            {/* Subsection 5 */}
            <div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
                Troubleshooting & GPU Layer Allocation Limits
              </h2>
              <p className="mb-4">
                When running the assistant alongside resource-intensive software like video editors or compiling large projects, memory pressure can force the OS to page local model weights out of GPU memory. This shifts inference back to the CPU, increasing latency.
              </p>
              <p>
                To resolve this, users can set custom parameters in the settings panel to lock model parameters in physical RAM (using `mlock`). We also recommend adjusting the GPU thread layer allocation count in Ollama's configuration file to reserve 2GB of unified VRAM for OS system processes, maintaining smooth generation speeds even under heavy CPU loads.
              </p>
            </div>

          </div>
        </section>

        {/* Specs Bento Grid */}
        <section className="py-16 md:py-24 max-w-[1200px] mx-auto px-6 border-t border-neutral-100">
          <h2 className="text-3xl font-extrabold text-neutral-900 tracking-tight mb-12 text-center">
            Local Processing Engine Capabilities
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-20">
            <div className="bg-[#F5F5F7] rounded-[32px] p-8 border border-neutral-200/40 flex gap-6">
              <Cpu className="w-12 h-12 text-[#7C3AED] shrink-0" />
              <div>
                <h3 className="text-xl font-bold text-neutral-900 mb-2">Apple Silicon Optimization</h3>
                <p className="text-neutral-500 leading-relaxed text-sm sm:text-base">
                  Avelyn utilizes the shared unified memory architectures of Apple M1, M2, M3, and M4 chips to execute LLM inferences without GPU/CPU context switches, giving you blazing-fast speed.
                </p>
              </div>
            </div>

            <div className="bg-[#F5F5F7] rounded-[32px] p-8 border border-neutral-200/40 flex gap-6">
              <Zap className="w-12 h-12 text-[#7C3AED] shrink-0" />
              <div>
                <h3 className="text-xl font-bold text-neutral-900 mb-2">Sub-Second Prefills & Token Streaming</h3>
                <p className="text-neutral-500 leading-relaxed text-sm sm:text-base">
                  By using dynamic loading and caching strategies, local model warming is executed in the background. The rewritten text streams back token-by-token directly inside a minimalist window.
                </p>
              </div>
            </div>

            <div className="bg-[#F5F5F7] rounded-[32px] p-8 border border-neutral-200/40 flex gap-6">
              <Eye className="w-12 h-12 text-[#7C3AED] shrink-0" />
              <div>
                <h3 className="text-xl font-bold text-neutral-900 mb-2">Zero Network Latency & Dependability</h3>
                <p className="text-neutral-500 leading-relaxed text-sm sm:text-base">
                  No api key quotas, no rate limits, and no server crashes. Avelyn works identical in remote mountain cabins, on flights, or in high-security corporate local areas.
                </p>
              </div>
            </div>

            <div className="bg-[#F5F5F7] rounded-[32px] p-8 border border-neutral-200/40 flex gap-6">
              <Terminal className="w-12 h-12 text-[#7C3AED] shrink-0" />
              <div>
                <h3 className="text-xl font-bold text-neutral-900 mb-2">Full Custom Model Support</h3>
                <p className="text-neutral-500 leading-relaxed text-sm sm:text-base">
                  Avelyn talks to Ollama via standard local ports. You can change your active model to any custom fine-tuned model (e.g. customized coding helpers) inside the UI panel.
                </p>
              </div>
            </div>
          </div>

          {/* Model Table */}
          <div className="max-w-[900px] mx-auto bg-white border border-neutral-200/60 rounded-[32px] p-8 shadow-sm">
            <h3 className="text-2xl font-bold text-neutral-900 mb-6 tracking-tight">Supported Offline & Cloud Model Profiles</h3>
            <div className="space-y-6">
              {models.map((model) => (
                <div key={model.name} className="flex flex-col sm:flex-row justify-between border-b border-neutral-100 pb-6 last:border-none last:pb-0">
                  <div className="max-w-md">
                    <h4 className="text-lg font-bold text-neutral-900 mb-1">{model.name}</h4>
                    <p className="text-neutral-500 text-sm leading-relaxed">{model.desc}</p>
                  </div>
                  <div className="mt-2 sm:mt-0">
                    <span className="inline-block px-3 py-1 bg-[#EDE9FE] text-[#7C3AED] font-semibold text-xs rounded-full">
                      {model.category}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
