---
name: pyqt6-development
description: PyQt6 dark theme UI development with responsive design and real-time updates
---

# PyQt6 Development Guide

## Installation

```bash
uv add pyqt6
```

## Dark Theme Base

```python
DARK_THEME = """
/* Antigravity Dark Theme - Cyan Accent */
QWidget {
    background-color: #0a0f1a;
    color: #b0b8c4;
    font-family: 'Segoe UI', 'Inter', Arial, sans-serif;
    font-size: 13px;
}

/* Sidebar */
QFrame#sidebar {
    background-color: #0f1419;
    border-right: 1px solid #2a3545;
}

/* Cards */
QFrame#card {
    background-color: #1a2535;
    border: 1px solid #2a3545;
    border-radius: 8px;
}
QFrame#card:hover {
    border-color: #3a4555;
}
QFrame#card[selected="true"] {
    border-color: #00bfa5;
}

/* Primary Button (Teal/Cyan) */
QPushButton#primary {
    background-color: #00bfa5;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    color: #0a0f1a;
    font-weight: 600;
}
QPushButton#primary:hover {
    background-color: #00d4aa;
}
QPushButton#primary:pressed {
    background-color: #00a896;
}

/* Secondary Button (Outlined) */
QPushButton#secondary {
    background-color: transparent;
    border: 1px solid #3a4555;
    border-radius: 6px;
    padding: 10px 20px;
    color: #b0b8c4;
    font-weight: 500;
}
QPushButton#secondary:hover {
    background-color: #1a2535;
    border-color: #4a5565;
}

/* Danger Button (Red) */
QPushButton#danger {
    background-color: #ef4444;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    color: #ffffff;
    font-weight: 600;
}
QPushButton#danger:hover {
    background-color: #f87171;
}

/* Default Button */
QPushButton {
    background-color: #1a2535;
    border: 1px solid #2a3545;
    border-radius: 6px;
    padding: 10px 20px;
    color: #ffffff;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #243045;
    border-color: #3a4555;
}
QPushButton:pressed {
    background-color: #0f1925;
}
QPushButton:disabled {
    background-color: #0f1419;
    color: #4a5565;
    border-color: #1a2535;
}

/* Terminal/Log Viewer */
QPlainTextEdit {
    background-color: #0a0f1a;
    color: #22c55e;
    border: 1px solid #2a3545;
    border-radius: 6px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 12px;
    padding: 12px;
}

/* Toggle Switch Colors */
/* ON state: #00bfa5 (cyan) */
/* OFF state: #3a4555 (gray) */

/* Labels */
QLabel {
    color: #b0b8c4;
}
QLabel#heading {
    color: #ffffff;
    font-size: 18px;
    font-weight: 600;
}
QLabel#subheading {
    color: #6b7280;
    font-size: 12px;
}

/* Inputs */
QLineEdit, QComboBox {
    background-color: #1a2535;
    border: 1px solid #2a3545;
    border-radius: 6px;
    padding: 8px 12px;
    color: #ffffff;
}
QLineEdit:focus, QComboBox:focus {
    border-color: #00bfa5;
}

/* Scrollbar */
QScrollBar:vertical {
    background-color: #0f1419;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background-color: #2a3545;
    border-radius: 4px;
    min-height: 40px;
}
QScrollBar::handle:vertical:hover {
    background-color: #3a4555;
}
"""
```

## Application Structure

```python
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ClawdBot UI")
        self.setMinimumSize(900, 600)
        self.setup_ui()
    
    def setup_ui(self):
        # Build UI here
        pass

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLE)
    
    # High DPI support
    app.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

## Real-time Terminal Log Widget

```python
from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtGui import QFont, QTextCursor
from PyQt6.QtCore import pyqtSignal, QObject

class LogSignal(QObject):
    append = pyqtSignal(str)

class TerminalLog(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setMaximumBlockCount(5000)  # Limit lines for performance
        self.setFont(QFont("Consolas", 10))
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #0d0d1a;
                color: #00ff88;
                border: 1px solid #2a2a4a;
                border-radius: 4px;
            }
        """)
        
        # Thread-safe signal
        self.log_signal = LogSignal()
        self.log_signal.append.connect(self._append_text)
    
    def _append_text(self, text: str):
        self.appendPlainText(text.rstrip())
        self.verticalScrollBar().setValue(
            self.verticalScrollBar().maximum()
        )
    
    def log(self, text: str):
        """Thread-safe log method"""
        self.log_signal.append.emit(text)
```

## Background Process Runner (Lag-Free)

```python
from PyQt6.QtCore import QThread, pyqtSignal
import subprocess
import sys

class ProcessRunner(QThread):
    output = pyqtSignal(str)
    error = pyqtSignal(str)
    finished = pyqtSignal(int)
    
    def __init__(self, command: list[str], shell: bool = False):
        super().__init__()
        self.command = command
        self.shell = shell
        self.process = None
        self._stop = False
    
    def run(self):
        try:
            # Platform-specific setup
            startupinfo = None
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            self.process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=self.shell,
                text=True,
                bufsize=1,
                startupinfo=startupinfo
            )
            
            # Stream output line by line
            for line in iter(self.process.stdout.readline, ''):
                if self._stop:
                    break
                self.output.emit(line)
            
            self.process.wait()
            self.finished.emit(self.process.returncode)
            
        except Exception as e:
            self.error.emit(str(e))
            self.finished.emit(-1)
    
    def stop(self):
        self._stop = True
        if self.process:
            self.process.terminate()
```

## Responsive Layout

```python
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QSplitter
)
from PyQt6.QtCore import Qt

class ResponsiveLayout(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.addWidget(QPushButton("Start"))
        left_layout.addWidget(QPushButton("Stop"))
        left_layout.addStretch()
        
        # Right panel (logs)
        self.log = TerminalLog()
        
        splitter.addWidget(left)
        splitter.addWidget(self.log)
        splitter.setSizes([200, 700])
        
        layout.addWidget(splitter)
```

## Copy Text from Terminal

```python
def contextMenuEvent(self, event):
    menu = self.createStandardContextMenu()
    
    copy_action = menu.addAction("Copy All")
    copy_action.triggered.connect(self.copy_all)
    
    clear_action = menu.addAction("Clear")
    clear_action.triggered.connect(self.clear)
    
    menu.exec(event.globalPos())

def copy_all(self):
    from PyQt6.QtWidgets import QApplication
    QApplication.clipboard().setText(self.toPlainText())
```

## Performance Tips

1. **Use QThread** for all subprocess operations
2. **Limit log lines** with `setMaximumBlockCount()`
3. **Batch updates** - don't emit signals too frequently
4. **Use signals** for thread-to-UI communication
5. **Avoid blocking** the main thread

## Run Application

```bash
uv run main.py
```

## Log Formatting

Clean ANSI codes and format logs for readability:

```python
import re

ANSI_PATTERN = re.compile(r'\x1b\[[0-9;]*m|\[\d+m')

def clean_log(text: str) -> str:
    # Remove ANSI codes
    text = ANSI_PATTERN.sub('', text).strip()
    if not text:
        return ""
    
    # Format: 2026-01-26T09:02:00.682Z [module] msg -> [09:02:00] [module] msg
    match = re.match(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z)\s*\[([^\]]+)\]\s*(.*)$', text)
    if match:
        time = match.group(1)[11:19]
        module = match.group(2).strip()
        msg = match.group(3).strip()
        return f"[{time}] [{module}] {msg}"
    return text
```

