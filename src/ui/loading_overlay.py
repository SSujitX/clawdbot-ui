# Loading overlay - blocks interaction during initialization

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor


class LoadingOverlay(QWidget):
    """Fullscreen overlay with blur effect and loading message"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("loadingOverlay")
        
        # Make it fullscreen over parent
        if parent:
            self.setGeometry(parent.rect())
        
        # Setup UI
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Loading message
        self.message = QLabel("Checking ClawdBot...")
        self.message.setStyleSheet("""
            QLabel {
                color: #e6edf3;
                font-size: 16px;
                font-weight: 500;
                background: transparent;
            }
        """)
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.message)
        
        # Animated dots
        self.dot_label = QLabel("...")
        self.dot_label.setStyleSheet("""
            QLabel {
                color: #58a6ff;
                font-size: 18px;
                font-weight: 600;
                background: transparent;
            }
        """)
        self.dot_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.dot_label)
        
        # Semi-transparent dark background with blur
        self.setStyleSheet("""
            QWidget#loadingOverlay {
                background-color: rgba(10, 15, 26, 0.85);
            }
        """)
        
        # Animate dots
        self.dot_count = 0
        self.dot_timer = QTimer(self)
        self.dot_timer.timeout.connect(self._animate_dots)
        self.dot_timer.start(400)
        
        # Block all events
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    
    def _animate_dots(self):
        """Animate the loading dots"""
        self.dot_count = (self.dot_count + 1) % 4
        dots = "." * self.dot_count
        self.dot_label.setText(dots if dots else " ")
    
    def paintEvent(self, event):
        """Paint semi-transparent background"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw backdrop
        backdrop = QColor(10, 15, 26, 217)  # 85% opacity
        painter.fillRect(self.rect(), backdrop)
    
    def resizeEvent(self, event):
        """Ensure overlay covers entire parent"""
        if self.parent():
            self.setGeometry(self.parent().rect())
        super().resizeEvent(event)
    
    def showEvent(self, event):
        """Ensure we're on top and grab focus"""
        super().showEvent(event)
        self.raise_()
        self.setFocus()
    
    def keyPressEvent(self, event):
        """Block all keyboard events"""
        event.accept()
    
    def mousePressEvent(self, event):
        """Block all mouse events"""
        event.accept()
