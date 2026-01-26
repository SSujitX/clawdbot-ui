# Version checking utilities for ClawdBot

import re
import os
import json
import subprocess
import sys
from urllib.request import urlopen
from urllib.error import URLError

GITHUB_API = "https://api.github.com/repos/clawdbot/clawdbot/releases/latest"


def _run_command(args: list[str], shell: bool = False) -> tuple[int, str, str]:
    # Run command and return (returncode, stdout, stderr)
    try:
        startupinfo = None
        creationflags = 0
        
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            creationflags = subprocess.CREATE_NO_WINDOW
        
        # On Windows, inherit PATH from user environment
        env = os.environ.copy()
        
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=8,  # Reduced timeout for faster startup
            shell=shell,
            startupinfo=startupinfo,
            creationflags=creationflags,
            env=env
        )
        
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return -1, "", str(e)


def get_installed_version() -> str | None:
    # Get installed ClawdBot version 
    if sys.platform == "win32":
        # Use cmd.exe which starts faster than PowerShell
        code, stdout, stderr = _run_command(
            "clawdbot --version", shell=True
        )
    else:
        code, stdout, stderr = _run_command(["clawdbot", "--version"])
    
    if code == 0 and stdout:
        # Clean any ANSI codes
        clean_output = re.sub(r'\x1b\[[0-9;]*m', '', stdout).strip()
        
        # Extract version - look for year-based version (2026.x.x) or semver
        # Match pattern: v2026.1.24-3 or 2026.1.24-3
        match = re.search(r'v?(\d{4}\.\d+\.\d+(?:-[\w\d]+)?)', clean_output)
        if match:
            return match.group(1)
            
        # Fallback to simple line split if regex fails but output looks simple
        lines = clean_output.split('\n')
        if lines:
            return lines[-1].strip()
            
        return clean_output
    return None


def get_gateway_status() -> dict:
    # Check if gateway is running
    if sys.platform == "win32":
        # Use shell for faster execution
        code, stdout, stderr = _run_command(
            "clawdbot gateway status --json", shell=True
        )
    else:
        code, stdout, stderr = _run_command(["clawdbot", "gateway", "status", "--json"])
    
    try:
        if stdout:
            # Try to parse JSON
            data = json.loads(stdout)
            if data.get("running"):
                return {
                    "running": True,
                    "pid": data.get("pid"),
                    "port": data.get("port", 18789),
                    "uptime": data.get("uptime")
                }
    except json.JSONDecodeError:
        pass
    
    # Try health check as fallback
    if sys.platform == "win32":
        code, stdout, stderr = _run_command(
            "clawdbot health --json", shell=True
        )
    else:
        code, stdout, stderr = _run_command(["clawdbot", "health", "--json"])
    
    if code == 0:
        return {"running": True, "port": 18789}
    
    # Final fallback: check if port 18789 is in use
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', 18789))
        sock.close()
        if result == 0:
            # Port is open, gateway is likely running
            return {"running": True, "port": 18789}
    except Exception:
        pass
    
    return {"running": False}


def get_latest_version() -> tuple[str | None, str | None]:
    # Get latest version from GitHub API
    # Returns (version, release_url)
    try:
        with urlopen(GITHUB_API, timeout=5) as response:
            data = json.loads(response.read().decode())
            tag = data.get("tag_name", "")
            version = tag.lstrip("v")
            url = data.get("html_url", "")
            return version, url
    except (URLError, json.JSONDecodeError, KeyError):
        return None, None


def parse_version(version: str) -> tuple[int, int, int, int]:
    # Parse version string like "2026.1.24-3" -> (2026, 1, 24, 3)
    match = re.match(r"(\d+)\.(\d+)\.(\d+)(?:-(\d+))?", version)
    if match:
        major = int(match.group(1))
        minor = int(match.group(2))
        patch = int(match.group(3))
        build = int(match.group(4)) if match.group(4) else 0
        return (major, minor, patch, build)
    return (0, 0, 0, 0)


def is_update_available(installed: str, latest: str) -> bool:
    # Compare versions to check if update is available
    installed_parts = parse_version(installed)
    latest_parts = parse_version(latest)
    
    # Compare major.minor.patch only (ignore build number)
    return latest_parts[:3] > installed_parts[:3]


def get_version_status() -> dict:
    # Get complete version status
    installed = get_installed_version()
    latest, release_url = get_latest_version()
    gateway = get_gateway_status()
    
    return {
        "installed": installed,
        "latest": latest,
        "release_url": release_url,
        "is_installed": installed is not None,
        "update_available": (
            is_update_available(installed, latest)
            if installed and latest else False
        ),
        "gateway": gateway
    }

