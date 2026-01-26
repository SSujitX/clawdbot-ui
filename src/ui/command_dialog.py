# Popup terminal dialog for command output

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
)
from PyQt6.QtCore import Qt
from src.ui.terminal import Terminal
from src.core.process import ProcessRunner


class CommandDialog(QDialog):
    # Popup dialog that shows real-time command output
    
    def __init__(self, parent=None, title="Running Command"):
        super().__init__(parent)
        self.runner = None
        self._setup_ui(title)
    
    def _setup_ui(self, title):
        self.setWindowTitle(title)
        self.setMinimumSize(600, 400)
        self.setModal(True)
        
        # Dark theme styling
        self.setStyleSheet("""
            QDialog {
                background-color: #0d1117;
                color: #ffffff;
            }
            QLabel {
                background: transparent;
                color: #ffffff;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton#closeBtn {
                background-color: #21262d;
                color: #c9d1d9;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: 500;
            }
            QPushButton#closeBtn:hover {
                background-color: #30363d;
                border-color: #8b949e;
            }
            QPushButton#closeBtn:disabled {
                color: #6e7681;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Header
        self.header = QLabel(title)
        layout.addWidget(self.header)
        
        # Terminal
        self.terminal = Terminal()
        self.terminal.setMinimumHeight(280)
        layout.addWidget(self.terminal)
        
        # Footer buttons
        footer = QHBoxLayout()
        footer.addStretch()
        
        self.copy_btn = QPushButton("Copy Log")
        self.copy_btn.setObjectName("closeBtn")
        self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_btn.clicked.connect(self._copy_log)
        footer.addWidget(self.copy_btn)
        
        self.close_btn = QPushButton("Close")
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setEnabled(False)  # Disabled while running
        footer.addWidget(self.close_btn)
        
        layout.addLayout(footer)
    
    def run_command(self, cmd, shell=False):
        # Run command and show output in terminal
        self.terminal.log(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
        self.terminal.log("-" * 50)
        
        self.runner = ProcessRunner(cmd, shell=shell)
        self.runner.output.connect(self.terminal.log)
        self.runner.finished.connect(self._on_finished)
        self.runner.start()
    
    def _on_finished(self, exit_code):
        self.terminal.log("-" * 50)
        if exit_code == 0:
            self.terminal.log("✓ Command completed successfully!")
        else:
            self.terminal.log(f"✗ Command exited with code: {exit_code}")
        
        self.close_btn.setEnabled(True)
        self.header.setText(f"{self.header.text()} - Done")
    
    def _copy_log(self):
        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText(self.terminal.toPlainText())
        self.copy_btn.setText("Copied!")
    
    def closeEvent(self, event):
        # Stop any running command when closing
        if self.runner and self.runner.isRunning():
            self.runner.stop()
            self.runner.wait(2000)
        event.accept()
