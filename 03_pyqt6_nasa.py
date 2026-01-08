"""
Hatch Control - PyQt6
=====================
Radio buttons: Open/Closed
Circle (Hatch): Green when Open, Black when Closed
Counter: Increments each time Open is clicked

To run: python 03_pyqt6_nasa.py
Install: pip install PyQt6
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QRadioButton, QGroupBox, QVBoxLayout, QHBoxLayout, QButtonGroup
)
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import Qt, QRectF


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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hatch Control - PyQt6")
        self.resize(600, 420)
        
        # Apply dark stylesheet
        self.setStyleSheet("""
            QMainWindow { background-color: #2b2b2b; }
            QWidget { background-color: #2b2b2b; color: #ffffff; }
            QLabel { background: transparent; }
            QGroupBox { 
                border: 2px solid #555555; 
                border-radius: 5px; 
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title { 
                subcontrol-origin: margin; 
                left: 10px; 
                padding: 0 5px;
            }
            QRadioButton { spacing: 8px; }
            QRadioButton::indicator { width: 18px; height: 18px; }
            QRadioButton::indicator:unchecked {
                border: 2px solid #555555;
                border-radius: 10px;
                background-color: #3a3a3a;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #4CAF50;
                border-radius: 10px;
                background-color: #4CAF50;
            }
        """)
        
        # State
        self.open_click_count = 0
        
        # Central content
        central = QWidget(self)
        self.setCentralWidget(central)
        
        # Title / Number display
        self.lblTitle = QLabel("Number")
        self.lblTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lblTitle.setStyleSheet("font-size: 18px; font-weight: 600;")
        
        self.lblNumber = QLabel("0")
        self.lblNumber.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lblNumber.setStyleSheet("font-size: 26px; color: #3B8ED0;")
        
        # Hatch display (circle)
        self.hatch = HatchWidget()
        
        # Radio buttons
        self.radioOpen = QRadioButton("Open")
        self.radioClosed = QRadioButton("Closed")
        self.radioClosed.setChecked(True)  # default 'Closed' -> black
        
        # Exclusive group (makes sure only one is selected)
        group = QButtonGroup(self)
        group.setExclusive(True)
        group.addButton(self.radioOpen)
        group.addButton(self.radioClosed)
        
        # Wire signals
        self.radioOpen.clicked.connect(self.on_open_clicked)
        self.radioClosed.clicked.connect(self.on_closed_clicked)
        
        # Layouts
        v_root = QVBoxLayout(central)
        
        v_root.addWidget(self.lblTitle)
        v_root.addWidget(self.lblNumber)
        
        # Hatch centered
        v_root.addWidget(self.hatch, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Radio group box
        gb = QGroupBox("State")
        h_radios = QHBoxLayout(gb)
        h_radios.addWidget(self.radioOpen)
        h_radios.addWidget(self.radioClosed)
        h_radios.addStretch(1)
        v_root.addWidget(gb)
        
        # Initialize hatch color
        self.hatch.set_color("black")
    
    def on_open_clicked(self):
        """Open clicked: turn hatch green and increment counter."""
        self.hatch.set_color("green")
        self.open_click_count += 1
        self.lblNumber.setText(str(self.open_click_count))
    
    def on_closed_clicked(self):
        """Closed clicked: turn hatch black (counter unchanged)."""
        self.hatch.set_color("black")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
