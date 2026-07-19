import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QTimer

app = QApplication(sys.argv)

w = QWidget()
w.resize(200, 200)

view_id = w.winId()
try:
    import objc
    view = objc.objc_object(c_void_p=int(view_id))
    window = view.window()
    print("Window:", window)
    if window:
        print("Initial collection behavior:", window.collectionBehavior())
        # NSWindowCollectionBehaviorMoveToActiveSpace = 1 << 1
        # NSWindowCollectionBehaviorFullScreenAuxiliary = 1 << 8
        behavior = window.collectionBehavior()
        behavior |= (1 << 1) | (1 << 8)
        window.setCollectionBehavior_(behavior)
        print("Updated collection behavior:", window.collectionBehavior())
except Exception as e:
    print("Error:", e)

QTimer.singleShot(100, app.quit)
sys.exit(app.exec())
