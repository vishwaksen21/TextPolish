import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Hotkey Configuration Guide — Avelyn Documentation",
  description: "Customize global keyboard shortcuts and push-to-talk voice triggers.",
  alternates: { canonical: "https://avelyn.software/docs/settings/hotkey-configuration" },
};

export default function HotkeyConfigurationDoc() {
  return (
    <DocPageLayout
      categoryTitle="Settings & Configuration"
      categorySlug="settings"
      itemSlug="hotkey-configuration"
      title="Hotkey Configuration Guide"
      description="Customize global trigger shortcuts and Push-to-Talk key combinations."
    >
      <h2>Global Trigger Shortcut</h2>
      <p>Configure your preferred global shortcut in Settings → Hotkeys (Default: <code>Option+Space</code>).</p>
    </DocPageLayout>
  );
}
