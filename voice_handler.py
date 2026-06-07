"""
Avelyn — Voice Commands Handler
===============================
Orchestrates the background VoiceEngine lifecycle, maps transcribed spoken
phrases to Avelyn actions (with local AI fallback), and manages the floating glassmorphic overlay.
"""

import sys
import requests
from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal, Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QApplication, QFrame, QGraphicsDropShadowEffect

from logger import logger
from settings import Settings

# ── Intent Mapping ───────────────────────────────────────────────────────────
VOICE_INTENT_MAP = {
    # Quick Actions
    "smart assist": "smart",
    "smart": "smart",
    "improve writing": "professional",
    "professional": "professional",
    "improve prompt": "improve_prompt",
    "improve": "improve_prompt",
    "fix grammar": "grammar",
    "grammar": "grammar",
    
    # More Actions
    "explain like i'm five": "eli5",
    "explain like i'm 5": "eli5",
    "explain": "eli5",
    "translate": "translate",
    "summarize": "summarize",
    "professional email": "email",
    "email": "email",
    "linkedin post": "linkedin",
    "linkedin": "linkedin",
    "meeting notes": "meeting_notes",
    "make shorter": "shorten",
    "shorten": "shorten",
    "format resume": "resume",
    "resume": "resume",
    "explain code": "explain_code",
    "debug code": "debug_code",
    
    # Code Generation mappings
    "generate code": "generate_code:python:adaptive",
    "code": "generate_code:python:adaptive",
    "python code": "generate_code:python:adaptive",
    "javascript code": "generate_code:javascript:adaptive",
    "java code": "generate_code:java:adaptive",
    "c plus plus code": "generate_code:cplusplus:adaptive",
    "c code": "generate_code:c:adaptive",
    "c sharp code": "generate_code:csharp:adaptive",
    "go code": "generate_code:go:adaptive",
    "rust code": "generate_code:rust:adaptive",
    "php code": "generate_code:php:adaptive",
    "kotlin code": "generate_code:kotlin:adaptive",
    "swift code": "generate_code:swift:adaptive",
    "dart code": "generate_code:dart:adaptive",
    "typescript code": "generate_code:typescript:adaptive",
}


def classify_intent_via_ai(settings: Settings, text: str) -> Optional[str]:
    """Uses the local Ollama instance to classify the voice command when deterministic match fails."""
    host = settings.get("ollama_host", "http://localhost:11434").rstrip('/')
    model = settings.get("ollama_model", "gemma3:4b")
    
    prompt = f"""You are an intent classifier for Avelyn writing and coding assistant.
Classify the following user voice command into exactly one of these action modes:
- 'grammar'
- 'smart'
- 'professional'
- 'improve_prompt'
- 'eli5'
- 'translate'
- 'summarize'
- 'email'
- 'linkedin'
- 'meeting_notes'
- 'shorten'
- 'resume'
- 'explain_code'
- 'debug_code'
- 'generate_code'

Return ONLY the single word mode name from the list above. If you cannot classify it, return 'unknown'. Do not output markdown, reasoning, explanations, or punctuation.

Voice command: "{text}"
Mode:"""

    try:
        url = f"{url}" if (url := f"{host}/api/generate") else ""
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.0,
                "num_predict": 10
            }
        }
        res = requests.post(url, json=payload, timeout=4.0)
        if res.status_code == 200:
            resp_data = res.json()
            mode = resp_data.get("response", "").strip().lower()
            logger.info("AI intent classification output: %r", mode)
            
            # Clean possible markdown formatting
            mode = mode.replace("'", "").replace('"', "").replace("`", "").strip()
            
            valid_modes = {
                "grammar", "smart", "professional", "improve_prompt", "eli5",
                "translate", "summarize", "email", "linkedin", "meeting_notes",
                "shorten", "resume", "explain_code", "debug_code", "generate_code"
            }
            if mode in valid_modes:
                return mode
    except Exception as exc:
        logger.error("AI intent classification failed: %s", exc)
        
    return None


class VoiceOverlay(QWidget):
    """A premium, glassmorphic floating pill indicating Voice Command capture."""
    
    def __init__(self, parent: Optional[QWidget] = None, theme: str = "dark") -> None:
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.ToolTip |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowTransparentForInput |
            Qt.WindowType.BypassWindowManagerHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self._pill = QFrame()
        self._pill.setObjectName("VoicePill")
        
        # Purple glassmorphic tailored styling
        if theme == "dark":
            self._pill.setStyleSheet("""
                QFrame#VoicePill {
                    background-color: rgba(30, 27, 75, 0.85);
                    border: 1px solid rgba(167, 139, 250, 0.45);
                    border-radius: 18px;
                }
            """)
        else:
            self._pill.setStyleSheet("""
                QFrame#VoicePill {
                    background-color: rgba(243, 244, 246, 0.9);
                    border: 1px solid rgba(124, 58, 237, 0.45);
                    border-radius: 18px;
                }
            """)
            
        self._pill_layout = QHBoxLayout(self._pill)
        self._pill_layout.setContentsMargins(16, 8, 16, 8)
        self._pill_layout.setSpacing(10)
        
        self._mic_lbl = QLabel("🎤")
        self._mic_lbl.setStyleSheet("font-size: 16px; background: transparent;")
        
        self._lbl = QLabel("Listening for command...")
        if theme == "dark":
            self._lbl.setStyleSheet("background: transparent; color: #FFFFFF; font-weight: 600; font-size: 14px;")
        else:
            self._lbl.setStyleSheet("background: transparent; color: #1F2937; font-weight: 600; font-size: 14px;")
            
        self._pill_layout.addWidget(self._mic_lbl)
        self._pill_layout.addWidget(self._lbl)
        
        # Soft Drop Shadow
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(15)
        self._shadow.setXOffset(0)
        self._shadow.setYOffset(3)
        self._shadow.setColor(QColor(0, 0, 0, 70))
        self._pill.setGraphicsEffect(self._shadow)
        
        layout.addWidget(self._pill)
        
        # Opacity Animations
        self._anim_in = QPropertyAnimation(self, b"windowOpacity")
        self._anim_in.setDuration(200)
        self._anim_in.setStartValue(0.0)
        self._anim_in.setEndValue(1.0)
        self._anim_in.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self._anim_out = QPropertyAnimation(self, b"windowOpacity")
        self._anim_out.setDuration(200)
        self._anim_out.setStartValue(1.0)
        self._anim_out.setEndValue(0.0)
        self._anim_out.setEasingCurve(QEasingCurve.Type.InCubic)
        self._anim_out.finished.connect(self.hide)
        
    def show_listening(self) -> None:
        self._lbl.setText("Listening...")
        self._mic_lbl.setText("🎤")
        self.setWindowOpacity(0.0)
        self.show()
        self._position_center()
        self._anim_in.start()

    def show_processing(self) -> None:
        self._lbl.setText("Processing Voice Command...")
        self._mic_lbl.setText("◴")
        self._position_center()

    def show_executing(self) -> None:
        self._lbl.setText("Executing...")
        self._mic_lbl.setText("✦")
        self._position_center()
        
    def show_recognized(self, text: str) -> None:
        self._lbl.setText(f"Recognized: {text}")
        self._mic_lbl.setText("✓")
        self._position_center()
        
    def hide_overlay(self) -> None:
        self._anim_out.start()
        
    def _position_center(self) -> None:
        app = QApplication.instance()
        if app:
            screen = app.primaryScreen().geometry()
            self.adjustSize()
            self.move(
                screen.x() + (screen.width() - self.width()) // 2,
                screen.y() + 80,  # Near screen top center
            )


class VoiceHandler(QObject):
    """Manages VoiceEngine background thread and coordinates action routing."""
    
    action_selected = pyqtSignal(str)              # Emits mode_id to run
    open_palette_requested = pyqtSignal(str)       # Prefills command palette
    notification_requested = pyqtSignal(str, str) # Emits (title, message)
    ai_classification_completed = pyqtSignal(str, str) # Emits (original_text, mode_id)
    
    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.settings = settings
        self.engine = None
        self.overlay = None
        self._last_status = "Inactive"
        self._voice_busy = False
        logger.info("VOICE_HANDLER_CREATED")
        self.ai_classification_completed.connect(self._handle_classified_mode)
        self.sync_with_settings()

    def set_busy(self, busy: bool) -> None:
        """Sets the busy status of the voice command pipeline."""
        self._voice_busy = busy
        if busy:
            logger.info("VOICE_BUSY_SET")
        else:
            logger.info("VOICE_BUSY_CLEARED")
        if self.engine:
            self.engine.set_busy(busy)
        
    def sync_with_settings(self) -> None:
        """Dynamically start, stop, or re-initialize VoiceEngine based on Settings configuration."""
        enabled = self.settings.voice_commands_enabled
        wake_word = self.settings.wake_word_enabled
        device = self.settings.microphone_device
        logger.info(
            "VOICE_SETTINGS enabled=%s wake_word=%s device=%r",
            enabled, wake_word, device or "default"
        )

        # Stop and join existing engine
        if self.engine:
            logger.info("VOICE_ENGINE_STOPPED")
            self.engine.stop()
            self.engine = None

        if not enabled:
            logger.warning("VOICE_ENGINE_NOT_STARTED: voice_commands_enabled=False")
            app = QApplication.instance()
            if app and hasattr(app, "voice_engine"):
                app.voice_engine = None
            return

        from voice_engine import VoiceEngine
        logger.info("VOICE_ENGINE_CREATED")
        self.engine = VoiceEngine(device_name=device, enable_wakeword=wake_word)
        self.engine.wake_word_detected.connect(self._on_wake_word_detected)
        self.engine.status_changed.connect(self._on_status_changed)
        self.engine.transcription_completed.connect(self._on_transcription_completed)
        self.engine.error_occurred.connect(self._on_error_occurred)

        # Put global reference on QApplication for UI queries
        app = QApplication.instance()
        if app:
            app.voice_engine = self.engine

        logger.info("VOICE_ENGINE_STARTING")
        self.engine.start()

    def trigger_ptt(self) -> None:
        """Trigger command capturing manually (Push-to-Talk)."""
        if getattr(self, "_voice_busy", False):
            logger.info("VOICE_WAKEWORD_IGNORED_BUSY")
            return
            
        if self.engine:
            self.set_busy(True)
            self.engine.trigger_ptt()
            self.show_overlay()
        else:
            self.notification_requested.emit("Voice Commands Inactive", "Enable Voice Commands in Settings first.")

    def show_overlay(self) -> None:
        """Shows floating overlay pill widget."""
        if not self.overlay:
            self.overlay = VoiceOverlay(theme=self.settings.theme)
        self.overlay.show_listening()

    def _on_wake_word_detected(self) -> None:
        if getattr(self, "_voice_busy", False):
            logger.info("VOICE_WAKEWORD_IGNORED_BUSY")
            return
            
        self.set_busy(True)
        logger.info("WAKE_WORD_DETECTED")
        self.show_overlay()

    def _on_status_changed(self, status: str) -> None:
        self._last_status = status
        if self.overlay:
            if status == "Listening":
                self.overlay.show_listening()
            elif status == "Processing":
                self.overlay.show_processing()

    def _on_error_occurred(self, err: str) -> None:
        logger.warning("Voice Engine error: %s", err)
        self.notification_requested.emit("Voice Engine Alert", err)
        if self.overlay:
            self.overlay.hide_overlay()

    def _on_transcription_completed(self, text: str) -> None:
        logger.info("VOICE_TRANSCRIPT: %r", text)
        if not text:
            # Cancel / Silence
            logger.warning("VOICE_COMMAND_FAILED: Empty transcription")
            self.set_busy(False)
            if self.overlay:
                self.overlay.hide_overlay()
            return
            
        # 1. Deterministic match check
        mode_id = self._match_deterministic(text)
        if mode_id:
            logger.info("VOICE_INTENT: %s (Deterministic)", mode_id)
            if self.overlay:
                self.overlay.show_recognized(text)
                QTimer.singleShot(800, self.overlay.hide_overlay)
            logger.info("VOICE_ACTION_DISPATCH: %s", mode_id)
            self.action_selected.emit(mode_id)
            logger.info("VOICE_COMMAND_DISPATCHED")
            return
            
        # 2. Local AI Intent Classifier Fallback
        logger.info("VOICE_INTENT: Deterministic matching failed. Running local AI classifier...")
        if self.overlay:
            self.overlay.show_processing()
            
        import threading
        def run_ai():
            mode = classify_intent_via_ai(self.settings, text)
            # Dispatch back onto Qt main GUI thread via signal
            self.ai_classification_completed.emit(text, mode or "unknown")
            
        threading.Thread(target=run_ai, daemon=True).start()

    def _handle_classified_mode(self, original_text: str, mode_id: Optional[str]) -> None:
        if self.overlay:
            self.overlay.hide_overlay()
            
        if mode_id and mode_id != "unknown":
            logger.info("VOICE_INTENT: %s (AI)", mode_id)
            logger.info("VOICE_ACTION_DISPATCH: %s", mode_id)
            self.action_selected.emit(mode_id)
            logger.info("VOICE_COMMAND_DISPATCHED")
        else:
            logger.warning("VOICE_COMMAND_FAILED: Unrecognized command")
            self.set_busy(False)
            self.notification_requested.emit("Voice command unrecognized", f"Could not match: '{original_text}'")
            # Prefill and open standard Command Palette
            self.open_palette_requested.emit(original_text)

    def _match_deterministic(self, text: str) -> Optional[str]:
        cleaned = text.lower().strip()
        for punc in [".", ",", "?", "!"]:
            cleaned = cleaned.replace(punc, "")
        cleaned = cleaned.strip()
        
        # Strip common wake prefixes
        for prefix in ["hey avelyn", "avelyn"]:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()
                if cleaned.startswith(",") or cleaned.startswith(":"):
                    cleaned = cleaned[1:].strip()
                    
        # 1. Exact match check
        if cleaned in VOICE_INTENT_MAP:
            return VOICE_INTENT_MAP[cleaned]
            
        # 2. Substring scan: match longer keys first to prioritize specific options
        sorted_keys = sorted(VOICE_INTENT_MAP.keys(), key=len, reverse=True)
        for key in sorted_keys:
            if key in cleaned:
                return VOICE_INTENT_MAP[key]
                
        return None
