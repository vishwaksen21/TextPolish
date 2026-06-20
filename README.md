# Avelyn 🟣

> **AI-powered global text enhancer** — Select any text, press a shortcut, and watch it transform into polished, professional prose instantly.

Works **system-wide** across browsers, VS Code, Word, Notepad, ChatGPT, and any editable text field on **macOS** and **Windows**.

---

## ✨ Features

| Feature                     | Details                                                     |
| --------------------------- | ----------------------------------------------------------- |
| 🌍 **Global hotkey**        | Works in any app, system-wide                               |
| 🤖 **Multiple AI backends** | Gemini, OpenAI, Ollama (offline)                            |
| 🎨 **5 enhancement modes**  | Professional, Creative, Technical, Concise, Academic        |
| 📺 **Streaming preview**    | See AI response token-by-token before replacing             |
| ↩ **Undo**                  | Instantly restore original text after replacement           |
| 🗂 **Prompt history**       | Last 50 enhancements saved locally                          |
| 🖥 **System tray**          | Lightweight background operation                            |
| 🌓 **Dark / Light theme**   | Fully themed PyQt6 interface                                |
| 🔑 **Settings UI**          | Configure API keys, shortcuts, modes without editing config |
| 🦙 **Offline mode**         | Ollama local LLM support                                    |

---

## 📁 Project Structure

```text
avelyn/
├── main.py               # Entry point
├── hotkeys.py            # Global hotkey listener (pynput)
├── clipboard_manager.py  # Clipboard read/write/restore
├── ai_processor.py       # Gemini + OpenAI + Ollama backends
├── ui.py                 # PyQt6 popup, settings, tray icon
├── settings.py           # JSON config (~/.avelyn/config.json)
├── platform_handler.py   # macOS / Windows platform hooks
├── logger.py             # Rotating file logger
├── assets/
│   ├── icon.png
│   ├── icon.icns
│   └── icon.ico
├── public/
│   └── logo.png
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Prerequisites

* Python 3.10+
* macOS 12+ (Intel or Apple Silicon) or Windows 10/11
* Gemini API key (free tier available)

### 2. Clone / Download

```bash
git clone https://github.com/yourname/avelyn.git
cd avelyn
```

### 3. Create a Virtual Environment

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Your API Key

#### macOS / Linux

```bash
echo '{"gemini_api_key": "YOUR_KEY_HERE"}' > ~/.avelyn/config.json
```

#### Windows PowerShell

```powershell
$dir = "$env:USERPROFILE\.avelyn"
New-Item -ItemType Directory -Force -Path $dir
'{"gemini_api_key": "YOUR_KEY_HERE"}' | Set-Content "$dir\config.json"
```

### 6. Run

```bash
python main.py
```

The app starts silently in the system tray.

---

## ⌨ Default Shortcut

| Platform | Shortcut         |
| -------- | ---------------- |
| macOS    | Ctrl + Shift + E |
| Windows  | Ctrl + Shift + E |

> Customizable in **Settings → Hotkeys**.

---

## 🔑 API Key Setup

### Gemini (Recommended)

1. Visit https://aistudio.google.com/app/apikey
2. Create an API key
3. Paste it into Settings → AI Provider

### OpenAI

1. Visit https://platform.openai.com/api-keys
2. Create an API key
3. Paste it into Settings → AI Provider

### Ollama (Offline)

```bash
ollama pull llama3
ollama serve
```

Set Provider to **Ollama** and Model to `llama3`.

---

## 🍎 macOS Setup Notes

### Accessibility Permission (Required)

1. Open **System Settings → Privacy & Security → Accessibility**
2. Click **+**
3. Add Python or the built application
4. Enable it

The application will prompt automatically on first launch.

### Apple Silicon

Fully supported.

---

## 🪟 Windows Setup Notes

### Defender / Antivirus

Some antivirus products may flag automation libraries such as `pynput` or `pyautogui`. Add the project directory to exclusions if required.

### Launch at Startup

Enable in:

**Settings → Hotkeys → Launch Avelyn at system login**

This adds an entry under:

```text
HKCU\Software\Microsoft\Windows\CurrentVersion\Run
```

---

## 🔧 CLI Flags

```bash
python main.py --debug
python main.py --test-clipboard
python main.py --test-ai
python main.py --version
```

---

## 📦 Building a Standalone Executable

Install PyInstaller:

```bash
pip install pyinstaller
```

### macOS (.app)

```bash
pyinstaller \
  --onefile \
  --windowed \
  --name "Avelyn" \
  --icon assets/icon.icns \
  --add-data "assets:assets" \
  main.py
```

Output:

```text
dist/Avelyn.app
```

### Windows (.exe)

```powershell
pyinstaller `
  --onefile `
  --windowed `
  --name "Avelyn" `
  --icon assets/icon.ico `
  --add-data "assets;assets" `
  main.py
```

Output:

```text
dist\Avelyn.exe
```

---

## 🗂 Configuration File

Location:

```text
~/.avelyn/config.json
```

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

```text
User selects text anywhere
        ↓
Presses Ctrl+Shift+E
        ↓
Avelyn saves clipboard
        ↓
Simulates Ctrl+C → copies selection
        ↓
Reads clipboard text
        ↓
Opens floating popup
        ↓
Streams AI response
        ↓
User clicks "Replace Text"
        ↓
Sets enhanced text to clipboard
        ↓
Simulates Ctrl+V
        ↓
Original clipboard restored
```

---

## 🤝 Troubleshooting

| Problem                     | Fix                                             |
| --------------------------- | ----------------------------------------------- |
| Hotkey not detected (macOS) | Grant Accessibility permission                  |
| API key not set             | Configure provider settings                     |
| Clipboard unchanged         | Ensure text is selected                         |
| Ollama connection refused   | Run `ollama serve`                              |
| PyQt6 import error          | Install PyQt6 in the active virtual environment |

---

# Contribution Guidelines

Thank you for your interest in contributing to **Avelyn**. Contributions from the open-source community are highly valued and help improve the application.

## How to Contribute

### 1. Fork the Repository

Fork the repository to your GitHub account.

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/Avelyn.git
cd Avelyn
```

### 3. Create a Branch

```bash
git checkout -b your-feature-name
```

### 4. Make Changes

Implement your feature, improvement, bug fix, or documentation update.

### 5. Test

Before submitting:

* Verify functionality works as expected
* Ensure no regressions are introduced
* Test on supported platforms when possible

### 6. Update Documentation

Update README and documentation for any user-facing changes.

### 7. Commit Changes

```bash
git commit -m "Add feature/fix: Describe your changes here"
```

### 8. Push Changes

```bash
git push origin your-feature-name
```

### 9. Open a Pull Request

Include:

* Clear title
* Detailed description
* Screenshots (if UI related)
* Testing notes

### 10. Code Review

Address feedback and requested changes promptly.

### 11. Merge

After approval, your contribution will be merged into the project.

## Development Guidelines

* Follow existing project structure
* Maintain code readability
* Avoid unnecessary dependencies
* Preserve cross-platform compatibility
* Write clear commit messages

## Reporting Issues

Before creating a new issue:

1. Search existing issues
2. Verify the problem is reproducible
3. Include logs, screenshots, and reproduction steps

## Questions

Feel free to open an issue or discussion for questions regarding development or contributions.

Thank you for helping make **Avelyn** better.

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

*Built with ❤ using Python, PyQt6, pynput, and modern AI models.*
