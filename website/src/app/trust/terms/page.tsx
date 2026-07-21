import { Metadata } from "next";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "Terms of Service — Avelyn",
  description: "Terms of Service governing the use of Avelyn software and documentation.",
  alternates: { canonical: "https://avelyn.software/trust/terms" },
};

export default function TermsPage() {
  return (
    <div className="flex flex-col min-h-screen bg-white">
      <Navbar />
      <main className="flex-1 pt-32 pb-20 max-w-4xl w-full mx-auto px-6 space-y-8">
        <h1 className="text-4xl font-extrabold text-neutral-900 tracking-tight">Terms of Service</h1>
        <div className="prose prose-purple max-w-none text-neutral-700 space-y-4">
          <p>By using Avelyn, you agree to these terms. Avelyn is provided "as is" without warranty. Users retain full ownership of all generated text.</p>
        </div>
      </main>
      <Footer />
    </div>
  );
}
