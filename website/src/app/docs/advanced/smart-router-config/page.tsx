import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Smart Router Config Guide — Avelyn Documentation",
  description: "Fine-tune task group mappings (Coding, Writing, Reasoning, Voice, Privacy).",
  alternates: { canonical: "https://avelyn.software/docs/advanced/smart-router-config" },
};

export default function SmartRouterConfigDoc() {
  return (
    <DocPageLayout
      categoryTitle="Advanced Customization"
      categorySlug="advanced"
      itemSlug="smart-router-config"
      title="Smart Router Configuration"
      description="Fine-tune task group provider mappings."
    >
      <h2>Task Mappings</h2>
      <p>Assign specific provider and model pairs to Coding, Writing, Reasoning, and Privacy task groups.</p>
    </DocPageLayout>
  );
}
