import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Smart Fallback Guide — Avelyn Documentation",
  description: "Configure multi-provider priority failover chains.",
  alternates: { canonical: "https://avelyn.software/docs/advanced/smart-fallback" },
};

export default function SmartFallbackDoc() {
  return (
    <DocPageLayout
      categoryTitle="Advanced Customization"
      categorySlug="advanced"
      itemSlug="smart-fallback"
      title="Smart Fallback Chain Configuration"
      description="Configure backup provider priority failover order."
    >
      <h2>Multi-Provider Failover Priority</h2>
      <p>Define secondary and tertiary backup providers (e.g. OpenRouter -&gt; Gemini -&gt; Local Ollama) to ensure zero downtime.</p>
    </DocPageLayout>
  );
}
