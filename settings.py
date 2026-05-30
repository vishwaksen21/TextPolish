"""
TextPolish — Settings
=====================
Manages persistent application configuration stored at
~/.textpolish/config.json. Provides typed accessors and auto-saves
on every change.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from logger import logger


CONFIG_DIR  = Path.home() / ".textpolish"
CONFIG_FILE = CONFIG_DIR / "config.json"

# ── Default configuration schema ─────────────────────────────────────────────
DEFAULT_CONFIG: Dict[str, Any] = {
    # Hotkey (pynput format)
    "hotkey":             "<ctrl>+<shift>+e",
    "shortcut_display":   "Ctrl+Shift+E",
    "hotkey_enabled":     True,

    # AI provider
    "ai_provider":        "ollama",   # "ollama" only
    "ollama_model":       "gemma3:4b",
    "ollama_host":        "http://localhost:11434",

    # Enhancement defaults
    "default_mode":       "professional",
    "auto_replace":       True,
    "first_run_completed": False,

    # UI
    "theme":              "dark",     # "dark" | "light"
    "popup_position":     "cursor",   # "cursor" | "center" | "top-right"

    # History
    "prompt_history":     [],
    "max_history":        50,

    # Misc
    "launch_at_startup":  False,
    "show_notifications": True,
}


class Settings:
    """
    Thread-safe application settings manager.

    Usage::

        settings = Settings()
        key = settings.gemini_api_key
        settings.set("theme", "light")
    """

    def __init__(self) -> None:
        self._config: Dict[str, Any] = {}
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self.load()

    # ── Persistence ──────────────────────────────────────────────────────────

    def load(self) -> None:
        """Load config from disk, filling missing keys with defaults."""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as fh:
                    stored = json.load(fh)
                # Merge: defaults first, stored values override.
                self._config = {**DEFAULT_CONFIG, **stored}
                logger.debug("Settings loaded from %s", CONFIG_FILE)
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning("Could not load settings (%s) — using defaults.", exc)
                self._config = DEFAULT_CONFIG.copy()
        else:
            self._config = DEFAULT_CONFIG.copy()
            self.save()   # Persist defaults on first run

    def save(self) -> None:
        """Write current config to disk."""
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as fh:
                json.dump(self._config, fh, indent=2, ensure_ascii=False)
            logger.debug("Settings saved.")
        except OSError as exc:
            logger.error("Failed to save settings: %s", exc)

    # ── Generic get / set ────────────────────────────────────────────────────

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default if default is not None else DEFAULT_CONFIG.get(key))

    def set(self, key: str, value: Any) -> None:
        self._config[key] = value
        self.save()

    # ── History management ────────────────────────────────────────────────────

    def add_to_history(self, original: str, enhanced: str, mode: str) -> None:
        """Prepend a history entry, capping the list at max_history."""
        entry = {
            "original":  original[:800],
            "enhanced":  enhanced[:800],
            "mode":      mode,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
        history: List[Dict] = self._config.get("prompt_history", [])
        history.insert(0, entry)
        cap = self._config.get("max_history", 50)
        self._config["prompt_history"] = history[:cap]
        self.save()

    def clear_history(self) -> None:
        self._config["prompt_history"] = []
        self.save()

    # ── Typed convenience properties ─────────────────────────────────────────

    @property
    def hotkey(self) -> str:
        return self._config.get("hotkey", DEFAULT_CONFIG["hotkey"])

    @property
    def shortcut_display(self) -> str:
        return self._config.get("shortcut_display", DEFAULT_CONFIG["shortcut_display"])

    @property
    def hotkey_enabled(self) -> bool:
        return bool(self._config.get("hotkey_enabled", True))

    @property
    def ai_provider(self) -> str:
        return self._config.get("ai_provider", "ollama")

    @property
    def ollama_model(self) -> str:
        return self._config.get("ollama_model", "gemma3:4b")

    @property
    def ollama_host(self) -> str:
        return self._config.get("ollama_host", "http://localhost:11434")

    @property
    def default_mode(self) -> str:
        return self._config.get("default_mode", "professional")
        
    @property
    def auto_replace(self) -> bool:
        return self._config.get("auto_replace", True)

    @auto_replace.setter
    def auto_replace(self, value: bool) -> None:
        self._config["auto_replace"] = value
        self.save()

    @property
    def theme(self) -> str:
        return self._config.get("theme", "dark")

    @property
    def prompt_history(self) -> List[Dict]:
        return self._config.get("prompt_history", [])

    @property
    def launch_at_startup(self) -> bool:
        return bool(self._config.get("launch_at_startup", False))

    @property
    def first_run_completed(self) -> bool:
        return bool(self._config.get("first_run_completed", False))
