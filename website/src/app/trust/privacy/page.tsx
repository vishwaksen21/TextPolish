import { Metadata } from "next";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "Privacy Policy — Avelyn",
  description: "Avelyn Privacy Policy: zero telemetry, zero analytics tracking, and local prompt processing.",
  alternates: { canonical: "https://avelyn.software/trust/privacy" },
};

export default function PrivacyPolicyPage() {
  return (
    <div className="flex flex-col min-h-screen bg-white">
      <Navbar />
      <main className="flex-1 pt-32 pb-20 max-w-4xl w-full mx-auto px-6 space-y-8">
        <h1 className="text-4xl font-extrabold text-neutral-900 tracking-tight">Privacy Policy</h1>
        <div className="prose prose-purple max-w-none text-neutral-700 space-y-4">
          <p>Effective Date: July 2026</p>
          <h2>1. Zero Telemetry & Analytics</h2>
          <p>Avelyn collects zero usage telemetry, zero analytics scripts, and zero prompt logs. We do not track your keystrokes, highlighted text, or active applications.</p>
          <h2>2. Local Execution Boundary</h2>
          <p>In Local AI mode, 100% of data processing occurs on your device via Ollama. No data is transmitted over external networks.</p>
          <h2>3. API Keys & Cloud Processing</h2>
          <p>When using OpenRouter or Gemini cloud providers, requests connect directly to provider API endpoints using your personal keys. Keys are stored locally at <code>~/.avelyn</code> and masked in the UI.</p>
        </div>
      </main>
      <Footer />
    </div>
  );
}
