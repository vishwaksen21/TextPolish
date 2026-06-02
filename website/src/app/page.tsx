import React from "react";
import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import FeaturesGrid from "@/components/FeaturesGrid";
import HowItWorks from "@/components/HowItWorks";
import ProductShowcase from "@/components/ProductShowcase";
import PrivacyFocus from "@/components/PrivacyFocus";
import FAQ from "@/components/FAQ";
import Testimonials from "@/components/Testimonials";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <div className="flex-1 flex flex-col min-h-screen bg-white">
      {/* Translucent floating Header */}
      <Navbar />

      {/* Hero Section containing Left Side CTA and Right Side Interactive settings card */}
      <Hero />

      {/* Main product show-off grid showcasing features & modes */}
      <FeaturesGrid />

      {/* Simplified horizontal storytelling timeline workflow */}
      <HowItWorks />

      {/* Grid of native macOS wizards & menu bar tray status screens */}
      <ProductShowcase />

      {/* High-trust local AI & privacy capability highlight */}
      <PrivacyFocus />

      {/* Accordion FAQ answers */}
      <FAQ />

      {/* Beta access registration & status cards */}
      <Testimonials />

      {/* Clean utility footer */}
      <Footer />
    </div>
  );
}
