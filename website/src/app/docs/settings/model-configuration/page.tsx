import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Model Configuration Guide — Avelyn Documentation",
  description: "Select active LLM models, set temperature parameters, and adjust system prompt presets.",
  alternates: { canonical: "https://avelyn.software/docs/settings/model-configuration" },
};

export default function ModelConfigurationDoc() {
  return (
    <DocPageLayout
      categoryTitle="Settings & Configuration"
      categorySlug="settings"
      itemSlug="model-configuration"
      title="Model Configuration Guide"
      description="Select active models and adjust temperature and token limits."
    >
      <h2>Model Selection & Parameters</h2>
      <p>Configure model identifiers, temperature (0.15 default), and context token limits in Settings → AI Provider.</p>
    </DocPageLayout>
  );
}
