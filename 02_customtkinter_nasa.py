"""
Hatch Control - CustomTkinter
=============================
Radio buttons: Open/Closed
Circle (Hatch): Green when Open, Black when Closed
Counter: Increments each time Open is clicked

To run: python 02_customtkinter_nasa.py
Install: pip install customtkinter
"""

import customtkinter as ctk


class HatchControl(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Window setup
        self.title("Hatch Control - CustomTkinter")
        self.geometry("600x420")
        
        # State
        self.open_click_count = 0
        self.state_var = ctk.StringVar(value="closed")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title label
        title_label = ctk.CTkLabel(
            main_frame,
            text="Number",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(0, 5))
        
        # Counter display
        self.counter_label = ctk.CTkLabel(
            main_frame,
            text="0",
            font=ctk.CTkFont(size=26),
            text_color="#3B8ED0"
        )
        self.counter_label.pack(pady=(0, 20))
        
        # Canvas for the Hatch circle
        self.canvas = ctk.CTkCanvas(
            main_frame,
            width=240,
            height=240,
            bg="#2b2b2b",
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
        
        # Radio button frame
        radio_frame = ctk.CTkFrame(main_frame)
        radio_frame.pack(fill="x", pady=20, padx=50)
        
        radio_label = ctk.CTkLabel(
            radio_frame,
            text="State",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        radio_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Radio buttons container
        radio_container = ctk.CTkFrame(radio_frame, fg_color="transparent")
        radio_container.pack(fill="x", padx=10, pady=10)
        
        # Open radio button
        self.radio_open = ctk.CTkRadioButton(
            radio_container,
            text="Open",
            variable=self.state_var,
            value="open",
            command=self.on_open_clicked,
            fg_color="green",
            hover_color="#228B22"
        )
        self.radio_open.pack(side="left", padx=20)
        
        # Closed radio button
        self.radio_closed = ctk.CTkRadioButton(
            radio_container,
            text="Closed",
            variable=self.state_var,
            value="closed",
            command=self.on_closed_clicked,
            fg_color="#CC0000",
            hover_color="#8B0000"
        )
        self.radio_closed.pack(side="left", padx=20)
    
    def on_open_clicked(self):
        """Open clicked: turn hatch green and increment counter."""
        self.canvas.itemconfig(self.hatch_circle, fill="green")
        self.open_click_count += 1
        self.counter_label.configure(text=str(self.open_click_count))
    
    def on_closed_clicked(self):
        """Closed clicked: turn hatch black (counter unchanged)."""
        self.canvas.itemconfig(self.hatch_circle, fill="black")


if __name__ == "__main__":
    app = HatchControl()
    app.mainloop()
