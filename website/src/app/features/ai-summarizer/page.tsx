import { Metadata } from "next";
import FeaturePageTemplate from "@/components/FeaturePageTemplate";

export const metadata: Metadata = {
  title: "AI Text Summarizer for Mac — Condense Articles & PDFs Instantly",
  description: "Summarize multi-page articles, PDFs, and meeting notes into key bullet points system-wide.",
  alternates: { canonical: "https://avelyn.software/features/ai-summarizer" },
};

export default function AISummarizerPage() {
  return (
    <FeaturePageTemplate
      slug="ai-summarizer"
      title="AI Text Summarizer for macOS"
      tagline="Condense Long Articles & Documents Instantly"
      description="Extract key executive takeaways, action items, and bullet points from multi-page PDFs, research papers, and articles."
      keyBenefits={[
        "Supports 8k context token windows for long document synthesis",
        "Generates clean Markdown bullet points",
        "Functions offline on Apple Silicon GPUs"
      ]}
      workflowSteps={[
        { step: "1", title: "Select Long Document", desc: "Highlight long text in Safari or Preview." },
        { step: "2", title: "Press Hotkey", desc: "Trigger Option+Space and select Summarize." },
        { step: "3", title: "Get Takeaways", desc: "Bullet summary streams into your notes." }
      ]}
      faqs={[]}
    />
  );
}
