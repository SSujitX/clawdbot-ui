# Platform detection and shell command utilities

import sys
import shutil


def is_windows() -> bool:
    return sys.platform == "win32"


def is_mac() -> bool:
    return sys.platform == "darwin"


def is_linux() -> bool:
    return sys.platform.startswith("linux")


def get_shell_command(script: str) -> list[str]:
    # Get platform-appropriate shell command
    if is_windows():
        return ["powershell", "-Command", script]
    return ["bash", "-c", script]


def get_clawdbot_path() -> str | None:
    # Find clawdbot executable in PATH
    return shutil.which("clawdbot")


def is_clawdbot_installed() -> bool:
    # Check if clawdbot is available
    return get_clawdbot_path() is not None


def get_install_command() -> list[str]:
    # Get platform-specific install command
    if is_windows():
        return ["powershell", "-Command", 
                "iwr -useb https://clawd.bot/install.ps1 | iex"]
    return ["bash", "-c", 
            "curl -fsSL https://clawd.bot/install.sh | bash"]


def get_gateway_command(port: int = 18789) -> list[str]:
    # Get command to start gateway
    if is_windows():
        return ["powershell", "-Command", f"clawdbot gateway --port {port}"]
    return ["bash", "-c", f"clawdbot gateway --port {port}"]


def get_skills_folder_path() -> str:
    # Get the ClawdBot skills folder path based on current user
    import os
    home = os.path.expanduser("~")
    return os.path.join(home, "clawd", "skills")


def count_skills() -> int:
    # Count installed skills in the skills folder
    import os
    skills_path = get_skills_folder_path()
    
    if not os.path.exists(skills_path):
        return 0
    
    # Count directories (each skill is a folder)
    try:
        items = os.listdir(skills_path)
        return len([item for item in items if os.path.isdir(os.path.join(skills_path, item))])
    except Exception:
        return 0


def open_skills_folder():
    # Open skills folder in File Explorer/Finder
    import os
    import subprocess
    
    skills_path = get_skills_folder_path()
    
    # Create folder if it doesn't exist
    if not os.path.exists(skills_path):
        os.makedirs(skills_path, exist_ok=True)
    
    # Open folder based on platform
    if is_windows():
        subprocess.Popen(["explorer", skills_path])
    elif is_mac():
        subprocess.Popen(["open", skills_path])
    else:  # Linux
        subprocess.Popen(["xdg-open", skills_path])
