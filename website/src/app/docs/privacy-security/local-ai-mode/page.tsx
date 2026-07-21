import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Local AI Mode Guide — Avelyn Documentation",
  description: "Learn how Local AI mode runs 100% offline with zero cloud telemetry using Ollama.",
  alternates: { canonical: "https://avelyn.software/docs/privacy-security/local-ai-mode" },
};

export default function LocalAIModeDoc() {
  return (
    <DocPageLayout
      categoryTitle="Privacy & Security"
      categorySlug="privacy-security"
      itemSlug="local-ai-mode"
      title="Local AI Mode Guide"
      description="Run 100% offline inference on your Mac with zero telemetry."
    >
      <h2>Zero Cloud Telemetry</h2>
      <p>Local AI mode processes all prompts using local model weights on Apple Silicon GPUs via Ollama. No data ever leaves your computer.</p>
    </DocPageLayout>
  );
}
