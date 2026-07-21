import { Metadata } from "next";
import FeaturePageTemplate from "@/components/FeaturePageTemplate";

export const metadata: Metadata = {
  title: "Cloud AI Engine — Google Gemini & OpenRouter Integration",
  description: "Connect personal API keys for ultra-fast Google Gemini Flash, Claude 3.5, and DeepSeek V3 streaming.",
  alternates: { canonical: "https://avelyn.software/features/cloud-ai" },
};

export default function CloudAIPage() {
  return (
    <FeaturePageTemplate
      slug="cloud-ai"
      title="Cloud AI Engine"
      tagline="High-Speed Streaming with Personal API Keys"
      description="Connect Google Gemini Flash, OpenRouter, or Custom API endpoints with encrypted personal API key security."
      keyBenefits={[
        "Ultra-low latency streaming SSE responses",
        "Access to 200+ top cloud LLMs",
        "Raw API pricing with zero middleman markup"
      ]}
      workflowSteps={[
        { step: "1", title: "Add API Key", desc: "Paste key in Settings → AI Provider." },
        { step: "2", title: "Select Model", desc: "Choose Gemini Flash or OpenRouter model." },
        { step: "3", title: "Stream", desc: "High-speed token streaming in real-time." }
      ]}
      faqs={[]}
    />
  );
}
