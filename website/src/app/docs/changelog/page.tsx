import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Avelyn Release Notes & Changelog — Version History",
  description: "Explore version history, bug fixes, performance improvements, and feature updates in Avelyn.",
  alternates: { canonical: "https://avelyn.software/docs/changelog" },
};

export default function ChangelogDoc() {
  return (
    <DocPageLayout
      categoryTitle="Changelog & Releases"
      categorySlug="changelog"
      itemSlug="changelog"
      title="Avelyn Release Notes & Changelog"
      description="Track feature updates, provider improvements, and macOS Sequoia performance updates."
    >
      <h2>Version 2.1.4 (Latest Release)</h2>
      <ul>
        <li><strong>Google Gemini Flash SDK:</strong> Integrated official <code>google-genai</code> Python library for low-latency streaming.</li>
        <li><strong>Smart Router Task Groups:</strong> Mapped task groups (Coding, Writing, Reasoning, Voice, Privacy) to customizable provider pairs.</li>
        <li><strong>Password Bullet Masking:</strong> Obfuscated API keys in Settings panels to prevent exposure during screen shares.</li>
        <li><strong>GPU Keep-Alive Timer:</strong> Implemented 120s 1-token ping to prevent Apple Silicon GPU compute sleep.</li>
      </ul>

      <h2>Version 2.0.0</h2>
      <ul>
        <li>Added multi-provider architecture (Ollama, OpenRouter, Custom OpenAI API).</li>
        <li>Introduced Command Palette with animated preset buttons.</li>
      </ul>
    </DocPageLayout>
  );
}
