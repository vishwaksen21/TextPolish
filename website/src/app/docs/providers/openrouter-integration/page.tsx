import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "OpenRouter Integration Guide — Avelyn Documentation",
  description: "Access 200+ top cloud LLMs (GPT-4o, Claude 3.5, DeepSeek V3) via OpenRouter.",
  alternates: { canonical: "https://avelyn.software/docs/providers/openrouter-integration" },
};

export default function OpenRouterIntegrationDoc() {
  return (
    <DocPageLayout
      categoryTitle="AI Providers"
      categorySlug="providers"
      itemSlug="openrouter-integration"
      title="OpenRouter Integration Guide"
      description="Connect OpenRouter to access GPT-4o, Claude 3.5, and DeepSeek V3 with personal API keys."
    >
      <h2>OpenRouter Setup</h2>
      <ol>
        <li>Paste your <code>sk-or-v1-...</code> API key into Settings → AI Provider.</li>
        <li>Select from dynamic cached model lists.</li>
      </ol>
    </DocPageLayout>
  );
}
