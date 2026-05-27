"""
TextPolish — AI Processor (FINAL OPTIMIZED VERSION)
===================================================

Purpose:
- AI prompt enhancement
- text polishing
- inline rewrite engine
- local offline AI assistant

Optimized for:
- Ollama
- gemma3:4b
- MacBook Air M1
- fast rewrite latency
- non-chatbot behavior

Behavior:
- improves prompts/instructions
- preserves intent
- concise rewrites only
- no essay generation
- no explanations
"""

from __future__ import annotations

import json
import re
import time
from typing import Generator, Optional

import requests

from logger import logger
from settings import Settings


# ──────────────────────────────────────────────────────────────────────────────
# Rewrite Modes
# ──────────────────────────────────────────────────────────────────────────────

MODE_PROMPTS = {
    "professional":
        "Rewrite this user instruction into a cleaner, clearer, and more professional prompt while preserving the original intent.",

    "creative":
        "Rewrite this instruction into a more creative and engaging prompt while preserving the original intent.",

    "technical":
        "Rewrite this instruction in a clearer and more technical way while preserving meaning.",

    "concise":
        "Rewrite this instruction in a shorter and clearer way while preserving meaning.",

    "academic":
        "Rewrite this instruction in a more academic and formal way while preserving intent.",
}

USER_TEMPLATE = """
{mode_prompt}

RULES:
- Keep the rewritten text natural
- Keep it human-readable
- Keep the same intent
- Improve grammar and wording
- Do NOT answer the request
- Do NOT generate the final content
- Return ONLY the improved prompt

TEXT:
{text}

REWRITTEN:
"""


def _build_prompt(text: str, mode: str) -> str:
    mode_prompt = MODE_PROMPTS.get(
        mode,
        MODE_PROMPTS["professional"]
    )

    return USER_TEMPLATE.format(
        mode_prompt=mode_prompt,
        text=text.strip()
    )


# ──────────────────────────────────────────────────────────────────────────────
# Response Cleanup
# ──────────────────────────────────────────────────────────────────────────────

def _clean_response(text: str) -> str:
    """
    Aggressively clean AI output to force rewrite-only behavior.
    """

    if not text:
        return ""

    # Remove markdown/code blocks
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`+", "", text)

    # Remove markdown symbols
    text = re.sub(r"[*_~#]", "", text)

    # Remove instruction echoes
    unwanted_patterns = [
        r"(?i)^rewrite.*?:",
        r"(?i)^improve.*?:",
        r"(?i)^enhance.*?:",
        r"(?i)^input[:\-]?",
        r"(?i)^output[:\-]?",
        r"(?i)^improved[:\-]?",
        r"(?i)^rewritten[:\-]?",
        r"(?i)^here.*?:",
        r"(?i)^sure[:,]?",
        r"(?i)^certainly[:,]?",
        r"(?i)^okay[:,]?",
        r"(?i)^of course[:,]?",
    ]

    for pattern in unwanted_patterns:
        text = re.sub(pattern, "", text).strip()

    # Remove extra whitespace
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s+", " ", text)

    text = text.strip()

    # Remove wrapping quotes
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1].strip()

    # Keep only first paragraph
    text = text.split("\n")[0]

    # Remove repeated sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    unique_sentences = []
    seen = set()

    for sentence in sentences:
        normalized = sentence.strip().lower()

        if normalized and normalized not in seen:
            unique_sentences.append(sentence.strip())
            seen.add(normalized)

    text = " ".join(unique_sentences).strip()

    # Hard output limit
    if len(text) > 180:
        cutoff = text[:180]

        if "." in cutoff:
            text = cutoff.rsplit(".", 1)[0] + "."
        else:
            text = cutoff

    return text.strip()


# ──────────────────────────────────────────────────────────────────────────────
# Ollama Backend
# ──────────────────────────────────────────────────────────────────────────────

def _call_ollama(
    text: str,
    mode: str,
    host: str,
    model: str = "gemma3:4b",
) -> Generator[str, None, None]:

    prompt = _build_prompt(text, mode)

    url = f"{host.rstrip('/')}/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "24h", # Keep model in RAM to eliminate cold-start load times

        "options": {
            "temperature": 0.2,
            "num_predict": 80,
            "top_p": 0.8,
            "num_ctx": 512,  # Drastically reduce memory footprint on M1 Air
        }
    }

    logger.info(
        "Ollama request: model=%s mode=%s chars=%d prompt_len=%d",
        model,
        mode,
        len(text),
        len(prompt),
    )

    start_time = time.perf_counter()

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=90,
        )

        response.raise_for_status()

        raw_result = response.json().get("response", "")

        cleaned_result = _clean_response(raw_result)

        elapsed = time.perf_counter() - start_time

        logger.info(
            "Ollama response: %.2fs latency, %d output chars",
            elapsed,
            len(cleaned_result),
        )

        if cleaned_result:
            yield cleaned_result

    except requests.ConnectionError:
        logger.error("Cannot connect to Ollama at %s", host)

        raise RuntimeError(
            f"Cannot connect to Ollama at {host}. "
            f"Ensure Ollama is running."
        )

    except requests.Timeout as exc:
        logger.error("Ollama timeout: %s", exc)

        raise RuntimeError(
            "Ollama request timed out."
        ) from exc

    except requests.HTTPError as exc:
        logger.error("HTTP error: %s", exc)

        raise RuntimeError(
            f"Ollama HTTP error {exc.response.status_code}"
        ) from exc

    except json.JSONDecodeError as exc:
        logger.error("JSON decode error: %s", exc)

        raise RuntimeError(
            "Invalid response from Ollama."
        ) from exc

    except Exception as exc:
        logger.error("Unexpected Ollama error: %s", exc)

        raise RuntimeError(
            f"Ollama error: {exc}"
        ) from exc


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

class AIProcessor:
    """
    TextPolish AI rewrite engine.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def enhance(
        self,
        text: str,
        mode: Optional[str] = None,
    ) -> Generator[str, None, None]:

        text = text.strip()

        if not text:
            raise ValueError("Input text is empty.")

        mode = mode or self._settings.default_mode

        yield from _call_ollama(
            text=text,
            mode=mode,
            host=self._settings.ollama_host,
            model=self._settings.ollama_model,
        )

    def test_connection(self) -> str:
        """
        Test Ollama connectivity.
        """

        probe = "improve this text"

        result = "".join(
            self.enhance(
                probe,
                mode="concise"
            )
        )

        return result or "Connection successful."