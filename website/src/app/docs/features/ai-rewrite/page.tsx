import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "AI Rewrite Guide — Avelyn Documentation",
  description: "Paraphrase, rephrase, expand, or shorten highlighted text system-wide.",
  alternates: { canonical: "https://avelyn.software/docs/features/ai-rewrite" },
};

export default function AIRewriteDoc() {
  return (
    <DocPageLayout
      categoryTitle="Core Features"
      categorySlug="features"
      itemSlug="ai-rewrite"
      title="AI Rewrite Guide"
      description="Paraphrase, expand, or condense text with custom instructions."
    >
      <h2>Flexible Paraphrasing & Transformation</h2>
      <p>
        AI Rewrite mode accepts custom prompt instructions (e.g. <em>"Make this sound energetic"</em> or <em>"Condense to 2 sentences"</em>) and transforms selected text in-place.
      </p>
    </DocPageLayout>
  );
}
