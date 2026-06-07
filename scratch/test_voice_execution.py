"""
Avelyn — End-to-End Voice Pipeline Verification Script
======================================================
Patches sounddevice to feed audio files into the VoiceEngine callback.
Runs the real wake-word, Whisper, and AI pipeline to prove the end-to-end
processing works successfully and verify custom wake-word discrimination.
"""

import sys
import os
import time
import numpy as np
import wave
from PyQt6.QtCore import QCoreApplication, QTimer, QObject
from PyQt6.QtWidgets import QApplication

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up mock UI classes BEFORE importing main or voice components
import PyQt6.QtWidgets
import PyQt6.QtGui

from PyQt6.QtCore import pyqtSignal

class MockWidget(PyQt6.QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
    def show(self): pass
    def hide(self): pass
    def close(self): pass
    def show_palette(self, *args, **kwargs): pass
    def setGraphicsEffect(self, *args, **kwargs): pass
    def show_message(self, *args, **kwargs): pass
    def update_status(self, *args, **kwargs): pass
    def setOpacity(self, *args, **kwargs): pass

class MockPalette(PyQt6.QtWidgets.QWidget):
    action_selected = pyqtSignal(str, str)
    cancelled = pyqtSignal()
    hidden = pyqtSignal()
    def __init__(self, *args, **kwargs):
        super().__init__()
    def show_palette(self, *args, **kwargs): pass
    def hide(self): pass

class MockTray(PyQt6.QtCore.QObject):
    open_settings_requested = pyqtSignal()
    quit_requested = pyqtSignal()
    pause_toggled = pyqtSignal(bool)
    def __init__(self, *args, **kwargs):
        super().__init__()
    def show(self): pass
    def hide(self): pass
    def notify(self, *args, **kwargs): pass

class MockOnboarding(PyQt6.QtWidgets.QWidget):
    setup_complete = pyqtSignal()
    def __init__(self, *args, **kwargs):
        super().__init__()
    def show(self): pass

class MockInstallerOverlay(PyQt6.QtWidgets.QWidget):
    retry_requested = pyqtSignal()
    def __init__(self, *args, **kwargs):
        super().__init__()
    def update_progress(self, *args, **kwargs): pass
    def show_error(self, *args, **kwargs): pass
    def show_success(self, *args, **kwargs): pass
    def hide(self): pass

# Patch ui module elements
import ui
real_ai_worker = ui.AIWorker
ui.EnhancementPopup = MockWidget
ui.SettingsWindow = MockWidget
ui.SystemTrayIcon = MockTray
ui.ToastOverlay = MockWidget
ui.CommandPalette = MockPalette
ui.InstallerOverlay = MockInstallerOverlay
ui.AIWorker = real_ai_worker

import onboarding
onboarding.OnboardingWindow = MockOnboarding
import permissions
class MockPermissionManager:
    @classmethod
    def check_accessibility(cls): return True
    @classmethod
    def check_input_monitoring(cls): return True
permissions.PermissionManager = MockPermissionManager

# Global variables for testing
MOCK_WAV_PATH = "test.wav"
WAKE_WORDS_DETECTED = []

class MockInputStream:
    def __init__(self, **kwargs):
        self.callback = kwargs.get('callback')
        self.blocksize = kwargs.get('blocksize', 1280)
        self.running = False
        
    def __enter__(self):
        self.running = True
        import threading
        
        def feed_audio():
            time.sleep(1.0) # wait for engine initialization
            logger.info("MOCK_MIC: Starting audio injection from %s...", MOCK_WAV_PATH)
            
            with wave.open(MOCK_WAV_PATH, "rb") as wf:
                while self.running:
                    frames = wf.readframes(self.blocksize)
                    if not frames:
                        logger.info("MOCK_MIC: Reached end of audio file. Injecting silence...")
                        # Feed 30 silent chunks (approx 2.4 seconds of silence) to trigger VAD
                        for _ in range(30):
                            if not self.running:
                                break
                            silent_data = np.zeros((self.blocksize, 1), dtype=np.int16)
                            self.callback(silent_data, self.blocksize, None, None)
                            time.sleep(0.08)
                        break
                    
                    data = np.frombuffer(frames, dtype=np.int16).reshape(-1, 1)
                    self.callback(data, self.blocksize, None, None)
                    time.sleep(0.08) # 80ms chunk interval
                    
        threading.Thread(target=feed_audio, daemon=True).start()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running = False

import sounddevice as sd
sd.InputStream = MockInputStream

import platform_handler as ph
ph.check_accessibility = lambda: True
ph.check_input_monitoring = lambda: True

from logger import logger, setup_logger
from main import AvelynApp
from settings import Settings

def main():
    setup_logger(debug=True)
    logger.info("=== Starting Voice Pipeline Real Execution Test ===")
    
    # Pre-configure settings
    settings = Settings()
    settings.set("first_run_completed", True)
    settings.set("voice_commands_enabled", True)
    settings.set("wake_word_enabled", True)
    settings.set("ollama_host", "http://localhost:11434")
    settings.set("ollama_model", "gemma3:4b")
    
    global MOCK_WAV_PATH, WAKE_WORDS_DETECTED
    
    qapp = QApplication(sys.argv)
    
    import argparse
    args = argparse.Namespace(debug=True, test_clipboard=False, test_ai=False)
    app = AvelynApp(args)
    app._capture_text_synchronously = lambda: "write a python function to add two numbers"
    app._hotkeys.start = lambda: None
    app._tray.show = lambda: None
    app._tray.notify = lambda: None

    # Track wake word detections
    def on_wake():
        name = "hey_avelyn" if "test.wav" in MOCK_WAV_PATH else "hey_jarvis"
        WAKE_WORDS_DETECTED.append(name)
        logger.info("WAKE_WORD_SIGNAL_EMITTED: %s", name)

    app._voice_handler.engine.wake_word_detected.connect(on_wake)

    # We mock paste_text to verify completion
    def mock_paste():
        logger.info("PASTE_SUCCESS=True")
        logger.info("=== TEST SUCCESS: Full pipeline completed! ===")
        logger.info("Wake words detected during run: %r", WAKE_WORDS_DETECTED)
        
        # Verify custom wake word triggered and old one didn't
        if "hey_jarvis" in WAKE_WORDS_DETECTED:
            logger.error("TEST FAILED: 'Hey Jarvis' woke up the system!")
            app._voice_handler.engine.stop()
            qapp.exit(1)
        elif "hey_avelyn" not in WAKE_WORDS_DETECTED:
            logger.error("TEST FAILED: 'Hey Avelyn' did not wake up the system!")
            app._voice_handler.engine.stop()
            qapp.exit(1)
        else:
            # Let the QTimer in main.py fire the complete/success/busy-clear signals first
            QTimer.singleShot(600, lambda: [
                logger.info("ALL WAKE-WORD LOGIC VERIFIED SUCCESSFULLY!"),
                app._voice_handler.engine.stop(),
                qapp.exit(0)
            ])

    ph.paste_text = mock_paste

    # Control the sequence
    def start_phase_1():
        global MOCK_WAV_PATH
        logger.info("\n--- PHASE 1: Testing Negative Wake-Word ('Hey Jarvis') ---")
        MOCK_WAV_PATH = "test_jarvis.wav"
        # The engine is already started, so it is reading test_jarvis.wav.
        # Wait 6 seconds, then stop Phase 1 and switch to Phase 2.
        QTimer.singleShot(6000, start_phase_2)

    def start_phase_2():
        global MOCK_WAV_PATH
        logger.info("Stopping Phase 1 engine...")
        app._voice_handler.engine.stop()
        
        logger.info("\n--- PHASE 2: Testing Positive Wake-Word ('Hey Avelyn') ---")
        MOCK_WAV_PATH = "test.wav"
        
        # Restart the engine with the new wav path
        logger.info("Starting Phase 2 engine...")
        app._voice_handler.engine.start()

    # Safety timeout
    timeout_timer = QTimer()
    timeout_timer.setInterval(45000)
    timeout_timer.timeout.connect(lambda: (
        logger.error("TEST FAILED: Timeout reached!"),
        app._voice_handler.engine.stop(),
        qapp.exit(1)
    ))
    timeout_timer.start()

    # Start the test sequence when app starts
    QTimer.singleShot(100, start_phase_1)

    sys.exit(app.run())

if __name__ == "__main__":
    main()
