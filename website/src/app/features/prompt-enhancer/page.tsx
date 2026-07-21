import { Metadata } from "next";
import FeaturePageTemplate from "@/components/FeaturePageTemplate";

export const metadata: Metadata = {
  title: "AI Prompt Enhancer for Mac — Optimize Raw Instructions System-Wide",
  description: "Transform raw, vague user instructions into structured LLM prompts automatically with Avelyn's AI Prompt Enhancer on macOS.",
  alternates: { canonical: "https://avelyn.software/features/prompt-enhancer" },
};

export default function PromptEnhancerPage() {
  return (
    <FeaturePageTemplate
      slug="prompt-enhancer"
      title="AI Prompt Enhancer for macOS"
      tagline="Transform Vague Queries into Rich LLM Prompts"
      description="Automatically expand raw user inputs into structured, context-rich prompts before routing them to local Ollama or cloud models."
      keyBenefits={[
        "Eliminates conversational filler and generic LLM answers",
        "Injects output format constraints, domain boundaries, and active tone rules",
        "Works globally across any Mac app via Option+Space shortcut"
      ]}
      workflowSteps={[
        { step: "1", title: "Highlight Any Text", desc: "Select raw notes or instructions in any Mac application." },
        { step: "2", title: "Trigger Hotkey", desc: "Press Option+Space to open the Command Palette." },
        { step: "3", title: "Select Enhance Prompt", desc: "Watch Avelyn expand and optimize your prompt before execution." }
      ]}
      faqs={[
        {
          question: "How does Prompt Enhancement improve LLM outputs?",
          answer: "By adding explicit role instructions, output format rules, and conciseness constraints, models generate precise, non-conversational results."
        }
      ]}
      relatedDocs={[
        { title: "Prompt Enhancement Guide", href: "/docs/features/prompt-enhancement", description: "Technical breakdown of prompt rules." }
      ]}
    />
  );
}
