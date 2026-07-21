"use client";

import React, { useState } from "react";
import { Check, X, Shield, Cpu, CreditCard, Clock, Calculator } from "lucide-react";

interface ComparisonItem {
  category: "privacy" | "workflow" | "cost";
  feature: string;
  avelyn: string;
  competitorText: string;
  avelynCheck: boolean;
  competitorCheck: boolean;
}

interface InteractiveComparisonProps {
  competitor?: "ChatGPT" | "Grammarly" | "Gemini" | "Claude" | "Copilot" | "Notion AI";
}

export default function InteractiveComparison({ competitor = "ChatGPT" }: InteractiveComparisonProps) {
  const [activeTab, setActiveTab] = useState<"all" | "privacy" | "workflow" | "cost">("all");
  const [teamSize, setTeamSize] = useState(5);
  const [editsPerDay, setEditsPerDay] = useState(15);

  const getComparisonData = (): ComparisonItem[] => {
    if (competitor === "Grammarly") {
      return [
        {
          category: "privacy",
          feature: "Data Privacy & Keylogging",
          avelyn: "Privacy-First. Local by default. Cloud API keys are masked in the UI & stored strictly on device. Zero telemetry.",
          competitorText: "Cloud-reliant. Monitored active key inputs sent to remote servers.",
          avelynCheck: true,
          competitorCheck: false,
        },
        {
          category: "privacy",
          feature: "Proprietary Data Handling",
          avelyn: "Perfect. Operates system-wide on Mac with offline memory buffers. Zero external logging.",
          competitorText: "High risk. Corporate IP and drafts analyzed on third-party clouds.",
          avelynCheck: true,
          competitorCheck: false,
        },
        {
          category: "workflow",
          feature: "Multi-Provider Smart Routing",
          avelyn: "Dynamic. Intelligently routes tasks between Local Ollama and Cloud APIs with smart fallbacks.",
          competitorText: "None. Locked into Grammarly's proprietary cloud models.",
          avelynCheck: true,
          competitorCheck: false,
        },
        {
          category: "workflow",
          feature: "Custom Prompts & Rewrites",
          avelyn: "Execute any custom AI prompt directly on highlighted text selections.",
          competitorText: "Confined to static style recommendations and template tones.",
          avelynCheck: true,
          competitorCheck: false,
        },
        {
          category: "workflow",
          feature: "Offline Compatibility",
          avelyn: "Fully offline via Local Ollama. Works on flights and secure air-gapped zones.",
          competitorText: "Requires active connection. Fails during outages or offline.",
          avelynCheck: true,
          competitorCheck: false,
        },
        {
          category: "workflow",
          feature: "Generation Cancellation",
          avelyn: "Immediate. Stop generations mid-flight to save RAM, CPU/GPU cycles, and tokens.",
          competitorText: "None. Must wait for generation to complete or time out.",
          avelynCheck: true,
          competitorCheck: false,
        },
        {
          category: "cost",
          feature: "Subscription & Limits",
          avelyn: "100% free core app. Use your own models locally or add private API keys.",
          competitorText: "Requires expensive monthly subscriptions for premium features.",
          avelynCheck: true,
          competitorCheck: false,
        },
        {
          category: "workflow",
          feature: "System Integration UI",
          avelyn: "Interactive command panel snaps directly to cursor on hotkey press.",
          competitorText: "Floating browser widgets or sidebar overlays that block view.",
          avelynCheck: true,
          competitorCheck: true,
        },
      ];
    }

    return [
      {
        category: "privacy",
        feature: "Data Privacy & Telemetry",
        avelyn: "Privacy-First. Stays local by default. Encrypted API key storage with password-masking. Zero cloud logging.",
        competitorText: "Cloud-reliant. Prompts are transmitted and potentially used for training.",
        avelynCheck: true,
        competitorCheck: false,
      },
      {
        category: "privacy",
        feature: "Compliance (HIPAA/GDPR)",
        avelyn: "100% compliant. Runs completely offline in local memory buffers. Stored keys are never sent to proxies.",
        competitorText: "Non-compliant by default. Requires expensive enterprise contracts.",
        avelynCheck: true,
        competitorCheck: false,
      },
      {
        category: "workflow",
        feature: "Multi-Provider Smart Routing",
        avelyn: "Yes. Routes between local Ollama and OpenRouter/Custom endpoints based on query rules.",
        competitorText: "No. Locked into OpenAI's cloud models.",
        avelynCheck: true,
        competitorCheck: false,
      },
      {
        category: "workflow",
        feature: "System-wide Integration",
        avelyn: "Native macOS menu bar. Trigger in any text editor, input, or IDE.",
        competitorText: "Isolated app/browser. Constantly copy-pasting back and forth.",
        avelynCheck: true,
        competitorCheck: false,
      },
      {
        category: "workflow",
        feature: "Offline Autonomy",
        avelyn: "Fully offline via local model hosting. Seamless automatic fallbacks to alternative endpoints.",
        competitorText: "Requires active internet. Subject to cloud server downtime or lag.",
        avelynCheck: true,
        competitorCheck: false,
      },
      {
        category: "workflow",
        feature: "Generation Cancellation",
        avelyn: "Yes. Cancel model responses immediately using a simple overlay button.",
        competitorText: "No. Generations cannot be interrupted mid-flight.",
        avelynCheck: true,
        competitorCheck: false,
      },
      {
        category: "cost",
        feature: "Subscription & Limits",
        avelyn: "100% free and open-source. Runs on your machine with zero caps.",
        competitorText: "$20/month subscription required for fast access. Strict hourly limits.",
        avelynCheck: true,
        competitorCheck: true,
      },
      {
        category: "cost",
        feature: "API Usage Fees",
        avelyn: "No mandatory fees. Use local open weights models or pay-as-you-go keys directly.",
        competitorText: "Requires pay-as-you-go developer tokens or active premium seats.",
        avelynCheck: true,
        competitorCheck: false,
      },
      {
        category: "workflow",
        feature: "Custom Prompt Library",
        avelyn: "Inline custom templates directly mapped to system shortcuts.",
        competitorText: "Needs prompt engineering chat loops for every single new task.",
        avelynCheck: true,
        competitorCheck: true,
      },
    ];
  };

  const comparisonData = getComparisonData();

  // Filter comparison list
  const filteredData = activeTab === "all" 
    ? comparisonData 
    : comparisonData.filter(item => item.category === activeTab);

  // Calculator logic:
  // Each edit saves ~30 seconds of typing/switching.
  // Pro license costs $15/month (Grammarly) or $20/month (ChatGPT) = $180 or $240/year per user.
  // Developer/writer time cost estimated at $50/hour.
  const secondsSavedPerEdit = 30;
  const hoursSavedPerYear = Math.round((teamSize * editsPerDay * secondsSavedPerEdit * 250) / 3600); // 250 working days
  const timeValueSaved = hoursSavedPerYear * 50;
  const licenseCostPerUser = competitor === "Grammarly" ? 180 : 240;
  const licensingSaved = teamSize * licenseCostPerUser;
  const totalSavings = timeValueSaved + licensingSaved;

  return (
    <div className="w-full max-w-5xl mx-auto px-4 py-8">
      {/* Category Tabs */}
      <div className="flex flex-wrap justify-center gap-2 mb-8">
        {[
          { id: "all", label: "All Features", icon: Cpu },
          { id: "privacy", label: "Security & Privacy", icon: Shield },
          { id: "workflow", label: "Workflow & Speed", icon: Clock },
          { id: "cost", label: "Cost & Limits", icon: CreditCard },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-full text-sm font-semibold transition-all duration-300 ${
                isActive 
                  ? "bg-[#7C3AED] text-white shadow-lg shadow-[#7C3AED]/25 scale-105" 
                  : "bg-neutral-50 hover:bg-neutral-100 text-neutral-600 hover:text-neutral-900 border border-neutral-200/50"
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Comparison Table Grid */}
      <div className="overflow-x-auto border border-neutral-200/60 rounded-3xl bg-white shadow-sm mb-16 transition-all duration-300">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-neutral-50/75 border-b border-neutral-200/60">
              <th className="p-6 text-xs font-bold text-neutral-900 uppercase tracking-wider">Feature</th>
              <th className="p-6 text-xs font-bold text-[#7C3AED] uppercase tracking-wider">Avelyn (Local AI)</th>
              <th className="p-6 text-xs font-bold text-neutral-500 uppercase tracking-wider">{competitor} (Cloud AI)</th>
            </tr>
          </thead>
          <tbody>
            {filteredData.map((row, idx) => (
              <tr 
                key={idx} 
                className="border-b border-neutral-100 last:border-none hover:bg-neutral-50/40 transition-colors duration-200"
              >
                <td className="p-6 font-semibold text-neutral-900 text-sm md:text-base">
                  {row.feature}
                </td>
                <td className="p-6 text-neutral-700 text-xs sm:text-sm">
                  <div className="flex items-start gap-2.5">
                    <div className="w-5 h-5 rounded-full bg-emerald-50 flex items-center justify-center shrink-0 mt-0.5">
                      <Check className="w-3.5 h-3.5 text-emerald-500" />
                    </div>
                    <span className="font-medium">{row.avelyn}</span>
                  </div>
                </td>
                <td className="p-6 text-neutral-400 text-xs sm:text-sm">
                  <div className="flex items-start gap-2.5">
                    <div className={`w-5 h-5 rounded-full flex items-center justify-center shrink-0 mt-0.5 ${
                      row.competitorCheck ? "bg-neutral-100" : "bg-rose-50"
                    }`}>
                      {row.competitorCheck ? (
                        <Check className="w-3.5 h-3.5 text-neutral-400" />
                      ) : (
                        <X className="w-3.5 h-3.5 text-rose-400" />
                      )}
                    </div>
                    <span className="font-medium">{row.competitorText}</span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Interactive Savings Calculator */}
      <div className="bg-[#FAFAFA] border border-neutral-200/60 rounded-3xl p-6 md:p-8 shadow-sm">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-[#7C3AED]/10 flex items-center justify-center">
            <Calculator className="w-5 h-5 text-[#7C3AED]" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-neutral-900">Avelyn ROI & Savings Calculator</h3>
            <p className="text-xs text-neutral-500 font-medium">Estimate your annual time and subscription savings</p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-8 items-center">
          {/* Controls */}
          <div className="space-y-6">
            <div>
              <div className="flex justify-between text-sm font-semibold mb-2">
                <span className="text-neutral-700">Team Size (Users)</span>
                <span className="text-[#7C3AED]">{teamSize}</span>
              </div>
              <input
                type="range"
                min="1"
                max="100"
                value={teamSize}
                onChange={(e) => setTeamSize(Number(e.target.value))}
                className="w-full h-2 bg-neutral-200 rounded-lg appearance-none cursor-pointer accent-[#7C3AED]"
              />
              <div className="flex justify-between text-[10px] text-neutral-400 mt-1">
                <span>1 user</span>
                <span>100 users</span>
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm font-semibold mb-2">
                <span className="text-neutral-700">AI Edits/Rewrites Per Day (Per User)</span>
                <span className="text-[#7C3AED]">{editsPerDay}</span>
              </div>
              <input
                type="range"
                min="1"
                max="50"
                value={editsPerDay}
                onChange={(e) => setEditsPerDay(Number(e.target.value))}
                className="w-full h-2 bg-neutral-200 rounded-lg appearance-none cursor-pointer accent-[#7C3AED]"
              />
              <div className="flex justify-between text-[10px] text-neutral-400 mt-1">
                <span>1 edit</span>
                <span>50 edits</span>
              </div>
            </div>
          </div>

          {/* Results Card */}
          <div className="bg-[#7C3AED] text-white rounded-2xl p-6 md:p-8 space-y-6 shadow-xl shadow-[#7C3AED]/20 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-[200px] h-[200px] bg-white/5 blur-[50px] rounded-full pointer-events-none" />
            
            <div className="grid grid-cols-2 gap-4 border-b border-white/10 pb-6">
              <div>
                <p className="text-[10px] font-bold uppercase tracking-widest text-white/70 mb-1">Time Saved / Year</p>
                <p className="text-2xl md:text-3xl font-extrabold">{hoursSavedPerYear} hrs</p>
              </div>
              <div>
                <p className="text-[10px] font-bold uppercase tracking-widest text-white/70 mb-1">Seats Cost Saved</p>
                <p className="text-2xl md:text-3xl font-extrabold">${licensingSaved.toLocaleString()}</p>
              </div>
            </div>

            <div>
              <p className="text-[10px] font-bold uppercase tracking-widest text-white/70 mb-1">Estimated Total Savings / Year</p>
              <p className="text-4xl md:text-5xl font-black">${totalSavings.toLocaleString()}</p>
              <p className="text-[10px] text-white/60 mt-2 font-medium">
                * Assumes average team editing value of $50/hr & ${licenseCostPerUser}/yr user license cost.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
