import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Google Gemini Integration Guide — Avelyn Documentation",
  description: "Connect Google Gemini 2.5 Flash for ultra-fast streaming responses using custom API keys.",
  alternates: { canonical: "https://avelyn.software/docs/providers/gemini-integration" },
};

export default function GeminiIntegrationDoc() {
  return (
    <DocPageLayout
      categoryTitle="AI Providers"
      categorySlug="providers"
      itemSlug="gemini-integration"
      title="Google Gemini Flash Integration Guide"
      description="Connect Google's Gemini Flash models using the official GenAI SDK."
    >
      <h2>Connecting Google Gemini Flash</h2>
      <ol>
        <li>Obtain a free API key from <code>aistudio.google.com</code>.</li>
        <li>Open Avelyn Settings → AI Provider.</li>
        <li>Select <strong>Google Gemini</strong> and paste your API key.</li>
        <li>Click <strong>Test Connection</strong> to verify setup.</li>
      </ol>
    </DocPageLayout>
  );
}