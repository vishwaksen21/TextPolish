import { Metadata } from "next";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "Avelyn Product Roadmap (2026)",
  description: "Explore planned features for Avelyn: Windows/Linux builds, vision model support, and custom prompt library sharing.",
  alternates: { canonical: "https://avelyn.software/trust/roadmap" },
};

export default function RoadmapPage() {
  return (
    <div className="flex flex-col min-h-screen bg-white">
      <Navbar />
      <main className="flex-1 pt-32 pb-20 max-w-4xl w-full mx-auto px-6 space-y-8">
        <h1 className="text-4xl font-extrabold text-neutral-900 tracking-tight">Product Roadmap</h1>
        <div className="prose prose-purple max-w-none text-neutral-700 space-y-4">
          <h2>Q3 2026: Vision Support & Multi-Modal Prompts</h2>
          <p>Support for screenshot image context in Command Palette.</p>
          <h2>Q4 2026: Windows & Linux Builds</h2>
          <p>Cross-platform release previews for Windows 11 and Ubuntu.</p>
        </div>
      </main>
      <Footer />
    </div>
  );
}
