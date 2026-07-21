import { Metadata } from "next";
import FeaturePageTemplate from "@/components/FeaturePageTemplate";

export const metadata: Metadata = {
  title: "AI Productivity App for Mac — System-Wide Hotkey Text Automation",
  description: "Maximize daily macOS productivity with global hotkeys, instant text replacement, and zero context switching.",
  alternates: { canonical: "https://avelyn.software/solutions/ai-productivity-app-mac" },
};

export default function AIProductivityAppMacSolution() {
  return (
    <FeaturePageTemplate
      slug="ai-productivity-app-mac"
      title="AI Productivity App for Mac"
      tagline="System-Wide Keyboard Text Automation"
      description="Save 45+ minutes daily by refining text, code, emails, and notes in-place without opening web browsers."
      keyBenefits={[
        "Eliminates browser copy-pasting and context switching",
        "Tracks daily time saved and character count locally",
        "Runs quietly in the macOS menu bar tray"
      ]}
      workflowSteps={[
        { step: "1", title: "Highlight", desc: "Select text anywhere on Mac." },
        { step: "2", title: "Trigger", desc: "Press Option+Space." },
        { step: "3", title: "Automate", desc: "Text is replaced in ~100 ms." }
      ]}
      faqs={[]}
    />
  );
}
