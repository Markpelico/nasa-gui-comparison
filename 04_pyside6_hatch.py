"""
Hatch Control GUI - PySide6
===========================
A professional aerospace hatch control interface using Qt6's official Python bindings.
Features smooth animations, glowing effects, and industrial design.

This demonstrates PySide6 (LGPL license) - nearly identical API to PyQt6.

Features:
- Open/Closed radio buttons
- Animated hatch circle with pulsing glow
- LED-style cycle counter

To run: python 04_pyside6_hatch.py
Install: pip install PySide6
"""

import sys
import math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QRadioButton, QButtonGroup, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QTimer, Property, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont, QRadialGradient


class HatchWidget(QWidget):
    """Custom widget that draws an animated hatch indicator with glow effects."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(320, 320)
        self._is_open = False
        self._glow_phase = 0.0
        self._progress = 0.0
        
        # Glow animation timer
        self.glow_timer = QTimer(self)
        self.glow_timer.timeout.connect(self._animate_glow)
        
        # Transition animation
        self._anim = QPropertyAnimation(self, b"progress")
        self._anim.setDuration(450)
        self._anim.setEasingCurve(QEasingCurve.Type.OutQuad)
    
    def get_progress(self):
        return self._progress
    
    def set_progress(self, val):
        self._progress = val
        self.update()
    
    progress = Property(float, get_progress, set_progress)
    
    def set_open(self, is_open: bool):
        """Set the hatch state with smooth animation."""
        self._is_open = is_open
        self._anim.setStartValue(self._progress)
        self._anim.setEndValue(1.0 if is_open else 0.0)
        self._anim.start()
        
        if is_open:
            self.glow_timer.start(40)
        else:
            self.glow_timer.stop()
            self._glow_phase = 0
    
    def _animate_glow(self):
        """Update the glow pulse phase."""
        self._glow_phase = (self._glow_phase + 0.14) % (2 * math.pi)
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        cx, cy = self.width() // 2, self.height() // 2
        radius = min(self.width(), self.height()) // 2 - 50
        p = self._progress
        
        # Dark background
        painter.fillRect(self.rect(), QColor("#0b0b10"))
        
        # Pulse factor for glow
        pulse = 0.65 + 0.35 * math.sin(self._glow_phase) if self._is_open else 1.0
        
        if p > 0.01:
            # === OPEN STATE ===
            # Outer glow rings
            glow_r = radius + 45
            glow = QRadialGradient(cx, cy, glow_r)
            g_intensity = int(120 * p * pulse)
            glow.setColorAt(0.0, QColor(0, g_intensity, 30, 200))
            glow.setColorAt(0.4, QColor(0, g_intensity // 2, 15, 100))
            glow.setColorAt(1.0, QColor(0, 0, 0, 0))
            painter.setBrush(QBrush(glow))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(cx - glow_r, cy - glow_r, glow_r * 2, glow_r * 2)
            
            # Main green circle
            green_val = int(150 + 105 * pulse * p)
            main_grad = QRadialGradient(cx, cy - radius // 3, radius * 1.4)
            main_grad.setColorAt(0.0, QColor(120, 255, 170))
            main_grad.setColorAt(0.35, QColor(0, green_val, 60))
            main_grad.setColorAt(1.0, QColor(0, green_val - 50, 35))
            
            painter.setBrush(QBrush(main_grad))
            painter.setPen(QPen(QColor(0, 255, 120), 4))
            painter.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)
        
        if p < 0.99:
            # === CLOSED STATE ===
            closed_alpha = int(255 * (1 - p))
            
            # Outer dark ring
            painter.setBrush(QBrush(QColor(18, 18, 24, closed_alpha)))
            painter.setPen(QPen(QColor(45, 45, 55, closed_alpha), 3))
            painter.drawEllipse(cx - radius - 12, cy - radius - 12,
                              (radius + 12) * 2, (radius + 12) * 2)
            
            # Main dark hatch
            dark_grad = QRadialGradient(cx, cy - radius // 4, radius * 1.3)
            dark_grad.setColorAt(0.0, QColor(28, 28, 35, closed_alpha))
            dark_grad.setColorAt(1.0, QColor(6, 6, 10, closed_alpha))
            
            painter.setBrush(QBrush(dark_grad))
            painter.setPen(QPen(QColor(55, 55, 65, closed_alpha), 4))
            painter.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)
        
        # Tick marks
        for angle in range(0, 360, 15):
            rad = math.radians(angle)
            length = 14 if angle % 45 == 0 else 7
            x1 = cx + (radius + 15) * math.cos(rad)
            y1 = cy + (radius + 15) * math.sin(rad)
            x2 = cx + (radius + 15 + length) * math.cos(rad)
            y2 = cy + (radius + 15 + length) * math.sin(rad)
            
            tick_color = QColor(0, 200, 90) if p > 0.5 else QColor(50, 50, 62)
            painter.setPen(QPen(tick_color, 2))
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))
        
        # Bolt decorations
        bolt_r = 9
        for angle in [45, 135, 225, 315]:
            rad = math.radians(angle)
            bx = cx + (radius - 28) * math.cos(rad)
            by = cy + (radius - 28) * math.sin(rad)
            bolt_color = QColor(0, 170, 85) if p > 0.5 else QColor(40, 40, 50)
            painter.setBrush(QBrush(bolt_color))
            painter.setPen(QPen(QColor(15, 15, 20), 2))
            painter.drawEllipse(int(bx - bolt_r), int(by - bolt_r), bolt_r * 2, bolt_r * 2)
        
        # Status text
        painter.setFont(QFont("Arial Black", 22))
        if p > 0.5:
            painter.setPen(QColor(0, 35, 10))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "OPEN")
        else:
            painter.setPen(QColor(65, 65, 80))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "CLOSED")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HATCH CONTROL SYSTEM")
        self.setFixedSize(540, 750)
        self.setStyleSheet("background-color: #0b0b10;")
        
        self.open_click_count = 0
        self.setup_ui()
    
    def setup_ui(self):
        central = QWidget(self)
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(0)
        
        # === HEADER ===
        header_frame = QFrame()
        header_frame.setStyleSheet("background: transparent;")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("◈ HATCH CONTROL")
        title.setStyleSheet("""
            color: #ff8844;
            font-size: 34px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)
        
        # Add glow to title
        title_glow = QGraphicsDropShadowEffect()
        title_glow.setBlurRadius(25)
        title_glow.setColor(QColor(255, 136, 68, 120))
        title_glow.setOffset(0, 0)
        title.setGraphicsEffect(title_glow)
        
        subtitle = QLabel("AIRLOCK MODULE A-7  •  DECK 3")
        subtitle.setStyleSheet("color: #505060; font-size: 14px;")
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_frame)
        layout.addSpacing(25)
        
        # === COUNTER ===
        counter_title = QLabel("CYCLE COUNT")
        counter_title.setStyleSheet("color: #606070; font-size: 13px; font-weight: bold;")
        layout.addWidget(counter_title)
        layout.addSpacing(8)
        
        counter_frame = QFrame()
        counter_frame.setStyleSheet("""
            QFrame {
                background-color: #040406;
                border: 2px solid #1a1a22;
                border-radius: 12px;
            }
        """)
        counter_layout = QVBoxLayout(counter_frame)
        
        self.lblNumber = QLabel("0")
        self.lblNumber.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lblNumber.setStyleSheet("""
            color: #ff9955;
            font-size: 72px;
            font-weight: bold;
            font-family: 'Courier New', monospace;
            padding: 12px;
        """)
        
        # Counter glow
        counter_glow = QGraphicsDropShadowEffect()
        counter_glow.setBlurRadius(35)
        counter_glow.setColor(QColor(255, 153, 85, 120))
        counter_glow.setOffset(0, 0)
        self.lblNumber.setGraphicsEffect(counter_glow)
        
        counter_layout.addWidget(self.lblNumber)
        layout.addWidget(counter_frame)
        
        # === HATCH ===
        layout.addSpacing(15)
        hatch_title = QLabel("HATCH STATUS")
        hatch_title.setStyleSheet("color: #606070; font-size: 13px; font-weight: bold;")
        layout.addWidget(hatch_title)
        
        self.hatch = HatchWidget()
        layout.addWidget(self.hatch, 1)
        
        # === CONTROLS ===
        control_frame = QFrame()
        control_frame.setStyleSheet("""
            QFrame {
                background-color: #101018;
                border-radius: 12px;
                padding: 10px;
            }
        """)
        control_layout = QVBoxLayout(control_frame)
        
        control_label = QLabel("CONTROL")
        control_label.setStyleSheet("color: #505060; font-size: 12px; font-weight: bold;")
        control_layout.addWidget(control_label)
        
        radio_row = QHBoxLayout()
        radio_row.setSpacing(45)
        
        self.radioOpen = QRadioButton("OPEN")
        self.radioOpen.setStyleSheet("""
            QRadioButton {
                color: #ddddee;
                font-size: 18px;
                font-weight: bold;
                spacing: 12px;
            }
            QRadioButton::indicator {
                width: 24px;
                height: 24px;
            }
            QRadioButton::indicator:unchecked {
                border: 3px solid #00aa66;
                border-radius: 13px;
                background: #080810;
            }
            QRadioButton::indicator:checked {
                border: 3px solid #00ff99;
                border-radius: 13px;
                background: #00cc77;
            }
        """)
        
        self.radioClosed = QRadioButton("CLOSED")
        self.radioClosed.setChecked(True)
        self.radioClosed.setStyleSheet("""
            QRadioButton {
                color: #ddddee;
                font-size: 18px;
                font-weight: bold;
                spacing: 12px;
            }
            QRadioButton::indicator {
                width: 24px;
                height: 24px;
            }
            QRadioButton::indicator:unchecked {
                border: 3px solid #cc4455;
                border-radius: 13px;
                background: #080810;
            }
            QRadioButton::indicator:checked {
                border: 3px solid #ff6677;
                border-radius: 13px;
                background: #dd4455;
            }
        """)
        
        group = QButtonGroup(self)
        group.setExclusive(True)
        group.addButton(self.radioOpen)
        group.addButton(self.radioClosed)
        
        self.radioOpen.clicked.connect(self.on_open_clicked)
        self.radioClosed.clicked.connect(self.on_closed_clicked)
        
        radio_row.addWidget(self.radioOpen)
        radio_row.addWidget(self.radioClosed)
        radio_row.addStretch()
        control_layout.addLayout(radio_row)
        
        layout.addWidget(control_frame)
        
        # === STATUS ===
        layout.addSpacing(18)
        self.status_label = QLabel("◉ SYSTEM READY")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            color: #00dd88;
            font-size: 14px;
            font-weight: bold;
            font-family: 'Courier New', monospace;
        """)
        layout.addWidget(self.status_label)
        
        # Initial state
        self.hatch.set_open(False)
    
    def on_open_clicked(self):
        """Open clicked: turn hatch green and increment counter."""
        self.hatch.set_open(True)
        self.open_click_count += 1
        self.lblNumber.setText(str(self.open_click_count))
        self.status_label.setText("◉ HATCH OPENING...")
        self.status_label.setStyleSheet(self.status_label.styleSheet().replace("#00dd88", "#ffaa44"))
        QTimer.singleShot(500, lambda: (
            self.status_label.setText("◉ HATCH OPEN - PRESSURIZED"),
            self.status_label.setStyleSheet(self.status_label.styleSheet().replace("#ffaa44", "#00ff88"))
        ))
    
    def on_closed_clicked(self):
        """Closed clicked: turn hatch black (counter unchanged)."""
        self.hatch.set_open(False)
        self.status_label.setText("◉ HATCH SEALED")
        self.status_label.setStyleSheet(self.status_label.styleSheet().replace("#ffaa44", "#00dd88").replace("#00ff88", "#00dd88"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

