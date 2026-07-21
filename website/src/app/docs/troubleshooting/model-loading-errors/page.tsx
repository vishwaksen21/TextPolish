import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Model Loading Errors — Avelyn Troubleshooting",
  description: "Handling missing weights and VRAM allocation failures in Ollama.",
  alternates: { canonical: "https://avelyn.software/docs/troubleshooting/model-loading-errors" },
};

export default function ModelLoadingErrorsDoc() {
  return (
    <DocPageLayout
      categoryTitle="Troubleshooting"
      categorySlug="troubleshooting"
      itemSlug="model-loading-errors"
      title="Fixing Model Loading Errors"
      description="Resolving missing Ollama weights and VRAM allocation errors."
    >
      <h2>Missing Model Weights</h2>
      <p>If Ollama reports a missing model error, execute <code>ollama pull gemma3:4b</code> in your macOS terminal.</p>
    </DocPageLayout>
  );
}
