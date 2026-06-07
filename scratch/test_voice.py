import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

try:
    from AppKit import NSSpeechRecognizer
    import objc
    print("PyObjC / AppKit speech recognizer imported successfully!")
except ImportError as e:
    print(f"Failed to import AppKit speech recognizer: {e}")
    sys.exit(1)

app = QApplication(sys.argv)

# Test creation of NSSpeechRecognizer
recognizer = NSSpeechRecognizer.alloc().init()
if recognizer:
    print("NSSpeechRecognizer successfully instantiated!")
    commands = ["fix grammar", "smart assist", "improve writing"]
    recognizer.setCommands_(commands)
    print("Configured commands:", recognizer.commands())
else:
    print("Failed to instantiate NSSpeechRecognizer.")

QTimer.singleShot(1000, app.quit)
sys.exit(app.exec())
