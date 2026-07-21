import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Smart Router Guide — Avelyn Documentation",
  description: "Learn how Avelyn routes tasks dynamically to specialized providers (Coding, Writing, Reasoning, Voice, Privacy).",
  alternates: { canonical: "https://avelyn.software/docs/providers/smart-router" },
};

export default function SmartRouterDoc() {
  return (
    <DocPageLayout
      categoryTitle="AI Providers"
      categorySlug="providers"
      itemSlug="smart-router"
      title="Smart Router Guide"
      description="Map task categories to specialized providers for maximum output quality."
    >
      <h2>Task-Based Automatic Routing</h2>
      <p>Configure task group mappings to send Coding tasks to DeepSeek, Writing tasks to Gemini, and Privacy tasks to Local Ollama.</p>
    </DocPageLayout>
  );
}
