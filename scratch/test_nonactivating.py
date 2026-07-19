import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test_nonactivating")

class NonActivatingWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Set Tool style to force NSPanel underlying window
        self.setWindowFlags(
            Qt.WindowType.Tool | 
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        layout = QVBoxLayout(self)
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Type something here...")
        layout.addWidget(self.input_field)
        self.resize(400, 100)
        self.move(500, 300)
        
        # Configure NSWindow/NSPanel properties
        QTimer.singleShot(0, self._pre_configure)

    def _pre_configure(self):
        try:
            import objc
            from ctypes import c_void_p
            view = objc.objc_object(c_void_p=int(self.winId()))
            window = view.window()
            if window:
                # 1. Collection behavior: join all spaces and auxiliary on fullscreen
                NSWindowCollectionBehaviorCanJoinAllSpaces = 1 << 0
                NSWindowCollectionBehaviorTransient = 1 << 3
                NSWindowCollectionBehaviorFullScreenAuxiliary = 1 << 8
                
                window.setCollectionBehavior_(
                    NSWindowCollectionBehaviorCanJoinAllSpaces |
                    NSWindowCollectionBehaviorTransient |
                    NSWindowCollectionBehaviorFullScreenAuxiliary
                )
                
                # 2. Non-activating style mask
                NSWindowStyleMaskNonactivatingPanel = 1 << 7
                current_style = window.styleMask()
                window.setStyleMask_(current_style | NSWindowStyleMaskNonactivatingPanel)
                
                # 3. Prevent hiding when app is inactive
                window.setHidesOnDeactivate_(False)
                
                # 4. Key window setup
                window.setBecomesKeyOnlyIfNeeded_(False)
                window.setFloatingPanel_(True)
                
                # 5. Set higher window level (Status/ScreenSaver or Floating)
                # Floating is level 3, Status is level 25. Let's try NSStatusWindowLevel = 25
                window.setLevel_(25)
                
                logger.info("Window pre-configured.")
        except Exception as e:
            logger.error("Pre-configure error: %s", e)

    def trigger_show(self):
        logger.info("trigger_show called.")
        import sys
        if sys.platform == "darwin":
            try:
                import objc
                from ctypes import c_void_p
                from AppKit import NSWorkspace
                
                active_app_before = "Unknown"
                front_app = NSWorkspace.sharedWorkspace().frontmostApplication()
                if front_app:
                    active_app_before = f"{front_app.localizedName()} ({front_app.bundleIdentifier()})"
                logger.info("ACTIVE_APP_BEFORE_SHOW: %s", active_app_before)
                logger.info("PALETTE_SHOW_REQUESTED")

                # Set visible to True for Qt logic
                self.setVisible(True)
                
                # Retrieve native window
                view = objc.objc_object(c_void_p=int(self.winId()))
                window = view.window()
                logger.info("PALETTE_WINDOW_CREATED")
                
                # Show native window using orderFrontRegardless
                logger.info("PALETTE_ORDER_FRONT")
                window.orderFrontRegardless()
                
                # Set Qt focus internally, or first responder
                window.makeFirstResponder_(objc.objc_object(c_void_p=int(self.input_field.winId())))
                
                # Wait a tiny bit and check state
                QTimer.singleShot(100, self.check_state)
            except Exception as e:
                logger.error("Show error: %s", e)
        else:
            self.show()
            self.input_field.setFocus()

    def check_state(self):
        try:
            import objc
            from ctypes import c_void_p
            from AppKit import NSWorkspace
            
            view = objc.objc_object(c_void_p=int(self.winId()))
            window = view.window()
            
            active_app_after = "Unknown"
            front_app = NSWorkspace.sharedWorkspace().frontmostApplication()
            if front_app:
                active_app_after = f"{front_app.localizedName()} ({front_app.bundleIdentifier()})"
            logger.info("ACTIVE_APP_AFTER_SHOW: %s", active_app_after)
            
            logger.info("Is key window: %s", window.isKeyWindow())
            if window.isKeyWindow():
                logger.info("PALETTE_BECAME_KEY")
                
            first_resp = window.firstResponder()
            logger.info("First responder: %s", first_resp)
            if first_resp:
                logger.info("PALETTE_RECEIVED_FOCUS")
                
        except Exception as e:
            logger.error("Check state error: %s", e)

def main():
    app = QApplication(sys.argv)
    w = NonActivatingWindow()
    
    # Show after 2 seconds to give user time to focus another window (e.g. terminal or browser)
    QTimer.singleShot(2000, w.trigger_show)
    
    # Exit after 10 seconds so the test doesn't hang forever
    QTimer.singleShot(10000, app.quit)
    
    app.exec()

if __name__ == "__main__":
    main()
