import { Metadata } from "next";
import FeaturePageTemplate from "@/components/FeaturePageTemplate";

export const metadata: Metadata = {
  title: "Grammar Correction AI for Mac — Zero Keylogging Grammar Fixing",
  description: "Fix grammar, spelling, and syntax errors in-place without background keyloggers or monthly fees.",
  alternates: { canonical: "https://avelyn.software/solutions/grammar-correction-ai" },
};

export default function GrammarCorrectionAISolution() {
  return (
    <FeaturePageTemplate
      slug="grammar-correction-ai"
      title="Grammar Correction AI for Mac"
      tagline="Neural Grammar & Syntax Refinement"
      description="Fix spelling, punctuation, and awkward phrasing instantly with local neural LLMs on macOS."
      keyBenefits={[
        "Understands technical domain jargon without false positive flags",
        "Runs 100% offline via local Ollama models",
        "Replaces text in-place in ~100 ms"
      ]}
      workflowSteps={[
        { step: "1", title: "Select Draft", desc: "Highlight text with typos." },
        { step: "2", title: "Press Hotkey", desc: "Trigger Option+Space." },
        { step: "3", title: "Fixed", desc: "Text is corrected automatically." }
      ]}
      faqs={[]}
    />
  );
}
