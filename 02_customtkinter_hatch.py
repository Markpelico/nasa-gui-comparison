"""
Hatch Control GUI - CustomTkinter
=================================
A modern, sleek hatch control interface with smooth animations and glowing effects.

Features:
- Open/Closed radio buttons with modern styling
- Animated hatch circle with pulsing glow
- LED-style cycle counter

To run: python 02_customtkinter_hatch.py
Install: pip install customtkinter
"""

import customtkinter as ctk
import math


class GlowingHatchCanvas(ctk.CTkCanvas):
    """Custom canvas that draws an animated glowing hatch indicator."""
    
    def __init__(self, parent, size=300, **kwargs):
        super().__init__(parent, width=size, height=size, 
                        highlightthickness=0, bg='#0d0d12', **kwargs)
        self.size = size
        self._is_open = False
        self._glow_phase = 0
        self._transition_progress = 0
        self._animating = False
        self.draw_hatch()
    
    def set_open(self, is_open: bool, animate: bool = True):
        """Set hatch state with optional animation."""
        if self._is_open == is_open:
            return
        self._is_open = is_open
        
        if is_open:
            self._animating = True
            self._animate_open()
        else:
            self._animating = False
            self._transition_progress = 0
            self.draw_hatch()
    
    def _animate_open(self):
        """Animate the hatch opening with glow pulse."""
        if not self._animating:
            return
        self._glow_phase = (self._glow_phase + 0.12) % (2 * math.pi)
        self._transition_progress = min(1.0, self._transition_progress + 0.08)
        self.draw_hatch()
        self.after(40, self._animate_open)
    
    def draw_hatch(self):
        """Render the hatch circle with current state."""
        self.delete("all")
        cx, cy = self.size // 2, self.size // 2
        radius = self.size // 2 - 45
        
        if self._is_open:
            pulse = 0.6 + 0.4 * math.sin(self._glow_phase)
            progress = self._transition_progress
            
            # Outer glow rings
            for i, alpha in enumerate([0.1, 0.2, 0.3, 0.4, 0.5]):
                glow_r = radius + 35 - i * 7
                green_intensity = int(60 * alpha * pulse)
                color = f'#{0:02x}{green_intensity:02x}{0:02x}'
                self.create_oval(cx - glow_r, cy - glow_r, cx + glow_r, cy + glow_r,
                               fill=color, outline='')
            
            # Main hatch circle
            green_val = int(160 + 95 * pulse * progress)
            self.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                           fill=f'#00{green_val:02x}00', outline='#00ff66', width=4)
            
            # Inner glossy highlight
            highlight_r = radius * 0.65
            self.create_arc(cx - highlight_r, cy - highlight_r - 10,
                          cx + highlight_r, cy + highlight_r - 30,
                          start=30, extent=120, fill='#33ff66', outline='')
            
            # Center status
            self.create_text(cx, cy + 10, text="OPEN",
                           font=("SF Pro Display", 28, "bold") if self._font_exists("SF Pro Display")
                           else ("Helvetica", 26, "bold"),
                           fill='#003300')
            
            # Decorative bolts
            self._draw_bolts(cx, cy, radius, '#00cc44')
        else:
            # Closed state - dark industrial look
            # Subtle outer ring
            self.create_oval(cx - radius - 12, cy - radius - 12,
                           cx + radius + 12, cy + radius + 12,
                           fill='#151518', outline='#252530', width=2)
            
            # Main circle
            self.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                           fill='#0a0a0c', outline='#3a3a44', width=4)
            
            # Inner shadow
            inner_r = radius - 20
            self.create_oval(cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r,
                           fill='#060608', outline='')
            
            # Status text
            self.create_text(cx, cy + 10, text="CLOSED",
                           font=("SF Pro Display", 24, "bold") if self._font_exists("SF Pro Display")
                           else ("Helvetica", 22, "bold"),
                           fill='#404050')
            
            # Decorative bolts
            self._draw_bolts(cx, cy, radius, '#303038')
        
        # Draw tick marks around edge
        self._draw_ticks(cx, cy, radius)
    
    def _draw_bolts(self, cx, cy, radius, color):
        """Draw decorative bolt heads around the hatch."""
        bolt_r = 8
        for angle in [45, 135, 225, 315]:
            rad = math.radians(angle)
            bx = cx + (radius - 25) * math.cos(rad)
            by = cy + (radius - 25) * math.sin(rad)
            self.create_oval(bx - bolt_r, by - bolt_r, bx + bolt_r, by + bolt_r,
                           fill=color, outline='#1a1a1a', width=2)
    
    def _draw_ticks(self, cx, cy, radius):
        """Draw tick marks around the hatch edge."""
        tick_color = '#00aa44' if self._is_open else '#2a2a32'
        for angle in range(0, 360, 15):
            rad = math.radians(angle)
            length = 12 if angle % 45 == 0 else 6
            x1 = cx + (radius + 8) * math.cos(rad)
            y1 = cy + (radius + 8) * math.sin(rad)
            x2 = cx + (radius + 8 + length) * math.cos(rad)
            y2 = cy + (radius + 8 + length) * math.sin(rad)
            self.create_line(x1, y1, x2, y2, fill=tick_color, width=2)
    
    def _font_exists(self, font_name):
        try:
            import tkinter.font as tkfont
            return font_name in tkfont.families()
        except:
            return False


class HatchControlApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Window setup
        self.title("HATCH CONTROL SYSTEM")
        self.geometry("520x720")
        self.resizable(False, False)
        self.configure(fg_color="#0d0d12")
        
        # State
        self.state_var = ctk.StringVar(value="closed")
        self.open_count = 0
        
        self.create_ui()
    
    def create_ui(self):
        # === HEADER ===
        header = ctk.CTkFrame(self, fg_color="#0d0d12", corner_radius=0)
        header.pack(fill="x", padx=30, pady=(30, 0))
        
        title = ctk.CTkLabel(
            header,
            text="◈ HATCH CONTROL",
            font=ctk.CTkFont(family="Helvetica", size=32, weight="bold"),
            text_color="#00ddff"
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header,
            text="AIRLOCK MODULE A-7  •  DECK 3",
            font=ctk.CTkFont(family="Helvetica", size=13),
            text_color="#505068"
        )
        subtitle.pack(anchor="w", pady=(2, 0))
        
        # === COUNTER SECTION ===
        counter_section = ctk.CTkFrame(self, fg_color="#0d0d12")
        counter_section.pack(fill="x", padx=30, pady=(30, 0))
        
        ctk.CTkLabel(
            counter_section,
            text="CYCLE COUNT",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#606078"
        ).pack(anchor="w")
        
        # Counter display frame
        counter_bg = ctk.CTkFrame(counter_section, fg_color="#050508", corner_radius=8)
        counter_bg.pack(fill="x", pady=(8, 0))
        
        self.counter_label = ctk.CTkLabel(
            counter_bg,
            text="0",
            font=ctk.CTkFont(family="Courier", size=64, weight="bold"),
            text_color="#00ff99"
        )
        self.counter_label.pack(pady=15)
        
        # === HATCH INDICATOR ===
        hatch_section = ctk.CTkFrame(self, fg_color="#0d0d12")
        hatch_section.pack(fill="both", expand=True, padx=30, pady=20)
        
        ctk.CTkLabel(
            hatch_section,
            text="HATCH STATUS",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#606078"
        ).pack(anchor="w")
        
        # Hatch canvas
        hatch_container = ctk.CTkFrame(hatch_section, fg_color="#0d0d12")
        hatch_container.pack(expand=True)
        
        self.hatch = GlowingHatchCanvas(hatch_container, size=300)
        self.hatch.pack(pady=10)
        
        # === CONTROL PANEL ===
        control_frame = ctk.CTkFrame(self, fg_color="#12121a", corner_radius=12)
        control_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        ctk.CTkLabel(
            control_frame,
            text="CONTROL",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#505068"
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        # Radio buttons row
        radio_row = ctk.CTkFrame(control_frame, fg_color="transparent")
        radio_row.pack(fill="x", padx=20, pady=(0, 20))
        
        self.open_radio = ctk.CTkRadioButton(
            radio_row,
            text="OPEN",
            variable=self.state_var,
            value="open",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#00cc66",
            hover_color="#00ff88",
            border_color="#00aa55",
            text_color="#ccccdd",
            command=self.on_state_change
        )
        self.open_radio.pack(side="left", padx=(20, 40))
        
        self.closed_radio = ctk.CTkRadioButton(
            radio_row,
            text="CLOSED",
            variable=self.state_var,
            value="closed",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#cc3344",
            hover_color="#ff4455",
            border_color="#aa2233",
            text_color="#ccccdd",
            command=self.on_state_change
        )
        self.closed_radio.pack(side="left", padx=20)
        
        # === STATUS BAR ===
        self.status_label = ctk.CTkLabel(
            self,
            text="◉ SYSTEM READY",
            font=ctk.CTkFont(family="Courier", size=13, weight="bold"),
            text_color="#00dd88"
        )
        self.status_label.pack(pady=(0, 25))
    
    def on_state_change(self):
        """Handle state change from radio buttons."""
        state = self.state_var.get()
        
        if state == "open":
            self.open_count += 1
            self.counter_label.configure(text=str(self.open_count))
            self.hatch.set_open(True)
            self.status_label.configure(text="◉ HATCH OPENING...", text_color="#ffcc00")
            self.after(600, lambda: self.status_label.configure(
                text="◉ HATCH OPEN - PRESSURIZED", text_color="#00ff88"))
        else:
            self.hatch.set_open(False)
            self.status_label.configure(text="◉ HATCH SEALED", text_color="#00dd88")


if __name__ == "__main__":
    app = HatchControlApp()
    app.mainloop()

