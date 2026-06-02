"""
Avelyn — Logger
===============
Centralized logging configuration. Writes DEBUG+ to a rotating log file
and INFO+ to stdout. All other modules import `logger` from here.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


LOG_DIR = Path.home() / ".avelyn" / "logs"


def setup_logger(name: str = "avelyn", debug: bool = False) -> logging.Logger:
    """
    Initialize and return the application logger.

    Args:
        name:  Logger name (default: 'avelyn').
        debug: If True, sets console handler to DEBUG level.

    Returns:
        Configured logging.Logger instance.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    # Guard against adding duplicate handlers on re-import.
    if log.handlers:
        return log

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(module)-20s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ── Rotating file handler: 5 MB × 3 backups ──────────────────────────────
    fh = RotatingFileHandler(
        LOG_DIR / "app.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    # ── Console handler ───────────────────────────────────────────────────────
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG if debug else logging.INFO)
    ch.setFormatter(fmt)

    log.addHandler(fh)
    log.addHandler(ch)
    return log


# Module-level singleton — all other modules do `from logger import logger`
logger = setup_logger()
