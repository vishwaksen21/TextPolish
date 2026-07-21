import { Metadata } from "next";
import FeaturePageTemplate from "@/components/FeaturePageTemplate";

export const metadata: Metadata = {
  title: "Native macOS AI Assistant — System-Wide Integration",
  description: "Native macOS menu bar tray application with global keyboard shortcuts and Apple Silicon optimization.",
  alternates: { canonical: "https://avelyn.software/features/mac-ai-assistant" },
};

export default function MacAIAssistantPage() {
  return (
    <FeaturePageTemplate
      slug="mac-ai-assistant"
      title="Native macOS AI Assistant"
      tagline="Built Exclusively for Mac Power Users"
      description="System-wide menu bar app designed for Apple Silicon M1/M2/M3/M4 with double-tap hotkeys and instant paste."
      keyBenefits={[
        "Native macOS menu bar tray integration",
        "Optimized for Apple Silicon Unified Memory Architecture",
        "Zero browser extension dependencies"
      ]}
      workflowSteps={[
        { step: "1", title: "Highlight", desc: "Select text anywhere on macOS." },
        { step: "2", title: "Hotkey", desc: "Press Option+Space." },
        { step: "3", title: "Instant Paste", desc: "Cmd+V replaces text automatically." }
      ]}
      faqs={[]}
    />
  );
}
