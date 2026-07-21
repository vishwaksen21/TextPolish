import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";
import SchemaMarkup from "@/components/SchemaMarkup";

export const metadata: Metadata = {
  title: "Permissions Setup Guide — Accessibility & Input Monitoring",
  description: "Learn how to configure macOS Accessibility and Input Monitoring permissions so Avelyn can capture text and auto-paste suggestions.",
  alternates: { canonical: "https://avelyn.software/docs/getting-started/permissions-setup" },
};

export default function PermissionsSetupDoc() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "name": "macOS Permissions Setup Guide for Avelyn",
    "headline": "Configuring TCC Permissions on macOS",
    "url": "https://avelyn.software/docs/getting-started/permissions-setup",
  };

  return (
    <>
      <SchemaMarkup schema={schema} />
      <DocPageLayout
        categoryTitle="Getting Started"
        categorySlug="getting-started"
        itemSlug="permissions-setup"
        title="macOS Permissions Setup Guide"
        description="Granting Accessibility and Input Monitoring permissions to enable global text replacement."
        relatedDocs={[
          { title: "Installation Guide", href: "/docs/getting-started/installation", description: "Downloading and placing DMG in Applications." },
          { title: "Quick Start Guide", href: "/docs/getting-started/quick-start", description: "Mastering double-tap hotkey triggers." }
        ]}
      >
        <h2>Why Avelyn Needs macOS Permissions</h2>
        <p>
          Avelyn is a privacy-first system-wide application. To refine highlighted text inside external applications (Chrome, Xcode, Slack, Apple Notes, Mail) without requiring individual browser extensions or IDE plugins, macOS requires explicit security authorization under Transparency, Consent, and Control (TCC).
        </p>

        <h2>1. Accessibility Permission</h2>
        <p>
          <strong>Purpose:</strong> Allows Avelyn to read the highlighted text in the currently active window and execute synthetic <code>Cmd+V</code> paste events to replace original text seamlessly.
        </p>

        <h3>How to Enable Accessibility:</h3>
        <ol>
          <li>Open <strong>System Settings</strong> on your Mac.</li>
          <li>Navigate to <strong>Privacy & Security → Accessibility</strong>.</li>
          <li>Click the <strong>+ (Plus)</strong> button or toggle the switch next to <strong>Avelyn</strong> to <code>ON</code>.</li>
          <li>If prompted, enter your Mac administrator password.</li>
        </ol>

        <h2>2. Input Monitoring Permission</h2>
        <p>
          <strong>Purpose:</strong> Allows Avelyn to listen for your global trigger shortcut (e.g., <code>Option+Space</code>) while running in the background menu bar tray.
        </p>

        <h3>How to Enable Input Monitoring:</h3>
        <ol>
          <li>Open <strong>System Settings</strong>.</li>
          <li>Navigate to <strong>Privacy & Security → Input Monitoring</strong>.</li>
          <li>Ensure the toggle switch next to <strong>Avelyn</strong> is set to <code>ON</code>.</li>
        </ol>

        <h2>Troubleshooting Revoked Permissions</h2>
        <p>
          If Avelyn stops replacing text after updating macOS, Apple security policies may have invalidated the old app signature hash.
        </p>
        <p><strong>To fix:</strong> Open System Settings → Accessibility, select Avelyn, click the <code>-</code> (Minus) button to remove the old entry, then re-add Avelyn from your <code>/Applications</code> folder.
        </p>
      </DocPageLayout>
    </>
  );
}