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
import threading
from typing import Generator, Optional, Callable

import requests

from logger import logger
from settings import Settings


# ──────────────────────────────────────────────────────────────────────────────
# Shared HTTP Session for Connection Reuse
# ──────────────────────────────────────────────────────────────────────────────

_session_lock = threading.Lock()
_shared_session: Optional[requests.Session] = None

def _get_shared_session() -> requests.Session:
    """Get or create a shared requests.Session for HTTP connection pooling."""
    global _shared_session
    with _session_lock:
        if _shared_session is None:
            _shared_session = requests.Session()
            # Configure connection pooling
            adapter = requests.adapters.HTTPAdapter(
                pool_connections=10,
                pool_maxsize=20,
                max_retries=0,  # We handle retries manually
                pool_block=False,
            )
            _shared_session.mount('http://', adapter)
            _shared_session.mount('https://', adapter)
        return _shared_session


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
        """,

    "explain_code":
        """
        Explain the provided code in simple words.
        Rules:
        * Explain line by line when helpful.
        * Focus on understanding.
        * Use beginner-friendly language.
        """,

    "debug_code":
        """
        Analyze code and:
        * Identify bugs.
        * Explain issues.
        * Suggest fixes.
        * Provide corrected code.
        """
}

# ──────────────────────────────────────────────────────────────────────────────
# Universal Code Generation System
# ──────────────────────────────────────────────────────────────────────────────

_CODE_SYSTEM_PROMPT = """\
Output ONLY runnable code. No markdown, no backticks, no explanations, no docstrings. Complete programs only."""

_LANG_PROMPTS = {
    "python":     "Python. Type hints, f-strings. Include main() for programs.",
    "javascript": "JavaScript ES6+. const/let, arrow functions, template literals.",
    "typescript": "TypeScript strict. Explicit types, interfaces, ES6+.",
    "java":       "Java. Complete class with main() method.",
    "c":          "C. Complete program with main(), include standard headers.",
    "cplusplus":  "C++17. Complete program with main(), include standard headers.",
    "csharp":     "C# modern. Complete program with Main() or top-level statements.",
    "go":         "Go. Package main with main() function, include imports.",
    "rust":       "Rust. Complete program with fn main().",
    "kotlin":     "Kotlin. Complete program with fun main().",
    "swift":      "Swift. Top-level script format.",
    "dart":       "Dart. void main() for programs.",
    "php":        "PHP 8. Start with <?php tag.",
}

_LANG_DISPLAY = {
    "python": "Python",
    "javascript": "JavaScript",
    "java": "Java",
    "cplusplus": "C++",
    "c": "C",
    "csharp": "C#",
    "go": "Go",
    "rust": "Rust",
    "php": "PHP",
    "kotlin": "Kotlin",
    "swift": "Swift",
    "dart": "Dart",
    "typescript": "TypeScript",
}


def _build_prompt(text: str, mode: str, custom_instruction: Optional[str] = None) -> str:
    from utils import PerfTracker
    PerfTracker.prompt_build_start = time.perf_counter()

    if mode.startswith("generate_code:"):
        parts = mode.split(":", 2)
        lang = parts[1].lower()
        lang_name = _LANG_DISPLAY.get(lang, lang.capitalize())
        lang_rules = _LANG_PROMPTS.get(lang, f"{lang_name}.")
        res = (
            f"{_CODE_SYSTEM_PROMPT}\n\n"
            f"{lang_rules}\n\n"
            f"REQUEST:\n{text.strip()}\n\nCODE:\n"
        )
        PerfTracker.prompt_build_end = time.perf_counter()
        return res

    if mode == "custom" and custom_instruction:
        mode_prompt = f"Follow this exact instruction to modify the text: {custom_instruction}"
    else:
        mode_prompt = MODE_PROMPTS.get(
            mode,
            MODE_PROMPTS["professional"]
        )

    # Use cached template
    template = _get_cached_prompt_template(mode)
    if mode == "custom" and custom_instruction:
        res = template.format(mode_prompt=mode_prompt, text=text.strip())
    else:
        res = template.format(text=text.strip())
    
    PerfTracker.prompt_build_end = time.perf_counter()
    return res


# ──────────────────────────────────────────────────────────────────────────────
# Prompt Template Caching
# ──────────────────────────────────────────────────────────────────────────────

# Cache for pre-compiled prompt templates to avoid repeated string operations
_PROMPT_TEMPLATE_CACHE: dict[str, str] = {}


def _get_cached_prompt_template(mode: str) -> str:
    """Get cached prompt template for a mode, or create and cache it."""
    if mode not in _PROMPT_TEMPLATE_CACHE:
        if mode.startswith("generate_code:"):
            parts = mode.split(":", 2)
            lang = parts[1].lower()
            lang_name = _LANG_DISPLAY.get(lang, lang.capitalize())
            lang_rules = _LANG_PROMPTS.get(lang, f"{lang_name}.")
            _PROMPT_TEMPLATE_CACHE[mode] = (
                f"{_CODE_SYSTEM_PROMPT.strip()}\n\n"
                f"{lang_rules}\n\n"
                f"REQUEST:\n{{text}}\n\nCODE:\n"
            )
        elif mode == "custom":
            _PROMPT_TEMPLATE_CACHE[mode] = f"{SYSTEM_PROMPT.strip()}\n\n{{mode_prompt}}\n\nINPUT:\n{{text}}\n\nOUTPUT:\n"
        else:
            mode_prompt = MODE_PROMPTS.get(mode, MODE_PROMPTS["professional"])
            _PROMPT_TEMPLATE_CACHE[mode] = f"{SYSTEM_PROMPT.strip()}\n\n{mode_prompt.strip()}\n\nINPUT:\n{{text}}\n\nOUTPUT:\n"
    return _PROMPT_TEMPLATE_CACHE[mode]


# ──────────────────────────────────────────────────────────────────────────────
# Response Cleanup
# ──────────────────────────────────────────────────────────────────────────────

# Modes that must preserve formatting, line breaks, and full length
_CODE_MODES = frozenset({"debug_code", "explain_code"})


def _is_code_mode(mode: str) -> bool:
    """Return True for any mode that generates or explains code."""
    return mode.startswith("generate_code:") or mode in _CODE_MODES


def _clean_response(text: str, mode: str) -> str:
    """
    Clean AI output.

    For code modes (generate_code:*, debug_code, explain_code):
      - Strip markdown fences only.
      - Preserve ALL lines, indentation, and blank lines.
      - Never flatten, truncate, or remove content.

    For text rewrite modes:
      - Remove markdown, echoed instructions, and redundant whitespace.
      - Apply sentence-level deduplication and length guard.
    """

    if not text:
        return ""

    # ── Code / explanation modes: minimal, non-destructive cleanup ────────────
    if _is_code_mode(mode):
        # Remove opening code fence (```python, ``` etc.)
        text = re.sub(r"^```[a-zA-Z0-9+#\-]*[ \t]*\n?", "", text)
        # Remove closing code fence at the very end
        text = re.sub(r"\n?```[ \t]*$", "", text)
        # Remove any remaining stray triple-backtick markers
        text = re.sub(r"```[a-zA-Z0-9+#\-]*", "", text)
        text = re.sub(r"```", "", text)
        # Return with original structure intact — NO line removal, NO flattening
        return text.strip()

    # ── Text rewrite modes ────────────────────────────────────────────────────
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

    # Flatten whitespace for single-line rewrite modes
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    # Remove wrapping quotes
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1].strip()

    # Short-mode guard: keep first sentence only + dedup + 180-char cap
    _long_modes = {
        "smart", "improve_prompt", "engineer_prompt", "email", "explain_code",
        "custom", "resume", "meeting_notes", "eli5", "debug_code",
    }
    if mode not in _long_modes and not _is_code_mode(mode):
        text = text.split("\n")[0]

        sentences = re.split(r'(?<=[.!?])\s+', text)
        unique_sentences: list[str] = []
        seen: set[str] = set()
        for sentence in sentences:
            normalized = sentence.strip().lower()
            if normalized and normalized not in seen:
                unique_sentences.append(sentence.strip())
                seen.add(normalized)
        text = " ".join(unique_sentences).strip()

        if len(text) > 180:
            cutoff = text[:180]
            text = (cutoff.rsplit(".", 1)[0] + ".") if "." in cutoff else cutoff

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
    prompt_est_tokens = len(prompt) // 4

    url = f"{host.rstrip('/')}/api/generate"

    # ── Per-mode token budgets ────────────────────────────────────────────────
    TOKEN_BUDGETS = {
        "grammar":         60,
        "shorten":         60,
        "tweet":           80,
        "professional":   120,
        "translate":      150,
        "linkedin":       150,
        "improve_prompt": 150,
        "smart":          150,
        "email":          200,
        "engineer_prompt":200,
        "eli5":           200,
        "explain_code":   400,
        "meeting_notes":  250,
        "resume":         300,
        "custom":         200,
        "debug_code":    1024,
    }

    if mode.startswith("generate_code:"):
        parts = mode.split(":")
        quality = parts[2] if len(parts) > 2 else "adaptive"
        word_count = len(text.split())
        if quality == "fast":
            num_predict = 250
        elif quality == "detailed":
            num_predict = 1000
        else:  # adaptive
            if word_count < 10:
                num_predict = 300   # simple one-liner programs
            elif word_count < 30:
                num_predict = 600   # medium complexity
            else:
                num_predict = 1000  # complex algorithms
    else:
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

    payload_bytes = len(json.dumps(payload).encode("utf-8"))

    logger.info(
        "GEN_START mode=%s num_predict=%d PROMPT_TOKEN_COUNT~%d REQUEST_PAYLOAD_SIZE=%d bytes",
        mode, num_predict, prompt_est_tokens, payload_bytes,
    )
    logger.info(
        "Ollama request: model=%s mode=%s prompt_tokens~%d num_predict=%d",
        model, mode, prompt_est_tokens, num_predict,
    )

    from utils import PerfTracker
    PerfTracker.http_setup_start = time.perf_counter()
    PerfTracker.ollama_start = time.perf_counter()

    session = _get_shared_session()

    try:
        response = session.post(
            url,
            json=payload,
            timeout=90,
            stream=True,        # Enable HTTP streaming
        )

        PerfTracker.http_setup_end = time.perf_counter()

        response.raise_for_status()
        logger.info("AI_REQUEST_SENT")

        # ── Stream tokens and accumulate ──────────────────────────────────────
        # BUG 3 FIX: Do NOT call _clean_response() on every chunk.
        # Yield raw accumulated text during streaming so the UI gets
        # real-time updates without destructive regex running 1000× on partial text.
        # _clean_response() runs exactly ONCE after the stream completes.
        full_response: list[str] = []
        token_count = 0
        for raw_line in response.iter_lines(chunk_size=1):
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
                    logger.info("FIRST_TOKEN t=%.3fs", PerfTracker.first_token - PerfTracker.ollama_start)
                full_response.append(token)
                token_count += 1
                # Yield the raw accumulated text — no cleaning mid-stream.
                # The UI displays this verbatim while generation is in progress.
                yield "".join(full_response)

            if chunk.get("done", False):
                break

        PerfTracker.generation_end = time.perf_counter()
        _gen_elapsed = PerfTracker.generation_end - PerfTracker.ollama_start
        _tps = token_count / (_gen_elapsed - (PerfTracker.first_token - PerfTracker.ollama_start)) if PerfTracker.first_token and _gen_elapsed > 0 else 0
        logger.info(
            "LAST_TOKEN t=%.3fs tokens=%d TOKENS_PER_SECOND=%.1f",
            _gen_elapsed,
            token_count,
            _tps,
        )

        # ── Single post-stream cleanup pass ───────────────────────────────────
        PerfTracker.response_clean_start = time.perf_counter()
        raw_result = "".join(full_response)
        cleaned_result = _clean_response(raw_result, mode)
        PerfTracker.response_clean_end = time.perf_counter()
        logger.info("AI_RESPONSE_RECEIVED")

        elapsed = time.perf_counter() - PerfTracker.ollama_start
        prefill_time = (PerfTracker.first_token - PerfTracker.ollama_start) if PerfTracker.first_token else elapsed
        tps_decode = token_count / (elapsed - prefill_time) if (elapsed - prefill_time) > 0 else 0
        logger.info(
            "GEN_COMPLETE mode=%s TTFT=%.2fs total=%.2fs raw_chars=%d final_chars=%d TOKENS_PER_SECOND=%.1f",
            mode, prefill_time, elapsed, len(raw_result), len(cleaned_result), tps_decode,
        )
        logger.info("FINAL_RESPONSE_LENGTH %d", len(cleaned_result))

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

        # Check local fast-path first (grammar micro-corrections without AI)
        fast_result = _local_fast_path(text, mode)
        if fast_result is not None:
            from utils import PerfTracker
            PerfTracker.ollama_start = time.perf_counter()
            PerfTracker.first_token = PerfTracker.ollama_start
            PerfTracker.generation_end = PerfTracker.ollama_start
            yield fast_result
            return

        # Build the prompt (same for all providers)
        prompt = _build_prompt(text, mode, custom_instruction)

        # Route to the configured provider (Ollama / Avelyn Cloud / Custom API)
        from providers import get_provider_for_settings
        from utils import PerfTracker
        
        PerfTracker.provider_select_start = time.perf_counter()
        provider = get_provider_for_settings(self._settings, mode, text)
        PerfTracker.provider_select_end = time.perf_counter()

        logger.info("AIProcessor.enhance: provider=%s mode=%s",
                    type(provider).__name__, mode)

        yield from provider.generate(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT,
            mode=mode,
            custom_instruction=custom_instruction,
            cancellation_check=cancellation_check,
        )

    def warm_model(self) -> None:
        """
        Warm up Ollama: load the model AND exercise the GPU compute path.
        Sending a real (tiny) prompt ensures the M1 GPU compute blocks are
        activated, not just the model weights loaded into RAM.
        """
        try:
            url = f"{self._settings.ollama_host.rstrip('/')}/api/generate"
            # Send a minimal real prompt so the GPU decode path is exercised.
            # An empty prompt loads weights but does NOT warm the compute units.
            payload = {
                "model": self._settings.ollama_model,
                "prompt": "Hi",
                "stream": False,
                "keep_alive": "24h",
                "options": {
                    "num_predict": 1,
                    "temperature": 0.0,
                    "num_ctx": 4096,
                },
            }
            logger.info("Ollama warm-up: sending minimal prompt to activate GPU compute path...")
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code == 200:
                data = response.json()
                load_ns = data.get("load_duration", 0)
                eval_ns = data.get("eval_duration", 0)
                logger.info(
                    "Ollama warm-up complete: load=%.2fs gpu_decode=%.2fs",
                    load_ns / 1e9, eval_ns / 1e9,
                )
            else:
                logger.warning("Ollama warm-up returned status %d", response.status_code)
        except Exception as exc:
            logger.warning("Ollama warm-up failed (non-fatal): %s", exc)

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