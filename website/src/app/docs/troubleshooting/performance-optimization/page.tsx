import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Performance Optimization Guide — Avelyn Troubleshooting",
  description: "Eliminate latency spikes, warm GPU idle routines, and optimize token throughput.",
  alternates: { canonical: "https://avelyn.software/docs/troubleshooting/performance-optimization" },
};

export default function PerformanceOptimizationDoc() {
  return (
    <DocPageLayout
      categoryTitle="Troubleshooting"
      categorySlug="troubleshooting"
      itemSlug="performance-optimization"
      title="Performance Optimization Guide"
      description="Eliminating latency spikes and warming Apple Silicon GPU compute blocks."
    >
      <h2>GPU Idle Sleep Prevention</h2>
      <p>Avelyn's background keep-alive timer sends a 1-token request every 120s to prevent M-series GPU idle sleep, keeping TTFT under 0.5 seconds.</p>
    </DocPageLayout>
  );
}
