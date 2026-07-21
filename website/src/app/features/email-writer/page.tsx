import { Metadata } from "next";
import FeaturePageTemplate from "@/components/FeaturePageTemplate";

export const metadata: Metadata = {
  title: "AI Email Writer for Mac — Draft Executive Emails from Bullet Points",
  description: "Turn raw bullet notes into polished emails with professional greetings and subject lines inside Apple Mail or Outlook.",
  alternates: { canonical: "https://avelyn.software/features/email-writer" },
};

export default function EmailWriterPage() {
  return (
    <FeaturePageTemplate
      slug="email-writer"
      title="AI Email Writer for macOS"
      tagline="Draft Executive Emails from Bullet Points"
      description="Transform raw thoughts and rough notes into persuasive, structured business emails directly inside Apple Mail, Outlook, or Superhuman."
      keyBenefits={[
        "Formats emails complete with subject lines, salutations, and clear call-to-actions",
        "Adjusts tone instantly between formal, persuasive, and friendly",
        "Operates directly in your active email client window"
      ]}
      workflowSteps={[
        { step: "1", title: "Write Bullet Notes", desc: "Type raw thoughts in your email reply compose box." },
        { step: "2", title: "Press Hotkey", desc: "Hit Option+Space and select Email mode." },
        { step: "3", title: "Instant Polish", desc: "AI transforms bullets into a complete email." }
      ]}
      faqs={[
        {
          question: "Does Avelyn access my email inbox?",
          answer: "No. Avelyn only reads text that you explicitly highlight and activate."
        }
      ]}
    />
  );
}
