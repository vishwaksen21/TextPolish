import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Auto Provider Guide — Avelyn Documentation",
  description: "Learn how Auto Provider dynamically routes queries based on character length and privacy rules.",
  alternates: { canonical: "https://avelyn.software/docs/providers/auto-provider" },
};

export default function AutoProviderDoc() {
  return (
    <DocPageLayout
      categoryTitle="AI Providers"
      categorySlug="providers"
      itemSlug="auto-provider"
      title="Auto Provider Guide"
      description="Dynamic provider routing based on text length and privacy logic."
    >
      <h2>Heuristic Provider Selection</h2>
      <p>Short queries (&lt;50 characters) automatically run on Local Ollama for speed, while long documents route to cloud models.</p>
    </DocPageLayout>
  );
}
