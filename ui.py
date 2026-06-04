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

LIGHT_TOKENS = {
    "PRIMARY": "#7C3AED",
    "PRIMARY_HOVER": "#6D28D9",
    "PRIMARY_LIGHT": "#EDE9FE",
    "PRIMARY_BORDER": "#D8B4FE",
    "PRIMARY_HOVER_BG": "rgba(124, 58, 237, 0.05)",
    "PRIMARY_HOVER_BORDER": "rgba(124, 58, 237, 0.10)",
    "TEXT_PRIMARY": "#0F172A",
    "TEXT_SECONDARY": "#64748B",
    "SURFACE": "#FFFFFF",
    "SURFACE_ALT": "#F8FAFC",
    "BORDER": "#E2E8F0",
    "BORDER_ALT": "#CBD5E1",
    # Status badges
    "STATUS_TESTING_BG": "#FEF3C7",
    "STATUS_TESTING_TEXT": "#92400E",
    "STATUS_TESTING_BORDER": "#FDE68A",
    "STATUS_CONNECTED_BG": "#DEF7EC",
    "STATUS_CONNECTED_TEXT": "#03543F",
    "STATUS_CONNECTED_BORDER": "#BCF0DA",
    "STATUS_FAILED_BG": "#FDE8E8",
    "STATUS_FAILED_TEXT": "#9B1C1C",
    "STATUS_FAILED_BORDER": "#FBD5D5",
}

DARK_TOKENS = {
    "PRIMARY": "#A78BFA",            # Lighter violet for dark mode readability
    "PRIMARY_HOVER": "#C084FC",      # Bright violet on hover
    "PRIMARY_LIGHT": "#2E1065",      # Deep purple selection background
    "PRIMARY_BORDER": "#6D28D9",     # Border purple
    "PRIMARY_HOVER_BG": "rgba(167, 139, 250, 0.05)",
    "PRIMARY_HOVER_BORDER": "rgba(167, 139, 250, 0.10)",
    "TEXT_PRIMARY": "#F8FAFC",       # Slate white text
    "TEXT_SECONDARY": "#94A3B8",     # Slate gray text
    "SURFACE": "#0B0A0F",            # Deep black/purple surface
    "SURFACE_ALT": "#16151A",        # Slightly lighter black/purple surface
    "BORDER": "#2E2A38",             # Dark purple/gray border
    "BORDER_ALT": "#3E384D",
    # Status badges (beautiful dark mode colors)
    "STATUS_TESTING_BG": "#78350F",
    "STATUS_TESTING_TEXT": "#FDE68A",
    "STATUS_TESTING_BORDER": "#D97706",
    "STATUS_CONNECTED_BG": "#064E3B",
    "STATUS_CONNECTED_TEXT": "#6EE7B7",
    "STATUS_CONNECTED_BORDER": "#059669",
    "STATUS_FAILED_BG": "#7F1D1D",
    "STATUS_FAILED_TEXT": "#FCA5A5",
    "STATUS_FAILED_BORDER": "#DC2626",
}

BASE_QSS_TEMPLATE = """
/* ── Base ───────────────────────────────────────────────── */
* {{
    font-family: "Inter", "Segoe UI", "SF Pro Display", system-ui, sans-serif;
    font-size: 13px;
}}

QDialog, QWidget {{
    background: {SURFACE_ALT};
    color: {TEXT_PRIMARY};
}}

QLabel {{
    color: {TEXT_PRIMARY};
    background: transparent;
}}

/* ── Scrollbars ─────────────────────────────────────────── */
QScrollBar:vertical {{
    background: {SURFACE_ALT};
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {BORDER};
    border-radius: 3px;
    min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{
    background: {PRIMARY};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    background: {SURFACE_ALT};
    height: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:horizontal {{
    background: {BORDER};
    border-radius: 3px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {PRIMARY};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}

/* ── Buttons ────────────────────────────────────────────── */
QPushButton {{
    background: {SURFACE};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 8px 18px;
    font-size: 13px;
    font-weight: 500;
}}
QPushButton:hover {{
    background: {SURFACE_ALT};
    border-color: {PRIMARY};
}}
QPushButton:pressed {{
    background: {BORDER};
}}
QPushButton:disabled {{
    color: {TEXT_SECONDARY};
    border-color: {BORDER};
    background: {SURFACE_ALT};
}}

QPushButton#replaceBtn {{
    background: {PRIMARY};
    border: none;
    color: #FFFFFF;
    font-weight: 600;
    padding: 9px 24px;
    border-radius: 8px;
}}
QPushButton#replaceBtn:hover {{
    background: {PRIMARY_HOVER};
}}
QPushButton#replaceBtn:disabled {{
    background: {BORDER};
    color: {TEXT_SECONDARY};
}}

QPushButton#cancelBtn {{
    color: {TEXT_SECONDARY};
}}
QPushButton#cancelBtn:hover {{
    color: {TEXT_PRIMARY};
    border-color: #D45454;
}}

QPushButton#undoBtn {{
    color: {TEXT_SECONDARY};
}}
QPushButton#undoBtn:hover {{
    color: {TEXT_PRIMARY};
    border-color: #54A071;
}}

QPushButton#settingsSaveBtn {{
    background: {PRIMARY};
    border: none;
    color: #FFFFFF;
    font-weight: 600;
    padding: 9px 24px;
    border-radius: 8px;
}}
QPushButton#settingsSaveBtn:hover {{
    background: {PRIMARY_HOVER};
}}

QPushButton#testBtn {{
    color: {PRIMARY};
    border-color: {PRIMARY};
}}
QPushButton#testBtn:hover {{
    background: {PRIMARY_LIGHT};
}}

/* ── Text areas ─────────────────────────────────────────── */
QTextEdit {{
    background: {SURFACE};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 14px;
    font-size: 14px;
    line-height: 1.6;
    selection-background-color: {PRIMARY_LIGHT};
}}
QTextEdit:focus {{
    border-color: {PRIMARY};
}}

/* ── Line edits ─────────────────────────────────────────── */
QLineEdit {{
    background: {SURFACE};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
}}
QLineEdit:focus {{
    border-color: {PRIMARY};
}}

/* ── Combo boxes ────────────────────────────────────────── */
QComboBox {{
    background: {SURFACE};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 7px 12px;
    font-size: 13px;
}}
QComboBox:hover {{
    border-color: {PRIMARY};
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox QAbstractItemView {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    color: {TEXT_PRIMARY};
    selection-background-color: {PRIMARY_LIGHT};
    selection-color: {PRIMARY};
    outline: none;
}}

/* ── Check boxes ────────────────────────────────────────── */
QCheckBox {{
    color: {TEXT_PRIMARY};
    spacing: 8px;
}}

/* ── List widgets ───────────────────────────────────────── */
QListWidget {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 10px;
    outline: none;
    color: {TEXT_PRIMARY};
    padding: 4px;
}}
QListWidget::item {{
    padding: 10px 12px;
    border-radius: 8px;
}}
QListWidget::item:selected {{
    background: {PRIMARY_LIGHT};
    color: {PRIMARY};
}}
QListWidget::item:hover:!selected {{
    background: {SURFACE_ALT};
}}

/* ── Group boxes ────────────────────────────────────────── */
QGroupBox {{
    border: 1px solid {BORDER};
    border-radius: 10px;
    margin-top: 14px;
    padding: 14px;
    color: {TEXT_SECONDARY};
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}}

/* ── Splitter ───────────────────────────────────────────── */
QSplitter::handle {{
    background: {BORDER};
    width: 1px;
    height: 1px;
}}
"""

SETTINGS_SCOPED_QSS_TEMPLATE = """
QDialog#SettingsWindow {{
    background: {SURFACE};
}}

QWidget#SettingsSidebar {{
    background: {SURFACE_ALT};
    border-right: 1px solid {BORDER};
}}

QListWidget#SettingsNav {{
    background: transparent;
    border: none;
    outline: none;
}}

QListWidget#SettingsNav::item {{
    padding: 9px 12px;
    margin: 2px 8px;
    border-radius: 8px;
    color: {TEXT_SECONDARY};
    font-size: 13px;
    font-weight: 500;
}}

QListWidget#SettingsNav::item:selected {{
    background: {PRIMARY_LIGHT};
    color: {PRIMARY};
    font-weight: 700;
}}

QListWidget#SettingsNav::item:hover:!selected {{
    background: rgba(124, 58, 237, 0.05);
    color: {TEXT_PRIMARY};
}}

QWidget#SettingsContent {{
    background: {SURFACE};
}}

QDialog#SettingsWindow QLabel {{
    color: {TEXT_PRIMARY};
}}

QDialog#SettingsWindow QLabel#SettingsTitle {{
    color: {TEXT_PRIMARY};
    font-size: 20px;
    font-weight: 700;
}}

QDialog#SettingsWindow QLabel#SettingsMuted {{
    color: {TEXT_SECONDARY};
    font-size: 12px;
}}

QDialog#SettingsWindow QLabel#SettingsAboutName {{
    font-size: 28px;
    font-weight: 800;
    color: {PRIMARY};
}}

QDialog#SettingsWindow QLabel#SettingsAboutVersion {{
    background: {PRIMARY_LIGHT};
    color: {PRIMARY};
    border: 1px solid {PRIMARY_BORDER};
    border-radius: 10px;
    padding: 3px 12px;
    font-size: 11px;
    font-weight: 600;
}}

QDialog#SettingsWindow QLabel#SettingsAboutDesc {{
    font-size: 13px;
    color: {TEXT_SECONDARY};
    line-height: 1.5;
}}

QFrame#SettingsCard {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
}}

QFrame#AboutCard {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 16px;
}}

QFrame#LogoContainer {{
    background: {PRIMARY_LIGHT};
    border: 2px solid {PRIMARY_BORDER};
    border-radius: 55px;
}}

QWidget#AboutLinks, QWidget#AboutFeatures, QWidget#ConnRow {{
    background: transparent;
}}

QFrame#SidebarPromoCard {{
    background: {PRIMARY_LIGHT};
    border: 1px solid {PRIMARY_BORDER};
    border-radius: 12px;
}}

QFrame#SidebarPromoCard QLabel {{
    background: transparent;
    border: none;
    color: {TEXT_SECONDARY};
}}

QFrame#SettingsDivider {{
    background-color: {BORDER};
    max-height: 1px;
    border: none;
}}

QFrame#SidebarDivider {{
    background-color: {BORDER};
    max-height: 1px;
    border: none;
}}

QToolButton#DisclosureButton {{
    background: transparent;
    border: none;
    color: {PRIMARY};
    font-size: 13px;
    font-weight: 600;
    padding: 6px 0;
}}
QToolButton#DisclosureButton:hover {{
    color: {PRIMARY_HOVER};
}}

QPushButton#SecondaryBtn {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    color: {PRIMARY};
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: 600;
}}
QPushButton#SecondaryBtn:hover {{
    background: {PRIMARY_LIGHT};
    border-color: {PRIMARY_BORDER};
}}
QPushButton#SecondaryBtn:pressed {{
    background: {PRIMARY_BORDER};
}}

QLineEdit#SettingsLineEdit {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 5px 8px;
    color: {TEXT_PRIMARY};
    font-size: 12px;
}}
QLineEdit#SettingsLineEdit:focus {{
    border-color: {PRIMARY};
}}

QComboBox#SettingsCombo {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 4px 8px;
    color: {TEXT_PRIMARY};
    font-size: 12px;
}}
QComboBox#SettingsCombo:hover {{
    border-color: {PRIMARY};
}}
QComboBox#SettingsCombo:focus {{
    border-color: {PRIMARY};
}}

QPushButton#AboutLink {{
    background: {PRIMARY_LIGHT};
    border: 1px solid {PRIMARY_BORDER};
    color: {PRIMARY};
    border-radius: 14px;
    padding: 6px 16px;
    font-size: 11px;
    font-weight: 600;
}}
QPushButton#AboutLink:hover {{
    background: {PRIMARY};
    border-color: {PRIMARY};
    color: #FFFFFF;
}}

QLabel#Keycap {{
    border: 1px solid {BORDER};
    border-bottom: 2.5px solid {BORDER_ALT};
    border-radius: 6px;
    background: {SURFACE_ALT};
    color: {TEXT_PRIMARY};
    font-size: 14px;
    font-weight: 600;
    padding: 2px 8px;
}}

QToolButton#ThemeCard {{
    background: {SURFACE};
    border: 1.5px solid {BORDER};
    border-radius: 12px;
    padding: 12px;
    color: {TEXT_SECONDARY};
    font-weight: 500;
}}
QToolButton#ThemeCard:hover {{
    background: {SURFACE_ALT};
    border-color: {PRIMARY_BORDER};
    color: {TEXT_PRIMARY};
}}
QToolButton#ThemeCard:checked {{
    background: {PRIMARY_LIGHT};
    border: 2px solid {PRIMARY};
    color: {PRIMARY};
    font-weight: 700;
}}
QToolButton#ThemeCard:disabled {{
    background: {SURFACE_ALT};
    border-color: {BORDER};
    color: {TEXT_SECONDARY};
}}

QCheckBox {{
    color: {TEXT_PRIMARY};
    spacing: 8px;
    background: transparent;
}}

QListWidget#SettingsHistory {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    outline: none;
    color: {TEXT_PRIMARY};
    padding: 6px;
}}
QListWidget#SettingsHistory::item {{
    padding: 8px 12px;
    border-radius: 8px;
    color: {TEXT_PRIMARY};
}}
QListWidget#SettingsHistory::item:hover {{
    background: {PRIMARY_LIGHT};
    color: {PRIMARY};
}}

QLabel#StatusBadge {{
    border-radius: 10px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 600;
    background: {SURFACE_ALT};
    color: {TEXT_SECONDARY};
    border: 1px solid {BORDER};
}}

QLabel#StatusBadge[status="testing"] {{
    background: {STATUS_TESTING_BG};
    color: {STATUS_TESTING_TEXT};
    border: 1px solid {STATUS_TESTING_BORDER};
}}

QLabel#StatusBadge[status="connected"] {{
    background: {STATUS_CONNECTED_BG};
    color: {STATUS_CONNECTED_TEXT};
    border: 1px solid {STATUS_CONNECTED_BORDER};
}}

QLabel#StatusBadge[status="failed"] {{
    background: {STATUS_FAILED_BG};
    color: {STATUS_FAILED_TEXT};
    border: 1px solid {STATUS_FAILED_BORDER};
}}

/* ── EnhancementPopup Scoped Styles ────────────────────────── */
QWidget#EnhancementCard {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 16px;
}}
QLabel#EnhancementIcon {{
    color: {PRIMARY};
    font-size: 20px;
    background: transparent;
}}
QLabel#EnhancementTitle {{
    color: {TEXT_PRIMARY};
    font-size: 16px;
    font-weight: 700;
    background: transparent;
}}
QLabel#EnhancementStatus {{
    color: {TEXT_SECONDARY};
    font-size: 12px;
    background: transparent;
}}
QPushButton#EnhancementCloseBtn {{
    background: transparent;
    color: {TEXT_SECONDARY};
    border: none;
    font-size: 14px;
}}
QPushButton#EnhancementCloseBtn:hover {{
    color: #EF4444;
}}
QFrame#EnhancementSeparator {{
    background-color: {BORDER};
    max-height: 1px;
    border: none;
}}
QLabel#EnhancementLabelOriginal {{
    color: {TEXT_SECONDARY};
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    background: transparent;
}}
QLabel#EnhancementLabelEnhanced {{
    color: {PRIMARY};
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    background: transparent;
}}

/* ── ModeButton QToolButton Style ──────────────────────────── */
QToolButton#ModeButton {{
    background: {SURFACE_ALT};
    color: {TEXT_SECONDARY};
    border: 1px solid {BORDER};
    border-radius: 15px;
    padding: 0 14px;
    font-size: 12px;
}}
QToolButton#ModeButton:hover {{
    background: {PRIMARY_LIGHT};
    color: {PRIMARY};
    border-color: {PRIMARY_BORDER};
}}
QToolButton#ModeButton:checked {{
    background: {PRIMARY};
    color: #FFFFFF;
    border: none;
    font-weight: 600;
}}

/* ── Settings Row & Section Headers ───────────────────────── */
QLabel#SettingsSectionHeader {{
    font-size: 10px;
    font-weight: 700;
    color: {TEXT_SECONDARY};
    letter-spacing: 1px;
    margin-top: 10px;
    margin-bottom: 4px;
    background: transparent;
    border: none;
}}

QLabel#KeycapLabel {{
    font-family: system-ui, -apple-system, sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: {PRIMARY};
    background: {PRIMARY_LIGHT};
    border: 1px solid {PRIMARY_BORDER};
    border-bottom: 2.5px solid {PRIMARY};
    border-radius: 5px;
    padding: 2px 6px;
    min-width: 14px;
    margin: 1px 0px;
}}

QWidget#SettingsRowIconWrapper {{
    background-color: {PRIMARY_LIGHT};
    border-radius: 15px;
}}

QLabel#SettingsRowTitle {{
    font-size: 13px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
    background: transparent;
    border: none;
}}
QLabel#SettingsRowDesc {{
    font-size: 11px;
    color: {TEXT_SECONDARY};
    background: transparent;
    border: none;
}}
QLabel#SettingsRowRightText {{
    font-size: 13px;
    color: {TEXT_SECONDARY};
    font-weight: 500;
    background: transparent;
    border: none;
}}

/* ── About Page Redesigns ─────────────────────────────────── */
QLabel#AboutFeaturePill {{
    background: {PRIMARY_LIGHT};
    color: {PRIMARY};
    border: 1px solid {PRIMARY_BORDER};
    border-radius: 12px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 600;
}}

/* ── Sidebar Custom Footer ─────────────────────────────────── */
QLabel#SidebarFootTitle {{
    font-size: 11px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
    background: transparent;
    border: none;
}}
QLabel#SidebarFootDesc {{
    font-size: 10px;
    color: {TEXT_SECONDARY};
    background: transparent;
    border: none;
}}
QLabel#SidebarPromoTitle {{
    font-size: 11px;
    font-weight: 700;
    color: {PRIMARY};
    background: transparent;
    border: none;
}}
QLabel#SidebarPromoDesc {{
    font-size: 10px;
    color: {TEXT_SECONDARY};
    line-height: 1.3;
    background: transparent;
    border: none;
}}
QLabel#SidebarPromoLink {{
    font-size: 10px;
    background: transparent;
    border: none;
}}
QLabel#SidebarPromoLink a {{
    color: {PRIMARY};
    font-weight: 700;
    text-decoration: none;
}}
QLabel#SidebarPromoLink a:hover {{
    color: {PRIMARY_HOVER};
}}

/* ── InstallerOverlay ─────────────────────────────────────── */
QWidget#InstallerOverlay {{
    background: transparent;
}}
QFrame#InstallerCard {{
    background-color: {SURFACE_ALT};
    border-radius: 14px;
    border: 1px solid {BORDER};
}}
QLabel#InstallerTitle {{
    color: {TEXT_PRIMARY};
    font-size: 15px;
    font-weight: 700;
    background: transparent;
}}
QProgressBar#InstallerProgress {{
    background-color: {BORDER};
    border-radius: 4px;
    border: none;
}}
QProgressBar#InstallerProgress::chunk {{
    background-color: {PRIMARY};
    border-radius: 4px;
}}
QLabel#InstallerStatus {{
    color: {TEXT_SECONDARY};
    font-size: 12px;
    background: transparent;
}}
QLabel#InstallerStatus[status="error"] {{
    color: #EF4444;
}}
QLabel#InstallerStatus[status="success"] {{
    color: #10B981;
}}
QLabel#InstallerNote {{
    color: {TEXT_SECONDARY};
    font-size: 11px;
    background: transparent;
}}
QPushButton#InstallerRetryBtn {{
    background-color: #EF4444;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 7px 0;
    font-weight: 600;
    font-size: 13px;
}}
QPushButton#InstallerRetryBtn:hover {{
    background-color: #DC2626;
}}

/* ── CommandPalette Scoped Styles ────────────────────────── */
QFrame#paletteCard {{
    background: {SURFACE};
    border-radius: 16px;
    border: 1px solid {PRIMARY_BORDER};
}}

QWidget#paletteSearchSection {{
    background: {SURFACE};
    border: 1.5px solid {BORDER};
    border-radius: 8px;
}}

QWidget#paletteSearchSection[focus="true"] {{
    border: 2px solid {PRIMARY};
}}

QLabel#PaletteSearchIcon {{
    color: {PRIMARY};
    font-size: 18px;
    background: transparent;
    border: none;
}}

QLineEdit#PaletteSearchEdit {{
    background: transparent;
    border: none;
    font-size: 15px;
    font-weight: 500;
    color: {TEXT_PRIMARY};
    padding: 2px 0;
}}

QLabel#PaletteEscBadge {{
    color: {TEXT_SECONDARY};
    font-size: 11px;
    background: {PRIMARY_LIGHT};
    border: 1px solid {PRIMARY_BORDER};
    border-radius: 5px;
    padding: 3px 7px;
}}

QFrame#PaletteDivider {{
    background-color: {BORDER};
    max-height: 1px;
    border: none;
}}

QWidget#PalettePreview {{
    background: {PRIMARY_LIGHT};
    border-bottom: 1px solid {BORDER};
}}

QLabel#PalettePreviewIcon {{
    color: {PRIMARY};
    font-size: 13px;
    background: transparent;
    border: none;
}}

QLabel#PalettePreviewLabel {{
    color: {TEXT_SECONDARY};
    font-size: 12px;
    font-style: italic;
    background: transparent;
    border: none;
}}

QWidget#PaletteFooter {{
    background: {SURFACE_ALT};
    border-top: 1px solid {BORDER};
    border-bottom-left-radius: 16px;
    border-bottom-right-radius: 16px;
}}

QLabel#PaletteNavHint {{
    color: {TEXT_SECONDARY};
    font-size: 11px;
    background: transparent;
    border: none;
}}

QLabel#PalettePowered {{
    color: {TEXT_SECONDARY};
    opacity: 0.7;
    font-size: 11px;
    background: transparent;
    border: none;
}}

QListWidget#paletteList {{
    background: transparent;
    border: none;
    outline: none;
}}

QListWidget#paletteList::item {{
    border-radius: 8px;
    padding: 0;
    margin: 1px 0;
    background: transparent;
}}

QListWidget#paletteList::item:selected {{
    background: transparent;
}}

QWidget#PaletteListContainer {{
    background: transparent;
}}

QLineEdit#PaletteSearchEdit::placeholder {{
    color: {TEXT_SECONDARY};
}}

/* ── ModeItemWidget Styles ── */
QWidget#ModeItemWidget {{
    background: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
}}

QWidget#ModeItemWidget:hover {{
    background: {PRIMARY_HOVER_BG};
    border: 1px solid {PRIMARY_HOVER_BORDER};
}}

QWidget#ModeItemWidget[selected="true"] {{
    background: {PRIMARY_LIGHT};
    border: 1px solid {PRIMARY_BORDER};
}}

QLabel#ModeItemIcon {{
    color: {PRIMARY};
    font-size: 14px;
    background: {PRIMARY_LIGHT};
    border-radius: 6px;
    border: none;
}}

QWidget#ModeItemWidget:hover QLabel#ModeItemIcon {{
    background: {PRIMARY_LIGHT};
}}

QWidget#ModeItemWidget[selected="true"] QLabel#ModeItemIcon {{
    color: {PRIMARY};
    background: {SURFACE};
}}

QLabel#ModeItemText {{
    color: {TEXT_PRIMARY};
    font-size: 13px;
    font-weight: 500;
    background: transparent;
    border: none;
}}

QWidget#ModeItemWidget:hover QLabel#ModeItemText {{
    color: {PRIMARY};
}}

QWidget#ModeItemWidget[selected="true"] QLabel#ModeItemText {{
    color: {PRIMARY};
    font-weight: 700;
}}

QLabel#ModeItemEnter {{
    color: transparent;
    font-size: 12px;
    background: transparent;
    border: none;
}}

QWidget#ModeItemWidget[selected="true"] QLabel#ModeItemEnter {{
    color: {PRIMARY};
}}

QWidget#PaletteSectionHeaderWidget {{
    background: transparent;
}}

QLabel#PaletteSectionHeaderLabel {{
    color: {TEXT_SECONDARY};
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    background: transparent;
    border: none;
}}
"""

def get_qss(theme: str) -> str:
    tokens = DARK_TOKENS if theme == "dark" else LIGHT_TOKENS
    base = BASE_QSS_TEMPLATE.format(**tokens)
    scoped = SETTINGS_SCOPED_QSS_TEMPLATE.format(**tokens)
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
            for cleaned_text in self._processor.enhance(self._text, self._mode, self._custom_instruction):
                self._full_result = cleaned_text
                self.chunk_received.emit(cleaned_text)
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
        self.setObjectName("ModeButton")
        self.mode_key = mode_key
        self.setText(label)
        self.setCheckable(True)
        self.setFixedHeight(30)


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
        card.setObjectName("EnhancementCard")
        root.addWidget(card)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # ── Header ────────────────────────────────────────────────────────────
        header = QHBoxLayout()
        icon_lbl = QLabel("✦")
        icon_lbl.setObjectName("EnhancementIcon")
        
        title_lbl = QLabel("Avelyn")
        title_lbl.setObjectName("EnhancementTitle")
        
        self._status_lbl = QLabel("Enhancing…")
        self._status_lbl.setObjectName("EnhancementStatus")
        
        close_btn = QPushButton("✕")
        close_btn.setObjectName("EnhancementCloseBtn")
        close_btn.setFixedSize(28, 28)
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
        sep.setObjectName("EnhancementSeparator")
        sep.setFrameShape(QFrame.Shape.HLine)
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
        orig_lbl.setObjectName("EnhancementLabelOriginal")
        
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
        enh_lbl.setObjectName("EnhancementLabelEnhanced")
        
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
    def _on_chunk(self, full_text: str) -> None:
        self._enhanced_text = full_text
        self._enh_edit.setPlainText(full_text)
        cursor = self._enh_edit.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
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
        
        from utils import PerfTracker
        import time
        PerfTracker.clipboard_replace_start = time.perf_counter()
        self._clipboard.set(self._enhanced_text)
        PerfTracker.clipboard_replace_end = time.perf_counter()
        
        self.hide()
        # Small delay to ensure popup is hidden before simulating paste.
        def do_paste():
            from platform_handler import paste_text
            paste_text()
            PerfTracker.pipeline_end = time.perf_counter()
            PerfTracker.log_summary()

        QTimer.singleShot(120, do_paste)
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

def _settings_nav_icon(icon_kind: str, theme: str = "light") -> QIcon:
    tokens = DARK_TOKENS if theme == "dark" else LIGHT_TOKENS
    icon = QIcon()
    icon.addPixmap(_paint_settings_icon(icon_kind, tokens["TEXT_SECONDARY"], 16), QIcon.Mode.Normal)
    icon.addPixmap(_paint_settings_icon(icon_kind, tokens["PRIMARY"], 16), QIcon.Mode.Selected)
    return icon

def _theme_preview(mode: str) -> QIcon:
    pix = QPixmap(120, 72)
    pix.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pix)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # ── Background colors ──
    bg_color = QColor("#F3F4F6") if mode == "light" else QColor("#1F2937")
    card_color = QColor("#FFFFFF") if mode == "light" else QColor("#2D3748")
    sidebar_bg = QColor("#E5E7EB") if mode == "light" else QColor("#111827")
    line_color = QColor("#D1D5DB") if mode == "light" else QColor("#4A5568")
    
    if mode == "system":
        painter.setClipRect(0, 0, 120, 72)
        
        # Left diagonal half is light
        path_light = QPainterPath()
        path_light.moveTo(0, 0)
        path_light.lineTo(120, 0)
        path_light.lineTo(0, 72)
        path_light.closeSubpath()
        painter.fillPath(path_light, QColor("#F3F4F6"))
        
        # Right diagonal half is dark
        path_dark = QPainterPath()
        path_dark.moveTo(120, 72)
        path_dark.lineTo(120, 0)
        path_dark.lineTo(0, 72)
        path_dark.closeSubpath()
        painter.fillPath(path_dark, QColor("#1F2937"))
        
        # Split line and frame
        painter.setPen(QPen(QColor("#9CA3AF"), 1))
        painter.drawLine(120, 0, 0, 72)
        painter.setPen(QPen(QColor("#9CA3AF"), 1.5))
        painter.drawRoundedRect(2, 2, 116, 68, 4, 4)
        
        painter.end()
        return QIcon(pix)
        
    # Paint standard solid light/dark preview
    painter.setBrush(bg_color)
    painter.setPen(QPen(line_color, 1))
    painter.drawRoundedRect(2, 2, 116, 68, 4, 4)
    
    # Sidebar
    painter.setBrush(sidebar_bg)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(2, 2, 34, 68, 4, 4)
    painter.drawRect(32, 2, 4, 68) # Cover rounded corners
    
    # Sidebar border line
    painter.setPen(QPen(line_color, 1))
    painter.drawLine(36, 2, 36, 70)
    
    # Titlebar dots
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("#EF4444"))
    painter.drawEllipse(8, 8, 5, 5)
    painter.setBrush(QColor("#F59E0B"))
    painter.drawEllipse(16, 8, 5, 5)
    painter.setBrush(QColor("#10B981"))
    painter.drawEllipse(24, 8, 5, 5)
    
    # Content rows/card
    painter.setPen(QPen(line_color, 1))
    painter.setBrush(card_color)
    painter.drawRoundedRect(44, 18, 68, 42, 2, 2)
    
    # Mock text rows inside card
    painter.setPen(QPen(line_color, 1))
    painter.drawLine(48, 26, 68, 26)
    painter.drawLine(48, 34, 86, 34)
    painter.drawLine(48, 42, 62, 42)
    
    # Sliders knobs representation
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("#7C3AED"))
    painter.drawEllipse(98, 24, 5, 5)
    painter.drawEllipse(92, 38, 5, 5)
    
    painter.end()
    return QIcon(pix)

def _divider_line() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Plain)
    line.setObjectName("SettingsDivider")
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

def _section_header(text: str) -> QLabel:
    lbl = QLabel(text.upper())
    lbl.setObjectName("SettingsSectionHeader")
    return lbl

def _keycap_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setObjectName("KeycapLabel")
    lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return lbl

def _premium_row(
    label_text: str,
    sub_label: str = "",
    icon_kind: str = "",
    widget: Optional[QWidget] = None,
    right_text: str = "",
    show_arrow: bool = False,
    theme: str = "light",
    icon_color: Optional[str] = None,
    icon_bg_color: Optional[str] = None,
) -> QWidget:
    row = QWidget()
    row.setObjectName("SettingsRow")
    l = QHBoxLayout(row)
    l.setContentsMargins(14, 10, 14, 10)
    l.setSpacing(12)

    if icon_kind:
        icon_wrapper = QWidget()
        icon_wrapper.setObjectName("SettingsRowIconWrapper")
        icon_wrapper.setFixedSize(30, 30)
        
        iw_layout = QHBoxLayout(icon_wrapper)
        iw_layout.setContentsMargins(0, 0, 0, 0)
        iw_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        tokens = DARK_TOKENS if theme == "dark" else LIGHT_TOKENS
        if icon_color is None:
            icon_color = tokens["PRIMARY"]
        
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
    text_l.addWidget(title)
    
    if sub_label:
        desc = QLabel(sub_label)
        desc.setObjectName("SettingsRowDesc")
        desc.setWordWrap(True)
        text_l.addWidget(desc)
        
    l.addWidget(text_w, 1)

    if widget is not None:
        l.addWidget(widget, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    elif right_text:
        rt = QLabel(right_text)
        rt.setObjectName("SettingsRowRightText")
        l.addWidget(rt)

    if show_arrow:
        tokens = DARK_TOKENS if theme == "dark" else LIGHT_TOKENS
        arrow = QLabel()
        arrow.setPixmap(_paint_settings_icon("chevron", tokens["PRIMARY"], 12))
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
        self.setMinimumSize(840, 620)
        self.resize(960, 680)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── Sidebar ───────────────────────────────────────────────────────────
        sidebar = QWidget()
        sidebar.setObjectName("SettingsSidebar")
        sidebar.setFixedWidth(240)
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(16, 24, 16, 24)
        sb_layout.setSpacing(16)

        from utils import get_resource_path
        logo_path = get_resource_path("public/logo.png")
        
        tokens = DARK_TOKENS if self._settings.theme == "dark" else LIGHT_TOKENS

        brand = QWidget()
        brand.setObjectName("SettingsBrand")
        brand_row = QHBoxLayout(brand)
        brand_row.setContentsMargins(0, 0, 0, 0)
        brand_row.setSpacing(12)

        logo_lbl = QLabel()
        logo_lbl.setFixedSize(48, 48)
        if logo_path.exists():
            pm = QPixmap(str(logo_path))
            if not pm.isNull():
                logo_lbl.setPixmap(pm.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            logo_lbl.setPixmap(_paint_settings_icon("sparkles", tokens["PRIMARY"], 48))

        brand_text_w = QWidget()
        brand_text_l = QVBoxLayout(brand_text_w)
        brand_text_l.setContentsMargins(0, 0, 0, 0)
        brand_text_l.setSpacing(1)

        name_lbl = QLabel("Avelyn")
        name_lbl.setObjectName("SidebarBrandName")
        subtitle_lbl = QLabel("AI Writing Assistant")
        subtitle_lbl.setObjectName("SidebarBrandSubtitle")

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
        self._sidebar.setFixedHeight(220)
        self._sidebar.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._sidebar.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        pages = [
            ("AI Provider", "sparkles"),
            ("Hotkeys", "keyboard"),
            ("Appearance", "palette"),
            ("History", "clock"),
            ("About", "info"),
        ]
        for label, icon_kind in pages:
            item = QListWidgetItem(label)
            item.setIcon(_settings_nav_icon(icon_kind, self._settings.theme))
            self._sidebar.addItem(item)
        self._sidebar.setCurrentRow(0)
        self._sidebar.currentRowChanged.connect(self._on_page_changed)
        sb_layout.addWidget(self._sidebar)
        
        sb_layout.addStretch(1)

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
        shield_icon.setPixmap(_paint_settings_icon("shield", tokens["PRIMARY"], 14))
        promo_title = QLabel("Private & Local")
        promo_title.setObjectName("SidebarPromoTitle")
        promo_header.addWidget(shield_icon)
        promo_header.addWidget(promo_title, 1)

        promo_desc = QLabel("Everything runs locally on your machine. Your data never leaves your device.")
        promo_desc.setObjectName("SidebarPromoDesc")
        promo_desc.setWordWrap(True)

        promo_link = QLabel("<a href='#'>Learn more ></a>")
        promo_link.setObjectName("SidebarPromoLink")

        promo_l.addLayout(promo_header)
        promo_l.addWidget(promo_desc)
        promo_l.addWidget(promo_link)
        sb_layout.addWidget(promo_card)
        sb_layout.addSpacing(4)

        # Thin divider separator above the footer
        sep = QFrame()
        sep.setObjectName("SidebarDivider")
        sep.setFrameShape(QFrame.Shape.HLine)
        sb_layout.addWidget(sep)

        # Intentional Footer
        footer = QWidget()
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(12, 10, 12, 10)
        footer_layout.setSpacing(3)

        foot_title = QLabel("Avelyn Desktop")
        foot_title.setObjectName("SidebarFootTitle")
        
        foot_desc = QLabel("v1.0.0-beta • Local AI")
        foot_desc.setObjectName("SidebarFootDesc")

        footer_layout.addWidget(foot_title)
        footer_layout.addWidget(foot_desc)
        sb_layout.addWidget(footer)

        # ── Content stack ─────────────────────────────────────────────────────
        content = QWidget()
        content.setObjectName("SettingsContent")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(32, 24, 32, 24)
        content_layout.setSpacing(24)

        self._stack = QStackedWidget()
        self._stack.setMaximumWidth(900)
        self._stack.addWidget(self._page_ai())
        self._stack.addWidget(self._page_hotkeys())
        self._stack.addWidget(self._page_appearance())
        self._stack.addWidget(self._page_history())
        self._stack.addWidget(self._page_about())

        content_layout.addWidget(self._stack, 1)

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

        tokens = DARK_TOKENS if self._settings.theme == "dark" else LIGHT_TOKENS

        title = QLabel("AI Provider")
        title.setObjectName("SettingsTitle")
        layout.addWidget(title)

        hint = QLabel("Configure how Avelyn connects to your local AI model.")
        hint.setObjectName("SettingsMuted")
        layout.addWidget(hint)

        # Section 1: General Configuration
        layout.addWidget(_section_header("General Configuration"))

        # Connection Status Layout
        conn_row = QWidget()
        conn_row.setObjectName("ConnRow")
        conn_l = QHBoxLayout(conn_row)
        conn_l.setContentsMargins(0, 0, 0, 0)
        conn_l.setSpacing(10)

        test_btn = QPushButton("Test Connection")
        test_btn.setObjectName("SecondaryBtn")
        test_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        test_btn.setIcon(QIcon(_paint_settings_icon("wave", tokens["PRIMARY"], 14)))
        test_btn.clicked.connect(self._on_test_connection)

        self._status_dot = QLabel("●")
        self._status_dot.hide() # Hidden: we use StatusBadge background instead!
        
        self._test_result = QLabel("Not Tested")
        self._test_result.setObjectName("StatusBadge")
        self._test_result.setProperty("status", "not_tested")
        self._test_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        conn_l.addWidget(self._status_dot)
        conn_l.addWidget(self._test_result)
        conn_l.addWidget(test_btn)

        self._conn_card = _premium_row(
            label_text="Local AI Connection",
            sub_label="Verify connection to your Ollama service.",
            icon_kind="server",
            icon_color=tokens["PRIMARY"],
            icon_bg_color=tokens["PRIMARY_LIGHT"],
            widget=conn_row,
            theme=self._settings.theme
        )

        # Default Mode Selection
        self._default_mode_combo = QComboBox()
        self._default_mode_combo.setObjectName("SettingsCombo")
        self._default_mode_combo.setFixedWidth(220)
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
            icon_color=tokens["PRIMARY"],
            icon_bg_color=tokens["PRIMARY_LIGHT"],
            widget=self._default_mode_combo,
            theme=self._settings.theme
        )
        # Group Connection Status and Default Mode under General Configuration
        layout.addWidget(_settings_group([self._conn_card, default_mode_card]))

        # Section 2: Engine Settings
        layout.addWidget(_section_header("Engine Settings"))

        # Advanced Settings Block
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
            icon_color=tokens["PRIMARY"],
            icon_bg_color=tokens["PRIMARY_LIGHT"],
            show_arrow=True,
            theme=self._settings.theme
        )
        
        # Host row
        self._ollama_host = QLineEdit(self._settings.ollama_host)
        self._ollama_host.setObjectName("SettingsLineEdit")
        self._ollama_host.setFixedWidth(220)
        host_row = _premium_row(
            label_text="Host",
            icon_kind="link",
            icon_color=tokens["PRIMARY"],
            icon_bg_color=tokens["PRIMARY_LIGHT"],
            widget=self._ollama_host,
            show_arrow=True,
            theme=self._settings.theme
        )

        # Model row
        self._ollama_model_edit = QLineEdit(self._settings.ollama_model)
        self._ollama_model_edit.setObjectName("SettingsLineEdit")
        self._ollama_model_edit.setPlaceholderText("e.g. gemma3:4b")
        self._ollama_model_edit.setFixedWidth(220)
        model_row = _premium_row(
            label_text="Model",
            icon_kind="cube",
            icon_color=tokens["PRIMARY"],
            icon_bg_color=tokens["PRIMARY_LIGHT"],
            widget=self._ollama_model_edit,
            show_arrow=True,
            theme=self._settings.theme
        )

        # Additional options row
        additional_row = _premium_row(
            label_text="Additional Options",
            sub_label="Customize advanced model settings",
            icon_kind="sliders",
            icon_color=tokens["PRIMARY"],
            icon_bg_color=tokens["PRIMARY_LIGHT"],
            show_arrow=True,
            theme=self._settings.theme
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

        # Section 3: Security & Privacy
        layout.addWidget(_section_header("Security & Privacy"))

        # Footer Banner
        footer_banner_row = _premium_row(
            label_text="100% Local. 100% Private.",
            sub_label="Avelyn never sends your data anywhere. All processing happens on your machine.",
            icon_kind="shield",
            icon_color=tokens["PRIMARY"],
            icon_bg_color=tokens["PRIMARY_LIGHT"],
            theme=self._settings.theme
        )
        layout.addWidget(_settings_group([footer_banner_row]))
        layout.addStretch()
        return w

    def _page_hotkeys(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(14)
        layout.setContentsMargins(0, 0, 0, 0)

        tokens = DARK_TOKENS if self._settings.theme == "dark" else LIGHT_TOKENS

        title = QLabel("Hotkeys")
        title.setObjectName("SettingsTitle")
        layout.addWidget(title)

        hint = QLabel("Configure system-wide keyboard shortcuts for Avelyn.")
        hint.setObjectName("SettingsMuted")
        layout.addWidget(hint)

        # Section 1: Shortcut Configuration
        layout.addWidget(_section_header("Shortcut Configuration"))

        # Global Shortcut Card
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
            icon_color=tokens["PRIMARY"],
            icon_bg_color=tokens["PRIMARY_LIGHT"],
            widget=preview_row,
            theme=self._settings.theme
        )

        self._hotkey_enabled_cb = QCheckBox()
        self._hotkey_enabled_cb.setFixedSize(20, 20)
        self._hotkey_enabled_cb.setChecked(self._settings.hotkey_enabled)
        enabled_card_row = _premium_row(
            label_text="Enable global hotkey",
            sub_label="Allows Avelyn to capture your selected text system-wide.",
            icon_kind="shield",
            icon_color=tokens["PRIMARY"],
            icon_bg_color=tokens["PRIMARY_LIGHT"],
            widget=self._hotkey_enabled_cb,
            theme=self._settings.theme
        )

        self._startup_cb = QCheckBox()
        self._startup_cb.setFixedSize(20, 20)
        self._startup_cb.setChecked(self._settings.launch_at_startup)
        startup_card_row = _premium_row(
            label_text="Launch at system login",
            sub_label="Start Avelyn in your menu bar automatically when you log in.",
            icon_kind="sliders",
            icon_color=tokens["PRIMARY"],
            icon_bg_color=tokens["PRIMARY_LIGHT"],
            widget=self._startup_cb,
            theme=self._settings.theme
        )

        layout.addWidget(_settings_group([shortcut_card_row, enabled_card_row, startup_card_row]))

        # Section 2: Advanced Integration
        layout.addWidget(_section_header("Advanced Integration"))

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
        self._hotkey_raw.setFixedWidth(220)
        
        raw_row = _premium_row(
            label_text="Raw internal hotkey (pynput)",
            sub_label="Leave blank to automatically convert from the display shortcut field.",
            icon_kind="sliders",
            icon_color=tokens["PRIMARY"],
            icon_bg_color=tokens["PRIMARY_LIGHT"],
            widget=self._hotkey_raw,
            theme=self._settings.theme
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

        tokens = DARK_TOKENS if self._settings.theme == "dark" else LIGHT_TOKENS

        title = QLabel("Appearance")
        title.setObjectName("SettingsTitle")
        layout.addWidget(title)

        hint = QLabel("Customize the visual style and notifications of Avelyn.")
        hint.setObjectName("SettingsMuted")
        layout.addWidget(hint)

        # Section 1: Theme Preferences
        layout.addWidget(_section_header("Theme Preferences"))

        tc_card = QFrame()
        tc_card.setObjectName("SettingsCard")
        tc_layout = QVBoxLayout(tc_card)
        tc_layout.setContentsMargins(18, 20, 18, 20)
        tc_layout.setSpacing(14)

        # Keep hidden combo for save compatibility
        self._theme_combo = QComboBox()
        self._theme_combo.setObjectName("SettingsCombo")
        self._theme_combo.addItems(["Dark", "Light"])
        self._theme_combo.setCurrentIndex(0 if self._settings.theme == "dark" else 1)
        self._theme_combo.hide()

        row = QHBoxLayout()
        row.setSpacing(16)

        light_btn = QToolButton()
        light_btn.setObjectName("ThemeCard")
        light_btn.setCheckable(True)
        light_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        light_btn.setIcon(_theme_preview("light"))
        light_btn.setIconSize(QSize(120, 72))
        light_btn.setText("Light Mode")
        light_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        light_btn.setFixedSize(160, 120)

        dark_btn = QToolButton()
        dark_btn.setObjectName("ThemeCard")
        dark_btn.setCheckable(True)
        dark_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        dark_btn.setIcon(_theme_preview("dark"))
        dark_btn.setIconSize(QSize(120, 72))
        dark_btn.setText("Dark Mode")
        dark_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        dark_btn.setFixedSize(160, 120)

        system_btn = QToolButton()
        system_btn.setObjectName("ThemeCard")
        system_btn.setCheckable(False)
        system_btn.setEnabled(False)
        system_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        system_btn.setIcon(_theme_preview("system"))
        system_btn.setIconSize(QSize(120, 72))
        system_btn.setText("System Theme")
        system_btn.setToolTip("System theme is not supported in this build.")
        system_btn.setFixedSize(160, 120)

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

        row.addStretch()
        row.addWidget(light_btn)
        row.addWidget(dark_btn)
        row.addWidget(system_btn)
        row.addStretch()
        tc_layout.addLayout(row)
        layout.addWidget(tc_card)

        # Section 2: Alerts & Notifications
        layout.addWidget(_section_header("Alerts & Notifications"))

        # Notifications Group Card
        self._notif_cb = QCheckBox()
        self._notif_cb.setFixedSize(20, 20)
        self._notif_cb.setChecked(self._settings.get("show_notifications", True))
        
        notif_row = _premium_row(
            label_text="System Notifications",
            sub_label="Display menu bar notifications for shortcut triggers and updates.",
            icon_kind="info",
            icon_color=tokens["PRIMARY"],
            icon_bg_color=tokens["PRIMARY_LIGHT"],
            widget=self._notif_cb,
            theme=self._settings.theme
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
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        tokens = DARK_TOKENS if self._settings.theme == "dark" else LIGHT_TOKENS

        card = QFrame()
        card.setObjectName("AboutCard")
        card.setFixedSize(540, 440)

        # Soft purple shadow
        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(35)
        shadow.setOffset(0, 10)
        from PyQt6.QtGui import QColor
        shadow.setColor(QColor(124, 58, 237, int(255 * 0.15)))
        card.setGraphicsEffect(shadow)

        card_l = QVBoxLayout(card)
        card_l.setContentsMargins(32, 28, 32, 28)
        card_l.setSpacing(12)
        card_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        from utils import get_resource_path
        logo_path = get_resource_path("public/logo.png")

        # Logo wrapped in circular badge
        logo_container = QFrame()
        logo_container.setObjectName("LogoContainer")
        logo_container.setFixedSize(110, 110)
        logo_container_layout = QVBoxLayout(logo_container)
        logo_container_layout.setContentsMargins(0, 0, 0, 0)
        logo_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo = QLabel()
        logo.setFixedSize(80, 80)
        if logo_path.exists():
            pm = QPixmap(str(logo_path))
            if not pm.isNull():
                logo.setPixmap(pm.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            logo.setPixmap(_paint_settings_icon("sparkles", tokens["PRIMARY"], 80))
        logo_container_layout.addWidget(logo)

        name = QLabel("Avelyn")
        name.setObjectName("SettingsAboutName")

        version = QLabel("Version 1.0.0")
        version.setObjectName("SettingsAboutVersion")

        # Feature Pills Row
        features = QWidget()
        features.setObjectName("AboutFeatures")
        features_l = QHBoxLayout(features)
        features_l.setContentsMargins(0, 4, 0, 4)
        features_l.setSpacing(8)

        def feature_pill(text: str) -> QLabel:
            lbl = QLabel(text)
            lbl.setObjectName("AboutFeaturePill")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            return lbl

        features_l.addStretch()
        features_l.addWidget(feature_pill("Local AI"))
        features_l.addWidget(feature_pill("Privacy First"))
        features_l.addWidget(feature_pill("Cross Platform"))
        features_l.addStretch()

        desc = QLabel(
            "A premium system-wide writing assistant powered by local AI.\n"
            "Runs entirely locally on your machine for complete speed, privacy, and security."
        )
        desc.setObjectName("SettingsAboutDesc")
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Premium Links Row
        links = QWidget()
        links.setObjectName("AboutLinks")
        links_l = QHBoxLayout(links)
        links_l.setContentsMargins(0, 8, 0, 0)
        links_l.setSpacing(12)

        def link_btn(label: str, url: str) -> QPushButton:
            from PyQt6.QtCore import QUrl
            from PyQt6.QtGui import QDesktopServices
            b = QPushButton(label)
            b.setObjectName("AboutLink")
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(url)))
            return b

        links_l.addStretch()
        links_l.addWidget(link_btn("Website", "https://www.avelyn.software"))
        links_l.addWidget(link_btn("GitHub", "https://github.com/vishwaksen21"))
        links_l.addWidget(link_btn("Privacy", "https://www.avelyn.software/#privacy"))
        links_l.addStretch()

        card_l.addWidget(logo_container, 0, Qt.AlignmentFlag.AlignCenter)
        card_l.addWidget(name, 0, Qt.AlignmentFlag.AlignCenter)
        card_l.addWidget(version, 0, Qt.AlignmentFlag.AlignCenter)
        card_l.addWidget(features, 0, Qt.AlignmentFlag.AlignCenter)
        card_l.addWidget(_divider_line())
        card_l.addWidget(desc, 0, Qt.AlignmentFlag.AlignCenter)
        card_l.addWidget(links, 0, Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(card, 0, Qt.AlignmentFlag.AlignCenter)
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
        self._test_result.setProperty("status", "testing")
        self._test_result.style().unpolish(self._test_result)
        self._test_result.style().polish(self._test_result)
        QApplication.processEvents()
        try:
            result = self._processor.test_connection()
            display_res = f"Connected: {result[:25]}..." if len(result) > 25 else f"Connected: {result}"
            self._test_result.setText(display_res)
            self._test_result.setProperty("status", "connected")
        except Exception as exc:                          # noqa: BLE001
            err_msg = str(exc)
            display_err = f"Failed: {err_msg[:25]}..." if len(err_msg) > 25 else f"Failed: {err_msg}"
            self._test_result.setText(display_err)
            self._test_result.setProperty("status", "failed")

        self._test_result.style().unpolish(self._test_result)
        self._test_result.style().polish(self._test_result)

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

    def notify(self, title: str, message: str, msecs: int = 2500) -> None:
        if self._settings.get("show_notifications", True):
            self.showMessage(title, message, QSystemTrayIcon.MessageIcon.Information, msecs)


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
        self.setObjectName("InstallerOverlay")
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
        card.setObjectName("InstallerCard")
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 160))
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 22, 24, 22)
        card_layout.setSpacing(14)

        self._title = QLabel("Setting up Local AI Engine")
        self._title.setObjectName("InstallerTitle")
        self._title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._progress = QProgressBar()
        self._progress.setObjectName("InstallerProgress")
        self._progress.setRange(0, 100)
        self._progress.setValue(0)
        self._progress.setTextVisible(False)
        self._progress.setFixedHeight(8)

        self._status = QLabel("Initializing...")
        self._status.setObjectName("InstallerStatus")
        self._status.setProperty("status", "normal")
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status.setWordWrap(True)

        self._note = QLabel("This only happens once.")
        self._note.setObjectName("InstallerNote")
        self._note.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._retry_btn = QPushButton("Retry")
        self._retry_btn.setObjectName("InstallerRetryBtn")
        self._retry_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._retry_btn.setFixedWidth(100)
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
        self._status.setProperty("status", "normal")
        self._status.style().unpolish(self._status)
        self._status.style().polish(self._status)
        self._progress.show()
        self._retry_btn.hide()
        self._note.show()
        self.repaint()
        QApplication.processEvents()

    def show_error(self, message: str) -> None:
        self._title.setText("Setup Failed")
        self._status.setText(message)
        self._status.setProperty("status", "error")
        self._status.style().unpolish(self._status)
        self._status.style().polish(self._status)
        self._progress.hide()
        self._note.hide()
        self._retry_btn.show()
        self.repaint()
        QApplication.processEvents()

    def show_success(self) -> None:
        self._title.setText("Ready!")
        self._status.setText("Local AI engine is running.")
        self._status.setProperty("status", "success")
        self._status.style().unpolish(self._status)
        self._status.style().polish(self._status)
        self._progress.setValue(100)
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

        shadow = QGraphicsDropShadowEffect(self._card)
        shadow.setBlurRadius(50)
        shadow.setXOffset(0)
        shadow.setYOffset(16)
        shadow.setColor(QColor(124, 58, 237, 30))
        self._card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self._card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        # ── Search bar section ───────────────────────────────────────────────
        self._search_container = QWidget()
        self._search_container.setObjectName("paletteSearchSection")
        
        search_layout = QHBoxLayout(self._search_container)
        search_layout.setContentsMargins(12, 8, 12, 8)
        search_layout.setSpacing(10)

        # Magnifier icon
        search_icon = QLabel("⌕")
        search_icon.setObjectName("PaletteSearchIcon")
        search_icon.setFixedWidth(22)

        # Input field
        self._input = QLineEdit()
        self._input.setObjectName("PaletteSearchEdit")
        self._input.setPlaceholderText("Ask AI or search actions...")
        self._input.textChanged.connect(self._on_search_changed)

        # Keyboard shortcut badge
        esc_badge = QLabel("Esc to close")
        esc_badge.setObjectName("PaletteEscBadge")

        search_layout.addWidget(search_icon)
        search_layout.addWidget(self._input, 1)
        search_layout.addWidget(esc_badge)

        # Wrap in layout to add margins inside the card
        search_outer = QVBoxLayout()
        search_outer.setContentsMargins(16, 16, 16, 10)
        search_outer.addWidget(self._search_container)
        card_layout.addLayout(search_outer)

        # ── Divider ──────────────────────────────────────────────────────────
        self._divider = QFrame()
        self._divider.setObjectName("PaletteDivider")
        self._divider.setFrameShape(QFrame.Shape.HLine)
        card_layout.addWidget(self._divider)

        # ── Selected text preview ────────────────────────────────────────────
        self._preview_widget = QWidget()
        self._preview_widget.setObjectName("PalettePreview")
        preview_layout = QHBoxLayout(self._preview_widget)
        preview_layout.setContentsMargins(16, 8, 16, 8)
        preview_layout.setSpacing(8)

        preview_icon = QLabel("↳")
        preview_icon.setObjectName("PalettePreviewIcon")
        preview_icon.setFixedWidth(14)

        self._preview_label = QLabel()
        self._preview_label.setObjectName("PalettePreviewLabel")
        self._preview_label.setWordWrap(False)

        preview_layout.addWidget(preview_icon)
        preview_layout.addWidget(self._preview_label, 1)
        self._preview_widget.hide()
        card_layout.addWidget(self._preview_widget)

        # ── Action list ──────────────────────────────────────────────────────
        list_container = QWidget()
        list_container.setObjectName("PaletteListContainer")
        list_container_layout = QVBoxLayout(list_container)
        list_container_layout.setContentsMargins(8, 6, 8, 10)
        list_container_layout.setSpacing(0)

        self._list = QListWidget()
        self._list.setObjectName("paletteList")
        self._list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._list.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self._list.itemDoubleClicked.connect(self._accept)
        self._list.itemClicked.connect(self._accept)
        list_container_layout.addWidget(self._list)
        card_layout.addWidget(list_container)

        # ── Footer ───────────────────────────────────────────────────────────
        footer = QWidget()
        footer.setObjectName("PaletteFooter")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(16, 7, 16, 7)

        nav_hint = QLabel("↑↓ navigate   ⏎ confirm   Type to filter")
        nav_hint.setObjectName("PaletteNavHint")

        powered = QLabel("Powered by Ollama")
        powered.setObjectName("PalettePowered")

        footer_layout.addWidget(nav_hint)
        footer_layout.addStretch()
        footer_layout.addWidget(powered)
        card_layout.addWidget(footer)

        outer.addWidget(self._card)
        self._input.installEventFilter(self)
        self._populate_list()

    def _style_mode_widget(self, widget: QWidget, selected: bool) -> None:
        layout = widget.layout()
        if not layout or layout.count() < 3:
            return
        icon_label = layout.itemAt(0).widget()
        text_label = layout.itemAt(1).widget()
        enter_hint = layout.itemAt(2).widget()
        
        widget.setProperty("selected", str(selected).lower())
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        
        for child in [icon_label, text_label, enter_hint]:
            if child:
                child.setProperty("selected", str(selected).lower())
                child.style().unpolish(child)
                child.style().polish(child)
                
        if enter_hint:
            if selected:
                enter_hint.show()
            else:
                enter_hint.hide()

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
        widget.setObjectName("PaletteSectionHeaderWidget")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(8, 6, 8, 2)

        label = QLabel(text.upper())
        label.setObjectName("PaletteSectionHeaderLabel")
        layout.addWidget(label)
        layout.addStretch()

        item.setSizeHint(QSize(0, 28))
        return item, widget

    def _make_mode_item(self, label: str, icon: str, mode_id: str, selected: bool = False) -> tuple:
        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, mode_id)

        widget = QWidget()
        widget.setObjectName("ModeItemWidget")
        
        # Icon badge
        icon_label = QLabel(icon)
        icon_label.setObjectName("ModeItemIcon")
        icon_label.setFixedSize(28, 28)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Label
        text_label = QLabel(label)
        text_label.setObjectName("ModeItemText")

        # Enter hint
        enter_hint = QLabel("⏎")
        enter_hint.setObjectName("ModeItemEnter")

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 7, 10, 7)
        layout.setSpacing(10)
        layout.addWidget(icon_label)
        layout.addWidget(text_label, 1)
        layout.addWidget(enter_hint)

        self._style_mode_widget(widget, selected)

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
        self._style_mode_widget(widget, selected)

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
        if obj == self._input:
            if event.type() == event.Type.FocusIn:
                self._search_container.setProperty("focus", "true")
                self._search_container.style().unpolish(self._search_container)
                self._search_container.style().polish(self._search_container)
            elif event.type() == event.Type.FocusOut:
                self._search_container.setProperty("focus", "false")
                self._search_container.style().unpolish(self._search_container)
                self._search_container.style().polish(self._search_container)
            elif event.type() == event.Type.KeyPress:
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
