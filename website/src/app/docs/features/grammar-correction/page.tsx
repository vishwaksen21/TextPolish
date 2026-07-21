import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Grammar Correction Guide — Avelyn Documentation",
  description: "Fix spelling, syntax, punctuation, and awkward phrasing instantly with local neural LLM models.",
  alternates: { canonical: "https://avelyn.software/docs/features/grammar-correction" },
};

export default function GrammarCorrectionDoc() {
  return (
    <DocPageLayout
      categoryTitle="Core Features"
      categorySlug="features"
      itemSlug="grammar-correction"
      title="Grammar Correction Guide"
      description="Fix spelling, punctuation, and syntax errors without altering author intent or tone."
    >
      <h2>Neural Grammar vs. Legacy Rule Checkers</h2>
      <p>
        Legacy grammar checkers flag domain terms, software code variables, and informal expressions as errors. Avelyn uses neural LLMs (Gemma 3, Llama 3) to analyze semantic intent—fixing real typos while respecting specialized vocabulary.
      </p>

      <h2>How to Use</h2>
      <p>Highlight messy text, press <code>Option+Space</code>, and select <strong>Grammar</strong>.</p>
    </DocPageLayout>
  );
}
