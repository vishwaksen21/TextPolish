import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Professional Writing Mode Guide — Avelyn Documentation",
  description: "Elevate casual drafts into clear, authoritative executive communication.",
  alternates: { canonical: "https://avelyn.software/docs/features/professional-writing" },
};

export default function ProfessionalWritingDoc() {
  return (
    <DocPageLayout
      categoryTitle="Core Features"
      categorySlug="features"
      itemSlug="professional-writing"
      title="Professional Writing Guide"
      description="Refine informal notes into clear, authoritative executive reports and client updates."
    >
      <h2>Executive Tone Elevation</h2>
      <p>
        Professional mode removes filler words, colloquial slang, and passive constructions—replacing them with concise active phrasing ideal for corporate reports, proposals, and emails.
      </p>
    </DocPageLayout>
  );
}
