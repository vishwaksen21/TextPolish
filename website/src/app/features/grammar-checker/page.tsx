import { Metadata } from "next";
import FeaturePageTemplate from "@/components/FeaturePageTemplate";

export const metadata: Metadata = {
  title: "AI Grammar Checker for Mac — Local & System-Wide Syntax Correction",
  description: "Fix grammar, spelling, and awkward phrasing in-place across Mail, Slack, Notion, and Xcode without cloud keyloggers.",
  alternates: { canonical: "https://avelyn.software/features/grammar-checker" },
};

export default function GrammarCheckerPage() {
  return (
    <FeaturePageTemplate
      slug="grammar-checker"
      title="Neural AI Grammar Checker for macOS"
      tagline="Fix Grammar System-Wide with Zero Cloud Keylogging"
      description="Refine spelling, punctuation, and awkward phrasing instantly with local neural LLMs that preserve your original tone and technical jargon."
      keyBenefits={[
        "Understands technical jargon and software variable names without false flags",
        "Runs 100% offline via local Ollama models or fast cloud APIs",
        "Replaces text directly inside your cursor location in under 100 ms"
      ]}
      workflowSteps={[
        { step: "1", title: "Select Messy Draft", desc: "Highlight text with typos or awkward grammar." },
        { step: "2", title: "Press Hotkey", desc: "Trigger Option+Space." },
        { step: "3", title: "Instant Correction", desc: "Grammar is fixed in-place automatically." }
      ]}
      faqs={[
        {
          question: "How is Avelyn Grammar Checker different from Grammarly?",
          answer: "Avelyn runs 100% offline with zero background keylogging—it only activates when manually triggered via hotkey."
        }
      ]}
      relatedDocs={[
        { title: "Grammar Correction Guide", href: "/docs/features/grammar-correction", description: "Learn about neural grammar." }
      ]}
    />
  );
}
