"""
NASA GUI Example - Qt Designer with PySide6 Loader
==================================================
This script demonstrates how to load a .ui file created with Qt Designer.
The .ui file (05_qt_designer_nasa.ui) contains the visual layout, while
this Python file adds the business logic.

To run: python 05_qt_designer_loader.py
Install: pip install PySide6

Qt Designer can be launched with:
  - pyside6-designer (comes with PySide6)
  - Or from Qt Creator IDE

WORKFLOW:
1. Design UI visually in Qt Designer → save as .ui file
2. Load .ui file in Python using QUiLoader (PySide6) or uic.loadUi (PyQt6)
3. Connect signals and add business logic in Python

ADVANTAGES OF Qt Designer:
- Visual WYSIWYG design
- Drag-and-drop widget placement
- Easy property editing
- Preview without running code
- Separates design from logic
"""

import sys
import random
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QTimer, QIODevice


class NASAControlPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Load the UI file
        self.load_ui()
        
        # State variables
        self.current_mode = "standby"
        self.telemetry = {
            "altitude": 0,
            "velocity": 0,
            "fuel": 100.0,
            "temperature": 72.5
        }
        
        # Connect signals to slots
        self.connect_signals()
        
        # Setup telemetry update timer
        self.setup_timer()
    
    def load_ui(self):
        """Load the .ui file created in Qt Designer"""
        # Get the path to the .ui file (same directory as this script)
        ui_path = Path(__file__).parent / "05_qt_designer_nasa.ui"
        
        # Method 1: Using QUiLoader (PySide6)
        # This loads the UI into a separate widget
        loader = QUiLoader()
        ui_file = QFile(str(ui_path))
        
        if not ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
            raise RuntimeError(f"Cannot open UI file: {ui_path}")
        
        self.ui = loader.load(ui_file)
        ui_file.close()
        
        if self.ui is None:
            raise RuntimeError(f"Failed to load UI from: {ui_path}")
        
        # Show the loaded UI
        self.ui.show()
    
    def connect_signals(self):
        """Connect UI signals to Python slots"""
        # Radio buttons
        self.ui.radioStandby.toggled.connect(lambda checked: self.mode_changed("standby") if checked else None)
        self.ui.radioLaunch.toggled.connect(lambda checked: self.mode_changed("launch") if checked else None)
        self.ui.radioOrbit.toggled.connect(lambda checked: self.mode_changed("orbit") if checked else None)
        self.ui.radioReentry.toggled.connect(lambda checked: self.mode_changed("reentry") if checked else None)
        
        # Buttons
        self.ui.abortButton.clicked.connect(self.abort_mission)
        self.ui.resetButton.clicked.connect(self.reset_systems)
        # Exit button is already connected in the .ui file via Qt Designer
    
    def setup_timer(self):
        """Setup timer for telemetry updates"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_telemetry)
        self.timer.start(500)
    
    def mode_changed(self, mode):
        """Handle mode selection change"""
        self.current_mode = mode
        status_messages = {
            "standby": "STATUS: SYSTEMS ON STANDBY",
            "launch": "STATUS: LAUNCH SEQUENCE INITIATED ⚠️",
            "orbit": "STATUS: STABLE ORBIT ACHIEVED",
            "reentry": "STATUS: RE-ENTRY PROCEDURES ACTIVE ⚠️"
        }
        self.ui.statusLabel.setText(status_messages.get(mode, "STATUS: UNKNOWN"))
    
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
        
        # Update displays (accessing widgets by their objectName from .ui file)
        self.ui.altitudeDisplay.setText(f"{min(int(self.telemetry['altitude']), 999999):06d}")
        self.ui.velocityDisplay.setText(f"{min(int(self.telemetry['velocity']), 999999):06d}")
        self.ui.fuelDisplay.setText(f"{self.telemetry['fuel']:.1f}")
        self.ui.tempDisplay.setText(f"{self.telemetry['temperature']:.1f}")
    
    def abort_mission(self):
        """Handle abort mission button"""
        self.current_mode = "standby"
        self.ui.radioStandby.setChecked(True)
        self.ui.statusLabel.setText("STATUS: ⚠️ MISSION ABORTED ⚠️")
    
    def reset_systems(self):
        """Handle reset systems button"""
        self.current_mode = "standby"
        self.ui.radioStandby.setChecked(True)
        self.telemetry = {
            "altitude": 0,
            "velocity": 0,
            "fuel": 100.0,
            "temperature": 72.5
        }
        self.ui.statusLabel.setText("STATUS: SYSTEMS RESET - NOMINAL")


# Alternative: PyQt6 version of loading .ui files
"""
# For PyQt6, you would use:
from PyQt6 import uic

class NASAControlPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load UI directly into self
        uic.loadUi("05_qt_designer_nasa.ui", self)
        
        # Now widgets are accessible as self.widgetName
        # e.g., self.radioStandby, self.altitudeDisplay, etc.
"""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create the controller (which loads the UI)
    controller = NASAControlPanel()
    
    sys.exit(app.exec())

