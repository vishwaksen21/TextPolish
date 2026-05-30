"""
TextPolish — Clipboard Manager (FINAL OPTIMIZED VERSION)
========================================================

Handles:
- clipboard save/restore
- reliable clipboard reading
- automatic inline replacement
- macOS/browser compatibility
- retry stabilization

Optimized for:
- macOS
- ChatGPT inputs
- Chrome
- Arc Browser
- VS Code
- TextEdit
- Windows compatibility
"""

import time
from typing import Optional

import pyperclip

from logger import logger


# ──────────────────────────────────────────────────────────────────────────────
# Clipboard Timing Configuration
# ──────────────────────────────────────────────────────────────────────────────

# Delay between clipboard polling attempts
_RETRY_DELAY = 0.02

# Total retry attempts
_MAX_RETRIES = 25

# Additional stabilization delay after copy
_POST_COPY_DELAY = 0.02


class ClipboardManager:
    """
    Robust cross-platform clipboard manager.
    """

    def __init__(self) -> None:
        self._saved: Optional[str] = None

    # ──────────────────────────────────────────────────────────────────────────
    # Save / Restore
    # ──────────────────────────────────────────────────────────────────────────

    def save(self) -> None:
        """
        Save current clipboard contents.
        """

        try:
            self._saved = pyperclip.paste() or ""

            logger.debug(
                "Clipboard saved (%d chars).",
                len(self._saved),
            )

        except Exception as exc:
            logger.warning(
                "Failed to save clipboard: %s",
                exc,
            )

            self._saved = ""

    def restore(self) -> None:
        """
        Restore original clipboard contents.
        """

        if self._saved is None:
            logger.debug(
                "No clipboard snapshot available to restore."
            )
            return

        try:
            pyperclip.copy(self._saved)

            logger.debug(
                "Clipboard restored successfully."
            )

        except Exception as exc:
            logger.warning(
                "Failed to restore clipboard: %s",
                exc,
            )

    # ──────────────────────────────────────────────────────────────────────────
    # Clipboard Read
    # ──────────────────────────────────────────────────────────────────────────

    def get(self) -> str:
        """
        Return current clipboard contents safely.
        """

        try:
            return pyperclip.paste() or ""

        except Exception as exc:
            logger.warning(
                "Clipboard read failed: %s",
                exc,
            )

            return ""

    def read_after_copy(
        self,
        previous: Optional[str] = None,
    ) -> str:
        """
        Read clipboard after simulated Cmd+C / Ctrl+C.

        Waits until clipboard changes from previous value.

        Returns:
            Clipboard text or empty string.
        """

        baseline = (
            previous
            if previous is not None
            else (self._saved or "")
        )

        logger.debug(
            "Waiting for clipboard update..."
        )

        # Extra stabilization delay
        time.sleep(_POST_COPY_DELAY)

        for attempt in range(1, _MAX_RETRIES + 1):

            time.sleep(_RETRY_DELAY)

            try:
                current = pyperclip.paste() or ""

            except Exception as exc:
                logger.warning(
                    "Clipboard read attempt %d failed: %s",
                    attempt,
                    exc,
                )
                continue

            logger.debug(
                "Clipboard attempt %d: %d chars",
                attempt,
                len(current),
            )

            # Ignore empty whitespace-only content
            if not current.strip():
                continue

            # Clipboard changed successfully
            if current != baseline:

                logger.info(
                    "Clipboard updated successfully on attempt %d (%d chars).",
                    attempt,
                    len(current),
                )

                logger.debug(
                    "Clipboard preview: '%s'",
                    current[:100],
                )

                return current

        # Clipboard never changed
        logger.warning(
            "Clipboard unchanged after %d retries.",
            _MAX_RETRIES,
        )

        logger.warning(
            "Selection may have failed or application blocked copy event."
        )

        return ""

    # ──────────────────────────────────────────────────────────────────────────
    # Clipboard Write
    # ──────────────────────────────────────────────────────────────────────────

    def set(self, text: str) -> bool:
        """
        Set clipboard contents safely.
        """

        try:

            text = text.strip()

            if not text:
                logger.warning(
                    "Attempted to set empty clipboard text."
                )
                return False

            pyperclip.copy(text)

            logger.debug(
                "Clipboard updated (%d chars).",
                len(text),
            )

            return True

        except Exception as exc:
            logger.error(
                "Failed to write clipboard: %s",
                exc,
            )

            return False

    # ──────────────────────────────────────────────────────────────────────────
    # Clipboard Snapshot Access
    # ──────────────────────────────────────────────────────────────────────────

    @property
    def saved_content(self) -> Optional[str]:
        """
        Return saved clipboard snapshot.
        """

        return self._saved