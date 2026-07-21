import { Metadata } from "next";
import DocPageLayout from "@/components/DocPageLayout";
import SchemaMarkup from "@/components/SchemaMarkup";

export const metadata: Metadata = {
  title: "Prompt Enhancement Feature Guide — Avelyn Documentation",
  description: "Learn how Avelyn transforms brief 3-word user instructions into rich, structured system prompts system-wide.",
  alternates: { canonical: "https://avelyn.software/docs/features/prompt-enhancement" },
};

export default function PromptEnhancementDoc() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "name": "Prompt Enhancement Feature Guide",
    "headline": "Automatic System-Wide Prompt Tuning with Avelyn",
    "url": "https://avelyn.software/docs/features/prompt-enhancement",
  };

  return (
    <>
      <SchemaMarkup schema={schema} />
      <DocPageLayout
        categoryTitle="Core Features"
        categorySlug="features"
        itemSlug="prompt-enhancement"
        title="Prompt Enhancement Guide"
        description="Transform raw, ambiguous instructions into context-aware system prompts before sending them to LLM providers."
        relatedDocs={[
          { title: "Custom System Prompts", href: "/docs/advanced/custom-system-prompts", description: "Configuring system prompt templates." },
          { title: "Prompt Enhancer Tool Page", href: "/features/prompt-enhancer", description: "Overview of prompt tuning." }
        ]}
      >
        <h2>What is Prompt Enhancement?</h2>
        <p>
          Raw user prompts like <em>"make better"</em> or <em>"fix text"</em> often yield generic, conversational AI responses. Avelyn's <strong>Prompt Enhancer</strong> intercepts short user inputs and applies systemic prompt expansion rules—injecting output format constraints, tone specifications, and domain boundaries.
        </p>

        <h2>Before & After Comparison</h2>
        <h3>Before (Raw Input):</h3>
        <pre><code>rewrite this email to customer about delayed shipping</code></pre>

        <h3>After (Avelyn Enhanced Prompt):</h3>
        <pre><code>Act as an empathetic Customer Success Lead. Rewrite the user's text into a concise, polite email informing the client of a shipping delay. Maintain an apologetic tone, provide reassurance on tracking updates, preserve clear formatting, and output ONLY the final email body without conversational intro chatter.</code></pre>

        <h2>How to Activate Prompt Enhancement</h2>
        <ol>
          <li>Highlight your text in any macOS app.</li>
          <li>Press <code>Option+Space</code> to trigger the Command Palette.</li>
          <li>Select <strong>Enhance Prompt</strong> or type custom instructions into the prompt bar.</li>
        </ol>
      </DocPageLayout>
    </>
  );
}