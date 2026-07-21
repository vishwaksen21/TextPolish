import { Metadata } from "next";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "Media Kit & Assets — Avelyn",
  description: "Download official Avelyn logos, screenshots, brand guidelines, and press assets.",
  alternates: { canonical: "https://avelyn.software/trust/media-kit" },
};

export default function MediaKitPage() {
  return (
    <div className="flex flex-col min-h-screen bg-white">
      <Navbar />
      <main className="flex-1 pt-32 pb-20 max-w-4xl w-full mx-auto px-6 space-y-8">
        <h1 className="text-4xl font-extrabold text-neutral-900 tracking-tight">Media Kit & Press Assets</h1>
        <div className="prose prose-purple max-w-none text-neutral-700 space-y-4">
          <p>Official logos, screenshots, and product descriptions for press and media reviews.</p>
        </div>
      </main>
      <Footer />
    </div>
  );
}
