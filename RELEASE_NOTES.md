# Avelyn Windows Beta v1 (v1.0.0-beta)

Welcome to the first beta release of **Avelyn** for Windows! 

Avelyn is a private, local-first AI writing assistant designed to work where you write. It intercepts selection hotkeys, provides a premium command palette overlay, runs AI transformations using a local model, and automatically replaces your text in-line.

---

## ✦ Core Features

*   **100% Local-First AI**: Runs using local models via Ollama. No cloud APIs, no external network requests, and your data never leaves your device.
*   **Automatic Setup**: Launches a first-run setup wizard that downloads Ollama silently, initializes the service, and pulls the `gemma3:4b` writing model.
*   **Global Hotkey Palette**: Highlight text in any application (Notepad, Word, VS Code, browsers) and press **`Ctrl+Shift+E`** to bring up the Avelyn command overlay.
*   **Smart In-Line Replacements**: Choose from 14 professional presets (Professional Email, Smart Assist, Fix Grammar, LinkedIn Post) and have the selected text automatically replaced instantly.

---

## ⚙️ How to Install & Run

1.  Download `Avelyn-Windows-Beta-v1.zip` from the assets section below.
2.  Extract the ZIP archive to a folder of your choice (e.g. `C:\Users\<User>\AppData\Local\Programs\Avelyn`).
3.  Double-click **`Avelyn.exe`** to launch the application.
4.  Follow the setup wizard to download and pull the local AI engine. Once completed, Avelyn will run silently in your System Tray.

---

## ⚠ Known Limitations

*   **Physical Key Hold Delay**: When triggering the hotkey (`Ctrl+Shift+E`), please release the keys quickly. If modifiers are held down physically during the virtual paste operation, Windows might occasionally block focus restoration.
*   **System Tray Menu UX**: Left-clicking the taskbar tray icon displays the context menu. To open the main **Settings** window, **double-click** the tray icon.
*   **False Positive Alerts**: As this binary is a custom-packaged Python application, Windows Defender or SmartScreen may show an warning during first launch. You can click "Run anyway" safely.

---

## 💬 Feedback & Bug Reports

Please report any bugs, issues, or suggestions on our GitHub Issues page. Mention **Windows Beta** in your issue title and attach log files found in:
`%USERPROFILE%\.avelyn\config.json` and `%USERPROFILE%\.avelyn\app.log`
