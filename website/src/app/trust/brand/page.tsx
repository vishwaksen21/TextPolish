import { Metadata } from "next";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "Brand Guidelines — Avelyn",
  description: "Official typography, color palette (#7C3AED), and logo usage rules for Avelyn.",
  alternates: { canonical: "https://avelyn.software/trust/brand" },
};

export default function BrandPage() {
  return (
    <div className="flex flex-col min-h-screen bg-white">
      <Navbar />
      <main className="flex-1 pt-32 pb-20 max-w-4xl w-full mx-auto px-6 space-y-8">
        <h1 className="text-4xl font-extrabold text-neutral-900 tracking-tight">Brand Guidelines</h1>
        <div className="prose prose-purple max-w-none text-neutral-700 space-y-4">
          <p>Primary Color Accent: <code>#7C3AED</code> (Purple / Violet)</p>
          <p>Fonts: Geist Sans and Geist Mono</p>
        </div>
      </main>
      <Footer />
    </div>
  );
}
