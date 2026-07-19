# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

# Add resources
datas = [
    ('assets', 'assets'),
    ('public', 'public'),
]

# Check if script exists, and bundle it if it does
scpt_path = Path('get_selected_text.scpt')
if scpt_path.exists():
    datas.append(('get_selected_text.scpt', '.'))

# macOS Info.plist configuration for permissions
info_plist = {
    'NSHighResolutionCapable': 'True',
    'NSPrincipalClass': 'NSApplication',
    'NSAppleEventsUsageDescription': 'Avelyn needs permission to read the active application name to restore focus after enhancing text.',
    'NSAccessibilityUsageDescription': 'Avelyn needs Accessibility permissions to simulate Cmd+C and Cmd+V for reading and writing text automatically.',
    'NSInputMonitoringUsageDescription': 'Avelyn needs Input Monitoring permissions to detect the global hotkey shortcut.',
    'NSMicrophoneUsageDescription': 'Avelyn needs microphone access to listen for your voice commands.',
    'CFBundleIdentifier': 'com.vishwaksen.avelyn',
    'CFBundleName': 'Avelyn',
    'CFBundleDisplayName': 'Avelyn',
    'LSUIElement': True, # Runs as a background/menu bar app (hides from dock)
}

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'pynput.keyboard._darwin',
        'pynput.mouse._darwin',
        'pynput.keyboard._win32',
        'pynput.mouse._win32',
        'urllib.request',
        'urllib.error',
        'zipfile',
        'shutil',
        # macOS AppKit / Foundation bindings
        'objc',
        'AppKit',
        'Foundation',
        'Cocoa',
        # Windows focus restoration
        'win32gui',
        'win32con',
        'win32process',
        'win32api',
        'psutil',
        'psutil._pswindows',
        # Voice packages
        'sounddevice',
        'numpy',
        'scipy',
        'openwakeword',
        'onnxruntime',
        'faster_whisper',
        # Google GenAI SDK
        'google.genai',
        'google.genai.client',
        'google.genai.types',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Avelyn',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None, # e.g. "Developer ID Application: Your Name (TeamID)"
    entitlements_file='Avelyn.entitlements' if sys.platform == 'darwin' else None, # Will be passed when codesign_identity is set
    icon='assets/icon.icns' if sys.platform == 'darwin' else 'assets/icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='Avelyn',
)

if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='Avelyn.app',
        icon='assets/icon.icns',
        bundle_identifier='com.vishwaksen.avelyn',
        info_plist=info_plist,
    )
