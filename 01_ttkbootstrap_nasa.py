"""
NASA GUI Example - ttkbootstrap
===============================
ttkbootstrap is a themed extension for tkinter that provides modern Bootstrap-style widgets.
It's built on top of standard tkinter/ttk, making it familiar to tkinter users.

To run: python 01_ttkbootstrap_nasa.py
Install: pip install ttkbootstrap
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import random

class NASAControlPanel:
    def __init__(self):
        # Create the main window with a dark theme
        # Available themes: cosmo, flatly, litera, minty, lumen, sandstone, 
        #                   yeti, pulse, united, morph, journal, darkly, 
        #                   superhero, solar, cyborg, vapor, simplex, cerculean
        self.root = ttk.Window(
            title="NASA Control Panel - ttkbootstrap",
            themename="cyborg",  # Dark futuristic theme
            size=(600, 500)
        )
        self.root.resizable(True, True)
        
        # Variables for radio buttons and readouts
        self.mode_var = ttk.StringVar(value="standby")
        self.telemetry_values = {
            "altitude": ttk.StringVar(value="000000"),
            "velocity": ttk.StringVar(value="000000"),
            "fuel": ttk.StringVar(value="100.0"),
            "temperature": ttk.StringVar(value="072.5")
        }
        
        self.create_widgets()
        self.update_telemetry()
        
    def create_widgets(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)
        
        # === HEADER ===
        header = ttk.Label(
            main_frame,
            text="🚀 NASA MISSION CONTROL",
            font=("Consolas", 24, "bold"),
            bootstyle="danger"  # Red accent color
        )
        header.pack(pady=(0, 20))
        
        # === MODE SELECTION (Radio Buttons) ===
        mode_frame = ttk.Labelframe(
            main_frame,
            text="OPERATION MODE",
            padding=15,
            bootstyle="info"
        )
        mode_frame.pack(fill=X, pady=10)
        
        modes = [
            ("STANDBY", "standby"),
            ("LAUNCH SEQUENCE", "launch"),
            ("ORBIT", "orbit"),
            ("RE-ENTRY", "reentry")
        ]
        
        # Create radio buttons in a row
        for text, value in modes:
            rb = ttk.Radiobutton(
                mode_frame,
                text=text,
                variable=self.mode_var,
                value=value,
                bootstyle="success-toolbutton",  # Green toggle-style buttons
                command=self.mode_changed
            )
            rb.pack(side=LEFT, padx=10, expand=YES)
        
        # === DIGITAL READOUTS ===
        readout_frame = ttk.Labelframe(
            main_frame,
            text="TELEMETRY DATA",
            padding=15,
            bootstyle="warning"
        )
        readout_frame.pack(fill=BOTH, expand=YES, pady=10)
        
        # Create digital display style readouts
        readouts = [
            ("ALTITUDE (m)", "altitude"),
            ("VELOCITY (m/s)", "velocity"),
            ("FUEL (%)", "fuel"),
            ("TEMP (°C)", "temperature")
        ]
        
        for i, (label, key) in enumerate(readouts):
            row = i // 2
            col = i % 2
            
            container = ttk.Frame(readout_frame)
            container.grid(row=row, column=col, padx=20, pady=15, sticky="ew")
            readout_frame.columnconfigure(col, weight=1)
            
            # Label
            lbl = ttk.Label(
                container,
                text=label,
                font=("Arial", 10),
                bootstyle="secondary"
            )
            lbl.pack(anchor="w")
            
            # Digital display - using Entry with readonly state for LED-like look
            display = ttk.Entry(
                container,
                textvariable=self.telemetry_values[key],
                font=("DS-Digital", 32) if self._font_exists("DS-Digital") else ("Consolas", 28),
                justify="right",
                bootstyle="success",
                state="readonly"
            )
            display.pack(fill=X)
        
        # === STATUS BAR ===
        self.status_var = ttk.StringVar(value="STATUS: SYSTEMS NOMINAL")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            font=("Consolas", 12),
            bootstyle="inverse-success"
        )
        status_bar.pack(fill=X, pady=(10, 0))
        
        # === CONTROL BUTTONS ===
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=X, pady=10)
        
        ttk.Button(
            btn_frame,
            text="ABORT MISSION",
            bootstyle="danger-outline",
            command=self.abort_mission
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="RESET SYSTEMS",
            bootstyle="warning-outline",
            command=self.reset_systems
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="EXIT",
            bootstyle="secondary",
            command=self.root.quit
        ).pack(side=RIGHT, padx=5)
    
    def _font_exists(self, font_name):
        """Check if a font exists on the system"""
        try:
            import tkinter.font as tkfont
            return font_name in tkfont.families()
        except:
            return False
    
    def mode_changed(self):
        mode = self.mode_var.get()
        status_messages = {
            "standby": "STATUS: SYSTEMS ON STANDBY",
            "launch": "STATUS: LAUNCH SEQUENCE INITIATED ⚠️",
            "orbit": "STATUS: STABLE ORBIT ACHIEVED",
            "reentry": "STATUS: RE-ENTRY PROCEDURES ACTIVE ⚠️"
        }
        self.status_var.set(status_messages.get(mode, "STATUS: UNKNOWN"))
    
    def update_telemetry(self):
        """Simulate telemetry data updates"""
        mode = self.mode_var.get()
        
        if mode == "launch":
            # Increasing altitude and velocity during launch
            alt = int(self.telemetry_values["altitude"].get()) + random.randint(100, 500)
            vel = int(self.telemetry_values["velocity"].get()) + random.randint(10, 50)
            fuel = float(self.telemetry_values["fuel"].get()) - random.uniform(0.1, 0.3)
        elif mode == "orbit":
            # Stable orbit with minor fluctuations
            alt = 408000 + random.randint(-100, 100)
            vel = 7660 + random.randint(-10, 10)
            fuel = float(self.telemetry_values["fuel"].get()) - random.uniform(0.01, 0.05)
        elif mode == "reentry":
            # Decreasing altitude during reentry
            alt = max(0, int(self.telemetry_values["altitude"].get()) - random.randint(500, 2000))
            vel = max(0, int(self.telemetry_values["velocity"].get()) - random.randint(50, 200))
            fuel = float(self.telemetry_values["fuel"].get())
        else:
            alt = 0
            vel = 0
            fuel = float(self.telemetry_values["fuel"].get())
        
        temp = 72.5 + random.uniform(-5, 15) if mode != "standby" else 72.5
        
        self.telemetry_values["altitude"].set(f"{min(alt, 999999):06d}")
        self.telemetry_values["velocity"].set(f"{min(vel, 999999):06d}")
        self.telemetry_values["fuel"].set(f"{max(fuel, 0):.1f}")
        self.telemetry_values["temperature"].set(f"{temp:.1f}")
        
        # Schedule next update
        self.root.after(500, self.update_telemetry)
    
    def abort_mission(self):
        self.mode_var.set("standby")
        self.status_var.set("STATUS: ⚠️ MISSION ABORTED ⚠️")
    
    def reset_systems(self):
        self.mode_var.set("standby")
        self.telemetry_values["altitude"].set("000000")
        self.telemetry_values["velocity"].set("000000")
        self.telemetry_values["fuel"].set("100.0")
        self.telemetry_values["temperature"].set("072.5")
        self.status_var.set("STATUS: SYSTEMS RESET - NOMINAL")
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = NASAControlPanel()
    app.run()

