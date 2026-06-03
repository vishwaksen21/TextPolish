"""
TextPolish — UI
================
Complete PyQt6 interface:
  • SystemTrayIcon  — tray icon + context menu (show/pause/settings/quit)
  • AIWorker        — QThread that streams AI responses
  • SpinnerWidget   — animated loading arc painted via QPainter
  • EnhancementPopup — main floating popup (original vs enhanced, mode picker,
                       streaming text, action buttons, undo)
  • SettingsWindow  — full settings panel with sidebar navigation

Design tokens:
  Dark background  #0D0D0F
  Surface          #16161B
  Card             #1E1E26
  Border           #2A2A38
  Accent (violet)  #7C3AED
  Accent hover     #6D28D9
  Text primary     #F0F0F8
  Text secondary   #9090A8
  Success          #10B981
  Error            #EF4444
"""

from __future__ import annotations

import math
import sys
from typing import Optional

from PyQt6.QtCore import (
    QEasingCurve, QObject, QPoint, QPropertyAnimation,
    QRect, QSize, Qt, QThread, QTimer, pyqtSignal, pyqtSlot,
)
from PyQt6.QtGui import (
    QColor, QCursor, QFont, QFontDatabase, QIcon, QLinearGradient,
    QPainter, QPainterPath, QPen, QPixmap,
)
from PyQt6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDialog, QFormLayout,
    QFrame, QGraphicsDropShadowEffect, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem, QMenu,
    QMessageBox, QProgressBar, QPushButton, QScrollArea, QSizePolicy,
    QSplitter, QStackedWidget, QSystemTrayIcon, QTextEdit,
    QToolButton, QVBoxLayout, QWidget,
)

from ai_processor import AIProcessor, MODE_PROMPTS
from clipboard_manager import ClipboardManager
from platform_handler import paste_text
from settings import Settings
from logger import logger


# ═══════════════════════════════════════════════════════════════════════════════
# STYLE SHEETS
# ═══════════════════════════════════════════════════════════════════════════════

DARK_QSS = """
/* ── Base ───────────────────────────────────────────────── */
* { font-family: "Inter", "Segoe UI", "SF Pro Display", system-ui, sans-serif;
    font-size: 13px; }

QDialog, QWidget { background: #F5F4F0; color: #1A1918; }

QLabel { color: #1A1918; background: transparent; }

/* ── Scrollbars ─────────────────────────────────────────── */
QScrollBar:vertical { background: #E6E4DD; width: 6px; border-radius: 3px; }
QScrollBar::handle:vertical { background: #C5C3BC; border-radius: 3px; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #D97757; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: #E6E4DD; height: 6px; border-radius: 3px; }
QScrollBar::handle:horizontal { background: #C5C3BC; border-radius: 3px; }
QScrollBar::handle:horizontal:hover { background: #D97757; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

/* ── Buttons ────────────────────────────────────────────── */
QPushButton {
    background: #FFFFFF; color: #1A1918;
    border: 1px solid #E6E4DD; border-radius: 8px;
    padding: 8px 18px; font-size: 13px; font-weight: 500;
}
QPushButton:hover { background: #F5F4F0; border-color: #D97757; }
QPushButton:pressed { background: #E6E4DD; }
QPushButton:disabled { color: #A3A09A; border-color: #E6E4DD; }

QPushButton#replaceBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #D97757, stop:1 #C46244);
    border: none; color: #FFFFFF; font-weight: 600;
    padding: 9px 24px; border-radius: 8px;
}
QPushButton#replaceBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #C46244, stop:1 #B05235);
}
QPushButton#replaceBtn:disabled { background: #E6E4DD; color: #A3A09A; }

QPushButton#cancelBtn { color: #6B6965; }
QPushButton#cancelBtn:hover { color: #1A1918; border-color: #D45454; }

QPushButton#undoBtn { color: #6B6965; }
QPushButton#undoBtn:hover { color: #1A1918; border-color: #54A071; }

QPushButton#settingsSaveBtn {
    background: #D97757; border: none; color: #FFF;
    font-weight: 600; padding: 9px 24px; border-radius: 8px;
}
QPushButton#settingsSaveBtn:hover { background: #C46244; }

QPushButton#testBtn { color: #D97757; border-color: #D97757; }
QPushButton#testBtn:hover { background: #F9EBE5; }

/* ── Text areas ─────────────────────────────────────────── */
QTextEdit {
    background: #FFFFFF; color: #1A1918;
    border: 1px solid #E6E4DD; border-radius: 10px;
    padding: 14px; font-size: 14px; line-height: 1.6;
    selection-background-color: rgba(217, 119, 87, 0.2);
}
QTextEdit:focus { border-color: #D97757; }

/* ── Line edits ─────────────────────────────────────────── */
QLineEdit {
    background: #FFFFFF; color: #1A1918;
    border: 1px solid #E6E4DD; border-radius: 8px;
    padding: 8px 12px; font-size: 13px;
}
QLineEdit:focus { border-color: #D97757; }

/* ── Combo boxes ────────────────────────────────────────── */
QComboBox {
    background: #FFFFFF; color: #1A1918;
    border: 1px solid #E6E4DD; border-radius: 8px;
    padding: 7px 12px; font-size: 13px;
}
QComboBox:hover { border-color: #D97757; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox QAbstractItemView {
    background: #FFFFFF; border: 1px solid #E6E4DD; color: #1A1918;
    selection-background-color: #F9EBE5; selection-color: #D97757; outline: none;
}

/* ── Check boxes ────────────────────────────────────────── */
QCheckBox { color: #F0F0F8; spacing: 8px; }
QCheckBox::indicator { width: 16px; height: 16px; border-radius: 4px;
    border: 1px solid #2A2A38; background: #16161B; }
QCheckBox::indicator:checked { background: #7C3AED; border-color: #7C3AED; }

/* ── List widgets ───────────────────────────────────────── */
QListWidget {
    background: #16161B; border: 1px solid #2A2A38; border-radius: 10px;
    outline: none; color: #F0F0F8; padding: 4px;
}
QListWidget::item { padding: 10px 12px; border-radius: 8px; }
QListWidget::item:selected { background: #2A1F4A; color: #A78BFA; }
QListWidget::item:hover:!selected { background: #1E1E26; }

/* ── Group boxes ────────────────────────────────────────── */
QGroupBox {
    border: 1px solid #2A2A38; border-radius: 10px;
    margin-top: 14px; padding: 14px; color: #9090A8; font-size: 11px;
    font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px;
}
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 6px; }

/* ── Frames / separators ────────────────────────────────── */
QFrame[frameShape="4"], QFrame[frameShape="5"] {
    color: #2A2A38; max-height: 1px;
}

/* ── Splitter ───────────────────────────────────────────── */
QSplitter::handle { background: #2A2A38; width: 1px; height: 1px; }
"""

LIGHT_QSS = """
* { font-family: "Inter", "Segoe UI", system-ui, sans-serif; font-size: 13px; }
QDialog, QWidget { background: #F5F5F7; color: #1A1A1F; }
QLabel { color: #1A1A1F; background: transparent; }
QScrollBar:vertical { background: #E5E5EA; width: 6px; border-radius: 3px; }
QScrollBar::handle:vertical { background: #C7C7CC; border-radius: 3px; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #7C3AED; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QPushButton { background: #FFFFFF; color: #1A1A1F; border: 1px solid #D1D1D6;
    border-radius: 8px; padding: 8px 18px; font-size: 13px; font-weight: 500; }
QPushButton:hover { background: #F0F0F7; border-color: #7C3AED; }
QPushButton#replaceBtn { background: #7C3AED; border: none; color: #FFF; font-weight: 600;
    padding: 9px 24px; border-radius: 8px; }
QPushButton#replaceBtn:hover { background: #6D28D9; }
QPushButton#cancelBtn { color: #636366; }
QPushButton#settingsSaveBtn { background: #7C3AED; border: none; color: #FFF; font-weight: 600; padding: 9px 24px; border-radius: 8px; }
QPushButton#testBtn { color: #7C3AED; border-color: #7C3AED; }
QTextEdit { background: #FFFFFF; color: #1A1A1F; border: 1px solid #D1D1D6;
    border-radius: 10px; padding: 14px; font-size: 14px; selection-background-color: #7C3AED40; }
QTextEdit:focus { border-color: #7C3AED; }
QLineEdit { background: #FFFFFF; color: #1A1A1F; border: 1px solid #D1D1D6;
    border-radius: 8px; padding: 8px 12px; }
QLineEdit:focus { border-color: #7C3AED; }
QComboBox { background: #FFFFFF; color: #1A1A1F; border: 1px solid #D1D1D6;
    border-radius: 8px; padding: 7px 12px; }
QComboBox:hover { border-color: #7C3AED; }
QComboBox QAbstractItemView { background: #FFFFFF; color: #1A1A1F;
    selection-background-color: #7C3AED; }
QCheckBox { color: #1A1A1F; spacing: 8px; }
QCheckBox::indicator { width: 16px; height: 16px; border-radius: 4px;
    border: 1px solid #C7C7CC; background: #FFFFFF; }
QCheckBox::indicator:checked { background: #7C3AED; border-color: #7C3AED; }
QListWidget { background: #FFFFFF; border: 1px solid #D1D1D6; border-radius: 10px;
    outline: none; color: #1A1A1F; padding: 4px; }
QListWidget::item { padding: 10px 12px; border-radius: 8px; }
QListWidget::item:selected { background: #EDE9FE; color: #5B21B6; }
QListWidget::item:hover:!selected { background: #F5F5F7; }
QGroupBox { border: 1px solid #D1D1D6; border-radius: 10px;
    margin-top: 14px; padding: 14px; color: #8E8E93; font-size: 11px; font-weight: 600; }
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 6px; }
"""


SETTINGS_LIGHT_SCOPED_QSS = """
QDialog#SettingsWindow {
    background: #F7F7F8;
}

QWidget#SettingsSidebar {
    background: #F7F7F8;
    border-right: 1px solid #E5E7EB;
}

QListWidget#SettingsNav {
    background: transparent;
    border: none;
    outline: none;
}

QListWidget#SettingsNav::item {
    padding: 10px 14px;
    margin: 2px 0;
    border-radius: 8px;
    color: #4B5563;
    font-size: 13px;
    font-weight: 500;
}

QListWidget#SettingsNav::item:selected {
    background: #F3EEFF;
    color: #7C3AED;
    border-left: 3px solid #7C3AED;
    border-top-left-radius: 0px;
    border-bottom-left-radius: 0px;
    font-weight: 600;
}

QListWidget#SettingsNav::item:hover:!selected {
    background: rgba(0, 0, 0, 0.03);
    color: #111827;
}

QWidget#SettingsContent {
    background: #F7F7F8;
}

QLabel#SettingsTitle {
    color: #111827;
    font-size: 20px;
    font-weight: 700;
}

QLabel#SettingsMuted {
    color: #6B7280;
    font-size: 12px;
}

QFrame#SettingsCard {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
}

QFrame#SidebarPromoCard {
    background: #F3EEFF;
    border: 1px solid #E5D5FF;
    border-radius: 12px;
}

QFrame#SettingsDivider {
    background-color: #E5E7EB;
    max-height: 1px;
    border: none;
}

QToolButton#DisclosureButton {
    background: transparent;
    border: none;
    color: #6B7280;
    font-size: 12px;
    font-weight: 600;
    padding: 6px 0;
}
QToolButton#DisclosureButton:hover { color: #111827; }

QPushButton#SecondaryBtn {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    color: #111827;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: 600;
}
QPushButton#SecondaryBtn:hover { background: #F8F8FA; border-color: #7C3AED; }

QLineEdit#SettingsLineEdit {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 6px;
    padding: 5px 8px;
    color: #111827;
    font-size: 12px;
}
QLineEdit#SettingsLineEdit:focus { border-color: #7C3AED; }

QComboBox#SettingsCombo {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 6px;
    padding: 4px 8px;
    color: #111827;
    font-size: 12px;
}
QComboBox#SettingsCombo:hover { border-color: #C5C7CB; }
QComboBox#SettingsCombo:focus { border-color: #7C3AED; }

QPushButton#AboutLink {
    background: transparent;
    border: none;
    color: #7C3AED;
    font-size: 13px;
    font-weight: 500;
    padding: 0;
}
QPushButton#AboutLink:hover {
    text-decoration: underline;
}

QLabel#Keycap {
    border: 1px solid #D1D5DB;
    border-bottom: 2px solid #C4C4C4;
    border-radius: 6px;
    background: #FAFAFA;
    color: #111827;
    font-size: 14px;
    font-weight: 600;
    padding: 2px 8px;
}
"""

SETTINGS_DARK_SCOPED_QSS = """
QDialog#SettingsWindow {
    background: #1C1C1E;
}

QWidget#SettingsSidebar {
    background: #1C1C1E;
    border-right: 1px solid #2C2C2E;
}

QListWidget#SettingsNav {
    background: transparent;
    border: none;
    outline: none;
}

QListWidget#SettingsNav::item {
    padding: 10px 14px;
    margin: 2px 0;
    border-radius: 8px;
    color: #9090A8;
    font-size: 13px;
    font-weight: 500;
}

QListWidget#SettingsNav::item:selected {
    background: rgba(255, 255, 255, 0.08);
    color: #F0F0F8;
    border-left: 3px solid #A78BFA;
    border-top-left-radius: 0px;
    border-bottom-left-radius: 0px;
    font-weight: 600;
}

QListWidget#SettingsNav::item:hover:!selected {
    background: rgba(255, 255, 255, 0.03);
    color: #F0F0F8;
}

QWidget#SettingsContent {
    background: #1C1C1E;
}

QLabel#SettingsTitle {
    color: #F0F0F8;
    font-size: 20px;
    font-weight: 700;
}

QLabel#SettingsMuted {
    color: #9090A8;
    font-size: 12px;
}

QFrame#SettingsCard {
    background: #2C2C2E;
    border: 1px solid #3C3C3E;
    border-radius: 12px;
}

QFrame#SidebarPromoCard {
    background: rgba(124, 58, 237, 0.12);
    border: 1px solid rgba(124, 58, 237, 0.25);
    border-radius: 12px;
}

QFrame#SettingsDivider {
    background-color: #3C3C3E;
    max-height: 1px;
    border: none;
}

QToolButton#DisclosureButton {
    background: transparent;
    border: none;
    color: #9090A8;
    font-size: 12px;
    font-weight: 600;
    padding: 6px 0;
}
QToolButton#DisclosureButton:hover { color: #F0F0F8; }

QPushButton#SecondaryBtn {
    background: #2C2C2E;
    border: 1px solid #3C3C3E;
    color: #F0F0F8;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: 600;
}
QPushButton#SecondaryBtn:hover { background: #353538; border-color: #A78BFA; }

QLineEdit#SettingsLineEdit {
    background: #1C1C1E;
    border: 1px solid #3C3C3E;
    border-radius: 6px;
    padding: 5px 8px;
    color: #F0F0F8;
    font-size: 12px;
}
QLineEdit#SettingsLineEdit:focus { border-color: #A78BFA; }

QComboBox#SettingsCombo {
    background: #1C1C1E;
    border: 1px solid #3C3C3E;
    border-radius: 6px;
    padding: 4px 8px;
    color: #F0F0F8;
    font-size: 12px;
}
QComboBox#SettingsCombo:hover { border-color: #4C4C4E; }
QComboBox#SettingsCombo:focus { border-color: #A78BFA; }

QPushButton#AboutLink {
    background: transparent;
    border: none;
    color: #A78BFA;
    font-size: 13px;
    font-weight: 500;
    padding: 0;
}
QPushButton#AboutLink:hover {
    text-decoration: underline;
}

QLabel#Keycap {
    border: 1px solid #4C4C4E;
    border-bottom: 2px solid #5C5C5F;
    border-radius: 6px;
    background: #2C2C2E;
    color: #F0F0F8;
    font-size: 14px;
    font-weight: 600;
    padding: 2px 8px;
}
"""


def get_qss(theme: str) -> str:
    base = DARK_QSS if theme == "dark" else LIGHT_QSS
    scoped = SETTINGS_DARK_SCOPED_QSS if theme == "dark" else SETTINGS_LIGHT_SCOPED_QSS
    return base + "\n" + scoped


# ═══════════════════════════════════════════════════════════════════════════════
# SPINNER WIDGET
# ═══════════════════════════════════════════════════════════════════════════════

class SpinnerWidget(QWidget):
    """Animated arc spinner drawn with QPainter."""

    def __init__(self, parent: Optional[QWidget] = None, size: int = 36) -> None:
        super().__init__(parent)
        self._size = size
        self._angle = 0
        self.setFixedSize(size, size)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)

    def start(self) -> None:
        self.show()
        self._timer.start(16)  # ~60 fps

    def stop(self) -> None:
        self._timer.stop()
        self.hide()

    def _tick(self) -> None:
        self._angle = (self._angle + 6) % 360
        self.update()

    def paintEvent(self, _event) -> None:  # type: ignore[override]
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.translate(self._size / 2, self._size / 2)
        p.rotate(self._angle)
        pen = QPen(QColor("#7C3AED"), 3)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(pen)
        r = (self._size - 6) / 2
        p.drawArc(
            int(-r), int(-r), int(r * 2), int(r * 2),
            0 * 16, 270 * 16,   # 270° arc gap = loading look
        )
        p.end()


# ═══════════════════════════════════════════════════════════════════════════════
# AI WORKER THREAD
# ═══════════════════════════════════════════════════════════════════════════════

class AIWorker(QThread):
    """
    Runs the AI streaming call in a background thread.
    Emits signals to update the UI safely from the Qt main thread.
    """

    chunk_received = pyqtSignal(str)    # Each text chunk as it arrives
    finished       = pyqtSignal(str)    # Full assembled result
    error_occurred = pyqtSignal(str)    # Error message

    def __init__(
        self,
        processor: AIProcessor,
        text: str,
        mode: str,
        custom_instruction: Optional[str] = None,
        parent: Optional[QObject] = None,
    ) -> None:
        super().__init__(parent)
        self._processor = processor
        self._text = text
        self._mode = mode
        self._custom_instruction = custom_instruction
        self._full_result = ""

    def run(self) -> None:
        try:
            for chunk in self._processor.enhance(self._text, self._mode, self._custom_instruction):
                self._full_result += chunk
                self.chunk_received.emit(chunk)
            self.finished.emit(self._full_result)
        except Exception as exc:                          # noqa: BLE001
            logger.error("AIWorker error: %s", exc)
            self.error_occurred.emit(str(exc))


# ═══════════════════════════════════════════════════════════════════════════════
# MODE BUTTON
# ═══════════════════════════════════════════════════════════════════════════════

class ModeButton(QToolButton):
    """Styled checkable mode pill button."""

    def __init__(self, label: str, mode_key: str, parent=None) -> None:
        super().__init__(parent)
        self.mode_key = mode_key
        self.setText(label)
        self.setCheckable(True)
        self.setFixedHeight(30)
        self._update_style(False)

    def _update_style(self, checked: bool) -> None:
        if checked:
            self.setStyleSheet(
                "QToolButton { background: #7C3AED; color: #FFF; border: none;"
                " border-radius: 15px; padding: 0 14px; font-weight: 600; font-size: 12px; }"
            )
        else:
            self.setStyleSheet(
                "QToolButton { background: #1E1E26; color: #9090A8; border: 1px solid #2A2A38;"
                " border-radius: 15px; padding: 0 14px; font-size: 12px; }"
                "QToolButton:hover { background: #2A2A38; color: #F0F0F8; border-color: #7C3AED; }"
            )

    def setChecked(self, checked: bool) -> None:
        super().setChecked(checked)
        self._update_style(checked)


# ═══════════════════════════════════════════════════════════════════════════════
# ENHANCEMENT POPUP
# ═══════════════════════════════════════════════════════════════════════════════

class EnhancementPopup(QDialog):
    """
    The primary user-facing popup.

    Shows the original text and streams the AI-enhanced version in real time.
    Provides Replace, Undo, and Cancel actions.
    """

    def __init__(
        self,
        settings: Settings,
        processor: AIProcessor,
        clipboard_mgr: ClipboardManager,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._settings    = settings
        self._processor   = processor
        self._clipboard   = clipboard_mgr
        self._worker: Optional[AIWorker] = None
        self._enhanced_text = ""
        self._original_text = ""
        self._current_mode  = settings.default_mode

        self._build_ui()
        self._apply_shadow()

    # ── Build ─────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumSize(700, 480)
        self.setMaximumSize(900, 640)

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(0)

        # ── Card container ────────────────────────────────────────────────────
        card = QWidget()
        bg = "#1E1E26" if self._settings.theme == "dark" else "#FFFFFF"
        card.setStyleSheet(
            f"background: {bg}; border-radius: 16px;"
        )
        root.addWidget(card)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # ── Header ────────────────────────────────────────────────────────────
        header = QHBoxLayout()
        icon_lbl = QLabel("✦")
        icon_lbl.setStyleSheet(
            "color: #7C3AED; font-size: 20px; background: transparent;"
        )
        title_lbl = QLabel("Avelyn")
        title_lbl.setStyleSheet(
            "color: #F0F0F8; font-size: 16px; font-weight: 700; background: transparent;"
        )
        self._status_lbl = QLabel("Enhancing…")
        self._status_lbl.setStyleSheet(
            "color: #9090A8; font-size: 12px; background: transparent;"
        )
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(28, 28)
        close_btn.setStyleSheet(
            "QPushButton { background: transparent; color: #9090A8; border: none; font-size: 14px; }"
            "QPushButton:hover { color: #EF4444; }"
        )
        close_btn.clicked.connect(self._on_cancel)

        header.addWidget(icon_lbl)
        header.addSpacing(8)
        header.addWidget(title_lbl)
        header.addStretch()
        header.addWidget(self._status_lbl)
        header.addSpacing(8)
        header.addWidget(close_btn)
        layout.addLayout(header)

        # ── Separator ─────────────────────────────────────────────────────────
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #2A2A38;")
        layout.addWidget(sep)

        # ── Mode pills ────────────────────────────────────────────────────────
        mode_row = QHBoxLayout()
        mode_row.setSpacing(8)
        self._mode_btns: dict[str, ModeButton] = {}
        modes = [
            ("Professional", "professional"),
            ("Creative",     "creative"),
            ("Technical",    "technical"),
            ("Concise",      "concise"),
            ("Academic",     "academic"),
        ]
        for label, key in modes:
            btn = ModeButton(label, key)
            btn.clicked.connect(lambda checked, k=key: self._on_mode_changed(k))
            if key == self._current_mode:
                btn.setChecked(True)
            self._mode_btns[key] = btn
            mode_row.addWidget(btn)
        mode_row.addStretch()
        layout.addLayout(mode_row)

        # ── Text areas ────────────────────────────────────────────────────────
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(8)
        splitter.setChildrenCollapsible(False)

        # Original (left)
        orig_panel = QWidget()
        orig_layout = QVBoxLayout(orig_panel)
        orig_layout.setContentsMargins(0, 0, 0, 0)
        orig_layout.setSpacing(6)
        orig_lbl = QLabel("Original")
        orig_lbl.setStyleSheet(
            "color: #9090A8; font-size: 11px; font-weight: 600; letter-spacing: 0.6px;"
            " text-transform: uppercase; background: transparent;"
        )
        self._orig_edit = QTextEdit()
        self._orig_edit.setReadOnly(True)
        self._orig_edit.setPlaceholderText("Original text will appear here…")
        orig_layout.addWidget(orig_lbl)
        orig_layout.addWidget(self._orig_edit)

        # Enhanced (right)
        enh_panel = QWidget()
        enh_layout = QVBoxLayout(enh_panel)
        enh_layout.setContentsMargins(0, 0, 0, 0)
        enh_layout.setSpacing(6)

        enh_header = QHBoxLayout()
        enh_lbl = QLabel("Enhanced")
        enh_lbl.setStyleSheet(
            "color: #7C3AED; font-size: 11px; font-weight: 600; letter-spacing: 0.6px;"
            " text-transform: uppercase; background: transparent;"
        )
        self._spinner = SpinnerWidget(size=20)
        enh_header.addWidget(enh_lbl)
        enh_header.addWidget(self._spinner)
        enh_header.addStretch()

        self._enh_edit = QTextEdit()
        self._enh_edit.setReadOnly(True)
        self._enh_edit.setPlaceholderText("AI-enhanced text will stream here…")
        enh_layout.addLayout(enh_header)
        enh_layout.addWidget(self._enh_edit)

        splitter.addWidget(orig_panel)
        splitter.addWidget(enh_panel)
        splitter.setSizes([340, 340])
        layout.addWidget(splitter, 1)

        # ── Action buttons ────────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.setObjectName("cancelBtn")
        self._cancel_btn.clicked.connect(self._on_cancel)

        self._undo_btn = QPushButton("↩  Undo")
        self._undo_btn.setObjectName("undoBtn")
        self._undo_btn.setEnabled(False)
        self._undo_btn.clicked.connect(self._on_undo)

        self._replace_btn = QPushButton("Replace Text  ✓")
        self._replace_btn.setObjectName("replaceBtn")
        self._replace_btn.setEnabled(False)
        self._replace_btn.clicked.connect(self._on_replace)

        btn_row.addWidget(self._cancel_btn)
        btn_row.addStretch()
        btn_row.addWidget(self._undo_btn)
        btn_row.addWidget(self._replace_btn)
        layout.addLayout(btn_row)

    def _apply_shadow(self) -> None:
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 120))
        self.setGraphicsEffect(shadow)

    # ── Public API ────────────────────────────────────────────────────────────

    def show_for_text(self, text: str) -> None:
        """Populate the popup with `text` and start the AI enhancement."""
        self._original_text = text
        self._enhanced_text = ""
        self._orig_edit.setPlainText(text)
        self._enh_edit.clear()
        self._replace_btn.setEnabled(False)
        self._undo_btn.setEnabled(False)
        self._status_lbl.setText("Enhancing…")
        self._spinner.start()

        # Position popup near cursor.
        cursor_pos = QCursor.pos()
        screen = QApplication.primaryScreen()
        if screen:
            sg = screen.availableGeometry()
            x = min(cursor_pos.x() + 20, sg.right() - self.width() - 20)
            y = min(cursor_pos.y() + 20, sg.bottom() - self.height() - 20)
            self.move(max(sg.left() + 20, x), max(sg.top() + 20, y))

        self.show()
        self._animate_in()
        self._start_enhancement()

    # ── Internal logic ────────────────────────────────────────────────────────

    def _animate_in(self) -> None:
        anim = QPropertyAnimation(self, b"windowOpacity", self)
        anim.setDuration(200)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()

    def _start_enhancement(self) -> None:
        if self._worker and self._worker.isRunning():
            self._worker.terminate()
            self._worker.wait(500)

        self._worker = AIWorker(self._processor, self._original_text, self._current_mode)
        self._worker.chunk_received.connect(self._on_chunk)
        self._worker.finished.connect(self._on_finished)
        self._worker.error_occurred.connect(self._on_error)
        self._worker.start()

    @pyqtSlot(str)
    def _on_chunk(self, chunk: str) -> None:
        self._enhanced_text += chunk
        cursor = self._enh_edit.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.insertText(chunk)
        self._enh_edit.setTextCursor(cursor)

    @pyqtSlot(str)
    def _on_finished(self, full_text: str) -> None:
        self._enhanced_text = full_text
        self._spinner.stop()
        self._status_lbl.setText(
            f"Ready • {len(full_text)} chars"
        )
        self._replace_btn.setEnabled(True)

    @pyqtSlot(str)
    def _on_error(self, msg: str) -> None:
        self._spinner.stop()
        self._status_lbl.setText("⚠ Error")
        self._enh_edit.setPlainText(f"Error: {msg}")
        self._replace_btn.setEnabled(False)

    def _on_mode_changed(self, key: str) -> None:
        for k, btn in self._mode_btns.items():
            btn.setChecked(k == key)
        self._current_mode = key
        # Re-run enhancement with new mode.
        self._enh_edit.clear()
        self._enhanced_text = ""
        self._replace_btn.setEnabled(False)
        self._status_lbl.setText("Re-enhancing…")
        self._spinner.start()
        self._start_enhancement()

    def _on_replace(self) -> None:
        if not self._enhanced_text:
            return
        logger.info("Replacing text (%d chars).", len(self._enhanced_text))
        self._clipboard.set(self._enhanced_text)
        self.hide()
        # Small delay to ensure popup is hidden before simulating paste.
        QTimer.singleShot(120, paste_text)
        self._undo_btn.setEnabled(True)

        # Save to history.
        self._settings.add_to_history(
            self._original_text, self._enhanced_text, self._current_mode
        )

    def _on_undo(self) -> None:
        logger.info("Undoing replacement.")
        self._clipboard.set(self._original_text)
        QTimer.singleShot(80, paste_text)
        self._undo_btn.setEnabled(False)
        self._status_lbl.setText("Undone ✓")

    def _on_cancel(self) -> None:
        if self._worker and self._worker.isRunning():
            self._worker.terminate()
        self._clipboard.restore()
        self.hide()

    # ── Drag to move (frameless window) ───────────────────────────────────────

    def mousePressEvent(self, event) -> None:  # type: ignore[override]
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event) -> None:   # type: ignore[override]
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, "_drag_pos"):
            self.move(event.globalPosition().toPoint() - self._drag_pos)

    def keyPressEvent(self, event) -> None:    # type: ignore[override]
        if event.key() == Qt.Key.Key_Escape:
            self._on_cancel()
        else:
            super().keyPressEvent(event)


# ═══════════════════════════════════════════════════════════════════════════════
# SETTINGS WIDGETS & VECTOR ICONS
# ═══════════════════════════════════════════════════════════════════════════════

def _paint_settings_icon(kind: str, color: str = "#111827", size: int = 24) -> QPixmap:
    pix = QPixmap(size, size)
    pix.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pix)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    pen = QPen(QColor(color))
    pen.setWidthF(1.5)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    
    # Scale coordinates to fit the actual size nicely (padding included)
    painter.scale(size / 24.0, size / 24.0)
    
    if kind == "sparkles":
        path = QPainterPath()
        # Large star
        path.moveTo(12, 3)
        path.quadTo(12, 12, 21, 12)
        path.quadTo(12, 12, 12, 21)
        path.quadTo(12, 12, 3, 12)
        path.quadTo(12, 12, 12, 3)
        
        # Small star top right
        path.moveTo(18, 5)
        path.quadTo(18, 8, 21, 8)
        path.quadTo(18, 8, 18, 11)
        path.quadTo(18, 8, 15, 8)
        path.quadTo(18, 8, 18, 5)
        painter.drawPath(path)
        
    elif kind == "keyboard":
        painter.drawRoundedRect(3, 5, 18, 14, 3, 3)
        painter.drawLine(8, 15, 16, 15)
        painter.drawPoint(6, 9)
        painter.drawPoint(9, 9)
        painter.drawPoint(12, 9)
        painter.drawPoint(15, 9)
        painter.drawPoint(18, 9)
        painter.drawPoint(6, 12)
        painter.drawPoint(18, 12)
        
    elif kind == "palette":
        path = QPainterPath()
        path.moveTo(12, 4)
        path.cubicTo(18, 4, 21, 8, 21, 12)
        path.cubicTo(21, 17, 17, 20, 12, 20)
        path.cubicTo(9, 20, 7, 18, 5, 16)
        path.cubicTo(3, 13, 6, 4, 12, 4)
        painter.drawPath(path)
        painter.drawPoint(10, 8)
        painter.drawPoint(15, 9)
        painter.drawPoint(16, 13)
        painter.drawPoint(12, 16)
        
    elif kind == "clock":
        painter.drawEllipse(3, 3, 18, 18)
        painter.drawLine(12, 12, 12, 7)
        painter.drawLine(12, 12, 16, 12)
        
    elif kind == "info":
        painter.drawEllipse(3, 3, 18, 18)
        painter.drawLine(12, 10, 12, 16)
        painter.drawPoint(12, 7)
        
    elif kind == "shield":
        path = QPainterPath()
        path.moveTo(12, 4)
        path.quadTo(19, 4, 19, 9)
        path.quadTo(19, 17, 12, 21)
        path.quadTo(5, 17, 5, 9)
        path.quadTo(5, 4, 12, 4)
        painter.drawPath(path)
        
    elif kind == "check":
        path = QPainterPath()
        path.moveTo(5, 12)
        path.lineTo(10, 17)
        path.lineTo(19, 6)
        painter.drawPath(path)
        
    elif kind == "wave":
        path = QPainterPath()
        path.moveTo(4, 12)
        path.quadTo(8, 6, 12, 12)
        path.quadTo(16, 18, 20, 12)
        painter.drawPath(path)
        
    elif kind == "server":
        painter.drawRoundedRect(4, 5, 16, 4, 1, 1)
        painter.drawRoundedRect(4, 10, 16, 4, 1, 1)
        painter.drawRoundedRect(4, 15, 16, 4, 1, 1)
        painter.drawPoint(12, 7)
        painter.drawPoint(12, 12)
        painter.drawPoint(12, 17)
        
    elif kind == "link":
        painter.save()
        painter.translate(9, 9)
        painter.rotate(-45)
        painter.drawRoundedRect(-6, -3, 12, 6, 3, 3)
        painter.restore()
        painter.save()
        painter.translate(15, 15)
        painter.rotate(-45)
        painter.drawRoundedRect(-6, -3, 12, 6, 3, 3)
        painter.restore()
        
    elif kind == "cube":
        painter.drawLine(12, 12, 12, 20)
        painter.drawLine(12, 4, 5, 8)
        painter.drawLine(12, 4, 19, 8)
        painter.drawLine(5, 8, 12, 12)
        painter.drawLine(19, 8, 12, 12)
        painter.drawLine(5, 8, 5, 16)
        painter.drawLine(19, 8, 19, 16)
        painter.drawLine(5, 16, 12, 20)
        painter.drawLine(19, 16, 12, 20)
        
    elif kind == "sliders":
        painter.drawLine(4, 8, 20, 8)
        painter.drawEllipse(14, 6, 4, 4)
        painter.drawLine(4, 12, 20, 12)
        painter.drawEllipse(8, 10, 4, 4)
        painter.drawLine(4, 16, 20, 16)
        painter.drawEllipse(16, 14, 4, 4)
        
    elif kind == "chevron":
        path = QPainterPath()
        path.moveTo(9, 7)
        path.lineTo(14, 12)
        path.lineTo(9, 17)
        painter.drawPath(path)
        
    else:
        painter.drawEllipse(10, 10, 4, 4)
        
    painter.end()
    return pix

def _settings_nav_icon(icon_kind: str) -> QIcon:
    return QIcon(_paint_settings_icon(icon_kind, "#4B5563", 16))

def _theme_preview(mode: str) -> QIcon:
    pix = QPixmap(96, 58)
    pix.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pix)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # ── Background colors ──
    bg_color = QColor("#F3F4F6") if mode == "light" else QColor("#1F2937")
    card_color = QColor("#FFFFFF") if mode == "light" else QColor("#2D3748")
    sidebar_bg = QColor("#E5E7EB") if mode == "light" else QColor("#111827")
    line_color = QColor("#D1D5DB") if mode == "light" else QColor("#4A5568")
    
    if mode == "system":
        painter.setClipRect(0, 0, 96, 58)
        
        # Left diagonal half is light
        path_light = QPainterPath()
        path_light.moveTo(0, 0)
        path_light.lineTo(96, 0)
        path_light.lineTo(0, 58)
        path_light.closeSubpath()
        painter.fillPath(path_light, QColor("#F3F4F6"))
        
        # Right diagonal half is dark
        path_dark = QPainterPath()
        path_dark.moveTo(96, 58)
        path_dark.lineTo(96, 0)
        path_dark.lineTo(0, 58)
        path_dark.closeSubpath()
        painter.fillPath(path_dark, QColor("#1F2937"))
        
        # Split line and frame
        painter.setPen(QPen(QColor("#9CA3AF"), 1))
        painter.drawLine(96, 0, 0, 58)
        painter.setPen(QPen(QColor("#9CA3AF"), 1.5))
        painter.drawRoundedRect(2, 2, 92, 54, 4, 4)
        
        painter.end()
        return QIcon(pix)
        
    # Paint standard solid light/dark preview
    painter.setBrush(bg_color)
    painter.setPen(QPen(line_color, 1))
    painter.drawRoundedRect(2, 2, 92, 54, 4, 4)
    
    # Sidebar
    painter.setBrush(sidebar_bg)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(2, 2, 26, 54, 4, 4)
    painter.drawRect(24, 2, 4, 54) # Cover rounded corners
    
    # Sidebar border line
    painter.setPen(QPen(line_color, 1))
    painter.drawLine(28, 2, 28, 56)
    
    # Titlebar dots
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("#EF4444"))
    painter.drawEllipse(6, 6, 4, 4)
    painter.setBrush(QColor("#F59E0B"))
    painter.drawEllipse(12, 6, 4, 4)
    painter.setBrush(QColor("#10B981"))
    painter.drawEllipse(18, 6, 4, 4)
    
    # Content rows/card
    painter.setPen(QPen(line_color, 1))
    painter.setBrush(card_color)
    painter.drawRoundedRect(34, 14, 52, 34, 2, 2)
    
    # Mock text rows inside card
    painter.setPen(QPen(line_color, 1))
    painter.drawLine(38, 20, 54, 20)
    painter.drawLine(38, 26, 68, 26)
    painter.drawLine(38, 32, 48, 32)
    
    # Sliders knobs representation
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("#7C3AED"))
    painter.drawEllipse(76, 18, 4, 4)
    painter.drawEllipse(72, 30, 4, 4)
    
    painter.end()
    return QIcon(pix)

def _divider_line() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Plain)
    line.setObjectName("SettingsDivider")
    line.setStyleSheet("background: #E5E7EB; border: none; height: 1px; max-height: 1px;")
    return line

def _settings_group(widgets: list[QWidget]) -> QWidget:
    card = QFrame()
    card.setObjectName("SettingsCard")
    layout = QVBoxLayout(card)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    for i, w in enumerate(widgets):
        layout.addWidget(w)
        if i < len(widgets) - 1:
            layout.addWidget(_divider_line())
    return card

def _keycap_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setObjectName("KeycapLabel")
    lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lbl.setStyleSheet(
        "font-family: system-ui, -apple-system, sans-serif; font-size: 11px; font-weight: 700; "
        "color: #1F2937; background: #FAFAFA; border: 1px solid #D1D5DB; "
        "border-bottom: 2.5px solid #C4C4C4; border-radius: 5px; "
        "padding: 2px 6px; min-width: 14px; margin: 1px 0px;"
    )
    return lbl

def _premium_row(
    label_text: str,
    sub_label: str = "",
    icon_kind: str = "",
    icon_color: str = "#7C3AED",
    icon_bg_color: str = "#F3EEFF",
    widget: Optional[QWidget] = None,
    right_text: str = "",
    show_arrow: bool = False,
) -> QWidget:
    row = QWidget()
    row.setObjectName("SettingsRow")
    l = QHBoxLayout(row)
    l.setContentsMargins(14, 10, 14, 10)
    l.setSpacing(12)

    if icon_kind:
        icon_wrapper = QWidget()
        icon_wrapper.setFixedSize(30, 30)
        icon_wrapper.setStyleSheet(
            f"background-color: {icon_bg_color}; border-radius: 15px;"
        )
        iw_layout = QHBoxLayout(icon_wrapper)
        iw_layout.setContentsMargins(0, 0, 0, 0)
        iw_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon_lbl = QLabel()
        icon_lbl.setPixmap(_paint_settings_icon(icon_kind, icon_color, 16))
        iw_layout.addWidget(icon_lbl)
        l.addWidget(icon_wrapper)

    text_w = QWidget()
    text_l = QVBoxLayout(text_w)
    text_l.setContentsMargins(0, 0, 0, 0)
    text_l.setSpacing(1)
    
    title = QLabel(label_text)
    title.setObjectName("SettingsRowTitle")
    title.setStyleSheet("font-size: 13px; font-weight: 600; color: #111827;")
    text_l.addWidget(title)
    
    if sub_label:
        desc = QLabel(sub_label)
        desc.setObjectName("SettingsRowDesc")
        desc.setStyleSheet("font-size: 11px; color: #6B7280;")
        desc.setWordWrap(True)
        text_l.addWidget(desc)
        
    l.addWidget(text_w, 1)

    if widget is not None:
        l.addWidget(widget)
    elif right_text:
        rt = QLabel(right_text)
        rt.setStyleSheet("font-size: 13px; color: #6B7280; font-weight: 500;")
        l.addWidget(rt)

    if show_arrow:
        arrow = QLabel()
        arrow.setPixmap(_paint_settings_icon("chevron", "#9CA3AF", 12))
        l.addWidget(arrow)

    return row


# ═══════════════════════════════════════════════════════════════════════════════
# SETTINGS WINDOW
# ═══════════════════════════════════════════════════════════════════════════════

class SettingsWindow(QDialog):
    """Full settings panel with sidebar navigation."""

    settings_changed = pyqtSignal()

    def __init__(
        self,
        settings: Settings,
        processor: AIProcessor,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._settings  = settings
        self._processor = processor
        self._build_ui()

    def _build_ui(self) -> None:
        self.setWindowTitle("Avelyn — Settings")
        self.setObjectName("SettingsWindow")
        self.setWindowFlags(
            Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint
        )
        self.setMinimumSize(680, 520)
        self.resize(760, 560)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── Sidebar ───────────────────────────────────────────────────────────
        sidebar = QWidget()
        sidebar.setObjectName("SettingsSidebar")
        sidebar.setFixedWidth(220)
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(12, 16, 12, 16)
        sb_layout.setSpacing(10)

        from utils import get_resource_path
        logo_path = get_resource_path("public/logo.png")
        
        brand = QWidget()
        brand.setObjectName("SettingsBrand")
        brand_row = QHBoxLayout(brand)
        brand_row.setContentsMargins(8, 4, 8, 8)
        brand_row.setSpacing(10)

        logo_lbl = QLabel()
        logo_lbl.setFixedSize(42, 42)
        if logo_path.exists():
            pm = QPixmap(str(logo_path))
            if not pm.isNull():
                logo_lbl.setPixmap(pm.scaled(42, 42, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            logo_lbl.setPixmap(_paint_settings_icon("sparkles", "#7C3AED", 42))

        brand_text_w = QWidget()
        brand_text_l = QVBoxLayout(brand_text_w)
        brand_text_l.setContentsMargins(0, 0, 0, 0)
        brand_text_l.setSpacing(1)

        name_lbl = QLabel("Avelyn")
        name_lbl.setStyleSheet("font-size: 18px; font-weight: 700; color: #111827;")
        subtitle_lbl = QLabel("AI Writing Assistant")
        subtitle_lbl.setStyleSheet("font-size: 12px; color: #6B7280;")

        brand_text_l.addWidget(name_lbl)
        brand_text_l.addWidget(subtitle_lbl)

        brand_row.addWidget(logo_lbl)
        brand_row.addWidget(brand_text_w, 1)

        sb_layout.addWidget(brand)
        sb_layout.addSpacing(4)

        self._sidebar = QListWidget()
        self._sidebar.setObjectName("SettingsNav")
        self._sidebar.setFrameShape(QFrame.Shape.NoFrame)
        self._sidebar.setIconSize(QSize(16, 16))

        pages = [
            ("AI Provider", "sparkles"),
            ("Hotkeys", "keyboard"),
            ("Appearance", "palette"),
            ("History", "clock"),
            ("About", "info"),
        ]
        for label, icon_kind in pages:
            item = QListWidgetItem(label)
            item.setIcon(_settings_nav_icon(icon_kind))
            self._sidebar.addItem(item)
        self._sidebar.setCurrentRow(0)
        self._sidebar.currentRowChanged.connect(self._on_page_changed)
        sb_layout.addWidget(self._sidebar)
        sb_layout.addSpacing(12)

        # Private & Local Card at the bottom of the sidebar
        promo_card = QFrame()
        promo_card.setObjectName("SidebarPromoCard")
        promo_l = QVBoxLayout(promo_card)
        promo_l.setContentsMargins(12, 12, 12, 12)
        promo_l.setSpacing(6)

        promo_header = QHBoxLayout()
        promo_header.setSpacing(6)
        shield_icon = QLabel()
        shield_icon.setFixedSize(14, 14)
        shield_icon.setPixmap(_paint_settings_icon("shield", "#7C3AED", 14))
        promo_title = QLabel("Private & Local")
        promo_title.setStyleSheet("font-size: 11px; font-weight: 700; color: #7C3AED;")
        promo_header.addWidget(shield_icon)
        promo_header.addWidget(promo_title, 1)

        promo_desc = QLabel("Everything runs locally on your machine. Your data never leaves your device.")
        promo_desc.setStyleSheet("font-size: 10px; color: #6B7280; line-height: 1.3;")
        promo_desc.setWordWrap(True)

        promo_link = QLabel("<a href='#' style='color: #7C3AED; font-weight: 700; text-decoration: none;'>Learn more ></a>")
        promo_link.setStyleSheet("font-size: 10px; font-weight: 700; color: #7C3AED;")

        promo_l.addLayout(promo_header)
        promo_l.addWidget(promo_desc)
        promo_l.addWidget(promo_link)
        sb_layout.addWidget(promo_card)
        sb_layout.addSpacing(8)

        # Footer Row with settings sliders/gear and version tag
        footer = QWidget()
        footer_row = QHBoxLayout(footer)
        footer_row.setContentsMargins(8, 0, 8, 0)
        footer_row.setSpacing(6)

        gear_icon = QLabel()
        gear_icon.setFixedSize(14, 14)
        gear_icon.setPixmap(_paint_settings_icon("sliders", "#9CA3AF", 14))

        ver_lbl = QLabel("v1.0.0")
        ver_lbl.setStyleSheet("font-size: 11px; color: #9CA3AF; font-weight: 500;")

        footer_row.addWidget(gear_icon)
        footer_row.addWidget(ver_lbl)
        footer_row.addStretch()
        sb_layout.addWidget(footer)

        # ── Content stack ─────────────────────────────────────────────────────
        content = QWidget()
        content.setObjectName("SettingsContent")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(16)

        self._stack = QStackedWidget()
        self._stack.addWidget(self._page_ai())
        self._stack.addWidget(self._page_hotkeys())
        self._stack.addWidget(self._page_appearance())
        self._stack.addWidget(self._page_history())
        self._stack.addWidget(self._page_about())

        content_layout.addWidget(self._stack)

        outer.addWidget(sidebar)
        outer.addWidget(content, 1)

        # ── Auto-save connections ─────────────────────────────────────────────
        self._default_mode_combo.currentIndexChanged.connect(self._auto_save)
        self._ollama_host.editingFinished.connect(self._auto_save)
        self._ollama_model_edit.editingFinished.connect(self._auto_save)
        self._hotkey_enabled_cb.toggled.connect(self._auto_save)
        self._hotkey_edit.editingFinished.connect(self._auto_save)
        self._hotkey_raw.editingFinished.connect(self._auto_save)
        self._startup_cb.toggled.connect(self._auto_save)
        self._theme_combo.currentIndexChanged.connect(self._auto_save)
        self._notif_cb.toggled.connect(self._auto_save)

    # ── Pages ─────────────────────────────────────────────────────────────────

    def _page_ai(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(14)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("AI Provider")
        title.setObjectName("SettingsTitle")
        layout.addWidget(title)

        hint = QLabel("Configure how Avelyn connects to your local AI model.")
        hint.setObjectName("SettingsMuted")
        layout.addWidget(hint)

        # 1. Connection Status Card
        conn_row = QWidget()
        conn_l = QHBoxLayout(conn_row)
        conn_l.setContentsMargins(0, 0, 0, 0)
        conn_l.setSpacing(10)

        test_btn = QPushButton("Test Connection")
        test_btn.setObjectName("SecondaryBtn")
        test_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        test_btn.setIcon(QIcon(_paint_settings_icon("wave", "#111827", 14)))
        test_btn.clicked.connect(self._on_test_connection)

        self._status_dot = QLabel("●")
        self._status_dot.setStyleSheet("color: #9CA3AF; font-size: 14px;")
        
        self._test_result = QLabel("Not Tested")
        self._test_result.setObjectName("SettingsMuted")
        self._test_result.setStyleSheet("color: #6B7280; font-size: 12px;")
        
        conn_l.addWidget(self._status_dot)
        conn_l.addWidget(self._test_result, 1)
        conn_l.addWidget(test_btn)

        self._conn_card = _premium_row(
            label_text="Connected",
            sub_label="Avelyn is ready to enhance your writing.",
            icon_kind="check",
            icon_color="#10B981",
            icon_bg_color="#DEF7EC",
            widget=conn_row
        )
        layout.addWidget(_settings_group([self._conn_card]))

        # 2. Default Mode Card
        self._default_mode_combo = QComboBox()
        self._default_mode_combo.setObjectName("SettingsCombo")
        self._mode_keys = [m[2] for m in CommandPalette.MODES]
        display_labels = [m[0] for m in CommandPalette.MODES]
        self._default_mode_combo.addItems(display_labels)
        try:
            mode_idx = self._mode_keys.index(self._settings.default_mode)
        except ValueError:
            mode_idx = 0
        self._default_mode_combo.setCurrentIndex(mode_idx)

        default_mode_card = _premium_row(
            label_text="Default Mode",
            sub_label="This is the default action selected when Avelyn opens.",
            icon_kind="sparkles",
            icon_color="#7C3AED",
            icon_bg_color="#F3EEFF",
            widget=self._default_mode_combo
        )
        layout.addWidget(_settings_group([default_mode_card]))

        # 3. Advanced Settings Block
        adv_btn = QToolButton()
        adv_btn.setObjectName("DisclosureButton")
        adv_btn.setText("▶  Advanced Settings")
        adv_btn.setCheckable(True)
        adv_btn.setChecked(False)
        adv_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        adv_panel = QFrame()
        adv_panel.setObjectName("SettingsCard")
        adv_panel.hide()
        adv_l = QVBoxLayout(adv_panel)
        adv_l.setContentsMargins(0, 4, 0, 4)
        adv_l.setSpacing(0)

        # Provider row
        provider_row = _premium_row(
            label_text="Provider",
            right_text="Ollama (Local)",
            icon_kind="server",
            icon_color="#7C3AED",
            icon_bg_color="#F3EEFF",
            show_arrow=True
        )
        
        # Host row
        self._ollama_host = QLineEdit(self._settings.ollama_host)
        self._ollama_host.setObjectName("SettingsLineEdit")
        self._ollama_host.setFixedWidth(200)
        host_row = _premium_row(
            label_text="Host",
            icon_kind="link",
            icon_color="#7C3AED",
            icon_bg_color="#F3EEFF",
            widget=self._ollama_host,
            show_arrow=True
        )

        # Model row
        self._ollama_model_edit = QLineEdit(self._settings.ollama_model)
        self._ollama_model_edit.setObjectName("SettingsLineEdit")
        self._ollama_model_edit.setPlaceholderText("e.g. gemma3:4b")
        self._ollama_model_edit.setFixedWidth(200)
        model_row = _premium_row(
            label_text="Model",
            icon_kind="cube",
            icon_color="#7C3AED",
            icon_bg_color="#F3EEFF",
            widget=self._ollama_model_edit,
            show_arrow=True
        )

        # Additional options row
        additional_row = _premium_row(
            label_text="Additional Options",
            sub_label="Customize advanced model settings",
            icon_kind="sliders",
            icon_color="#7C3AED",
            icon_bg_color="#F3EEFF",
            show_arrow=True
        )

        adv_l.addWidget(provider_row)
        adv_l.addWidget(_divider_line())
        adv_l.addWidget(host_row)
        adv_l.addWidget(_divider_line())
        adv_l.addWidget(model_row)
        adv_l.addWidget(_divider_line())
        adv_l.addWidget(additional_row)

        def _toggle_adv(checked: bool) -> None:
            adv_btn.setText("▼  Advanced Settings" if checked else "▶  Advanced Settings")
            adv_panel.setVisible(checked)

        adv_btn.toggled.connect(_toggle_adv)

        layout.addWidget(adv_btn)
        layout.addWidget(adv_panel)

        # 4. Footer Banner
        footer_banner_row = _premium_row(
            label_text="100% Local. 100% Private.",
            sub_label="Avelyn never sends your data anywhere. All processing happens on your machine.",
            icon_kind="shield",
            icon_color="#7C3AED",
            icon_bg_color="#F3EEFF"
        )
        layout.addWidget(_settings_group([footer_banner_row]))
        layout.addStretch()
        return w

    def _page_hotkeys(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(14)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Hotkeys")
        title.setObjectName("SettingsTitle")
        layout.addWidget(title)

        hint = QLabel("Configure system-wide keyboard shortcuts for Avelyn.")
        hint.setObjectName("SettingsMuted")
        layout.addWidget(hint)

        # 1. Global Shortcut Card
        preview_row = QWidget()
        preview_l = QHBoxLayout(preview_row)
        preview_l.setContentsMargins(0, 0, 0, 0)
        preview_l.setSpacing(8)

        self._keycap_host = QWidget()
        self._keycap_layout = QHBoxLayout(self._keycap_host)
        self._keycap_layout.setContentsMargins(0, 0, 0, 0)
        self._keycap_layout.setSpacing(6)
        preview_l.addWidget(self._keycap_host, 1)

        self._hotkey_edit = QLineEdit(self._settings.shortcut_display)
        self._hotkey_edit.setObjectName("SettingsLineEdit")
        self._hotkey_edit.setPlaceholderText("Ctrl+Shift+E")
        self._hotkey_edit.setFixedWidth(140)
        preview_l.addWidget(self._hotkey_edit)

        shortcut_card_row = _premium_row(
            label_text="Global Shortcut",
            sub_label="Visual keyboard keycaps representing the current trigger shortcut.",
            icon_kind="keyboard",
            icon_color="#7C3AED",
            icon_bg_color="#F3EEFF",
            widget=preview_row
        )

        self._hotkey_enabled_cb = QCheckBox("Enable Shortcut")
        self._hotkey_enabled_cb.setChecked(self._settings.hotkey_enabled)
        enabled_card_row = _premium_row(
            label_text="Enable global hotkey",
            sub_label="Allows Avelyn to capture your selected text system-wide.",
            icon_kind="shield",
            icon_color="#7C3AED",
            icon_bg_color="#F3EEFF",
            widget=self._hotkey_enabled_cb
        )

        self._startup_cb = QCheckBox("Launch on login")
        self._startup_cb.setChecked(self._settings.launch_at_startup)
        startup_card_row = _premium_row(
            label_text="Launch at system login",
            sub_label="Start Avelyn in your menu bar automatically when you log in.",
            icon_kind="sliders",
            icon_color="#7C3AED",
            icon_bg_color="#F3EEFF",
            widget=self._startup_cb
        )

        layout.addWidget(_settings_group([shortcut_card_row, enabled_card_row, startup_card_row]))

        # Advanced disclosure
        adv_btn = QToolButton()
        adv_btn.setObjectName("DisclosureButton")
        adv_btn.setText("▶  Advanced Hotkey Details")
        adv_btn.setCheckable(True)
        adv_btn.setChecked(False)
        adv_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        adv_panel = QFrame()
        adv_panel.setObjectName("SettingsCard")
        adv_panel.hide()
        adv_l = QVBoxLayout(adv_panel)
        adv_l.setContentsMargins(0, 4, 0, 4)
        adv_l.setSpacing(0)

        self._hotkey_raw = QLineEdit(self._settings.hotkey)
        self._hotkey_raw.setObjectName("SettingsLineEdit")
        self._hotkey_raw.setPlaceholderText("<ctrl>+<shift>+e")
        self._hotkey_raw.setFixedWidth(200)
        
        raw_row = _premium_row(
            label_text="Raw internal hotkey (pynput)",
            sub_label="Leave blank to automatically convert from the display shortcut field.",
            icon_kind="sliders",
            icon_color="#7C3AED",
            icon_bg_color="#F3EEFF",
            widget=self._hotkey_raw
        )
        adv_l.addWidget(raw_row)

        def _toggle_adv(checked: bool) -> None:
            adv_btn.setText("▼  Advanced Hotkey Details" if checked else "▶  Advanced Hotkey Details")
            adv_panel.setVisible(checked)

        adv_btn.toggled.connect(_toggle_adv)
        layout.addWidget(adv_btn)
        layout.addWidget(adv_panel)

        # Keycap preview wiring
        def _to_keycaps(text: str) -> list[str]:
            parts = [p.strip() for p in text.split("+") if p.strip()]
            mapped: list[str] = []
            for ptxt in parts:
                low = ptxt.lower()
                if low in ("ctrl", "control"):
                    mapped.append("⌃")
                elif low in ("shift",):
                    mapped.append("⇧")
                elif low in ("alt", "option"):
                    mapped.append("⌥")
                elif low in ("cmd", "command", "meta"):
                    mapped.append("⌘")
                else:
                    mapped.append(ptxt.upper() if len(ptxt) == 1 else ptxt)
            return mapped or ["⌃", "⇧", "E"]

        def _render_keycaps() -> None:
            while self._keycap_layout.count():
                item = self._keycap_layout.takeAt(0)
                if item and item.widget():
                    item.widget().deleteLater()
            for cap in _to_keycaps(self._hotkey_edit.text()):
                self._keycap_layout.addWidget(_keycap_label(cap))
            self._keycap_layout.addStretch()

        self._hotkey_edit.textChanged.connect(lambda _t: _render_keycaps())
        _render_keycaps()

        layout.addStretch()
        return w

    def _page_appearance(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(14)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Appearance")
        title.setObjectName("SettingsTitle")
        layout.addWidget(title)

        hint = QLabel("Customize the visual style and notifications of Avelyn.")
        hint.setObjectName("SettingsMuted")
        layout.addWidget(hint)

        # 1. Theme Preferences Group
        tc_card = QFrame()
        tc_card.setObjectName("SettingsCard")
        tc_layout = QVBoxLayout(tc_card)
        tc_layout.setContentsMargins(18, 16, 18, 16)
        tc_layout.setSpacing(14)

        tc_title = QLabel("Theme Preferences")
        tc_title.setStyleSheet("font-size: 13px; font-weight: 600; color: #111827;")
        tc_layout.addWidget(tc_title)

        # Keep hidden combo for save compatibility
        self._theme_combo = QComboBox()
        self._theme_combo.setObjectName("SettingsCombo")
        self._theme_combo.addItems(["Dark", "Light"])
        self._theme_combo.setCurrentIndex(0 if self._settings.theme == "dark" else 1)
        self._theme_combo.hide()

        row = QHBoxLayout()
        row.setSpacing(14)

        light_btn = QToolButton()
        light_btn.setObjectName("ThemeCard")
        light_btn.setCheckable(True)
        light_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        light_btn.setIcon(_theme_preview("light"))
        light_btn.setIconSize(QSize(96, 58))
        light_btn.setText("Light Mode")
        light_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        dark_btn = QToolButton()
        dark_btn.setObjectName("ThemeCard")
        dark_btn.setCheckable(True)
        dark_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        dark_btn.setIcon(_theme_preview("dark"))
        dark_btn.setIconSize(QSize(96, 58))
        dark_btn.setText("Dark Mode")
        dark_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        system_btn = QToolButton()
        system_btn.setObjectName("ThemeCard")
        system_btn.setCheckable(False)
        system_btn.setEnabled(False)
        system_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        system_btn.setIcon(_theme_preview("system"))
        system_btn.setIconSize(QSize(96, 58))
        system_btn.setText("System Theme")
        system_btn.setToolTip("System theme is not supported in this build.")

        def _select_theme(mode: str) -> None:
            if mode == "dark":
                dark_btn.setChecked(True)
                light_btn.setChecked(False)
                self._theme_combo.setCurrentIndex(0)
            else:
                light_btn.setChecked(True)
                dark_btn.setChecked(False)
                self._theme_combo.setCurrentIndex(1)

        light_btn.clicked.connect(lambda: _select_theme("light"))
        dark_btn.clicked.connect(lambda: _select_theme("dark"))
        _select_theme(self._settings.theme)

        row.addWidget(light_btn)
        row.addWidget(dark_btn)
        row.addWidget(system_btn)
        row.addStretch()
        tc_layout.addLayout(row)
        layout.addWidget(tc_card)

        # 2. Notifications Group Card
        self._notif_cb = QCheckBox("Show notifications")
        self._notif_cb.setChecked(self._settings.get("show_notifications", True))
        
        notif_row = _premium_row(
            label_text="System Notifications",
            sub_label="Display menu bar notifications for shortcut triggers and updates.",
            icon_kind="info",
            icon_color="#7C3AED",
            icon_bg_color="#F3EEFF",
            widget=self._notif_cb
        )
        layout.addWidget(_settings_group([notif_row]))
        layout.addStretch()
        return w

    def _page_history(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(14)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("History")
        title.setObjectName("SettingsTitle")
        layout.addWidget(title)

        history = self._settings.prompt_history
        if not history:
            empty_w = QWidget()
            empty_l = QVBoxLayout(empty_w)
            empty_l.setContentsMargins(0, 80, 0, 80)
            empty_l.setSpacing(14)

            icon_lbl = QLabel()
            icon_lbl.setFixedSize(64, 64)
            icon_lbl.setStyleSheet("background: #F3EEFF; border-radius: 32px;")
            icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_lbl.setPixmap(_paint_settings_icon("clock", "#7C3AED", 32))
            
            ttl = QLabel("No history yet")
            ttl.setObjectName("SettingsHistoryTitle")
            
            desc = QLabel("Enhancements you apply system-wide will appear here.")
            desc.setObjectName("SettingsMuted")
            desc.setWordWrap(True)
            desc.setAlignment(Qt.AlignmentFlag.AlignCenter)

            empty_l.addWidget(icon_lbl, 0, Qt.AlignmentFlag.AlignCenter)
            empty_l.addWidget(ttl, 0, Qt.AlignmentFlag.AlignCenter)
            empty_l.addWidget(desc, 0, Qt.AlignmentFlag.AlignCenter)
            
            layout.addWidget(empty_w)
            layout.addStretch()
            return w

        self._history_list = QListWidget()
        self._history_list.setObjectName("SettingsHistory")
        for entry in history:
            ts = entry.get("timestamp", "")[:19].replace("T", " ")
            mode = entry.get("mode", "?")
            orig = entry.get("original", "")[:60].replace("\n", " ")
            item = QListWidgetItem(f"[{ts}]  {mode.upper()}  —  {orig}…")
            self._history_list.addItem(item)
        layout.addWidget(self._history_list)

        clear_btn = QPushButton("Clear History")
        clear_btn.setObjectName("SecondaryBtn")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.clicked.connect(self._on_clear_history)
        layout.addWidget(clear_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        return w

    def _page_about(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(14)
        layout.setContentsMargins(0, 40, 0, 40)

        from utils import get_resource_path
        logo_path = get_resource_path("public/logo.png")

        logo = QLabel()
        logo.setFixedSize(56, 56)
        if logo_path.exists():
            pm = QPixmap(str(logo_path))
            if not pm.isNull():
                logo.setPixmap(pm.scaled(56, 56, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            logo.setPixmap(_paint_settings_icon("sparkles", "#7C3AED", 56))

        name = QLabel("Avelyn")
        name.setObjectName("SettingsAboutName")

        version = QLabel("Version 1.0.0")
        version.setObjectName("SettingsAboutVersion")

        desc = QLabel(
            "A premium system-wide writing assistant powered by local AI.\n"
            "Runs entirely locally on your machine for complete speed, privacy, and security."
        )
        desc.setObjectName("SettingsAboutDesc")
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Premium Links Row
        links = QWidget()
        links_l = QHBoxLayout(links)
        links_l.setContentsMargins(0, 16, 0, 0)
        links_l.setSpacing(8)

        def link_btn(label: str, url: str) -> QPushButton:
            b = QPushButton(label)
            b.setObjectName("AboutLink")
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(url)))
            return b

        dot1 = QLabel("·")
        dot1.setStyleSheet("color: #6B7280; font-weight: bold; font-size: 14px;")
        dot2 = QLabel("·")
        dot2.setStyleSheet("color: #6B7280; font-weight: bold; font-size: 14px;")

        links_l.addStretch()
        links_l.addWidget(link_btn("Website", "https://avelyn.app"))
        links_l.addWidget(dot1)
        links_l.addWidget(link_btn("GitHub", "https://github.com/vishwaksen21/Avelyn"))
        links_l.addWidget(dot2)
        links_l.addWidget(link_btn("Privacy Policy", "https://avelyn.app/privacy"))
        links_l.addStretch()

        layout.addWidget(logo, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(links, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        return w

    # ── Slots ─────────────────────────────────────────────────────────────────

    @pyqtSlot(int)
    def _on_page_changed(self, idx: int) -> None:
        self._stack.setCurrentIndex(idx)
        page = self._stack.currentWidget()
        if page is None:
            return
        eff = page.graphicsEffect()
        if eff is None:
            from PyQt6.QtWidgets import QGraphicsOpacityEffect
            eff = QGraphicsOpacityEffect(page)
            page.setGraphicsEffect(eff)
        try:
            eff.setOpacity(0.0)  # type: ignore[attr-defined]
        except Exception:
            return
        anim = QPropertyAnimation(eff, b"opacity", self)
        anim.setDuration(160)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()

    def _auto_save(self) -> None:
        self._settings.set("ai_provider",     "ollama")
        self._settings.set("ollama_host",     self._ollama_host.text().strip())
        self._settings.set("ollama_model",    self._ollama_model_edit.text().strip())
        self._settings.set("default_mode",    self._mode_keys[self._default_mode_combo.currentIndex()])
        self._settings.set("hotkey",          self._hotkey_raw.text().strip() or self._hotkey_edit.text().strip())
        self._settings.set("shortcut_display",self._hotkey_edit.text().strip())
        self._settings.set("hotkey_enabled",  self._hotkey_enabled_cb.isChecked())
        self._settings.set("launch_at_startup", self._startup_cb.isChecked())
        self._settings.set("theme",           "dark" if self._theme_combo.currentIndex() == 0 else "light")
        self._settings.set("show_notifications", self._notif_cb.isChecked())

        from platform_handler import set_launch_at_startup
        set_launch_at_startup(self._startup_cb.isChecked())

        self.settings_changed.emit()

    def _on_test_connection(self) -> None:
        self._test_result.setText("Testing…")
        self._status_dot.setStyleSheet("color: #F59E0B; font-size: 14px;") # Orange dot
        QApplication.processEvents()
        try:
            result = self._processor.test_connection()
            self._test_result.setText(f"Connected — {result[:60]}")
            self._test_result.setStyleSheet("color: #10B981; font-size: 12px; font-weight: 500;")
            self._status_dot.setStyleSheet("color: #10B981; font-size: 14px;") # Green dot
        except Exception as exc:                          # noqa: BLE001
            self._test_result.setText(f"Connection Failed: {exc}")
            self._test_result.setStyleSheet("color: #EF4444; font-size: 12px; font-weight: 500;")
            self._status_dot.setStyleSheet("color: #EF4444; font-size: 14px;") # Red dot

    def _on_clear_history(self) -> None:
        reply = QMessageBox.question(
            self, "Clear History",
            "Are you sure you want to clear all prompt history?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._settings.clear_history()
            self._history_list.clear()
            self._history_list.addItem("History cleared.")


# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM TRAY
# ═══════════════════════════════════════════════════════════════════════════════

class SystemTrayIcon(QSystemTrayIcon):
    """
    Manages the system tray icon, context menu, and notifications.
    Bridges tray actions to the main application.
    """

    open_settings_requested = pyqtSignal()
    quit_requested          = pyqtSignal()
    pause_toggled           = pyqtSignal(bool)   # True = paused

    def __init__(self, settings: Settings, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._settings = settings
        self._paused   = False
        self._build_icon()
        self._build_menu()
        self.activated.connect(self._on_activated)

    def _build_icon(self) -> None:
        """Create a programmatic icon if no icon file is found."""
        from utils import get_resource_path
        icon_path = get_resource_path("assets/icon.png")
        if icon_path.exists():
            self.setIcon(QIcon(str(icon_path)))
        else:
            # Draw a minimal ✦ icon programmatically.
            px = QPixmap(64, 64)
            px.fill(QColor(0, 0, 0, 0))
            p = QPainter(px)
            p.setRenderHint(QPainter.RenderHint.Antialiasing)
            p.setBrush(QColor("#7C3AED"))
            p.setPen(Qt.PenStyle.NoPen)
            # Simple diamond shape.
            path = QPainterPath()
            path.moveTo(32, 4)
            path.lineTo(60, 32)
            path.lineTo(32, 60)
            path.lineTo(4, 32)
            path.closeSubpath()
            p.drawPath(path)
            p.end()
            self.setIcon(QIcon(px))
        self.setToolTip(f"Avelyn — {self._settings.shortcut_display}")

    def _build_menu(self) -> None:
        menu = QMenu()
        menu.setStyleSheet(
            "QMenu { background: #1E1E26; color: #F0F0F8; border: 1px solid #2A2A38; border-radius: 8px; padding: 4px; }"
            "QMenu::item { padding: 8px 18px; border-radius: 6px; }"
            "QMenu::item:selected { background: #2A2A38; }"
        )

        title_act = menu.addAction("✦  Avelyn")
        title_act.setEnabled(False)
        menu.addSeparator()

        status_act = menu.addAction(f"Shortcut: {self._settings.shortcut_display}")
        status_act.setEnabled(False)
        menu.addSeparator()

        self._pause_act = menu.addAction("⏸  Pause")
        self._pause_act.triggered.connect(self._on_pause_toggle)

        settings_act = menu.addAction("⚙  Settings")
        settings_act.triggered.connect(self.open_settings_requested.emit)
        menu.addSeparator()

        quit_act = menu.addAction("✕  Quit")
        quit_act.triggered.connect(self.quit_requested.emit)

        self.setContextMenu(menu)

    def _on_activated(self, reason) -> None:
        if sys.platform == "darwin":
            if reason == QSystemTrayIcon.ActivationReason.Trigger:
                # Single click → open settings on macOS
                self.open_settings_requested.emit()
        else:
            if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
                # Double click → open settings on Windows/Linux
                self.open_settings_requested.emit()

    def _on_pause_toggle(self) -> None:
        self._paused = not self._paused
        self._pause_act.setText("▶  Resume" if self._paused else "⏸  Pause")
        self.pause_toggled.emit(self._paused)
        verb = "paused" if self._paused else "resumed"
        self.showMessage("Avelyn", f"Hotkey {verb}.", QSystemTrayIcon.MessageIcon.Information, 2000)

    def notify(self, title: str, message: str) -> None:
        if self._settings.get("show_notifications", True):
            self.showMessage(title, message, QSystemTrayIcon.MessageIcon.Information, 2500)


# ═══════════════════════════════════════════════════════════════════════════════
# TOAST OVERLAY
# ═══════════════════════════════════════════════════════════════════════════════

from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QGraphicsOpacityEffect
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve

class InstallerOverlay(QWidget):
    """
    Frameless overlay shown during first-run Ollama installation.
    Features: progress bar, status text, success state, error state + retry button.
    Always stays on top; never freezes the event loop.
    """

    retry_requested = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self.resize(400, 170)
        self._center_on_screen()

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)

        card = QFrame()
        card.setObjectName("installerCard")
        card.setStyleSheet("""
            #installerCard {
                background-color: rgba(14, 14, 18, 245);
                border-radius: 14px;
                border: 1px solid rgba(255, 255, 255, 22);
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 160))
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 22, 24, 22)
        card_layout.setSpacing(14)

        self._title = QLabel("Setting up Local AI Engine")
        self._title.setStyleSheet(
            "color: #F0F0F8; font-size: 15px; font-weight: 700; background: transparent;"
        )
        self._title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._progress = QProgressBar()
        self._progress.setRange(0, 100)
        self._progress.setValue(0)
        self._progress.setTextVisible(False)
        self._progress.setFixedHeight(8)
        self._progress.setStyleSheet("""
            QProgressBar {
                background-color: rgba(255, 255, 255, 18);
                border-radius: 4px;
                border: none;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #3b82f6, stop:1 #818cf8);
                border-radius: 4px;
            }
        """)

        self._status = QLabel("Initializing...")
        self._status.setStyleSheet(
            "color: rgba(240,240,248,160); font-size: 12px; background: transparent;"
        )
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status.setWordWrap(True)

        self._note = QLabel("This only happens once.")
        self._note.setStyleSheet(
            "color: rgba(240,240,248,80); font-size: 11px; background: transparent;"
        )
        self._note.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._retry_btn = QPushButton("Retry")
        self._retry_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._retry_btn.setFixedWidth(100)
        self._retry_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444; color: white; border: none;
                border-radius: 8px; padding: 7px 0;
                font-weight: 600; font-size: 13px;
            }
            QPushButton:hover { background-color: #dc2626; }
            QPushButton:pressed { background-color: #b91c1c; }
        """)
        self._retry_btn.hide()
        self._retry_btn.clicked.connect(self.retry_requested.emit)

        card_layout.addWidget(self._title)
        card_layout.addWidget(self._progress)
        card_layout.addWidget(self._status)
        card_layout.addWidget(self._note)
        card_layout.addWidget(self._retry_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        root.addWidget(card)

    def update_progress(self, percent: int, text: str) -> None:
        self._progress.setValue(percent)
        self._status.setText(text)
        self._status.setStyleSheet(
            "color: rgba(240,240,248,160); font-size: 12px; background: transparent;"
        )
        self._progress.show()
        self._retry_btn.hide()
        self._note.show()
        self.repaint()
        QApplication.processEvents()

    def show_error(self, message: str) -> None:
        self._title.setText("Setup Failed")
        self._status.setText(message)
        self._status.setStyleSheet(
            "color: #ef4444; font-size: 12px; background: transparent;"
        )
        self._progress.hide()
        self._note.hide()
        self._retry_btn.show()
        self.repaint()
        QApplication.processEvents()

    def show_success(self) -> None:
        self._title.setText("Ready!")
        self._status.setText("Local AI engine is running.")
        self._status.setStyleSheet(
            "color: #22c55e; font-size: 12px; background: transparent;"
        )
        self._progress.setValue(100)
        self._progress.setStyleSheet("""
            QProgressBar {
                background-color: rgba(255,255,255,18);
                border-radius: 4px; border: none;
            }
            QProgressBar::chunk { background-color: #22c55e; border-radius: 4px; }
        """)
        self._note.hide()
        self._retry_btn.hide()
        self.repaint()
        QApplication.processEvents()

    def _center_on_screen(self) -> None:
        screen = QApplication.primaryScreen()
        if screen:
            geo = screen.geometry()
            self.move(
                geo.x() + (geo.width()  - self.width())  // 2,
                geo.y() + (geo.height() - self.height()) // 2,
            )

    def closeEvent(self, event) -> None:
        """Log and ignore close events — InstallerOverlay must never close during installation."""
        from logger import logger as _log
        _log.critical("INSTALLER OVERLAY RECEIVED CLOSE EVENT")
        super().closeEvent(event)

class ToastOverlay(QWidget):
    """A premium, animated frameless pill overlay to indicate activity."""
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        # Use ToolTip to prevent focus stealing, but force on-top
        self.setWindowFlags(
            Qt.WindowType.ToolTip |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowTransparentForInput |
            Qt.WindowType.BypassWindowManagerHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # The actual pill
        self._pill = QFrame()
        self._pill_layout = QHBoxLayout(self._pill)
        self._pill_layout.setContentsMargins(20, 10, 20, 10)

        
        # Label
        self._lbl = QLabel("✨ Enhancing...")
        self._lbl.setStyleSheet("background: transparent; color: #FFFFFF; font-weight: 600; font-size: 15px;")
        self._pill_layout.addWidget(self._lbl)
        
        # Shadow Effect
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(20)
        self._shadow.setXOffset(0)
        self._shadow.setYOffset(4)
        self._shadow.setColor(QColor(0, 0, 0, 80))
        self._pill.setGraphicsEffect(self._shadow)
        
        layout.addWidget(self._pill)
        
        # Animations
        self._anim_in = QPropertyAnimation(self, b"windowOpacity")
        self._anim_in.setDuration(250)
        self._anim_in.setStartValue(0.0)
        self._anim_in.setEndValue(1.0)
        self._anim_in.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self._anim_out = QPropertyAnimation(self, b"windowOpacity")
        self._anim_out.setDuration(300)
        self._anim_out.setStartValue(1.0)
        self._anim_out.setEndValue(0.0)
        self._anim_out.setEasingCurve(QEasingCurve.Type.InCubic)
        self._anim_out.finished.connect(self.hide)
        
        # Loading dots timer
        self._dot_count = 0
        self._base_text = "✨ Enhancing"
        self._loading_timer = QTimer(self)
        self._loading_timer.setInterval(400)
        self._loading_timer.timeout.connect(self._update_loading_text)
        
        self.hide()
        
    def _update_loading_text(self) -> None:
        self._dot_count = (self._dot_count + 1) % 4
        self._lbl.setText(self._base_text + "." * self._dot_count)
        self.adjustSize()
        
    def show_message(self, text: str, loading: bool = False, success: bool = False, error: bool = False) -> None:
        # Reset state
        self._loading_timer.stop()
        self._anim_in.stop()
        self._anim_out.stop()
        
        if loading:
            self._base_text = text.replace(".", "")
            self._dot_count = 0
            self._lbl.setText(self._base_text)
            self._loading_timer.start()
        else:
            self._lbl.setText(text)
            
        # Anthropic Glassmorphism styling based on state
        if success:
            self._pill.setStyleSheet("background: rgba(84, 160, 113, 0.95); border: 1px solid rgba(0, 0, 0, 0.05); border-radius: 20px;")
            self._shadow.setColor(QColor(84, 160, 113, 60))
        elif error:
            self._pill.setStyleSheet("background: rgba(212, 84, 84, 0.95); border: 1px solid rgba(0, 0, 0, 0.05); border-radius: 20px;")
            self._shadow.setColor(QColor(212, 84, 84, 60))
        else:
            self._pill.setStyleSheet("background: rgba(245, 244, 240, 0.95); border: 1px solid rgba(0, 0, 0, 0.08); border-radius: 20px;")
            self._lbl.setStyleSheet("color: #1A1918; font-weight: 500;")
            self._shadow.setColor(QColor(0, 0, 0, 40))
            
        self.adjustSize()
        
        # Position bottom center
        screen = QApplication.primaryScreen()
        if screen:
            sg = screen.availableGeometry()
            x = sg.x() + (sg.width() - self.width()) // 2
            y = sg.bottom() - 120
            self.move(int(x), int(y))
            
        self.show()
        self.raise_()
        self.repaint()
        
        logger.info("Overlay shown: %s", text)
        
        # Fade in if not fully visible
        if self.windowOpacity() < 1.0:
            self.setWindowOpacity(0.0)
            self._anim_in.start()
            
        # Auto-hide if it's a transient message (success/error)
        if success or error:
            QTimer.singleShot(1500, self._trigger_fade_out)
            
    def _trigger_fade_out(self) -> None:
        self._anim_in.stop()
        self._anim_out.start()


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND PALETTE
# ═══════════════════════════════════════════════════════════════════════════════

class CommandPalette(QWidget):
    """
    A Raycast/Notion AI-grade floating command palette.
    Features:
      - Glassmorphism card with drop shadow
      - Selected-text preview pill at top
      - Live fuzzy search filtering of modes
      - Keyboard navigation (Up/Down/Enter/Escape)
      - Smooth fade + scale-in animation
      - Two-column icon + label rows with keyboard shortcut hints
      - Section grouping (Quick Actions / All Modes)
    """
    action_selected = pyqtSignal(str, str)   # (mode_id, custom_instruction)
    cancelled       = pyqtSignal()
    hidden          = pyqtSignal()            # emitted after hide animation completes

    # ── Mode registry ─────────────────────────────────────────────────────────
    MODES = [
        # (display_label, icon, mode_id, section)
        ("Smart Assist",       "◈", "smart",          "Quick Actions"),
        ("Improve Writing",    "✦", "professional",   "Quick Actions"),
        ("Improve Prompt",     "⌖", "improve_prompt", "Quick Actions"),
        ("Fix Grammar",        "✓", "grammar",         "Quick Actions"),
        ("Engineer Prompt",    "⚙", "engineer_prompt", "All Modes"),
        ("Professional Email", "✉", "email",           "All Modes"),
        ("Engaging Tweet",     "⤹", "tweet",           "All Modes"),
        ("LinkedIn Post",      "≡", "linkedin",        "All Modes"),
        ("Meeting Notes",      "☷", "meeting_notes",  "All Modes"),
        ("Explain like I'm 5","⍰", "eli5",           "All Modes"),
        ("Translate to English","↬","translate",       "All Modes"),
        ("Explain Code",       "⟨⟩","explain_code",   "All Modes"),
        ("Format Resume",      "☑", "resume",          "All Modes"),
        ("Make Shorter",       "◂", "shorten",         "All Modes"),
    ]

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._selected_text: str = ""
        self._visible_modes = list(self.MODES)

        self._build_ui()
        self._build_animations()
        self.hide()

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 20, 20, 20)

        # ── Main card ────────────────────────────────────────────────────────
        self._card = QFrame()
        self._card.setObjectName("paletteCard")
        self._card.setStyleSheet("""
            QFrame#paletteCard {
                background: rgba(252, 251, 248, 0.97);
                border-radius: 16px;
                border: 1px solid rgba(0,0,0,0.07);
            }
        """)

        shadow = QGraphicsDropShadowEffect(self._card)
        shadow.setBlurRadius(50)
        shadow.setXOffset(0)
        shadow.setYOffset(16)
        shadow.setColor(QColor(0, 0, 0, 55))
        self._card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self._card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        # ── Search bar section ───────────────────────────────────────────────
        search_section = QWidget()
        search_section.setStyleSheet("background: transparent;")
        search_layout = QHBoxLayout(search_section)
        search_layout.setContentsMargins(16, 16, 16, 10)
        search_layout.setSpacing(10)

        # Magnifier icon
        search_icon = QLabel("⌕")
        search_icon.setStyleSheet(
            "color: rgba(100,95,90,0.7); font-size: 18px; background: transparent;"
        )
        search_icon.setFixedWidth(22)

        # Input field
        self._input = QLineEdit()
        self._input.setPlaceholderText("Ask AI or search actions...")
        self._input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                font-size: 15px;
                font-weight: 500;
                color: #1A1918;
                padding: 2px 0;
            }
            QLineEdit::placeholder {
                color: rgba(100,95,90,0.5);
            }
        """)
        self._input.textChanged.connect(self._on_search_changed)

        # Keyboard shortcut badge
        esc_badge = QLabel("Esc to close")
        esc_badge.setStyleSheet("""
            color: rgba(100,95,90,0.45);
            font-size: 11px;
            background: rgba(0,0,0,0.05);
            border-radius: 5px;
            padding: 3px 7px;
        """)

        search_layout.addWidget(search_icon)
        search_layout.addWidget(self._input, 1)
        search_layout.addWidget(esc_badge)
        card_layout.addWidget(search_section)

        # ── Divider ──────────────────────────────────────────────────────────
        self._divider = QFrame()
        self._divider.setFrameShape(QFrame.Shape.HLine)
        self._divider.setStyleSheet("background: rgba(0,0,0,0.06); max-height: 1px;")
        card_layout.addWidget(self._divider)

        # ── Selected text preview ────────────────────────────────────────────
        self._preview_widget = QWidget()
        self._preview_widget.setStyleSheet(
            "background: rgba(217,119,87,0.08); border-bottom: 1px solid rgba(0,0,0,0.05);"
        )
        preview_layout = QHBoxLayout(self._preview_widget)
        preview_layout.setContentsMargins(16, 8, 16, 8)
        preview_layout.setSpacing(8)

        preview_icon = QLabel("↳")
        preview_icon.setStyleSheet(
            "color: #D97757; font-size: 13px; background: transparent;"
        )
        preview_icon.setFixedWidth(14)

        self._preview_label = QLabel()
        self._preview_label.setStyleSheet(
            "color: rgba(100,95,90,0.75); font-size: 12px; "
            "font-style: italic; background: transparent;"
        )
        self._preview_label.setWordWrap(False)

        preview_layout.addWidget(preview_icon)
        preview_layout.addWidget(self._preview_label, 1)
        self._preview_widget.hide()
        card_layout.addWidget(self._preview_widget)

        # ── Action list ──────────────────────────────────────────────────────
        list_container = QWidget()
        list_container.setStyleSheet("background: transparent;")
        list_container_layout = QVBoxLayout(list_container)
        list_container_layout.setContentsMargins(8, 6, 8, 10)
        list_container_layout.setSpacing(0)

        self._list = QListWidget()
        self._list.setObjectName("paletteList")
        self._list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._list.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                border-radius: 8px;
                padding: 0;
                margin: 1px 0;
                background: transparent;
            }
            QListWidget::item:selected {
                background: transparent;
            }
        """)

        self._list.itemDoubleClicked.connect(self._accept)
        self._list.itemClicked.connect(self._accept)
        list_container_layout.addWidget(self._list)
        card_layout.addWidget(list_container)

        # ── Footer ───────────────────────────────────────────────────────────
        footer = QWidget()
        footer.setStyleSheet(
            "background: rgba(0,0,0,0.025); border-top: 1px solid rgba(0,0,0,0.05);"
            "border-bottom-left-radius: 16px; border-bottom-right-radius: 16px;"
        )
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(16, 7, 16, 7)

        nav_hint = QLabel("↑↓ navigate   ⏎ confirm   Type to filter")
        nav_hint.setStyleSheet(
            "color: rgba(100,95,90,0.4); font-size: 11px; background: transparent;"
        )

        powered = QLabel("Powered by Ollama")
        powered.setStyleSheet(
            "color: rgba(100,95,90,0.3); font-size: 11px; background: transparent;"
        )

        footer_layout.addWidget(nav_hint)
        footer_layout.addStretch()
        footer_layout.addWidget(powered)
        card_layout.addWidget(footer)

        outer.addWidget(self._card)
        self._input.installEventFilter(self)
        self._populate_list()

    def _build_animations(self) -> None:
        from PyQt6.QtCore import QParallelAnimationGroup, QRect

        # ── Fade in ──────────────────────────────────────────────────────────
        self._fade_in = QPropertyAnimation(self, b"windowOpacity")
        self._fade_in.setDuration(200)
        self._fade_in.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._fade_in.setStartValue(0.0)
        self._fade_in.setEndValue(1.0)

        # ── Fade out ─────────────────────────────────────────────────────────
        self._fade_out = QPropertyAnimation(self, b"windowOpacity")
        self._fade_out.setDuration(130)
        self._fade_out.setEasingCurve(QEasingCurve.Type.InCubic)
        self._fade_out.setStartValue(1.0)
        self._fade_out.setEndValue(0.0)
        self._fade_out.finished.connect(self._on_fully_hidden)

        # ── Geometry slide-up (pos animation) ────────────────────────────────
        self._slide_in  = QPropertyAnimation(self, b"pos")
        self._slide_in.setDuration(200)
        self._slide_in.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._slide_out = QPropertyAnimation(self, b"pos")
        self._slide_out.setDuration(130)
        self._slide_out.setEasingCurve(QEasingCurve.Type.InCubic)

        # Convenience aliases used by old code paths
        self._anim_in  = self._fade_in
        self._anim_out = self._fade_out

    # ── List population ───────────────────────────────────────────────────────

    def _make_section_header(self, text: str) -> QListWidgetItem:
        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, "__header__")
        item.setFlags(Qt.ItemFlag.NoItemFlags)

        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(8, 6, 8, 2)

        label = QLabel(text.upper())
        label.setStyleSheet(
            "color: rgba(100,95,90,0.45); font-size: 10px; "
            "font-weight: 700; letter-spacing: 1px; background: transparent;"
        )
        layout.addWidget(label)
        layout.addStretch()

        item.setSizeHint(QSize(0, 28))
        return item, widget

    def _make_mode_item(self, label: str, icon: str, mode_id: str, selected: bool = False) -> tuple:
        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, mode_id)

        widget = QWidget()
        bg = "rgba(217,119,87,0.12)" if selected else "transparent"
        widget.setStyleSheet(f"background: {bg}; border-radius: 8px;")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 7, 10, 7)
        layout.setSpacing(10)

        # Icon badge
        icon_label = QLabel(icon)
        icon_label.setFixedSize(28, 28)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(
            "color: #D97757; font-size: 14px; "
            "background: rgba(217,119,87,0.1); border-radius: 6px;"
        )

        # Label
        text_label = QLabel(label)
        weight = "600" if selected else "400"
        color = "#1A1918" if selected else "#2A2725"
        text_label.setStyleSheet(
            f"color: {color}; font-size: 13px; font-weight: {weight}; background: transparent;"
        )

        # Enter hint (only on selected)
        enter_hint = QLabel("⏎")
        enter_hint.setStyleSheet(
            "color: rgba(100,95,90,0.35); font-size: 12px; background: transparent;"
        )
        enter_hint.setVisible(selected)

        layout.addWidget(icon_label)
        layout.addWidget(text_label, 1)
        layout.addWidget(enter_hint)

        item.setSizeHint(QSize(0, 44))
        return item, widget

    def _populate_list(self) -> None:
        self._list.clear()
        current_section = None

        for i, (label, icon, mode_id, section) in enumerate(self._visible_modes):
            # Section header
            if section != current_section:
                h_item, h_widget = self._make_section_header(section)
                self._list.addItem(h_item)
                self._list.setItemWidget(h_item, h_widget)
                current_section = section

            selected = (self._list.count() == 1 and i == 0) or False
            m_item, m_widget = self._make_mode_item(label, icon, mode_id, selected)
            self._list.addItem(m_item)
            self._list.setItemWidget(m_item, m_widget)

        # Select first real (non-header) item
        self._select_first_real_item()

    def _select_first_real_item(self) -> None:
        for i in range(self._list.count()):
            item = self._list.item(i)
            if item and item.data(Qt.ItemDataRole.UserRole) != "__header__":
                self._list.setCurrentItem(item)
                self._update_item_highlight(i, True)
                return

    def _update_item_highlight(self, row: int, selected: bool) -> None:
        item = self._list.item(row)
        if not item or item.data(Qt.ItemDataRole.UserRole) == "__header__":
            return
        widget = self._list.itemWidget(item)
        if not widget:
            return
        bg = "rgba(217,119,87,0.12)" if selected else "transparent"
        widget.setStyleSheet(f"background: {bg}; border-radius: 8px;")
        # Update child labels
        layout = widget.layout()
        if layout and layout.count() >= 3:
            # icon, text_label, enter_hint
            text_w = layout.itemAt(1).widget()
            enter_w = layout.itemAt(2).widget()
            if text_w:
                weight = "600" if selected else "400"
                color = "#1A1918" if selected else "#2A2725"
                text_w.setStyleSheet(
                    f"color: {color}; font-size: 13px; font-weight: {weight}; background: transparent;"
                )
            if enter_w:
                enter_w.setVisible(selected)

    # ── Public API ────────────────────────────────────────────────────────────

    def show_palette(self, selected_text: str = "") -> None:
        self._selected_text = selected_text
        self._input.clear()
        self._visible_modes = list(self.MODES)
        self._populate_list()

        # Preview selected text
        if selected_text:
            preview = selected_text.strip()
            if len(preview) > 60:
                preview = preview[:57] + "..."
            self._preview_label.setText('\u201c' + preview + '\u201d')
            self._preview_widget.show()
        else:
            self._preview_widget.hide()

        # Size & center
        self.resize(580, 440)
        screen = QApplication.primaryScreen()
        if screen:
            sg = screen.availableGeometry()
            x = sg.x() + (sg.width()  - self.width())  // 2
            y = sg.y() + (sg.height() - self.height())  // 3
            self.move(int(x), int(y))

        # Position: start 18px lower, slide up to final position
        final_y = int(y)
        start_y = final_y + 18
        self.move(int(x), start_y)

        self.setWindowOpacity(0.0)
        self.show()
        self.raise_()
        self.activateWindow()
        self._input.setFocus()

        # Slide-up destination
        from PyQt6.QtCore import QPoint
        self._slide_in.setStartValue(QPoint(int(x), start_y))
        self._slide_in.setEndValue(QPoint(int(x), final_y))
        self._fade_in.start()
        self._slide_in.start()

    def hide_palette(self) -> None:
        self._fade_in.stop()
        self._slide_in.stop()
        # Slide down while fading out
        from PyQt6.QtCore import QPoint
        cur = self.pos()
        self._slide_out.setStartValue(cur)
        self._slide_out.setEndValue(QPoint(cur.x(), cur.y() + 12))
        self._fade_out.start()
        self._slide_out.start()

    def _on_fully_hidden(self) -> None:
        self.hide()
        self.hidden.emit()

    # ── Interaction ───────────────────────────────────────────────────────────

    def _on_search_changed(self, text: str) -> None:
        query = text.strip().lower()
        if query:
            self._visible_modes = [
                m for m in self.MODES
                if query in m[0].lower() or query in m[2].lower()
            ]
        else:
            self._visible_modes = list(self.MODES)
        self._populate_list()

    def _current_real_row(self) -> int:
        """Return index of currently selected non-header row."""
        return self._list.currentRow()

    def _move_selection(self, direction: int) -> None:
        current = self._list.currentRow()
        self._update_item_highlight(current, False)

        count = self._list.count()
        new_row = current
        for _ in range(count):
            new_row = (new_row + direction) % count
            item = self._list.item(new_row)
            if item and item.data(Qt.ItemDataRole.UserRole) != "__header__":
                break

        self._list.setCurrentRow(new_row)
        self._update_item_highlight(new_row, True)
        self._list.scrollToItem(self._list.item(new_row))

    def _accept(self) -> None:
        custom_instr = self._input.text().strip()
        if custom_instr and not any(
            custom_instr.lower() in m[0].lower() for m in self.MODES
        ):
            self.action_selected.emit("custom", custom_instr)
        else:
            row = self._list.currentRow()
            item = self._list.item(row)
            if item:
                mode_id = item.data(Qt.ItemDataRole.UserRole)
                if mode_id and mode_id != "__header__":
                    self.action_selected.emit(mode_id, "")
        self.hide_palette()

    def eventFilter(self, obj: QObject, event) -> bool:
        if obj == self._input and event.type() == event.Type.KeyPress:
            key = event.key()
            if key == Qt.Key.Key_Up:
                self._move_selection(-1)
                return True
            elif key == Qt.Key.Key_Down:
                self._move_selection(1)
                return True
            elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                self._accept()
                return True
            elif key == Qt.Key.Key_Escape:
                self.cancelled.emit()
                self.hide_palette()
                return True
        return super().eventFilter(obj, event)
