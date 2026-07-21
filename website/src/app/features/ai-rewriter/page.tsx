import { Metadata } from "next";
import FeaturePageTemplate from "@/components/FeaturePageTemplate";

export const metadata: Metadata = {
  title: "AI Text Rewriter for Mac — Paraphrase & Transform Text System-Wide",
  description: "Paraphrase, expand, shorten, or change tone of highlighted text across any macOS application.",
  alternates: { canonical: "https://avelyn.software/features/ai-rewriter" },
};

export default function AIRewriterPage() {
  return (
    <FeaturePageTemplate
      slug="ai-rewriter"
      title="AI Text Rewriter for macOS"
      tagline="Paraphrase & Adapt Text System-Wide"
      description="Rewrite, rephrase, expand, or condense highlighted text across any Mac application with customized tone rules."
      keyBenefits={[
        "Custom instructions: type any prompt to reshape tone or length",
        "Preserves original formatting and Markdown structure",
        "Works offline or via high-speed cloud providers"
      ]}
      workflowSteps={[
        { step: "1", title: "Highlight Text", desc: "Select text in Pages, Notion, or Slack." },
        { step: "2", title: "Type Instruction", desc: "Type custom rephrase instructions." },
        { step: "3", title: "Replace", desc: "Text is updated in-place instantly." }
      ]}
      faqs={[]}
    />
  );
}
