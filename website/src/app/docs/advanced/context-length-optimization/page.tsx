import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Context Length Optimization — Avelyn Documentation",
  description: "Token budgeting strategies for low-memory Macs.",
  alternates: { canonical: "https://avelyn.software/docs/advanced/context-length-optimization" },
};

export default function ContextLengthOptimizationDoc() {
  return (
    <DocPageLayout
      categoryTitle="Advanced Customization"
      categorySlug="advanced"
      itemSlug="context-length-optimization"
      title="Context Length Optimization"
      description="Optimize token context budgets for low-memory Macs."
    >
      <h2>Token Optimization Strategies</h2>
      <p>Configure dynamic prompt truncation and token budgeting to prevent VRAM spikes on 8 GB RAM Macs.</p>
    </DocPageLayout>
  );
}
