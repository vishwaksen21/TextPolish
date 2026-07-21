import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Coding Assistant Guide — Avelyn Documentation",
  description: "Refactor, explain, debug, and document code snippets across VS Code, Xcode, and JetBrains.",
  alternates: { canonical: "https://avelyn.software/docs/features/coding-assistant" },
};

export default function CodingAssistantDoc() {
  return (
    <DocPageLayout
      categoryTitle="Core Features"
      categorySlug="features"
      itemSlug="coding-assistant"
      title="Coding Assistant Guide"
      description="Refactor code, generate unit tests, and add docstrings inside any IDE."
    >
      <h2>System-Wide Code Refactoring</h2>
      <p>
        Highlight code blocks inside VS Code, Xcode, JetBrains, or Terminal, press <code>Option+Space</code>, and select <strong>Code</strong> to refactor, explain, or fix bugs automatically.
      </p>
    </DocPageLayout>
  );
}
