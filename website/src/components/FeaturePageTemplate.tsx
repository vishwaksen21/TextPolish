import React from "react";
import Metadata from "next";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Breadcrumbs from "@/components/Breadcrumbs";
import RelatedLinks, { LinkItem } from "@/components/RelatedLinks";
import SchemaMarkup from "@/components/SchemaMarkup";
import { Sparkles, CheckCircle2, ArrowRight, Shield, Zap } from "lucide-react";

export interface FeaturePageProps {
  slug: string;
  title: string;
  tagline: string;
  description: string;
  keyBenefits: string[];
  workflowSteps: { step: string; title: string; desc: string }[];
  faqs: { question: string; answer: string }[];
  relatedDocs?: LinkItem[];
}

export default function FeaturePageTemplate({
  slug,
  title,
  tagline,
  description,
  keyBenefits,
  workflowSteps,
  faqs,
  relatedDocs = [],
}: FeaturePageProps) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": `Avelyn — ${title}`,
    "applicationCategory": "ProductivityApplication",
    "operatingSystem": "macOS",
    "description": description,
    "url": `https://avelyn.software/features/${slug}`
  };

  const breadcrumbs = [
    { label: "Features", href: "/features" },
    { label: title }
  ];

  return (
    <div className="flex flex-col min-h-screen bg-white">
      <SchemaMarkup schema={schema} />
      <Navbar />

      <main className="flex-1 pt-28 sm:pt-32 pb-16 sm:pb-20 max-w-[1200px] w-full mx-auto px-4 sm:px-6">
        <Breadcrumbs items={breadcrumbs} />

        {/* Hero Section */}
        <section className="relative p-6 sm:p-8 md:p-14 rounded-3xl bg-gradient-to-br from-neutral-900 via-neutral-950 to-[#120B2E] text-white overflow-hidden shadow-2xl mb-12 sm:mb-16">
          <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-[#7C3AED]/20 blur-[150px] rounded-full pointer-events-none" />
          
          <div className="relative z-10 max-w-3xl space-y-4 sm:space-y-6">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-xs font-semibold text-purple-300">
              <Sparkles className="w-3.5 h-3.5" />
              <span>{tagline}</span>
            </div>

            <h1 className="text-3xl sm:text-4xl md:text-6xl font-extrabold tracking-tight text-white leading-tight">
              {title}
            </h1>

            <p className="text-base sm:text-lg md:text-xl text-neutral-300 leading-relaxed">
              {description}
            </p>

            <div className="pt-2 sm:pt-4 flex flex-wrap gap-3 sm:gap-4">
              <Link
                href="/#beta"
                className="inline-flex items-center justify-center px-5 sm:px-6 py-3 rounded-full bg-[#7C3AED] text-white text-sm sm:text-base font-bold hover:bg-[#6D28D9] transition-all shadow-lg hover:scale-[1.02] w-full sm:w-auto text-center"
              >
                Try {title} Free
                <ArrowRight className="w-4 h-4 ml-2" />
              </Link>
              <Link
                href="/docs"
                className="inline-flex items-center justify-center px-5 sm:px-6 py-3 rounded-full bg-white/10 text-white text-sm sm:text-base font-semibold hover:bg-white/20 transition-all border border-white/10 w-full sm:w-auto text-center"
              >
                View Documentation
              </Link>
            </div>
          </div>
        </section>

        {/* Key Benefits Grid */}
        <section className="mb-12 sm:mb-16 space-y-6 sm:space-y-8" aria-label="Key Benefits">
          <div className="text-center max-w-2xl mx-auto">
            <h2 className="text-2xl sm:text-3xl font-extrabold text-neutral-900">Why Use {title}?</h2>
            <p className="text-sm sm:text-base text-neutral-600 mt-2">Designed for maximum speed, system-wide availability, and complete privacy.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6">
            {keyBenefits.map((benefit, idx) => (
              <div key={idx} className="p-5 sm:p-6 rounded-2xl border border-neutral-200/80 bg-white shadow-sm flex items-start space-x-3">
                <CheckCircle2 className="w-5 h-5 text-[#7C3AED] flex-shrink-0 mt-0.5" />
                <span className="text-sm font-semibold text-neutral-800 leading-relaxed">{benefit}</span>
              </div>
            ))}
          </div>
        </section>

        {/* Workflow Timeline */}
        <section className="mb-12 sm:mb-16 p-6 sm:p-8 md:p-12 rounded-3xl bg-neutral-50 border border-neutral-200/80 space-y-6 sm:space-y-8" aria-label="Workflow Steps">
          <div className="text-center max-w-2xl mx-auto">
            <h2 className="text-2xl sm:text-3xl font-extrabold text-neutral-900">How It Works</h2>
            <p className="text-sm sm:text-base text-neutral-600 mt-2">3 steps to instant text refinement in any application.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
            {workflowSteps.map((step, idx) => (
              <div key={idx} className="relative p-5 sm:p-6 rounded-2xl bg-white border border-neutral-200 shadow-sm space-y-3">
                <span className="inline-block px-3 py-1 rounded-full bg-purple-100 text-[#7C3AED] text-xs font-bold">
                  Step {step.step}
                </span>
                <h3 className="text-base sm:text-lg font-bold text-neutral-900">{step.title}</h3>
                <p className="text-sm text-neutral-600 leading-relaxed">{step.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* FAQs */}
        {faqs.length > 0 && (
          <section className="mb-12 sm:mb-16 space-y-4 sm:space-y-6" aria-label="Feature FAQs">
            <h2 className="text-xl sm:text-2xl font-bold text-neutral-900">Frequently Asked Questions</h2>
            <div className="space-y-3 sm:space-y-4">
              {faqs.map((faq, idx) => (
                <div key={idx} className="p-5 sm:p-6 rounded-2xl border border-neutral-200/80 bg-white shadow-sm">
                  <h3 className="text-base font-bold text-neutral-900">{faq.question}</h3>
                  <p className="text-sm text-neutral-600 mt-2 leading-relaxed">{faq.answer}</p>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Related Links */}
        <RelatedLinks docs={relatedDocs} />
      </main>

      <Footer />
    </div>
  );
}
