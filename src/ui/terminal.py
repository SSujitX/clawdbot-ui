# Terminal log widget with real-time output and copy support

import re
from PyQt6.QtWidgets import QPlainTextEdit, QMenu
from PyQt6.QtGui import QFont, QAction
from PyQt6.QtCore import pyqtSignal, QObject

# Regex to strip ANSI escape codes
ANSI_PATTERN = re.compile(r'\x1b\[[0-9;]*m|\[\d+m')


def clean_log(text: str) -> str:
    # Remove ANSI codes and format log line
    text = ANSI_PATTERN.sub('', text)
    text = text.strip()
    
    if not text:
        return ""
    
    # Format timestamp and brackets for readability
    # Pattern: 2026-01-26T09:02:00.682Z [module] message
    match = re.match(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z)\s*\[([^\]]+)\]\s*(.*)$', text)
    if match:
        time = match.group(1)[11:19]  # Extract HH:MM:SS
        module = match.group(2).strip()
        msg = match.group(3).strip()
        return f"[{time}] [{module}] {msg}"
    
    return text


class LogSignal(QObject):
    # Signal for thread-safe log updates
    append = pyqtSignal(str)
    clear = pyqtSignal()


class Terminal(QPlainTextEdit):
    # Real-time terminal log viewer
    
    def __init__(self):
        super().__init__()
        self._setup_widget()
        self._setup_signals()
    
    def _setup_widget(self):
        # Configure terminal appearance and behavior
        self.setReadOnly(True)
        self.setMaximumBlockCount(5000)
        self.setFont(QFont("Consolas", 10))
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
    
    def _setup_signals(self):
        # Connect thread-safe signals
        self.signal = LogSignal()
        self.signal.append.connect(self._append_text)
        self.signal.clear.connect(self.clear)
    
    def _append_text(self, text: str):
        # Clean and add text, scroll to bottom
        cleaned = clean_log(text)
        if cleaned:
            self.appendPlainText(cleaned)
            scrollbar = self.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
    
    def log(self, text: str):
        # Thread-safe logging method
        self.signal.append.emit(text)
    
    def clear_logs(self):
        # Thread-safe clear method
        self.signal.clear.emit()
    
    def contextMenuEvent(self, event):
        # Custom right-click menu
        menu = QMenu(self)
        
        copy_action = QAction("Copy Selection", self)
        copy_action.triggered.connect(self.copy)
        menu.addAction(copy_action)
        
        copy_all_action = QAction("Copy All", self)
        copy_all_action.triggered.connect(self._copy_all)
        menu.addAction(copy_all_action)
        
        menu.addSeparator()
        
        clear_action = QAction("Clear", self)
        clear_action.triggered.connect(self.clear)
        menu.addAction(clear_action)
        
        menu.exec(event.globalPos())
    
    def _copy_all(self):
        # Copy entire log content to clipboard
        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText(self.toPlainText())

