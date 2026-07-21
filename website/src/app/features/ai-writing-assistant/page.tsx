import { Metadata } from "next";
import FeaturePageTemplate from "@/components/FeaturePageTemplate";

export const metadata: Metadata = {
  title: "AI Writing Assistant for Mac — Privacy-First System-Wide Refinement",
  description: "System-wide AI writing assistant for macOS. Refine drafts, shift tone, and fix grammar without cloud tracking.",
  alternates: { canonical: "https://avelyn.software/features/ai-writing-assistant" },
};

export default function AIWritingAssistantPage() {
  return (
    <FeaturePageTemplate
      slug="ai-writing-assistant"
      title="System-Wide AI Writing Assistant for Mac"
      tagline="Privacy-First Writing Acceleration"
      description="Refine drafts, fix grammar, rewrite proposals, and adapt tone across every app on your Mac."
      keyBenefits={[
        "Works globally across all native macOS apps",
        "100% offline local privacy with Ollama",
        "Zero subscription fees for local AI"
      ]}
      workflowSteps={[
        { step: "1", title: "Highlight", desc: "Select text in any Mac app." },
        { step: "2", title: "Trigger", desc: "Press Option+Space." },
        { step: "3", title: "Refine", desc: "AI rewrites text in-place." }
      ]}
      faqs={[]}
    />
  );
}
