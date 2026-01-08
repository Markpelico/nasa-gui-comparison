# Hatch Control - GUI Framework Comparison

Simple GUI demonstrating radio buttons and visual feedback across 5 Python GUI frameworks.

## The Design

Based on a test diagram showing:
- **Radio buttons**: Open / Closed
- **Hatch circle**: Green when Open, Black when Closed  
- **Counter**: Increments each time "Open" is clicked

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run any version
python 01_ttkbootstrap_nasa.py
python 02_customtkinter_nasa.py
python 03_pyqt6_nasa.py
python 04_pyside6_nasa.py
python 05_qt_designer_loader.py
```

## Framework Comparison

| Framework | Circle Drawing | Radio Button Style |
|-----------|---------------|-------------------|
| **ttkbootstrap** | Canvas oval | `bootstyle="success"` |
| **CustomTkinter** | CTkCanvas oval | `fg_color="green"` |
| **PyQt6** | Custom QWidget + QPainter | QSS stylesheet |
| **PySide6** | Custom QWidget + QPainter | QSS stylesheet |
| **Qt Designer** | Placeholder → custom widget | Visual property panel |

## Code Patterns

### Drawing a Circle

**tkinter-based (ttkbootstrap, CustomTkinter):**
```python
canvas = Canvas(parent, width=240, height=240)
circle = canvas.create_oval(10, 10, 230, 230, fill="black")
canvas.itemconfig(circle, fill="green")  # Change color
```

**Qt-based (PyQt6, PySide6):**
```python
class HatchWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(self._color))
        painter.drawEllipse(rect)
```

### Radio Buttons

**ttkbootstrap:**
```python
radio = ttk.Radiobutton(parent, text="Open", variable=var, 
                        value="open", command=callback, bootstyle="success")
```

**CustomTkinter:**
```python
radio = ctk.CTkRadioButton(parent, text="Open", variable=var,
                           value="open", command=callback, fg_color="green")
```

**PyQt6/PySide6:**
```python
radio = QRadioButton("Open")
group = QButtonGroup(self)
group.addButton(radio)
radio.clicked.connect(callback)
```

## Files

```
nasa_gui_comparison/
├── 01_ttkbootstrap_nasa.py    # ttkbootstrap version
├── 02_customtkinter_nasa.py   # CustomTkinter version
├── 03_pyqt6_nasa.py           # PyQt6 version
├── 04_pyside6_nasa.py         # PySide6 version
├── 05_qt_designer_nasa.ui     # Qt Designer layout file
├── 05_qt_designer_loader.py   # Loads .ui + adds logic
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## Key Differences

| Aspect | tkinter-based | Qt-based |
|--------|--------------|----------|
| Canvas drawing | Built-in Canvas widget | Custom paintEvent() |
| Color change | `itemconfig(id, fill=color)` | `widget.update()` |
| Event loop | `root.mainloop()` | `app.exec()` |
| Styling | bootstyle / fg_color params | QSS stylesheets |
