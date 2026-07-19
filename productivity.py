import json
import threading
from datetime import date
from pathlib import Path
from typing import Dict, Any

from logger import logger

CONFIG_DIR = Path.home() / ".avelyn"
STATS_FILE = CONFIG_DIR / "productivity.json"

class ProductivityTracker:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(ProductivityTracker, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self._lock = threading.Lock()
        self._stats = {
            "totals": {
                "words_improved": 0,
                "commands_executed": 0,
                "time_saved_seconds": 0
            },
            "by_mode": {},
            "daily": {}
        }
        self.load()

    def load(self) -> None:
        with self._lock:
            if STATS_FILE.exists():
                try:
                    with open(STATS_FILE, "r", encoding="utf-8") as fh:
                        stored = json.load(fh)
                    # Merge defaults
                    for k in ["totals", "by_mode", "daily"]:
                        if k in stored:
                            if k == "totals":
                                self._stats["totals"] = {**self._stats["totals"], **stored["totals"]}
                            else:
                                self._stats[k] = stored[k]
                    logger.debug("Productivity stats loaded from %s", STATS_FILE)
                except Exception as exc:
                    logger.warning("Could not load productivity stats (%s) — using defaults.", exc)

    def save(self) -> None:
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with open(STATS_FILE, "w", encoding="utf-8") as fh:
                json.dump(self._stats, fh, indent=2, ensure_ascii=False)
        except OSError as exc:
            logger.error("Failed to save productivity stats: %s", exc)

    def record_execution(self, original_text: str, mode: str) -> None:
        """Record a single successful AI text improvement."""
        with self._lock:
            words = len(original_text.strip().split())
            if words == 0:
                words = 1  # count at least 1 word for any operation
                
            # Estimated time saved: 10s per command flat + 1.5s per word
            time_saved = 10.0 + (words * 1.5)
            
            # Totals
            self._stats["totals"]["words_improved"] += words
            self._stats["totals"]["commands_executed"] += 1
            self._stats["totals"]["time_saved_seconds"] += int(time_saved)
            
            # Mode
            self._stats["by_mode"][mode] = self._stats["by_mode"].get(mode, 0) + 1
            
            # Daily
            today_str = date.today().isoformat()
            if today_str not in self._stats["daily"]:
                self._stats["daily"][today_str] = {
                    "words_improved": 0,
                    "commands_executed": 0,
                    "time_saved_seconds": 0
                }
            self._stats["daily"][today_str]["words_improved"] += words
            self._stats["daily"][today_str]["commands_executed"] += 1
            self._stats["daily"][today_str]["time_saved_seconds"] += int(time_saved)
            
            self.save()
            logger.info("Recorded productivity: words=%d, mode=%s, time_saved=%.1fs", words, mode, time_saved)

    def get_stats(self) -> Dict[str, Any]:
        with self._lock:
            # Return a copy to avoid external modification issues
            return json.loads(json.dumps(self._stats))
            
    def get_daily_goal_progress(self, goal_words: int = 1000) -> Dict[str, Any]:
        with self._lock:
            today_str = date.today().isoformat()
            today_data = self._stats["daily"].get(today_str, {"words_improved": 0, "commands_executed": 0, "time_saved_seconds": 0})
            words = today_data["words_improved"]
            pct = min(100, int((words / goal_words) * 100)) if goal_words > 0 else 100
            return {
                "current": words,
                "goal": goal_words,
                "percentage": pct,
                "commands": today_data["commands_executed"],
                "time_saved": today_data["time_saved_seconds"]
            }
