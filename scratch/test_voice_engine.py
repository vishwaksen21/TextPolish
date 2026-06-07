"""
Avelyn — Voice Engine Verification Tool
=========================================
A command-line script to test the VoiceEngine (openWakeWord and faster-whisper)
interactively without running the main PyQt GUI application.
"""

import sys
import os
import time
from PyQt6.QtCore import QCoreApplication

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from voice_engine import VoiceEngine
from settings import Settings
from logger import logger, setup_logger

def main():
    setup_logger(debug=True)
    logger.info("=== Starting Voice Engine Interactive Test ===")
    
    # Initialize a basic QCoreApplication event loop context
    app = QCoreApplication(sys.argv)
    
    settings = Settings()
    
    # Enable Voice Commands and Wake Word for this test execution
    settings.set("voice_commands_enabled", True)
    settings.set("wake_word_enabled", True)
    
    device = settings.microphone_device
    wake_word = settings.wake_word_enabled
    
    logger.info("Initializing VoiceEngine (Device: %r, Wake-word: %s)", device or "default", wake_word)
    engine = VoiceEngine(device_name=device, enable_wakeword=wake_word)
    
    # Connect signals
    engine.status_changed.connect(lambda status: logger.info("SIGNAL [status_changed]: %s", status))
    engine.wake_word_detected.connect(lambda: logger.info("SIGNAL [wake_word_detected]: WAKE WORD DETECTED!"))
    engine.transcription_completed.connect(lambda text: logger.info("SIGNAL [transcription_completed]: %r", text))
    engine.error_occurred.connect(lambda err: logger.error("SIGNAL [error_occurred]: %s", err))
    
    # Thread target to query user input for PTT simulation
    import threading
    def ptt_loop():
        time.sleep(2.0)
        logger.info("Engine is running.")
        logger.info("Mode 1: Speak the wake word (e.g. 'Hey Jarvis' or 'Alexa' default, or 'Hey Avelyn' if custom ONNX is in assets).")
        logger.info("Mode 2: Type 'p' and hit Enter to trigger manual Push-to-Talk (PTT).")
        logger.info("Type 'q' and hit Enter to quit.")
        
        while True:
            cmd = input().strip().lower()
            if cmd == 'q':
                logger.info("Stopping VoiceEngine...")
                engine.stop()
                QCoreApplication.quit()
                break
            elif cmd == 'p':
                logger.info("Simulating PTT keypress... Speak your command now!")
                engine.trigger_ptt()
            else:
                logger.info("Unknown input. Type 'p' to speak, or 'q' to quit.")
                
    threading.Thread(target=ptt_loop, daemon=True).start()
    
    # Start the thread
    engine.start()
    
    # Run loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
