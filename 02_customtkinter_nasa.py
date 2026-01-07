"""
NASA GUI Example - CustomTkinter
================================
CustomTkinter is a modern UI library based on tkinter with custom widgets 
that provide a sleek, modern appearance out of the box.

To run: python 02_customtkinter_nasa.py
Install: pip install customtkinter
"""

import customtkinter as ctk
import random

class NASAControlPanel(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure appearance
        ctk.set_appearance_mode("dark")  # "light", "dark", or "system"
        ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
        
        # Window setup
        self.title("NASA Control Panel - CustomTkinter")
        self.geometry("650x550")
        self.minsize(600, 500)
        
        # Configure custom colors for NASA theme
        self.nasa_blue = "#0B3D91"
        self.nasa_red = "#FC3D21"
        self.digital_green = "#00FF41"
        
        # Variables
        self.mode_var = ctk.StringVar(value="standby")
        self.telemetry_values = {
            "altitude": ctk.StringVar(value="000000"),
            "velocity": ctk.StringVar(value="000000"),
            "fuel": ctk.StringVar(value="100.0"),
            "temperature": ctk.StringVar(value="072.5")
        }
        self.status_var = ctk.StringVar(value="STATUS: SYSTEMS NOMINAL")
        
        self.create_widgets()
        self.update_telemetry()
    
    def create_widgets(self):
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # === HEADER ===
        header_frame = ctk.CTkFrame(main_frame, fg_color=self.nasa_blue, corner_radius=10)
        header_frame.pack(fill="x", pady=(0, 15))
        
        header = ctk.CTkLabel(
            header_frame,
            text="🚀 NASA MISSION CONTROL",
            font=ctk.CTkFont(family="Helvetica", size=28, weight="bold"),
            text_color="white"
        )
        header.pack(pady=15)
        
        # === MODE SELECTION (Radio Buttons) ===
        mode_frame = ctk.CTkFrame(main_frame)
        mode_frame.pack(fill="x", pady=10)
        
        mode_label = ctk.CTkLabel(
            mode_frame,
            text="OPERATION MODE",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        mode_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Radio button container
        radio_frame = ctk.CTkFrame(mode_frame, fg_color="transparent")
        radio_frame.pack(fill="x", padx=10, pady=10)
        
        modes = [
            ("STANDBY", "standby"),
            ("LAUNCH", "launch"),
            ("ORBIT", "orbit"),
            ("RE-ENTRY", "reentry")
        ]
        
        # CustomTkinter radio buttons
        for i, (text, value) in enumerate(modes):
            rb = ctk.CTkRadioButton(
                radio_frame,
                text=text,
                variable=self.mode_var,
                value=value,
                command=self.mode_changed,
                font=ctk.CTkFont(size=13),
                fg_color=self.nasa_red,
                hover_color="#FF6B6B",
                border_color="#666666"
            )
            rb.grid(row=0, column=i, padx=15, pady=5)
            radio_frame.columnconfigure(i, weight=1)
        
        # === DIGITAL READOUTS ===
        readout_frame = ctk.CTkFrame(main_frame)
        readout_frame.pack(fill="both", expand=True, pady=10)
        
        readout_label = ctk.CTkLabel(
            readout_frame,
            text="TELEMETRY DATA",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        readout_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Grid for readouts
        readout_grid = ctk.CTkFrame(readout_frame, fg_color="transparent")
        readout_grid.pack(fill="both", expand=True, padx=10, pady=10)
        
        readouts = [
            ("ALTITUDE (m)", "altitude"),
            ("VELOCITY (m/s)", "velocity"),
            ("FUEL (%)", "fuel"),
            ("TEMP (°C)", "temperature")
        ]
        
        for i, (label, key) in enumerate(readouts):
            row = i // 2
            col = i % 2
            
            # Container for each readout
            container = ctk.CTkFrame(readout_grid, fg_color="#1a1a1a", corner_radius=8)
            container.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            readout_grid.columnconfigure(col, weight=1)
            readout_grid.rowconfigure(row, weight=1)
            
            # Label
            lbl = ctk.CTkLabel(
                container,
                text=label,
                font=ctk.CTkFont(size=11),
                text_color="#888888"
            )
            lbl.pack(anchor="w", padx=15, pady=(10, 0))
            
            # Digital display using CTkEntry for LED-like appearance
            display_frame = ctk.CTkFrame(container, fg_color="#000000", corner_radius=5)
            display_frame.pack(fill="x", padx=15, pady=(5, 15))
            
            display = ctk.CTkLabel(
                display_frame,
                textvariable=self.telemetry_values[key],
                font=ctk.CTkFont(family="Courier", size=32, weight="bold"),
                text_color=self.digital_green,
                anchor="e"
            )
            display.pack(fill="x", padx=10, pady=8)
        
        # === STATUS BAR ===
        status_frame = ctk.CTkFrame(main_frame, fg_color="#003300", corner_radius=5)
        status_frame.pack(fill="x", pady=10)
        
        status_label = ctk.CTkLabel(
            status_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(family="Courier", size=14, weight="bold"),
            text_color=self.digital_green
        )
        status_label.pack(pady=10)
        
        # === CONTROL BUTTONS ===
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        ctk.CTkButton(
            btn_frame,
            text="ABORT MISSION",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=self.nasa_red,
            hover_color="#CC2E1A",
            command=self.abort_mission,
            width=140
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="RESET SYSTEMS",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#CC7000",
            hover_color="#995300",
            command=self.reset_systems,
            width=140
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="EXIT",
            font=ctk.CTkFont(size=13),
            fg_color="#444444",
            hover_color="#333333",
            command=self.quit,
            width=100
        ).pack(side="right", padx=5)
    
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
            alt = int(self.telemetry_values["altitude"].get()) + random.randint(100, 500)
            vel = int(self.telemetry_values["velocity"].get()) + random.randint(10, 50)
            fuel = float(self.telemetry_values["fuel"].get()) - random.uniform(0.1, 0.3)
        elif mode == "orbit":
            alt = 408000 + random.randint(-100, 100)
            vel = 7660 + random.randint(-10, 10)
            fuel = float(self.telemetry_values["fuel"].get()) - random.uniform(0.01, 0.05)
        elif mode == "reentry":
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
        
        self.after(500, self.update_telemetry)
    
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


if __name__ == "__main__":
    app = NASAControlPanel()
    app.mainloop()

