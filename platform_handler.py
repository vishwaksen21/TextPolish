"""
TextPolish — Platform Handler (FINAL OPTIMIZED VERSION)
=======================================================

Handles:
- Copy selected text
- Paste enhanced text
- macOS accessibility
- Launch at startup
- Auto-start Ollama

Optimized for:
- macOS stability
- Browser text fields
- ChatGPT inputs
- VS Code
- Native apps
- Cross-platform support
"""

import subprocess
import sys
import time
from typing import Optional

from pynput.keyboard import Controller, Key

from logger import logger


# ──────────────────────────────────────────────────────────────────────────────
# Keyboard Controller & State
# ──────────────────────────────────────────────────────────────────────────────

keyboard = Controller()
_macos_active_app: Optional[str] = None


# ──────────────────────────────────────────────────────────────────────────────
# Platform Detection
# ──────────────────────────────────────────────────────────────────────────────

IS_MACOS = sys.platform == "darwin"
IS_WINDOWS = sys.platform == "win32"
IS_LINUX = not IS_MACOS and not IS_WINDOWS


# ──────────────────────────────────────────────────────────────────────────────
# Copy Selection
# ──────────────────────────────────────────────────────────────────────────────

def copy_selection() -> None:
    """
    Copy currently selected text from the active application.

    macOS:
        Cmd + C

    Windows/Linux:
        Ctrl + C
    """
    global _macos_active_app

    try:
        # Record the active application so we can restore focus before pasting
        if IS_MACOS:
            try:
                res = subprocess.run(
                    ['osascript', '-e', 'tell application "System Events" to get bundle identifier of first application process whose frontmost is true'],
                    capture_output=True, text=True, timeout=1
                )
                if res.returncode == 0:
                    _macos_active_app = res.stdout.strip()
                    logger.debug("Active app recorded (bundle id): %s", _macos_active_app)
            except Exception as e:
                logger.debug("Failed to record active app: %s", e)

        logger.debug("Waiting for selection stabilization...")

        # Allow macOS/browser selection to stabilize
        time.sleep(0.1)

        modifier = Key.cmd if IS_MACOS else Key.ctrl

        with keyboard.pressed(modifier):
            keyboard.press("c")
            keyboard.release("c")

        logger.debug("Copy shortcut sent successfully.")

    except Exception as exc:
        logger.error("copy_selection failed: %s", exc)


# ──────────────────────────────────────────────────────────────────────────────
# Paste Text
# ──────────────────────────────────────────────────────────────────────────────

def paste_text() -> None:
    """
    Paste clipboard content into active application.

    macOS:
        Cmd + V

    Windows/Linux:
        Ctrl + V
    """
    global _macos_active_app

    try:
        # Restore focus to the original application if Terminal stole it
        if IS_MACOS and _macos_active_app:
            try:
                logger.debug("Reactivating original app: %s", _macos_active_app)
                subprocess.run(
                    ['osascript', '-e', f'tell application id "{_macos_active_app}" to activate'],
                    timeout=1
                )
                time.sleep(0.05)
            except Exception as e:
                logger.debug("Failed to reactivate app: %s", e)

        # Ensure clipboard is fully updated
        time.sleep(0.10)

        modifier = Key.cmd if IS_MACOS else Key.ctrl

        with keyboard.pressed(modifier):
            keyboard.press("v")
            keyboard.release("v")

        logger.debug("Paste shortcut sent successfully.")

    except Exception as exc:
        logger.error("paste_text failed: %s", exc)


# ──────────────────────────────────────────────────────────────────────────────
# macOS Accessibility
# ──────────────────────────────────────────────────────────────────────────────

def check_accessibility() -> bool:
    """
    Check whether Accessibility permissions are granted.

    Returns:
        True if accessible or not macOS.
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
    """
    Open macOS Accessibility settings.
    """

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
    """
    Configure launch-at-login behavior.
    """

    import os

    path = app_path or os.path.abspath(sys.argv[0])

    try:

        # ── macOS ────────────────────────────────────────────────────────────

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

        # ── Windows ──────────────────────────────────────────────────────────

        elif IS_WINDOWS:

            import winreg

            key_path = (
                r"Software\Microsoft\Windows\CurrentVersion\Run"
            )

            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                key_path,
                0,
                winreg.KEY_SET_VALUE,
            ) as reg_key:

                if enabled:
                    winreg.SetValueEx(
                        reg_key,
                        "TextPolish",
                        0,
                        winreg.REG_SZ,
                        f'"{path}"',
                    )
                else:
                    try:
                        winreg.DeleteValue(reg_key, "TextPolish")
                    except FileNotFoundError:
                        pass

            success = True

        # ── Linux ────────────────────────────────────────────────────────────

        else:

            from pathlib import Path

            autostart_dir = (
                Path.home() / ".config" / "autostart"
            )

            autostart_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            entry = autostart_dir / "textpolish.desktop"

            if enabled:

                entry.write_text(
                    f"""
[Desktop Entry]
Type=Application
Name=TextPolish
Exec={path}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
"""
                )

            elif entry.exists():
                entry.unlink()

            success = True

        logger.info(
            "Launch at startup %s.",
            "enabled" if enabled else "disabled"
        )

        return success

    except Exception as exc:
        logger.error(
            "set_launch_at_startup failed: %s",
            exc,
        )
        return False


# ──────────────────────────────────────────────────────────────────────────────
# Ollama Auto Start
# ──────────────────────────────────────────────────────────────────────────────

def start_ollama_app() -> None:
    """
    Automatically start Ollama if not already running.
    """

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
                    creationflags=0x08000000,
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
        logger.warning(
            "Failed to start Ollama automatically: %s",
            exc,
        )


# ──────────────────────────────────────────────────────────────────────────────
# Platform Name
# ──────────────────────────────────────────────────────────────────────────────

def platform_name() -> str:
    """
    Human-readable platform name.
    """

    if IS_MACOS:
        return "macOS"

    if IS_WINDOWS:
        return "Windows"

    return "Linux"