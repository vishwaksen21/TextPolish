export interface ComparisonFeature {
  feature: string;
  avelyn: boolean | string;
  competitor: boolean | string;
  detail: string;
}

export interface CompetitorComparison {
  name: string;
  slug: string;
  headline: string;
  description: string;
  metaTitle: string;
  metaDescription: string;
  pricingComparison: {
    avelyn: string;
    competitor: string;
  };
  features: ComparisonFeature[];
  strengths: {
    avelyn: string[];
    competitor: string[];
  };
  limitations: {
    avelyn: string[];
    competitor: string[];
  };
  useCases: {
    avelynBestFor: string[];
    competitorBestFor: string[];
  };
  faqs: { question: string; answer: string }[];
}

export const comparisonsData: Record<string, CompetitorComparison> = {
  "chatgpt": {
    name: "ChatGPT",
    slug: "avelyn-vs-chatgpt",
    headline: "Avelyn vs ChatGPT: System-Wide Local AI vs Browser Web Chat",
    description: "Compare Avelyn's native system-wide hotkey text replacement and local offline AI against ChatGPT's web browser interface.",
    metaTitle: "Avelyn vs ChatGPT Comparison (2026) — System-Wide vs Browser AI",
    metaDescription: "Detailed comparison of Avelyn vs ChatGPT. Discover why system-wide hotkeys, local offline Ollama execution, and zero telemetry beat browser copy-pasting.",
    pricingComparison: {
      avelyn: "100% Free for Local Offline AI · Pay-as-you-go for cloud API keys",
      competitor: "$20/month ChatGPT Plus subscription required for GPT-4o & Web search"
    },
    features: [
      { feature: "System-Wide Global Hotkey", avelyn: true, competitor: false, detail: "Avelyn operates in any Mac app; ChatGPT requires opening a browser tab." },
      { feature: "Instant In-Place Text Replacement", avelyn: true, competitor: false, detail: "Avelyn automatically replaces highlighted text via Cmd+V." },
      { feature: "100% Offline Local AI (Ollama)", avelyn: true, competitor: false, detail: "Avelyn runs Gemma 3 locally; ChatGPT requires active internet connection." },
      { feature: "Zero Telemetry & Prompt Logging", avelyn: true, competitor: false, detail: "Avelyn does not store or train on prompts; ChatGPT logs chats by default." },
      { feature: "Multi-Provider Smart Router", avelyn: true, competitor: false, detail: "Avelyn routes tasks across Ollama, Gemini, OpenRouter, and Custom APIs." },
      { feature: "API Key Ownership (BYO Key)", avelyn: true, competitor: false, detail: "Use your own API keys with raw provider pricing." }
    ],
    strengths: {
      avelyn: [
        "Native macOS performance with zero context switching",
        "100% offline local privacy with Ollama",
        "Works across Xcode, Mail, Slack, Pages, Notes, Terminal",
        "Dynamic Smart Router and Smart Fallback failover"
      ],
      competitor: [
        "Large web multimodal interface with DALL-E image generation",
        "Built-in web search browsing integration",
        "Pre-built GPT custom agent store"
      ]
    },
    limitations: {
      avelyn: [
        "Requires local download of models (~3-5 GB) for offline mode",
        "Focused exclusively on writing, prompt enhancement, and coding refinement"
      ],
      competitor: [
        "Requires manual copying and pasting between browser and apps",
        "Cloud-only: non-functional when offline",
        "Requires $20/mo subscription for premium models"
      ]
    },
    useCases: {
      avelynBestFor: [
        "Mac users who want to refine text inside daily work applications",
        "Developers, writers, and privacy-conscious professionals",
        "Air-gapped offline work environments"
      ],
      competitorBestFor: [
        "General web browsing search queries",
        "Generating synthetic image artwork via DALL-E",
        "Interactive conversational research"
      ]
    },
    faqs: [
      {
        question: "Can I use ChatGPT models inside Avelyn?",
        answer: "Yes! By entering your OpenRouter API key or OpenAI custom API key in Avelyn Settings, you can trigger GPT-4o and GPT-4o-mini directly via global hotkeys."
      },
      {
        question: "Is Avelyn faster than opening ChatGPT in Chrome?",
        answer: "Significantly faster. Avelyn eliminates opening browser tabs, navigating to chatgpt.com, pasting text, waiting for response, and copying back. Avelyn replaces text in ~100 ms."
      }
    ]
  },
  "grammarly": {
    name: "Grammarly",
    slug: "avelyn-vs-grammarly",
    headline: "Avelyn vs Grammarly: Neural AI System-Wide Refinement vs Cloud Grammar",
    description: "Compare Avelyn's privacy-first local neural LLMs against Grammarly's cloud grammar subscription widget.",
    metaTitle: "Avelyn vs Grammarly Comparison (2026) — Local AI vs Subscription Grammar",
    metaDescription: "Discover why Avelyn's local offline neural models, prompt enhancement, and customizable AI providers beat Grammarly's costly cloud subscriptions.",
    pricingComparison: {
      avelyn: "100% Free for Local Offline AI · Zero monthly subscription",
      competitor: "$12 - $30 per month per user subscription"
    },
    features: [
      { feature: "Neural Prompt & Text Refinement", avelyn: true, competitor: "Basic Grammar", detail: "Avelyn rewrites, summarizes, expands, and codes; Grammarly focuses on grammar rules." },
      { feature: "Local Offline AI Processing", avelyn: true, competitor: false, detail: "Avelyn runs 100% offline; Grammarly sends every keystroke to cloud servers." },
      { feature: "Zero Telemetry / Keylogging", avelyn: true, competitor: false, detail: "Avelyn only activates on hotkey press; Grammarly monitors background typing." },
      { feature: "Coding & Developer Mode", avelyn: true, competitor: false, detail: "Avelyn refactors code and adds docstrings; Grammarly does not support coding syntax." },
      { feature: "Multi-Language Translation (50+)", avelyn: true, competitor: false, detail: "Avelyn translates system-wide; Grammarly is English-focused." }
    ],
    strengths: {
      avelyn: [
        "100% free offline local processing with Ollama",
        "Full control over LLM choice (Gemma 3, Gemini, Claude, DeepSeek)",
        "Zero background keylogging or persistent cursor widgets",
        "Developer coding refactor support"
      ],
      competitor: [
        "Real-time passive typing underlined error indicators",
        "Built-in plagiarism detector for academic essays",
        "Team style guide policy enforcement"
      ]
    },
    limitations: {
      avelyn: [
        "Requires manual hotkey trigger rather than passive red underlines",
        "Optimized for macOS rather than browser extension fleets"
      ],
      competitor: [
        "Monitors all desktop keystrokes when active",
        "High recurring annual subscription costs",
        "Cannot run offline without internet connection"
      ]
    },
    useCases: {
      avelynBestFor: [
        "Privacy-conscious users who reject background keyloggers",
        "Developers and technical writers who need multi-language & code support",
        "Users looking for zero monthly subscription fees"
      ],
      competitorBestFor: [
        "Students needing basic spellcheck and plagiarism detection",
        "Corporate teams enforcing basic grammar style rules"
      ]
    },
    faqs: [
      {
        question: "Does Avelyn track my typing like Grammarly does?",
        answer: "No. Avelyn never tracks background typing. It only reads highlighted text when you explicitly trigger your hotkey."
      }
    ]
  },
  "gemini": {
    name: "Google Gemini",
    slug: "avelyn-vs-gemini",
    headline: "Avelyn vs Google Gemini: Desktop Hotkey Integration vs Web App",
    description: "Compare Avelyn's native macOS interface and hybrid local/cloud engine against Google Gemini Web.",
    metaTitle: "Avelyn vs Google Gemini (2026) — Mac Desktop Assistant vs Gemini Web",
    metaDescription: "Compare Avelyn and Google Gemini. See how Avelyn leverages Gemini Flash API inside native macOS apps while offering local offline Ollama fallbacks.",
    pricingComparison: {
      avelyn: "Free Local AI · Free/Pay-as-you-go Gemini Flash API key",
      competitor: "Free web version · $19.99/mo Gemini Advanced"
    },
    features: [
      { feature: "System-Wide Text Highlight Hotkey", avelyn: true, competitor: false, detail: "Avelyn activates inside Mail, Slack, and Xcode; Gemini requires web app." },
      { feature: "Local Offline Backup (Ollama)", avelyn: true, competitor: false, detail: "Avelyn falls back to offline Gemma 3 when internet drops." },
      { feature: "Gemini Flash API Integration", avelyn: true, competitor: true, detail: "Avelyn connects directly to Gemini Flash API with custom keys." },
      { feature: "Automatic Text Replacement", avelyn: true, competitor: false, detail: "Replaces highlighted text directly inside original application." }
    ],
    strengths: {
      avelyn: ["System-wide native hotkey", "Offline backup capability", "Multi-provider choice"],
      competitor: ["Deep Google Workspace web integrations", "Multimodal video analysis"]
    },
    limitations: {
      avelyn: ["Requires Mac desktop application"],
      competitor: ["Requires browser tab switching and copy-pasting"]
    },
    useCases: {
      avelynBestFor: ["Mac power users wanting Gemini speed inside native apps"],
      competitorBestFor: ["Google Docs web research"]
    },
    faqs: [
      {
        question: "Can I use Gemini Flash inside Avelyn?",
        answer: "Yes! Avelyn has native Google GenAI SDK integration. Input your Gemini API key in Settings for ultra-fast response streaming."
      }
    ]
  },
  "claude": {
    name: "Claude (Anthropic)",
    slug: "avelyn-vs-claude",
    headline: "Avelyn vs Claude: Desktop Workflow Automation vs Anthropic Web Chat",
    description: "Compare Avelyn's native hotkey text replacement with Claude 3.5 Sonnet / Haiku against the web interface.",
    metaTitle: "Avelyn vs Claude 3.5 (2026) — System-Wide Hotkey vs Claude Web",
    metaDescription: "Compare Avelyn and Anthropic Claude. Use Claude 3.5 Haiku system-wide in any Mac app with zero copy-pasting via Avelyn.",
    pricingComparison: {
      avelyn: "Free Local AI · Pay-as-you-go for Claude API via OpenRouter",
      competitor: "$20/month Claude Pro subscription"
    },
    features: [
      { feature: "System-Wide Global Hotkey", avelyn: true, competitor: false, detail: "Avelyn invokes Claude 3.5 in any app." },
      { feature: "Offline Fallback", avelyn: true, competitor: false, detail: "Falls back to local Ollama if offline." },
      { feature: "Claude 3.5 Haiku / Sonnet via API", avelyn: true, competitor: true, detail: "Use Claude models with exact API usage pricing." }
    ],
    strengths: {
      avelyn: ["System-wide text replacement", "Pay-as-you-go pricing instead of $20/mo", "Offline local fallback"],
      competitor: ["Web Artifacts preview pane"]
    },
    limitations: {
      avelyn: ["Requires OpenRouter API key for Claude access"],
      competitor: ["Web app only; requires manual copying and pasting"]
    },
    useCases: {
      avelynBestFor: ["Writers and developers wanting Claude quality directly inside Mac apps"],
      competitorBestFor: ["Web artifacts sandbox testing"]
    },
    faqs: [
      {
        question: "How do I access Claude 3.5 in Avelyn?",
        answer: "Add your OpenRouter API key in Settings → AI Provider and select Claude 3.5 Haiku or Sonnet as your provider model."
      }
    ]
  },
  "copilot": {
    name: "Microsoft Copilot",
    slug: "avelyn-vs-copilot",
    headline: "Avelyn vs Microsoft Copilot: Privacy-First Mac AI vs Enterprise Cloud",
    description: "Compare Avelyn's native Apple Silicon local AI against Microsoft Copilot's cloud-dependent suite.",
    metaTitle: "Avelyn vs Microsoft Copilot (2026) — Privacy Mac AI vs Copilot",
    metaDescription: "Detailed comparison between Avelyn and Microsoft Copilot. Learn why Avelyn's zero telemetry and local Ollama engine outperform Copilot for Mac users.",
    pricingComparison: {
      avelyn: "100% Free for Local Offline AI",
      competitor: "$30/user/month Microsoft 365 Copilot"
    },
    features: [
      { feature: "Local Offline Execution", avelyn: true, competitor: false, detail: "Avelyn runs offline; Copilot requires Azure cloud connection." },
      { feature: "Zero Corporate Telemetry", avelyn: true, competitor: false, detail: "Avelyn tracks zero telemetry." },
      { feature: "Works Outside Office Apps", avelyn: true, competitor: false, detail: "Avelyn works in all Mac apps, IDEs, and browsers." }
    ],
    strengths: {
      avelyn: ["Native macOS optimization", "100% offline privacy", "Works in any Mac application"],
      competitor: ["Deep Integration with Microsoft Office 365 apps"]
    },
    limitations: {
      avelyn: ["Focused on text, prompt, and code refinement"],
      competitor: ["High per-user monthly cost", "Cloud lock-in"]
    },
    useCases: {
      avelynBestFor: ["Mac power users, developers, and privacy-conscious professionals"],
      competitorBestFor: ["Dedicated Microsoft 365 enterprise organizations"]
    },
    faqs: [
      {
        question: "Does Avelyn require a Microsoft 365 subscription?",
        answer: "No. Avelyn is an independent native Mac application requiring no subscriptions."
      }
    ]
  },
  "notion-ai": {
    name: "Notion AI",
    slug: "avelyn-vs-notion-ai",
    headline: "Avelyn vs Notion AI: System-Wide Assistant vs Single-App Assistant",
    description: "Compare Avelyn's global system-wide capability against Notion AI's single-app limitation.",
    metaTitle: "Avelyn vs Notion AI (2026) — System-Wide Mac AI vs Notion Only",
    metaDescription: "Compare Avelyn and Notion AI. Discover why system-wide text enhancement across Mail, Xcode, Slack, and Safari beats single-app AI.",
    pricingComparison: {
      avelyn: "Free Local AI · Zero monthly subscription",
      competitor: "$10/user/month Notion AI add-on"
    },
    features: [
      { feature: "System-Wide Global Availability", avelyn: true, competitor: false, detail: "Avelyn works in all Mac apps; Notion AI only works inside Notion." },
      { feature: "Local Offline Processing", avelyn: true, competitor: false, detail: "Avelyn runs offline with Ollama." },
      { feature: "Developer Coding Assistant", avelyn: true, competitor: false, detail: "Refactors code inside IDEs." }
    ],
    strengths: {
      avelyn: ["Works across all apps on Mac", "100% offline local privacy", "No monthly add-on fee"],
      competitor: ["Integrated database property auto-fill in Notion"]
    },
    limitations: {
      avelyn: ["Not deeply tied to Notion database formulas"],
      competitor: ["Locked strictly inside the Notion workspace"]
    },
    useCases: {
      avelynBestFor: ["Users who write in multiple Mac applications"],
      competitorBestFor: ["Users living exclusively inside Notion"]
    },
    faqs: [
      {
        question: "Can I use Avelyn inside Notion?",
        answer: "Yes! Simply highlight text in Notion and trigger Avelyn's hotkey."
      }
    ]
  }
};
