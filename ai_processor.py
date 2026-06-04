"""
Avelyn — AI Processor (FINAL OPTIMIZED VERSION)
==============================================

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
from typing import Generator, Optional, Callable

import requests

from logger import logger
from settings import Settings


# ──────────────────────────────────────────────────────────────────────────────
# Rewrite Modes
# ──────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
You are Avelyn. Output ONLY the finalized transformed text. No explanations, no introductions, no markdown, and preserve user intent.
"""

MODE_PROMPTS = {
    "smart":
        """
        Analyze the text and automatically apply the best transformation (e.g. improve_prompt, email, linkedin, grammar, professional).
        """,

    "improve_prompt":
        """
        Convert the input into a clear, specific, and concise AI prompt.
        """,

    "engineer_prompt":
        """
        Transform the input into a highly engineered prompt with a defined expert role/persona, output formatting, and quality constraints.
        """,

    "email":
        """
        Rewrite the text as a professional, concise email with a clear subject line if appropriate.
        """,

    "translate":
        """
        Translate the text into fluent, natural English.
        """,

    "explain_code":
        """
        Provide a concise, developer-friendly explanation of the key functions and logic in this code.
        """,

    "grammar":
        """
        Correct grammar, spelling, punctuation, and structure while preserving meaning and tone.
        """,

    "professional":
        """
        Rewrite the text to be professional, clear, and polished.
        """,

    "linkedin":
        """
        Rewrite the content as an engaging LinkedIn post with a strong hook, short paragraphs, and minimal emojis.
        """,

    "summarize":
        """
        Summarize the text concisely, removing repetition and preserving key information.
        """,

    "shorten":
        """
        Rewrite the text in fewer words while preserving meaning and readability.
        """,

    "expand":
        """
        Expand the text with useful details to improve flow and clarity.
        """,

    "resume":
        """
        Convert the input into ATS-friendly resume content using action verbs. Keep it concise.
        """,

    "tweet":
        """
        Rewrite as a concise, engaging social media post.
        """,

    "meeting_notes":
        """
        Convert the text into structured meeting notes with key points and action items.
        """,

    "eli5":
        """
        Explain the content in simple terms that a beginner can understand.
        """
}

def _build_prompt(text: str, mode: str, custom_instruction: Optional[str] = None) -> str:
    from utils import PerfTracker
    PerfTracker.prompt_build_start = time.perf_counter()
    if mode == "custom" and custom_instruction:
        mode_prompt = f"Follow this exact instruction to modify the text: {custom_instruction}"
    else:
        mode_prompt = MODE_PROMPTS.get(
            mode,
            MODE_PROMPTS["professional"]
        )

    res = f"{SYSTEM_PROMPT.strip()}\n\n{mode_prompt.strip()}\n\nINPUT:\n{text.strip()}\n\nOUTPUT:\n"
    PerfTracker.prompt_build_end = time.perf_counter()
    return res


# ──────────────────────────────────────────────────────────────────────────────
# Response Cleanup
# ──────────────────────────────────────────────────────────────────────────────

def _clean_response(text: str, mode: str) -> str:
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

    # Keep only first paragraph for short rewrite modes
    if mode not in ("smart", "improve_prompt", "engineer_prompt", "email", "explain_code", "custom", "resume", "meeting_notes", "eli5"):
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
    custom_instruction: Optional[str] = None,
    cancellation_check: Optional[Callable[[], bool]] = None,
) -> Generator[str, None, None]:

    prompt = _build_prompt(text, mode, custom_instruction)

    url = f"{host.rstrip('/')}/api/generate"

    # ── Per-mode token budgets (tighter = faster) ─────────────────────────────
    # Simple rewrites need very few tokens; only detailed modes get more.
    TOKEN_BUDGETS = {
        "grammar":        60,
        "shorten":        60,
        "tweet":          80,
        "professional":  120,
        "translate":     150,
        "linkedin":      150,
        "improve_prompt":150,
        "smart":         150,
        "email":         200,
        "engineer_prompt":200,
        "eli5":          200,
        "explain_code":  250,
        "meeting_notes": 250,
        "resume":        300,
        "custom":        200,
    }
    num_predict = TOKEN_BUDGETS.get(mode, 150)

    # CRITICAL FIX: Do NOT change num_ctx dynamically! 
    # Ollama unloads and reloads the entire model if num_ctx changes between requests.
    # A constant num_ctx ensures the model stays pinned in RAM (keep_alive works).
    # Prefill speed depends on the prompt length, not the max context size.
    num_ctx = 4096

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,             # Stream tokens as they arrive → feels instant
        "keep_alive": "24h",        # Keep model loaded in RAM (eliminates cold-start)
        "options": {
            "temperature":  0.15,   # Low = deterministic & fast, no creative meandering
            "num_predict":  num_predict,
            "top_p":        0.8,
            "top_k":        20,     # Restrict vocabulary → faster sampling
            "num_ctx":      num_ctx,
            "repeat_penalty": 1.1,  # Prevent repetitive output padding
        }
    }

    logger.info("AI_REQUEST_BEGIN")
    logger.info(
        "Ollama request: model=%s mode=%s chars=%d num_predict=%d",
        model, mode, len(text), num_predict,
    )

    from utils import PerfTracker
    PerfTracker.ollama_start = time.perf_counter()

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=90,
            stream=True,        # Enable HTTP streaming
        )

        response.raise_for_status()
        logger.info("AI_REQUEST_SENT")

        # ── Stream tokens and accumulate ──────────────────────────────────────
        full_response = []
        for raw_line in response.iter_lines():
            if cancellation_check and cancellation_check():
                logger.info("Ollama request cancelled cooperatively. Closing stream.")
                response.close()
                return

            if not raw_line:
                continue
            try:
                chunk = json.loads(raw_line)
            except json.JSONDecodeError:
                continue

            token = chunk.get("response", "")
            if token:
                if not PerfTracker.first_token:
                    PerfTracker.first_token = time.perf_counter()
                full_response.append(token)
                
                # Yield full accumulated cleaned text so far for live stream
                accumulated_raw = "".join(full_response)
                cleaned_result = _clean_response(accumulated_raw, mode)
                yield cleaned_result

            if chunk.get("done", False):
                break

        PerfTracker.generation_end = time.perf_counter()

        raw_result = "".join(full_response)
        cleaned_result = _clean_response(raw_result, mode)
        logger.info("AI_RESPONSE_RECEIVED")

        elapsed = time.perf_counter() - PerfTracker.ollama_start
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


def _local_fast_path(text: str, mode: str) -> Optional[str]:
    """
    Perform fast-path corrections locally for simple grammar/whitespace/capitalization issues
    without calling the LLM, if applicable.
    
    Only applies to 'grammar' mode when changes are minor formatting cleanups.
    """
    if mode != "grammar":
        return None
        
    cleaned = text.strip()
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    
    # Capitalize start of sentences
    sentences = re.split(r"(\s*[\.\!\?]+\s*)", cleaned)
    for i in range(0, len(sentences), 2):
        s = sentences[i]
        if s:
            first_idx = next((idx for idx, ch in enumerate(s) if ch.isalnum()), None)
            if first_idx is not None:
                sentences[i] = s[:first_idx] + s[first_idx].upper() + s[first_idx+1:]
    cleaned = "".join(sentences)
    
    # Capitalize standalone 'i'
    cleaned = re.sub(r"\bi\b", "I", cleaned)
    cleaned = re.sub(r"\bi'm\b", "I'm", cleaned)
    cleaned = re.sub(r"\bi'd\b", "I'd", cleaned)
    cleaned = re.sub(r"\bi'll\b", "I'll", cleaned)
    cleaned = re.sub(r"\bi've\b", "I've", cleaned)
    
    # Fix spacing before basic punctuation
    cleaned = re.sub(r"\s+([,\.\?\!])", r"\1", cleaned)
    
    # Match semantic chars (lowercased without non-alphanumeric chars)
    norm_orig = re.sub(r"[^a-zA-Z0-9]", "", text).lower()
    norm_new = re.sub(r"[^a-zA-Z0-9]", "", cleaned).lower()
    
    if len(text) < 60 and norm_orig == norm_new:
        logger.info("Local fast-path applied successfully.")
        return cleaned
        
    return None


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

class AIProcessor:
    """
    Avelyn AI rewrite engine.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def enhance(
        self,
        text: str,
        mode: Optional[str] = None,
        custom_instruction: Optional[str] = None,
        cancellation_check: Optional[Callable[[], bool]] = None,
    ) -> Generator[str, None, None]:

        text = text.strip()

        if not text:
            raise ValueError("Input text is empty.")

        mode = mode or self._settings.default_mode

        # Check local fast-path first
        fast_result = _local_fast_path(text, mode)
        if fast_result is not None:
            from utils import PerfTracker
            PerfTracker.ollama_start = time.perf_counter()
            PerfTracker.first_token = PerfTracker.ollama_start
            PerfTracker.generation_end = PerfTracker.ollama_start
            yield fast_result
            return

        yield from _call_ollama(
            text=text,
            mode=mode,
            host=self._settings.ollama_host,
            model=self._settings.ollama_model,
            custom_instruction=custom_instruction,
            cancellation_check=cancellation_check,
        )

    def warm_model(self) -> None:
        """
        Warm up the model at startup by loading it into RAM.
        """
        try:
            url = f"{self._settings.ollama_host.rstrip('/')}/api/generate"
            payload = {
                "model": self._settings.ollama_model,
                "prompt": "",
                "keep_alive": "24h"
            }
            logger.info("Ollama model warming started...")
            response = requests.post(url, json=payload, timeout=30)
            if response.status_code == 200:
                logger.info("Ollama model warmed successfully.")
            else:
                logger.warning("Ollama model warming returned status code %d", response.status_code)
        except Exception as exc:
            logger.warning("Ollama model warming failed (non-fatal): %s", exc)

    def test_connection(self) -> str:
        """
        Test Ollama connectivity.
        """

        probe = "improve this text"

        result = "".join(
            self.enhance(
                probe,
                mode="professional"
            )
        )

        return result or "Connection successful."