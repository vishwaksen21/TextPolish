# Avelyn Windows Beta — Tester Guide

Thank you for participating in the Avelyn Windows Beta testing program! This guide covers setup, standard workflows, and troubleshooting tips.

---

## 🚀 Getting Started

### 1. Extraction
Extract the contents of `Avelyn-Windows-Beta-v1.zip` to a folder on your local drive (e.g. `C:\Avelyn`).

### 2. Startup
Double-click `Avelyn.exe` inside the folder.
*   *Note*: If Windows SmartScreen blocks the app, click **More Info** -> **Run anyway**.

### 3. Setup Wizard
The wizard will check for a local Ollama server. If not found:
*   It will automatically download Ollama to `%LOCALAPPDATA%\Avelyn\Ollama`.
*   It will launch the Ollama service silently.
*   It will download the `gemma3:4b` writing model (~2.5 GB). 
*   *Keep the window open during this download.*

Once completed, Avelyn will run in the background as a tray icon in your taskbar.

---

## 📝 Testing the Core Workflow

Perform the following workflow to verify end-to-end functionality:

1.  Open **Notepad** (or Word, VS Code, Slack, or any web browser).
2.  Write some draft text (e.g., `"tell john i will meet him at 3pm tomorrow"`).
3.  Highlight the text.
4.  Press **`Ctrl+Shift+E`** on your keyboard, then release the keys.
5.  Wait for the overlay menu to appear.
6.  Select **"Professional Email"** (or another preset).
7.  The AI will generate the revised version locally, and the highlighted text will automatically update in place.

---

## 🛠️ Settings & custom hotkeys

*   To open the settings panel, **double-click** the Avelyn system tray icon.
*   In settings, you can toggle between **Light/Dark themes**, configure the active **AI Model**, or disable **Auto-Replace** (which copies output to your clipboard instead of replacing highlighted text in-line).

---

## 🐛 Troubleshooting & Logs

If the application crashes or text replacement fails:

1.  **Check logs**: Logs are saved in `%USERPROFILE%\.avelyn\app.log`.
2.  **Verify Ollama Port**: Open your web browser and go to `http://127.0.0.1:11434`. You should see *"Ollama is running"*.
3.  **Submit Reports**: Copy the log text and submit it to the project coordinator.
