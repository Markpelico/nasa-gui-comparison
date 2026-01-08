# Hatch Control GUI - Framework Comparison

Professional aerospace-style hatch control interface implemented in 5 different Python GUI frameworks. Each version demonstrates the same functionality with framework-specific approaches and styling.

![Hatch Control Preview](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Features

All implementations include:

- **🔘 Radio Buttons** - Open/Closed state selection
- **⭕ Animated Hatch Circle** - Glowing green (open) or dark (closed)
- **🔢 Cycle Counter** - Increments each time "Open" is clicked
- **✨ Smooth Animations** - Pulsing glow effects and transitions
- **🌙 Dark Aerospace Theme** - Professional industrial styling

## 🚀 Quick Start

```bash
# Install all dependencies
pip install -r requirements.txt

# Run any version
python 01_ttkbootstrap_hatch.py
python 02_customtkinter_hatch.py
python 03_pyqt6_hatch.py
python 04_pyside6_hatch.py
python 05_qt_designer_hatch_loader.py
```

## 📁 File Structure

```
nasa_gui_comparison/
├── 01_ttkbootstrap_hatch.py      # Bootstrap-themed tkinter
├── 02_customtkinter_hatch.py     # Modern CustomTkinter
├── 03_pyqt6_hatch.py             # PyQt6 with animations
├── 04_pyside6_hatch.py           # PySide6 (LGPL, orange theme)
├── 05_qt_designer_hatch.ui       # Qt Designer visual layout
├── 05_qt_designer_hatch_loader.py # Loader for .ui file
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

## 🔍 Framework Comparison

| Feature | ttkbootstrap | CustomTkinter | PyQt6 | PySide6 | Qt Designer |
|---------|-------------|---------------|-------|---------|-------------|
| **Base** | tkinter/ttk | tkinter | Qt6 | Qt6 | Qt6 (.ui) |
| **License** | MIT | MIT | GPL/Commercial | LGPL | LGPL |
| **Styling** | bootstyle="" | fg_color="" | QSS (CSS-like) | QSS | Property panel |
| **Animation** | after() | after() | QPropertyAnimation | QPropertyAnimation | Python code |
| **Custom Paint** | Canvas | CTkCanvas | paintEvent() | paintEvent() | paintEvent() |
| **Learning Curve** | Easy | Easy | Medium | Medium | Easy (visual) |

## 🎨 Visual Differences

Each framework has a unique color accent to make them distinguishable:

| Framework | Primary Accent | Counter Color |
|-----------|---------------|---------------|
| ttkbootstrap | Cyan (#00ccff) | Green (#00ff88) |
| CustomTkinter | Cyan (#00ddff) | Green (#00ff99) |
| PyQt6 | Cyan (#00ddff) | Green (#00ff99) |
| PySide6 | Orange (#ff8844) | Orange (#ff9955) |
| Qt Designer | Cyan (#44ddff) | Green (#00ff99) |

## 💻 Code Patterns

### Radio Button Creation

**ttkbootstrap:**
```python
ttk.Radiobutton(
    parent,
    text="OPEN",
    variable=self.state_var,
    value="open",
    bootstyle="success-toolbutton-outline",
    command=self.on_state_change
)
```

**CustomTkinter:**
```python
ctk.CTkRadioButton(
    parent,
    text="OPEN",
    variable=self.state_var,
    value="open",
    fg_color="#00cc66",
    command=self.on_state_change
)
```

**PyQt6/PySide6:**
```python
radio = QRadioButton("OPEN")
radio.setStyleSheet("""
    QRadioButton::indicator:checked {
        background-color: #00cc66;
    }
""")
radio.clicked.connect(self.on_open)
```

### Custom Painting (Hatch Circle)

**tkinter/ttkbootstrap:**
```python
class GlowingHatch(ttk.Canvas):
    def draw_hatch(self):
        self.create_oval(x1, y1, x2, y2, fill=color, outline=outline)
```

**PyQt6/PySide6:**
```python
class HatchWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(rect)
```

### Animation Timers

**tkinter-based:**
```python
self.root.after(50, self._animate_glow)  # 50ms timer
```

**Qt-based:**
```python
self.timer = QTimer(self)
self.timer.timeout.connect(self._animate)
self.timer.start(40)  # 40ms timer
```

## 🛠 Modifying the Code

### Change Hatch Colors

Look for these variables in each file:
- Open color: Usually `#00ff88` or similar green
- Closed color: Usually `#0d0d0d` or dark variant
- Glow color: Calculated from base color with alpha

### Add More States

1. Add new radio button to the UI
2. Add handler function
3. Update hatch color logic in `set_open()` or paint methods

### Change Animation Speed

- tkinter: Modify `after(50, ...)` milliseconds
- Qt: Modify `timer.start(40)` or `QPropertyAnimation.setDuration()`

## 🎓 Learning Resources

- [ttkbootstrap Docs](https://ttkbootstrap.readthedocs.io/)
- [CustomTkinter Docs](https://customtkinter.tomschimansky.com/)
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [PySide6 Documentation](https://doc.qt.io/qtforpython-6/)
- [Qt Designer Manual](https://doc.qt.io/qt-6/qtdesigner-manual.html)

## 📄 License

MIT License - Use freely for your aerospace GUI projects!

