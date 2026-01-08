"""
Hatch Control GUI - PyQt6
=========================
A professional aerospace-grade hatch control interface with smooth animations,
glowing effects, and industrial design elements.

Features:
- Open/Closed radio buttons
- Animated hatch indicator with pulsing glow
- LED-style cycle counter
- Smooth Qt animations

To run: python 03_pyqt6_hatch.py
Install: pip install PyQt6
"""

import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QRadioButton, QButtonGroup, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QFont, QRadialGradient, QLinearGradient


class HatchIndicator(QWidget):
    """Custom widget that draws an animated hatch status indicator."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(320, 320)
        self._is_open = False
        self._glow_phase = 0.0
        self._open_progress = 0.0
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_animation)
        
        # Smooth transition animation
        self._animation = QPropertyAnimation(self, b"open_progress")
        self._animation.setDuration(400)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def get_open_progress(self):
        return self._open_progress
    
    def set_open_progress(self, value):
        self._open_progress = value
        self.update()
    
    open_progress = pyqtProperty(float, get_open_progress, set_open_progress)
    
    def set_open(self, is_open: bool):
        """Set hatch state with animation."""
        self._is_open = is_open
        self._animation.setStartValue(self._open_progress)
        self._animation.setEndValue(1.0 if is_open else 0.0)
        self._animation.start()
        
        if is_open:
            self.timer.start(35)
        else:
            self.timer.stop()
            self._glow_phase = 0
    
    def _update_animation(self):
        """Update glow animation phase."""
        self._glow_phase = (self._glow_phase + 0.15) % (2 * math.pi)
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        cx, cy = self.width() // 2, self.height() // 2
        radius = min(self.width(), self.height()) // 2 - 50
        progress = self._open_progress
        
        # Background
        painter.fillRect(self.rect(), QColor("#0d0d14"))
        
        if progress > 0.01:
            # Calculate glow intensity
            pulse = 0.6 + 0.4 * math.sin(self._glow_phase) if self._is_open else 1.0
            
            # Outer glow (radial gradient)
            glow_radius = radius + 40
            glow_gradient = QRadialGradient(cx, cy, glow_radius)
            green_intensity = int(100 * progress * pulse)
            glow_gradient.setColorAt(0, QColor(0, green_intensity, 0, 180))
            glow_gradient.setColorAt(0.5, QColor(0, green_intensity // 2, 0, 80))
            glow_gradient.setColorAt(1, QColor(0, 0, 0, 0))
            painter.setBrush(QBrush(glow_gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(cx - glow_radius, cy - glow_radius, 
                              glow_radius * 2, glow_radius * 2)
            
            # Main hatch circle (green)
            green_val = int(140 + 115 * pulse * progress)
            main_gradient = QRadialGradient(cx, cy - radius // 3, radius * 1.5)
            main_gradient.setColorAt(0, QColor(100, 255, 150))
            main_gradient.setColorAt(0.3, QColor(0, green_val, 50))
            main_gradient.setColorAt(1, QColor(0, green_val - 40, 30))
            
            painter.setBrush(QBrush(main_gradient))
            painter.setPen(QPen(QColor(0, 255, 100), 4))
            painter.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)
        
        if progress < 0.99:
            # Closed state overlay
            closed_alpha = int(255 * (1 - progress))
            
            # Outer ring
            painter.setBrush(QBrush(QColor(20, 20, 25, closed_alpha)))
            painter.setPen(QPen(QColor(50, 50, 60, closed_alpha), 3))
            painter.drawEllipse(cx - radius - 10, cy - radius - 10, 
                              (radius + 10) * 2, (radius + 10) * 2)
            
            # Main dark circle
            dark_gradient = QRadialGradient(cx, cy - radius // 4, radius * 1.2)
            dark_gradient.setColorAt(0, QColor(30, 30, 35, closed_alpha))
            dark_gradient.setColorAt(1, QColor(8, 8, 12, closed_alpha))
            
            painter.setBrush(QBrush(dark_gradient))
            painter.setPen(QPen(QColor(60, 60, 70, closed_alpha), 4))
            painter.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)
        
        # Draw tick marks
        self._draw_ticks(painter, cx, cy, radius, progress)
        
        # Draw bolt decorations
        self._draw_bolts(painter, cx, cy, radius, progress)
        
        # Status text
        painter.setFont(QFont("Arial Black", 22))
        if progress > 0.5:
            painter.setPen(QColor(0, 40, 10))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "OPEN")
        else:
            painter.setPen(QColor(70, 70, 85))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "CLOSED")
    
    def _draw_ticks(self, painter, cx, cy, radius, progress):
        """Draw tick marks around the hatch."""
        for angle in range(0, 360, 15):
            rad = math.radians(angle)
            length = 15 if angle % 45 == 0 else 8
            
            x1 = cx + (radius + 12) * math.cos(rad)
            y1 = cy + (radius + 12) * math.sin(rad)
            x2 = cx + (radius + 12 + length) * math.cos(rad)
            y2 = cy + (radius + 12 + length) * math.sin(rad)
            
            if progress > 0.5:
                color = QColor(0, 200, 80)
            else:
                color = QColor(50, 50, 60)
            
            painter.setPen(QPen(color, 2))
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))
    
    def _draw_bolts(self, painter, cx, cy, radius, progress):
        """Draw decorative bolt heads."""
        bolt_radius = 10
        for angle in [45, 135, 225, 315]:
            rad = math.radians(angle)
            bx = cx + (radius - 30) * math.cos(rad)
            by = cy + (radius - 30) * math.sin(rad)
            
            if progress > 0.5:
                color = QColor(0, 180, 80)
            else:
                color = QColor(45, 45, 55)
            
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(QColor(20, 20, 25), 2))
            painter.drawEllipse(int(bx - bolt_radius), int(by - bolt_radius),
                              bolt_radius * 2, bolt_radius * 2)


class HatchControlWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HATCH CONTROL SYSTEM")
        self.setFixedSize(540, 750)
        self.setStyleSheet("background-color: #0d0d14;")
        
        # State
        self.open_count = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(0)
        
        # === HEADER ===
        title = QLabel("◈ HATCH CONTROL")
        title.setStyleSheet("""
            color: #00ddff;
            font-size: 34px;
            font-weight: bold;
            font-family: 'Segoe UI', Arial;
        """)
        layout.addWidget(title)
        
        subtitle = QLabel("AIRLOCK MODULE A-7  •  DECK 3")
        subtitle.setStyleSheet("color: #505068; font-size: 14px; margin-bottom: 25px;")
        layout.addWidget(subtitle)
        
        # === COUNTER SECTION ===
        counter_label = QLabel("CYCLE COUNT")
        counter_label.setStyleSheet("color: #606078; font-size: 13px; font-weight: bold; margin-top: 15px;")
        layout.addWidget(counter_label)
        
        counter_frame = QFrame()
        counter_frame.setStyleSheet("""
            QFrame {
                background-color: #050508;
                border-radius: 10px;
                margin-top: 8px;
            }
        """)
        counter_layout = QVBoxLayout(counter_frame)
        
        self.counter_display = QLabel("0")
        self.counter_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.counter_display.setStyleSheet("""
            color: #00ff99;
            font-size: 72px;
            font-weight: bold;
            font-family: 'Courier New', monospace;
            padding: 15px;
        """)
        
        # Add glow effect to counter
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(30)
        glow.setColor(QColor(0, 255, 150, 100))
        glow.setOffset(0, 0)
        self.counter_display.setGraphicsEffect(glow)
        
        counter_layout.addWidget(self.counter_display)
        layout.addWidget(counter_frame)
        
        # === HATCH INDICATOR ===
        hatch_label = QLabel("HATCH STATUS")
        hatch_label.setStyleSheet("color: #606078; font-size: 13px; font-weight: bold; margin-top: 20px;")
        layout.addWidget(hatch_label)
        
        self.hatch = HatchIndicator()
        layout.addWidget(self.hatch, 1)
        
        # === CONTROL PANEL ===
        control_frame = QFrame()
        control_frame.setStyleSheet("""
            QFrame {
                background-color: #12121a;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        control_layout = QVBoxLayout(control_frame)
        
        control_title = QLabel("CONTROL")
        control_title.setStyleSheet("color: #505068; font-size: 12px; font-weight: bold;")
        control_layout.addWidget(control_title)
        
        # Radio buttons
        radio_layout = QHBoxLayout()
        radio_layout.setSpacing(50)
        
        self.button_group = QButtonGroup(self)
        
        self.open_radio = QRadioButton("OPEN")
        self.open_radio.setStyleSheet("""
            QRadioButton {
                color: #ccccdd;
                font-size: 18px;
                font-weight: bold;
                spacing: 12px;
            }
            QRadioButton::indicator {
                width: 24px;
                height: 24px;
            }
            QRadioButton::indicator:unchecked {
                border: 3px solid #00aa55;
                border-radius: 13px;
                background: #0a0a0f;
            }
            QRadioButton::indicator:checked {
                border: 3px solid #00ff88;
                border-radius: 13px;
                background: #00cc66;
            }
        """)
        
        self.closed_radio = QRadioButton("CLOSED")
        self.closed_radio.setChecked(True)
        self.closed_radio.setStyleSheet("""
            QRadioButton {
                color: #ccccdd;
                font-size: 18px;
                font-weight: bold;
                spacing: 12px;
            }
            QRadioButton::indicator {
                width: 24px;
                height: 24px;
            }
            QRadioButton::indicator:unchecked {
                border: 3px solid #aa3344;
                border-radius: 13px;
                background: #0a0a0f;
            }
            QRadioButton::indicator:checked {
                border: 3px solid #ff5566;
                border-radius: 13px;
                background: #cc3344;
            }
        """)
        
        self.button_group.addButton(self.open_radio)
        self.button_group.addButton(self.closed_radio)
        
        self.open_radio.clicked.connect(self.on_open)
        self.closed_radio.clicked.connect(self.on_closed)
        
        radio_layout.addWidget(self.open_radio)
        radio_layout.addWidget(self.closed_radio)
        radio_layout.addStretch()
        
        control_layout.addLayout(radio_layout)
        layout.addWidget(control_frame)
        
        # === STATUS BAR ===
        self.status_label = QLabel("◉ SYSTEM READY")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            color: #00dd88;
            font-size: 14px;
            font-weight: bold;
            font-family: 'Courier New', monospace;
            margin-top: 20px;
        """)
        layout.addWidget(self.status_label)
    
    def on_open(self):
        """Handle Open button click."""
        self.open_count += 1
        self.counter_display.setText(str(self.open_count))
        self.hatch.set_open(True)
        self.status_label.setText("◉ HATCH OPENING...")
        self.status_label.setStyleSheet(self.status_label.styleSheet().replace("#00dd88", "#ffcc00"))
        QTimer.singleShot(500, self._update_status_open)
    
    def _update_status_open(self):
        self.status_label.setText("◉ HATCH OPEN - PRESSURIZED")
        self.status_label.setStyleSheet(self.status_label.styleSheet().replace("#ffcc00", "#00ff88"))
    
    def on_closed(self):
        """Handle Closed button click."""
        self.hatch.set_open(False)
        self.status_label.setText("◉ HATCH SEALED")
        self.status_label.setStyleSheet(self.status_label.styleSheet().replace("#ffcc00", "#00dd88").replace("#00ff88", "#00dd88"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HatchControlWindow()
    window.show()
    sys.exit(app.exec())

