import { Metadata } from "next";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "Release Notes — Avelyn",
  description: "Official release notes and changelog for Avelyn releases.",
  alternates: { canonical: "https://avelyn.software/trust/release-notes" },
};

export default function ReleaseNotesPage() {
  return (
    <div className="flex flex-col min-h-screen bg-white">
      <Navbar />
      <main className="flex-1 pt-32 pb-20 max-w-4xl w-full mx-auto px-6 space-y-8">
        <h1 className="text-4xl font-extrabold text-neutral-900 tracking-tight">Release Notes</h1>
        <div className="prose prose-purple max-w-none text-neutral-700 space-y-4">
          <h2>v2.1.4</h2>
          <p>Integrated Google GenAI SDK, password masking, and Smart Router task groups.</p>
        </div>
      </main>
      <Footer />
    </div>
  );
}
