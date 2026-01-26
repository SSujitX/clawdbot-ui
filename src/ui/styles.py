# Clean Dark Theme - White Buttons, Black Background

DARK_THEME = """
/* ============================================
   BASE - Black Background
   ============================================ */
QWidget {
    background-color: #0d1117;
    color: #ffffff;
    font-family: 'Segoe UI', 'SF Pro Text', sans-serif;
    font-size: 13px;
}

/* Labels should be transparent by default */
QLabel {
    background-color: transparent;
}

/* ============================================
   SIDEBAR
   ============================================ */
QFrame#sidebar {
    background-color: #010409;
    border-right: 1px solid #21262d;
}

QLabel#title {
    background-color: transparent;
    font-size: 18px;
    font-weight: 600;
    color: #ffffff;
}

QLabel#subtitle {
    background-color: transparent;
    color: #8b949e;
    font-size: 11px;
}

/* ============================================
   NAV BUTTONS - White BG, Black Text when selected
   ============================================ */
QPushButton#navBtn {
    text-align: left;
    background-color: transparent;
    border: none;
    border-radius: 6px;
    padding: 10px 14px;
    color: #8b949e;
    font-weight: 500;
    font-size: 13px;
    margin: 2px 6px;
}

QPushButton#navBtn:hover {
    background-color: #21262d;
    color: #ffffff;
}

QPushButton#navBtn:checked {
    background-color: #ffffff;
    color: #000000;
    font-weight: 600;
}

QPushButton#navBtn:checked:hover {
    background-color: #f0f0f0;
    color: #000000;
}

/* ============================================
   STATUS PANEL
   ============================================ */
QFrame#statusPanel {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    margin: 8px 6px;
}

/* ============================================
   CONTENT
   ============================================ */
QWidget#content {
    background-color: #0d1117;
}

/* ============================================
   CARDS
   ============================================ */
QFrame#card {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
}

/* ============================================
   TYPOGRAPHY
   ============================================ */
QLabel#sectionTitle {
    font-size: 24px;
    font-weight: 600;
    color: #ffffff;
}

QLabel#sectionDesc {
    color: #8b949e;
    font-size: 14px;
}

QLabel#cardTitle {
    font-size: 11px;
    font-weight: 600;
    color: #8b949e;
    letter-spacing: 0.5px;
}

/* ============================================
   BUTTONS - White BG, Black Text
   ============================================ */
QPushButton {
    background-color: #ffffff;
    color: #000000;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #e6e6e6;
}

QPushButton:pressed {
    background-color: #cccccc;
}

QPushButton:disabled {
    background-color: #30363d;
    color: #6e7681;
}

/* Primary Button - Keep white */
QPushButton#primaryBtn {
    background-color: #ffffff;
    color: #000000;
}

QPushButton#primaryBtn:hover {
    background-color: #e6e6e6;
}

/* Success Button - Green with white text */
QPushButton#successBtn {
    background-color: #238636;
    color: #ffffff;
}

QPushButton#successBtn:hover {
    background-color: #2ea043;
}

QPushButton#successBtn:disabled {
    background-color: #21262d;
    color: #6e7681;
}

/* Danger Button - Red outline */
QPushButton#dangerBtn {
    background-color: transparent;
    color: #f85149;
    border: 1px solid #f85149;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 500;
}

QPushButton#dangerBtn:hover {
    background-color: rgba(248, 81, 73, 0.1);
}

QPushButton#dangerBtn:disabled {
    color: #6e7681;
    border-color: #30363d;
}

/* Action Button - White with black text */
QPushButton#actionBtn {
    background-color: #ffffff;
    color: #000000;
    border: none;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 500;
}

QPushButton#actionBtn:hover {
    background-color: #e6e6e6;
}

QPushButton#actionBtn:disabled {
    background-color: #30363d;
    color: #6e7681;
}

/* Info Button - Blue */
QPushButton#infoBtn {
    background-color: #1f6feb;
    color: #ffffff;
}

QPushButton#infoBtn:hover {
    background-color: #388bfd;
}

/* ============================================
   INPUTS
   ============================================ */
QLineEdit {
    background-color: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 10px 12px;
    color: #ffffff;
}

QLineEdit:focus {
    border-color: #58a6ff;
}

/* ============================================
   TERMINAL
   ============================================ */
QPlainTextEdit {
    background-color: #010409;
    color: #7ee787;
    border: 1px solid #21262d;
    border-radius: 8px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 12px;
    padding: 12px;
}

/* ============================================
   SCROLLBARS - Simple & Clean
   ============================================ */
QScrollBar:vertical {
    background-color: #0d1117;
    width: 6px;
    margin: 0;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #30363d;
    border-radius: 3px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #484f58;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
    height: 0;
    border: none;
}

QScrollBar:horizontal {
    background-color: #0d1117;
    height: 6px;
    margin: 0;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #30363d;
    border-radius: 3px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #484f58;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: none;
    width: 0;
    border: none;
}

/* ============================================
   TOOLTIPS
   ============================================ */
QToolTip {
    background-color: #161b22;
    color: #ffffff;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px 10px;
}

/* ============================================
   MENUS
   ============================================ */
QMenu {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 6px;
}

QMenu::item {
    padding: 8px 14px;
    border-radius: 4px;
    color: #ffffff;
}

QMenu::item:selected {
    background-color: #21262d;
}

/* ============================================
   DIVIDER
   ============================================ */
QFrame#divider {
    background-color: #21262d;
    max-height: 1px;
}
"""
