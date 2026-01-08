"""
Hatch Control - ttkbootstrap
============================
Radio buttons: Open/Closed
Circle (Hatch): Green when Open, Black when Closed
Counter: Increments each time Open is clicked

To run: python 01_ttkbootstrap_nasa.py
Install: pip install ttkbootstrap
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class HatchControl:
    def __init__(self):
        # Create main window with dark theme
        self.root = ttk.Window(
            title="Hatch Control - ttkbootstrap",
            themename="darkly",
            size=(600, 420)
        )
        
        # State
        self.open_click_count = 0
        self.state_var = ttk.StringVar(value="closed")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)
        
        # Title label
        title_label = ttk.Label(
            main_frame,
            text="Number",
            font=("Helvetica", 18, "bold"),
            bootstyle="light"
        )
        title_label.pack(pady=(0, 5))
        
        # Counter display
        self.counter_label = ttk.Label(
            main_frame,
            text="0",
            font=("Helvetica", 26),
            bootstyle="info"
        )
        self.counter_label.pack(pady=(0, 20))
        
        # Canvas for the Hatch circle
        self.canvas = ttk.Canvas(
            main_frame,
            width=240,
            height=240,
            highlightthickness=0
        )
        self.canvas.pack(pady=20)
        
        # Draw initial circle (black = closed)
        self.hatch_circle = self.canvas.create_oval(
            10, 10, 230, 230,
            fill="black",
            outline="gray",
            width=2
        )
        
        # Radio button group
        radio_frame = ttk.Labelframe(main_frame, text="State", padding=15)
        radio_frame.pack(fill=X, pady=20)
        
        # Open radio button
        self.radio_open = ttk.Radiobutton(
            radio_frame,
            text="Open",
            variable=self.state_var,
            value="open",
            command=self.on_open_clicked,
            bootstyle="success"
        )
        self.radio_open.pack(side=LEFT, padx=20)
        
        # Closed radio button
        self.radio_closed = ttk.Radiobutton(
            radio_frame,
            text="Closed",
            variable=self.state_var,
            value="closed",
            command=self.on_closed_clicked,
            bootstyle="danger"
        )
        self.radio_closed.pack(side=LEFT, padx=20)
    
    def on_open_clicked(self):
        """Open clicked: turn hatch green and increment counter."""
        self.canvas.itemconfig(self.hatch_circle, fill="green")
        self.open_click_count += 1
        self.counter_label.config(text=str(self.open_click_count))
    
    def on_closed_clicked(self):
        """Closed clicked: turn hatch black (counter unchanged)."""
        self.canvas.itemconfig(self.hatch_circle, fill="black")
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = HatchControl()
    app.run()
