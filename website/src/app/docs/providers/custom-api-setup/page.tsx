import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Custom API Setup Guide — Avelyn Documentation",
  description: "Connect LM Studio, vLLM, Groq, or OpenAI-compatible endpoints to Avelyn.",
  alternates: { canonical: "https://avelyn.software/docs/providers/custom-api-setup" },
};

export default function CustomAPISetupDoc() {
  return (
    <DocPageLayout
      categoryTitle="AI Providers"
      categorySlug="providers"
      itemSlug="custom-api-setup"
      title="Custom API Setup Guide"
      description="Connect LM Studio, vLLM, Groq, or self-hosted OpenAI-compatible endpoints."
    >
      <h2>OpenAI-Compatible Endpoint Configuration</h2>
      <p>Enter your custom base URL (e.g. <code>http://localhost:1234/v1</code>) and model identifier in Settings.</p>
    </DocPageLayout>
  );
}
