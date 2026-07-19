import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt

class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.Tool | 
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        layout = QVBoxLayout(self)
        self.input_field = QLineEdit(self)
        layout.addWidget(self.input_field)
        self.resize(300, 200)
        self.move(500, 300)
        
        # Configure NSWindow collections at startup
        QTimer.singleShot(0, self._pre_configure)

    def _pre_configure(self):
        try:
            import objc
            from ctypes import c_void_p
            view = objc.objc_object(c_void_p=int(self.winId()))
            window = view.window()
            if window:
                NSWindowCollectionBehaviorCanJoinAllSpaces = 1 << 0
                NSWindowCollectionBehaviorTransient = 1 << 3
                NSWindowCollectionBehaviorFullScreenAuxiliary = 1 << 8
                
                window.setCollectionBehavior_(
                    NSWindowCollectionBehaviorCanJoinAllSpaces |
                    NSWindowCollectionBehaviorTransient |
                    NSWindowCollectionBehaviorFullScreenAuxiliary
                )
                window.setBecomesKeyOnlyIfNeeded_(False)
                window.setFloatingPanel_(True)
                print("Pre-configured window collection behavior.")
        except Exception as e:
            print("Pre-configure error:", e)

    def trigger_show(self):
        print("trigger_show called.")
        # Activate app to make it key, but since CanJoinAllSpaces is set, it should not switch spaces
        import sys
        if sys.platform == "darwin":
            try:
                import objc
                from ctypes import c_void_p
                view = objc.objc_object(c_void_p=int(self.winId()))
                window = view.window()
                
                # Show window
                self.setVisible(True)
                
                # Activate application ignoring other apps
                from AppKit import NSApplication, NSApplicationActivateIgnoringOtherApps
                # On macOS, NSApp is the shared NSApplication instance
                app = NSApplication.sharedApplication()
                app.activateIgnoringOtherApps_(True)
                
                # Make window key
                window.makeKeyAndOrderFront_(None)
                window.makeFirstResponder_(objc.objc_object(c_void_p=int(self.input_field.winId())))
            except Exception as e:
                print("Darwin native activation error:", e)
                self.show()
                self.raise_()
                self.activateWindow()
                self.input_field.setFocus()
        else:
            self.show()
            self.raise_()
            self.activateWindow()
            self.input_field.setFocus()

def test():
    app = QApplication(sys.argv)
    w = TestWindow()
    
    # Simulate hotkey fire after 1 second
    QTimer.singleShot(1000, w.trigger_show)
    
    # Wait and check
    def check():
        import objc
        from ctypes import c_void_p
        view = objc.objc_object(c_void_p=int(w.winId()))
        window = view.window()
        if window:
            print("Is active application:", NSWorkspace.sharedWorkspace().frontmostApplication().bundleIdentifier())
            print("Is key window:", window.isKeyWindow())
        app.quit()
        
    QTimer.singleShot(2500, check)
    app.exec()

if __name__ == "__main__":
    from AppKit import NSWorkspace
    test()
