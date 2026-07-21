import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";

export const metadata: Metadata = {
  title: "Email Writing Mode Guide — Avelyn Documentation",
  description: "Draft crisp, persuasive emails from bullet points inside Mail or Outlook.",
  alternates: { canonical: "https://avelyn.software/docs/features/email-writing" },
};

export default function EmailWritingDoc() {
  return (
    <DocPageLayout
      categoryTitle="Core Features"
      categorySlug="features"
      itemSlug="email-writing"
      title="Email Writing Guide"
      description="Turn quick bullet notes into polished emails with subject lines and greetings."
    >
      <h2>Email Drafting Workflow</h2>
      <p>
        Highlight brief bullet points in Apple Mail, Outlook, or Superhuman, hit <code>Option+Space</code>, and select <strong>Email</strong> to generate structured messages.
      </p>
    </DocPageLayout>
  );
}
