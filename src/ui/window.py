# Main window - ClawdBot control panel UI

import os
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QStackedWidget,
    QButtonGroup,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap

from src.ui.terminal import Terminal
from src.ui.command_dialog import CommandDialog
from src.ui.loading_overlay import LoadingOverlay
from src.core.process import ProcessRunner
from src.core.version import get_version_status
from src.utils.platform import get_gateway_command, get_install_command, is_windows


def get_icon_path():
    """Get the path to the ClawdBot icon"""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base_dir, "assets", "clawdbot.png")


class VersionChecker(QThread):
    finished = pyqtSignal(dict)

    def run(self):
        status = get_version_status()
        self.finished.emit(status)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.gateway_runner = None
        self.version_status = None
        self.loading_overlay = None
        self._setup_window()
        self._setup_ui()
        self._show_loading_overlay()
        self._check_version()

    def _setup_window(self):
        self.setWindowTitle("ClawdBot Control Panel")
        self.setMinimumSize(900, 600)
        self.resize(1000, 680)

        icon_path = get_icon_path()
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._create_sidebar())

        self.stack = QStackedWidget()
        self.stack.setObjectName("content")
        layout.addWidget(self.stack)

        # Create pages
        self.dashboard_page = self._create_dashboard_page()
        self.clawdhub_page = self._create_clawdhub_page()
        self.terminal_page = self._create_terminal_page()
        self.settings_page = self._create_settings_page()
        
        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.clawdhub_page)
        self.stack.addWidget(self.terminal_page)
        self.stack.addWidget(self.settings_page)
        self.stack.setCurrentWidget(self.dashboard_page)

    def _create_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(240)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 24, 20, 24)
        layout.setSpacing(4)

        # Brand Section
        brand_container = QWidget()
        brand_container.setObjectName("brandContainer")
        brand_container.setStyleSheet("""
            QWidget#brandContainer {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 10px;
            }
        """)
        brand_layout = QHBoxLayout(brand_container)
        brand_layout.setContentsMargins(12, 12, 12, 12)
        brand_layout.setSpacing(12)

        icon_path = get_icon_path()
        if os.path.exists(icon_path):
            logo_label = QLabel()
            pixmap = QPixmap(icon_path)
            scaled_pixmap = pixmap.scaled(
                40,
                40,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setFixedSize(40, 40)
            brand_layout.addWidget(logo_label)

        title_stack = QWidget()
        title_stack.setStyleSheet("background: transparent;")
        title_layout = QVBoxLayout(title_stack)
        title_layout.setContentsMargins(0,0,0,0)
        title_layout.setSpacing(0)

        title = QLabel("ClawdBot")
        title.setObjectName("title")
        title_layout.addWidget(title)

        subtitle = QLabel("Control Panel")
        subtitle.setObjectName("subtitle")
        title_layout.addWidget(subtitle)

        self.header_version = QLabel("")
        self.header_version.setStyleSheet("background: transparent; color: #6e7681; font-size: 10px;")
        title_layout.addWidget(self.header_version)

        brand_layout.addWidget(title_stack)
        brand_layout.addStretch()

        layout.addWidget(brand_container)
        layout.addSpacing(28)

        # Nav Buttons (exclusive group - only one selected at a time)
        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        
        self.nav_dashboard = self._add_nav_btn(layout, "Dashboard")
        self.nav_clawdhub = self._add_nav_btn(layout, "ClawdHub")
        self.nav_terminal = self._add_nav_btn(layout, "Terminal")
        self.nav_settings = self._add_nav_btn(layout, "Settings")
        
        # Add to exclusive group
        self.nav_group.addButton(self.nav_dashboard)
        self.nav_group.addButton(self.nav_clawdhub)
        self.nav_group.addButton(self.nav_terminal)
        self.nav_group.addButton(self.nav_settings)
        
        # Connect to page switching
        self.nav_dashboard.clicked.connect(lambda: self.stack.setCurrentWidget(self.dashboard_page))
        self.nav_clawdhub.clicked.connect(lambda: self.stack.setCurrentWidget(self.clawdhub_page))
        self.nav_terminal.clicked.connect(lambda: self.stack.setCurrentWidget(self.terminal_page))
        self.nav_settings.clicked.connect(lambda: self.stack.setCurrentWidget(self.settings_page))
        
        # Set Dashboard as default selected
        self.nav_dashboard.setChecked(True)

        layout.addStretch()

        # Quick Links Section
        links_label = QLabel("QUICK LINKS")
        links_label.setStyleSheet(
            "background: transparent; color: #484f58; font-size: 10px; font-weight: 600; letter-spacing: 1px; margin-bottom: 8px;"
        )
        layout.addWidget(links_label)

        # Links row
        links_row = QHBoxLayout()
        links_row.setSpacing(6)
        links_row.setContentsMargins(0, 0, 0, 0)

        skills_btn = QPushButton("Skills")
        skills_btn.setObjectName("linkBtn")
        skills_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        skills_btn.setToolTip("Browse ClawdHub Skills")
        skills_btn.clicked.connect(lambda: self._open_url("https://clawdhub.com/skills"))
        skills_btn.setStyleSheet("""
            QPushButton#linkBtn {
                background-color: #1a2332;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 6px 10px;
                color: #8b949e;
                font-size: 11px;
                font-weight: 500;
            }
            QPushButton#linkBtn:hover {
                background-color: #243045;
                border-color: #58a6ff;
                color: #58a6ff;
            }
        """)
        links_row.addWidget(skills_btn)

        docs_btn = QPushButton("Docs")
        docs_btn.setObjectName("linkBtn")
        docs_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        docs_btn.setToolTip("Open Documentation")
        docs_btn.clicked.connect(lambda: self._open_url("https://docs.clawd.bot/"))
        docs_btn.setStyleSheet("""
            QPushButton#linkBtn {
                background-color: #1a2332;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 6px 10px;
                color: #8b949e;
                font-size: 11px;
                font-weight: 500;
            }
            QPushButton#linkBtn:hover {
                background-color: #243045;
                border-color: #58a6ff;
                color: #58a6ff;
            }
        """)
        links_row.addWidget(docs_btn)

        layout.addLayout(links_row)
        layout.addSpacing(12)

        # Status Panel
        status_panel = QFrame()
        status_panel.setObjectName("statusPanel")
        status_panel.setStyleSheet("""
            QFrame#statusPanel {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 10px;
            }
        """)
        status_layout = QVBoxLayout(status_panel)
        status_layout.setContentsMargins(12, 12, 12, 12)
        status_layout.setSpacing(10)

        status_header = QHBoxLayout()
        status_title = QLabel("STATUS")
        status_title.setStyleSheet(
            "background: transparent; color: #484f58; font-size: 10px; font-weight: 600; letter-spacing: 1px;"
        )
        status_header.addWidget(status_title)
        status_header.addStretch()
        status_layout.addLayout(status_header)

        self.status_label = QLabel("Checking...")
        self.status_label.setStyleSheet(
            "background: transparent; color: #e6edf3; font-weight: 500; font-size: 13px;"
        )
        self.status_label.setWordWrap(True)
        status_layout.addWidget(self.status_label)

        # Quick stop button (hidden by default, shown when running)
        self.quick_stop_btn = QPushButton("Stop Gateway")
        self.quick_stop_btn.setObjectName("dangerBtn")
        self.quick_stop_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.quick_stop_btn.clicked.connect(self._on_stop)
        self.quick_stop_btn.setVisible(False)
        self.quick_stop_btn.setMinimumHeight(32)
        status_layout.addWidget(self.quick_stop_btn)

        layout.addWidget(status_panel)

        return sidebar

    def _add_nav_btn(self, layout, text):
        btn = QPushButton(text)
        btn.setObjectName("navBtn")
        btn.setCheckable(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(36)
        layout.addWidget(btn)
        return btn

    def _create_dashboard_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(36, 36, 36, 36)
        layout.setSpacing(20)

        # Header
        header = QLabel("Gateway Control")
        header.setObjectName("sectionTitle")
        layout.addWidget(header)

        desc = QLabel("Manage the local ClawdBot gateway service.")
        desc.setObjectName("sectionDesc")
        layout.addWidget(desc)

        # Controls Card
        controls_card = QFrame()
        controls_card.setObjectName("card")
        card_layout = QVBoxLayout(controls_card)
        card_layout.setContentsMargins(24, 20, 24, 20)
        card_layout.setSpacing(18)

        # Status Row
        status_row = QHBoxLayout()
        status_row.setSpacing(12)

        status_title = QLabel("Service Status")
        status_title.setStyleSheet("font-weight: 600; color: #e6edf3; font-size: 14px;")
        status_row.addWidget(status_title)
        status_row.addStretch()

        self.indicator = QLabel("● Stopped")
        self.indicator.setStyleSheet(
            """
            color: #7d8590;
            font-weight: 600;
            font-size: 12px;
            background-color: #21262d;
            padding: 5px 12px;
            border-radius: 4px;
        """
        )
        status_row.addWidget(self.indicator)

        card_layout.addLayout(status_row)

        # Divider
        divider = QFrame()
        divider.setObjectName("divider")
        divider.setFixedHeight(1)
        card_layout.addWidget(divider)

        # Buttons Row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.start_btn = QPushButton("Start Service")
        self.start_btn.setObjectName("actionBtn")
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.clicked.connect(self._on_start)
        self.start_btn.setFixedWidth(110)
        btn_row.addWidget(self.start_btn)

        self.stop_btn = QPushButton("Stop Service")
        self.stop_btn.setObjectName("actionBtn")
        self.stop_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stop_btn.clicked.connect(self._on_stop)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setFixedWidth(110)
        btn_row.addWidget(self.stop_btn)

        # Open Gateway button (visible when running)
        self.open_btn = QPushButton("Open Gateway")
        self.open_btn.setObjectName("actionBtn")
        self.open_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.open_btn.clicked.connect(self._on_open_gateway)
        self.open_btn.setVisible(False)
        self.open_btn.setFixedWidth(110)
        btn_row.addWidget(self.open_btn)

        # Open UI button (visible when running)
        self.open_ui_btn = QPushButton("Open UI")
        self.open_ui_btn.setObjectName("actionBtn")
        self.open_ui_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.open_ui_btn.clicked.connect(self._on_open_ui)
        self.open_ui_btn.setVisible(False)
        self.open_ui_btn.setFixedWidth(110)
        btn_row.addWidget(self.open_ui_btn)

        btn_row.addStretch()

        self.install_btn = QPushButton("Install ClawdBot")
        self.install_btn.setObjectName("primaryBtn")
        self.install_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.install_btn.clicked.connect(self._on_install)
        self.install_btn.setVisible(False)
        btn_row.addWidget(self.install_btn)

        self.update_btn = QPushButton("Upgrade")
        self.update_btn.setObjectName("infoBtn")
        self.update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_btn.clicked.connect(self._on_update)
        self.update_btn.setVisible(False)
        btn_row.addWidget(self.update_btn)

        self.uninstall_btn = QPushButton("Uninstall")
        self.uninstall_btn.setObjectName("dangerBtn")
        self.uninstall_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.uninstall_btn.clicked.connect(self._on_uninstall)
        self.uninstall_btn.setVisible(False)
        btn_row.addWidget(self.uninstall_btn)

        card_layout.addLayout(btn_row)
        layout.addWidget(controls_card)

        # Terminal Header Row
        term_header = QHBoxLayout()
        term_label = QLabel("SERVICE LOGS")
        term_label.setObjectName("cardTitle")
        term_header.addWidget(term_label)
        term_header.addStretch()
        
        self.copy_logs_btn = QPushButton("Copy Logs")
        self.copy_logs_btn.setObjectName("actionBtn")
        self.copy_logs_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_logs_btn.clicked.connect(self._copy_logs)
        self.copy_logs_btn.setFixedSize(100, 28)
        term_header.addWidget(self.copy_logs_btn)
        
        layout.addLayout(term_header)

        # Terminal
        self.terminal = Terminal()
        self.terminal.setMinimumHeight(220)
        layout.addWidget(self.terminal, 1)

        return page


    def _create_clawdhub_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 20, 24, 20)  # Reduced from 36
        layout.setSpacing(12)  # Reduced from 20

        header = QLabel("ClawdHub")
        header.setObjectName("sectionTitle")
        layout.addWidget(header)

        desc = QLabel("Install plugins and extensions for ClawdBot.")
        desc.setObjectName("sectionDesc")
        layout.addWidget(desc)

        # Install/Update Card
        install_card = QFrame()
        install_card.setObjectName("card")
        install_layout = QVBoxLayout(install_card)
        install_layout.setContentsMargins(16, 12, 16, 12)  # Reduced from 20, 16
        install_layout.setSpacing(10)  # Reduced from 12

        install_header = QHBoxLayout()
        install_title = QLabel("ClawdHub CLI")
        install_title.setStyleSheet("background: transparent; font-weight: 600; font-size: 14px; color: #ffffff;")
        install_header.addWidget(install_title)
        install_header.addStretch()
        
        self.clawdhub_status = QLabel("Checking...")
        self.clawdhub_status.setStyleSheet("background: transparent; color: #8b949e; font-size: 12px;")
        install_header.addWidget(self.clawdhub_status)
        install_layout.addLayout(install_header)

        install_desc = QLabel("Install plugins like Spotify, YouTube, etc.")
        install_desc.setStyleSheet("background: transparent; color: #8b949e; font-size: 12px;")
        install_layout.addWidget(install_desc)

        # Buttons row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        
        self.clawdhub_install_btn = QPushButton("Install")
        self.clawdhub_install_btn.setObjectName("successBtn")
        self.clawdhub_install_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clawdhub_install_btn.clicked.connect(self._on_install_clawdhub)
        btn_row.addWidget(self.clawdhub_install_btn)
        
        self.clawdhub_update_btn = QPushButton("Update")
        self.clawdhub_update_btn.setObjectName("actionBtn")
        self.clawdhub_update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clawdhub_update_btn.clicked.connect(self._on_update_clawdhub)
        self.clawdhub_update_btn.setVisible(False)
        self.clawdhub_update_btn.setFixedWidth(100)
        btn_row.addWidget(self.clawdhub_update_btn)
        
        self.clawdhub_uninstall_btn = QPushButton("Uninstall")
        self.clawdhub_uninstall_btn.setObjectName("dangerBtn")
        self.clawdhub_uninstall_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clawdhub_uninstall_btn.clicked.connect(self._on_uninstall_clawdhub)
        self.clawdhub_uninstall_btn.setVisible(False)
        self.clawdhub_uninstall_btn.setFixedWidth(100)
        btn_row.addWidget(self.clawdhub_uninstall_btn)
        
        btn_row.addStretch()
        install_layout.addLayout(btn_row)

        layout.addWidget(install_card)

        # Skills Management Card
        skills_card = QFrame()
        skills_card.setObjectName("card")
        skills_layout = QVBoxLayout(skills_card)
        skills_layout.setContentsMargins(16, 12, 16, 12)  # Reduced
        skills_layout.setSpacing(10)  # Reduced

        skills_header = QHBoxLayout()
        skills_title = QLabel("Skills Management")
        skills_title.setStyleSheet("background: transparent; font-weight: 600; font-size: 14px; color: #ffffff;")
        skills_header.addWidget(skills_title)
        skills_header.addStretch()
        
        # Skills count label
        from src.utils.platform import count_skills
        skill_count = count_skills()
        self.skills_count_label = QLabel(f"{skill_count} skills installed")
        self.skills_count_label.setStyleSheet("background: transparent; color: #8b949e; font-size: 12px;")
        skills_header.addWidget(self.skills_count_label)
        skills_layout.addLayout(skills_header)

        from src.utils.platform import get_skills_folder_path
        skills_path = get_skills_folder_path()
        skills_desc = QLabel(f"Manage skills manually in: {skills_path}")
        skills_desc.setStyleSheet("background: transparent; color: #8b949e; font-size: 11px;")
        skills_layout.addWidget(skills_desc)

        # Open folder button
        open_folder_btn = QPushButton("Open Skills Folder")
        open_folder_btn.setObjectName("actionBtn")
        open_folder_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        open_folder_btn.clicked.connect(self._on_open_skills_folder)
        open_folder_btn.setFixedWidth(140)
        skills_layout.addWidget(open_folder_btn)

        layout.addWidget(skills_card)

        # Command Card
        cmd_card = QFrame()
        cmd_card.setObjectName("card")
        cmd_layout = QVBoxLayout(cmd_card)
        cmd_layout.setContentsMargins(16, 12, 16, 12)  # Reduced
        cmd_layout.setSpacing(10)  # Reduced

        cmd_title = QLabel("Install Skills")
        cmd_title.setStyleSheet("background: transparent; font-weight: 600; font-size: 14px; color: #ffffff;")
        cmd_layout.addWidget(cmd_title)

        cmd_desc = QLabel("Enter skill path to install (e.g., spotify, self-improving-agent) - clawdhub install spotify")
        cmd_desc.setStyleSheet("background: transparent; color: #8b949e; font-size: 12px;")
        cmd_layout.addWidget(cmd_desc)

        # Command input row
        cmd_row = QHBoxLayout()
        cmd_row.setSpacing(10)

        from PyQt6.QtWidgets import QLineEdit
        self.clawdhub_input = QLineEdit()
        self.clawdhub_input.setPlaceholderText("spotify or self-improving-agent")
        self.clawdhub_input.setStyleSheet("""
            QLineEdit {
                background-color: #0d1117;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 10px 14px;
                color: #e6edf3;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #58a6ff;
            }
        """)
        self.clawdhub_input.returnPressed.connect(self._on_run_clawdhub_cmd)
        cmd_row.addWidget(self.clawdhub_input)

        run_btn = QPushButton("Install")
        run_btn.setObjectName("actionBtn")
        run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        run_btn.clicked.connect(self._on_run_clawdhub_cmd)
        run_btn.setFixedSize(80, 36)
        cmd_row.addWidget(run_btn)

        cmd_layout.addLayout(cmd_row)
        layout.addWidget(cmd_card)

        # Terminal Header
        term_header = QHBoxLayout()
        term_label = QLabel("CLAWDHUB LOGS")
        term_label.setObjectName("cardTitle")
        term_header.addWidget(term_label)
        term_header.addStretch()

        copy_btn = QPushButton("Copy Logs")
        copy_btn.setObjectName("actionBtn")
        copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        copy_btn.clicked.connect(self._copy_clawdhub_logs)
        copy_btn.setFixedSize(100, 28)
        term_header.addWidget(copy_btn)
        self.clawdhub_copy_btn = copy_btn

        layout.addLayout(term_header)

        # Terminal
        self.clawdhub_terminal = Terminal()
        self.clawdhub_terminal.setMinimumHeight(150)  # Reduced from 200
        layout.addWidget(self.clawdhub_terminal, 1)

        # Check ClawdHub install status after UI is ready
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(500, self._check_clawdhub)

        return page

    def _create_terminal_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(36, 36, 36, 36)
        layout.setSpacing(20)

        # Header
        header = QLabel("Terminal")
        header.setObjectName("sectionTitle")
        layout.addWidget(header)

        desc = QLabel("Execute ClawdBot commands with admin privileges.")
        desc.setObjectName("sectionDesc")
        layout.addWidget(desc)

        # Command Input Card
        cmd_card = QFrame()
        cmd_card.setObjectName("card")
        cmd_layout = QVBoxLayout(cmd_card)
        cmd_layout.setContentsMargins(20, 16, 20, 16)
        cmd_layout.setSpacing(12)

        cmd_title = QLabel("Run Command")
        cmd_title.setStyleSheet("background: transparent; font-weight: 600; font-size: 14px; color: #ffffff;")
        cmd_layout.addWidget(cmd_title)

        cmd_desc = QLabel("Enter any command to execute with admin privileges (e.g., clawdbot configure, python --version)")
        cmd_desc.setStyleSheet("background: transparent; color: #8b949e; font-size: 12px;")
        cmd_layout.addWidget(cmd_desc)

        # Command input row
        cmd_row = QHBoxLayout()
        cmd_row.setSpacing(10)

        from PyQt6.QtWidgets import QLineEdit
        self.terminal_input = QLineEdit()
        self.terminal_input.setPlaceholderText("clawdbot configure or npm --version")
        self.terminal_input.setStyleSheet("""
            QLineEdit {
                background-color: #0d1117;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 10px 14px;
                color: #e6edf3;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #58a6ff;
            }
        """)
        self.terminal_input.returnPressed.connect(self._on_execute_terminal_cmd)
        cmd_row.addWidget(self.terminal_input)

        execute_btn = QPushButton("Execute")
        execute_btn.setObjectName("actionBtn")
        execute_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        execute_btn.clicked.connect(self._on_execute_terminal_cmd)
        execute_btn.setFixedSize(90, 36)
        cmd_row.addWidget(execute_btn)

        cmd_layout.addLayout(cmd_row)
        layout.addWidget(cmd_card)

        # Terminal Output Header
        term_header = QHBoxLayout()
        term_label = QLabel("TERMINAL OUTPUT")
        term_label.setObjectName("cardTitle")
        term_header.addWidget(term_label)
        term_header.addStretch()

        copy_btn = QPushButton("Copy Logs")
        copy_btn.setObjectName("actionBtn")
        copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        copy_btn.clicked.connect(self._copy_terminal_logs)
        copy_btn.setFixedSize(100, 28)
        term_header.addWidget(copy_btn)

        clear_btn = QPushButton("Clear Logs")
        clear_btn.setObjectName("actionBtn")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.clicked.connect(self._clear_terminal_logs)
        clear_btn.setFixedSize(100, 28)
        term_header.addWidget(clear_btn)

        layout.addLayout(term_header)

        # Terminal Output
        self.cmd_terminal = Terminal()
        self.cmd_terminal.setMinimumHeight(300)
        layout.addWidget(self.cmd_terminal, 1)

        return page

    def _create_settings_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(36, 36, 36, 36)
        layout.setSpacing(20)

        header = QLabel("Settings")
        header.setObjectName("sectionTitle")
        layout.addWidget(header)

        desc = QLabel("Application preferences and information.")
        desc.setObjectName("sectionDesc")
        layout.addWidget(desc)

        # About Card
        about_card = QFrame()
        about_card.setObjectName("card")
        about_layout = QVBoxLayout(about_card)
        about_layout.setContentsMargins(20, 16, 20, 16)
        about_layout.setSpacing(12)

        about_title = QLabel("About ClawdBot")
        about_title.setStyleSheet("background: transparent; font-weight: 600; font-size: 14px; color: #ffffff;")
        about_layout.addWidget(about_title)

        # Version info (will be updated)
        self.settings_version = QLabel("Version: Checking...")
        self.settings_version.setStyleSheet("background: transparent; color: #8b949e; font-size: 13px;")
        about_layout.addWidget(self.settings_version)

        self.settings_latest = QLabel("Latest: Checking...")
        self.settings_latest.setStyleSheet("background: transparent; color: #8b949e; font-size: 13px;")
        about_layout.addWidget(self.settings_latest)

        self.settings_gateway = QLabel("Gateway: Checking...")
        self.settings_gateway.setStyleSheet("background: transparent; color: #8b949e; font-size: 13px;")
        about_layout.addWidget(self.settings_gateway)

        layout.addWidget(about_card)

        # Maintenance Card
        maint_card = QFrame()
        maint_card.setObjectName("card")
        maint_layout = QVBoxLayout(maint_card)
        maint_layout.setContentsMargins(20, 16, 20, 16)
        maint_layout.setSpacing(12)

        maint_title = QLabel("Maintenance")
        maint_title.setStyleSheet("background: transparent; font-weight: 600; font-size: 14px; color: #ffffff;")
        maint_layout.addWidget(maint_title)

        maint_desc = QLabel("Update, reset, or uninstall ClawdBot.")
        maint_desc.setStyleSheet("background: transparent; color: #8b949e; font-size: 12px;")
        maint_layout.addWidget(maint_desc)

        maint_btn_row = QHBoxLayout()
        maint_btn_row.setSpacing(10)

        self.settings_update_btn = QPushButton("Check for Updates")
        self.settings_update_btn.setObjectName("actionBtn")
        self.settings_update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_update_btn.clicked.connect(self._on_update)
        maint_btn_row.addWidget(self.settings_update_btn)

        self.settings_reset_btn = QPushButton("Reset")
        self.settings_reset_btn.setObjectName("actionBtn")
        self.settings_reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_reset_btn.clicked.connect(self._on_reset)
        self.settings_reset_btn.setFixedWidth(80)
        maint_btn_row.addWidget(self.settings_reset_btn)

        self.settings_uninstall_btn = QPushButton("Uninstall")
        self.settings_uninstall_btn.setObjectName("dangerBtn")
        self.settings_uninstall_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_uninstall_btn.clicked.connect(self._on_uninstall)
        self.settings_uninstall_btn.setFixedWidth(100)
        maint_btn_row.addWidget(self.settings_uninstall_btn)

        maint_btn_row.addStretch()
        maint_layout.addLayout(maint_btn_row)

        layout.addWidget(maint_card)
        layout.addStretch()
        return page
    
    def _show_loading_overlay(self):
        """Show loading overlay to block interaction during initialization"""
        self.loading_overlay = LoadingOverlay(self.centralWidget())
        self.loading_overlay.show()
        self.loading_overlay.raise_()

    def _check_version(self):
        self.status_label.setText("Checking...")
        self.terminal.log("⋯ Checking ClawdBot installation...")

        self.version_checker = VersionChecker()
        self.version_checker.finished.connect(self._on_version_checked)
        self.version_checker.start()

    def _on_version_checked(self, status: dict):
        # Hide loading overlay - initialization complete
        if self.loading_overlay:
            self.loading_overlay.hide()
            self.loading_overlay.deleteLater()
            self.loading_overlay = None
        
        self.version_status = status

        if not status["is_installed"]:
            self.status_label.setText("Not installed")
            self.indicator.setText("● Not Installed")
            self.indicator.setStyleSheet(
                """
                color: #fbbf24;
                font-weight: 600;
                font-size: 12px;
                background-color: rgba(251, 191, 36, 0.12);
                padding: 5px 12px;
                border-radius: 4px;
            """
            )
            self.install_btn.setVisible(True)
            self.start_btn.setVisible(False)
            self.stop_btn.setVisible(False)
            self.update_btn.setVisible(False)
            self.uninstall_btn.setVisible(False)
            self.terminal.log("✗ ClawdBot is not installed")
            self.terminal.log("  Click 'Install ClawdBot' to install.")
            self.terminal.log("━" * 60)
            # Update settings page
            self.settings_version.setText("Version: Not installed")
            self.settings_latest.setText(f"Latest: {status.get('latest', 'Unknown')}")
            self.settings_gateway.setText("Gateway: Not available")
            
            # Disable maintenance buttons in settings
            if hasattr(self, 'settings_update_btn'):
                self.settings_update_btn.setEnabled(False)
            if hasattr(self, 'settings_reset_btn'):
                self.settings_reset_btn.setEnabled(False)
            if hasattr(self, 'settings_uninstall_btn'):
                self.settings_uninstall_btn.setEnabled(False)
        else:
            version = status["installed"]
            self.header_version.setText(f"v{version}")
            self.install_btn.setVisible(False)
            self.start_btn.setVisible(True)
            
            # Update settings page
            self.settings_version.setText(f"Version: v{version}")
            
            # Enable maintenance buttons in settings
            if hasattr(self, 'settings_update_btn'):
                self.settings_update_btn.setEnabled(True)
            if hasattr(self, 'settings_reset_btn'):
                self.settings_reset_btn.setEnabled(True)
            if hasattr(self, 'settings_uninstall_btn'):
                self.settings_uninstall_btn.setEnabled(True)
            self.settings_latest.setText(f"Latest: v{status.get('latest', version)}")
            gateway = status.get("gateway", {})
            if gateway.get("running"):
                port = gateway.get('port', 18789)
                self.settings_gateway.setText(f"Gateway: Running on port {port}")
            else:
                self.settings_gateway.setText("Gateway: Stopped")

            gateway = status.get("gateway", {})
            if gateway.get("running"):
                pid = gateway.get('pid', '')
                port = gateway.get('port', 18789)
                pid_text = f" (PID: {pid})" if pid else ""
                self.status_label.setText(f"Running on port {port}{pid_text}")
                self.indicator.setText("● Running")
                self.indicator.setStyleSheet(
                    """
                    color: #4ade80;
                    font-weight: 600;
                    font-size: 12px;
                    background-color: rgba(34, 197, 94, 0.15);
                    padding: 5px 12px;
                    border-radius: 4px;
                """
                )
                self.start_btn.setEnabled(False)
                self.start_btn.setText("Running")
                self.stop_btn.setEnabled(True)
                self.quick_stop_btn.setVisible(True)
                self.open_btn.setVisible(True)
                self.open_ui_btn.setVisible(True)
                self.terminal.log(f"✓ ClawdBot installed (v{version})")
                self.terminal.log(f"✓ Gateway running on ws://127.0.0.1:{port}{pid_text}")
                self.terminal.log("ℹ Live logs only appear when you start the gateway from this UI")
                self.terminal.log("  To see logs, stop the gateway and restart it using 'Start Service'")
                self.terminal.log("━" * 60)
            else:
                self.status_label.setText("Gateway Stopped")
                self.indicator.setText("● Stopped")
                self.start_btn.setEnabled(True)
                self.start_btn.setText("Start Service")
                self.stop_btn.setEnabled(False)
                self.quick_stop_btn.setVisible(False)
                self.open_btn.setVisible(False)
                self.open_ui_btn.setVisible(False)
                self.indicator.setStyleSheet(
                    """
                    color: #7d8590;
                    font-weight: 600;
                    font-size: 12px;
                    background-color: #21262d;
                    padding: 5px 12px;
                    border-radius: 4px;
                """
                )
                self.start_btn.setEnabled(True)
                self.start_btn.setText("Start Service")
                self.stop_btn.setEnabled(False)
                self.quick_stop_btn.setVisible(False)
                self.open_btn.setVisible(False)
                self.open_ui_btn.setVisible(False)  # Only show when gateway is running
                self.terminal.log(f"✓ ClawdBot installed (v{version})")
                self.terminal.log("○ Gateway stopped - click 'Start Service' to run")
                self.terminal.log("━" * 60)

                # Show upgrade button if update available
                if status["update_available"]:
                    latest = status["latest"]
                    self.update_btn.setVisible(True)
                    self.update_btn.setText(f"Upgrade to v{latest}")
                    self.terminal.log(f"Update available: v{latest}")
                else:
                    self.update_btn.setVisible(False)
                
                # Show uninstall button when installed
                self.uninstall_btn.setVisible(True)

    def _on_start(self):
        self.terminal.log("Starting gateway...")
        self.start_btn.setEnabled(False)
        self.indicator.setText("● Starting...")
        self.indicator.setStyleSheet(
            """
            color: #fbbf24;
            font-weight: 600;
            font-size: 12px;
            background-color: rgba(251, 191, 36, 0.12);
            padding: 5px 12px;
            border-radius: 4px;
        """
        )

        self.gateway_runner = ProcessRunner(get_gateway_command())
        self.gateway_runner.output.connect(self.terminal.log)
        self.gateway_runner.error.connect(lambda e: self.terminal.log(f"Error: {e}"))
        self.gateway_runner.started.connect(self._on_gateway_started)
        self.gateway_runner.finished.connect(self._on_gateway_stopped)
        self.gateway_runner.start()

    def _on_gateway_started(self):
        self.status_label.setText("Gateway Running")
        self.indicator.setText("● Running")
        self.indicator.setStyleSheet(
            """
            color: #4ade80;
            font-weight: 600;
            font-size: 12px;
            background-color: rgba(34, 197, 94, 0.15);
            padding: 5px 12px;
            border-radius: 4px;
        """
        )
        self.stop_btn.setEnabled(True)
        self.quick_stop_btn.setVisible(True)
        self.open_btn.setVisible(True)
        self.terminal.log("✓ Gateway started on ws://127.0.0.1:18789")
        self.terminal.log("━" * 60)

    def _on_stop(self):
        self.terminal.log("⋯ Stopping gateway...")
        self.stop_btn.setEnabled(False)
        self.quick_stop_btn.setEnabled(False)
        
        # If we have a local runner, stop it
        if self.gateway_runner:
            self.gateway_runner.stop()
        
        # Run clawdbot gateway stop command
        cmd = (
            ["clawdbot", "gateway", "stop"]
            if not is_windows()
            else ["powershell", "-Command", "clawdbot gateway stop"]
        )
        runner = ProcessRunner(cmd)
        runner.output.connect(self.terminal.log)
        runner.finished.connect(self._on_stop_finished)
        runner.start()
    
    def _on_stop_finished(self, exit_code):
        self.terminal.log("✓ Gateway stopped" if exit_code == 0 else f"Stop completed (code: {exit_code})")
        self.terminal.log("━" * 60)
        self._check_version()

    def _on_gateway_stopped(self, exit_code: int):
        # Recheck actual gateway status - it might still be running (e.g., was already running)
        self.terminal.log(f"Process exited (code: {exit_code})")
        self.terminal.log("━" * 60)
        self.gateway_runner = None
        
        # Recheck version/status to get accurate state
        self._check_version()

    def _on_install(self):
        self.terminal.log("Installing ClawdBot...")
        self.install_btn.setEnabled(False)
        runner = ProcessRunner(get_install_command(), shell=True)
        runner.output.connect(self.terminal.log)
        runner.finished.connect(lambda c: (self.terminal.log("━" * 60), self._check_version()))
        runner.start()

    def _on_update(self):
        cmd = (
            ["clawdbot", "update"]
            if not is_windows()
            else ["powershell", "-Command", "clawdbot update"]
        )
        dialog = CommandDialog(self, "Updating ClawdBot")
        dialog.run_command(cmd)
        dialog.exec()
        self._check_version()

    def _on_uninstall(self):
        cmd = (
            ["clawdbot", "uninstall", "--all", "--yes"]
            if not is_windows()
            else ["powershell", "-Command", "clawdbot uninstall --all --yes"]
        )
        dialog = CommandDialog(self, "Uninstalling ClawdBot")
        dialog.run_command(cmd)
        dialog.exec()
        self._check_version()

    def _on_reset(self):
        cmd = (
            ["clawdbot", "reset", "--yes"]
            if not is_windows()
            else ["powershell", "-Command", "clawdbot reset --yes"]
        )
        dialog = CommandDialog(self, "Resetting ClawdBot")
        dialog.run_command(cmd)
        dialog.exec()
        self._check_version()

    def _on_open_gateway(self):
        import webbrowser
        port = 18789
        if self.version_status and self.version_status.get("gateway"):
            port = self.version_status["gateway"].get("port", 18789)
        url = f"http://127.0.0.1:{port}"
        webbrowser.open(url)
        self.terminal.log(f"Opening gateway: {url}")

    def _on_open_ui(self):
        # Run clawdbot dashboard - it opens the UI automatically
        import subprocess
        
        self.terminal.log("Opening dashboard UI...")
        try:
            cmd = "clawdbot dashboard"
            result = subprocess.run(
                cmd, shell=True,
                capture_output=True, text=True, timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW if is_windows() else 0
            )
            
            if result.returncode == 0:
                self.terminal.log("✓ Dashboard UI opened in browser")
            else:
                self.terminal.log(f"✗ Failed to open dashboard (code: {result.returncode})")
                if result.stderr:
                    self.terminal.log(result.stderr)
        except Exception as e:
            self.terminal.log(f"✗ Error opening UI: {e}")

    def _copy_logs(self):
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QTimer
        QApplication.clipboard().setText(self.terminal.toPlainText())
        self.copy_logs_btn.setText("Copied!")
        self.terminal.log("✓ Logs copied to clipboard")
        # Revert text after 2 seconds
        QTimer.singleShot(2000, lambda: self.copy_logs_btn.setText("Copy Logs"))

    def _on_install_clawdhub(self):
        self.clawdhub_terminal.log("⋯ Installing ClawdHub...")
        self.clawdhub_install_btn.setEnabled(False)
        cmd = "npm install -g clawdhub undici"
        self.clawdhub_runner = ProcessRunner(cmd, shell=True)
        self.clawdhub_runner.output.connect(self.clawdhub_terminal.log)
        self.clawdhub_runner.finished.connect(self._on_clawdhub_installed)
        self.clawdhub_runner.start()

    def _on_clawdhub_installed(self, exit_code):
        if exit_code == 0:
            self.clawdhub_terminal.log("✓ ClawdHub installed successfully!")
            self._check_clawdhub()
        else:
            self.clawdhub_terminal.log(f"✗ Installation failed (code: {exit_code})")
            self.clawdhub_install_btn.setEnabled(True)

    def _on_update_clawdhub(self):
        self.clawdhub_terminal.log("⋯ Updating ClawdHub...")
        self.clawdhub_update_btn.setEnabled(False)
        cmd = "npm update -g clawdhub undici"
        self.clawdhub_runner = ProcessRunner(cmd, shell=True)
        self.clawdhub_runner.output.connect(self.clawdhub_terminal.log)
        self.clawdhub_runner.finished.connect(self._on_clawdhub_updated)
        self.clawdhub_runner.start()

    def _on_clawdhub_updated(self, exit_code):
        if exit_code == 0:
            self.clawdhub_terminal.log("✓ ClawdHub updated!")
        else:
            self.clawdhub_terminal.log(f"✗ Update failed (code: {exit_code})")
        self.clawdhub_update_btn.setEnabled(True)
        self._check_clawdhub()

    def _on_uninstall_clawdhub(self):
        self.clawdhub_terminal.log("⋯ Uninstalling ClawdHub...")
        self.clawdhub_uninstall_btn.setEnabled(False)
        cmd = "npm uninstall -g clawdhub"
        self.clawdhub_runner = ProcessRunner(cmd, shell=True)
        self.clawdhub_runner.output.connect(self.clawdhub_terminal.log)
        self.clawdhub_runner.finished.connect(self._on_clawdhub_uninstalled)
        self.clawdhub_runner.start()

    def _on_clawdhub_uninstalled(self, exit_code):
        if exit_code == 0:
            self.clawdhub_terminal.log("✓ ClawdHub uninstalled!")
        else:
            self.clawdhub_terminal.log(f"✗ Uninstall failed (code: {exit_code})")
        self._check_clawdhub()

    def _check_clawdhub(self):
        # Check if clawdhub is installed
        import subprocess
        try:
            # Method 1: Check binary
            cmd = "clawdhub --version"
            result = subprocess.run(
                cmd, shell=True,
                capture_output=True, text=True, timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW if is_windows() else 0
            )
            
            fullname = ""
            if result.returncode == 0:
                fullname = result.stdout.strip()
            
            # Method 2: Check npm global list (fallback if binary not in PATH)
            if not fullname:
                cmd = "npm list -g clawdhub --depth=0"
                result = subprocess.run(
                    cmd, shell=True,
                    capture_output=True, text=True, timeout=8,
                    creationflags=subprocess.CREATE_NO_WINDOW if is_windows() else 0
                )
                if "clawdhub@" in result.stdout:
                    # Extract version from npm output
                    import re
                    match = re.search(r'clawdhub@([\d\.]+)', result.stdout)
                    if match:
                        fullname = match.group(1)
                    else:
                        fullname = "Installed"

            if fullname:
                # Clean version string
                version = fullname.replace("clawdhub/", "").replace("v", "")
                self.clawdhub_status.setText(f"Installed (v{version})")
                self.clawdhub_install_btn.setVisible(False)
                self.clawdhub_update_btn.setVisible(True)
                self.clawdhub_update_btn.setEnabled(True)
                self.clawdhub_uninstall_btn.setVisible(True)
                self.clawdhub_uninstall_btn.setEnabled(True)
            else:
                self._set_clawdhub_not_installed()
        except Exception as e:
            self.clawdhub_terminal.log(f"Check error: {e}")
            self._set_clawdhub_not_installed()

    def _set_clawdhub_not_installed(self):
        self.clawdhub_status.setText("Not installed")
        self.clawdhub_install_btn.setVisible(True)
        self.clawdhub_install_btn.setEnabled(True)
        self.clawdhub_update_btn.setVisible(False)
        self.clawdhub_uninstall_btn.setVisible(False)

    def _on_run_clawdhub_cmd(self):
        plugin_name = self.clawdhub_input.text().strip()
        if not plugin_name:
            return
        
        # Auto-prepend 'clawdhub install' to the plugin name
        cmd = f"clawdhub install {plugin_name}"
        self.clawdhub_terminal.log(f"$ {cmd}")
        self.clawdhub_input.clear()
        
        self.clawdhub_runner = ProcessRunner(cmd, shell=True)
        self.clawdhub_runner.output.connect(self.clawdhub_terminal.log)
        self.clawdhub_runner.finished.connect(self._on_clawdhub_cmd_finished)
        self.clawdhub_runner.start()
    
    def _on_clawdhub_cmd_finished(self, exit_code):
        # Log result and refresh skill count
        if exit_code == 0:
            self.clawdhub_terminal.log("✓ Done")
            # Refresh skill count after successful installation
            from src.utils.platform import count_skills
            skill_count = count_skills()
            self.skills_count_label.setText(f"{skill_count} skills installed")
        else:
            self.clawdhub_terminal.log(f"✗ Failed (exit: {exit_code})")


    def _copy_clawdhub_logs(self):
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QTimer
        QApplication.clipboard().setText(self.clawdhub_terminal.toPlainText())
        self.clawdhub_copy_btn.setText("Copied!")
        self.clawdhub_terminal.log("✓ Logs copied to clipboard")
        QTimer.singleShot(2000, lambda: self.clawdhub_copy_btn.setText("Copy Logs"))
    
    def _on_open_skills_folder(self):
        # Open skills folder in File Explorer and refresh count
        from src.utils.platform import open_skills_folder, count_skills
        open_skills_folder()
        self.clawdhub_terminal.log("✓ Skills folder opened")
        
        # Refresh skill count
        skill_count = count_skills()
        self.skills_count_label.setText(f"{skill_count} skills installed")
    
    def _on_execute_terminal_cmd(self):
        # Get command exactly as typed
        cmd = self.terminal_input.text().strip()
        if not cmd:
            return
        
        # Run command directly without modification
        self.cmd_terminal.log(f"$ {cmd}")
        self.cmd_terminal.log("⋯ Executing with admin privileges...")
        self.terminal_input.clear()
        
        # Run with admin privileges
        self.terminal_runner = ProcessRunner(cmd, shell=True, admin=True)
        self.terminal_runner.output.connect(self.cmd_terminal.log)
        self.terminal_runner.error.connect(lambda e: self.cmd_terminal.log(f"❌ Error: {e}"))
        self.terminal_runner.finished.connect(self._on_terminal_cmd_finished)
        self.terminal_runner.start()
    
    def _on_terminal_cmd_finished(self, exit_code):
        # Log completion status
        if exit_code == 0:
            self.cmd_terminal.log("✓ Command completed successfully")
        else:
            self.cmd_terminal.log(f"✗ Command failed (exit code: {exit_code})")
        self.cmd_terminal.log("━" * 60)
    
    def _open_url(self, url: str):
        # Open URL in default browser
        import webbrowser
        webbrowser.open(url)
    
    def _copy_terminal_logs(self):
        # Copy terminal output to clipboard
        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText(self.cmd_terminal.toPlainText())
        self.cmd_terminal.log("✓ Logs copied to clipboard")
    
    def _clear_terminal_logs(self):
        # Clear terminal output
        self.cmd_terminal.clear()
        self.cmd_terminal.log("Terminal cleared")

    def closeEvent(self, event):
        # Stop any gateway process started by this app
        if self.gateway_runner:
            self.gateway_runner.stop()
            self.gateway_runner.wait(3000)
        
        # Stop ClawdHub runner if running
        if hasattr(self, 'clawdhub_runner') and self.clawdhub_runner:
            if self.clawdhub_runner.isRunning():
                self.clawdhub_runner.terminate()
                self.clawdhub_runner.wait(2000)
        
        # Stop Terminal runner if running  
        if hasattr(self, 'terminal_runner') and self.terminal_runner:
            if self.terminal_runner.isRunning():
                self.terminal_runner.terminate()
                self.terminal_runner.wait(2000)
        
        # Stop version checker if running
        if hasattr(self, 'version_checker') and self.version_checker:
            if self.version_checker.isRunning():
                self.version_checker.terminate()
                self.version_checker.wait(1000)
        
        # Also stop any background gateway service
        try:
            import subprocess
            import sys
            if sys.platform == "win32":
                subprocess.run(
                    ["powershell", "-NoProfile", "-Command", "clawdbot gateway stop"],
                    capture_output=True,
                    timeout=5,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                subprocess.run(["clawdbot", "gateway", "stop"], capture_output=True, timeout=5)
        except Exception:
            pass  # Ignore errors during cleanup
        
        event.accept()

