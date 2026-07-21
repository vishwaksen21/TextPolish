import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Translation Guide — Avelyn Documentation",
  description: "Translate highlighted text between 50+ languages without leaving your application.",
  alternates: { canonical: "https://avelyn.software/docs/features/translation" },
};

export default function TranslationDoc() {
  return (
    <DocPageLayout
      categoryTitle="Core Features"
      categorySlug="features"
      itemSlug="translation"
      title="Translation Guide"
      description="Translate text across 50+ languages system-wide without opening browser tabs."
    >
      <h2>System-Wide Multilingual Translation</h2>
      <p>
        Highlight foreign text in Slack, Safari, or Pages, trigger <code>Option+Space</code>, and select <strong>Translate</strong> to receive instant, natural-sounding translations.
      </p>
    </DocPageLayout>
  );
}
