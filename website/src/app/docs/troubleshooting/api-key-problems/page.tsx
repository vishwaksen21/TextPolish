import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "API Key Problems — Avelyn Troubleshooting",
  description: "Fixing 401 unauthorized, rate-limiting, and key validation errors for OpenRouter and Gemini.",
  alternates: { canonical: "https://avelyn.software/docs/troubleshooting/api-key-problems" },
};

export default function APIKeyProblemsDoc() {
  return (
    <DocPageLayout
      categoryTitle="Troubleshooting"
      categorySlug="troubleshooting"
      itemSlug="api-key-problems"
      title="Fixing API Key Validation Errors"
      description="Resolving 401 Unauthorized, rate-limiting, and credit exhaustion issues."
    >
      <h2>Common API Key Issues</h2>
      <ul>
        <li><strong>HTTP 401 Invalid Key:</strong> Verify that your API key string does not contain leading spaces.</li>
        <li><strong>HTTP 402 Insufficient Credits:</strong> Top up your OpenRouter credits balance.</li>
        <li><strong>HTTP 429 Rate Limited:</strong> Enable Smart Fallback to failover to local models.</li>
      </ul>
    </DocPageLayout>
  );
}
