"""
Avelyn — Platform Handler
=========================
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

# pynput keyboard controller — initialised defensively at module load.
# On Windows, Controller() calls into Win32 keyboard APIs which can fail if
# pynput DLLs are missing from the PyInstaller bundle or if a security tool
# blocks the hook.  We must never let this crash at import time.
try:
    from pynput.keyboard import Controller as _KbController, Key
    _keyboard_controller: _KbController | None = _KbController()
    logger.debug("STARTUP: pynput keyboard Controller initialised OK")
except Exception as _pynput_exc:
    logger.warning(
        "STARTUP WARN: pynput keyboard Controller init failed (%s). "
        "Keyboard simulation (copy/paste) will be unavailable.",
        _pynput_exc,
    )
    _keyboard_controller = None
    try:
        from pynput.keyboard import Key          # Key constants may still import
    except Exception:
        Key = None  # type: ignore[assignment]


def _get_keyboard() -> _KbController | None:
    """Return the shared keyboard controller, or None if unavailable."""
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
                is_tp = (bid == "com.vishwaksen.avelyn" or "Avelyn" in name)
                return {
                    "bundle_id":    bid,
                    "name":         name,
                    "is_avelyn":     is_tp,
                    "is_active":    app.isActive(),
                }
        except Exception as e:
            return {"error": str(e)}
        return {"bundle_id": "None", "name": "None", "is_avelyn": False, "is_active": False}

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
                is_tp = "Avelyn" in name or "avelyn" in name.lower()
                return {
                    "hwnd":         hwnd,
                    "name":         name,
                    "pid":          pid,
                    "is_avelyn":     is_tp,
                }
        except Exception as e:
            return {"error": str(e)}
        return {"hwnd": 0, "name": "Unknown", "is_avelyn": False}

    return {"name": "Unknown", "is_avelyn": False}


def record_active_app() -> None:
    """
    Snapshot the currently frontmost app so focus can be restored before pasting.
    Call BEFORE showing any Avelyn window that will steal focus.

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
        logger.info("IS_AVELYN_BEFORE_CAPTURE=%s",     app_info_before.get("is_avelyn"))

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
        time.sleep(0.05)

        # On Windows, wait until the user has released the physical hotkey modifier keys.
        # This prevents physical keys from clashing with pynput's virtual keystrokes (e.g. sending Ctrl+Shift+C).
        if IS_WINDOWS:
            try:
                import win32api
                import win32con
                
                win32_modifiers = [
                    win32con.VK_CONTROL,
                    win32con.VK_SHIFT,
                    win32con.VK_MENU,   # Alt
                    win32con.VK_LWIN,   # Left Windows
                    win32con.VK_RWIN,   # Right Windows
                ]
                
                logger.debug("Waiting for physical modifier keys to be released...")
                start_wait = time.perf_counter()
                while time.perf_counter() - start_wait < 0.5:
                    pressed = False
                    for vk in win32_modifiers:
                        if win32api.GetAsyncKeyState(vk) < 0:
                            pressed = True
                            break
                    if not pressed:
                        logger.debug("Physical modifiers released successfully.")
                        break
                    time.sleep(0.01)
                else:
                    logger.warning("Modifier release wait timed out after 500ms.")
            except Exception as exc:
                logger.error("Error during physical modifier release check: %s", exc)

        # ── Send copy keystroke ──────────────────────────────────────────────────────
        kb = _get_keyboard()
        if kb is None or Key is None:
            logger.error("copy_selection: keyboard controller unavailable, skipping Ctrl/Cmd+C")
            return
        kb.release(Key.ctrl)
        kb.release(Key.shift)
        kb.release(Key.alt)
        kb.release(Key.cmd)
        
        if IS_MACOS:
            logger.debug("Sending Cmd+C via pynput.")
            with kb.pressed(Key.cmd):
                kb.press('c')
                kb.release('c')
            
            # Re-inject osascript System Events fallback trigger immediately, without diagnostic sleeps
            logger.debug("Sending Cmd+C via osascript fallback.")
            subprocess.run(
                ['osascript', '-e', 'tell application "System Events" to keystroke "c" using command down'],
                capture_output=True, text=True, timeout=3
            )
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
        logger.info("IS_AVELYN_AFTER_CAPTURE=%s",     app_info_after.get("is_avelyn"))

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
    
    from utils import PerfTracker
    PerfTracker.focus_restore_start = time.perf_counter()

    try:
        app_info_before = get_frontmost_app_diagnostics()
        logger.info("=== PASTE PHASE: BEFORE FOCUS RESTORATION ===")
        logger.info("ACTIVE_APP_BEFORE_PASTE_NAME=%s",   app_info_before.get("name"))
        logger.info("ACTIVE_APP_BEFORE_PASTE_BUNDLE=%s", app_info_before.get("bundle_id") or app_info_before.get("hwnd"))
        logger.info("IS_AVELYN_BEFORE_PASTE=%s",     app_info_before.get("is_avelyn"))

        restore_success = False

        # ── Restore focus to original app ─────────────────────────────────────
        if IS_MACOS and _macos_active_app:
            logger.info("ACTIVE_APP_BEFORE_PASTE=%s", _macos_active_app)
            try:
                activated = False

                # 1. Try standard AppKit first (highly reliable, no Automation permission needed)
                try:
                    logger.debug("Running AppKit activateWithOptions_")
                    from AppKit import NSWorkspace, NSApplicationActivateIgnoringOtherApps
                    apps = NSWorkspace.sharedWorkspace().runningApplications()
                    for app in apps:
                        if app.bundleIdentifier() == _macos_active_app:
                            activated = app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
                            logger.debug("AppKit activateWithOptions_ returned: %s", activated)
                            break
                except Exception as e:
                    logger.debug("AppKit activation failed: %s", e)

                # 2. If AppKit fails to activate, try osascript as a fallback
                if not activated:
                    logger.debug("Running osascript activation fallback")
                    import subprocess
                    script = f'tell application id "{_macos_active_app}" to activate'
                    res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, check=False)
                    if res.returncode == 0:
                        activated = True
                        logger.debug("osascript activation successful.")
                    else:
                        logger.debug("osascript activation failed (code %d): %s", res.returncode, res.stderr)

                restore_success = activated
            except Exception as e:
                logger.debug("Failed to reactivate app via AppKit/osascript: %s", e)

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
        PerfTracker.focus_restore_end = time.perf_counter()

        # Small clipboard stabilization delay
        # macOS WindowServer requires ~50ms to complete the focus transition animation (reduced from 100ms)
        if IS_MACOS:
            time.sleep(0.05)
        else:
            time.sleep(0.03)

        # ── Send paste keystroke ─────────────────────────────────────────────────────
        PerfTracker.paste_start = time.perf_counter()
        kb = _get_keyboard()
        if kb is None or Key is None:
            logger.error("paste_text: keyboard controller unavailable, skipping Ctrl/Cmd+V")
            return
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
        PerfTracker.paste_end = time.perf_counter()

    except Exception as exc:
        logger.error("paste_text failed: %s", exc)
        PerfTracker.focus_restore_end = time.perf_counter()
        PerfTracker.paste_end = time.perf_counter()


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
                        name:"Avelyn",
                        path:"{path}",
                        hidden:false
                    }}
                end tell
                '''
                if enabled
                else
                '''
                tell application "System Events"
                    delete (login items whose name is "Avelyn")
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
                    winreg.SetValueEx(reg_key, "Avelyn", 0, winreg.REG_SZ, f'"{path}"')
                else:
                    try:
                        winreg.DeleteValue(reg_key, "Avelyn")
                    except FileNotFoundError:
                        pass
            success = True

        else:
            from pathlib import Path
            autostart_dir = Path.home() / ".config" / "autostart"
            autostart_dir.mkdir(parents=True, exist_ok=True)
            entry = autostart_dir / "avelyn.desktop"
            if enabled:
                entry.write_text(
                    f"[Desktop Entry]\nType=Application\nName=Avelyn\n"
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