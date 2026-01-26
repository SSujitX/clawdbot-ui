# Application initialization and entry point

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from src.ui.window import MainWindow, get_icon_path
from src.ui.styles import DARK_THEME


def run() -> int:
    # Initialize and run the application
    
    # Enable high DPI support (must be before QApplication)
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    
    # Set application icon (shows in taskbar)
    icon_path = get_icon_path()
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Set application metadata
    app.setApplicationName("ClawdBot Control Panel")
    app.setOrganizationName("ClawdBot")
    
    # Apply dark theme
    app.setStyleSheet(DARK_THEME)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    return app.exec()
