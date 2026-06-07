"""
Avelyn — Voice Commands Engine
===============================
Implements background audio capture, wake-word detection using openWakeWord (ONNX),
and command transcription using faster-whisper. Runs off the main GUI thread.
"""

import queue
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from logger import logger

class VoiceEngine(QThread):
    """
    Runs a background thread to continuously capture microphone data, run
    wake-word inference, and transcribe spoken commands.
    """
    wake_word_detected = pyqtSignal()
    status_changed = pyqtSignal(str)          # "Ready", "Listening", "Processing", "Inactive"
    transcription_completed = pyqtSignal(str) # Emits the transcribed text
    error_occurred = pyqtSignal(str)          # Emits human-readable errors

    def __init__(self, device_name: str = "", enable_wakeword: bool = False) -> None:
        super().__init__()
        self.device_name = device_name
        self.enable_wakeword = enable_wakeword
        self.running = False
        self.audio_queue = queue.Queue()
        self.is_ptt_active = False # Push-To-Talk trigger flag
        self.status_text = "Inactive"
        self._busy = False

    def set_busy(self, busy: bool) -> None:
        """Sets whether the engine should ignore wake-word detection."""
        self._busy = busy

    def stop(self) -> None:
        """Safely terminate the engine thread."""
        self.running = False
        self.wait()

    def trigger_ptt(self) -> None:
        """Programmatically trigger Push-To-Talk command recording."""
        self.is_ptt_active = True

    def set_status(self, status: str) -> None:
        """Update status_text and emit signal."""
        self.status_text = status
        self.status_changed.emit(status)

    def run(self) -> None:
        self.running = True
        self.set_status("Inactive")

        # Lazy load libraries to preserve 0MB RAM idle overhead when disabled
        try:
            import sounddevice as sd
            from openwakeword.model import Model
            from faster_whisper import WhisperModel
        except ImportError as e:
            err_msg = f"Missing dependency: {e.name}. Please install required packages."
            logger.error("VoiceEngine error: %s", err_msg)
            self.error_occurred.emit(err_msg)
            self.set_status("Inactive")
            return

        # 1. Initialize openWakeWord Model
        try:
            import os
            base_dir = os.path.dirname(os.path.abspath(__file__))
            custom_model = os.path.join(base_dir, "assets", "models", "hey_avelyn.onnx")

            if os.path.exists(custom_model):
                oww_model = Model(wakeword_models=[custom_model], inference_framework="onnx")
                logger.info("Loaded custom wake-word model: hey_avelyn.onnx")
            else:
                oww_model = Model(inference_framework="onnx")
                logger.info("VOICE_ENGINE_STARTED: Loaded default openwakeword models (hey_jarvis, alexa, etc.)")
        except Exception as e:
            logger.error("Failed to load openWakeWord model: %s", e)
            self.error_occurred.emit("Failed to load wake word engine.")
            self.set_status("Inactive")
            return

        # 2. Initialize Whisper Model (CPU execution, INT8 quantization for maximum speed)
        try:
            whisper_model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
            logger.info("VOICE_ENGINE_STARTED: Loaded faster-whisper tiny.en model")
        except Exception as e:
            logger.error("Failed to load faster-whisper model: %s", e)
            self.error_occurred.emit("Failed to load speech transcription engine.")
            self.set_status("Inactive")
            return

        # Audio stream callback
        def callback(indata, frames, time, status):
            if status:
                logger.warning("Audio input warning: %s", status)
            self.audio_queue.put(indata.copy())

        # Determine configured device index
        device_index = None
        if self.device_name:
            try:
                devices = sd.query_devices()
                for idx, dev in enumerate(devices):
                    if dev['name'] == self.device_name and dev['max_input_channels'] > 0:
                        device_index = idx
                        break
            except Exception as e:
                logger.error("Error querying audio devices: %s", e)

        # Config parameters: 16kHz mono, blocksize 1280 samples (80ms chunks)
        samplerate = 16000
        blocksize = 1280

        try:
            logger.info("MICROPHONE_STREAM_OPENING: device=%r samplerate=%d", device_index, samplerate)
            stream = sd.InputStream(
                device=device_index,
                channels=1,
                samplerate=samplerate,
                blocksize=blocksize,
                dtype='int16',
                callback=callback
            )
            logger.info("MICROPHONE_STREAM_OPENED")
        except Exception as e:
            logger.exception("MICROPHONE_STREAM_FAILED: %s", e)
            self.error_occurred.emit("Failed to open microphone. Check connections and permissions.")
            self.set_status("Inactive")
            return

        self.set_status("Ready")
        logger.info("VOICE_ENGINE_STARTED")

        # Drain any residual samples from queue
        while not self.audio_queue.empty():
            self.audio_queue.get()

        # State machine variables
        recording = False
        command_buffer = []
        silence_counter = 0
        speech_detected = False
        
        # Performance parameters:
        max_recording_chunks = 75   # ~6 seconds max recording limit
        silence_limit_chunks = 18    # ~1.5 seconds silence limit
        silence_threshold = 250      # RMS energy threshold for silence VAD

        with stream:
            while self.running:
                try:
                    data = self.audio_queue.get(timeout=0.1)
                except queue.Empty:
                    continue

                audio_chunk = data.reshape(-1)
                
                # VAD: Calculate Root Mean Square (RMS) energy of the chunk
                rms = np.sqrt(np.mean(audio_chunk.astype(np.float64)**2))

                # Check manual Push-to-Talk or Wake Word triggers
                trigger_woke = False
                if self.is_ptt_active:
                    self.is_ptt_active = False
                    trigger_woke = True
                    logger.info("Push-To-Talk active. Starting command recording.")

                if not recording:
                    # Run wake word detection in always-listening mode
                    if self.enable_wakeword and not self._busy:
                        prediction = oww_model.predict(audio_chunk)
                        for mdl, score in prediction.items():
                            if score > 0.5:
                                logger.info("WAKE_WORD_DETECTED: %s with score %.2f", mdl, score)
                                trigger_woke = True
                                break

                    if trigger_woke:
                        recording = True
                        command_buffer = []
                        silence_counter = 0
                        speech_detected = False
                        self.wake_word_detected.emit()
                        self.set_status("Listening")
                        logger.info("VOICE_LISTEN_START")
                else:
                    # Accumulating voice command
                    command_buffer.append(audio_chunk)

                    if rms > silence_threshold:
                        speech_detected = True
                        silence_counter = 0
                    else:
                        silence_counter += 1

                    # Stop conditions:
                    # 1. Silence detected after speech started
                    # 2. Maximum timeout without any speech detected (~3 seconds / 38 chunks)
                    # 3. Maximum total recording duration reached (~6 seconds / 75 chunks)
                    stop_recording = False
                    if speech_detected and silence_counter >= silence_limit_chunks:
                        logger.info("VAD: Silence detected. Stopping recording.")
                        stop_recording = True
                    elif not speech_detected and silence_counter >= 38:
                        logger.info("VAD: Speech timeout. Stopping recording.")
                        stop_recording = True
                    elif len(command_buffer) >= max_recording_chunks:
                        logger.info("VAD: Max recording length reached. Stopping recording.")
                        stop_recording = True

                    if stop_recording:
                        recording = False
                        self.set_status("Processing")
                        logger.info("VOICE_LISTEN_STOP")

                        # Transcribe command
                        if len(command_buffer) > 5 and speech_detected:
                            full_audio = np.concatenate(command_buffer)
                            # Convert to normalized float32 for Whisper
                            audio_f32 = full_audio.astype(np.float32) / 32768.0

                            try:
                                logger.info("Transcribing audio buffer size: %d samples...", len(audio_f32))
                                segments, info = whisper_model.transcribe(audio_f32, beam_size=5)
                                transcript = " ".join([seg.text for seg in segments]).strip()
                                logger.info("VOICE_TRANSCRIPT: %r", transcript)
                                self.transcription_completed.emit(transcript)
                            except Exception as e:
                                logger.error("Whisper transcription failed: %s", e)
                                self.error_occurred.emit("Transcription failed.")
                                self.transcription_completed.emit("")
                        else:
                            logger.info("VAD: Audio capture was too short or silent.")
                            self.transcription_completed.emit("")

                        self.set_status("Ready")

        self.set_status("Inactive")
        logger.info("VOICE_ENGINE_STOPPED")
