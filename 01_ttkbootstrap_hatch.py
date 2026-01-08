"""
Hatch Control GUI - ttkbootstrap
================================
A sleek aerospace-style hatch control panel with animated status indicator.

Features:
- Open/Closed radio buttons
- Animated hatch circle with glow effects
- Click counter with LED-style display

To run: python 01_ttkbootstrap_hatch.py
Install: pip install ttkbootstrap
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import math


class GlowingHatch(ttk.Canvas):
    """Custom canvas widget that draws a glowing hatch circle."""
    
    def __init__(self, parent, size=280, **kwargs):
        super().__init__(parent, width=size, height=size, 
                        highlightthickness=0, bg='#0a0a0f', **kwargs)
        self.size = size
        self._is_open = False
        self._glow_phase = 0
        self._animating = False
        self.draw_hatch()
    
    def set_open(self, is_open: bool):
        """Set hatch state and trigger animation."""
        self._is_open = is_open
        if is_open and not self._animating:
            self._animating = True
            self._animate_glow()
        elif not is_open:
            self._animating = False
            self.draw_hatch()
    
    def _animate_glow(self):
        """Animate the glow effect when open."""
        if not self._animating:
            return
        self._glow_phase = (self._glow_phase + 0.15) % (2 * math.pi)
        self.draw_hatch()
        self.after(50, self._animate_glow)
    
    def draw_hatch(self):
        """Draw the hatch circle with glow effect."""
        self.delete("all")
        cx, cy = self.size // 2, self.size // 2
        radius = self.size // 2 - 40
        
        if self._is_open:
            # Pulsing glow intensity
            pulse = 0.7 + 0.3 * math.sin(self._glow_phase)
            
            # Draw multiple glow layers (outer to inner)
            glow_colors = [
                (radius + 35, f'#001a00'),
                (radius + 28, f'#003300'),
                (radius + 20, f'#004d00'),
                (radius + 12, f'#006600'),
                (radius + 6, f'#008000'),
            ]
            for glow_radius, color in glow_colors:
                self.create_oval(
                    cx - glow_radius, cy - glow_radius,
                    cx + glow_radius, cy + glow_radius,
                    fill=color, outline=''
                )
            
            # Main circle - vibrant green
            green_val = int(180 + 75 * pulse)
            main_color = f'#00{green_val:02x}00'
            self.create_oval(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                fill=main_color, outline='#00ff00', width=3
            )
            
            # Inner highlight
            highlight_radius = radius - 20
            self.create_oval(
                cx - highlight_radius, cy - highlight_radius + 5,
                cx + highlight_radius - 40, cy - 20,
                fill='#44ff44', outline=''
            )
            
            # Status text
            self.create_text(cx, cy, text="OPEN", 
                           font=("Orbitron", 24, "bold") if self._font_exists("Orbitron") 
                           else ("Arial Black", 22, "bold"),
                           fill='#001100')
        else:
            # Closed state - dark with subtle ring
            # Outer ring glow
            self.create_oval(
                cx - radius - 8, cy - radius - 8,
                cx + radius + 8, cy + radius + 8,
                fill='#1a1a1a', outline='#333333', width=2
            )
            
            # Main circle - dark
            self.create_oval(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                fill='#0d0d0d', outline='#444444', width=3
            )
            
            # Subtle inner shadow
            self.create_oval(
                cx - radius + 15, cy - radius + 15,
                cx + radius - 15, cy + radius - 15,
                fill='#080808', outline=''
            )
            
            # Status text
            self.create_text(cx, cy, text="CLOSED", 
                           font=("Orbitron", 20, "bold") if self._font_exists("Orbitron")
                           else ("Arial Black", 18, "bold"),
                           fill='#444444')
        
        # Draw hatch lines (decorative)
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x1 = cx + (radius - 30) * math.cos(rad)
            y1 = cy + (radius - 30) * math.sin(rad)
            x2 = cx + (radius - 10) * math.cos(rad)
            y2 = cy + (radius - 10) * math.sin(rad)
            line_color = '#00aa00' if self._is_open else '#333333'
            self.create_line(x1, y1, x2, y2, fill=line_color, width=2)
    
    def _font_exists(self, font_name):
        try:
            import tkinter.font as tkfont
            return font_name in tkfont.families()
        except:
            return False


class HatchControlApp:
    def __init__(self):
        # Create main window with dark theme
        self.root = ttk.Window(
            title="HATCH CONTROL SYSTEM",
            themename="cyborg",
            size=(500, 650),
            resizable=(False, False)
        )
        self.root.configure(bg='#0a0a0f')
        
        # State
        self.state_var = ttk.StringVar(value="closed")
        self.open_count = 0
        
        self.create_ui()
    
    def create_ui(self):
        # Main container
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill=BOTH, expand=YES)
        main.configure(style='dark.TFrame')
        
        # === HEADER ===
        header_frame = ttk.Frame(main)
        header_frame.pack(fill=X, pady=(0, 20))
        
        title = ttk.Label(
            header_frame,
            text="⬡ HATCH CONTROL SYSTEM",
            font=("Consolas", 22, "bold"),
            foreground="#00ccff",
            background="#0a0a0f"
        )
        title.pack()
        
        subtitle = ttk.Label(
            header_frame,
            text="AIRLOCK MODULE A-7",
            font=("Consolas", 11),
            foreground="#666677",
            background="#0a0a0f"
        )
        subtitle.pack()
        
        # === COUNTER DISPLAY ===
        counter_frame = ttk.Frame(main)
        counter_frame.pack(fill=X, pady=15)
        
        ttk.Label(
            counter_frame,
            text="CYCLE COUNT",
            font=("Arial", 10, "bold"),
            foreground="#888899",
            background="#0a0a0f"
        ).pack()
        
        # LED-style counter display
        self.counter_display = ttk.Label(
            counter_frame,
            text="0",
            font=("DS-Digital", 56) if self._font_exists("DS-Digital") else ("Courier", 52, "bold"),
            foreground="#00ff88",
            background="#050505",
            width=8,
            anchor="center"
        )
        self.counter_display.pack(pady=5)
        
        # === HATCH INDICATOR ===
        hatch_frame = ttk.Frame(main)
        hatch_frame.pack(fill=BOTH, expand=YES, pady=15)
        
        ttk.Label(
            hatch_frame,
            text="HATCH STATUS",
            font=("Arial", 10, "bold"),
            foreground="#888899",
            background="#0a0a0f"
        ).pack()
        
        self.hatch = GlowingHatch(hatch_frame, size=280)
        self.hatch.pack(pady=10)
        
        # === CONTROL PANEL ===
        control_frame = ttk.Labelframe(
            main,
            text="CONTROL",
            padding=20,
            bootstyle="info"
        )
        control_frame.pack(fill=X, pady=15)
        
        # Radio buttons container
        radio_container = ttk.Frame(control_frame)
        radio_container.pack()
        
        # OPEN button
        self.open_radio = ttk.Radiobutton(
            radio_container,
            text="  OPEN  ",
            variable=self.state_var,
            value="open",
            bootstyle="success-toolbutton-outline",
            command=self.on_state_change,
            width=12
        )
        self.open_radio.pack(side=LEFT, padx=20)
        
        # CLOSED button
        self.closed_radio = ttk.Radiobutton(
            radio_container,
            text=" CLOSED ",
            variable=self.state_var,
            value="closed",
            bootstyle="danger-toolbutton-outline",
            command=self.on_state_change,
            width=12
        )
        self.closed_radio.pack(side=LEFT, padx=20)
        
        # === STATUS BAR ===
        self.status_var = ttk.StringVar(value="◉ SYSTEM READY")
        status = ttk.Label(
            main,
            textvariable=self.status_var,
            font=("Consolas", 11),
            foreground="#00ff88",
            background="#0a0a0f"
        )
        status.pack(pady=(15, 0))
    
    def _font_exists(self, font_name):
        try:
            import tkinter.font as tkfont
            return font_name in tkfont.families()
        except:
            return False
    
    def on_state_change(self):
        """Handle radio button state change."""
        state = self.state_var.get()
        
        if state == "open":
            self.open_count += 1
            self.counter_display.configure(text=str(self.open_count))
            self.hatch.set_open(True)
            self.status_var.set("◉ HATCH OPENING...")
            self.root.after(500, lambda: self.status_var.set("◉ HATCH OPEN - PRESSURIZED"))
        else:
            self.hatch.set_open(False)
            self.status_var.set("◉ HATCH SECURED")
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = HatchControlApp()
    app.run()

