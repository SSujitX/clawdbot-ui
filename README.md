# ClawdBot Control Panel

A sleek desktop application for managing your ClawdBot AI gateway, skills, and commands. Built with PyQt6 for Windows and macOS.

![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-Desktop_App-green?logo=qt&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 🎛️ Gateway Control
- **Start/Stop Service** - One-click gateway management
- **Real-time Logs** - Live streaming of gateway output
- **Status Monitoring** - Visual indicators (Running/Stopped/Not Installed)
- **Open Gateway** - Quick access to `http://127.0.0.1:18789`
- **Open Dashboard** - Launch web UI with authentication token

### 📦 ClawdHub Skills Manager
- **Install Skills** - Humanizer, self-improving-agent, and more
- **Skills Management** - View and manage installed skills
- **Open Skills Folder** - Direct access to skills directory
- **Update/Uninstall** - Full lifecycle management

### 💻 Admin Terminal
- **Run Any Command** - Execute with admin privileges
- **PowerShell Integration** - UAC elevation on Windows
- **Real-time Output** - Live command streaming
- **Copy/Clear Logs** - Easy log management

### ⚙️ Settings & Maintenance
- **Version Info** - Current and latest version display
- **Check Updates** - One-click update checking
- **Reset/Uninstall** - Maintenance operations

### 🎨 Modern UI
- **Dark Theme** - Easy on the eyes
- **Sidebar Navigation** - Dashboard, ClawdHub, Terminal, Settings
- **Quick Links** - Skills Hub & Documentation
- **Responsive Design** - Polished, professional look

## 📋 Requirements

- Python 3.13 or higher
- Windows 10/11 or macOS
- [ClawdBot](https://clawd.bot) installed (for full functionality)

## 🚀 Installation

### Using UV (Recommended)

```bash
# Clone the repository
git clone https://github.com/SSujitX/clawdbot-ui.git
cd clawdbot-ui

# Install dependencies and run
uv sync
uv run main.py
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/SSujitX/clawdbot-ui.git
cd clawdbot-ui

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 📖 Usage

### Starting the Gateway

1. Launch the application
2. Navigate to **Dashboard**
3. Click **Start Service**
4. View live logs in the terminal panel

### Installing Skills

1. Navigate to **ClawdHub**
2. Enter skill name (e.g., `humanizer`)
3. Click **Install**
4. Monitor progress in the log panel

### Running Admin Commands

1. Navigate to **Terminal**
2. Enter your command (e.g., `clawdbot configure`)
3. Click **Execute**
4. Approve UAC prompt if required (Windows)

## 🔗 Quick Links

- [ClawdHub Skills](https://clawdhub.com/skills) - Browse available skills
- [Documentation](https://docs.clawd.bot/) - Official ClawdBot docs

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| UI Framework | PyQt6 |
| Package Manager | UV |
| Language | Python 3.13+ |
| Styling | Custom Dark Theme CSS |
| Process Management | QThread + subprocess |

## 📁 Project Structure

```
clawdbot-ui/
├── main.py                 # Entry point
├── pyproject.toml          # Project configuration
├── src/
│   ├── app.py              # Application setup
│   ├── ui/
│   │   ├── window.py       # Main window (4 pages)
│   │   ├── terminal.py     # Log viewer widget
│   │   ├── command_dialog.py # Modal command runner
│   │   └── styles.py       # Dark theme CSS
│   ├── core/
│   │   ├── process.py      # Background process runner
│   │   └── version.py      # Version checking
│   └── utils/
│       └── platform.py     # Platform detection + skills utilities
└── .agent/skills/          # Development skills
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [ClawdBot](https://clawd.bot) - The AI gateway this UI controls
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - Python bindings for Qt
- [UV](https://github.com/astral-sh/uv) - Fast Python package manager

---

<p align="center">
  <b>Made with ❤️ for developers who take control</b>
</p>

<p align="center">
  <a href="https://www.star-history.com/#SSujitX/clawdbot-ui&Date">
    <img src="https://api.star-history.com/svg?repos=SSujitX/clawdbot-ui&type=Date" width="500" alt="Star History">
  </a>
</p>

<p align="center">
  <img src="https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2FSSujitX%2Fclawdbot-ui&countColor=%23263759" alt="Visitors">
</p>

---

<p align="center">
  Made with ❤️ for the ClawdBot community
</p>

