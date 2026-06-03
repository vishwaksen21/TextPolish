"""
Avelyn — Entry Point
====================
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
from installer import Installer

class InstallWorker(QThread):
    """
    Background thread: download Ollama, start server, pull model.
    Never blocks the UI thread.
    """
    progress  = pyqtSignal(int, str)   # (percent 0-100, status_text)
    finished  = pyqtSignal(bool, str)  # (success, error_message)

    def __init__(self, model_name: str, parent=None) -> None:
        super().__init__(parent)
        self._model_name = model_name

    def run(self) -> None:
        try:
            def cb(percent: int, text: str) -> None:
                self.progress.emit(percent, text)

            cb(2, "Checking installation...")

            # Step 1: Download & extract if binary is missing
            if Installer.needs_installation():
                Installer.download_and_extract_ollama(cb)
            else:
                cb(48, "Ollama already installed.")

            # Step 2: Start the server
            cb(50, "Starting Ollama...")
            Installer.start_ollama()

            # Step 3: Wait for server to be ready
            cb(52, "Waiting for server...")
            if not Installer.verify_installation(max_wait=30):
                raise RuntimeError(
                    "Ollama server did not start in time.\n"
                    "Please launch Ollama manually and restart Avelyn."
                )

            # Step 4: Pull model
            Installer.pull_model(self._model_name, cb)

            self.finished.emit(True, "")
        except Exception as exc:
            logger.error("Installation failed: %s", exc)
            self.finished.emit(False, str(exc))
from clipboard_manager import ClipboardManager
from ai_processor    import AIProcessor
from hotkeys         import HotkeyBridge, HotkeyManager
from ui              import (
    EnhancementPopup, SettingsWindow, SystemTrayIcon, 
    AIWorker, ToastOverlay, CommandPalette, InstallerOverlay
)
from onboarding      import OnboardingWindow
from permissions     import PermissionManager
import platform_handler as ph


# ── Version ───────────────────────────────────────────────────────────────────
__version__ = "1.0.0"
APP_NAME    = "Avelyn"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="avelyn",
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
    mgr.set("Avelyn clipboard test 🟣")
    result = mgr.get()
    print(f"  After set:         {repr(result)}")
    mgr.restore()
    restored = mgr.get()
    print(f"  After restore:     {repr(restored[:40])}")
    assert result == "Avelyn clipboard test 🟣", "SET failed"
    assert restored == original, "RESTORE failed"
    print("  ✓ All clipboard operations passed.\n")


def run_ai_test(settings: Settings) -> None:
    print("=== AI connection smoke test ===")
    proc = AIProcessor(settings)
    result = proc.test_connection()
    print(f"  Response: {result[:120]}")
    print("  ✓ AI connection OK.\n")


# ── Auto Replacer ─────────────────────────────────────────────────────────────

class CommandPaletteWorkflow(QObject):
    """Handles the Command Palette UI and background text replacement."""
    
    def __init__(self, settings: Settings, processor: AIProcessor, clipboard: ClipboardManager, tray: SystemTrayIcon) -> None:
        super().__init__()
        self._settings = settings
        self._processor = processor
        self._clipboard = clipboard
        self._tray = tray
        
        self._palette = CommandPalette()
        self._toast = ToastOverlay()
        self._worker: AIWorker | None = None
        
        self._current_text = ""
        self._palette_is_hidden = True   # tracks whether palette animation has completed
        self._pending_paste    = False   # enhanced text is ready, waiting for palette close

        self._palette.action_selected.connect(self._on_action_selected)
        self._palette.cancelled.connect(self._on_cancelled)
        self._palette.hidden.connect(self._on_palette_hidden)
        
    def show_capturing(self) -> None:
        self._toast.show_message("◴ Capturing Selection...", loading=True)
        
    def start_workflow(self, text: str) -> None:
        if self._worker is not None and self._worker.isRunning():
            logger.warning("Workflow is already running. Ignoring hotkey.")
            return
            
        logger.info("Command Palette triggered for text: %r", text[:20])
        self._current_text = text
        self._palette_is_hidden = False
        self._pending_paste = False
        self._toast.hide()
        # The active app bundle was ALREADY captured by platform_handler.copy_selection() 
        # before any UI was shown. Do not re-record it here, or it will record Avelyn!
        self._palette.show_palette(selected_text=text)
        
    def _on_action_selected(self, mode: str, custom_instruction: str) -> None:
        logger.info("MODE_SELECTED")
        logger.info("START_REPLACEMENT")
        logger.info("Command Palette action selected: %s (custom: %s)", mode, custom_instruction)
        self._toast.show_message("✦ Enhancing with AI...", loading=True)
        
        self._worker = AIWorker(self._processor, self._current_text, mode, custom_instruction)
        logger.info("AIWORKER_CREATED")
        self._worker.finished.connect(self._on_ai_finished)
        self._worker.error_occurred.connect(self._on_error)
        self._worker.start()
        logger.info("AIWORKER_STARTED")
        
    def _on_cancelled(self) -> None:
        logger.info("Command Palette cancelled by user.")
        self._restore_clipboard()
        
    def _on_ai_finished(self, enhanced_text: str) -> None:
        if not enhanced_text:
            self._toast.show_message("⚠ Empty response", error=True)
            self._clipboard.restore()
            self._worker = None
            return

        self._clipboard.set(enhanced_text)
        logger.info("CLIPBOARD_UPDATED")
        logger.info("Enhanced text ready. Palette hidden: %s", self._palette_is_hidden)

        if self._palette_is_hidden:
            # Palette already closed — paste after focus-settle delay.
            # 400ms gives macOS window manager time to return focus to the original app.
            QTimer.singleShot(400, self._perform_paste)
        else:
            # Palette still animating — set flag so _on_palette_hidden triggers paste
            self._pending_paste = True

    def _on_palette_hidden(self) -> None:
        """Fires after palette fade-out animation completes."""
        self._palette_is_hidden = True
        if self._pending_paste:
            self._pending_paste = False
            logger.info("Palette closed. Triggering paste now.")
            # Give macOS 400ms to fully return focus to the original app after
            # the palette window closes. The AppKit activation + window manager
            # focus transfer needs this time to complete before we paste.
            QTimer.singleShot(400, self._perform_paste)

    def _perform_paste(self) -> None:
        try:
            self._toast.show_message("◴ Replacing Text...", loading=True)
            # NOTE: Do NOT call QApplication.processEvents() here.
            # It flushes pending Qt events which may include window-activation
            # events that bring Avelyn back to the foreground right before
            # Cmd+V is sent — causing the paste to land in Avelyn instead of Chrome.
            
            ph.paste_text()
            logger.info("PASTE_TRIGGERED")
            logger.info("Auto-replaced selected text successfully.")
            # Show toast 400ms after paste so it doesn't disrupt Cmd+V
            QTimer.singleShot(400, lambda: [self._toast.show_message("✓ Complete", success=True), logger.info("REPLACEMENT_COMPLETE")])
        finally:
            # Restore clipboard well after paste completes
            QTimer.singleShot(2000, self._restore_clipboard)
        
    def _restore_clipboard(self) -> None:
        self._clipboard.restore()
        self._worker = None
        self._current_text = ""
        
    def _on_error(self, msg: str) -> None:
        self._toast.show_message("⚠ Error", error=True)
        logger.error("Workflow failed: %s", msg)
        
        if "DIAGNOSTIC RESULTS:" in msg:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(None, "Diagnostic Mode", msg)
        else:
            self._tray.notify(APP_NAME, f"AI Error: {msg[:50]}")
            
        self._clipboard.restore()
        self._worker = None


# ── Application class ─────────────────────────────────────────────────────────

class AvelynApp:
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
        self._qapp = QApplication.instance()
        if self._qapp is None:
            self._qapp = QApplication(sys.argv)
        self._qapp.setApplicationName(APP_NAME)
        self._qapp.setApplicationVersion(__version__)
        self._qapp.setQuitOnLastWindowClosed(False)   # Keep alive as tray app

        # Apply stylesheet.
        from ui import get_qss
        self._qapp.setStyleSheet(get_qss(self._settings.theme))
        self._current_theme = self._settings.theme
        self._current_hotkey = self._settings.hotkey

        # Load Inter font if available.
        _load_font()

        # ── UI components ─────────────────────────────────────────────────────
        self._tray    = SystemTrayIcon(self._settings)
        self._popup   = EnhancementPopup(self._settings, self._processor, self._clipboard)
        self._workflow = CommandPaletteWorkflow(self._settings, self._processor, self._clipboard, self._tray)
        self._settings_win: SettingsWindow | None = None

        # ── Hotkey bridge (thread → Qt signal) ────────────────────────────────
        self._bridge  = HotkeyBridge()
        self._hotkeys = HotkeyManager(self._bridge, self._settings.hotkey, self._clipboard)

        self._wire_signals()

    def _wire_signals(self) -> None:
        # Hotkey bridge → replacement logic
        self._bridge.hotkey_pressed.connect(self._workflow.show_capturing)
        self._bridge.text_captured.connect(self._on_text_captured)
        self._bridge.nothing_selected.connect(self._on_nothing_selected)
        self._bridge.error_occurred.connect(self._on_hotkey_error)

        # Tray → actions
        self._tray.open_settings_requested.connect(self._show_settings)
        self._tray.quit_requested.connect(self._quit)
        self._tray.pause_toggled.connect(self._hotkeys.set_enabled)

    def run(self) -> int:
        """Start all services and enter the Qt event loop."""
        # On macOS, verify required permissions even if first_run_completed is True.
        # This prevents silent failures in packaged mode if permissions are missing.
        permissions_ok = True
        if ph.IS_MACOS:
            permissions_ok = PermissionManager.check_accessibility() and PermissionManager.check_input_monitoring()

        if not self._settings.get("first_run_completed", False) or not permissions_ok:
            logger.info("First run or missing permissions detected (permissions_ok=%s). Starting onboarding...", permissions_ok)
            self._start_onboarding()
        else:
            self._finish_startup()

        return self._qapp.exec()

    def _start_onboarding(self) -> None:
        self._onboarding = OnboardingWindow(self._settings, self._processor)
        self._onboarding.setup_complete.connect(self._on_setup_complete)
        self._onboarding.show()

    def _on_setup_complete(self) -> None:
        self._onboarding.deleteLater()
        self._onboarding = None
        self._finish_startup()

    def _finish_startup(self) -> None:
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
        
        # Start Ollama background process silently if missing
        import threading
        def background_ollama():
            from installer import Installer
            try:
                Installer.start_ollama()
            except:
                pass
        threading.Thread(target=background_ollama, daemon=True).start()

        logger.info("%s v%s started. Platform: %s", APP_NAME, __version__, ph.platform_name())
        logger.info("PACKAGED_MODE=%s", getattr(sys, 'frozen', False))

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
        """Reload hotkey listener and re-apply stylesheet after settings save if changed."""
        theme = self._settings.theme
        if theme != getattr(self, "_current_theme", None):
            self._current_theme = theme
            from ui import get_qss
            self._qapp.setStyleSheet(get_qss(theme))
            logger.info("Theme updated to: %s", theme)

        hotkey = self._settings.hotkey
        if hotkey != getattr(self, "_current_hotkey", None):
            self._current_hotkey = hotkey
            self._hotkeys.restart(hotkey)
            logger.info("Settings reloaded; hotkey restarted with: %s", hotkey)

    def _on_text_captured(self, text: str) -> None:
        if self._settings.auto_replace:
            self._workflow.start_workflow(text)
        else:
            self._popup.show_for_text(text)

    def _on_nothing_selected(self) -> None:
        if self._settings.auto_replace:
            self._workflow._toast.hide()
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
        if "Accessibility" in msg or "pynput" in msg:
            self._show_accessibility_dialog()
        else:
            self._tray.notify(APP_NAME, f"Hotkey error: {msg[:80]}")

    def _show_accessibility_dialog(self) -> None:
        msg = QMessageBox()
        msg.setWindowTitle(f"{APP_NAME} — Permissions Revoked")
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(
            "<b>macOS has revoked Accessibility permissions for Avelyn.</b><br><br>"
            "This usually happens after an update. The global hotkey has been disabled.<br><br>"
            "To fix this:<br>"
            "1. Open System Settings<br>"
            "2. Remove (minus button) the old Avelyn entry<br>"
            "3. Add it back again and ensure the switch is on."
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Open)
        msg.button(QMessageBox.StandardButton.Open).setText("Open System Settings")
        
        if msg.exec() == QMessageBox.StandardButton.Open:
            PermissionManager.request_accessibility()

    def _quit(self) -> None:
        logger.info("Shutting down %s.", APP_NAME)
        self._hotkeys.stop()
        try:
            self._clipboard.restore()
        except Exception:
            pass
        self._qapp.quit()


# ── Font loader ──────────────────────────────────────────────────────────────

def _load_font() -> None:
    """Attempt to load Inter from the assets directory."""
    from utils import get_resource_path
    font_dir = get_resource_path("assets")
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
    settings = Settings()

    needs_install = Installer.needs_installation() or not Installer.is_server_running()

    if needs_install and not settings.get("first_run_completed"):
        # ── First-run installer flow ──────────────────────────────────────────
        logger.info("First run or Ollama missing. Triggering auto-installer...")
        app = QApplication(sys.argv)
        overlay = InstallerOverlay()
        overlay.show()
        QApplication.processEvents()

        model_name = settings.ollama_model
        worker = InstallWorker(model_name)
        worker.progress.connect(overlay.update_progress)

        # Keep references alive (prevent GC)
        _refs = {"overlay": overlay, "worker": worker, "app": app}

        def _on_install_finished(success: bool, error_msg: str) -> None:
            if success:
                overlay.show_success()
                settings.set("first_run_completed", True)
                logger.info("Installation complete. Launching Avelyn...")
                # Show success for 1.5s then launch
                QTimer.singleShot(1500, lambda: _launch_after_install(args))
            else:
                logger.error("Installation failed: %s", error_msg)
                overlay.show_error(error_msg)

        def _on_retry() -> None:
            logger.info("User requested retry...")
            worker2 = InstallWorker(model_name)
            worker2.progress.connect(overlay.update_progress)
            worker2.finished.connect(_on_install_finished)
            _refs["worker2"] = worker2
            overlay.update_progress(0, "Retrying...")
            worker2.start()

        def _launch_after_install(launch_args) -> None:
            tp_app = AvelynApp(launch_args)
            tp_app._finish_startup()
            overlay.hide()
            # app.exec() is already running; just start the app object
            _refs["tp_app"] = tp_app

        overlay.retry_requested.connect(_on_retry)
        worker.finished.connect(_on_install_finished)
        worker.start()
        sys.exit(app.exec())

    elif needs_install and settings.get("first_run_completed"):
        # Ollama installed before but not running — just start it silently
        logger.info("Ollama not running. Starting server silently...")
        try:
            Installer.start_ollama()
        except Exception as exc:
            logger.warning("Could not auto-start Ollama: %s", exc)
        app = AvelynApp(args)
        sys.exit(app.run())

    else:
        app = AvelynApp(args)
        sys.exit(app.run())


if __name__ == "__main__":
    main()
