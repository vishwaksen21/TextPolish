import { Metadata } from "next";
import FeaturePageTemplate from "@/components/FeaturePageTemplate";

export const metadata: Metadata = {
  title: "AI Prompt Enhancer Tool — System-Wide Prompt Tuning on Mac",
  description: "Automatically expand raw 3-word notes into detail-oriented system prompts before executing LLMs.",
  alternates: { canonical: "https://avelyn.software/solutions/prompt-enhancer-tool" },
};

export default function PromptEnhancerToolSolution() {
  return (
    <FeaturePageTemplate
      slug="prompt-enhancer-tool"
      title="AI Prompt Enhancer Tool"
      tagline="Transform Raw Instructions into Precision Prompts"
      description="Automatically expand brief user queries into context-rich system prompts system-wide on macOS."
      keyBenefits={[
        "Eliminates conversational filler and generic chatbot replies",
        "Injects output constraints and tone boundaries",
        "Works across all native macOS apps"
      ]}
      workflowSteps={[
        { step: "1", title: "Type Raw Note", desc: "Type a brief 3-word instruction." },
        { step: "2", title: "Trigger Hotkey", desc: "Press Option+Space." },
        { step: "3", title: "Enhance", desc: "Avelyn expands the prompt automatically." }
      ]}
      faqs={[]}
    />
  );
}
