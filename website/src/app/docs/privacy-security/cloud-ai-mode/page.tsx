import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Cloud AI Mode Guide — Avelyn Documentation",
  description: "Secure cloud requests using personal OpenRouter or Gemini API keys.",
  alternates: { canonical: "https://avelyn.software/docs/privacy-security/cloud-ai-mode" },
};

export default function CloudAIModeDoc() {
  return (
    <DocPageLayout
      categoryTitle="Privacy & Security"
      categorySlug="privacy-security"
      itemSlug="cloud-ai-mode"
      title="Cloud AI Mode Guide"
      description="Direct TLS-encrypted API calls using personal API keys."
    >
      <h2>Encrypted Cloud API Calls</h2>
      <p>Cloud AI Mode connects directly to OpenRouter or Google Gemini endpoints using your personal API keys, bypassing third-party proxy servers.</p>
    </DocPageLayout>
  );
}
