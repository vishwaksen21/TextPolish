import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Offline Mode Guide — Avelyn Documentation",
  description: "Air-gapped operation for confidential enterprise work with zero internet connectivity required.",
  alternates: { canonical: "https://avelyn.software/docs/privacy-security/offline-mode" },
};

export default function OfflineModeDoc() {
  return (
    <DocPageLayout
      categoryTitle="Privacy & Security"
      categorySlug="privacy-security"
      itemSlug="offline-mode"
      title="Offline Air-Gapped Operation"
      description="Run Avelyn during flights, off-grid travel, or air-gapped corporate networks."
    >
      <h2>Air-Gapped Operation</h2>
      <p>In Offline Mode, Avelyn disables all network socket calls, functioning 100% locally via local IPC calls to Ollama.</p>
    </DocPageLayout>
  );
}
