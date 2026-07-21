import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Context Window Guide — Avelyn Documentation",
  description: "Manage memory and token budget allocations (2k / 4k / 8k tokens) for Apple Silicon Macs.",
  alternates: { canonical: "https://avelyn.software/docs/settings/context-window" },
};

export default function ContextWindowDoc() {
  return (
    <DocPageLayout
      categoryTitle="Settings & Configuration"
      categorySlug="settings"
      itemSlug="context-window"
      title="Context Window Management"
      description="Optimize memory and token context limits (2,048 – 8,192 tokens)."
    >
      <h2>Token Budgeting</h2>
      <p>Adjust context window caps (2,048, 4,096, 8,192 tokens) to balance RAM utilization and document size capacity.</p>
    </DocPageLayout>
  );
}
