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
You are Avelyn.

Your task is to transform text according to the selected mode.

Rules:
- Return ONLY the final result.
- Never explain what you changed.
- Never include introductions.
- Never include phrases like:
  'Here's the rewritten version'
  'Certainly'
  'Sure'
  'Output:'
- Never use markdown unless explicitly required.
- Preserve the user's intent.
- Produce production-quality output.
"""

MODE_PROMPTS = {
    "smart":
        """
        Analyze the user's text and automatically determine the best transformation.

        Examples:
        - Prompt-like text → improve_prompt
        - Email-like text → email
        - Social post → linkedin
        - Poor grammar → grammar
        - General text → professional

        Return only the transformed result.
        """,

    "improve_prompt":
        """
        Convert the user's input into a concise, high-quality AI prompt.

        Requirements:
        - Preserve the original intent.
        - Improve clarity and specificity.
        - Add useful context only when necessary.
        - Keep the prompt concise.
        - Do not invent excessive details.
        - Return only the improved prompt.
        """,

    "engineer_prompt":
        """
        Transform the user's input into a highly engineered, production-ready AI prompt.

        Requirements:
        - Preserve the original intent.
        - Define a suitable expert role/persona.
        - Specify the desired output format (like JSON, bullet points, etc.).
        - Add constraints that improve response quality.
        - Do not explain your changes.
        - Return ONLY the engineered prompt.
        """,

    "email":
        """
        Rewrite the text as a professional email.

        Requirements:
        - Maintain the original intent.
        - Use a clear subject line if appropriate.
        - Improve grammar and tone.
        - Keep the email concise and professional.
        - Add greeting and closing only when needed.
        - Return ONLY the email.
        """,

    "translate":
        """
        Translate the text into fluent English.

        Requirements:
        - Preserve meaning, tone, and context.
        - Use natural and professional wording.
        - Do not add explanations.
        - Return ONLY the translated text.
        """,

    "explain_code":
        """
        Explain the provided code.

        Requirements:
        - Describe the purpose of the code.
        - Explain key functions and logic.
        - Keep the explanation concise and developer-friendly.
        - Use bullet points when helpful.
        - Return ONLY the explanation.
        """,

    "grammar":
        """
        Correct grammar, spelling, punctuation, and sentence structure.

        Requirements:
        - Preserve the original meaning.
        - Preserve the original tone.
        - Improve readability.
        - Do not rewrite unnecessarily.
        - Return ONLY the corrected text.
        """,

    "professional":
        """
        Rewrite the text in a professional and polished manner.

        Requirements:
        - Improve clarity and structure.
        - Maintain the original meaning.
        - Use confident and professional language.
        - Remove unnecessary filler.
        - Return ONLY the rewritten text.
        """,

    "linkedin":
        """
        Rewrite the content as a professional LinkedIn post.

        Requirements:
        - Create a strong opening hook.
        - Improve readability using short paragraphs.
        - Maintain authenticity.
        - End with a natural closing statement.
        - Avoid excessive emojis.
        - Return ONLY the LinkedIn post.
        """,

    "summarize":
        """
        Summarize the text.

        Requirements:
        - Preserve key information.
        - Remove repetition.
        - Keep the summary concise.
        - Return ONLY the summary.
        """,

    "shorten":
        """
        Rewrite the text in fewer words.

        Requirements:
        - Preserve meaning.
        - Remove unnecessary details.
        - Improve readability.
        - Return ONLY the shortened version.
        """,

    "expand":
        """
        Expand the text while preserving its meaning.

        Requirements:
        - Add clarity and useful detail.
        - Improve flow and readability.
        - Avoid repetition.
        - Return ONLY the expanded version.
        """,

    "resume":
        """
        Convert the input into ATS-friendly resume content.

        Requirements:
        - Use strong action verbs.
        - Keep concise and measurable.
        - Return ONLY the result.
        """,

    "tweet":
        """
        Rewrite as a concise, engaging social media post.

        Requirements:
        - Return ONLY the post.
        """,

    "meeting_notes":
        """
        Convert the text into structured meeting notes.

        Requirements:
        - Include key points and action items.
        - Return ONLY the notes.
        """,

    "eli5":
        """
        Explain the content in simple terms that a beginner can understand.

        Requirements:
        - Return ONLY the explanation.
        """
}

def _build_prompt(text: str, mode: str, custom_instruction: Optional[str] = None) -> str:
    if mode == "custom" and custom_instruction:
        mode_prompt = f"Follow this exact instruction to modify the text: {custom_instruction}"
    else:
        mode_prompt = MODE_PROMPTS.get(
            mode,
            MODE_PROMPTS["professional"]
        )

    return f"{SYSTEM_PROMPT.strip()}\n\n{mode_prompt.strip()}\n\nINPUT:\n{text.strip()}\n\nOUTPUT:\n"


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

    start_time = time.perf_counter()

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
                full_response.append(token)

            if chunk.get("done", False):
                break

        raw_result = "".join(full_response)
        cleaned_result = _clean_response(raw_result, mode)
        logger.info("AI_RESPONSE_RECEIVED")

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

        yield from _call_ollama(
            text=text,
            mode=mode,
            host=self._settings.ollama_host,
            model=self._settings.ollama_model,
            custom_instruction=custom_instruction,
            cancellation_check=cancellation_check,
        )

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