"""
Avelyn — Global Hotkey Manager
==============================
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
from logger import logger
from platform_handler import IS_MACOS, copy_selection
from settings import Settings

if IS_MACOS:
    try:
        import contextlib
        from pynput._util import darwin
        # PRE-COMPUTE the keyboard context on the MAIN THREAD to avoid TCC trace traps on macOS 14+
        # when the pynput listener tries to call TISGetInputSourceProperty on a background thread.
        with darwin.keycode_context() as _ctx:
            _precomputed_ctx = _ctx

        @contextlib.contextmanager
        def _patched_keycode_context():
            yield _precomputed_ctx

        darwin.keycode_context = _patched_keycode_context
        import pynput.keyboard._darwin as kb_darwin  # type: ignore[import]
        kb_darwin.keycode_context = _patched_keycode_context
        logger.debug("pynput keycode_context patched to avoid macOS background thread crash.")
    except Exception as e:
        logger.warning(f"Failed to patch pynput: {e}")


class HotkeyBridge(QObject):
    """
    Qt bridge that safely crosses the thread boundary between the pynput
    listener thread and the Qt main thread.

    Connect to `text_captured` to receive the selected text when the
    hotkey fires.  Qt's queued connection mechanism ensures the slot runs
    in the receiver's thread (the Qt event loop).
    """

    # Emitted immediately when the hotkey is detected, before copying.
    hotkey_pressed = pyqtSignal()

    # Emitted with the captured text after a successful hotkey + copy cycle.
    text_captured = pyqtSignal(str)

    # Emitted when the hotkey fires but nothing was selected (empty clipboard).
    nothing_selected = pyqtSignal()

    # Emitted on any unexpected error.
    error_occurred = pyqtSignal(str)

    # Emitted with the captured text after a successful PTT copy cycle.
    ptt_text_captured = pyqtSignal(str)


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
        settings: Optional[Settings] = None,
    ) -> None:
        self._bridge = bridge
        self._hotkey = hotkey
        self._clipboard = clipboard_manager or ClipboardManager()
        self._settings = settings
        self._listener = None        # pynput GlobalHotKeys instance
        self._enabled = True         # Can be toggled to pause without stopping
        self._lock = threading.Lock()
        self._is_processing = False

    # ── Listener lifecycle ────────────────────────────────────────────────────

    def start(self) -> None:
        """Start the global hotkey listener in a daemon thread."""
        try:
            from pynput import keyboard as kb              # type: ignore[import]
        except ImportError:
            logger.error("pynput is not installed. Run: pip install pynput")
            return

        hotkeys = {self._hotkey: self._on_hotkey_fired}
        if self._settings and self._settings.get("voice_commands_enabled", False):
            hotkeys["<ctrl>+<shift>+v"] = self._on_ptt_fired

        try:
            self._listener = kb.GlobalHotKeys(hotkeys)
            self._listener.daemon = True
            self._listener.start()
            logger.info("Hotkey listener started: %s (Voice PTT enabled: %s)", 
                        self._hotkey, 
                        self._settings.get("voice_commands_enabled", False) if self._settings else False)
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
        Spawns a background thread immediately to prevent blocking the macOS Quartz Event Tap.
        """
        from utils import PerfTracker
        PerfTracker.reset()
        
        with self._lock:
            if not self._enabled:
                logger.debug("Hotkey fired but processing is paused.")
                return
            if self._is_processing:
                logger.debug("Hotkey fired but already processing.")
                return
            self._is_processing = True

        threading.Thread(target=self._process_hotkey_task, daemon=True).start()

    def _process_hotkey_task(self) -> None:
        """The actual work for the hotkey, running in a non-blocking thread."""
        try:
            logger.debug("Hotkey processing started in background thread.")
            
            import uuid
            import time
            import platform_handler
            from utils import PerfTracker
            
            # 1. Save what's currently on the clipboard.
            PerfTracker.clipboard_save_start = time.perf_counter()
            self._clipboard.save()
            previous = self._clipboard.saved_content or ""
            PerfTracker.clipboard_save_end = time.perf_counter()
            logger.debug("CLIPBOARD_BEFORE_CAPTURE_LEN=%d", len(previous))
            logger.debug("CLIPBOARD_BEFORE_CAPTURE_PREVIEW=%r", previous[:20])
            
            # 1.5 Inject a temporary unique marker to definitively detect if Cmd+C worked.
            temp_marker = f"__AVELYN_{uuid.uuid4().hex}__"
            self._clipboard.set(temp_marker)
            logger.debug("UUID_MARKER_INJECTED=%s", temp_marker[:20])
            logger.debug("UUID inserted: %s", temp_marker[:20])
            logger.debug("CLIPBOARD_AFTER_UUID_INJECTION=%r", (self._clipboard.get() or "")[:20])
            logger.debug("Clipboard immediately after UUID insert: %s", (self._clipboard.get() or "")[:20])
            logger.debug("UUID_STATUS=%s", "Injected" if self._clipboard.get() == temp_marker else "Failed to Inject")

            # 2. Small delay to let any key-up events settle before we send Ctrl+C.
            time.sleep(0.05)

            # 3. Simulate copy on the TARGET application.
            PerfTracker.capture_start = time.perf_counter()
            PerfTracker.active_app_detect_start = time.perf_counter()
            copy_selection()
            PerfTracker.active_app_detect_end = time.perf_counter()
            PerfTracker.capture_end = time.perf_counter()
            
            # CRITICAL FIX: Emit the hotkey_pressed signal ONLY AFTER copy_selection() finishes!
            # If we emit it before, the main thread shows the Qt ToastOverlay, which forces macOS
            # to make Python the active application, causing Cmd+C to be sent to Python instead of Chrome/etc.
            self._bridge.hotkey_pressed.emit()
            
            logger.info("ACTIVE_APP_BEFORE_CAPTURE=%s", platform_handler._macos_active_app or "Unknown")

            # 4. Read clipboard with retry (wait for it to change from temp_marker)
            PerfTracker.clip_read_start = time.perf_counter()
            text = self._clipboard.read_after_copy(previous=temp_marker)
            PerfTracker.clip_read_end = time.perf_counter()
            
            logger.debug("Clipboard after copy: '%s'", text[:20] if text else "")
            logger.debug("STILL_UUID=%s", "True" if text == temp_marker else "False")
            logger.debug("CLIPBOARD_CHANGED=%s", "True" if text != temp_marker and text != "" else "False")
            logger.debug("COPY_SUCCESS=%s", "True" if text != temp_marker and text != "" else "False")

            # 5. Signal Qt.
            if not text or len(text.strip()) < 3:
                logger.warning("Selection validation failed: length %d, content: %r", len(text) if text else 0, text[:20] if text else "")
                self._bridge.nothing_selected.emit()
            else:
                logger.info("TEXT_CAPTURED")
                logger.info("Captured %d chars for enhancement. Preview: %r", len(text), text[:20])
                self._bridge.text_captured.emit(text)

        except Exception as exc:                          # noqa: BLE001
            logger.error("Error in hotkey callback: %s", exc)
            self._bridge.error_occurred.emit(str(exc))
        finally:
            with self._lock:
                self._is_processing = False

    def _on_ptt_fired(self) -> None:
        """
        Called by pynput when Ctrl+Shift+V is pressed.
        Spawns a background thread immediately to run selection capture and start recording.
        """
        with self._lock:
            if not self._enabled:
                logger.debug("PTT fired but processing is paused.")
                return
            if self._is_processing:
                logger.debug("PTT fired but already processing.")
                return
            self._is_processing = True

        threading.Thread(target=self._process_ptt_task, daemon=True).start()

    def _process_ptt_task(self) -> None:
        """Copies selection and then triggers PTT."""
        try:
            logger.debug("PTT copy cycle started in background thread.")
            import uuid
            import time
            import platform_handler

            # 1. Save clipboard and inject UUID
            self._clipboard.save()
            temp_marker = f"__AVELYN_{uuid.uuid4().hex}__"
            self._clipboard.set(temp_marker)

            time.sleep(0.05)

            # 2. Trigger Cmd+C
            copy_selection()

            # 3. Read clipboard
            text = self._clipboard.read_after_copy(previous=temp_marker)

            # 4. Signal Qt
            if not text or text == temp_marker or len(text.strip()) < 3:
                logger.warning("PTT Selection empty. Signaling nothing_selected.")
                self._bridge.nothing_selected.emit()
            else:
                logger.info("PTT Selection captured: %d chars", len(text))
                self._bridge.ptt_text_captured.emit(text)

        except Exception as exc:
            logger.error("Error in PTT task: %s", exc)
            self._bridge.error_occurred.emit(str(exc))
        finally:
            with self._lock:
                self._is_processing = False
