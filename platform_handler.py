"""
TextPolish — Platform Handler
==============================
Handles:
- Copy selected text          (macOS: osascript, Windows: pynput Ctrl+C)
- Paste enhanced text         (macOS: osascript, Windows: win32gui + pynput Ctrl+V)
- Active application tracking (macOS: AppKit NSWorkspace, Windows: win32gui)
- Focus restoration           (macOS: NSRunningApplication.activate, Windows: SetForegroundWindow)
- Launch at startup
- Auto-start Ollama
"""

import subprocess
import sys
import time
from typing import Optional

from logger import logger
from pynput.keyboard import Controller, Key
_keyboard_controller = Controller()

def _get_keyboard():
    return _keyboard_controller


# ──────────────────────────────────────────────────────────────────────────────
# Platform Detection
# ──────────────────────────────────────────────────────────────────────────────

IS_MACOS   = sys.platform == "darwin"
IS_WINDOWS = sys.platform == "win32"
IS_LINUX   = not IS_MACOS and not IS_WINDOWS


# ──────────────────────────────────────────────────────────────────────────────
# Active App Tracking
# ──────────────────────────────────────────────────────────────────────────────

# macOS: bundle identifier string  (e.g. "com.google.Chrome")
# Windows: HWND integer            (e.g. 12345678)
_macos_active_app: Optional[str] = None   # macOS bundle ID
_windows_active_hwnd: Optional[int] = None  # Windows HWND


def get_frontmost_app_diagnostics() -> dict:
    """
    Return a dict describing the currently frontmost application.
    Works on macOS (AppKit) and Windows (win32gui).
    """
    if IS_MACOS:
        try:
            from AppKit import NSWorkspace
            app = NSWorkspace.sharedWorkspace().frontmostApplication()
            if app:
                bid  = app.bundleIdentifier() or "Unknown"
                name = app.localizedName()     or "Unknown"
                is_tp = (bid == "com.vishwaksen.textpolish" or "TextPolish" in name)
                return {
                    "bundle_id":    bid,
                    "name":         name,
                    "is_textpolish": is_tp,
                    "is_active":    app.isActive(),
                }
        except Exception as e:
            return {"error": str(e)}
        return {"bundle_id": "None", "name": "None", "is_textpolish": False, "is_active": False}

    if IS_WINDOWS:
        try:
            import win32gui
            import win32process
            import psutil
            hwnd = win32gui.GetForegroundWindow()
            if hwnd:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                try:
                    proc = psutil.Process(pid)
                    name = proc.name()
                except Exception:
                    name = "Unknown"
                is_tp = "TextPolish" in name or "textpolish" in name.lower()
                return {
                    "hwnd":         hwnd,
                    "name":         name,
                    "pid":          pid,
                    "is_textpolish": is_tp,
                }
        except Exception as e:
            return {"error": str(e)}
        return {"hwnd": 0, "name": "Unknown", "is_textpolish": False}

    return {"name": "Unknown", "is_textpolish": False}


def record_active_app() -> None:
    """
    Snapshot the currently frontmost app so focus can be restored before pasting.
    Call BEFORE showing any TextPolish window that will steal focus.

    macOS:   stores bundle identifier string
    Windows: stores HWND integer
    """
    global _macos_active_app, _windows_active_hwnd

    if IS_MACOS:
        try:
            from AppKit import NSWorkspace
            app = NSWorkspace.sharedWorkspace().frontmostApplication()
            if app:
                _macos_active_app = app.bundleIdentifier()
                logger.debug("Active app recorded via AppKit (bundle id): %s", _macos_active_app)
        except Exception as exc:
            logger.debug("record_active_app (macOS) failed: %s", exc)

    elif IS_WINDOWS:
        try:
            import win32gui
            hwnd = win32gui.GetForegroundWindow()
            if hwnd:
                _windows_active_hwnd = hwnd
                logger.debug("Active window recorded via win32gui (HWND): %d", hwnd)
        except Exception as exc:
            logger.debug("record_active_app (Windows) failed: %s", exc)


# ──────────────────────────────────────────────────────────────────────────────
# Copy Selection
# ──────────────────────────────────────────────────────────────────────────────

def copy_selection() -> None:
    """
    Copy currently selected text from the active application.

    Uses pynput on all platforms. On macOS, this is now safe because
    the hotkey_pressed signal (which shows the Qt UI) is delayed until
    after this function completes.
    """
    global _macos_active_app, _windows_active_hwnd

    try:
        app_info_before = get_frontmost_app_diagnostics()
        logger.info("=== CAPTURE PHASE: BEFORE COPY ===")
        logger.info("ACTIVE_APP_BEFORE_CAPTURE_NAME=%s",   app_info_before.get("name"))
        logger.info("ACTIVE_APP_BEFORE_CAPTURE_BUNDLE=%s", app_info_before.get("bundle_id") or app_info_before.get("hwnd"))
        logger.info("ACTIVE_APP=%s", app_info_before.get("name"))
        logger.info("ACTIVE_BUNDLE_ID=%s", app_info_before.get("bundle_id") or app_info_before.get("hwnd"))
        logger.info("IS_TEXTPOLISH_BEFORE_CAPTURE=%s",     app_info_before.get("is_textpolish"))

        # ── Record active app BEFORE any UI is shown ──────────────────────────
        app_name = app_info_before.get("name")
        logger.info(f"Frontmost app before copy: {app_name}")
        if IS_MACOS:
            try:
                from AppKit import NSWorkspace
                app = NSWorkspace.sharedWorkspace().frontmostApplication()
                if app:
                    _macos_active_app = app.bundleIdentifier()
                    logger.debug("Active app recorded via AppKit (bundle id): %s", _macos_active_app)
            except Exception as e:
                logger.debug("Failed to record active app via AppKit: %s", e)

        elif IS_WINDOWS:
            try:
                import win32gui
                hwnd = win32gui.GetForegroundWindow()
                if hwnd:
                    _windows_active_hwnd = hwnd
                    logger.debug("Active window recorded via win32gui (HWND): %d", hwnd)
            except Exception as e:
                logger.debug("Failed to record active window via win32gui: %s", e)

        # Allow selection to stabilize
        logger.debug("Waiting for selection stabilization...")
        time.sleep(0.1)

        # ── Send copy keystroke ───────────────────────────────────────────────
        kb = _get_keyboard()
        kb.release(Key.ctrl)
        kb.release(Key.shift)
        kb.release(Key.alt)
        kb.release(Key.cmd)
        
        if IS_MACOS:
            logger.debug("Sending Cmd+C via pynput.")
            with kb.pressed(Key.cmd):
                kb.press('c')
                kb.release('c')
        else:
            logger.debug("Sending Ctrl+C via pynput.")
            with kb.pressed(Key.ctrl):
                kb.press('c')
                kb.release('c')
                
        logger.debug("Copy shortcut sent successfully.")

        app_info_after = get_frontmost_app_diagnostics()
        logger.info("=== CAPTURE PHASE: AFTER COPY ===")
        logger.info("ACTIVE_APP_AFTER_CAPTURE_NAME=%s",   app_info_after.get("name"))
        logger.info("ACTIVE_APP_AFTER_CAPTURE_BUNDLE=%s", app_info_after.get("bundle_id") or app_info_after.get("hwnd"))
        logger.info("IS_TEXTPOLISH_AFTER_CAPTURE=%s",     app_info_after.get("is_textpolish"))

    except Exception as exc:
        logger.error("copy_selection failed: %s", exc)


# ──────────────────────────────────────────────────────────────────────────────
# Paste Text
# ──────────────────────────────────────────────────────────────────────────────

def paste_text() -> None:
    """
    Paste clipboard content into the previously active application.

    macOS:   AppKit focus restoration + pynput Cmd+V
    Windows: win32gui.SetForegroundWindow + pynput Ctrl+V
    """
    global _macos_active_app, _windows_active_hwnd

    try:
        app_info_before = get_frontmost_app_diagnostics()
        logger.info("=== PASTE PHASE: BEFORE FOCUS RESTORATION ===")
        logger.info("ACTIVE_APP_BEFORE_PASTE_NAME=%s",   app_info_before.get("name"))
        logger.info("ACTIVE_APP_BEFORE_PASTE_BUNDLE=%s", app_info_before.get("bundle_id") or app_info_before.get("hwnd"))
        logger.info("IS_TEXTPOLISH_BEFORE_PASTE=%s",     app_info_before.get("is_textpolish"))

        restore_success = False

        # ── Restore focus to original app ─────────────────────────────────────
        if IS_MACOS and _macos_active_app:
            logger.info("ACTIVE_APP_BEFORE_PASTE=%s", _macos_active_app)
            try:
                logger.debug("Reactivating original app via AppKit: %s", _macos_active_app)
                from AppKit import NSWorkspace, NSApplicationActivateIgnoringOtherApps
                apps = NSWorkspace.sharedWorkspace().runningApplications()
                for app in apps:
                    if app.bundleIdentifier() == _macos_active_app:
                        restore_success = app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
                        break
            except Exception as e:
                logger.debug("Failed to reactivate app via AppKit: %s", e)

        elif IS_WINDOWS and _windows_active_hwnd:
            logger.info("ACTIVE_HWND_BEFORE_PASTE=%d", _windows_active_hwnd)
            try:
                import win32gui
                import win32con

                try:
                    import win32process
                    win32gui.AllowSetForegroundWindow(win32con.ASFW_ANY)
                except Exception:
                    pass

                result = win32gui.SetForegroundWindow(_windows_active_hwnd)
                restore_success = bool(result)
                logger.debug("SetForegroundWindow(%d) returned: %s", _windows_active_hwnd, restore_success)

                # Give Windows a moment to complete the focus transfer
                time.sleep(0.15)
            except Exception as e:
                logger.debug("Failed to restore focus via win32gui: %s", e)

        logger.info("FOCUS_RESTORE_SUCCESS=%s", restore_success)

        # Small clipboard stabilization delay
        # macOS WindowServer requires ~400ms to complete the focus transition animation
        if IS_MACOS:
            time.sleep(0.40)
        else:
            time.sleep(0.15)

        app_info_after = get_frontmost_app_diagnostics()
        logger.info("=== PASTE PHASE: AFTER FOCUS RESTORATION (RIGHT BEFORE PASTE) ===")
        logger.info("ACTIVE_APP_AFTER_PASTE_NAME=%s",   app_info_after.get("name"))
        logger.info("ACTIVE_APP_AFTER_PASTE_BUNDLE=%s", app_info_after.get("bundle_id") or app_info_after.get("hwnd"))
        logger.info("IS_TEXTPOLISH_AFTER_PASTE=%s",     app_info_after.get("is_textpolish"))

        # ── Send paste keystroke ──────────────────────────────────────────────
        kb = _get_keyboard()
        kb.release(Key.ctrl)
        kb.release(Key.shift)
        kb.release(Key.alt)
        kb.release(Key.cmd)

        if IS_MACOS:
            logger.debug("Sending Cmd+V via pynput.")
            with kb.pressed(Key.cmd):
                kb.press('v')
                kb.release('v')
        else:
            logger.debug("Sending Ctrl+V via pynput.")
            with kb.pressed(Key.ctrl):
                kb.press('v')
                kb.release('v')

        logger.debug("Paste shortcut sent successfully.")
        logger.info("PASTE_SENT=True")
        logger.info("PASTE_SUCCESS=True")

    except Exception as exc:
        logger.error("paste_text failed: %s", exc)


# ──────────────────────────────────────────────────────────────────────────────
# macOS Accessibility
# ──────────────────────────────────────────────────────────────────────────────

def check_accessibility() -> bool:
    """
    Check whether Accessibility permissions are granted.
    On Windows, this is always True (no equivalent TCC system).
    """
    if not IS_MACOS:
        return True

    try:
        script = (
            'tell application "System Events" '
            'to get name of every process whose visible is true'
        )
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            timeout=5,
        )
        return result.returncode == 0
    except Exception as exc:
        logger.warning("Accessibility check failed: %s", exc)
        return False


def request_accessibility() -> None:
    """Open macOS Accessibility settings. No-op on Windows."""
    if not IS_MACOS:
        return
    logger.info("Opening Accessibility settings.")
    try:
        subprocess.Popen([
            "open",
            "x-apple.systempreferences:"
            "com.apple.preference.security"
            "?Privacy_Accessibility"
        ])
    except Exception as exc:
        logger.error("Could not open Accessibility settings: %s", exc)


# ──────────────────────────────────────────────────────────────────────────────
# Launch At Startup
# ──────────────────────────────────────────────────────────────────────────────

def set_launch_at_startup(
    enabled: bool,
    app_path: Optional[str] = None
) -> bool:
    """Configure launch-at-login behavior."""
    import os
    path = app_path or os.path.abspath(sys.argv[0])

    try:
        if IS_MACOS:
            script = (
                f'''
                tell application "System Events"
                    make login item at end with properties {{
                        name:"TextPolish",
                        path:"{path}",
                        hidden:false
                    }}
                end tell
                '''
                if enabled
                else
                '''
                tell application "System Events"
                    delete (login items whose name is "TextPolish")
                end tell
                '''
            )
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                timeout=10,
            )
            success = result.returncode == 0

        elif IS_WINDOWS:
            import winreg
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE
            ) as reg_key:
                if enabled:
                    winreg.SetValueEx(reg_key, "TextPolish", 0, winreg.REG_SZ, f'"{path}"')
                else:
                    try:
                        winreg.DeleteValue(reg_key, "TextPolish")
                    except FileNotFoundError:
                        pass
            success = True

        else:
            from pathlib import Path
            autostart_dir = Path.home() / ".config" / "autostart"
            autostart_dir.mkdir(parents=True, exist_ok=True)
            entry = autostart_dir / "textpolish.desktop"
            if enabled:
                entry.write_text(
                    f"[Desktop Entry]\nType=Application\nName=TextPolish\n"
                    f"Exec={path}\nHidden=false\nNoDisplay=false\n"
                    f"X-GNOME-Autostart-enabled=true\n"
                )
            elif entry.exists():
                entry.unlink()
            success = True

        logger.info("Launch at startup %s.", "enabled" if enabled else "disabled")
        return success

    except Exception as exc:
        logger.error("set_launch_at_startup failed: %s", exc)
        return False


# ──────────────────────────────────────────────────────────────────────────────
# Ollama Auto Start
# ──────────────────────────────────────────────────────────────────────────────

def start_ollama_app() -> None:
    """Automatically start Ollama if not already running."""
    try:
        logger.info("Attempting to start Ollama...")

        if IS_MACOS:
            subprocess.Popen(
                ["open", "-a", "Ollama"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        elif IS_WINDOWS:
            import os
            ollama_path = os.path.expandvars(
                r"%LOCALAPPDATA%\Programs\Ollama\ollama app.exe"
            )
            if os.path.exists(ollama_path):
                subprocess.Popen(
                    [ollama_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=0x08000000,  # CREATE_NO_WINDOW
                )
            else:
                subprocess.Popen(
                    ["ollama", "serve"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=0x08000000,
                )

        logger.info("Ollama launch command executed.")

    except Exception as exc:
        logger.warning("Failed to start Ollama automatically: %s", exc)


# ──────────────────────────────────────────────────────────────────────────────
# Platform Name
# ──────────────────────────────────────────────────────────────────────────────

def platform_name() -> str:
    if IS_MACOS:
        return "macOS"
    if IS_WINDOWS:
        return "Windows"
    return "Linux"