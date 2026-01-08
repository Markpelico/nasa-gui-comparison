"""
Hatch Control - Qt Designer with PySide6 Loader
================================================
Loads the .ui file and adds the custom HatchWidget + logic.

To run: python 05_qt_designer_loader.py
Install: pip install PySide6

Note: The .ui file contains a placeholder widget that we replace
with our custom HatchWidget at runtime.
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtGui import QPainter, QPen, QBrush, QColor
from PySide6.QtCore import Qt, QRectF


class HatchWidget(QWidget):
    """A simple widget that draws a large circle (the 'Hatch') in the current color."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._color = QColor("black")  # default: Closed
        self.setMinimumSize(240, 240)
    
    def set_color(self, color):
        self._color = QColor(color)
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        size = min(self.width(), self.height())
        # Center the circle
        rect = QRectF(
            (self.width() - size) / 2,
            (self.height() - size) / 2,
            size,
            size
        )
        # Fill circle
        painter.setBrush(QBrush(self._color))
        painter.setPen(QPen(Qt.GlobalColor.gray, 2))
        painter.drawEllipse(rect)


class HatchController:
    """Controller that loads UI and adds business logic."""
    
    def __init__(self):
        # Load the UI file
        ui_path = Path(__file__).parent / "05_qt_designer_nasa.ui"
        
        loader = QUiLoader()
        ui_file = QFile(str(ui_path))
        
        if not ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
            raise RuntimeError(f"Cannot open UI file: {ui_path}")
        
        self.ui = loader.load(ui_file)
        ui_file.close()
        
        if self.ui is None:
            raise RuntimeError(f"Failed to load UI from: {ui_path}")
        
        # State
        self.open_click_count = 0
        
        # Replace placeholder with actual HatchWidget
        self.hatch = HatchWidget()
        
        # Find and replace the placeholder
        placeholder = self.ui.findChild(QWidget, "hatchPlaceholder")
        if placeholder:
            layout = placeholder.parent().layout()
            index = layout.indexOf(placeholder)
            layout.removeWidget(placeholder)
            placeholder.deleteLater()
            layout.insertWidget(index, self.hatch, 1, Qt.AlignmentFlag.AlignCenter)
        
        # Connect signals
        self.ui.radioOpen.clicked.connect(self.on_open_clicked)
        self.ui.radioClosed.clicked.connect(self.on_closed_clicked)
        
        # Initialize
        self.hatch.set_color("black")
        
        # Show the UI
        self.ui.show()
    
    def on_open_clicked(self):
        """Open clicked: turn hatch green and increment counter."""
        self.hatch.set_color("green")
        self.open_click_count += 1
        self.ui.lblNumber.setText(str(self.open_click_count))
    
    def on_closed_clicked(self):
        """Closed clicked: turn hatch black (counter unchanged)."""
        self.hatch.set_color("black")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = HatchController()
    sys.exit(app.exec())
