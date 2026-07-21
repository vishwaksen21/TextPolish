import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Auto Provider Config — Avelyn Documentation",
  description: "Adjust character threshold rules and privacy fallbacks for automatic provider selection.",
  alternates: { canonical: "https://avelyn.software/docs/advanced/auto-provider-config" },
};

export default function AutoProviderConfigDoc() {
  return (
    <DocPageLayout
      categoryTitle="Advanced Customization"
      categorySlug="advanced"
      itemSlug="auto-provider-config"
      title="Auto Provider Configuration"
      description="Adjust character thresholds and heuristic routing rules."
    >
      <h2>Heuristic Tuning</h2>
      <p>Customize short text length thresholds (&lt;50 characters) and code syntax detection triggers.</p>
    </DocPageLayout>
  );
}
