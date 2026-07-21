import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";
import SchemaMarkup from "@/components/SchemaMarkup";

export const metadata: Metadata = {
  title: "Avelyn Installation Guide — Download & Setup for macOS",
  description: "Learn how to download the Avelyn DMG installer, verify checksums, install on Apple Silicon or Intel Macs, and complete initial setup.",
  alternates: { canonical: "https://avelyn.software/docs/getting-started/installation" },
};

export default function InstallationDoc() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "name": "Avelyn Installation Guide for macOS",
    "headline": "Installing Avelyn on macOS Sequoia & Sonoma",
    "url": "https://avelyn.software/docs/getting-started/installation",
  };

  return (
    <>
      <SchemaMarkup schema={schema} />
      <DocPageLayout
        categoryTitle="Getting Started"
        categorySlug="getting-started"
        itemSlug="installation"
        title="Installation Guide for macOS"
        description="Download, install, and verify Avelyn on Apple Silicon (M1/M2/M3/M4) and Intel Macs."
        relatedDocs={[
          { title: "First Launch Walkthrough", href: "/docs/getting-started/first-launch", description: "Configuring default AI providers." },
          { title: "Permissions Setup", href: "/docs/getting-started/permissions-setup", description: "Granting Accessibility rights." }
        ]}
      >
        <h2>System Requirements</h2>
        <ul>
          <li><strong>Operating System:</strong> macOS Sonoma 14.0 or macOS Sequoia 15.0+</li>
          <li><strong>Architecture:</strong> Apple Silicon (M1/M2/M3/M4) recommended; Intel Macs fully supported.</li>
          <li><strong>Memory:</strong> 8 GB RAM minimum (16 GB+ recommended for running 7B local Ollama models).</li>
          <li><strong>Storage:</strong> 150 MB for the core Avelyn app; 3–5 GB optional disk space for local LLM weights.</li>
        </ul>

        <h2>Step-by-Step Installation</h2>
        <ol>
          <li>
            <strong>Download DMG:</strong> Download the latest <code>.dmg</code> installer from the official website or GitHub Releases repository.
          </li>
          <li>
            <strong>Open Disk Image:</strong> Double-click <code>Avelyn-v2.1.dmg</code> to mount the volume.
          </li>
          <li>
            <strong>Drag to Applications:</strong> Drag the Avelyn icon into your macOS <code>/Applications</code> directory.
          </li>
          <li>
            <strong>Launch Avelyn:</strong> Open Avelyn from Launchpad or Spotlight (<code>Cmd+Space</code>).
          </li>
        </ol>

        <h2>Verifying Download Checksums</h2>
        <p>
          For security-conscious environments, verify the integrity of the downloaded installer using terminal SHA-256 validation:
        </p>
        <pre><code>shasum -a 256 Avelyn-v2.1.dmg</code></pre>
        <p>Compare the output against the published checksum hash on our GitHub Releases page.</p>

        <h2>Homebrew Installation</h2>
        <p>You can also install and update Avelyn using Homebrew Cask:</p>
        <pre><code>brew install --cask avelyn</code></pre>

        <h2>Next Steps</h2>
        <p>
          Proceed to the <a href="/docs/getting-started/permissions-setup">Permissions Setup guide</a> to grant Accessibility and Input Monitoring rights required for global hotkey text replacement.
        </p>
      </DocPageLayout>
    </>
  );
}