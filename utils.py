import os
import sys
import time
from pathlib import Path

def get_resource_path(relative_path: str) -> Path:
    """
    Get the absolute path to a resource, works for dev and for PyInstaller.
    PyInstaller creates a temp folder and stores path in _MEIPASS.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS)
    except Exception:
        base_path = Path(__file__).parent
        
    return base_path / relative_path


class PerfTracker:
    pipeline_start = 0.0
    capture_start = 0.0
    capture_end = 0.0
    clip_read_start = 0.0
    clip_read_end = 0.0
    prompt_build_start = 0.0
    prompt_build_end = 0.0
    ollama_start = 0.0
    first_token = 0.0
    generation_end = 0.0
    clipboard_replace_start = 0.0
    clipboard_replace_end = 0.0
    pipeline_end = 0.0

    @classmethod
    def reset(cls):
        cls.pipeline_start = time.perf_counter()
        cls.capture_start = 0.0
        cls.capture_end = 0.0
        cls.clip_read_start = 0.0
        cls.clip_read_end = 0.0
        cls.prompt_build_start = 0.0
        cls.prompt_build_end = 0.0
        cls.ollama_start = 0.0
        cls.first_token = 0.0
        cls.generation_end = 0.0
        cls.clipboard_replace_start = 0.0
        cls.clipboard_replace_end = 0.0
        cls.pipeline_end = 0.0

    @classmethod
    def log_summary(cls):
        import time
        from logger import logger
        
        selection_capture = cls.capture_end - cls.capture_start if cls.capture_end and cls.capture_start else 0.0
        clip_read = cls.clip_read_end - cls.clip_read_start if cls.clip_read_end and cls.clip_read_start else 0.0
        prompt_build = cls.prompt_build_end - cls.prompt_build_start if cls.prompt_build_end and cls.prompt_build_start else 0.0
        first_token = cls.first_token - cls.ollama_start if cls.first_token and cls.ollama_start else 0.0
        generation_complete = cls.generation_end - cls.ollama_start if cls.generation_end and cls.ollama_start else 0.0
        clipboard_replace = cls.clipboard_replace_end - cls.clipboard_replace_start if cls.clipboard_replace_end and cls.clipboard_replace_start else 0.0
        total_pipeline = cls.pipeline_end - cls.pipeline_start if cls.pipeline_end and cls.pipeline_start else 0.0

        logger.info(f"PERF: Selection Capture = {selection_capture:.2f}s")
        logger.info(f"PERF: Clipboard Read = {clip_read:.2f}s")
        logger.info(f"PERF: Prompt Build = {prompt_build:.2f}s")
        logger.info("PERF: Ollama Request Start")
        logger.info(f"PERF: First Token = {first_token:.2f}s")
        logger.info(f"PERF: Generation Complete = {generation_complete:.2f}s")
        logger.info(f"PERF: Clipboard Replace = {clipboard_replace:.2f}s")
        logger.info(f"PERF: Total Pipeline = {total_pipeline:.2f}s")

