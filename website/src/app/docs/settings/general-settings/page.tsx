import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "General Settings Guide — Avelyn Documentation",
  description: "Configure launch on startup, tray behavior, and auto-replace preferences.",
  alternates: { canonical: "https://avelyn.software/docs/settings/general-settings" },
};

export default function GeneralSettingsDoc() {
  return (
    <DocPageLayout
      categoryTitle="Settings & Configuration"
      categorySlug="settings"
      itemSlug="general-settings"
      title="General Settings Guide"
      description="Configure core application startup, menu bar behavior, and auto-replace rules."
    >
      <h2>Application Preferences</h2>
      <ul>
        <li><strong>Launch on Startup:</strong> Automatically start Avelyn when logging into macOS.</li>
        <li><strong>Auto-Replace Text:</strong> Instantly paste output upon generation completion.</li>
        <li><strong>Sound Notifications:</strong> Play subtle completion audio cues.</li>
      </ul>
    </DocPageLayout>
  );
}
