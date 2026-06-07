import React from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Check, X } from "lucide-react";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Avelyn vs ChatGPT — Private Local ChatGPT Alternative for macOS",
  description: "Compare Avelyn vs ChatGPT. Discover a local, zero-telemetry ChatGPT alternative for macOS that operates entirely offline without subscriptions or token limits.",
  alternates: {
    canonical: "/avelyn-vs-chatgpt",
  },
};

export default function AvelynVsChatGptPage() {
  const comparison = [
    {
      feature: "Data Privacy & Telemetry",
      avelyn: "100% Local. No logs, no telemetry, no data leaves your machine.",
      chatgpt: "Cloud-reliant. Prompts are sent to servers and potentially used for training.",
      avelynCheck: true,
      chatgptCheck: false
    },
    {
      feature: "Offline Capabilities",
      avelyn: "Fully offline. Works on flights, remote areas, and air-gapped systems.",
      chatgpt: "Requires active, fast internet connection. Fails during outages.",
      avelynCheck: true,
      chatgptCheck: false
    },
    {
      feature: "System-wide Integration",
      avelyn: "Native macOS menu bar app. Works in VS Code, Slack, Word, and textareas.",
      chatgpt: "Mainly browser or isolated desktop app. Requires copying text back and forth.",
      avelynCheck: true,
      chatgptCheck: false
    },
    {
      feature: "Subscription & Limits",
      avelyn: "Free. Runs open weights models locally with zero limits or quotas.",
      chatgpt: "Premium tier needed for fast access. Has strict hourly rate limits.",
      avelynCheck: true,
      chatgptCheck: true
    },
    {
      feature: "Custom Prompts",
      avelyn: "Inline custom prompts directly on highlighted text blocks.",
      chatgpt: "Chat-based structure requiring copy, paste, instruction, copy-back.",
      avelynCheck: true,
      chatgptCheck: true
    }
  ];

  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "Why is Avelyn a secure ChatGPT alternative for macOS?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Avelyn operates as a secure ChatGPT alternative because it runs all large language models locally on your Apple Silicon hardware. Unlike ChatGPT, which transmits text selections to OpenAI servers for processing, Avelyn runs entirely offline in a local sandbox with zero cloud telemetry, ensuring your code and drafts never leave your device."
        }
      },
      {
        "@type": "Question",
        "name": "Can I use Avelyn completely offline without an internet connection?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes, Avelyn is 100% functional offline when configured with a local inference engine like Ollama. This makes it an ideal alternative in high-security corporate networks, on flights, or in remote settings where internet access is unavailable or insecure."
        }
      },
      {
        "@type": "Question",
        "name": "Is there a subscription fee to use Avelyn?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "No, Avelyn is completely free and open-source. It utilizes open-weights models running directly on your system, removing the need for monthly API fees, subscription quotas, or token caps."
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
        "name": "Avelyn vs ChatGPT",
        "item": "https://avelyn.software/avelyn-vs-chatgpt"
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
              Avelyn vs ChatGPT: Private ChatGPT Alternative for macOS
            </h1>
            <p className="text-lg font-medium leading-relaxed text-neutral-500 max-w-xl mx-auto">
              Compare the key differences between running lightweight models locally on macOS and routing private texts to cloud servers.
            </p>
          </div>
        </section>

        {/* Content Section (SEO Keyword Expansion) */}
        <section className="py-16 max-w-[1000px] mx-auto px-6 leading-relaxed text-neutral-600 font-medium">
          <div className="space-y-12">
            
            {/* Subsection 1 */}
            <div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
                Why Developers Require a Local ChatGPT Alternative for macOS
              </h2>
              <p className="mb-4">
                For developers, engineers, and financial analysts, copy-pasting data into OpenAI's web interface is a high-risk activity. Corporate IP policies, data protection regulations (such as GDPR or HIPAA), and strict NDA guidelines make cloud storage of highlighted snippets a severe liability. 
              </p>
              <p className="mb-4">
                Avelyn serves as a native, private **ChatGPT alternative for macOS** that directly solves this dilemma. By integrating standard model interfaces with local inference engines, users can highlight active blocks of code, configuration files, or corporate emails and refine them in-place. Because the text never leaves local memory buffers, data leakage risks are completely eliminated.
              </p>
              <p>
                In addition, because cloud models require constant network latency buffers, editing small phrases can take several seconds of network handshakes. Running models on your unified memory architecture reduces these lags to near zero, providing instant re-write updates right inside your active editor view.
              </p>
            </div>

            {/* Subsection 2 */}
            <div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
                Offline Autonomy vs Cloud Server Outages
              </h2>
              <p className="mb-4">
                ChatGPT requires a stable and high-speed internet connection to complete inquiries. In secure localized environments, airplane cabins, or areas with poor cellular coverage, cloud assistants fail completely. Furthermore, during high-demand server outages, OpenAI rates limit free and paid tiers alike.
              </p>
              <p>
                By running models locally via Ollama, the assistant operates 100% offline. It is immune to network dropouts and api gateway overloads. This guarantees that your writing helper remains fully active regardless of your location. Learn how this works on our <a href="/what-is-avelyn" className="text-[#7C3AED] hover:underline font-bold">What is Avelyn page</a> or read about the local setup steps on the <a href="/avelyn-ai" className="text-[#7C3AED] hover:underline font-bold">Avelyn AI guide page</a>.
              </p>
            </div>

            {/* Subsection 3 */}
            <div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
                Complete Data Privacy Audit
              </h2>
              <p className="mb-4">
                Using cloud AI tools means trusting an external vendor with your raw text inputs, drafts, and editing history. These databases are subject to search warrants, data breaches, and model training ingestion rules. 
              </p>
              <p className="mb-4">
                The macOS assistant uses a local sandbox that blocks all outbound socket bindings. It creates no usage logs on cloud servers, contains zero error telemetry trackers, and does not require registration profiles. Your data remains strictly yours. For information on comparing local privacy to other popular assistants, check our <a href="/avelyn-vs-grammarly" className="text-[#7C3AED] hover:underline font-bold">Avelyn vs Grammarly guide</a>.
              </p>
              <p>
                Moreover, because the application is fully open source, the underlying source code can be audited by security departments at any time. Security teams can trace variables, hook points, and clipboard events to ensure that text inputs are processed inside memory enclaves, matching strict regulatory requirements for financial or healthcare processing.
              </p>
            </div>

            {/* Subsection 4 */}
            <div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-neutral-900 tracking-tight mb-4">
                Financial Economics: Local Hardware vs Subscription Quotas
              </h2>
              <p className="mb-4">
                Paid cloud subscriptions typically cost $20 per user monthly, which scales quickly across development teams. They also enforce strict token rate limits or request caps during periods of high platform demand, disrupting developer workflows.
              </p>
              <p className="mb-4">
                Operating local open weights models via a system-wide macOS assistant yields substantial cost savings. Since inference runs entirely on your own Apple Silicon GPU cores, there are no ongoing monthly fees, rate limit quotas, or API costs. You gain a highly responsive, unlimited writing helper for a one-time hardware investment.
              </p>
              <p>
                This local model execution also means that you are not constrained by prompt length limits or model throttling. While cloud services limit context sizes to manage their own cloud hosting costs, your local GPU is only constrained by your system's memory limits. You can refine entire files, parse thousands of lines of logs, or edit lengthy scripts without worrying about subscription tiers, API quotas, or credit usage bills.
              </p>
            </div>

          </div>
        </section>

        {/* Comparison Details */}
        <section className="py-16 md:py-24 max-w-[1000px] mx-auto px-6 border-t border-neutral-100">
          <h2 className="text-3xl font-extrabold text-neutral-900 tracking-tight mb-8 text-center">
            Detailed Comparison Table
          </h2>

          <div className="overflow-x-auto border border-neutral-200/60 rounded-[32px] bg-white shadow-sm mb-16">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-neutral-50 border-b border-neutral-200/60">
                  <th className="p-6 text-sm font-bold text-neutral-900 uppercase tracking-wider">Feature</th>
                  <th className="p-6 text-sm font-bold text-[#7C3AED] uppercase tracking-wider">Avelyn (Local Offline)</th>
                  <th className="p-6 text-sm font-bold text-neutral-500 uppercase tracking-wider">ChatGPT (Cloud AI)</th>
                </tr>
              </thead>
              <tbody>
                {comparison.map((row) => (
                  <tr key={row.feature} className="border-b border-neutral-100 last:border-none hover:bg-neutral-50/50 transition-colors">
                    <td className="p-6 font-bold text-neutral-900 text-sm sm:text-base">{row.feature}</td>
                    <td className="p-6 text-neutral-600 text-xs sm:text-sm font-medium">
                      <div className="flex items-start gap-2">
                        <Check className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                        <span>{row.avelyn}</span>
                      </div>
                    </td>
                    <td className="p-6 text-neutral-400 text-xs sm:text-sm font-medium">
                      <div className="flex items-start gap-2">
                        {row.chatgptCheck ? (
                          <Check className="w-4 h-4 text-neutral-400 shrink-0 mt-0.5" />
                        ) : (
                          <X className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                        )}
                        <span>{row.chatgpt}</span>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="space-y-10">
            <div>
              <h3 className="text-2xl font-bold text-neutral-900 mb-4 tracking-tight">Why Choose Avelyn over ChatGPT?</h3>
              <p className="text-neutral-500 leading-relaxed font-medium">
                ChatGPT is an excellent conversational partner, but it is built as a destination. You have to open a tab, copy your text, paste it, formulate instructions, wait for generation, copy the output, go back to your app, and paste it. Avelyn simplifies this loop down to 3 keystrokes and runs entirely offline on your Mac, keeping your confidential documents completely private.
              </p>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
