import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Summarization Mode Guide — Avelyn Documentation",
  description: "Condense multi-page articles, PDFs, and meeting transcripts into key bullet points.",
  alternates: { canonical: "https://avelyn.software/docs/features/summarization" },
};

export default function SummarizationDoc() {
  return (
    <DocPageLayout
      categoryTitle="Core Features"
      categorySlug="features"
      itemSlug="summarization"
      title="Summarization Guide"
      description="Extract key takeaways and action items from long articles and reports."
    >
      <h2>Executive Bullet Summaries</h2>
      <p>
        Highlight long paragraphs or multi-page text blocks to extract key executive takeaways, action items, or bullet points in seconds.
      </p>
    </DocPageLayout>
  );
}
