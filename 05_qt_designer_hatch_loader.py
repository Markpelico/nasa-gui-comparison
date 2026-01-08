"""
Hatch Control GUI - Qt Designer + PySide6 Loader
=================================================
This script loads a .ui file created with Qt Designer and adds the
business logic (animations, counter, state management).

WORKFLOW:
1. Design UI visually in Qt Designer (pyside6-designer)
2. Save as .ui file
3. Load in Python using QUiLoader
4. Connect signals and add custom behavior

To run: python 05_qt_designer_hatch_loader.py
Install: pip install PySide6

Launch Qt Designer: pyside6-designer
"""

import sys
import math
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QTimer, QIODevice
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QRadialGradient


class AnimatedHatchWidget(QWidget):
    """
    Custom animated hatch widget to replace the static placeholder from Qt Designer.
    This demonstrates how to add custom painted widgets alongside .ui files.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(280, 280)
        self._is_open = False
        self._glow_phase = 0.0
        self._progress = 0.0
        self._target_progress = 0.0
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(40)
    
    def set_open(self, is_open: bool):
        """Set hatch state with animation."""
        self._is_open = is_open
        self._target_progress = 1.0 if is_open else 0.0
    
    def _animate(self):
        """Update animation state."""
        # Smooth transition
        diff = self._target_progress - self._progress
        self._progress += diff * 0.12
        
        # Glow pulse when open
        if self._is_open:
            self._glow_phase = (self._glow_phase + 0.14) % (2 * math.pi)
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        cx, cy = self.width() // 2, self.height() // 2
        radius = min(self.width(), self.height()) // 2 - 25
        p = self._progress
        
        # Background
        painter.fillRect(self.rect(), QColor("#0c0c14"))
        
        pulse = 0.65 + 0.35 * math.sin(self._glow_phase) if self._is_open else 1.0
        
        if p > 0.01:
            # Glow effect
            glow_r = radius + 35
            glow = QRadialGradient(cx, cy, glow_r)
            g = int(100 * p * pulse)
            glow.setColorAt(0.0, QColor(0, g, 25, 180))
            glow.setColorAt(0.5, QColor(0, g // 2, 10, 80))
            glow.setColorAt(1.0, QColor(0, 0, 0, 0))
            painter.setBrush(QBrush(glow))
            painter.setPen(QPen(QColor(0, 0, 0, 0)))
            painter.drawEllipse(cx - glow_r, cy - glow_r, glow_r * 2, glow_r * 2)
            
            # Main green circle
            green = int(140 + 115 * pulse * p)
            grad = QRadialGradient(cx, cy - radius // 3, radius * 1.4)
            grad.setColorAt(0.0, QColor(100, 255, 160))
            grad.setColorAt(0.35, QColor(0, green, 50))
            grad.setColorAt(1.0, QColor(0, green - 45, 30))
            painter.setBrush(QBrush(grad))
            painter.setPen(QPen(QColor(0, 255, 100), 4))
            painter.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)
        
        if p < 0.99:
            alpha = int(255 * (1 - p))
            
            # Dark ring
            painter.setBrush(QBrush(QColor(15, 15, 22, alpha)))
            painter.setPen(QPen(QColor(40, 40, 52, alpha), 3))
            painter.drawEllipse(cx - radius - 10, cy - radius - 10,
                              (radius + 10) * 2, (radius + 10) * 2)
            
            # Dark circle
            dark = QRadialGradient(cx, cy - radius // 4, radius * 1.3)
            dark.setColorAt(0.0, QColor(25, 25, 32, alpha))
            dark.setColorAt(1.0, QColor(5, 5, 10, alpha))
            painter.setBrush(QBrush(dark))
            painter.setPen(QPen(QColor(50, 50, 60, alpha), 4))
            painter.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)
        
        # Tick marks
        for angle in range(0, 360, 15):
            rad = math.radians(angle)
            length = 12 if angle % 45 == 0 else 6
            x1 = cx + (radius + 10) * math.cos(rad)
            y1 = cy + (radius + 10) * math.sin(rad)
            x2 = cx + (radius + 10 + length) * math.cos(rad)
            y2 = cy + (radius + 10 + length) * math.sin(rad)
            color = QColor(0, 180, 80) if p > 0.5 else QColor(45, 45, 58)
            painter.setPen(QPen(color, 2))
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))
        
        # Bolts
        bolt_r = 8
        for angle in [45, 135, 225, 315]:
            rad = math.radians(angle)
            bx = cx + (radius - 25) * math.cos(rad)
            by = cy + (radius - 25) * math.sin(rad)
            color = QColor(0, 160, 80) if p > 0.5 else QColor(38, 38, 48)
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(QColor(12, 12, 18), 2))
            painter.drawEllipse(int(bx - bolt_r), int(by - bolt_r), bolt_r * 2, bolt_r * 2)


class HatchController:
    """
    Controller that loads the .ui file and adds interactivity.
    """
    
    def __init__(self):
        # Load the .ui file
        ui_path = Path(__file__).parent / "05_qt_designer_hatch.ui"
        
        loader = QUiLoader()
        ui_file = QFile(str(ui_path))
        
        if not ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
            raise RuntimeError(f"Cannot open UI file: {ui_path}")
        
        self.window = loader.load(ui_file)
        ui_file.close()
        
        if self.window is None:
            raise RuntimeError(f"Failed to load UI from: {ui_path}")
        
        # State
        self.open_count = 0
        
        # Create custom animated hatch widget
        self.hatch_widget = AnimatedHatchWidget()
        
        # Replace the placeholder with our custom widget
        # First, get the placeholder and its parent layout
        placeholder = self.window.findChild(QWidget, "hatchPlaceholder")
        if placeholder:
            parent_layout = placeholder.parent().layout()
            if parent_layout:
                # Find the index of the placeholder
                index = parent_layout.indexOf(placeholder)
                # Remove placeholder
                placeholder.hide()
                parent_layout.removeWidget(placeholder)
                # Insert our custom widget
                parent_layout.insertWidget(index, self.hatch_widget)
        
        # Connect signals
        self.window.radioOpen.clicked.connect(self.on_open_clicked)
        self.window.radioClosed.clicked.connect(self.on_closed_clicked)
        
        # Show window
        self.window.show()
    
    def on_open_clicked(self):
        """Handle Open radio button click."""
        self.open_count += 1
        self.window.numberDisplay.setText(str(self.open_count))
        self.hatch_widget.set_open(True)
        
        # Update hatch status label (if it still exists)
        if hasattr(self.window, 'hatchStatusLabel'):
            self.window.hatchStatusLabel.setText("OPEN")
            self.window.hatchStatusLabel.setStyleSheet("""
                color: #00ff88;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
            """)
        
        # Update status
        self.window.statusLabel.setText("◉ HATCH OPENING...")
        self.window.statusLabel.setStyleSheet("""
            color: #ffcc44;
            font-size: 13px;
            font-weight: bold;
            font-family: 'Courier New', monospace;
            background: transparent;
            margin-top: 12px;
        """)
        
        # Delayed status update
        QTimer.singleShot(500, self._update_status_open)
    
    def _update_status_open(self):
        """Update status after hatch opens."""
        self.window.statusLabel.setText("◉ HATCH OPEN - PRESSURIZED")
        self.window.statusLabel.setStyleSheet("""
            color: #00ff88;
            font-size: 13px;
            font-weight: bold;
            font-family: 'Courier New', monospace;
            background: transparent;
            margin-top: 12px;
        """)
    
    def on_closed_clicked(self):
        """Handle Closed radio button click."""
        self.hatch_widget.set_open(False)
        
        if hasattr(self.window, 'hatchStatusLabel'):
            self.window.hatchStatusLabel.setText("CLOSED")
            self.window.hatchStatusLabel.setStyleSheet("""
                color: #404058;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
            """)
        
        self.window.statusLabel.setText("◉ HATCH SEALED")
        self.window.statusLabel.setStyleSheet("""
            color: #00dd88;
            font-size: 13px;
            font-weight: bold;
            font-family: 'Courier New', monospace;
            background: transparent;
            margin-top: 12px;
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = HatchController()
    sys.exit(app.exec())

