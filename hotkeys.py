"""
TextPolish — Global Hotkey Manager
====================================
Uses pynput to listen for a global keyboard shortcut across all applications.
When the shortcut fires, it:
  1. Saves the current clipboard state.
  2. Simulates Ctrl+C / Cmd+C to copy whatever the user has selected.
  3. Waits for the clipboard to update.
  4. Emits a Qt signal with the captured text so the main thread can
     show the enhancement popup.

The listener runs in a daemon thread (managed by pynput) so it never
blocks the Qt event loop.
"""

from __future__ import annotations

import sys
import time
import threading
from typing import Callable, Optional

from PyQt6.QtCore import QObject, pyqtSignal

from clipboard_manager import ClipboardManager
from platform_handler import copy_selection
from logger import logger


class HotkeyBridge(QObject):
    """
    Qt bridge that safely crosses the thread boundary between the pynput
    listener thread and the Qt main thread.

    Connect to `text_captured` to receive the selected text when the
    hotkey fires.  Qt's queued connection mechanism ensures the slot runs
    in the receiver's thread (the Qt event loop).
    """

    # Emitted with the captured text after a successful hotkey + copy cycle.
    text_captured = pyqtSignal(str)

    # Emitted when the hotkey fires but nothing was selected (empty clipboard).
    nothing_selected = pyqtSignal()

    # Emitted on any unexpected error.
    error_occurred = pyqtSignal(str)


class HotkeyManager:
    """
    Manages the pynput global hotkey listener lifecycle.

    Usage::

        bridge = HotkeyBridge()
        bridge.text_captured.connect(show_popup)
        manager = HotkeyManager(bridge, hotkey="<ctrl>+<shift>+e")
        manager.start()
        # ... application runs ...
        manager.stop()
    """

    def __init__(
        self,
        bridge: HotkeyBridge,
        hotkey: str = "<ctrl>+<shift>+e",
        clipboard_manager: Optional[ClipboardManager] = None,
    ) -> None:
        self._bridge = bridge
        self._hotkey = hotkey
        self._clipboard = clipboard_manager or ClipboardManager()
        self._listener = None        # pynput GlobalHotKeys instance
        self._enabled = True         # Can be toggled to pause without stopping
        self._lock = threading.Lock()

    # ── Listener lifecycle ────────────────────────────────────────────────────

    def start(self) -> None:
        """Start the global hotkey listener in a daemon thread."""
        try:
            from pynput import keyboard as kb              # type: ignore[import]
        except ImportError:
            logger.error("pynput is not installed. Run: pip install pynput")
            return

        hotkeys = {self._hotkey: self._on_hotkey_fired}

        try:
            self._listener = kb.GlobalHotKeys(hotkeys)
            self._listener.daemon = True
            self._listener.start()
            logger.info("Hotkey listener started: %s", self._hotkey)
        except Exception as exc:                          # noqa: BLE001
            logger.error("Failed to start hotkey listener: %s", exc)
            self._bridge.error_occurred.emit(
                f"Could not register global hotkey '{self._hotkey}'.\n"
                f"Error: {exc}\n\n"
                "On macOS, grant Accessibility permission in\n"
                "System Settings → Privacy & Security → Accessibility."
            )

    def stop(self) -> None:
        """Stop the hotkey listener."""
        if self._listener is not None:
            try:
                self._listener.stop()
                logger.info("Hotkey listener stopped.")
            except Exception as exc:                      # noqa: BLE001
                logger.warning("Error stopping hotkey listener: %s", exc)
            self._listener = None

    def restart(self, new_hotkey: Optional[str] = None) -> None:
        """Restart the listener, optionally with a new hotkey string."""
        self.stop()
        if new_hotkey:
            self._hotkey = new_hotkey
        self.start()

    # ── Pause / resume ────────────────────────────────────────────────────────

    def set_enabled(self, enabled: bool) -> None:
        """Pause (False) or resume (True) hotkey processing."""
        with self._lock:
            self._enabled = enabled
        state = "resumed" if enabled else "paused"
        logger.info("Hotkey %s.", state)

    @property
    def is_enabled(self) -> bool:
        return self._enabled

    # ── Core callback ─────────────────────────────────────────────────────────

    def _on_hotkey_fired(self) -> None:
        """
        Called by pynput in its own thread when the hotkey is pressed.

        Sequence:
          1. Check if hotkey processing is enabled.
          2. Snapshot current clipboard (for restore later).
          3. Simulate Ctrl/Cmd+C to copy the current selection.
          4. Read the new clipboard content with retry logic.
          5. Emit the appropriate Qt signal (thread-safe via queued connection).
        """
        with self._lock:
            if not self._enabled:
                logger.debug("Hotkey fired but processing is paused.")
                return

        logger.debug("Hotkey fired.")

        import uuid
        try:
            # 1. Save what's currently on the clipboard.
            self._clipboard.save()
            previous = self._clipboard.saved_content or ""
            
            # 1.5 Inject a temporary unique marker to definitively detect if Cmd+C worked.
            # Without this, selecting the exact same text again makes the clipboard look unchanged!
            temp_marker = f"__TEXTPOLISH_{uuid.uuid4().hex}__"
            self._clipboard.set(temp_marker)

            # 2. Small delay to let any key-up events settle before we send Ctrl+C.
            time.sleep(0.05)

            # 3. Simulate copy.
            copy_selection()

            # 4. Read clipboard with retry (wait for it to change from temp_marker)
            text = self._clipboard.read_after_copy(previous=temp_marker)
            
            logger.info("Clipboard after copy: '%s'", text)

            # 5. Signal Qt.
            if not text or len(text.strip()) < 3:
                logger.warning("Selection validation failed: length %d, content: %r", len(text) if text else 0, text)
                self._bridge.nothing_selected.emit()
            else:
                logger.info("Captured %d chars for enhancement. Preview: %r", len(text), text[:50])
                self._bridge.text_captured.emit(text)

        except Exception as exc:                          # noqa: BLE001
            logger.error("Error in hotkey callback: %s", exc)
            self._bridge.error_occurred.emit(str(exc))
