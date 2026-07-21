import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Custom System Prompts Guide — Avelyn Documentation",
  description: "Create domain-specific custom mode presets and tailored system prompt rules.",
  alternates: { canonical: "https://avelyn.software/docs/advanced/custom-system-prompts" },
};

export default function CustomSystemPromptsDoc() {
  return (
    <DocPageLayout
      categoryTitle="Advanced Customization"
      categorySlug="advanced"
      itemSlug="custom-system-prompts"
      title="Custom System Prompts Guide"
      description="Design custom system prompts and mode presets tailored to your industry."
    >
      <h2>Tailored Preset Engine</h2>
      <p>Add custom mode buttons with specialized system prompts in Settings → Custom Modes.</p>
    </DocPageLayout>
  );
}
