import { Metadata } from "next";
import FeaturePageTemplate from "@/components/FeaturePageTemplate";

export const metadata: Metadata = {
  title: "AI Coding Assistant for Mac — Refactor & Debug Code System-Wide",
  description: "Refactor, explain, and debug code snippets inside VS Code, Xcode, JetBrains, and Terminal with AI hotkeys.",
  alternates: { canonical: "https://avelyn.software/features/coding-assistant" },
};

export default function CodingAssistantPage() {
  return (
    <FeaturePageTemplate
      slug="coding-assistant"
      title="AI Developer Coding Assistant for macOS"
      tagline="Refactor & Debug Code in Any IDE"
      description="Refactor code, generate unit tests, explain complex algorithms, and add docstrings across VS Code, Xcode, and JetBrains."
      keyBenefits={[
        "Strips conversational meta-talk and outputs clean code snippets",
        "Routes code tasks automatically to DeepSeek-Coder or Claude 3.5",
        "Works globally across any text editor or terminal session"
      ]}
      workflowSteps={[
        { step: "1", title: "Highlight Code", desc: "Select code block in your IDE." },
        { step: "2", title: "Press Hotkey", desc: "Trigger Option+Space and select Code." },
        { step: "3", title: "Refactored Output", desc: "Clean code replaces original selection." }
      ]}
      faqs={[]}
    />
  );
}
