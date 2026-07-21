export interface FAQItem {
  id: string;
  category: "installation" | "features" | "providers" | "pricing" | "privacy" | "offline" | "gemini" | "ollama" | "openrouter" | "macos" | "performance" | "security";
  question: string;
  answer: string;
}

export const FAQ_CATEGORIES = [
  { id: "all", label: "All Questions" },
  { id: "installation", label: "Installation & Setup" },
  { id: "features", label: "Features & Modes" },
  { id: "providers", label: "AI Providers & Routing" },
  { id: "privacy", label: "Privacy & Zero Telemetry" },
  { id: "offline", label: "Offline Mode" },
  { id: "ollama", label: "Local Ollama" },
  { id: "gemini", label: "Google Gemini" },
  { id: "openrouter", label: "OpenRouter & Cloud" },
  { id: "macos", label: "macOS Integration" },
  { id: "performance", label: "Performance & Hardware" },
  { id: "security", label: "Security & Keys" },
  { id: "pricing", label: "Pricing & License" },
];

export const faqDatabase: FAQItem[] = [
  // --- INSTALLATION & SETUP (15) ---
  {
    id: "inst-1",
    category: "installation",
    question: "What macOS versions are supported by Avelyn?",
    answer: "Avelyn supports macOS Sonoma (14.0+) and macOS Sequoia (15.0+). Both Apple Silicon (M1/M2/M3/M4) and Intel Macs are natively supported."
  },
  {
    id: "inst-2",
    category: "installation",
    question: "How do I install Avelyn on my Mac?",
    answer: "Download the `.dmg` installer from our website, open the disk image, and drag Avelyn into your Applications folder. On first launch, the onboarding wizard guides you through granting Accessibility permissions."
  },
  {
    id: "inst-3",
    category: "installation",
    question: "Why does Avelyn require macOS Accessibility permissions?",
    answer: "Accessibility permissions allow Avelyn to read the currently highlighted text in any app (Chrome, Xcode, Slack, Pages, Notes) and paste the AI-enhanced text seamlessly back into your active cursor location."
  },
  {
    id: "inst-4",
    category: "installation",
    question: "Why does Avelyn ask for Input Monitoring permissions?",
    answer: "Input Monitoring allows Avelyn to listen for your global system-wide hotkey trigger (Option+Space or custom shortcut) even when Avelyn is running in the background menu bar."
  },
  {
    id: "inst-5",
    category: "installation",
    question: "Can I install Avelyn via Homebrew?",
    answer: "Yes! You can install Avelyn via Homebrew Cask using `brew install --cask avelyn`."
  },
  {
    id: "inst-6",
    category: "installation",
    question: "Does Avelyn auto-update itself?",
    answer: "Avelyn includes a non-intrusive update checker that notifies you in the system tray when a new stable release is available."
  },
  {
    id: "inst-7",
    category: "installation",
    question: "How do I trigger the auto-installer overlay during first setup?",
    answer: "If you do not have Ollama installed, Avelyn automatically detects it on startup and displays an overlay wizard that downloads Ollama and pulls recommended default models like Gemma 3."
  },
  {
    id: "inst-8",
    category: "installation",
    question: "What should I do if macOS says 'Avelyn cannot be opened because it is from an unidentified developer'?",
    answer: "Avelyn is signed and notarized by Apple. If you encounter Gatekeeper warnings, open System Settings → Privacy & Security, scroll to Security, and click 'Open Anyway'."
  },
  {
    id: "inst-9",
    category: "installation",
    question: "Can I run Avelyn without administrator rights?",
    answer: "Yes, Avelyn runs in user space inside your `~/Applications` folder. Admin rights are only needed once to grant initial Accessibility permissions in macOS Settings."
  },
  {
    id: "inst-10",
    category: "installation",
    question: "How do I verify the integrity of the downloaded DMG package?",
    answer: "We publish SHA-256 checksums for every release on our GitHub Releases page. You can verify your download using `shasum -a 256 Avelyn-Installer.dmg`."
  },
  {
    id: "inst-11",
    category: "installation",
    question: "Does Avelyn run on Windows or Linux?",
    answer: "Avelyn's core architecture is built with cross-platform Python and PyQt6. The macOS version is fully released, while Windows and Linux builds are in active preview."
  },
  {
    id: "inst-12",
    category: "installation",
    question: "How do I completely uninstall Avelyn?",
    answer: "To completely uninstall, drag Avelyn from Applications to Trash, and delete the user config folder at `~/.avelyn`."
  },
  {
    id: "inst-13",
    category: "installation",
    question: "Does Avelyn support silent deployment for enterprise fleets?",
    answer: "Yes, system administrators can deploy Avelyn via MDM profiles (Jamf, Kandji) pre-granting TCC permissions and distributing standard `config.json` templates."
  },
  {
    id: "inst-14",
    category: "installation",
    question: "Can I customize the installation directory?",
    answer: "Avelyn can be placed in `/Applications` for all users or `~/Applications` for single-user installations."
  },
  {
    id: "inst-15",
    category: "installation",
    question: "What happens if I update macOS from Sonoma to Sequoia?",
    answer: "macOS updates may occasionally reset TCC permissions. If Avelyn stops capturing text after a major OS upgrade, simply toggle Accessibility off and on in System Settings."
  },

  // --- FEATURES & MODES (20) ---
  {
    id: "feat-1",
    category: "features",
    question: "What is Prompt Enhancement?",
    answer: "Prompt Enhancement takes brief or raw user instructions (e.g., 'fix email') and expands them into structured, context-rich prompts before sending them to the AI provider."
  },
  {
    id: "feat-2",
    category: "features",
    question: "How does Grammar Correction work in Avelyn?",
    answer: "Grammar Correction fixes spelling mistakes, punctuation errors, awkward phrasing, and verb tense inconsistencies without altering your original tone or meaning."
  },
  {
    id: "feat-3",
    category: "features",
    question: "What does the Professional Writing mode do?",
    answer: "Professional mode elevates casual writing into clear, authoritative executive communication suitable for reports, memos, and client emails."
  },
  {
    id: "feat-4",
    category: "features",
    question: "How does Email Writing mode work?",
    answer: "Email mode reformats raw bullet points into polished business emails complete with subject lines, greeting structures, and call-to-action closings."
  },
  {
    id: "feat-5",
    category: "features",
    question: "What options are available in AI Rewrite mode?",
    answer: "AI Rewrite supports tone shifting (formal, persuasive, concise, friendly), text expansion, text shortening, and style adaptation."
  },
  {
    id: "feat-6",
    category: "features",
    question: "How many languages are supported in Translation mode?",
    answer: "Avelyn supports instant translation across 50+ major languages including Spanish, French, German, Japanese, Chinese, Portuguese, Hindi, and Arabic."
  },
  {
    id: "feat-7",
    category: "features",
    question: "What does Summarization mode do?",
    answer: "Summarization extracts key takeaways, executive summaries, or bulleted action items from long articles, PDFs, and meeting notes."
  },
  {
    id: "feat-8",
    category: "features",
    question: "How does the Coding Assistant mode help developers?",
    answer: "Coding Assistant refactors messy code, adds docstrings, explains complex functions, generates unit tests, and fixes syntax bugs inside VS Code, Xcode, or JetBrains IDEs."
  },
  {
    id: "feat-9",
    category: "features",
    question: "Can I create custom modes in Avelyn?",
    answer: "Yes! You can add custom mode presets in Settings with custom system prompts tailored to your specific workflow or industry."
  },
  {
    id: "feat-10",
    category: "features",
    question: "What is the Command Palette?",
    answer: "The Command Palette is a floating overlay triggered by your hotkey. It displays preset action buttons, custom prompt text inputs, and streaming AI response previews."
  },
  {
    id: "feat-11",
    category: "features",
    question: "How does Instant Text Replacement work?",
    answer: "After the AI generates the output, Avelyn copies the output to the clipboard and sends a synthetic `Cmd+V` event to paste it right back over your selected text."
  },
  {
    id: "feat-12",
    category: "features",
    question: "Can I cancel a streaming AI generation mid-way?",
    answer: "Yes! Pressing `Escape` or clicking the cancel button instantly stops the active HTTP stream without modifying your text."
  },
  {
    id: "feat-13",
    category: "features",
    question: "Does Avelyn preserve original clipboard history?",
    answer: "Yes! Avelyn saves your existing clipboard contents prior to processing and restores your original clipboard item shortly after performing the text replacement."
  },
  {
    id: "feat-14",
    category: "features",
    question: "What is Push-to-Talk (PTT) Voice Control?",
    answer: "Push-to-Talk allows you to hold down a hotkey, speak your instruction into your Mac's microphone, and let Avelyn execute the command hands-free."
  },
  {
    id: "feat-15",
    category: "features",
    question: "How does Tone Shifting work?",
    answer: "Tone Shifting alters emotional register—transforming blunt draft notes into warm customer support replies or firm contract follow-ups."
  },
  {
    id: "feat-16",
    category: "features",
    question: "Can Avelyn format outputs in Markdown or HTML?",
    answer: "Yes, depending on your prompt instruction or mode configuration, outputs can be formatted as clean Markdown, plain text, or structured tables."
  },
  {
    id: "feat-17",
    category: "features",
    question: "Does Avelyn work in web browsers like Chrome and Safari?",
    answer: "Avelyn works system-wide across all applications including Chrome, Safari, Firefox, Slack, Notion, Obsidian, Apple Notes, and Microsoft Word."
  },
  {
    id: "feat-18",
    category: "features",
    question: "What is the Productivity Dashboard?",
    answer: "The Productivity Dashboard tracks your daily time saved, character count refined, and mode usage statistics locally on your machine."
  },
  {
    id: "feat-19",
    category: "features",
    question: "Can I preview AI suggestions before pasting?",
    answer: "Yes! If Auto-Replace is disabled in Settings, Avelyn displays a preview window allowing you to inspect, edit, or copy the suggestion before applying."
  },
  {
    id: "feat-20",
    category: "features",
    question: "How does Avelyn handle code syntax highlighting?",
    answer: "In Coding Assistant mode, Avelyn strips conversational filler and formats clean, syntactically correct code blocks matching your active programming language."
  },

  // --- AI PROVIDERS & ROUTING (20) ---
  {
    id: "prov-1",
    category: "providers",
    question: "What AI providers does Avelyn support?",
    answer: "Avelyn supports Local Ollama (offline), Avelyn Cloud / OpenRouter, Google Gemini, and Custom OpenAI-compatible endpoints (LM Studio, vLLM, Groq, DeepSeek)."
  },
  {
    id: "prov-2",
    category: "providers",
    question: "What is the Smart Router?",
    answer: "The Smart Router automatically routes tasks to specialized providers based on task categories (e.g., Coding tasks to Claude/DeepSeek, Privacy tasks to Local Ollama)."
  },
  {
    id: "prov-3",
    category: "providers",
    question: "How does Auto Provider selection work?",
    answer: "Auto Provider dynamically analyzes text length and task privacy rules—routing short snippets (<50 chars) to Local Ollama for speed and long documents to Cloud models."
  },
  {
    id: "prov-4",
    category: "providers",
    question: "What are Smart Fallbacks?",
    answer: "Smart Fallbacks ensure reliability: if your primary cloud provider experiences downtime or rate limits, Avelyn automatically retries using your secondary fallback provider."
  },
  {
    id: "prov-5",
    category: "providers",
    question: "Can I use my own OpenRouter API key?",
    answer: "Yes! Simply paste your OpenRouter API key into Settings → AI Provider to access 200+ top LLMs on a pay-as-you-go basis."
  },
  {
    id: "prov-6",
    category: "providers",
    question: "Is Google Gemini Flash supported natively?",
    answer: "Yes! Avelyn includes dedicated Google GenAI SDK integration for ultra-fast Gemini Flash responses."
  },
  {
    id: "prov-7",
    category: "providers",
    question: "Can I connect local models running in LM Studio or vLLM?",
    answer: "Yes! Select 'Custom API' in Settings, enter your local server URL (e.g., `http://localhost:1234/v1`), and specify your model identifier."
  },
  {
    id: "prov-8",
    category: "providers",
    question: "How does Avelyn fetch available OpenRouter models?",
    answer: "Avelyn queries OpenRouter's dynamic `/v1/models` API and caches the model catalog locally for 24 hours."
  },
  {
    id: "prov-9",
    category: "providers",
    question: "Does Avelyn support free OpenRouter models?",
    answer: "Yes! Models tagged with `:free` on OpenRouter (such as DeepSeek V3 Free and Gemma 3 27B Free) are supported out of the box."
  },
  {
    id: "prov-10",
    category: "providers",
    question: "Can I override the model selection for specific task groups?",
    answer: "Yes! Under Settings → Router Config, you can explicitly set provider and model pairs for Coding, Writing, Reasoning, Voice, and Privacy tasks."
  },
  {
    id: "prov-11",
    category: "providers",
    question: "What happens if Ollama is not running when an Ollama provider request is made?",
    answer: "Avelyn automatically attempts to start the Ollama background daemon silently. If it fails, Smart Fallback routes the request to your configured fallback provider."
  },
  {
    id: "prov-12",
    category: "providers",
    question: "What context window sizes are supported?",
    answer: "Avelyn supports configurable context windows ranging from 2,048 tokens up to 8,192 tokens depending on model memory limits."
  },
  {
    id: "prov-13",
    category: "providers",
    question: "Does Avelyn stream tokens in real time?",
    answer: "Yes! All providers yield partial tokens in real-time using Server-Sent Events (SSE) for minimal Time-To-First-Token (TTFT)."
  },
  {
    id: "prov-14",
    category: "providers",
    question: "How does token budgeting prevent memory bloat?",
    answer: "Avelyn dynamically truncates prompt history and caps `max_tokens` based on selected task requirements to keep generation swift."
  },
  {
    id: "prov-15",
    category: "providers",
    question: "Can I use Anthropic Claude models?",
    answer: "Yes, via OpenRouter or Custom API endpoints configured for Claude 3.5 Sonnet / Haiku."
  },
  {
    id: "prov-16",
    category: "providers",
    question: "Can I use DeepSeek V3 or DeepSeek R1 models?",
    answer: "Yes! You can run DeepSeek models locally via Ollama or via OpenRouter / DeepSeek custom endpoints."
  },
  {
    id: "prov-17",
    category: "providers",
    question: "What temperature setting does Avelyn use?",
    answer: "By default, Avelyn uses a low temperature (0.15) for precise, consistent writing, but this can be adjusted in settings."
  },
  {
    id: "prov-18",
    category: "providers",
    question: "Does Avelyn store my API keys in plain text?",
    answer: "No! API keys are stored in user-scoped application config files and masked in the UI with password bullets."
  },
  {
    id: "prov-19",
    category: "providers",
    question: "What is the GPU Keep-Alive routine?",
    answer: "On Apple Silicon M-series Macs, macOS idles GPU compute blocks after ~60s. Avelyn sends a lightweight 1-token ping every 120s to keep Neural Engine TTFT under 0.5s."
  },
  {
    id: "prov-20",
    category: "providers",
    question: "How do I switch active AI providers on the fly?",
    answer: "You can switch active providers instantly in Settings → AI Provider, or let the Smart Router handle switching automatically per task."
  },

  // --- PRIVACY & SECURITY (15) ---
  {
    id: "priv-1",
    category: "privacy",
    question: "Does Avelyn collect telemetry or usage analytics?",
    answer: "No. Avelyn has zero tracking scripts, zero analytics telemetry, and zero diagnostic reporting. Your prompts and usage data stay 100% on your machine."
  },
  {
    id: "priv-2",
    category: "privacy",
    question: "Are my highlighted texts sent to Avelyn's servers?",
    answer: "No. Avelyn does not operate any central prompt logging servers. In Local AI mode, text never leaves your Mac. In Cloud mode, text goes directly to your provider."
  },
  {
    id: "priv-3",
    category: "privacy",
    question: "How does Local AI mode ensure 100% privacy?",
    answer: "Local AI mode processes prompts using Ollama running on `localhost:11434`. You can disconnect from Wi-Fi entirely and Avelyn will function seamlessly."
  },
  {
    id: "priv-4",
    category: "privacy",
    question: "How are API keys secured in Settings?",
    answer: "API keys are masked with bullet characters in the settings GUI, preventing shoulder-surfing or accidental exposure during screen shares."
  },
  {
    id: "priv-5",
    category: "privacy",
    question: "Does Avelyn train AI models on my data?",
    answer: "Never. Local models do not train on inputs. When using OpenRouter or Gemini cloud providers, data retention policies are governed by your personal API account."
  },
  {
    id: "priv-6",
    category: "privacy",
    question: "Where are settings and history saved on my Mac?",
    answer: "All configuration files, settings JSON, and productivity metrics are stored locally in your user folder at `~/.avelyn`."
  },
  {
    id: "priv-7",
    category: "privacy",
    question: "Does Avelyn read passwords or sensitive input fields?",
    answer: "No. Avelyn only reads text that you explicitly highlight and activate using your manual hotkey trigger."
  },
  {
    id: "priv-8",
    category: "privacy",
    question: "Can I use Avelyn in air-gapped corporate environments?",
    answer: "Yes! Set Local Ollama as your provider, turn on Offline Mode, and Avelyn will operate strictly within your air-gapped network."
  },
  {
    id: "priv-9",
    category: "privacy",
    question: "Is my personal data encrypted at rest?",
    answer: "Settings files are stored in user-restricted directory space (`~/.avelyn`) protected by standard macOS file system permissions."
  },
  {
    id: "priv-10",
    category: "privacy",
    question: "What permissions does Avelyn require on macOS?",
    answer: "Avelyn requires Accessibility permissions (for text replacement) and Input Monitoring permissions (for global hotkey triggers)."
  },
  {
    id: "priv-11",
    category: "privacy",
    question: "Does Avelyn share data with third-party advertisers?",
    answer: "No. We have no advertising partners, data brokers, or monetization models involving user data."
  },
  {
    id: "priv-12",
    category: "privacy",
    question: "How can I purge all local data?",
    answer: "Simply delete the `~/.avelyn` directory to erase all settings, model caches, and history."
  },
  {
    id: "priv-13",
    category: "privacy",
    question: "Does Avelyn log my prompt text to disk?",
    answer: "By default, debug logs only record operational metrics (latency, token counts, mode IDs). Full prompt text logging is disabled."
  },
  {
    id: "priv-14",
    category: "privacy",
    question: "Is Avelyn SOC2 or GDPR compliant?",
    answer: "Because Avelyn is a client-side application that processes data locally or via direct API connections, zero user data passes through our infrastructure, simplifying compliance."
  },
  {
    id: "priv-15",
    category: "privacy",
    question: "Can I restrict cloud routing for confidential projects?",
    answer: "Yes! Enable Privacy Task Routing to automatically force confidential or short text prompts to Local Ollama."
  },

  // --- OFFLINE MODE (10) ---
  {
    id: "off-1",
    category: "offline",
    question: "Can Avelyn work without an internet connection?",
    answer: "Yes! When configured with Local Ollama, Avelyn works 100% offline without requiring internet access."
  },
  {
    id: "off-2",
    category: "offline",
    question: "Which models work best offline?",
    answer: "For offline use on Mac, we recommend Gemma 3 4B, Llama 3.2 3B, Qwen 2.5 7B, or Mistral 7B."
  },
  {
    id: "off-3",
    category: "offline",
    question: "Does offline mode affect generation quality?",
    answer: "Modern 4B and 7B local models deliver exceptional grammar, email writing, and prompt enhancement performance offline."
  },
  {
    id: "off-4",
    category: "offline",
    question: "How do I download local models for offline use?",
    answer: "Avelyn's auto-installer pulls default models, or you can run `ollama pull gemma3:4b` in Terminal."
  },
  {
    id: "off-5",
    category: "offline",
    question: "Does Push-to-Talk voice recognition work offline?",
    answer: "Yes, voice-to-text processing uses local macOS speech APIs without sending audio recordings to cloud servers."
  },
  {
    id: "off-6",
    category: "offline",
    question: "How much disk space is required for offline models?",
    answer: "4B models require ~3 GB of disk space, while 7B/8B models require ~5 GB."
  },
  {
    id: "off-7",
    category: "offline",
    question: "Can I switch to cloud providers when internet is restored?",
    answer: "Yes! Avelyn seamlessly toggles between local and cloud providers dynamically."
  },
  {
    id: "off-8",
    category: "offline",
    question: "What happens if I trigger a cloud provider while offline?",
    answer: "Avelyn catches network errors instantly and falls back to Local Ollama automatically if Smart Fallback is enabled."
  },
  {
    id: "off-9",
    category: "offline",
    question: "Are offline models fast on M1/M2/M3 Macs?",
    answer: "Extremely fast! Unified Memory on Apple Silicon allows local models to achieve 40–80 tokens per second."
  },
  {
    id: "off-10",
    category: "offline",
    question: "Is offline mode available in the free version?",
    answer: "Yes! Offline Local AI mode is a core foundation of Avelyn and is fully available to all users."
  },

  // --- LOCAL OLLAMA (10) ---
  {
    id: "oll-1",
    category: "ollama",
    question: "What is Ollama?",
    answer: "Ollama is an open-source local LLM runner that allows you to run large language models locally on macOS."
  },
  {
    id: "oll-2",
    category: "ollama",
    question: "Does Avelyn install Ollama automatically?",
    answer: "Yes! If Ollama is not detected, Avelyn offers a one-click auto-installer wizard."
  },
  {
    id: "oll-3",
    category: "ollama",
    question: "What host port does Ollama use?",
    answer: "Ollama runs locally on port 11434 (`http://localhost:11434`)."
  },
  {
    id: "oll-4",
    category: "ollama",
    question: "Can I use custom GGUF models with Ollama and Avelyn?",
    answer: "Yes! Any custom model created via an Ollama `Modelfile` can be selected in Avelyn's model configuration."
  },
  {
    id: "oll-5",
    category: "ollama",
    question: "How do I update local Ollama models?",
    answer: "Run `ollama pull <model-name>` in Terminal to update your local weights to the latest version."
  },
  {
    id: "oll-6",
    category: "ollama",
    question: "Why does Ollama take a few seconds on first generation?",
    answer: "The first request loads model weights from SSD into Mac VRAM. Avelyn's warm GPU routine keeps models loaded in memory."
  },
  {
    id: "oll-7",
    category: "ollama",
    question: "How do I check if Ollama is running?",
    answer: "Open `http://localhost:11434` in your browser—it should return 'Ollama is running'."
  },
  {
    id: "oll-8",
    category: "ollama",
    question: "Can I change the Ollama host URL in Avelyn?",
    answer: "Yes! In Settings → AI Provider, you can customize the Ollama host URL for remote network instances."
  },
  {
    id: "oll-9",
    category: "ollama",
    question: "What Ollama models are recommended for coding?",
    answer: "DeepSeek-Coder V2, Qwen 2.5 Coder 7B, and CodeLlama."
  },
  {
    id: "oll-10",
    category: "ollama",
    question: "What Ollama models are recommended for writing?",
    answer: "Gemma 3 4B, Llama 3.1 8B, and Mistral 7B."
  },

  // --- GOOGLE GEMINI (5) ---
  {
    id: "gem-1",
    category: "gemini",
    question: "How do I integrate Google Gemini Flash with Avelyn?",
    answer: "Select Gemini in Settings → AI Provider and enter your Google AI Studio API key."
  },
  {
    id: "gem-2",
    category: "gemini",
    question: "Is Gemini Flash faster than local models?",
    answer: "Gemini Flash offers ultra-low latency streaming with high token throughput for long documents."
  },
  {
    id: "gem-3",
    category: "gemini",
    question: "Where do I get a Gemini API key?",
    answer: "Get a free API key at `aistudio.google.com`."
  },
  {
    id: "gem-4",
    category: "gemini",
    question: "Does Avelyn use the official Google GenAI SDK?",
    answer: "Yes, Avelyn integrates the official `google-genai` Python library."
  },
  {
    id: "gem-5",
    category: "gemini",
    question: "Which Gemini models are supported?",
    answer: "Gemini 2.5 Flash, Gemini 1.5 Pro, and Gemini 2.0 Flash thinking models."
  },

  // --- OPENROUTER & CLOUD (5) ---
  {
    id: "open-1",
    category: "openrouter",
    question: "What is OpenRouter?",
    answer: "OpenRouter is an API aggregator providing access to OpenAI, Anthropic, Google, Meta, and open-source models via a single API key."
  },
  {
    id: "open-2",
    category: "openrouter",
    question: "How do I configure OpenRouter in Avelyn?",
    answer: "Enter your `sk-or-v1-...` API key in Settings → AI Provider under Avelyn Cloud."
  },
  {
    id: "open-3",
    category: "openrouter",
    question: "Can I use GPT-4o and Claude 3.5 Haiku?",
    answer: "Yes! Both models are selectable in Avelyn Cloud Settings."
  },
  {
    id: "open-4",
    category: "openrouter",
    question: "What happens if my OpenRouter account runs out of credits?",
    answer: "Avelyn catches HTTP 402 credit errors gracefully and prompts you to switch providers or top up."
  },
  {
    id: "open-5",
    category: "openrouter",
    question: "Does Avelyn mark up OpenRouter token costs?",
    answer: "No. You pay standard raw API prices directly to OpenRouter."
  },

  // --- MACOS INTEGRATION (5) ---
  {
    id: "mac-1",
    category: "macos",
    question: "Does Avelyn support Apple Silicon M1, M2, M3, M4 Macs?",
    answer: "Yes! Avelyn is optimized for Apple Silicon Unified Memory and Metal acceleration."
  },
  {
    id: "mac-2",
    category: "macos",
    question: "How do I change the global hotkey?",
    answer: "Open Settings → Hotkeys and press your preferred key combination."
  },
  {
    id: "mac-3",
    category: "macos",
    question: "Does Avelyn run in the macOS Menu Bar?",
    answer: "Yes, Avelyn lives quietly in your system tray menu bar for instant access."
  },
  {
    id: "mac-4",
    category: "macos",
    question: "Why did Avelyn stop pasting after a macOS update?",
    answer: "macOS updates occasionally reset TCC permissions. Re-enable Accessibility in System Settings."
  },
  {
    id: "mac-5",
    category: "macos",
    question: "Does Avelyn work in full-screen spaces?",
    answer: "Yes! The Command Palette overlay activates seamlessly across multiple spaces."
  },

  // --- PERFORMANCE & HARDWARE (5) ---
  {
    id: "perf-1",
    category: "performance",
    question: "How much RAM does Avelyn use?",
    answer: "The lightweight desktop shell uses ~60 MB RAM. Local model memory depends on model size (3–6 GB)."
  },
  {
    id: "perf-2",
    category: "performance",
    question: "Does Avelyn drain Mac battery life?",
    answer: "Avelyn sleeps when inactive, using zero CPU/GPU cycles until invoked."
  },
  {
    id: "perf-3",
    category: "performance",
    question: "How fast is text replacement?",
    answer: "Text replacement takes ~100 ms after AI generation completes."
  },
  {
    id: "perf-4",
    category: "performance",
    question: "What is Time-To-First-Token (TTFT)?",
    answer: "TTFT measures latency before streaming begins. Cloud models average 200–400 ms; local models average 300–600 ms."
  },
  {
    id: "perf-5",
    category: "performance",
    question: "How can I optimize speed on an 8 GB RAM Mac?",
    answer: "Use Gemma 3 4B local model or Gemini Flash cloud model."
  },

  // --- SECURITY & KEYS (5) ---
  {
    id: "sec-1",
    category: "security",
    question: "Are my API keys stored securely?",
    answer: "API keys are saved in local application storage (`~/.avelyn`) and masked in the UI."
  },
  {
    id: "sec-2",
    category: "security",
    question: "Does Avelyn transmit telemetry to third parties?",
    answer: "Zero telemetry or analytics are transmitted."
  },
  {
    id: "sec-3",
    category: "security",
    question: "Can I inspect the network activity of Avelyn?",
    answer: "Yes, network requests connect directly to your configured provider endpoints."
  },
  {
    id: "sec-4",
    category: "security",
    question: "Is the installer signed and notarized?",
    answer: "Yes, release builds are signed with Apple Developer ID certificates."
  },
  {
    id: "sec-5",
    category: "security",
    question: "How do I report security concerns?",
    answer: "Report vulnerabilities via security@avelyn.software or GitHub security advisories."
  },

  // --- PRICING & LICENSE (5) ---
  {
    id: "prc-1",
    category: "pricing",
    question: "Is Avelyn free to use?",
    answer: "Yes! Avelyn is free for local offline AI use. Cloud AI usage relies on your own API keys."
  },
  {
    id: "prc-2",
    category: "pricing",
    question: "Are there monthly subscription fees?",
    answer: "No subscription fees. You only pay provider API costs if using cloud keys."
  },
  {
    id: "prc-3",
    category: "pricing",
    question: "Can I use Avelyn for commercial work?",
    answer: "Yes! Commercial use is fully allowed."
  },
  {
    id: "prc-4",
    category: "pricing",
    question: "Is there a team or enterprise license?",
    answer: "We offer pre-configured fleet deployment assistance for enterprise teams."
  },
  {
    id: "prc-5",
    category: "pricing",
    question: "How can I support Avelyn development?",
    answer: "Star our GitHub repository and share Avelyn with fellow Mac users!"
  }
];
