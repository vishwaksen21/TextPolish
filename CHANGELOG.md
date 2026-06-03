# Changelog

All notable changes to the Avelyn project will be documented in this file.

---

## [1.0.0-beta] — 2026-06-03

### Added
*   **Windows Platform Support**: Core engine refactoring to support both Windows (`win32`) and macOS (`darwin`).
*   **Win32 Registry Startup Integration**: Auto-start configuration implemented using native Windows registry keys under `Software\Microsoft\Windows\CurrentVersion\Run`.
*   **Windows Ollama Installer**: Silent downloader, installer, and service starter for the standalone Windows Ollama client.
*   **Windows Package Specification**: Configured `Avelyn.spec` with all Windows-specific imports (`win32gui`, `win32con`, `win32process`, `win32api`, `psutil`) for PyInstaller executable compiling.

### Fixed
*   **Physical Modifier Keys Collision**: Implemented a physical modifier key check loop in `platform_handler.py` that waits up to 500ms for modifier key release. This resolves the `Ctrl+Shift+C` collision and ensures standard `Ctrl+C` triggers successfully.
*   **Onboarding Index Lockups**: Replaced hardcoded integer step indices in `onboarding.py` with dynamic stack widget reference identity checks, fixing the setup retry button on Windows.
*   **Branding Uniformity**: Replaced all remaining user-facing references of the legacy name `"TextPolish"` with `"Avelyn"` in tray tooltips, popup headers, menus, and notification boxes.
*   **System Tray Setting Action**: Modified the system tray activation handler in `ui.py` so that double-click is required to open the Settings pane on Windows, preventing settings from launching on single left-click events.
