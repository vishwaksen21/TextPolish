import { Metadata } from "next";
import FeaturePageTemplate from "@/components/FeaturePageTemplate";

export const metadata: Metadata = {
  title: "AI Email Writer for Mac — Draft Executive Emails in Seconds",
  description: "Turn raw bullet notes into structured business emails directly inside Apple Mail or Outlook.",
  alternates: { canonical: "https://avelyn.software/solutions/ai-email-writer-mac" },
};

export default function AIEmailWriterMacSolution() {
  return (
    <FeaturePageTemplate
      slug="ai-email-writer-mac"
      title="AI Email Writer for Mac"
      tagline="Draft Executive Emails from Bullet Points"
      description="Turn quick bullet notes into polished emails with subject lines and salutations inside Apple Mail or Outlook."
      keyBenefits={[
        "Operates directly inside Mail, Outlook, and Superhuman",
        "Adjusts tone between formal, persuasive, and friendly",
        "Zero data retention or email inbox scraping"
      ]}
      workflowSteps={[
        { step: "1", title: "Write Bullets", desc: "Type raw thoughts in email compose box." },
        { step: "2", title: "Press Hotkey", desc: "Trigger Option+Space and select Email." },
        { step: "3", title: "Instant Polish", desc: "AI formats complete email body." }
      ]}
      faqs={[]}
    />
  );
}
