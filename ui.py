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
    QMessageBox, QPushButton, QScrollArea, QSizePolicy,
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

QDialog, QWidget { background: #0D0D0F; color: #F0F0F8; }

QLabel { color: #F0F0F8; background: transparent; }

/* ── Scrollbars ─────────────────────────────────────────── */
QScrollBar:vertical { background: #16161B; width: 6px; border-radius: 3px; }
QScrollBar::handle:vertical { background: #2A2A38; border-radius: 3px; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #7C3AED; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: #16161B; height: 6px; border-radius: 3px; }
QScrollBar::handle:horizontal { background: #2A2A38; border-radius: 3px; }
QScrollBar::handle:horizontal:hover { background: #7C3AED; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

/* ── Buttons ────────────────────────────────────────────── */
QPushButton {
    background: #1E1E26; color: #F0F0F8;
    border: 1px solid #2A2A38; border-radius: 8px;
    padding: 8px 18px; font-size: 13px; font-weight: 500;
}
QPushButton:hover { background: #2A2A38; border-color: #7C3AED; }
QPushButton:pressed { background: #16161B; }
QPushButton:disabled { color: #4A4A5A; border-color: #1E1E26; }

QPushButton#replaceBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7C3AED, stop:1 #5B21B6);
    border: none; color: #FFFFFF; font-weight: 600;
    padding: 9px 24px; border-radius: 8px;
}
QPushButton#replaceBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #6D28D9, stop:1 #4C1D95);
}
QPushButton#replaceBtn:disabled { background: #2A2A38; color: #4A4A5A; }

QPushButton#cancelBtn { color: #9090A8; }
QPushButton#cancelBtn:hover { color: #F0F0F8; border-color: #EF4444; }

QPushButton#undoBtn { color: #9090A8; }
QPushButton#undoBtn:hover { color: #F0F0F8; border-color: #10B981; }

QPushButton#settingsSaveBtn {
    background: #7C3AED; border: none; color: #FFF;
    font-weight: 600; padding: 9px 24px; border-radius: 8px;
}
QPushButton#settingsSaveBtn:hover { background: #6D28D9; }

QPushButton#testBtn { color: #7C3AED; border-color: #7C3AED; }
QPushButton#testBtn:hover { background: #1A1025; }

/* ── Text areas ─────────────────────────────────────────── */
QTextEdit {
    background: #16161B; color: #F0F0F8;
    border: 1px solid #2A2A38; border-radius: 10px;
    padding: 14px; font-size: 14px; line-height: 1.6;
    selection-background-color: #7C3AED40;
}
QTextEdit:focus { border-color: #7C3AED; }

/* ── Line edits ─────────────────────────────────────────── */
QLineEdit {
    background: #16161B; color: #F0F0F8;
    border: 1px solid #2A2A38; border-radius: 8px;
    padding: 8px 12px; font-size: 13px;
}
QLineEdit:focus { border-color: #7C3AED; }

/* ── Combo boxes ────────────────────────────────────────── */
QComboBox {
    background: #16161B; color: #F0F0F8;
    border: 1px solid #2A2A38; border-radius: 8px;
    padding: 7px 12px; font-size: 13px;
}
QComboBox:hover { border-color: #7C3AED; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox QAbstractItemView {
    background: #1E1E26; border: 1px solid #2A2A38; color: #F0F0F8;
    selection-background-color: #7C3AED; outline: none;
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


def get_qss(theme: str) -> str:
    return DARK_QSS if theme == "dark" else LIGHT_QSS


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
        parent: Optional[QObject] = None,
    ) -> None:
        super().__init__(parent)
        self._processor = processor
        self._text = text
        self._mode = mode
        self._full_result = ""

    def run(self) -> None:
        try:
            for chunk in self._processor.enhance(self._text, self._mode):
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
        title_lbl = QLabel("TextPolish")
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
        self.setWindowTitle("TextPolish — Settings")
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
        sidebar.setFixedWidth(180)
        sidebar.setStyleSheet(
            "background: #13131A; border-right: 1px solid #2A2A38;" if self._settings.theme == "dark"
            else "background: #F0F0F5; border-right: 1px solid #D1D1D6;"
        )
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(12, 20, 12, 20)
        sb_layout.setSpacing(4)

        logo_lbl = QLabel("✦  TextPolish")
        logo_lbl.setStyleSheet(
            "color: #7C3AED; font-size: 15px; font-weight: 700; background: transparent;"
        )
        sb_layout.addWidget(logo_lbl)
        sb_layout.addSpacing(16)

        self._sidebar = QListWidget()
        self._sidebar.setFrameShape(QFrame.Shape.NoFrame)
        self._sidebar.setStyleSheet(
            "QListWidget { background: transparent; border: none; }"
            "QListWidget::item { padding: 10px 12px; border-radius: 8px; color: #9090A8; }"
            "QListWidget::item:selected { background: #2A1F4A; color: #A78BFA; }"
            "QListWidget::item:hover:!selected { background: #1E1E26; color: #F0F0F8; }"
        )
        pages = ["🤖  AI Provider", "⌨  Hotkeys", "🎨  Appearance", "📜  History", "ℹ  About"]
        for page in pages:
            self._sidebar.addItem(page)
        self._sidebar.setCurrentRow(0)
        self._sidebar.currentRowChanged.connect(self._on_page_changed)
        sb_layout.addWidget(self._sidebar)
        sb_layout.addStretch()

        ver_lbl = QLabel("v1.0.0")
        ver_lbl.setStyleSheet("color: #4A4A5A; font-size: 11px; background: transparent;")
        sb_layout.addWidget(ver_lbl)

        # ── Content stack ─────────────────────────────────────────────────────
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(28, 24, 28, 24)
        content_layout.setSpacing(16)

        self._stack = QStackedWidget()
        self._stack.addWidget(self._page_ai())
        self._stack.addWidget(self._page_hotkeys())
        self._stack.addWidget(self._page_appearance())
        self._stack.addWidget(self._page_history())
        self._stack.addWidget(self._page_about())

        # Save / Close buttons
        btn_row = QHBoxLayout()
        save_btn = QPushButton("Save Changes")
        save_btn.setObjectName("settingsSaveBtn")
        save_btn.clicked.connect(self._on_save)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        btn_row.addStretch()
        btn_row.addWidget(close_btn)
        btn_row.addWidget(save_btn)

        content_layout.addWidget(self._stack)
        content_layout.addLayout(btn_row)

        outer.addWidget(sidebar)
        outer.addWidget(content, 1)

    # ── Pages ─────────────────────────────────────────────────────────────────

    def _page_ai(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel("AI Provider")
        lbl.setStyleSheet("font-size: 20px; font-weight: 700; color: #F0F0F8; background: transparent;")
        layout.addWidget(lbl)

        # Provider selector
        grp = QGroupBox("Provider")
        grp_layout = QFormLayout(grp)
        
        lbl_provider = QLabel("Ollama (Local Offline)")
        lbl_provider.setStyleSheet("color: #7C3AED; font-weight: 600;")
        grp_layout.addRow("Backend:", lbl_provider)

        self._default_mode_combo = QComboBox()
        self._default_mode_combo.addItems(["Professional", "Creative", "Technical", "Concise", "Academic"])
        mode_idx = list(MODE_PROMPTS.keys()).index(self._settings.default_mode) if self._settings.default_mode in MODE_PROMPTS else 0
        self._default_mode_combo.setCurrentIndex(mode_idx)
        grp_layout.addRow("Default mode:", self._default_mode_combo)
        layout.addWidget(grp)

        # Ollama Configuration
        ollama_grp = QGroupBox("Ollama Settings")
        ol_layout = QFormLayout(ollama_grp)
        self._ollama_host = QLineEdit(self._settings.ollama_host)
        self._ollama_model_edit = QLineEdit(self._settings.ollama_model)
        self._ollama_model_edit.setPlaceholderText("e.g. gemma3:4b, mistral, llama3")
        ol_layout.addRow("Host:", self._ollama_host)
        ol_layout.addRow("Model:", self._ollama_model_edit)
        layout.addWidget(ollama_grp)

        # Test connection
        test_btn = QPushButton("Test Connection")
        test_btn.setObjectName("testBtn")
        self._test_result = QLabel("")
        self._test_result.setStyleSheet("color: #10B981; background: transparent; font-size: 12px;")
        self._test_result.setWordWrap(True)
        test_btn.clicked.connect(self._on_test_connection)

        btn_row = QHBoxLayout()
        btn_row.addWidget(test_btn)
        btn_row.addWidget(self._test_result)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        layout.addStretch()
        return w

    def _page_hotkeys(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel("Hotkeys")
        lbl.setStyleSheet("font-size: 20px; font-weight: 700; color: #F0F0F8; background: transparent;")
        layout.addWidget(lbl)

        grp = QGroupBox("Global Shortcut")
        g_layout = QFormLayout(grp)

        self._hotkey_edit = QLineEdit(self._settings.shortcut_display)
        self._hotkey_edit.setPlaceholderText("e.g. Ctrl+Shift+E")
        hint = QLabel("Use standard key names: Ctrl, Alt, Shift, Cmd (macOS)\nExample: Ctrl+Shift+E")
        hint.setStyleSheet("color: #9090A8; font-size: 11px; background: transparent;")
        hint.setWordWrap(True)

        self._hotkey_raw = QLineEdit(self._settings.hotkey)
        self._hotkey_raw.setPlaceholderText("pynput format: <ctrl>+<shift>+e")
        raw_hint = QLabel("pynput format used internally. Leave blank to auto-convert from above.")
        raw_hint.setStyleSheet("color: #9090A8; font-size: 11px; background: transparent;")

        g_layout.addRow("Display label:", self._hotkey_edit)
        g_layout.addRow("", hint)
        g_layout.addRow("Raw pynput key:", self._hotkey_raw)
        g_layout.addRow("", raw_hint)

        self._hotkey_enabled_cb = QCheckBox("Enable global hotkey")
        self._hotkey_enabled_cb.setChecked(self._settings.hotkey_enabled)
        g_layout.addRow("", self._hotkey_enabled_cb)

        layout.addWidget(grp)

        startup_grp = QGroupBox("Startup")
        s_layout = QFormLayout(startup_grp)
        self._startup_cb = QCheckBox("Launch TextPolish at system login")
        self._startup_cb.setChecked(self._settings.launch_at_startup)
        s_layout.addRow("", self._startup_cb)
        layout.addWidget(startup_grp)

        layout.addStretch()
        return w

    def _page_appearance(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel("Appearance")
        lbl.setStyleSheet("font-size: 20px; font-weight: 700; color: #F0F0F8; background: transparent;")
        layout.addWidget(lbl)

        grp = QGroupBox("Theme")
        g_layout = QFormLayout(grp)
        self._theme_combo = QComboBox()
        self._theme_combo.addItems(["Dark", "Light"])
        self._theme_combo.setCurrentIndex(0 if self._settings.theme == "dark" else 1)
        g_layout.addRow("Color theme:", self._theme_combo)

        self._notif_cb = QCheckBox("Show system notifications")
        self._notif_cb.setChecked(self._settings.get("show_notifications", True))
        g_layout.addRow("", self._notif_cb)
        layout.addWidget(grp)
        layout.addStretch()
        return w

    def _page_history(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel("Prompt History")
        lbl.setStyleSheet("font-size: 20px; font-weight: 700; color: #F0F0F8; background: transparent;")
        layout.addWidget(lbl)

        self._history_list = QListWidget()
        history = self._settings.prompt_history
        if history:
            for entry in history:
                ts   = entry.get("timestamp", "")[:19].replace("T", " ")
                mode = entry.get("mode", "?")
                orig = entry.get("original", "")[:60].replace("\n", " ")
                item = QListWidgetItem(f"[{ts}]  {mode.upper()}  —  {orig}…")
                self._history_list.addItem(item)
        else:
            self._history_list.addItem("No history yet.")

        layout.addWidget(self._history_list)

        clear_btn = QPushButton("Clear History")
        clear_btn.setObjectName("cancelBtn")
        clear_btn.clicked.connect(self._on_clear_history)
        layout.addWidget(clear_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        return w

    def _page_about(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        logo = QLabel("✦  TextPolish")
        logo.setStyleSheet("color: #7C3AED; font-size: 28px; font-weight: 800; background: transparent;")
        desc = QLabel(
            "A cross-platform AI productivity assistant that enhances selected text\n"
            "system-wide with a single keyboard shortcut.\n\n"
            "Supports Gemini, OpenAI, and Ollama (offline).\n\n"
            "Version 1.0.0 • MIT License\n"
            "Built with Python, PyQt6, pynput, and pyperclip."
        )
        desc.setStyleSheet("color: #9090A8; font-size: 13px; line-height: 1.6; background: transparent;")
        desc.setWordWrap(True)

        layout.addWidget(logo)
        layout.addSpacing(8)
        layout.addWidget(desc)
        layout.addStretch()
        return w

    # ── Slots ─────────────────────────────────────────────────────────────────

    @pyqtSlot(int)
    def _on_page_changed(self, idx: int) -> None:
        self._stack.setCurrentIndex(idx)

    def _on_save(self) -> None:
        self._settings.set("ai_provider",     "ollama")
        self._settings.set("ollama_host",     self._ollama_host.text().strip())
        self._settings.set("ollama_model",    self._ollama_model_edit.text().strip())
        self._settings.set("default_mode",    list(MODE_PROMPTS.keys())[self._default_mode_combo.currentIndex()])
        self._settings.set("hotkey",          self._hotkey_raw.text().strip() or self._hotkey_edit.text().strip())
        self._settings.set("shortcut_display",self._hotkey_edit.text().strip())
        self._settings.set("hotkey_enabled",  self._hotkey_enabled_cb.isChecked())
        self._settings.set("launch_at_startup", self._startup_cb.isChecked())
        self._settings.set("theme",           "dark" if self._theme_combo.currentIndex() == 0 else "light")
        self._settings.set("show_notifications", self._notif_cb.isChecked())

        from platform_handler import set_launch_at_startup
        set_launch_at_startup(self._startup_cb.isChecked())

        self.settings_changed.emit()
        QMessageBox.information(self, "Saved", "Settings saved successfully.")

    def _on_test_connection(self) -> None:
        self._test_result.setText("Testing…")
        self._test_result.setStyleSheet("color: #9090A8; background: transparent; font-size: 12px;")
        QApplication.processEvents()
        try:
            result = self._processor.test_connection()
            self._test_result.setText(f"✓ {result[:80]}")
            self._test_result.setStyleSheet("color: #10B981; background: transparent; font-size: 12px;")
        except Exception as exc:                          # noqa: BLE001
            self._test_result.setText(f"✗ {exc}")
            self._test_result.setStyleSheet("color: #EF4444; background: transparent; font-size: 12px;")

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
        icon_path = __import__("pathlib").Path(__file__).parent / "assets" / "icon.png"
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
        self.setToolTip(f"TextPolish — {self._settings.shortcut_display}")

    def _build_menu(self) -> None:
        menu = QMenu()
        menu.setStyleSheet(
            "QMenu { background: #1E1E26; color: #F0F0F8; border: 1px solid #2A2A38; border-radius: 8px; padding: 4px; }"
            "QMenu::item { padding: 8px 18px; border-radius: 6px; }"
            "QMenu::item:selected { background: #2A2A38; }"
        )

        title_act = menu.addAction("✦  TextPolish")
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
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            # Single click → open settings on macOS, double-click on Windows.
            self.open_settings_requested.emit()

    def _on_pause_toggle(self) -> None:
        self._paused = not self._paused
        self._pause_act.setText("▶  Resume" if self._paused else "⏸  Pause")
        self.pause_toggled.emit(self._paused)
        verb = "paused" if self._paused else "resumed"
        self.showMessage("TextPolish", f"Hotkey {verb}.", QSystemTrayIcon.MessageIcon.Information, 2000)

    def notify(self, title: str, message: str) -> None:
        if self._settings.get("show_notifications", True):
            self.showMessage(title, message, QSystemTrayIcon.MessageIcon.Information, 2500)


# ═══════════════════════════════════════════════════════════════════════════════
# TOAST OVERLAY
# ═══════════════════════════════════════════════════════════════════════════════

from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QGraphicsOpacityEffect
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve

class ToastOverlay(QWidget):
    """A premium, animated frameless pill overlay to indicate activity."""
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        # Use ToolTip to prevent focus stealing
        self.setWindowFlags(
            Qt.WindowType.ToolTip |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowTransparentForInput
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
        self._anim_out.stop()
        
        if loading:
            self._base_text = text.replace(".", "")
            self._dot_count = 0
            self._lbl.setText(self._base_text)
            self._loading_timer.start()
        else:
            self._lbl.setText(text)
            
        # Glassmorphism styling based on state
        if success:
            self._pill.setStyleSheet("background: rgba(16, 185, 129, 0.95); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 20px;")
            self._shadow.setColor(QColor(16, 185, 129, 60))
        elif error:
            self._pill.setStyleSheet("background: rgba(239, 68, 68, 0.95); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 20px;")
            self._shadow.setColor(QColor(239, 68, 68, 60))
        else:
            self._pill.setStyleSheet("background: rgba(30, 30, 32, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px;")
            self._shadow.setColor(QColor(0, 0, 0, 100))
            
        self.adjustSize()
        
        # Position bottom center
        screen = QApplication.primaryScreen()
        if screen:
            sg = screen.availableGeometry()
            x = sg.x() + (sg.width() - self.width()) // 2
            y = sg.bottom() - 120
            self.move(int(x), int(y))
            
        # Fade in if not fully visible
        if self.windowOpacity() < 1.0:
            self.setWindowOpacity(0.0)
            self.show()
            self.raise_()
            self._anim_in.start()
            
        # Auto-hide if it's a transient message (success/error)
        if success or error:
            QTimer.singleShot(1500, self._trigger_fade_out)
            
    def _trigger_fade_out(self) -> None:
        self._anim_in.stop()
        self._anim_out.start()
