import { Metadata } from "next";
import FeaturePageTemplate from "@/components/FeaturePageTemplate";

export const metadata: Metadata = {
  title: "Best AI Writing Assistant for Mac (2026) — System-Wide Local AI",
  description: "Avelyn is the privacy-first AI writing assistant for macOS. Refine drafts, fix grammar, and rewrite text system-wide with local Ollama or cloud models.",
  alternates: { canonical: "https://avelyn.software/solutions/ai-writing-assistant-mac" },
};

export default function AIWritingAssistantMacSolution() {
  return (
    <FeaturePageTemplate
      slug="ai-writing-assistant-mac"
      title="AI Writing Assistant for Mac"
      tagline="Privacy-First System-Wide Text Refinement"
      description="The definitive system-wide AI writing assistant for macOS. Highlight text anywhere, trigger Option+Space, and refine writing in under 100 ms."
      keyBenefits={[
        "System-wide global hotkey integration across Mail, Xcode, Slack, Safari",
        "100% offline local AI option with zero cloud tracking",
        "Multi-provider router: Ollama, Gemini Flash, OpenRouter, Custom APIs"
      ]}
      workflowSteps={[
        { step: "1", title: "Select Text", desc: "Highlight text in any Mac app." },
        { step: "2", title: "Press Hotkey", desc: "Trigger Option+Space shortcut." },
        { step: "3", title: "Auto Replace", desc: "AI rewrites text in-place instantly." }
      ]}
      faqs={[
        {
          question: "Why is Avelyn the best AI writing assistant for Mac?",
          answer: "Because it works system-wide via native global hotkeys without requiring copy-pasting into web browser tabs."
        }
      ]}
    />
  );
}
