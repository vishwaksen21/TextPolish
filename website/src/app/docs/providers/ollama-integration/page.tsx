import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Local Ollama Integration Guide — Avelyn Documentation",
  description: "Run 100% offline LLMs (Gemma 3, Llama 3, Qwen) on Apple Silicon with zero cloud dependency.",
  alternates: { canonical: "https://avelyn.software/docs/providers/ollama-integration" },
};

export default function OllamaIntegrationDoc() {
  return (
    <DocPageLayout
      categoryTitle="AI Providers"
      categorySlug="providers"
      itemSlug="ollama-integration"
      title="Local Ollama Integration Guide"
      description="Run 100% offline LLMs locally on macOS with zero cloud telemetry."
    >
      <h2>Configuring Local Ollama</h2>
      <p>
        Avelyn connects to Ollama running on <code>http://localhost:11434</code>.
      </p>
      <pre><code>ollama pull gemma3:4b</code></pre>
    </DocPageLayout>
  );
}