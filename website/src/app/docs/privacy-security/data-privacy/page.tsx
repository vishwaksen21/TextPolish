import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Data Privacy Architecture — Avelyn Documentation",
  description: "Learn how Avelyn enforces zero keylogging, zero telemetry, and local storage isolation.",
  alternates: { canonical: "https://avelyn.software/docs/privacy-security/data-privacy" },
};

export default function DataPrivacyDoc() {
  return (
    <DocPageLayout
      categoryTitle="Privacy & Security"
      categorySlug="privacy-security"
      itemSlug="data-privacy"
      title="Data Privacy Architecture"
      description="Zero telemetry, zero prompt storage, and isolated local config files."
    >
      <h2>Zero Telemetry Policy</h2>
      <p>Avelyn contains zero analytics code, zero tracking pixels, and zero phone-home routines. All settings reside locally at <code>~/.avelyn</code>.</p>
    </DocPageLayout>
  );
}
