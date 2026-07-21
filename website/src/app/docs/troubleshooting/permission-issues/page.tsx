import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Permission Issues Guide — Avelyn Troubleshooting",
  description: "Resetting macOS Accessibility and Input Monitoring permissions after OS upgrades.",
  alternates: { canonical: "https://avelyn.software/docs/troubleshooting/permission-issues" },
};

export default function PermissionIssuesDoc() {
  return (
    <DocPageLayout
      categoryTitle="Troubleshooting"
      categorySlug="troubleshooting"
      itemSlug="permission-issues"
      title="Resetting macOS Accessibility Permissions"
      description="Fixing revoked Accessibility and Input Monitoring permissions."
    >
      <h2>Resetting TCC Authorizations</h2>
      <p>If Avelyn stops pasting after macOS updates, remove and re-add Avelyn in System Settings → Privacy &amp; Security → Accessibility.</p>
    </DocPageLayout>
  );
}
