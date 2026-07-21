import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Ollama Connection Issues — Avelyn Troubleshooting",
  description: "Resolving server port 11434, daemon startup errors, and local connection timeouts.",
  alternates: { canonical: "https://avelyn.software/docs/troubleshooting/ollama-connection-issues" },
};

export default function OllamaConnectionIssuesDoc() {
  return (
    <DocPageLayout
      categoryTitle="Troubleshooting"
      categorySlug="troubleshooting"
      itemSlug="ollama-connection-issues"
      title="Resolving Ollama Connection Issues"
      description="Fixing local host 11434 connection failures and server daemon errors."
    >
      <h2>Connection Error Diagnostics</h2>
      <p>If Avelyn reports "Cannot connect to Ollama at http://localhost:11434", follow these diagnostic steps:</p>
      <ol>
        <li>Check if Ollama daemon is running in Terminal: <code>ollama ps</code></li>
        <li>Manually start server daemon: <code>ollama serve</code></li>
        <li>Verify port availability: <code>curl http://localhost:11434</code></li>
      </ol>
    </DocPageLayout>
  );
}
