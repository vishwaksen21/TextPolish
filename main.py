"""
TextPolish — Entry Point
=========================
Bootstraps the entire application:
  1. Parses CLI flags (--debug, --test-clipboard, --test-ai).
  2. Initialises settings, clipboard manager, AI processor.
  3. Checks platform-specific requirements (Accessibility on macOS).
  4. Creates the PyQt6 application, system tray, and enhancement popup.
  5. Starts the global hotkey listener thread.
  6. Enters the Qt event loop.
  7. On exit, cleanly shuts down threads and restores the clipboard.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
import requests

from PyQt6.QtCore    import Qt, QTimer, QObject, QThread, pyqtSignal
from PyQt6.QtGui     import QFont, QFontDatabase
from PyQt6.QtWidgets import QApplication, QMessageBox

from logger          import logger, setup_logger
from settings        import Settings
from clipboard_manager import ClipboardManager
from ai_processor    import AIProcessor
from hotkeys         import HotkeyBridge, HotkeyManager
from ui              import EnhancementPopup, SettingsWindow, SystemTrayIcon, AIWorker
import platform_handler as ph


# ── Version ───────────────────────────────────────────────────────────────────
__version__ = "1.0.0"
APP_NAME    = "TextPolish"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="textpolish",
        description="AI-powered global text enhancer.",
    )
    parser.add_argument("--debug",           action="store_true", help="Enable DEBUG logging.")
    parser.add_argument("--test-clipboard",  action="store_true", help="Smoke-test clipboard and exit.")
    parser.add_argument("--test-ai",         action="store_true", help="Smoke-test AI connection and exit.")
    parser.add_argument("--version",         action="version",    version=f"%(prog)s {__version__}")
    return parser.parse_args()


# ── Smoke tests (--test-* flags) ──────────────────────────────────────────────

def run_clipboard_test() -> None:
    print("=== Clipboard smoke test ===")
    import pyperclip
    mgr = ClipboardManager()
    mgr.save()
    original = mgr.get()
    print(f"  Original clipboard: {repr(original[:40])}")
    mgr.set("TextPolish clipboard test 🟣")
    result = mgr.get()
    print(f"  After set:         {repr(result)}")
    mgr.restore()
    restored = mgr.get()
    print(f"  After restore:     {repr(restored[:40])}")
    assert result == "TextPolish clipboard test 🟣", "SET failed"
    assert restored == original, "RESTORE failed"
    print("  ✓ All clipboard operations passed.\n")


def run_ai_test(settings: Settings) -> None:
    print("=== AI connection smoke test ===")
    proc = AIProcessor(settings)
    result = proc.test_connection()
    print(f"  Response: {result[:120]}")
    print("  ✓ AI connection OK.\n")


# ── macOS Accessibility guard ─────────────────────────────────────────────────

def ensure_macos_accessibility(app: QApplication) -> None:
    """
    On macOS, check for Accessibility permission.  If not granted, show a
    dialog explaining how to grant it and offer to open System Settings.
    The user can still proceed (the hotkey just won't work until they grant it).
    """
    if not ph.IS_MACOS:
        return

    if ph.check_accessibility():
        logger.info("macOS Accessibility permission: granted.")
        return

    logger.warning("macOS Accessibility permission NOT granted.")
    msg = QMessageBox()
    msg.setWindowTitle(f"{APP_NAME} — Accessibility Required")
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setText(
        "<b>Accessibility permission is required</b> for TextPolish to detect "
        "global hotkeys and simulate copy/paste.<br><br>"
        "Please grant access in:<br>"
        "<b>System Settings → Privacy &amp; Security → Accessibility</b><br><br>"
        "Add <b>TextPolish</b> (or <b>python</b>) to the list and enable it."
    )
    msg.setStandardButtons(
        QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Open
    )
    msg.button(QMessageBox.StandardButton.Open).setText("Open System Settings")
    reply = msg.exec()
    if reply == QMessageBox.StandardButton.Open:
        ph.request_accessibility()


# ── Ollama Startup Worker ─────────────────────────────────────────────────────

class OllamaStartupWorker(QThread):
    finished_ok = pyqtSignal()
    model_missing = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self._settings = settings
        
    def run(self):
        host = self._settings.ollama_host.rstrip('/')
        model = self._settings.ollama_model
        
        # Initial check
        try:
            resp = requests.get(f"{host}/api/tags", timeout=2)
            resp.raise_for_status()
            logger.info("Ollama server detected.")
            self._check_model(resp.json(), model)
            return
        except Exception:
            logger.info("Ollama not running. Launching automatically...")
            ph.start_ollama_app()
            
        # Polling loop
        import time
        max_retries = 15
        for i in range(max_retries):
            time.sleep(1)
            try:
                resp = requests.get(f"{host}/api/tags", timeout=2)
                resp.raise_for_status()
                logger.info("Ollama startup successful.")
                self._check_model(resp.json(), model)
                return
            except Exception:
                continue
                
        # If we reach here, it failed.
        self.error_occurred.emit("Ollama local AI server could not be started automatically. Please launch Ollama manually.")
        
    def _check_model(self, data: dict, model: str):
        available_models = [m.get("name", "") for m in data.get("models", [])]
        if model not in available_models and f"{model}:latest" not in available_models:
            logger.warning("Model '%s' not found.", model)
            self.model_missing.emit(model)
        else:
            self.finished_ok.emit()



# ── Auto Replacer ─────────────────────────────────────────────────────────────

class AutoReplacer(QObject):
    """Handles silent background text replacement without a popup."""
    
    def __init__(self, settings: Settings, processor: AIProcessor, clipboard: ClipboardManager, tray: SystemTrayIcon) -> None:
        super().__init__()
        self._settings = settings
        self._processor = processor
        self._clipboard = clipboard
        self._tray = tray
        self._worker: AIWorker | None = None
        
    def start_replacement(self, text: str) -> None:
        if self._worker is not None and self._worker.isRunning():
            logger.warning("AutoReplacer is already running. Ignoring hotkey.")
            return
            
        logger.info("Auto-replace triggered for text: %r", text[:30])
        # clipboard.save() was already done by hotkeys.py
        
        self._worker = AIWorker(self._processor, text, self._settings.default_mode)
        self._worker.finished.connect(self._on_ai_finished)
        self._worker.error_occurred.connect(self._on_error)
        self._worker.start()
        
    def _on_ai_finished(self, enhanced_text: str) -> None:
        if not enhanced_text:
            self._clipboard.restore()
            self._worker = None
            return

        self._clipboard.set(enhanced_text)

        logger.info("Prepared enhanced text for inline replacement.")

        # Delay paste slightly for clipboard stabilization
        QTimer.singleShot(150, self._perform_paste)

    def _perform_paste(self) -> None:
        try:
            ph.paste_text()
            logger.info("Auto-replaced selected text successfully.")
        finally:
            # Restore clipboard AFTER paste fully completes
            QTimer.singleShot(1800, self._restore_clipboard)
        
    def _restore_clipboard(self) -> None:
        self._clipboard.restore()
        self._worker = None
        
    def _on_error(self, msg: str) -> None:
        logger.error("AutoReplace failed: %s", msg)
        self._tray.notify(APP_NAME, f"AI Error: {msg[:50]}")
        self._clipboard.restore()
        self._worker = None


# ── Application class ─────────────────────────────────────────────────────────

class TextPolishApp:
    """
    Root application object.  Owns all components and wires them together.
    """

    def __init__(self, args: argparse.Namespace) -> None:
        self._args = args

        # ── Core services ─────────────────────────────────────────────────────
        self._settings  = Settings()
        self._clipboard = ClipboardManager()
        self._processor = AIProcessor(self._settings)

        # ── Qt application ────────────────────────────────────────────────────
        self._qapp = QApplication(sys.argv)
        self._qapp.setApplicationName(APP_NAME)
        self._qapp.setApplicationVersion(__version__)
        self._qapp.setQuitOnLastWindowClosed(False)   # Keep alive as tray app

        # Apply stylesheet.
        from ui import get_qss
        self._qapp.setStyleSheet(get_qss(self._settings.theme))

        # Load Inter font if available.
        _load_font()

        # ── macOS permission check ────────────────────────────────────────────
        ensure_macos_accessibility(self._qapp)

        # ── Ollama validation (Non-blocking) ──────────────────────────────────
        self._startup_worker = OllamaStartupWorker(self._settings, self._qapp)
        self._startup_worker.model_missing.connect(self._on_model_missing)
        self._startup_worker.error_occurred.connect(self._on_ollama_error)
        self._startup_worker.start()

        # ── UI components ─────────────────────────────────────────────────────
        self._tray    = SystemTrayIcon(self._settings)
        self._popup   = EnhancementPopup(self._settings, self._processor, self._clipboard)
        self._auto_replacer = AutoReplacer(self._settings, self._processor, self._clipboard, self._tray)
        self._settings_win: SettingsWindow | None = None

        # ── Hotkey bridge (thread → Qt signal) ────────────────────────────────
        self._bridge  = HotkeyBridge()
        self._hotkeys = HotkeyManager(self._bridge, self._settings.hotkey, self._clipboard)

        self._wire_signals()

    def _wire_signals(self) -> None:
        # Hotkey bridge → replacement logic
        self._bridge.text_captured.connect(self._on_text_captured)
        self._bridge.nothing_selected.connect(self._on_nothing_selected)
        self._bridge.error_occurred.connect(self._on_hotkey_error)

        # Tray → actions
        self._tray.open_settings_requested.connect(self._show_settings)
        self._tray.quit_requested.connect(self._quit)
        self._tray.pause_toggled.connect(self._hotkeys.set_enabled)

    def run(self) -> int:
        """Start all services and enter the Qt event loop."""
        # Start hotkey listener.
        if self._settings.hotkey_enabled:
            self._hotkeys.start()
        else:
            logger.info("Hotkey listener disabled in settings.")

        # Show tray icon.
        self._tray.show()
        self._tray.notify(
            APP_NAME,
            f"Running in background. Press {self._settings.shortcut_display} "
            "to enhance selected text.",
        )

        logger.info("%s v%s started. Platform: %s", APP_NAME, __version__, ph.platform_name())
        return self._qapp.exec()

    # ── Slots / handlers ──────────────────────────────────────────────────────

    def _show_settings(self) -> None:
        if self._settings_win is None:
            self._settings_win = SettingsWindow(self._settings, self._processor)
            self._settings_win.settings_changed.connect(self._on_settings_changed)

        from ui import get_qss
        self._settings_win.setStyleSheet(get_qss(self._settings.theme))
        self._settings_win.show()
        self._settings_win.raise_()
        self._settings_win.activateWindow()

    def _on_settings_changed(self) -> None:
        """Reload hotkey listener and re-apply stylesheet after settings save."""
        from ui import get_qss
        self._qapp.setStyleSheet(get_qss(self._settings.theme))
        # Restart hotkey with potentially new shortcut.
        self._hotkeys.restart(self._settings.hotkey)
        logger.info("Settings reloaded; hotkey restarted.")

    def _on_text_captured(self, text: str) -> None:
        if self._settings.auto_replace:
            self._auto_replacer.start_replacement(text)
        else:
            self._popup.show_for_text(text)

    def _on_nothing_selected(self) -> None:
        self._tray.notify(
            APP_NAME,
            "No text selected. Select some text first, then press the shortcut.",
        )

    def _on_model_missing(self, model: str) -> None:
        self._tray.notify(APP_NAME, f"AI Model missing. Please run: ollama pull {model}", msecs=10000)
        
    def _on_ollama_error(self, msg: str) -> None:
        self._tray.notify(APP_NAME, msg, msecs=10000)

    def _on_hotkey_error(self, msg: str) -> None:
        logger.error("Hotkey error: %s", msg)
        self._tray.notify(APP_NAME, f"Hotkey error: {msg[:80]}")

    def _quit(self) -> None:
        logger.info("Shutting down %s.", APP_NAME)
        self._hotkeys.stop()
        try:
            self._clipboard.restore()
        except Exception:
            pass
        self._qapp.quit()


# ── Font loader ───────────────────────────────────────────────────────────────

def _load_font() -> None:
    """Attempt to load Inter from the assets directory."""
    font_dir = Path(__file__).parent / "assets"
    for ttf in font_dir.glob("Inter*.ttf"):
        QFontDatabase.addApplicationFont(str(ttf))


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    args = parse_args()

    if args.debug:
        setup_logger(debug=True)
        logger.debug("Debug mode enabled.")

    # ── CLI smoke tests (no GUI) ──────────────────────────────────────────────
    if args.test_clipboard:
        run_clipboard_test()
        sys.exit(0)

    if args.test_ai:
        settings = Settings()
        run_ai_test(settings)
        sys.exit(0)

    # ── Full application ──────────────────────────────────────────────────────
    app = TextPolishApp(args)
    sys.exit(app.run())


if __name__ == "__main__":
    main()
