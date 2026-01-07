"""
NASA GUI Example - PySide6
==========================
PySide6 is the official Qt for Python binding, offering similar functionality 
to PyQt6 but with LGPL licensing. The API is nearly identical to PyQt6.

To run: python 04_pyside6_nasa.py
Install: pip install PySide6

KEY DIFFERENCES FROM PyQt6:
- Import from PySide6 instead of PyQt6
- Signal/slot syntax slightly different (Signal vs pyqtSignal)
- exec() instead of exec_() (both use exec() in Qt6 versions)
- Some enum access differs
"""

import sys
import random
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QRadioButton, QButtonGroup, QFrame, QPushButton,
    QGridLayout, QGroupBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont


class DigitalDisplay(QLabel):
    """Custom widget for LED-style digital display"""
    def __init__(self, initial_value="000000"):
        super().__init__(initial_value)
        self.setStyleSheet("""
            QLabel {
                background-color: #000000;
                color: #FF6600;
                border: 2px solid #444444;
                border-radius: 5px;
                padding: 10px 15px;
                font-family: 'Courier New', monospace;
                font-size: 28px;
                font-weight: bold;
            }
        """)
        self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.setMinimumWidth(180)


class NASAControlPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NASA Control Panel - PySide6")
        self.setMinimumSize(650, 550)
        
        # NASA colors - using orange theme to differentiate from PyQt6
        self.nasa_blue = "#0B3D91"
        self.accent_orange = "#FF6600"
        self.digital_color = "#FF6600"
        
        # State variables
        self.current_mode = "standby"
        self.telemetry = {
            "altitude": 0,
            "velocity": 0,
            "fuel": 100.0,
            "temperature": 72.5
        }
        
        # Apply dark stylesheet with orange accents
        self.setStyleSheet(self._get_stylesheet())
        
        self.setup_ui()
        self.setup_timer()
    
    def _get_stylesheet(self):
        return f"""
            QMainWindow {{
                background-color: #16213e;
            }}
            QWidget {{
                background-color: #16213e;
                color: #e8e8e8;
            }}
            QGroupBox {{
                border: 2px solid #0f3460;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                font-size: 12px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: {self.accent_orange};
            }}
            QRadioButton {{
                spacing: 8px;
                font-size: 13px;
            }}
            QRadioButton::indicator {{
                width: 18px;
                height: 18px;
            }}
            QRadioButton::indicator:unchecked {{
                border: 2px solid #555555;
                border-radius: 10px;
                background-color: #1a1a2e;
            }}
            QRadioButton::indicator:checked {{
                border: 2px solid {self.accent_orange};
                border-radius: 10px;
                background-color: {self.accent_orange};
            }}
            QPushButton {{
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton#abort {{
                background-color: #e94560;
                border: none;
                color: white;
            }}
            QPushButton#abort:hover {{
                background-color: #c73e54;
            }}
            QPushButton#reset {{
                background-color: {self.accent_orange};
                border: none;
                color: white;
            }}
            QPushButton#reset:hover {{
                background-color: #cc5200;
            }}
            QPushButton#exit {{
                background-color: #0f3460;
                border: none;
                color: white;
            }}
            QPushButton#exit:hover {{
                background-color: #1a4a7d;
            }}
        """
    
    def setup_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # === HEADER ===
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.nasa_blue}, stop:1 #1a4a7d);
                border-radius: 10px;
            }}
        """)
        header_layout = QVBoxLayout(header_frame)
        
        header_label = QLabel("🛸 NASA MISSION CONTROL")
        header_label.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet("color: white; background: transparent; padding: 15px;")
        header_layout.addWidget(header_label)
        
        main_layout.addWidget(header_frame)
        
        # === MODE SELECTION (Radio Buttons) ===
        mode_group = QGroupBox("OPERATION MODE")
        mode_layout = QHBoxLayout(mode_group)
        mode_layout.setContentsMargins(20, 25, 20, 15)
        
        # PySide6 uses QButtonGroup similarly to PyQt6
        self.mode_button_group = QButtonGroup(self)
        modes = [
            ("STANDBY", "standby"),
            ("LAUNCH", "launch"),
            ("ORBIT", "orbit"),
            ("RE-ENTRY", "reentry")
        ]
        
        for text, value in modes:
            rb = QRadioButton(text)
            rb.setProperty("mode_value", value)
            self.mode_button_group.addButton(rb)
            mode_layout.addWidget(rb)
            if value == "standby":
                rb.setChecked(True)
        
        # PySide6 signal connection (same as PyQt6 in Qt6)
        self.mode_button_group.buttonClicked.connect(self.mode_changed)
        main_layout.addWidget(mode_group)
        
        # === DIGITAL READOUTS ===
        readout_group = QGroupBox("TELEMETRY DATA")
        readout_layout = QGridLayout(readout_group)
        readout_layout.setContentsMargins(20, 25, 20, 15)
        readout_layout.setSpacing(20)
        
        self.displays = {}
        readouts = [
            ("ALTITUDE (m)", "altitude"),
            ("VELOCITY (m/s)", "velocity"),
            ("FUEL (%)", "fuel"),
            ("TEMP (°C)", "temperature")
        ]
        
        for i, (label_text, key) in enumerate(readouts):
            row = i // 2
            col = i % 2
            
            container = QFrame()
            container.setStyleSheet("""
                QFrame {
                    background-color: #0d1b2a;
                    border-radius: 8px;
                    border: 1px solid #0f3460;
                    padding: 10px;
                }
            """)
            container_layout = QVBoxLayout(container)
            
            label = QLabel(label_text)
            label.setStyleSheet("color: #7f8c8d; font-size: 11px; background: transparent; border: none;")
            container_layout.addWidget(label)
            
            initial = "000000" if key not in ["fuel", "temperature"] else "100.0" if key == "fuel" else "072.5"
            display = DigitalDisplay(initial)
            self.displays[key] = display
            container_layout.addWidget(display)
            
            readout_layout.addWidget(container, row, col)
        
        main_layout.addWidget(readout_group)
        
        # === STATUS BAR ===
        status_frame = QFrame()
        status_frame.setStyleSheet(f"""
            QFrame {{
                background-color: #1a1a00;
                border: 1px solid {self.accent_orange};
                border-radius: 5px;
            }}
        """)
        status_layout = QVBoxLayout(status_frame)
        
        self.status_label = QLabel("STATUS: SYSTEMS NOMINAL")
        self.status_label.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        self.status_label.setStyleSheet(f"color: {self.digital_color}; background: transparent; border: none;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_layout.addWidget(self.status_label)
        
        main_layout.addWidget(status_frame)
        
        # === CONTROL BUTTONS ===
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        abort_btn = QPushButton("ABORT MISSION")
        abort_btn.setObjectName("abort")
        abort_btn.clicked.connect(self.abort_mission)
        btn_layout.addWidget(abort_btn)
        
        reset_btn = QPushButton("RESET SYSTEMS")
        reset_btn.setObjectName("reset")
        reset_btn.clicked.connect(self.reset_systems)
        btn_layout.addWidget(reset_btn)
        
        btn_layout.addStretch()
        
        exit_btn = QPushButton("EXIT")
        exit_btn.setObjectName("exit")
        exit_btn.clicked.connect(self.close)
        btn_layout.addWidget(exit_btn)
        
        main_layout.addLayout(btn_layout)
    
    def setup_timer(self):
        """Setup timer for telemetry updates"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_telemetry)
        self.timer.start(500)
    
    def mode_changed(self, button):
        self.current_mode = button.property("mode_value")
        status_messages = {
            "standby": "STATUS: SYSTEMS ON STANDBY",
            "launch": "STATUS: LAUNCH SEQUENCE INITIATED ⚠️",
            "orbit": "STATUS: STABLE ORBIT ACHIEVED",
            "reentry": "STATUS: RE-ENTRY PROCEDURES ACTIVE ⚠️"
        }
        self.status_label.setText(status_messages.get(self.current_mode, "STATUS: UNKNOWN"))
    
    def update_telemetry(self):
        """Simulate telemetry data updates"""
        mode = self.current_mode
        
        if mode == "launch":
            self.telemetry["altitude"] += random.randint(100, 500)
            self.telemetry["velocity"] += random.randint(10, 50)
            self.telemetry["fuel"] -= random.uniform(0.1, 0.3)
        elif mode == "orbit":
            self.telemetry["altitude"] = 408000 + random.randint(-100, 100)
            self.telemetry["velocity"] = 7660 + random.randint(-10, 10)
            self.telemetry["fuel"] -= random.uniform(0.01, 0.05)
        elif mode == "reentry":
            self.telemetry["altitude"] = max(0, self.telemetry["altitude"] - random.randint(500, 2000))
            self.telemetry["velocity"] = max(0, self.telemetry["velocity"] - random.randint(50, 200))
        else:
            self.telemetry["altitude"] = 0
            self.telemetry["velocity"] = 0
        
        self.telemetry["temperature"] = 72.5 + random.uniform(-5, 15) if mode != "standby" else 72.5
        self.telemetry["fuel"] = max(0, self.telemetry["fuel"])
        
        # Update displays
        self.displays["altitude"].setText(f"{min(int(self.telemetry['altitude']), 999999):06d}")
        self.displays["velocity"].setText(f"{min(int(self.telemetry['velocity']), 999999):06d}")
        self.displays["fuel"].setText(f"{self.telemetry['fuel']:.1f}")
        self.displays["temperature"].setText(f"{self.telemetry['temperature']:.1f}")
    
    def abort_mission(self):
        self.current_mode = "standby"
        for button in self.mode_button_group.buttons():
            if button.property("mode_value") == "standby":
                button.setChecked(True)
                break
        self.status_label.setText("STATUS: ⚠️ MISSION ABORTED ⚠️")
    
    def reset_systems(self):
        self.current_mode = "standby"
        for button in self.mode_button_group.buttons():
            if button.property("mode_value") == "standby":
                button.setChecked(True)
                break
        self.telemetry = {
            "altitude": 0,
            "velocity": 0,
            "fuel": 100.0,
            "temperature": 72.5
        }
        self.status_label.setText("STATUS: SYSTEMS RESET - NOMINAL")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NASAControlPanel()
    window.show()
    sys.exit(app.exec())

