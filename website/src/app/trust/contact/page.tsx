import { Metadata } from "next";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "Contact Us — Avelyn",
  description: "Get in touch with the Avelyn engineering and support team.",
  alternates: { canonical: "https://avelyn.software/trust/contact" },
};

export default function ContactPage() {
  return (
    <div className="flex flex-col min-h-screen bg-white">
      <Navbar />
      <main className="flex-1 pt-32 pb-20 max-w-4xl w-full mx-auto px-6 space-y-8">
        <h1 className="text-4xl font-extrabold text-neutral-900 tracking-tight">Contact & Support</h1>
        <div className="prose prose-purple max-w-none text-neutral-700 space-y-4">
          <p>Email support: <code>chilukurvishwak21@gmail.com</code></p>
          <p>GitHub Repository: <code>github.com/vishwaksen21/Avelyn</code></p>
        </div>
      </main>
      <Footer />
    </div>
  );
}
