import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";
import SchemaMarkup from "@/components/SchemaMarkup";

export const metadata: Metadata = {
  title: "First Launch & Setup Wizard — Avelyn Documentation",
  description: "Walkthrough of Avelyn's first launch wizard, automatic Ollama installation, initial model pull, and system tray setup.",
  alternates: { canonical: "https://avelyn.software/docs/getting-started/first-launch" },
};

export default function FirstLaunchDoc() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "name": "First Launch & Setup Wizard Guide",
    "headline": "Configuring Avelyn on First Launch",
    "url": "https://avelyn.software/docs/getting-started/first-launch",
  };

  return (
    <>
      <SchemaMarkup schema={schema} />
      <DocPageLayout
        categoryTitle="Getting Started"
        categorySlug="getting-started"
        itemSlug="first-launch"
        title="First Launch & Onboarding Setup"
        description="Configure your initial AI provider, run the automatic installer overlay, and learn menu bar tray interactions."
        relatedDocs={[
          { title: "Permissions Setup", href: "/docs/getting-started/permissions-setup", description: "Granting system replacement permissions." },
          { title: "Ollama Integration", href: "/docs/providers/ollama-integration", description: "Local offline LLM setup." }
        ]}
      >
        <h2>Initial Onboarding Wizard</h2>
        <p>
          When launching Avelyn for the first time, an onboarding window appears to help you set up your core preferences.
        </p>

        <h3>Automatic Ollama Auto-Installer</h3>
        <p>
          If Avelyn detects that Local Ollama is not yet installed on your Mac, a full-screen background worker automatically:
        </p>
        <ol>
          <li>Downloads the official Ollama binary.</li>
          <li>Starts the local background server daemon on port 11434.</li>
          <li>Pulls the default recommended <strong>Gemma 3 4B</strong> model weights.</li>
        </ol>

        <h2>System Tray Icon Behavior</h2>
        <p>
          Avelyn runs quietly in your macOS Menu Bar (system tray). Clicking the tray icon opens a menu with quick actions:
        </p>
        <ul>
          <li><strong>Open Settings:</strong> Adjust hotkeys, AI providers, and model parameters.</li>
          <li><strong>Pause/Resume Listener:</strong> Temporarily disable global hotkey capture.</li>
          <li><strong>View Productivity Metrics:</strong> Inspect total words refined and estimated time saved.</li>
          <li><strong>Quit Avelyn:</strong> Cleanly terminate background threads and restore your clipboard.</li>
        </ul>

        <h2>Choosing Your Starting Provider Mode</h2>
        <p>During setup, select your preferred operating mode:</p>
        <ul>
          <li><strong>Local AI Mode (Default):</strong> 100% offline using Ollama with zero cloud telemetry.</li>
          <li><strong>Avelyn Cloud (OpenRouter):</strong> Enter your OpenRouter API key for GPT-4o, DeepSeek V3, or Claude 3.5.</li>
          <li><strong>Google Gemini Flash:</strong> Enter your free Google AI Studio key for high-speed streaming.</li>
          <li><strong>Smart Router:</strong> Automatically select providers based on task type.</li>
        </ul>
      </DocPageLayout>
    </>
  );
}