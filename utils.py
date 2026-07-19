import os
import sys
import time
import threading
from pathlib import Path

def get_resource_path(relative_path: str) -> Path:
    """
    Get the absolute path to a resource, works for dev and for PyInstaller.
    PyInstaller creates a temp folder and stores path in _MEIPASS.
    """
    try:
        base_path = Path(sys._MEIPASS)
    except Exception:
        base_path = Path(__file__).parent
        
    return base_path / relative_path


class PerfTracker:
    # Core pipeline stages
    pipeline_start = 0.0
    pipeline_end = 0.0
    
    # Hotkey & clipboard
    hotkey_detect_start = 0.0
    hotkey_detect_end = 0.0
    clipboard_save_start = 0.0
    clipboard_save_end = 0.0
    capture_start = 0.0
    capture_end = 0.0
    clip_read_start = 0.0
    clip_read_end = 0.0
    active_app_detect_start = 0.0
    active_app_detect_end = 0.0
    focus_restore_start = 0.0
    focus_restore_end = 0.0
    
    # Prompt building
    prompt_build_start = 0.0
    prompt_build_end = 0.0
    prompt_template_load_start = 0.0
    prompt_template_load_end = 0.0
    config_load_start = 0.0
    config_load_end = 0.0
    
    # Provider & routing
    provider_select_start = 0.0
    provider_select_end = 0.0
    router_start = 0.0
    router_end = 0.0
    smart_fallback_init_start = 0.0
    smart_fallback_init_end = 0.0
    provider_creation_start = 0.0
    provider_creation_end = 0.0
    
    # HTTP & streaming
    http_setup_start = 0.0
    http_setup_end = 0.0
    ollama_start = 0.0
    first_token = 0.0
    generation_end = 0.0
    response_clean_start = 0.0
    response_clean_end = 0.0
    
    # Clipboard replacement
    clipboard_replace_start = 0.0
    clipboard_replace_end = 0.0
    paste_start = 0.0
    paste_end = 0.0
    
    @classmethod
    def reset(cls):
        now = time.perf_counter()
        cls.pipeline_start = now
        cls.pipeline_end = 0.0
        cls.hotkey_detect_start = now
        cls.hotkey_detect_end = 0.0
        cls.clipboard_save_start = 0.0
        cls.clipboard_save_end = 0.0
        cls.capture_start = 0.0
        cls.capture_end = 0.0
        cls.clip_read_start = 0.0
        cls.clip_read_end = 0.0
        cls.active_app_detect_start = 0.0
        cls.active_app_detect_end = 0.0
        cls.focus_restore_start = 0.0
        cls.focus_restore_end = 0.0
        cls.prompt_build_start = 0.0
        cls.prompt_build_end = 0.0
        cls.prompt_template_load_start = 0.0
        cls.prompt_template_load_end = 0.0
        cls.config_load_start = 0.0
        cls.config_load_end = 0.0
        cls.provider_select_start = 0.0
        cls.provider_select_end = 0.0
        cls.router_start = 0.0
        cls.router_end = 0.0
        cls.smart_fallback_init_start = 0.0
        cls.smart_fallback_init_end = 0.0
        cls.provider_creation_start = 0.0
        cls.provider_creation_end = 0.0
        cls.http_setup_start = 0.0
        cls.http_setup_end = 0.0
        cls.ollama_start = 0.0
        cls.first_token = 0.0
        cls.generation_end = 0.0
        cls.response_clean_start = 0.0
        cls.response_clean_end = 0.0
        cls.clipboard_replace_start = 0.0
        cls.clipboard_replace_end = 0.0
        cls.paste_start = 0.0
        cls.paste_end = 0.0

    @classmethod
    def log_summary(cls):
        from logger import logger
        
        def ms(start, end):
            if start and end:
                return (end - start) * 1000
            return 0.0

        logger.info("========== Performance ==========")
        logger.info(f"Hotkey Detection:      {ms(cls.hotkey_detect_start, cls.hotkey_detect_end):.1f} ms")
        logger.info(f"Clipboard Save:        {ms(cls.clipboard_save_start, cls.clipboard_save_end):.1f} ms")
        logger.info(f"Clipboard Capture:     {ms(cls.capture_start, cls.capture_end):.1f} ms")
        logger.info(f"Clipboard Read:        {ms(cls.clip_read_start, cls.clip_read_end):.1f} ms")
        logger.info(f"Active App Detection:  {ms(cls.active_app_detect_start, cls.active_app_detect_end):.1f} ms")
        logger.info(f"Focus Restoration:     {ms(cls.focus_restore_start, cls.focus_restore_end):.1f} ms")
        logger.info(f"Prompt Template Load:  {ms(cls.prompt_template_load_start, cls.prompt_template_load_end):.1f} ms")
        logger.info(f"Prompt Build:          {ms(cls.prompt_build_start, cls.prompt_build_end):.1f} ms")
        logger.info(f"Config Load:           {ms(cls.config_load_start, cls.config_load_end):.1f} ms")
        logger.info(f"Provider Selection:    {ms(cls.provider_select_start, cls.provider_select_end):.1f} ms")
        logger.info(f"Router:                {ms(cls.router_start, cls.router_end):.1f} ms")
        logger.info(f"Smart Fallback Init:   {ms(cls.smart_fallback_init_start, cls.smart_fallback_init_end):.1f} ms")
        logger.info(f"Provider Creation:     {ms(cls.provider_creation_start, cls.provider_creation_end):.1f} ms")
        logger.info(f"HTTP Setup:            {ms(cls.http_setup_start, cls.http_setup_end):.1f} ms")
        logger.info(f"Time to First Token:   {ms(cls.ollama_start, cls.first_token):.1f} ms")
        logger.info(f"Streaming Duration:    {ms(cls.first_token, cls.generation_end):.1f} ms")
        logger.info(f"Response Clean:        {ms(cls.response_clean_start, cls.response_clean_end):.1f} ms")
        logger.info(f"Clipboard Replace:     {ms(cls.clipboard_replace_start, cls.clipboard_replace_end):.1f} ms")
        logger.info(f"Paste:                 {ms(cls.paste_start, cls.paste_end):.1f} ms")
        logger.info(f"Total Pipeline:        {ms(cls.pipeline_start, cls.pipeline_end):.1f} ms")
        logger.info("=================================")