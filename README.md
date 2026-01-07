# NASA GUI Framework Comparison

This project compares 5 different Python GUI frameworks for building NASA-style control panels. Each implementation has the same functionality (radio buttons for mode selection, digital readouts for telemetry) but showcases the different coding styles and visual appearances.

## Quick Start

```bash
# Install all dependencies
pip install -r requirements.txt

# Run any example
python 01_ttkbootstrap_nasa.py
python 02_customtkinter_nasa.py
python 03_pyqt6_nasa.py
python 04_pyside6_nasa.py
python 05_qt_designer_loader.py
```

## Framework Comparison

| Feature | ttkbootstrap | CustomTkinter | PyQt6 | PySide6 | Qt Designer |
|---------|-------------|---------------|-------|---------|-------------|
| **Base** | tkinter/ttk | tkinter | Qt6 | Qt6 | Qt6 (.ui files) |
| **License** | MIT | MIT | GPL/Commercial | LGPL | LGPL |
| **Learning Curve** | Easy | Easy | Medium | Medium | Easy (visual) |
| **Native Look** | Themed | Modern Custom | Native + Custom | Native + Custom | Native + Custom |
| **Code Verbosity** | Low | Low | Medium | Medium | Low (visual design) |
| **Cross-Platform** | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 1. ttkbootstrap (`01_ttkbootstrap_nasa.py`)

**Best for:** Quick prototypes, Bootstrap-style theming, tkinter familiarity

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Create window with built-in theme
root = ttk.Window(themename="cyborg")

# Widgets use 'bootstyle' parameter for styling
btn = ttk.Button(root, text="Click", bootstyle="danger-outline")
rb = ttk.Radiobutton(root, text="Option", bootstyle="success-toolbutton")
```

**Key Features:**
- 20+ built-in themes (cosmo, darkly, cyborg, vapor, etc.)
- Simple `bootstyle` parameter for colors and styles
- Drop-in replacement for standard ttk
- Familiar tkinter patterns

---

## 2. CustomTkinter (`02_customtkinter_nasa.py`)

**Best for:** Modern-looking apps, dark mode support, rounded widgets

```python
import customtkinter as ctk

# Set appearance mode and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Custom widgets with modern styling
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        btn = ctk.CTkButton(self, text="Click", fg_color="#FF0000")
        rb = ctk.CTkRadioButton(self, text="Option", fg_color="#00FF00")
```

**Key Features:**
- Built-in dark/light mode switching
- Rounded, modern widget appearances
- CTkFont for consistent typography
- Automatic DPI scaling

---

## 3. PyQt6 (`03_pyqt6_nasa.py`)

**Best for:** Complex applications, extensive widget library, commercial projects (with license)

```python
from PyQt6.QtWidgets import QApplication, QMainWindow, QRadioButton
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: #1a1a2e;")
        
        rb = QRadioButton("Option")
        rb.setStyleSheet("QRadioButton::indicator:checked { background: red; }")
```

**Key Features:**
- Comprehensive widget set
- Powerful QSS (CSS-like) styling
- Signal/slot mechanism for events
- QTimer for updates
- Extensive documentation

---

## 4. PySide6 (`04_pyside6_nasa.py`)

**Best for:** Commercial projects (LGPL), Qt integration, same features as PyQt6

```python
from PySide6.QtWidgets import QApplication, QMainWindow, QRadioButton
from PySide6.QtCore import Qt

# Nearly identical to PyQt6!
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        rb = QRadioButton("Option")
```

**Key Differences from PyQt6:**
- LGPL license (more permissive for commercial use)
- Official Qt binding (maintained by Qt Company)
- `Signal` instead of `pyqtSignal`
- Minor API differences in some areas

---

## 5. Qt Designer (`05_qt_designer_nasa.ui` + `05_qt_designer_loader.py`)

**Best for:** Visual design, team collaboration, separating design from logic

### Workflow:

1. **Design visually** → Open Qt Designer:
   ```bash
   pyside6-designer
   ```

2. **Create .ui file** → Drag-drop widgets, set properties, save

3. **Load in Python:**
   ```python
   from PySide6.QtUiTools import QUiLoader
   
   loader = QUiLoader()
   ui = loader.load("design.ui")
   ui.buttonName.clicked.connect(self.handler)
   ```

**Advantages:**
- WYSIWYG editing
- Non-programmers can design UI
- Preview without running code
- Clean separation of concerns

---

## Code Pattern Comparison

### Creating a Window

| Framework | Code |
|-----------|------|
| ttkbootstrap | `root = ttk.Window(title="App", themename="darkly")` |
| CustomTkinter | `class App(ctk.CTk): ...` then `app = App()` |
| PyQt6/PySide6 | `class Window(QMainWindow): ...` then `window = Window()` |
| Qt Designer | Design in GUI, load with `QUiLoader` |

### Radio Buttons

| Framework | Code |
|-----------|------|
| ttkbootstrap | `ttk.Radiobutton(parent, text="Opt", variable=var, value="x", bootstyle="success")` |
| CustomTkinter | `ctk.CTkRadioButton(parent, text="Opt", variable=var, value="x", fg_color="#00FF00")` |
| PyQt6/PySide6 | `rb = QRadioButton("Opt")` + `QButtonGroup` for mutual exclusion |
| Qt Designer | Drag RadioButton widget, set properties in panel |

### Styling

| Framework | Method |
|-----------|--------|
| ttkbootstrap | `bootstyle` parameter + themes |
| CustomTkinter | `fg_color`, `text_color`, etc. parameters |
| PyQt6/PySide6 | `setStyleSheet()` with QSS (CSS-like) |
| Qt Designer | Property panel or stylesheet editor |

### Event Loop / Timers

| Framework | Timer Code |
|-----------|------------|
| ttkbootstrap | `root.after(500, callback)` |
| CustomTkinter | `self.after(500, callback)` |
| PyQt6/PySide6 | `QTimer.timeout.connect(callback)` |

---

## Recommendations by Use Case

| Use Case | Recommended Framework |
|----------|----------------------|
| Quick prototype | ttkbootstrap or CustomTkinter |
| Modern dark UI | CustomTkinter |
| Complex enterprise app | PyQt6 or PySide6 |
| Commercial product (free) | PySide6 (LGPL) |
| Team with designers | Qt Designer + PySide6 |
| Learning GUI programming | ttkbootstrap (simplest) |
| NASA/Industrial look | Any (all support dark themes) |

---

## File Structure

```
nasa_gui_comparison/
├── 01_ttkbootstrap_nasa.py    # ttkbootstrap example
├── 02_customtkinter_nasa.py   # CustomTkinter example
├── 03_pyqt6_nasa.py           # PyQt6 example
├── 04_pyside6_nasa.py         # PySide6 example
├── 05_qt_designer_nasa.ui     # Qt Designer UI file
├── 05_qt_designer_loader.py   # Python loader for .ui file
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

---

## Modifying the Examples

### Adding a New Readout

1. **ttkbootstrap/CustomTkinter:** Add to `self.telemetry_values` dict, create label + display widget
2. **PyQt6/PySide6:** Add to `self.telemetry` dict, create `DigitalDisplay` widget, add to grid
3. **Qt Designer:** Drag QLabel widgets, set objectName, reference in Python

### Changing Colors

1. **ttkbootstrap:** Change `themename` or use different `bootstyle` values
2. **CustomTkinter:** Modify `fg_color`, `text_color` parameters
3. **PyQt6/PySide6:** Edit the stylesheet string in `_get_stylesheet()`
4. **Qt Designer:** Edit styleSheet property in property panel

### Adding New Modes

Add to the `modes` list and `status_messages` dict in each file.

---

## Launch Qt Designer

```bash
# With PySide6 installed:
pyside6-designer

# Or with PyQt6:
pyqt6-tools designer
```

