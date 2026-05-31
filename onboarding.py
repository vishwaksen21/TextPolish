"""
TextPolish — First-Run Setup Wizard
===================================
A multi-step onboarding flow to ensure all permissions and dependencies
are resolved before the user attempts to use the application.

On macOS: shows Accessibility + Input Monitoring permission pages.
On Windows/Linux: skips those pages (no equivalent TCC system).
"""

import sys

from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject, QThread
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedWidget, QFrame, QProgressBar, QMessageBox, QApplication
)

from settings import Settings
from permissions import PermissionManager
from installer import Installer
from ai_processor import AIProcessor
import platform_handler as ph

IS_MACOS   = sys.platform == "darwin"
IS_WINDOWS = sys.platform == "win32"

class SetupWorker(QThread):
    progress = pyqtSignal(int, str)
    finished_ok = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, mode: str, model_name: str = ""):
        super().__init__()
        self.mode = mode # 'ollama' or 'model'
        self.model_name = model_name

    def run(self):
        try:
            if self.mode == 'ollama':
                if Installer.needs_installation():
                    Installer.download_and_extract_ollama(self._emit_progress)
                Installer.start_ollama()
                if not Installer.verify_installation(20):
                    raise RuntimeError("Ollama server failed to start.")
            elif self.mode == 'model':
                Installer.pull_model(self.model_name, self._emit_progress)
            self.finished_ok.emit()
        except Exception as e:
            self.error.emit(str(e))

    def _emit_progress(self, pct: int, msg: str):
        self.progress.emit(pct, msg)

class OnboardingWindow(QWidget):
    """
    Main setup wizard window containing a sequence of setup pages.
    Emits `setup_complete` when finished.
    """
    setup_complete = pyqtSignal()

    def __init__(self, settings: Settings, processor: AIProcessor):
        super().__init__()
        self._settings = settings
        self._processor = processor
        self.setWindowTitle("TextPolish Setup")
        self.setFixedSize(600, 450)
        
        # Center on screen
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: #1A1A24; color: #F0F0F8; font-family: -apple-system, system-ui;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QFrame()
        header.setStyleSheet("background: #13131A; border-bottom: 1px solid #2A2A38;")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(20, 15, 20, 15)
        
        title = QLabel("✦ TextPolish Setup")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #7C3AED; border: none;")
        h_layout.addWidget(title)
        
        self.step_label = QLabel("Step 1 of 1")
        self.step_label.setStyleSheet("font-size: 13px; color: #9090A8; border: none;")
        h_layout.addWidget(self.step_label, alignment=Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(header)

        # Stack
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Build pages — macOS permission pages are skipped on Windows/Linux
        self._build_welcome_page()
        if IS_MACOS:
            self._build_accessibility_page()
            self._build_input_monitoring_page()
        self._build_ollama_page()
        self._build_model_page()
        self._build_complete_page()

        # Update total step count after building pages
        self.step_label.setText(f"Step 1 of {self.stack.count()}")
        
        # Footer
        footer = QFrame()
        footer.setStyleSheet("background: #1A1A24; border-top: 1px solid #2A2A38;")
        f_layout = QHBoxLayout(footer)
        f_layout.setContentsMargins(20, 15, 20, 15)
        
        self.btn_back = QPushButton("Back")
        self.btn_back.setStyleSheet(self._btn_style(primary=False))
        self.btn_back.clicked.connect(self._prev_page)
        self.btn_back.hide()
        
        self.btn_retry = QPushButton("Retry")
        self.btn_retry.setStyleSheet(self._btn_style(primary=False))
        self.btn_retry.clicked.connect(self._retry_current_page)
        self.btn_retry.hide()
        
        f_layout.addWidget(self.btn_back)
        f_layout.addWidget(self.btn_retry)
        f_layout.addStretch()
        
        self.btn_next = QPushButton("Continue")
        self.btn_next.setStyleSheet(self._btn_style(primary=True))
        self.btn_next.setMinimumWidth(100)
        self.btn_next.clicked.connect(self._next_page)
        f_layout.addWidget(self.btn_next)
        
        main_layout.addWidget(footer)
        
        self.stack.currentChanged.connect(self._on_page_changed)
        
        # Polling timer for permissions
        self.poll_timer = QTimer(self)
        self.poll_timer.timeout.connect(self._poll_status)
        self.poll_timer.setInterval(1000)
        
        self.center_window()

    def center_window(self):
        screen = self.screen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )

    def _btn_style(self, primary: bool = False) -> str:
        if primary:
            return """
                QPushButton {
                    background: #7C3AED; color: white; border: none;
                    border-radius: 6px; padding: 8px 16px; font-weight: bold;
                }
                QPushButton:hover { background: #8B5CF6; }
                QPushButton:disabled { background: #4C3C73; color: #888; }
            """
        return """
            QPushButton {
                background: #2A2A38; color: white; border: 1px solid #3A3A4A;
                border-radius: 6px; padding: 8px 16px; font-weight: bold;
            }
            QPushButton:hover { background: #3A3A4A; }
        """

    def _create_page(self) -> QWidget:
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(40, 40, 40, 40)
        l.setAlignment(Qt.AlignmentFlag.AlignTop)
        return w

    def _add_title(self, layout: QVBoxLayout, text: str):
        lbl = QLabel(text)
        lbl.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(lbl)

    def _add_text(self, layout: QVBoxLayout, text: str):
        lbl = QLabel(text)
        lbl.setStyleSheet("font-size: 14px; color: #C0C0D0; line-height: 1.4;")
        lbl.setWordWrap(True)
        layout.addWidget(lbl)

    # ── Pages ─────────────────────────────────────────────────────────────────

    def _build_welcome_page(self):
        p = self._create_page()
        l = p.layout()
        l.addStretch()
        self._add_title(l, "Welcome to TextPolish")
        if IS_MACOS:
            body = (
                "TextPolish is a powerful AI assistant that lives in your menu bar.\n\n"
                "To magically read and replace text across all your apps, we need to set up "
                "a few macOS permissions and download the local AI model.\n\n"
                "This setup will only take a minute."
            )
        else:
            body = (
                "TextPolish is a powerful AI assistant that lives in your system tray.\n\n"
                "To read and replace text across all your apps, we need to download "
                "the local AI model. No special permissions are required on Windows.\n\n"
                "This setup will only take a minute."
            )
        self._add_text(l, body)
        l.addStretch()
        self.stack.addWidget(p)

    def _build_accessibility_page(self):
        p = self._create_page()
        l = p.layout()
        self._add_title(l, "Accessibility Permission")
        self._add_text(l, 
            "TextPolish needs Accessibility access to simulate the 'Copy' and 'Paste' "
            "keyboard shortcuts (Cmd+C / Cmd+V) when you trigger an enhancement.\n"
        )
        
        self.acc_status = QLabel("⚠ Waiting for permission...")
        self.acc_status.setStyleSheet("color: #FBBF24; font-weight: bold; font-size: 14px; margin-top: 15px;")
        l.addWidget(self.acc_status)
        
        btn = QPushButton("Open System Settings")
        btn.setStyleSheet(self._btn_style(False))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(PermissionManager.request_accessibility)
        
        row = QHBoxLayout()
        row.addWidget(btn)
        row.addStretch()
        l.addLayout(row)
        
        self.stack.addWidget(p)

    def _build_input_monitoring_page(self):
        p = self._create_page()
        l = p.layout()
        self._add_title(l, "Global Hotkeys")
        self._add_text(l, 
            "TextPolish needs to listen for your global shortcut (Ctrl+Shift+E) "
            "even when it's running in the background. "
            "macOS calls this 'Input Monitoring'."
        )
        self.input_status = QLabel("Checking...")
        self.input_status.setStyleSheet("color: #9090A8; font-weight: bold; font-size: 14px; margin-top: 15px;")
        l.addWidget(self.input_status)

        self.btn_open_input = QPushButton("Open System Settings")
        self.btn_open_input.setStyleSheet(self._btn_style(False))
        self.btn_open_input.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_open_input.clicked.connect(PermissionManager.request_input_monitoring)
        self.btn_open_input.hide()
        
        row = QHBoxLayout()
        row.addWidget(self.btn_open_input)
        row.addStretch()
        l.addLayout(row)

        self.stack.addWidget(p)

    def _build_ollama_page(self):
        p = self._create_page()
        l = p.layout()
        self._add_title(l, "Local AI Engine")
        self._add_text(l,
            "TextPolish runs entirely on your computer using Ollama. "
            "This keeps your data 100% private and offline."
        )

        self.ol_status = QLabel("Checking installation...")
        self.ol_status.setStyleSheet("color: #9090A8; font-weight: bold; font-size: 14px; margin-top: 10px;")
        l.addWidget(self.ol_status)

        self.ol_progress = QProgressBar()
        self.ol_progress.setTextVisible(False)
        self.ol_progress.setFixedHeight(6)
        self.ol_progress.hide()
        l.addWidget(self.ol_progress)

        self.stack.addWidget(p)

    def _build_model_page(self):
        p = self._create_page()
        l = p.layout()
        self._add_title(l, f"Downloading Model ({self._settings.ollama_model})")
        self._add_text(l, 
            "We need to download the AI model. This is a one-time ~2.5GB download. "
            "Please keep this window open."
        )
        
        self.mod_status = QLabel("Checking model...")
        self.mod_status.setStyleSheet("color: #9090A8; font-weight: bold; font-size: 14px; margin-top: 10px;")
        l.addWidget(self.mod_status)
        
        self.mod_progress = QProgressBar()
        self.mod_progress.setTextVisible(False)
        self.mod_progress.setFixedHeight(6)
        self.mod_progress.hide()
        l.addWidget(self.mod_progress)
        
        self.stack.addWidget(p)

    def _build_complete_page(self):
        p = self._create_page()
        l = p.layout()
        l.addStretch()
        self._add_title(l, "✓ You're all set!")
        self._add_text(l, 
            f"TextPolish is running in your menu bar.\n\n"
            f"Select any text in any app, and press {self._settings.shortcut_display} "
            f"to bring up the Command Palette."
        )
        l.addStretch()
        self.stack.addWidget(p)

    # ── Logic ─────────────────────────────────────────────────────────────────

    def _on_page_changed(self, idx: int):
        self.step_label.setText(f"Step {idx + 1} of {self.stack.count()}")
        self.btn_back.setVisible(idx > 0 and idx < self.stack.count() - 1)
        self.btn_next.setText("Finish" if idx == self.stack.count() - 1 else "Continue")
        self.btn_retry.hide()

        self.poll_timer.stop()
        self.btn_next.setEnabled(True)

        if IS_MACOS:
            # macOS page order: 0=Welcome, 1=Accessibility, 2=InputMonitoring, 3=Ollama, 4=Model, 5=Complete
            if idx == 1:   # Accessibility
                self.poll_timer.start()
                self._poll_status()
            elif idx == 2: # Input Monitoring
                self.poll_timer.start()
                self._poll_status()
            elif idx == 3: # Ollama
                self._check_ollama()
            elif idx == 4: # Model
                self._check_model()
        else:
            # Windows/Linux page order: 0=Welcome, 1=Ollama, 2=Model, 3=Complete
            if idx == 1:   # Ollama
                self._check_ollama()
            elif idx == 2: # Model
                self._check_model()

    def _poll_status(self):
        """Only called on macOS (pages 1 and 2 only exist there)."""
        idx = self.stack.currentIndex()
        if idx == 1:  # Accessibility (macOS only)
            if PermissionManager.check_accessibility():
                self.acc_status.setText("✓ Granted")
                self.acc_status.setStyleSheet("color: #10B981; font-weight: bold; font-size: 14px; margin-top: 15px;")
                self.btn_next.setEnabled(True)
            else:
                self.acc_status.setText("⚠ Waiting for permission...")
                self.acc_status.setStyleSheet("color: #FBBF24; font-weight: bold; font-size: 14px; margin-top: 15px;")
                self.btn_next.setEnabled(False)
        elif idx == 2:  # Input Monitoring (macOS only)
            if PermissionManager.check_input_monitoring():
                self.input_status.setText("✓ Ready")
                self.input_status.setStyleSheet("color: #10B981; font-weight: bold; font-size: 14px; margin-top: 15px;")
                self.btn_open_input.hide()
                self.btn_next.setEnabled(True)
            else:
                self.input_status.setText("⚠ Waiting for permission...")
                self.input_status.setStyleSheet("color: #FBBF24; font-weight: bold; font-size: 14px; margin-top: 15px;")
                self.btn_open_input.show()
                self.btn_next.setEnabled(False)

    def _retry_current_page(self):
        idx = self.stack.currentIndex()
        if idx == 3:
            self._check_ollama()
        elif idx == 4:
            self._check_model()

    # (Removed _check_input_monitoring as it is now handled by _poll_status)

    def _check_ollama(self):
        self.btn_next.setEnabled(False)
        self.btn_back.setEnabled(False)
        self.btn_retry.hide()
        
        self.ol_status.setText("Checking installation...")
        self.ol_status.setStyleSheet("color: #FBBF24; font-weight: bold; font-size: 14px; margin-top: 10px;")
        self.ol_progress.show()
        self.ol_progress.setValue(0)
        
        self._worker = SetupWorker('ollama')
        self._worker.progress.connect(self._on_ol_progress)
        self._worker.finished_ok.connect(self._on_ol_done)
        self._worker.error.connect(self._on_ol_err)
        self._worker.start()

    def _on_ol_progress(self, pct: int, msg: str):
        self.ol_progress.setValue(pct)
        self.ol_status.setText(msg)

    def _on_ol_done(self):
        self.ol_status.setText("✓ Ollama running locally")
        self.ol_status.setStyleSheet("color: #10B981; font-weight: bold; font-size: 14px; margin-top: 10px;")
        self.ol_progress.hide()
        self.btn_next.setEnabled(True)

    def _on_ol_err(self, err: str):
        err_lower = err.lower()
        if "network error" in err_lower or "name or service not known" in err_lower or "timed out" in err_lower:
            friendly_err = "No internet connection detected. Please check your Wi-Fi and try again."
        elif "corrupt" in err_lower:
            friendly_err = "The downloaded file was corrupted. Please retry the download."
        elif "failed to start" in err_lower:
            friendly_err = "Ollama installed but failed to start. Please restart your Mac and try again."
        else:
            friendly_err = f"An unexpected error occurred: {err}"
            
        self.ol_status.setText(f"⚠ {friendly_err}")
        self.ol_status.setStyleSheet("color: #EF4444; font-weight: bold; font-size: 13px; margin-top: 10px;")
        self.btn_next.setEnabled(False)
        self.btn_back.setEnabled(True)
        self.btn_retry.show()

    def _check_model(self):
        self.btn_next.setEnabled(False)
        self.btn_back.setEnabled(False)
        self.btn_retry.hide()
        
        self.mod_status.setText("Checking model...")
        self.mod_status.setStyleSheet("color: #FBBF24; font-weight: bold; font-size: 14px; margin-top: 10px;")
        self.mod_progress.show()
        self.mod_progress.setValue(0)
        
        self._worker = SetupWorker('model', self._settings.ollama_model)
        self._worker.progress.connect(self._on_mod_progress)
        self._worker.finished_ok.connect(self._on_mod_done)
        self._worker.error.connect(self._on_mod_err)
        self._worker.start()

    def _on_mod_progress(self, pct: int, msg: str):
        self.mod_progress.setValue(pct)
        self.mod_status.setText(msg)

    def _on_mod_done(self):
        self.mod_status.setText(f"✓ Model {self._settings.ollama_model} ready")
        self.mod_status.setStyleSheet("color: #10B981; font-weight: bold; font-size: 14px; margin-top: 10px;")
        self.mod_progress.hide()
        self.btn_next.setEnabled(True)

    def _on_mod_err(self, err: str):
        err_lower = err.lower()
        if "network error" in err_lower or "name or service not known" in err_lower or "timed out" in err_lower:
            friendly_err = "Download interrupted. Please check your internet connection and try again."
        else:
            friendly_err = f"Failed to download model: {err}"
            
        self.mod_status.setText(f"⚠ {friendly_err}")
        self.mod_status.setStyleSheet("color: #EF4444; font-weight: bold; font-size: 13px; margin-top: 10px;")
        self.btn_next.setEnabled(False)
        self.btn_back.setEnabled(True)
        self.btn_retry.show()

    def _prev_page(self):
        self.stack.setCurrentIndex(max(0, self.stack.currentIndex() - 1))

    def _next_page(self):
        if self.stack.currentIndex() == self.stack.count() - 1:
            self._settings.set("first_run_completed", True)
            self._settings.save()
            self.setup_complete.emit()
            self.close()
        else:
            self.stack.setCurrentIndex(min(self.stack.count() - 1, self.stack.currentIndex() + 1))
