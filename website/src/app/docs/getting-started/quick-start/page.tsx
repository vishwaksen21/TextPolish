import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";
import SchemaMarkup from "@/components/SchemaMarkup";

export const metadata: Metadata = {
  title: "Quick Start Guide — Avelyn Documentation",
  description: "Master Avelyn in 5 minutes: trigger global hotkeys, refine highlighted text, switch modes, and configure auto-replacement.",
  alternates: { canonical: "https://avelyn.software/docs/getting-started/quick-start" },
};

export default function QuickStartDoc() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "name": "Quick Start Guide for Avelyn",
    "headline": "Getting Productive in 5 Minutes with Avelyn",
    "url": "https://avelyn.software/docs/getting-started/quick-start",
  };

  return (
    <>
      <SchemaMarkup schema={schema} />
      <DocPageLayout
        categoryTitle="Getting Started"
        categorySlug="getting-started"
        itemSlug="quick-start"
        title="Quick Start Guide"
        description="Learn the 3-step workflow to enhance text anywhere on macOS in under 5 seconds."
        relatedDocs={[
          { title: "Prompt Enhancement", href: "/docs/features/prompt-enhancement", description: "Learn how prompt tuning works." },
          { title: "Hotkey Configuration", href: "/docs/settings/hotkey-configuration", description: "Customizing keyboard shortcuts." }
        ]}
      >
        <h2>The 3-Step Core Workflow</h2>

        <h3>Step 1: Highlight Text Anywhere</h3>
        <p>
          Select text inside any active macOS application—such as an email draft in Mail, a pull request comment on GitHub, a function in VS Code, or notes in Notion.
        </p>

        <h3>Step 2: Trigger Global Hotkey</h3>
        <p>
          Press your global shortcut (Default: <code>Option+Space</code> or <code>Double-Tap Option</code>). The Command Palette overlay instantly opens centered on your active screen display.
        </p>

        <h3>Step 3: Select Action or Type Instruction</h3>
        <p>
          Click one of the preset mode buttons (e.g., <strong>Grammar</strong>, <strong>Professional</strong>, <strong>Email</strong>, <strong>Code</strong>) or type a custom instruction (e.g., <em>"Make this sound energetic and bulleted"</em>).
        </p>

        <h2>Auto-Replace vs. Preview Mode</h2>
        <ul>
          <li><strong>Auto-Replace (Enabled by default):</strong> As soon as generation finishes, Avelyn writes the result to the clipboard and pastes it over your highlighted text automatically.</li>
          <li><strong>Preview Mode:</strong> Displays a popover window showing the refined text, allowing you to review, copy, or edit before accepting.</li>
        </ul>

        <h2>Canceling Mid-Stream</h2>
        <p>
          If you start an AI generation by accident, press <code>Escape</code> or click the cancel button in the Command Palette to stop the stream immediately.
        </p>
      </DocPageLayout>
    </>
  );
}
