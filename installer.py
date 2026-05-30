"""
TextPolish — Installer
======================
Handles auto-detection, download, installation, and verification of
the Ollama binary and the configured AI model.

Supports:
  - macOS (Ollama-darwin.zip)
  - Windows (ollama-windows-amd64.zip)

Never crashes. All errors are propagated as RuntimeError for the caller
to display in the InstallerOverlay.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import zipfile
from typing import Callable

from logger import logger

# ── Platform detection ────────────────────────────────────────────────────────

IS_MACOS   = sys.platform == "darwin"
IS_WINDOWS = sys.platform == "win32"

# ── Download URLs ─────────────────────────────────────────────────────────────

OLLAMA_MAC_URL = "https://ollama.com/download/Ollama-darwin.zip"
OLLAMA_WIN_URL = (
    "https://github.com/ollama/ollama/releases/latest/download/"
    "ollama-windows-amd64.zip"
)

# ── Ollama API ────────────────────────────────────────────────────────────────

OLLAMA_BASE = "http://127.0.0.1:11434"

ProgressCallback = Callable[[int, str], None]


class Installer:
    """
    Static utility class for managing Ollama installation lifecycle.
    """

    # ── Detection ─────────────────────────────────────────────────────────────

    @staticmethod
    def get_ollama_path() -> str:
        """Return the path to the ollama binary, or empty string if not found."""
        # 1. System PATH
        sys_path = shutil.which("ollama")
        if sys_path:
            return sys_path

        # 2. macOS: user Applications (no sudo needed)
        if IS_MACOS:
            candidate = os.path.expanduser(
                "~/Applications/Ollama.app/Contents/Resources/ollama"
            )
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                return candidate

            # System-level Applications (installed by official .pkg)
            candidate2 = "/Applications/Ollama.app/Contents/Resources/ollama"
            if os.path.isfile(candidate2) and os.access(candidate2, os.X_OK):
                return candidate2

        # 3. Windows: user-level install path we control
        if IS_WINDOWS:
            candidate = os.path.expanduser(
                r"~\AppData\Local\TextPolish\Ollama\ollama.exe"
            )
            if os.path.isfile(candidate):
                return candidate

        return ""

    @staticmethod
    def needs_installation() -> bool:
        """Return True when the ollama binary cannot be found at all."""
        return Installer.get_ollama_path() == ""

    # ── Server detection ──────────────────────────────────────────────────────

    @staticmethod
    def is_server_running() -> bool:
        """Return True if the Ollama HTTP server is reachable right now."""
        try:
            resp = urllib.request.urlopen(
                f"{OLLAMA_BASE}/api/tags", timeout=1
            )
            return resp.status == 200
        except Exception:
            return False

    # ── Download & extract ────────────────────────────────────────────────────

    @staticmethod
    def download_and_extract_ollama(cb: ProgressCallback) -> str:
        """
        Download the Ollama binary for the current platform and extract it to a
        user-owned directory (no administrator/root prompt required).

        Returns the path to the installed ollama binary.
        Raises RuntimeError on any failure.
        """
        if IS_MACOS:
            target_dir = os.path.expanduser("~/Applications")
            zip_name   = "Ollama-darwin.zip"
            url        = OLLAMA_MAC_URL
            final_bin  = os.path.join(
                target_dir, "Ollama.app", "Contents", "Resources", "ollama"
            )
        elif IS_WINDOWS:
            target_dir = os.path.expanduser(
                r"~\AppData\Local\TextPolish\Ollama"
            )
            zip_name  = "ollama-windows-amd64.zip"
            url       = OLLAMA_WIN_URL
            final_bin = os.path.join(target_dir, "ollama.exe")
        else:
            raise RuntimeError(
                "Automatic Ollama installation is only supported on macOS and Windows.\n"
                "Please install Ollama manually from https://ollama.com"
            )

        os.makedirs(target_dir, exist_ok=True)
        zip_path = os.path.join(target_dir, zip_name)

        cb(5, "Downloading Ollama...")
        logger.info("Downloading Ollama from %s", url)

        try:
            def _reporthook(blocknum: int, blocksize: int, totalsize: int) -> None:
                if totalsize > 0:
                    downloaded = min(blocknum * blocksize, totalsize)
                    # Scale download progress into 5-40%
                    pct = 5 + int((downloaded / totalsize) * 35)
                    cb(pct, "Downloading Ollama...")

            urllib.request.urlretrieve(url, zip_path, _reporthook)

        except urllib.error.URLError as exc:
            _safe_remove(zip_path)
            raise RuntimeError(
                f"Network error while downloading Ollama.\nCheck your internet connection.\n({exc})"
            )
        except Exception as exc:
            _safe_remove(zip_path)
            raise RuntimeError(f"Download failed: {exc}")

        cb(40, "Installing Ollama...")
        logger.info("Extracting Ollama to %s", target_dir)

        try:
            # Remove stale app folder so extraction is clean
            if IS_MACOS:
                stale = os.path.join(target_dir, "Ollama.app")
                if os.path.isdir(stale):
                    shutil.rmtree(stale)

            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(target_dir)

            if IS_MACOS:
                os.chmod(final_bin, 0o755)

        except zipfile.BadZipFile:
            raise RuntimeError(
                "The downloaded Ollama archive is corrupt. Please try again."
            )
        except PermissionError as exc:
            raise RuntimeError(
                f"Permission denied while installing Ollama.\n({exc})"
            )
        finally:
            _safe_remove(zip_path)

        cb(48, "Ollama installed.")
        logger.info("Ollama binary installed at: %s", final_bin)
        return final_bin

    # ── Server startup ────────────────────────────────────────────────────────

    @staticmethod
    def start_ollama() -> None:
        """
        Launch `ollama serve` as a background process.
        Does nothing if the server is already running.
        Raises RuntimeError if the binary cannot be found.
        """
        if Installer.is_server_running():
            logger.info("Ollama server already running.")
            return

        bin_path = Installer.get_ollama_path()
        if not bin_path:
            raise RuntimeError(
                "Ollama binary not found. Please reinstall TextPolish."
            )

        logger.info("Starting Ollama server: %s serve", bin_path)
        try:
            startupinfo = None
            if IS_WINDOWS:
                import subprocess as _sp
                startupinfo = _sp.STARTUPINFO()
                startupinfo.dwFlags |= _sp.STARTF_USESHOWWINDOW

            subprocess.Popen(
                [bin_path, "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                startupinfo=startupinfo,
                env=dict(os.environ, OLLAMA_HOST="127.0.0.1:11434"),
            )
        except Exception as exc:
            raise RuntimeError(f"Failed to start Ollama server: {exc}")

    # ── Startup verification ──────────────────────────────────────────────────

    @staticmethod
    def verify_installation(max_wait: int = 20) -> bool:
        """
        Block (in a background thread) until the Ollama HTTP API responds,
        or until `max_wait` seconds elapse.

        Returns True on success, False on timeout.
        """
        logger.info("Waiting for Ollama server (up to %ds)…", max_wait)
        for _ in range(max_wait):
            try:
                resp = urllib.request.urlopen(
                    f"{OLLAMA_BASE}/api/tags", timeout=1
                )
                if resp.status == 200:
                    logger.info("Ollama server is ready.")
                    return True
            except Exception:
                pass
            time.sleep(1)

        logger.error("Ollama server did not start within %ds.", max_wait)
        return False

    # ── Model verification ────────────────────────────────────────────────────

    @staticmethod
    def is_model_available(model_name: str) -> bool:
        """Return True if the model is already pulled locally."""
        try:
            resp = urllib.request.urlopen(
                f"{OLLAMA_BASE}/api/tags", timeout=2
            )
            data = json.loads(resp.read())
            available = [m.get("name", "") for m in data.get("models", [])]
            return model_name in available or f"{model_name}:latest" in available
        except Exception:
            return False

    # ── Model pull ────────────────────────────────────────────────────────────

    @staticmethod
    def pull_model(model_name: str, cb: ProgressCallback) -> None:
        """
        Pull `model_name` via the local Ollama API, streaming progress into `cb`.
        Progress is mapped to 55–95%.
        Raises RuntimeError on failure.
        """
        if Installer.is_model_available(model_name):
            logger.info("Model '%s' already present. Skipping pull.", model_name)
            cb(95, f"{model_name} already installed.")
            return

        cb(55, f"Downloading {model_name}...")
        logger.info("Pulling model: %s", model_name)

        req = urllib.request.Request(
            f"{OLLAMA_BASE}/api/pull",
            data=json.dumps({"name": model_name}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req) as response:
                for raw_line in response:
                    if not raw_line:
                        continue
                    try:
                        data = json.loads(raw_line.decode())
                    except json.JSONDecodeError:
                        continue

                    status = data.get("status", "")
                    total  = data.get("total", 0)
                    done   = data.get("completed", 0)

                    if total > 0:
                        # 55 → 95%
                        pct = 55 + int((done / total) * 40)
                        cb(min(pct, 95), f"Downloading {model_name}…")
                    else:
                        cb(95, f"Finalizing {model_name}: {status}")

        except urllib.error.URLError as exc:
            raise RuntimeError(
                f"Network error while pulling '{model_name}'.\n({exc})"
            )
        except Exception as exc:
            raise RuntimeError(f"Failed to pull model '{model_name}': {exc}")

        cb(100, "Installation Complete ✓")
        logger.info("Model '%s' pulled successfully.", model_name)


# ── Private helpers ───────────────────────────────────────────────────────────

def _safe_remove(path: str) -> None:
    """Remove a file without raising if it is already gone."""
    try:
        if os.path.exists(path):
            os.remove(path)
    except OSError:
        pass
