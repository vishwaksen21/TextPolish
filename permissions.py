"""
TextPolish — Permission Manager
================================
macOS: checks and requests Accessibility + Input Monitoring via TCC.
Windows: no equivalent permission system — all checks return True.
Linux: no equivalent — all checks return True.
"""

import sys
import platform
import subprocess
from logger import logger


IS_MACOS   = sys.platform == "darwin"
IS_WINDOWS = sys.platform == "win32"


class PermissionManager:
    """Manages system permissions. macOS only; Windows/Linux always return True."""

    @staticmethod
    def is_macos() -> bool:
        return IS_MACOS

    @staticmethod
    def is_windows() -> bool:
        return IS_WINDOWS

    @staticmethod
    def check_accessibility() -> bool:
        """
        macOS: checks AXIsProcessTrusted via CoreGraphics.
        Windows/Linux: always True — no Accessibility TCC equivalent exists.
        """
        if not IS_MACOS:
            return True

        try:
            import ctypes
            import ctypes.util

            lib_path = ctypes.util.find_library('ApplicationServices')
            if not lib_path:
                logger.warning("Could not find ApplicationServices library.")
                return False

            app_services = ctypes.cdll.LoadLibrary(lib_path)
            is_trusted = app_services.AXIsProcessTrusted()
            return bool(is_trusted)

        except Exception as e:
            logger.error("Error checking accessibility permissions: %s", e)
            return False

    @staticmethod
    def request_accessibility() -> None:
        """
        macOS: opens System Settings → Accessibility.
        Windows/Linux: no-op.
        """
        if not IS_MACOS:
            return

        logger.info("Opening macOS System Settings -> Accessibility")
        try:
            subprocess.run([
                "open",
                "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
            ], check=False)
        except Exception as e:
            logger.error("Failed to open System Settings: %s", e)

    @staticmethod
    def request_input_monitoring() -> None:
        """
        macOS: opens System Settings → Input Monitoring.
        Windows/Linux: no-op.
        """
        if not IS_MACOS:
            return

        logger.info("Opening macOS System Settings -> Input Monitoring")
        try:
            subprocess.run([
                "open",
                "x-apple.systempreferences:com.apple.preference.security?Privacy_ListenEvent"
            ], check=False)
        except Exception as e:
            logger.error("Failed to open System Settings (Input Monitoring): %s", e)

    @staticmethod
    def check_input_monitoring() -> bool:
        """
        macOS: tests whether Input Monitoring permission is granted using IOKit.
        Windows/Linux: always True — no permission required for global hotkeys.
        """
        if not IS_MACOS:
            return True

        try:
            import ctypes
            import ctypes.util
            # Resolve and load IOKit framework path dynamically
            lib_path = ctypes.util.find_library('IOKit')
            if not lib_path:
                logger.warning("Could not find IOKit library.")
                return False
            iokit = ctypes.cdll.LoadLibrary(lib_path)
            # IOHIDCheckAccess C prototype: IOHIDAccessType IOHIDCheckAccess(IOHIDRequestType requestType);
            # kIOHIDRequestTypeListenEvent = 0
            # kIOHIDAccessTypeGranted = 0
            access_type = iokit.IOHIDCheckAccess(0)
            return access_type == 0
        except Exception as e:
            logger.error("Input monitoring check failed via IOHIDCheckAccess: %s", e)
            return False
