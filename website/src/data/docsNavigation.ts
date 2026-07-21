export interface DocItem {
  title: string;
  slug: string;
  description?: string;
}

export interface DocCategory {
  title: string;
  slug: string;
  items: DocItem[];
}

export const docCategories: DocCategory[] = [
  {
    title: "Getting Started",
    slug: "getting-started",
    items: [
      { title: "Installation", slug: "installation", description: "Download, verify DMG, and install Avelyn on macOS." },
      { title: "First Launch", slug: "first-launch", description: "Initial setup wizard and model configuration." },
      { title: "Permissions Setup", slug: "permissions-setup", description: "Granting macOS Accessibility and Input Monitoring permissions." },
      { title: "Quick Start Guide", slug: "quick-start", description: "Mastering the double-tap shortcut and basic text replacement." },
    ],
  },
  {
    title: "Core Features",
    slug: "features",
    items: [
      { title: "Prompt Enhancement", slug: "prompt-enhancement", description: "Automatically refine vague queries into high-precision prompts." },
      { title: "Grammar Correction", slug: "grammar-correction", description: "Instant rule-based and neural grammar and syntax fixing." },
      { title: "Professional Writing", slug: "professional-writing", description: "Elevate tone, clarity, and phrasing for executive communication." },
      { title: "Email Writing", slug: "email-writing", description: "Draft crisp, persuasive emails directly inside Mail or Outlook." },
      { title: "AI Rewrite", slug: "ai-rewrite", description: "Paraphrase, rephrase, expand, or condense highlighted text." },
      { title: "Translation", slug: "translation", description: "Translate between 50+ languages system-wide without tab-switching." },
      { title: "Summarization", slug: "summarization", description: "Condense long articles, PDFs, and meeting notes into key bullet points." },
      { title: "Coding Assistant", slug: "coding-assistant", description: "Refactor, explain, and debug code snippets inside any editor." },
    ],
  },
  {
    title: "AI Providers",
    slug: "providers",
    items: [
      { title: "Gemini Integration", slug: "gemini-integration", description: "Connecting Google Gemini Flash for ultra-fast cloud responses." },
      { title: "Ollama Integration", slug: "ollama-integration", description: "Running local LLMs (Gemma 3, Llama 3, Qwen) completely offline." },
      { title: "OpenRouter Integration", slug: "openrouter-integration", description: "Accessing Claude 3.5, GPT-4o, DeepSeek V3 via OpenRouter API key." },
      { title: "Custom API Setup", slug: "custom-api-setup", description: "Configuring LM Studio, vLLM, Groq, or OpenAI-compatible endpoints." },
      { title: "Smart Router", slug: "smart-router", description: "Task-based automatic routing to specialized models." },
      { title: "Auto Provider", slug: "auto-provider", description: "Dynamic provider selection based on query length and privacy rules." },
    ],
  },
  {
    title: "Privacy & Security",
    slug: "privacy-security",
    items: [
      { title: "Local AI Mode", slug: "local-ai-mode", description: "100% offline inference with zero data leaving your Mac." },
      { title: "Cloud AI Mode", slug: "cloud-ai-mode", description: "Encrypted API requests using your personal API keys." },
      { title: "Data Privacy", slug: "data-privacy", description: "Zero analytics tracking, prompt logging, or diagnostic collection." },
      { title: "Offline Mode", slug: "offline-mode", description: "Air-gapped operation for confidential enterprise work." },
    ],
  },
  {
    title: "Settings & Configuration",
    slug: "settings",
    items: [
      { title: "General Settings", slug: "general-settings", description: "Launch on startup, tray behavior, and auto-replace toggles." },
      { title: "Hotkey Configuration", slug: "hotkey-configuration", description: "Customizing global hotkeys and push-to-talk triggers." },
      { title: "Model Configuration", slug: "model-configuration", description: "Setting default models, temperature, and system prompts." },
      { title: "Context Window", slug: "context-window", description: "Managing token budgets (2k / 4k / 8k context limits)." },
      { title: "Theme & Appearance", slug: "theme-appearance", description: "Dark, Light, and Glassmorphic aesthetic customization." },
    ],
  },
  {
    title: "Advanced Customization",
    slug: "advanced",
    items: [
      { title: "Custom System Prompts", slug: "custom-system-prompts", description: "Creating custom mode presets tailored to your domain." },
      { title: "Context Length Optimization", slug: "context-length-optimization", description: "Token budgeting strategies for low-memory Macs." },
      { title: "Smart Router Config", slug: "smart-router-config", description: "Fine-tuning task group mappings (Coding, Writing, Reasoning)." },
      { title: "Auto Provider Config", slug: "auto-provider-config", description: "Adjusting character thresholds and privacy fallbacks." },
      { title: "Smart Fallback", slug: "smart-fallback", description: "Configuring multi-provider priority failovers." },
    ],
  },
  {
    title: "Troubleshooting",
    slug: "troubleshooting",
    items: [
      { title: "Ollama Connection Issues", slug: "ollama-connection-issues", description: "Resolving server port 11434 and daemon startup errors." },
      { title: "API Key Problems", slug: "api-key-problems", description: "Fixing 401 unauthorized, rate-limiting, and key validation issues." },
      { title: "Performance Optimization", slug: "performance-optimization", description: "Eliminating latency spikes and warm GPU idle routines." },
      { title: "Permission Issues", slug: "permission-issues", description: "Resetting macOS Accessibility and Input Monitoring permissions." },
      { title: "Model Loading Errors", slug: "model-loading-errors", description: "Handling missing weights and VRAM allocation failures." },
    ],
  },
  {
    title: "Changelog & Releases",
    slug: "changelog",
    items: [
      { title: "Release Notes", slug: "changelog", description: "Version history, feature additions, and bug fixes." },
    ]
  }
];

export function getFlatDocList() {
  const flat: { category: string; categorySlug: string; item: DocItem }[] = [];
  docCategories.forEach((cat) => {
    cat.items.forEach((item) => {
      flat.push({ category: cat.title, categorySlug: cat.slug, item });
    });
  });
  return flat;
}
