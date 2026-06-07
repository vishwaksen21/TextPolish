import sys
import time
from PyQt6.QtCore import QCoreApplication
from hotkeys import HotkeyBridge, HotkeyManager
from clipboard_manager import ClipboardManager

def test_hotkey_manager():
    # We need a QCoreApplication (or QApplication) to instantiate QObjects/signals
    app = QCoreApplication(sys.argv)
    
    bridge = HotkeyBridge()
    manager = HotkeyManager(bridge, hotkey="<ctrl>+<shift>+e")
    
    print("Starting HotkeyManager...")
    manager.start()
    
    time.sleep(1.0)
    
    print("Stopping HotkeyManager...")
    manager.stop()
    print("HotkeyManager stopped successfully.")

if __name__ == '__main__':
    test_hotkey_manager()
