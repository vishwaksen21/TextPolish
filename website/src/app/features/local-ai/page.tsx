import { Metadata } from "next";
import FeaturePageTemplate from "@/components/FeaturePageTemplate";

export const metadata: Metadata = {
  title: "Local Offline AI Engine — 100% Private Mac AI",
  description: "Run local LLMs (Gemma 3, Llama 3) via Ollama with 100% offline privacy and zero data tracking.",
  alternates: { canonical: "https://avelyn.software/features/local-ai" },
};

export default function LocalAIPage() {
  return (
    <FeaturePageTemplate
      slug="local-ai"
      title="Local Offline AI Engine"
      tagline="100% Offline Privacy with Ollama"
      description="Run open-source LLMs locally on Apple Silicon GPUs without internet connectivity or corporate data leaks."
      keyBenefits={[
        "100% offline air-gapped security",
        "Zero prompt telemetry or analytics tracking",
        "Free local execution without subscriptions"
      ]}
      workflowSteps={[
        { step: "1", title: "Install Ollama", desc: "Auto-installer pulls model weights." },
        { step: "2", title: "Select Local AI", desc: "Set provider to Local Ollama." },
        { step: "3", title: "Offline Refinement", desc: "Process text with zero internet requirement." }
      ]}
      faqs={[]}
    />
  );
}
