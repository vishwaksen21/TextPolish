import { Metadata } from "next";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "Security & API Key Safety — Avelyn",
  description: "Learn about Avelyn's security architecture, API key obfuscation, and notarization.",
  alternates: { canonical: "https://avelyn.software/trust/security" },
};

export default function SecurityPage() {
  return (
    <div className="flex flex-col min-h-screen bg-white">
      <Navbar />
      <main className="flex-1 pt-32 pb-20 max-w-4xl w-full mx-auto px-6 space-y-8">
        <h1 className="text-4xl font-extrabold text-neutral-900 tracking-tight">Security & API Key Architecture</h1>
        <div className="prose prose-purple max-w-none text-neutral-700 space-y-4">
          <h2>Apple Notarization & Code Signing</h2>
          <p>Avelyn binaries are signed with Apple Developer ID certificates and notarized by Apple Gatekeeper servers.</p>
          <h2>API Key Obfuscation</h2>
          <p>Keys are stored in user-restricted application storage (`~/.avelyn`) and masked with password bullets in the GUI.</p>
        </div>
      </main>
      <Footer />
    </div>
  );
}
