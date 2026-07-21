import { Metadata } from "next";
import FeaturePageTemplate from "@/components/FeaturePageTemplate";

export const metadata: Metadata = {
  title: "Best AI Assistant for Developers on Mac — Refactor Code & Docstrings",
  description: "Refactor code, generate unit tests, and add docstrings across VS Code, Xcode, JetBrains, and Terminal.",
  alternates: { canonical: "https://avelyn.software/solutions/best-ai-assistant-developers" },
};

export default function BestAIAssistantDevelopersSolution() {
  return (
    <FeaturePageTemplate
      slug="best-ai-assistant-developers"
      title="Best AI Assistant for Developers on Mac"
      tagline="Refactor Code in Any IDE or Terminal"
      description="System-wide developer coding assistant: refactor code, generate tests, explain algorithms, and format docstrings."
      keyBenefits={[
        "Works globally across VS Code, Xcode, JetBrains, and Terminal",
        "Routes code tasks automatically to DeepSeek-Coder or Claude 3.5",
        "Strips conversational meta-talk and outputs clean code snippets"
      ]}
      workflowSteps={[
        { step: "1", title: "Select Code", desc: "Highlight code block in your editor." },
        { step: "2", title: "Press Hotkey", desc: "Trigger Option+Space and select Code." },
        { step: "3", title: "Refactored", desc: "Clean code replaces selection in-place." }
      ]}
      faqs={[]}
    />
  );
}
