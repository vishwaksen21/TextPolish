import { Metadata } from "next";
import FeaturePageTemplate from "@/components/FeaturePageTemplate";

export const metadata: Metadata = {
  title: "Offline AI Writing Assistant for Mac — 100% Air-Gapped Privacy",
  description: "Run offline local LLMs (Gemma 3, Llama 3) on Apple Silicon. Zero internet requirement, zero corporate data leaks.",
  alternates: { canonical: "https://avelyn.software/solutions/offline-ai-writing-assistant" },
};

export default function OfflineAIWritingAssistantSolution() {
  return (
    <FeaturePageTemplate
      slug="offline-ai-writing-assistant"
      title="Offline AI Writing Assistant for Mac"
      tagline="Air-Gapped Local AI Execution"
      description="Run open-source LLMs locally on Apple Silicon GPUs without internet connectivity or corporate telemetry."
      keyBenefits={[
        "100% offline air-gapped processing via Local Ollama",
        "Zero data transmission over the network",
        "Zero recurring subscription fees"
      ]}
      workflowSteps={[
        { step: "1", title: "Setup Ollama", desc: "One-click local model installation." },
        { step: "2", title: "Select Local AI", desc: "Choose Gemma 3 or Llama 3." },
        { step: "3", title: "Air-Gapped Refinement", desc: "Refine text with Wi-Fi disconnected." }
      ]}
      faqs={[]}
    />
  );
}
