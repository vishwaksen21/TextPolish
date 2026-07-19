"""
Avelyn — AI Provider Layer
==========================

Implements a universal multi-provider AI backend:
  - OllamaProvider      (local, offline)
  - OpenRouterProvider  (Avelyn Cloud — user's own OpenRouter key)
  - CustomAPIProvider   (BYO key, any OpenAI-compatible endpoint)

All providers expose the same streaming Generator interface so that
AIProcessor never needs to know which backend is active.

Usage::

    provider = ProviderManager.get_provider(settings)
    for partial_text in provider.generate(prompt, system_prompt, mode,
                                           custom_instruction, cancel_fn):
        update_ui(partial_text)
"""

from __future__ import annotations

import json
import time
import threading
from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Generator, Optional
from pathlib import Path

import requests

from logger import logger


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
# Provider Enum
# ──────────────────────────────────────────────────────────────────────────────

class AIProvider(Enum):
    OLLAMA       = "ollama"
    GEMINI       = "gemini"
    AVELYN_CLOUD = "avelyn_cloud"
    CUSTOM_API   = "custom_api"


# ──────────────────────────────────────────────────────────────────────────────
# Provider Presets (Custom API)
# ──────────────────────────────────────────────────────────────────────────────

CUSTOM_PROVIDER_PRESETS: dict[str, str] = {
    "OpenAI":      "https://api.openai.com/v1",
    "OpenRouter":  "https://openrouter.ai/api/v1",
    "Anthropic":   "https://api.anthropic.com",
    "Groq":        "https://api.groq.com/openai/v1",
    "DeepSeek":    "https://api.deepseek.com",
    "Gemini":      "https://generativelanguage.googleapis.com/v1beta/openai",
    "LM Studio":   "http://localhost:1234/v1",
    "vLLM":        "http://localhost:8000/v1",
    "Custom":      "",
}

# Models available in Avelyn Cloud (OpenRouter)
AVELYN_CLOUD_MODELS: list[tuple[str, str]] = [
    ("GPT-4o Mini (Fast & Cheap)",          "openai/gpt-4o-mini"),
    ("Claude 3.5 Haiku (Fast & High Quality)", "anthropic/claude-3.5-haiku"),
    ("Gemini 2.5 Flash (Ultra Fast)",       "google/gemini-2.5-flash"),
    ("Gemma 3 27B (Free - Queued/Slow)",    "google/gemma-3-27b-it:free"),
    ("DeepSeek V3 (Free - Queued/Slow)",    "deepseek/deepseek-chat-v3-0324:free"),
    ("Kimi K2 (Free - Queued/Slow)",        "moonshotai/kimi-k2:free"),
    ("Qwen3 235B (Free - Queued/Slow)",     "qwen/qwen3-235b-a22b:free"),
]


def fetch_openrouter_models(api_key: Optional[str] = None) -> list[tuple[str, str]]:
    """
    Fetch available models from OpenRouter API and cache them locally.
    Returns a list of (display_name, model_id) tuples.
    Uses a 24-hour cache expiration check.
    """
    cache_path = Path.home() / ".avelyn" / "openrouter_models.json"
    
    # Check if cache is fresh (< 24 hours)
    if cache_path.exists():
        try:
            mtime = cache_path.stat().st_mtime
            if time.time() - mtime < 86400:  # 24 hours in seconds
                logger.debug("OpenRouter models cache is fresh. Using cached copy.")
                with open(cache_path, "r", encoding="utf-8") as fh:
                    cached = json.load(fh)
                    if cached:
                        return [(str(item[0]), str(item[1])) for item in cached]
        except Exception as e:
            logger.debug("Failed to read dynamic models cache: %s", e)

    # Try to fetch from API
    try:
        headers = {
            "HTTP-Referer": "https://avelyn.app",
            "X-Title": "Avelyn",
        }
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
            
        resp = requests.get("https://openrouter.ai/api/v1/models", headers=headers, timeout=5)
        if resp.ok:
            data = resp.json()
            models_list = data.get("data", [])
            if models_list:
                result = []
                for m in models_list:
                    model_id = m.get("id", "")
                    name = m.get("name", "")
                    is_free = False
                    pricing = m.get("pricing", {})
                    if pricing:
                        prompt_price = float(pricing.get("prompt", 0))
                        completion_price = float(pricing.get("completion", 0))
                        if prompt_price == 0 and completion_price == 0:
                            is_free = True
                    
                    display_name = name
                    if is_free and "free" not in name.lower():
                        display_name += " (Free)"
                    result.append((display_name, model_id))
                
                # Sort fast/paid models to top, then alphabetically
                result.sort(key=lambda x: ("free" in x[0].lower(), x[0]))
                
                # Cache them
                cache_path.parent.mkdir(parents=True, exist_ok=True)
                with open(cache_path, "w", encoding="utf-8") as fh:
                    json.dump(result, fh, indent=2)
                return result
    except Exception as e:
        logger.debug("Failed to fetch OpenRouter models dynamically: %s", e)
        
    # Read from cache if API fetch failed (even if older than 24 hours)
    if cache_path.exists():
        try:
            with open(cache_path, "r", encoding="utf-8") as fh:
                cached = json.load(fh)
                if cached:
                    return [(str(item[0]), str(item[1])) for item in cached]
        except Exception:
            pass
            
    # Fallback to hardcoded list
    return AVELYN_CLOUD_MODELS


# ──────────────────────────────────────────────────────────────────────────────
# Base Provider Interface
# ──────────────────────────────────────────────────────────────────────────────

class BaseProvider(ABC):
    """
    Abstract streaming AI provider.

    Subclasses must implement generate(), which yields progressively longer
    accumulated strings during streaming, then a final clean string at the end —
    exactly the same contract as _call_ollama() in ai_processor.py.
    """
    
    # Shared session for connection pooling
    _shared_session: Optional[requests.Session] = None
    _session_lock = threading.Lock()

    @classmethod
    def _get_session(cls) -> requests.Session:
        """Get or create a shared session for connection pooling."""
        if cls._shared_session is None:
            with cls._session_lock:
                if cls._shared_session is None:
                    cls._shared_session = requests.Session()
                    # Configure connection pooling
                    adapter = requests.adapters.HTTPAdapter(
                        pool_connections=10,
                        pool_maxsize=20,
                        max_retries=0,  # We handle retries at application level
                    )
                    cls._shared_session.mount('http://', adapter)
                    cls._shared_session.mount('https://', adapter)
        return cls._shared_session

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: str,
        mode: str,
        custom_instruction: Optional[str] = None,
        cancellation_check: Optional[Callable[[], bool]] = None,
    ) -> Generator[str, None, None]:
        """
        Yield partial (streaming) text, then one final cleaned result.
        Raise RuntimeError with a user-friendly message on any failure.
        """
        ...

    def test_connection(self) -> tuple[bool, str]:
        """
        Quick smoke-test.  Returns (success, human-readable message).
        Default implementation calls generate() with a tiny probe.
        """
        try:
            result = "".join(self.generate(
                prompt="Hi",
                system_prompt="Reply in one word.",
                mode="grammar",
            ))
            return True, f"Connected ({result.strip()[:20]})"
        except RuntimeError as exc:
            return False, str(exc)
        except Exception as exc:
            return False, f"Unexpected error: {exc}"


# ──────────────────────────────────────────────────────────────────────────────
# Ollama Provider
# ──────────────────────────────────────────────────────────────────────────────

class OllamaProvider(BaseProvider):
    """
    Wraps the existing Ollama backend.  Delegates directly to _call_ollama()
    in ai_processor so that all existing logic (token budgets, keep_alive,
    num_ctx, perf tracking) remains unchanged.
    """

    def __init__(self, host: str, model: str) -> None:
        self._host  = host
        self._model = model

    def generate(
        self,
        prompt: str,
        system_prompt: str,
        mode: str,
        custom_instruction: Optional[str] = None,
        cancellation_check: Optional[Callable[[], bool]] = None,
    ) -> Generator[str, None, None]:
        # Import here to avoid a circular dependency at module load time.
        from ai_processor import _call_ollama
        yield from _call_ollama(
            text=prompt,
            mode=mode,
            host=self._host,
            model=self._model,
            custom_instruction=custom_instruction,
            cancellation_check=cancellation_check,
        )

    def test_connection(self) -> tuple[bool, str]:
        try:
            url = f"{self._host.rstrip('/')}/api/tags"
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            models = [m.get("name", "") for m in data.get("models", [])]
            if self._model in models:
                return True, f"Connected · {self._model} available"
            elif models:
                return True, f"Connected · {self._model} not found (available: {', '.join(models[:3])})"
            else:
                return True, "Connected · no models loaded yet"
        except requests.ConnectionError:
            return False, f"Cannot connect to Ollama at {self._host}"
        except requests.Timeout:
            return False, "Connection timed out"
        except Exception as exc:
            return False, f"Error: {exc}"


# ──────────────────────────────────────────────────────────────────────────────
# OpenRouter Provider  (Avelyn Cloud)
# ──────────────────────────────────────────────────────────────────────────────

_OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class OpenRouterProvider(BaseProvider):
    """
    Calls the OpenRouter API using the user's own API key.
    Supports streaming SSE (Server-Sent Events) in the same pattern as Ollama.
    """

    def __init__(self, api_key: str, model: str) -> None:
        self._api_key = api_key
        self._model   = model
        self._session = _get_shared_session()

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization":  f"Bearer {self._api_key}",
            "Content-Type":   "application/json",
            "HTTP-Referer":   "https://avelyn.app",
            "X-Title":        "Avelyn",
        }

    @staticmethod
    def _mask_key(key: str) -> str:
        if len(key) <= 8:
            return "***"
        return key[:4] + "****" + key[-4:]

# ── Core streaming call ───────────────────────────────────────────────────

    def generate(
        self,
        prompt: str,
        system_prompt: str,
        mode: str,
        custom_instruction: Optional[str] = None,
        cancellation_check: Optional[Callable[[], bool]] = None,
    ) -> Generator[str, None, None]:

        if not self._api_key:
            raise RuntimeError("Avelyn Cloud: no API key configured. Add your OpenRouter key in Settings → AI Provider.")

        # Build the message array expected by the /chat/completions endpoint
        messages = [
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user",   "content": prompt.strip()},
        ]

        # Estimate prompt tokens (rough: 1 token ≈ 4 chars)
        prompt_text = system_prompt.strip() + "\n" + prompt.strip()
        prompt_tokens = len(prompt_text) // 4

        payload = {
            "model":       self._model,
            "messages":    messages,
            "stream":      True,
            "temperature": 0.15,
            "max_tokens":  4096,
        }

        # Log complete request details for benchmarking
        logger.info("=" * 60)
        logger.info("OPENROUTER REQUEST DETAILS")
        logger.info("=" * 60)
        logger.info("Model:           %s", self._model)
        logger.info("Prompt Tokens:   %d (est)", prompt_tokens)
        logger.info("Max Tokens:      %d", payload["max_tokens"])
        logger.info("Temperature:     %.2f", payload["temperature"])
        logger.info("Stream:          %s", payload["stream"])
        logger.info("System Prompt:   %d chars", len(system_prompt.strip()))
        logger.info("User Prompt:     %d chars", len(prompt.strip()))
        logger.info("Total Prompt:    %d chars", len(prompt_text))
        logger.info("Payload JSON:    %s", json.dumps(payload, separators=(',', ':'))[:500])
        logger.info("=" * 60)

        from utils import PerfTracker
        PerfTracker.ollama_start = time.perf_counter()

        try:
            response = self._session.post(
                _OPENROUTER_URL,
                headers=self._headers(),
                json=payload,
                timeout=90,
                stream=True,
            )
        except requests.ConnectionError:
            raise RuntimeError("Cannot connect to Avelyn Cloud. Check your internet connection.")
        except requests.Timeout:
            raise RuntimeError("Avelyn Cloud request timed out.")

        # ── HTTP-level error handling ─────────────────────────────────────────
        if response.status_code >= 500:
            raise RuntimeError("Provider is temporarily unavailable.")
        if response.status_code == 401:
            raise RuntimeError("Invalid API key. Check your OpenRouter key in Settings.")
        if response.status_code == 402:
            raise RuntimeError("Insufficient credits on your OpenRouter account.")
        if response.status_code == 429:
            raise RuntimeError("Rate limit reached. Try again in a moment.")
        if response.status_code == 404:
            raise RuntimeError(f"Model '{self._model}' not found on OpenRouter.")
        if not response.ok:
            raise RuntimeError(f"Avelyn Cloud error {response.status_code}: {response.text[:120]}")

        # ── Stream SSE tokens ─────────────────────────────────────────────────
        full_response: list[str] = []
        token_count   = 0

        for raw_line in response.iter_lines(chunk_size=1):
            if cancellation_check and cancellation_check():
                response.close()
                return

            if not raw_line:
                continue

            line = raw_line.decode("utf-8") if isinstance(raw_line, bytes) else raw_line
            if not line.startswith("data: "):
                continue
            data_str = line[6:].strip()
            if data_str == "[DONE]":
                break

            try:
                chunk = json.loads(data_str)
            except json.JSONDecodeError:
                continue

            delta = chunk.get("choices", [{}])[0].get("delta", {})
            token = delta.get("content", "")
            if token:
                if not PerfTracker.first_token:
                    PerfTracker.first_token = time.perf_counter()
                    logger.info("FIRST_TOKEN t=%.3fs",
                                PerfTracker.first_token - PerfTracker.ollama_start)
                full_response.append(token)
                token_count += 1
                yield "".join(full_response)

        PerfTracker.generation_end = time.perf_counter()
        raw_result = "".join(full_response)

        # Run the same post-stream cleanup as Ollama
        from ai_processor import _clean_response
        cleaned = _clean_response(raw_result, mode)

        logger.info("OpenRouter complete: mode=%s tokens=%d chars=%d→%d",
                    mode, token_count, len(raw_result), len(cleaned))

        if cleaned:
            yield cleaned

    # ── Test connection ───────────────────────────────────────────────────────

    def test_connection(self) -> tuple[bool, str]:
        if not self._api_key:
            return False, "No API key entered"
        try:
            resp = requests.get(
                "https://openrouter.ai/api/v1/models",
                headers=self._headers(),
                timeout=8,
            )
            if resp.status_code == 401:
                return False, "Invalid API key"
            if resp.status_code == 429:
                return False, "Rate limited — key is valid"
            resp.raise_for_status()
            return True, f"Connected · {self._model}"
        except requests.ConnectionError:
            return False, "Network Error — check internet connection"
        except requests.Timeout:
            return False, "Connection timed out"
        except Exception as exc:
            return False, f"Error: {exc}"


# ──────────────────────────────────────────────────────────────────────────────
# Gemini Provider (Google Gen AI SDK)
# ──────────────────────────────────────────────────────────────────────────────

# Default built-in Gemini API key (centralized for easy rotation)
_DEFAULT_GEMINI_API_KEY = "AQ.Ab8RN6LmRkep9BnEMfCKFWOPKh8LW7xYj84KY_86tmz7kKKSEw"


class GeminiProvider(BaseProvider):
    """
    Calls the Google Gemini API using the official google-genai Python SDK.
    Supports streaming responses with the same interface as other providers.
    """

    def __init__(self, api_key: str = "", model: str = "models/gemini-flash-latest") -> None:
        self._user_api_key = api_key
        self._model = model
        self._client = self._create_client()

    def _create_client(self):
        """Create a GenAI client with the effective API key."""
        try:
            from google import genai
            api_key = self._get_api_key()
            client = genai.Client(api_key=api_key)
            logger.info("GeminiProvider: Created GenAI client for model %s", self._model)
            return client
        except Exception as e:
            logger.error("GeminiProvider: Failed to create GenAI client: %s", e)
            raise RuntimeError(f"Failed to initialize Google GenAI SDK: {e}")

    def _get_api_key(self) -> str:
        """Return the effective API key: user-provided > built-in default."""
        return self._user_api_key if self._user_api_key else _DEFAULT_GEMINI_API_KEY

    def _headers(self) -> dict[str, str]:
        """Not used for GenAI SDK but kept for interface compatibility."""
        return {}

    @staticmethod
    def _mask_key(key: str) -> str:
        if len(key) <= 8:
            return "***"
        return key[:4] + "****" + key[-4:]

    def generate(
        self,
        prompt: str,
        system_prompt: str,
        mode: str,
        custom_instruction: Optional[str] = None,
        cancellation_check: Optional[Callable[[], bool]] = None,
    ) -> Generator[str, None, None]:

        api_key = self._get_api_key()
        if not api_key:
            raise RuntimeError("Gemini: no API key configured. Add your Google AI key in Settings → AI Provider.")

        # Estimate prompt tokens (rough: 1 token ≈ 4 chars)
        prompt_text = system_prompt.strip() + "\n" + prompt.strip()
        prompt_tokens = len(prompt_text) // 4

        # Configure generation - optimized for speed
        from google.genai import types
        
        # Use smaller max tokens for rewrite tasks (most outputs < 1024 tokens)
        max_tokens = 1024 if mode not in ("explain_code", "debug_code", "engineer_prompt", "smart") else 2048
        
        config = types.GenerateContentConfig(
            temperature=0.0,  # Deterministic = faster
            max_output_tokens=max_tokens,
            system_instruction=system_prompt.strip(),
            # Disable thinking for flash models (faster)
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        )

        # Log request details for benchmarking
        logger.info("=" * 60)
        logger.info("GEMINI REQUEST DETAILS")
        logger.info("=" * 60)
        logger.info("Model:           %s", self._model)
        logger.info("Prompt Tokens:   %d (est)", prompt_tokens)
        logger.info("Max Tokens:      %d", config.max_output_tokens)
        logger.info("Temperature:     %.2f", config.temperature)
        logger.info("System Prompt:   %d chars", len(system_prompt.strip()))
        logger.info("User Prompt:     %d chars", len(prompt.strip()))
        logger.info("Total Prompt:    %d chars", len(prompt_text))
        logger.info("API Key:         %s", self._mask_key(api_key))
        logger.info("=" * 60)

        from utils import PerfTracker
        PerfTracker.ollama_start = time.perf_counter()

        try:
            # Use the GenAI SDK with streaming
            response_stream = self._client.models.generate_content_stream(
                model=self._model,
                contents=prompt.strip(),
                config=config,
            )

            full_response: list[str] = []
            token_count = 0

            for chunk in response_stream:
                if cancellation_check and cancellation_check():
                    logger.info("Gemini request cancelled cooperatively.")
                    return

                # Extract text from chunk
                if chunk.text:
                    if not PerfTracker.first_token:
                        PerfTracker.first_token = time.perf_counter()
                        logger.info("FIRST_TOKEN t=%.3fs",
                                    PerfTracker.first_token - PerfTracker.ollama_start)
                    full_response.append(chunk.text)
                    token_count += 1
                    yield "".join(full_response)

            PerfTracker.generation_end = time.perf_counter()
            raw_result = "".join(full_response)

            # Post-stream cleanup
            from ai_processor import _clean_response
            cleaned = _clean_response(raw_result, mode)

            logger.info("Gemini complete: mode=%s tokens=%d chars=%d→%d",
                        mode, token_count, len(raw_result), len(cleaned))

            if cleaned:
                yield cleaned

        except Exception as exc:
            logger.error("Gemini error: %s", exc)
            # Provide user-friendly error messages
            error_msg = str(exc).lower()
            if "api key" in error_msg or "unauthorized" in error_msg or "401" in error_msg:
                raise RuntimeError("Invalid Gemini API key. Check your key in Settings.")
            elif "quota" in error_msg or "429" in error_msg:
                raise RuntimeError("Gemini rate limit reached. Try again in a moment.")
            elif "not found" in error_msg or "404" in error_msg:
                raise RuntimeError(f"Model '{self._model}' not found or not accessible.")
            elif "network" in error_msg or "connection" in error_msg:
                raise RuntimeError("Cannot connect to Gemini API. Check your internet connection.")
            else:
                raise RuntimeError(f"Gemini error: {exc}")

    def test_connection(self) -> tuple[bool, str]:
        """Quick connection test using a minimal prompt."""
        api_key = self._get_api_key()
        if not api_key:
            return False, "No API key configured"
        try:
            from google.genai import types
            config = types.GenerateContentConfig(
                max_output_tokens=1,
                temperature=0.0,
            )
            response = self._client.models.generate_content(
                model=self._model,
                contents="Hi",
                config=config,
            )
            if response.text:
                return True, f"Connected · {self._model}"
            return True, f"Connected · {self._model} (no response text)"
        except Exception as exc:
            error_msg = str(exc).lower()
            if "api key" in error_msg or "unauthorized" in error_msg or "401" in error_msg:
                return False, "Invalid API key"
            elif "quota" in error_msg or "429" in error_msg:
                return False, "Rate limited — key is valid"
            elif "network" in error_msg or "connection" in error_msg:
                return False, "Network Error — check internet connection"
            return False, f"Error: {exc}"


# ──────────────────────────────────────────────────────────────────────────────
# Custom API Provider  (BYO key, OpenAI-compatible)
# ──────────────────────────────────────────────────────────────────────────────

class CustomAPIProvider(BaseProvider):
    """
    OpenAI-compatible chat completions endpoint.
    Works with: OpenAI, Groq, DeepSeek, Gemini (OpenAI-compat path),
    LM Studio, vLLM, and any server that implements /chat/completions.

    Anthropic's native /v1/messages format is NOT supported — use Anthropic
    via OpenRouter instead (they have an OpenAI-compat wrapper).
    """

    def __init__(self, base_url: str, api_key: str, model: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key  = api_key
        self._model    = model
        self._session  = _get_shared_session()

    def _headers(self) -> dict[str, str]:
        h: dict[str, str] = {"Content-Type": "application/json"}
        if self._api_key:
            h["Authorization"] = f"Bearer {self._api_key}"
        return h

    @staticmethod
    def _mask_key(key: str) -> str:
        if len(key) <= 8:
            return "***"
        return key[:4] + "****" + key[-4:]

    def generate(
        self,
        prompt: str,
        system_prompt: str,
        mode: str,
        custom_instruction: Optional[str] = None,
        cancellation_check: Optional[Callable[[], bool]] = None,
    ) -> Generator[str, None, None]:

        if not self._base_url:
            raise RuntimeError("Custom API: no base URL configured. Set it in Settings → AI Provider.")

        url = f"{self._base_url}/chat/completions"
        messages = [
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user",   "content": prompt.strip()},
        ]
        payload = {
            "model":       self._model,
            "messages":    messages,
            "stream":      True,
            "temperature": 0.15,
            "max_tokens":  4096,
        }

        logger.info("CustomAPI request: url=%s model=%s mode=%s key=%s",
                    url, self._model, mode,
                    self._mask_key(self._api_key) if self._api_key else "(none)")

        from utils import PerfTracker
        PerfTracker.ollama_start = time.perf_counter()

        try:
            response = requests.post(
                url,
                headers=self._headers(),
                json=payload,
                timeout=90,
                stream=True,
            )
        except requests.ConnectionError:
            raise RuntimeError(f"Cannot connect to {self._base_url}. Check the URL and server.")
        except requests.Timeout:
            raise RuntimeError("Custom API request timed out.")

        if response.status_code >= 500:
            raise RuntimeError("Provider is temporarily unavailable.")
        if response.status_code == 401:
            raise RuntimeError("Invalid API key for the custom endpoint.")
        if response.status_code == 429:
            raise RuntimeError("Rate limit reached. Try again in a moment.")
        if response.status_code == 404:
            raise RuntimeError(f"Model '{self._model}' not found or endpoint URL is wrong.")
        if not response.ok:
            raise RuntimeError(f"Custom API error {response.status_code}: {response.text[:120]}")

        full_response: list[str] = []
        token_count   = 0

        for raw_line in response.iter_lines():
            if cancellation_check and cancellation_check():
                response.close()
                return

            if not raw_line:
                continue
            line = raw_line.decode("utf-8") if isinstance(raw_line, bytes) else raw_line
            if not line.startswith("data: "):
                continue
            data_str = line[6:].strip()
            if data_str == "[DONE]":
                break

            try:
                chunk = json.loads(data_str)
            except json.JSONDecodeError:
                continue

            delta = chunk.get("choices", [{}])[0].get("delta", {})
            token = delta.get("content", "")
            if token:
                if not PerfTracker.first_token:
                    PerfTracker.first_token = time.perf_counter()
                full_response.append(token)
                token_count += 1
                yield "".join(full_response)

        PerfTracker.generation_end = time.perf_counter()
        raw_result = "".join(full_response)

        from ai_processor import _clean_response
        cleaned = _clean_response(raw_result, mode)

        logger.info("CustomAPI complete: mode=%s tokens=%d chars=%d→%d",
                    mode, token_count, len(raw_result), len(cleaned))

        if cleaned:
            yield cleaned

    def test_connection(self) -> tuple[bool, str]:
        if not self._base_url:
            return False, "No base URL entered"
        try:
            # Try /models endpoint (standard OpenAI-compat)
            resp = requests.get(
                f"{self._base_url}/models",
                headers=self._headers(),
                timeout=8,
            )
            if resp.status_code == 401:
                return False, "Invalid API key"
            if resp.status_code == 404:
                # Some servers don't have /models — try a minimal completions call
                return self._test_via_completion()
            if not resp.ok:
                return False, f"HTTP {resp.status_code}"
            return True, f"Connected · {self._model}"
        except requests.ConnectionError:
            return False, f"Cannot connect to {self._base_url}"
        except requests.Timeout:
            return False, "Connection timed out"
        except Exception as exc:
            return False, f"Error: {exc}"

    def _test_via_completion(self) -> tuple[bool, str]:
        """Fallback test: send a minimal non-streaming completion."""
        try:
            url = f"{self._base_url}/chat/completions"
            payload = {
                "model": self._model,
                "messages": [{"role": "user", "content": "hi"}],
                "max_tokens": 1,
                "stream": False,
            }
            resp = requests.post(url, headers=self._headers(), json=payload, timeout=10)
            if resp.status_code == 401:
                return False, "Invalid API key"
            if resp.status_code == 404:
                return False, f"Model '{self._model}' not found"
            if not resp.ok:
                return False, f"HTTP {resp.status_code}"
            return True, f"Connected · {self._model}"
        except Exception as exc:
            return False, str(exc)


# ──────────────────────────────────────────────────────────────────────────────
# Task Groups & Routing rules
# ──────────────────────────────────────────────────────────────────────────────

TASK_GROUPS = {
    "coding": {
        "modes": ["explain_code", "debug_code", "refactor_code"],
        "prefixes": ["generate_code:"]
    },
    "writing": {
        "modes": ["professional", "email", "linkedin", "tweet", "summarize", "shorten", "expand", "resume", "meeting_notes", "translate"],
        "prefixes": []
    },
    "reasoning": {
        "modes": ["smart", "eli5", "improve_prompt", "engineer_prompt"],
        "prefixes": []
    },
    "voice": {
        "modes": ["voice_default"],
        "prefixes": ["voice:"]
    },
    "privacy": {
        "modes": ["privacy"],
        "prefixes": []
    }
}


def get_task_group(mode: str) -> str:
    """Map a command palette mode to one of the 6 task groups (coding, writing, reasoning, voice, privacy, default)."""
    from utils import PerfTracker
    PerfTracker.router_start = time.perf_counter()
    
    for group, rule in TASK_GROUPS.items():
        if mode in rule["modes"]:
            PerfTracker.router_end = time.perf_counter()
            return group
        if any(mode.startswith(p) for p in rule["prefixes"]):
            PerfTracker.router_end = time.perf_counter()
            return group
    PerfTracker.router_end = time.perf_counter()
    return "default"


def _make_provider_instance(settings, provider_name: str, model: str) -> BaseProvider:
    """Helper to instantiate a provider by name with settings and custom model override."""
    # Use cached instances if settings haven't changed
    cache_key = (provider_name, model, settings.ollama_host, settings.avelyn_cloud_api_key, 
                 settings.gemini_api_key, settings.custom_api_base_url, settings.custom_api_key)
    if not hasattr(_make_provider_instance, '_cache'):
        _make_provider_instance._cache = {}
    if cache_key in _make_provider_instance._cache:
        return _make_provider_instance._cache[cache_key]
    
    if provider_name == AIProvider.AVELYN_CLOUD.value:
        provider = OpenRouterProvider(
            api_key=settings.avelyn_cloud_api_key,
            model=model,
        )
    elif provider_name == AIProvider.GEMINI.value:
        provider = GeminiProvider(
            api_key=settings.gemini_api_key,
            model=model,
        )
    elif provider_name == AIProvider.CUSTOM_API.value:
        provider = CustomAPIProvider(
            base_url=settings.custom_api_base_url,
            api_key=settings.custom_api_key,
            model=model,
        )
    else:
        # Default to local Ollama
        provider = OllamaProvider(
            host=settings.ollama_host,
            model=model,
        )
    
    _make_provider_instance._cache[cache_key] = provider
    return provider


# ──────────────────────────────────────────────────────────────────────────────
# Provider Manager  (factory + smart fallback)
# ──────────────────────────────────────────────────────────────────────────────

class ProviderManager:
    """
    Factory that reads settings and returns the configured provider.

    Supports:
      1. Single Provider: Everything routes to settings.ai_provider.
      2. Smart Router: Routing based on task mode (coding, writing, reasoning, voice, privacy, default).
    """

    @staticmethod
    def get_single_provider(settings) -> BaseProvider:
        """Return the active provider instance from current settings (for single provider mode)."""
        from utils import PerfTracker
        PerfTracker.provider_creation_start = time.perf_counter()
        
        provider_name = settings.ai_provider
        
        logger.info("ProviderSelection: mode=single, ai_provider='%s', available=[ollama, gemini, avelyn_cloud, custom_api]",
                    provider_name)
        
        if provider_name == AIProvider.AVELYN_CLOUD.value:
            provider = OpenRouterProvider(
                api_key=settings.avelyn_cloud_api_key,
                model=settings.avelyn_cloud_model,
            )
        elif provider_name == AIProvider.GEMINI.value:
            provider = GeminiProvider(
                api_key=settings.gemini_api_key,
                model=settings.gemini_model,
            )
        elif provider_name == AIProvider.CUSTOM_API.value:
            provider = CustomAPIProvider(
                base_url=settings.custom_api_base_url,
                api_key=settings.custom_api_key,
                model=settings.custom_api_model,
            )
        else:
            # Default / "ollama"
            provider = OllamaProvider(
                host=settings.ollama_host,
                model=settings.ollama_model,
            )
        
        PerfTracker.provider_creation_end = time.perf_counter()
        logger.info("ProviderSelection: selected %s (model=%s)",
                    type(provider).__name__, getattr(provider, '_model', 'N/A'))
        return provider

    @staticmethod
    def get_routed_provider(settings, mode: str) -> BaseProvider:
        """Return the correct provider dynamically routed by the task mode from router_config."""
        from utils import PerfTracker
        PerfTracker.provider_selection_start = time.perf_counter()
        
        task = get_task_group(mode)
        task_config = settings.router_config.get(task, {})
        
        provider_name = task_config.get("provider", "ollama")
        model = task_config.get("model", "gemma3:4b")
        
        logger.info("SmartRouter: routed mode '%s' (task '%s') to provider '%s' with model '%s'",
                    mode, task, provider_name, model)
        
        PerfTracker.provider_selection_end = time.perf_counter()
        PerfTracker.provider_creation_start = time.perf_counter()
        
        provider = _make_provider_instance(settings, provider_name, model)
        
        PerfTracker.provider_creation_end = time.perf_counter()
        return provider

    @staticmethod
    def get_auto_routed_provider(settings, mode: str, text: str) -> BaseProvider:
        """
        Dynamically route based on selected text length, content, and task group:
          - Selected text is very short (< 50 chars) and privacy/default task -> Local Ollama.
          - Privacy/Local tasks -> Local Ollama.
          - Coding task or programming syntax in text -> Router Coding Provider.
          - Long documents (> 2000 chars) -> Router Writing Provider.
          - Default -> Task-specific provider.
        """
        from utils import PerfTracker
        PerfTracker.provider_selection_start = time.perf_counter()
        
        text_len = len(text)
        task = get_task_group(mode)
        
        logger.info("AutoRouter: input: mode='%s', text_len=%d, task='%s', ai_provider_mode='%s'",
                    mode, text_len, task, settings.ai_provider_mode)
        
        # 1. Local/Short text path (only for privacy or default tasks)
        # Check if the configured provider for this task is ollama, otherwise use the configured provider
        task_config = settings.router_config.get(task, {})
        configured_provider = task_config.get("provider", "ollama")
        
        if text_len < 50 and task in ("privacy", "default") and configured_provider == "ollama":
            logger.info("AutoRouter: text is short (%d chars) and task is '%s' with ollama provider -> routing to Ollama", text_len, task)
            PerfTracker.provider_selection_end = time.perf_counter()
            PerfTracker.provider_creation_start = time.perf_counter()
            provider = OllamaProvider(settings.ollama_host, settings.ollama_model)
            PerfTracker.provider_creation_end = time.perf_counter()
            return provider
            
        # 2. Local/Privacy task path
        if task == "privacy":
            logger.info("AutoRouter: privacy task -> routing to Ollama")
            PerfTracker.provider_selection_end = time.perf_counter()
            PerfTracker.provider_creation_start = time.perf_counter()
            provider = OllamaProvider(settings.ollama_host, settings.ollama_model)
            PerfTracker.provider_creation_end = time.perf_counter()
            return provider
            
        # 3. Coding tasks / Syntax detection
        is_code = (
            task == "coding"
            or "def " in text
            or "class " in text
            or "function " in text
            or "{" in text
            or "import " in text
        )
        if is_code:
            logger.info("AutoRouter: coding content/syntax detected -> routing to Coding task provider")
            task_config = settings.router_config.get("coding", {})
            PerfTracker.provider_selection_end = time.perf_counter()
            PerfTracker.provider_creation_start = time.perf_counter()
            provider = _make_provider_instance(settings, task_config.get("provider", "ollama"), task_config.get("model", "gemma3:4b"))
            PerfTracker.provider_creation_end = time.perf_counter()
            return provider
            
        # 4. Long documents (> 2000 chars)
        if text_len > 2000:
            logger.info("AutoRouter: long document (%d chars) -> routing to Writing task provider", text_len)
            task_config = settings.router_config.get("writing", {})
            PerfTracker.provider_selection_end = time.perf_counter()
            PerfTracker.provider_creation_start = time.perf_counter()
            provider = _make_provider_instance(settings, task_config.get("provider", "avelyn_cloud"), task_config.get("model", "openai/gpt-4o-mini"))
            PerfTracker.provider_creation_end = time.perf_counter()
            return provider
            
        # 5. Fallback/Standard routing
        task_config = settings.router_config.get(task, {})
        provider_name = task_config.get("provider", "ollama")
        model = task_config.get("model", "gemma3:4b")
        logger.info("AutoRouter: standard match -> routed mode '%s' (task '%s') to provider '%s' with model '%s' (from router_config['%s'])",
                    mode, task, provider_name, model, task)
        
        PerfTracker.provider_selection_end = time.perf_counter()
        PerfTracker.provider_creation_start = time.perf_counter()
        provider = _make_provider_instance(settings, provider_name, model)
        PerfTracker.provider_creation_end = time.perf_counter()
        return provider

    @staticmethod
    def get_fallback_chain(settings, mode: str, text: str = "") -> list[BaseProvider]:
        """
        Return [primary, fallback1, fallback2] ordered by user-configurable priority,
        with each fallback running task-specific models.
        """
        from utils import PerfTracker
        PerfTracker.smart_fallback_init_start = time.perf_counter()
        
        chain: list[BaseProvider] = []
        
        # Determine active primary
        if settings.ai_provider_mode == "auto":
            primary_provider = ProviderManager.get_auto_routed_provider(settings, mode, text)
        elif settings.ai_provider_mode == "smart_router":
            primary_provider = ProviderManager.get_routed_provider(settings, mode)
        else:
            primary_provider = ProviderManager.get_single_provider(settings)
            
        chain.append(primary_provider)

        # Get task-appropriate models for fallbacks
        task = get_task_group(mode)
        
        # Helper to extract the model configured for a task under a specific provider
        def _get_model_for_provider_and_task(provider_name: str, task_name: str) -> str:
            # Check smart router configuration
            task_config = settings.router_config.get(task_name, {})
            # If the provider is the one we configure for this task, use the configured model.
            if task_config.get("provider") == provider_name:
                return task_config.get("model", "gemma3:4b")
            
            # Fall back to provider default models
            if provider_name == "avelyn_cloud":
                return settings.avelyn_cloud_model
            if provider_name == "gemini":
                return settings.gemini_model
            if provider_name == "custom_api":
                return settings.custom_api_model
            return settings.ollama_model

        # Determine type of primary provider
        if isinstance(primary_provider, OllamaProvider):
            primary_type = "ollama"
        elif isinstance(primary_provider, OpenRouterProvider):
            primary_type = "avelyn_cloud"
        elif isinstance(primary_provider, GeminiProvider):
            primary_type = "gemini"
        else:
            primary_type = "custom_api"

        # Follow user-configured priority list for remaining fallbacks (copy list to avoid mutation)
        fallback_order = list(settings.fallback_chain)
        # Ensure we have all provider types represented in case of config deletion
        for pt in ["ollama", "gemini", "avelyn_cloud", "custom_api"]:
            if pt not in fallback_order:
                fallback_order.append(pt)

        # Build clean remaining chain by skipping already seen provider types (prevents duplicates)
        seen = {primary_type}
        remaining = []
        for p in fallback_order:
            if p not in seen:
                seen.add(p)
                remaining.append(p)

        for p in remaining:
            m = _get_model_for_provider_and_task(p, task)
            if p == "ollama":
                chain.append(OllamaProvider(settings.ollama_host, m))
            elif p == "gemini":
                chain.append(GeminiProvider(settings.gemini_api_key, m))
            elif p == "avelyn_cloud" and settings.avelyn_cloud_api_key:
                chain.append(OpenRouterProvider(settings.avelyn_cloud_api_key, m))
            elif p == "custom_api" and settings.custom_api_base_url:
                chain.append(CustomAPIProvider(settings.custom_api_base_url, settings.custom_api_key, m))

        PerfTracker.smart_fallback_init_end = time.perf_counter()
        return chain


class SmartFallbackProvider(BaseProvider):
    """
    Wraps a provider chain.  On RuntimeError from the primary provider,
    automatically retries with the next available provider.
    """

    def __init__(self, chain: list[BaseProvider]) -> None:
        self._chain = chain

    def generate(
        self,
        prompt: str,
        system_prompt: str,
        mode: str,
        custom_instruction: Optional[str] = None,
        cancellation_check: Optional[Callable[[], bool]] = None,
    ) -> Generator[str, None, None]:

        last_exc: Optional[RuntimeError] = None
        for i, provider in enumerate(self._chain):
            try:
                logger.info("SmartFallback: trying provider %d/%d: %s",
                            i + 1, len(self._chain), type(provider).__name__)
                yield from provider.generate(prompt, system_prompt, mode,
                                             custom_instruction, cancellation_check)
                return   # success
            except RuntimeError as exc:
                logger.warning("SmartFallback: provider %s failed: %s — trying next",
                               type(provider).__name__, exc)
                last_exc = exc

        # All providers failed
        raise last_exc or RuntimeError("All AI providers failed.")


def get_provider_for_settings(settings, mode: str = "grammar", text: str = "") -> BaseProvider:
    """
    Public convenience function used by AIProcessor.
    Returns SmartFallbackProvider when enabled, otherwise the routed or primary provider.
    """
    from utils import PerfTracker
    PerfTracker.provider_selection_start = time.perf_counter()
    
    # Log the decision context
    logger.info("=" * 60)
    logger.info("PROVIDER SELECTION: mode='%s', text_len=%d, ai_provider_mode='%s', ai_provider='%s', smart_fallback=%s",
                mode, len(text), settings.ai_provider_mode, settings.ai_provider, settings.smart_fallback_enabled)
    logger.info("ROUTER CONFIG: %s", settings.router_config)
    logger.info("FALLBACK CHAIN: %s", settings.fallback_chain)
    
    if settings.smart_fallback_enabled:
        chain = ProviderManager.get_fallback_chain(settings, mode, text)
        if len(chain) > 1:
            PerfTracker.provider_selection_end = time.perf_counter()
            logger.info("PROVIDER SELECTED: SmartFallbackProvider (chain: %s)", [type(p).__name__ for p in chain])
            return SmartFallbackProvider(chain)
        
    if settings.ai_provider_mode == "auto":
        provider = ProviderManager.get_auto_routed_provider(settings, mode, text)
        PerfTracker.provider_selection_end = time.perf_counter()
        logger.info("PROVIDER SELECTED: %s (via AutoRouter)", type(provider).__name__)
        return provider
        
    if settings.ai_provider_mode == "smart_router":
        provider = ProviderManager.get_routed_provider(settings, mode)
        PerfTracker.provider_selection_end = time.perf_counter()
        logger.info("PROVIDER SELECTED: %s (via SmartRouter)", type(provider).__name__)
        return provider
        
    provider = ProviderManager.get_single_provider(settings)
    PerfTracker.provider_selection_end = time.perf_counter()
    logger.info("PROVIDER SELECTED: %s (via SingleProvider: ai_provider='%s')", type(provider).__name__, settings.ai_provider)
    return provider


# ──────────────────────────────────────────────────────────────────────────────
# Standalone test helper  (used by Settings UI)
# ──────────────────────────────────────────────────────────────────────────────

def test_provider_connection(provider: BaseProvider) -> tuple[bool, str]:
    """
    Run the provider's test_connection() and return (success, display_message).
    The display message is safe to show directly in the UI status badge.
    """
    try:
        return provider.test_connection()
    except Exception as exc:
        return False, f"Unexpected error: {exc}"
