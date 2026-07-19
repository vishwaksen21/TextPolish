import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, Qt, QEvent
from PyQt6.QtGui import QKeyEvent
from ui import CommandPalette

def main():
    app = QApplication(sys.argv)
    palette = CommandPalette()
    palette.show_palette(selected_text="test text")
    
    print("Initial list count:", palette._list.count())
    print("Initial current row:", palette._list.currentRow())
    
    # Simulate pressing Key_Down
    print("\n--- Simulating Down Arrow ---")
    event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Down, Qt.KeyboardModifier.NoModifier)
    result = palette.eventFilter(palette._input, event)
    print("Event filtered:", result)
    print("Current row after Down:", palette._list.currentRow())
    
    # Simulate pressing Key_Down again
    print("\n--- Simulating Down Arrow Again ---")
    result = palette.eventFilter(palette._input, event)
    print("Event filtered:", result)
    print("Current row after second Down:", palette._list.currentRow())
    
    # Simulate pressing Key_Down directly on the palette window
    print("\n--- Simulating Down Arrow Directly on Palette Window ---")
    event_direct = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Down, Qt.KeyboardModifier.NoModifier)
    QApplication.sendEvent(palette, event_direct)
    print("Current row after Direct Down:", palette._list.currentRow())
    
    QTimer.singleShot(100, app.quit)
    app.exec()

if __name__ == "__main__":
    main()
