# TextPolish 🟣

> **AI-powered global text enhancer** — Select any text, press a shortcut, and watch it transform into polished, professional prose instantly.

Works **system-wide** across browsers, VS Code, Word, Notepad, ChatGPT, and any editable text field on **macOS** and **Windows**.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🌍 **Global hotkey** | Works in any app, system-wide |
| 🤖 **Multiple AI backends** | Gemini, OpenAI, Ollama (offline) |
| 🎨 **5 enhancement modes** | Professional, Creative, Technical, Concise, Academic |
| 📺 **Streaming preview** | See AI response token-by-token before replacing |
| ↩ **Undo** | Instantly restore original text after replacement |
| 🗂 **Prompt history** | Last 50 enhancements saved locally |
| 🖥 **System tray** | Lightweight background operation |
| 🌓 **Dark / Light theme** | Fully themed PyQt6 interface |
| 🔑 **Settings UI** | Configure API keys, shortcuts, modes without editing config |
| 🦙 **Offline mode** | Ollama local LLM support |

---

## 📁 Project Structure

```
textpolish/
├── main.py               # Entry point
├── hotkeys.py            # Global hotkey listener (pynput)
├── clipboard_manager.py  # Clipboard read/write/restore
├── ai_processor.py       # Gemini + OpenAI + Ollama backends
├── ui.py                 # PyQt6 popup, settings, tray icon
├── settings.py           # JSON config (~/.textpolish/config.json)
├── platform_handler.py   # macOS / Windows platform hooks
├── logger.py             # Rotating file logger
├── assets/
│   └── icon.png          # App icon
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.10+** — [python.org](https://python.org)
- **macOS** 12+ (Intel or Apple Silicon) **or Windows** 10/11
- A **Gemini API key** — [aistudio.google.com](https://aistudio.google.com) (free tier available)

### 2. Clone / Download

```bash
# Clone the repo (or download the ZIP and extract it)
git clone https://github.com/yourname/textpolish.git
cd textpolish
```

### 3. Create a virtual environment

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure your API key

Either run the app and open **Settings → AI Provider**, or set it manually:

```bash
# macOS / Linux
echo '{"gemini_api_key": "YOUR_KEY_HERE"}' > ~/.textpolish/config.json

# Windows PowerShell
$dir = "$env:USERPROFILE\.textpolish"
New-Item -ItemType Directory -Force -Path $dir
'{"gemini_api_key": "YOUR_KEY_HERE"}' | Set-Content "$dir\config.json"
```

### 6. Run

```bash
python main.py
```

The app starts silently in the **system tray** (macOS menu bar / Windows taskbar).

---

## ⌨ Default Shortcut

| Platform | Shortcut |
|---|---|
| macOS | `Ctrl + Shift + E` |
| Windows | `Ctrl + Shift + E` |

> Customisable in **Settings → Hotkeys**.

---

## 🔑 API Key Setup

### Gemini (Recommended — free tier)
1. Visit [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Create an API key
3. Paste it in **Settings → AI Provider → Gemini API Key**

### OpenAI
1. Visit [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create a key
3. Paste it in **Settings → AI Provider → OpenAI API Key**

### Ollama (Offline / Local)
1. Install Ollama: [ollama.ai](https://ollama.ai)
2. Pull a model: `ollama pull llama3`
3. Start Ollama: `ollama serve`
4. In Settings, set Provider to **Ollama** and Model to `llama3`

---

## 🍎 macOS Setup Notes

### Accessibility Permission (Required)
TextPolish needs **Accessibility permission** to detect global hotkeys and simulate Ctrl+C / Ctrl+V.

1. Open **System Settings → Privacy & Security → Accessibility**
2. Click the **+** button
3. Add **Python** (or the TextPolish app bundle if built)
4. Toggle it **ON**

The app will prompt you automatically on first launch.

### Apple Silicon
Fully compatible. No special setup needed.

---

## 🪟 Windows Setup Notes

### Defender / Antivirus
Some antivirus tools flag `pyautogui` / `pynput` as suspicious (they simulate keystrokes). Add the project folder as an exclusion if needed.

### Launch at Startup
Enable in **Settings → Hotkeys → Launch TextPolish at system login**. This adds a registry key under `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`.

---

## 🔧 CLI Flags

```bash
# Run with verbose debug logging
python main.py --debug

# Smoke-test clipboard operations (no GUI)
python main.py --test-clipboard

# Smoke-test AI connection (no GUI)
python main.py --test-ai

# Show version
python main.py --version
```

---

## 📦 Building a Standalone Executable

Install PyInstaller:
```bash
pip install pyinstaller
```

### macOS `.app` bundle
```bash
pyinstaller \
  --onefile \
  --windowed \
  --name "TextPolish" \
  --icon assets/icon.icns \
  --add-data "assets:assets" \
  main.py
```
Output: `dist/TextPolish.app`

### Windows `.exe`
```powershell
pyinstaller `
  --onefile `
  --windowed `
  --name "TextPolish" `
  --icon assets/icon.ico `
  --add-data "assets;assets" `
  main.py
```
Output: `dist\TextPolish.exe`

---

## 🗂 Configuration File

Located at `~/.textpolish/config.json`. Edited automatically by the Settings UI.

```json
{
  "hotkey": "<ctrl>+<shift>+e",
  "shortcut_display": "Ctrl+Shift+E",
  "hotkey_enabled": true,
  "ai_provider": "gemini",
  "gemini_api_key": "YOUR_KEY",
  "openai_api_key": "",
  "openai_model": "gpt-4o-mini",
  "ollama_model": "llama3",
  "ollama_host": "http://localhost:11434",
  "default_mode": "professional",
  "theme": "dark",
  "launch_at_startup": false,
  "show_notifications": true,
  "prompt_history": [],
  "max_history": 50
}
```

---

## 🔄 Workflow

```
User selects text anywhere
        ↓
Presses Ctrl+Shift+E
        ↓
TextPolish saves clipboard
        ↓
Simulates Ctrl+C → copies selection
        ↓
Reads clipboard text
        ↓
Opens floating popup (near cursor)
        ↓
Streams AI response in real time
        ↓
User clicks "Replace Text"
        ↓
Sets enhanced text to clipboard
        ↓
Simulates Ctrl+V → pastes in-place
        ↓
Original clipboard restored
```

---

## 🤝 Troubleshooting

| Problem | Fix |
|---|---|
| Hotkey not detected (macOS) | Grant Accessibility permission (see above) |
| "API key not set" error | Open Settings → AI Provider and enter your key |
| Clipboard unchanged after hotkey | Ensure text is actually selected; retry |
| Ollama connection refused | Run `ollama serve` first |
| PyQt6 import error | Run `pip install PyQt6` inside your venv |

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

*Built with ❤ using Python, PyQt6, pynput, and the Gemini API.*
