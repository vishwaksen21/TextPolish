import { Metadata } from "next";
import FeaturePageTemplate from "@/components/FeaturePageTemplate";

export const metadata: Metadata = {
  title: "AI Translation Tool for Mac — System-Wide Multilingual Translation",
  description: "Translate highlighted text between 50+ languages instantly without leaving your active Mac app.",
  alternates: { canonical: "https://avelyn.software/features/translation" },
};

export default function TranslationPage() {
  return (
    <FeaturePageTemplate
      slug="translation"
      title="AI Translation Tool for macOS"
      tagline="Translate 50+ Languages System-Wide"
      description="Translate text across Spanish, French, German, Japanese, Chinese, and 50+ languages without switching browser tabs."
      keyBenefits={[
        "Preserves natural idiomatic tone and technical terms",
        "Operates directly inside Mail, Slack, Pages, and Chrome",
        "Supports local offline translation via Ollama"
      ]}
      workflowSteps={[
        { step: "1", title: "Highlight Text", desc: "Select text in any language." },
        { step: "2", title: "Select Translate", desc: "Choose your target language." },
        { step: "3", title: "Instant Result", desc: "Translated text is pasted in-place." }
      ]}
      faqs={[]}
    />
  );
}
