---
name: async-subprocess
description: Non-blocking subprocess execution with real-time output streaming
---

# Async Subprocess Patterns

## PyQt6 Thread-Based Runner

```python
from PyQt6.QtCore import QThread, pyqtSignal
import subprocess
import sys

class CommandRunner(QThread):
    """Non-blocking command runner with real-time output"""
    
    output_line = pyqtSignal(str)      # Each line of output
    error_line = pyqtSignal(str)       # Error output
    process_finished = pyqtSignal(int) # Exit code
    process_started = pyqtSignal()     # Process started
    
    def __init__(self, command: list[str], cwd: str = None, 
                 shell: bool = False, admin: bool = False):
        super().__init__()
        self.command = command
        self.cwd = cwd
        self.shell = shell
        self.admin = admin
        self.process = None
        self._stopped = False
    
    def run(self):
        try:
            cmd = self._prepare_command()
            
            # Windows: hide console window
            startupinfo = None
            creationflags = 0
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                creationflags = subprocess.CREATE_NO_WINDOW
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=self.shell,
                cwd=self.cwd,
                text=True,
                bufsize=1,  # Line buffered
                startupinfo=startupinfo,
                creationflags=creationflags
            )
            
            self.process_started.emit()
            
            # Stream output in real-time
            while True:
                if self._stopped:
                    self.process.terminate()
                    break
                
                line = self.process.stdout.readline()
                if not line and self.process.poll() is not None:
                    break
                if line:
                    self.output_line.emit(line.rstrip('\n\r'))
            
            exit_code = self.process.wait()
            self.process_finished.emit(exit_code)
            
        except Exception as e:
            self.error_line.emit(f"Error: {str(e)}")
            self.process_finished.emit(-1)
    
    def _prepare_command(self) -> list:
        """Prepare command with admin elevation if needed"""
        if not self.admin:
            return self.command
        
        if sys.platform == "win32":
            # PowerShell elevation
            cmd_str = " ".join(self.command)
            return [
                "powershell", "-Command",
                f"Start-Process powershell -ArgumentList '-Command {cmd_str}' -Verb RunAs -Wait"
            ]
        else:
            # macOS/Linux with osascript
            cmd_str = " ".join(self.command)
            return [
                "osascript", "-e",
                f'do shell script "{cmd_str}" with administrator privileges'
            ]
    
    def stop(self):
        """Gracefully stop the process"""
        self._stopped = True
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
```

## Usage in PyQt6

```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.runners = []
        self.setup_ui()
    
    def run_command(self, command: list[str], admin: bool = False):
        runner = CommandRunner(command, admin=admin)
        runner.output_line.connect(self.terminal.log)
        runner.error_line.connect(lambda e: self.terminal.log(f"❌ {e}"))
        runner.process_finished.connect(self.on_process_done)
        runner.process_started.connect(lambda: self.terminal.log("▶ Started"))
        
        self.runners.append(runner)
        runner.start()
        return runner
    
    def on_process_done(self, exit_code: int):
        if exit_code == 0:
            self.terminal.log("✅ Completed successfully")
        else:
            self.terminal.log(f"⚠ Exited with code: {exit_code}")
    
    def closeEvent(self, event):
        # Clean up all runners
        for runner in self.runners:
            runner.stop()
            runner.wait(2000)  # Wait max 2 seconds
        event.accept()
```

## Platform Detection

```python
import sys
import platform

def get_platform_info():
    return {
        "os": sys.platform,           # 'win32', 'darwin', 'linux'
        "os_name": platform.system(), # 'Windows', 'Darwin', 'Linux'
        "is_windows": sys.platform == "win32",
        "is_mac": sys.platform == "darwin",
        "is_linux": sys.platform.startswith("linux"),
    }

def get_shell_command(script: str) -> list[str]:
    """Get platform-appropriate shell command"""
    if sys.platform == "win32":
        return ["powershell", "-Command", script]
    else:
        return ["bash", "-c", script]
```

## Multiple Concurrent Processes

```python
class ProcessManager:
    def __init__(self):
        self.processes: dict[str, CommandRunner] = {}
    
    def start(self, name: str, command: list[str]) -> CommandRunner:
        if name in self.processes:
            self.stop(name)
        
        runner = CommandRunner(command)
        runner.finished.connect(lambda: self._cleanup(name))
        self.processes[name] = runner
        runner.start()
        return runner
    
    def stop(self, name: str):
        if name in self.processes:
            self.processes[name].stop()
            self.processes[name].wait(2000)
    
    def stop_all(self):
        for name in list(self.processes.keys()):
            self.stop(name)
    
    def _cleanup(self, name: str):
        if name in self.processes:
            del self.processes[name]
```

## Key Points

1. **Always use QThread** - Never block the main thread
2. **Use signals** - Thread-safe UI updates
3. **Buffer output** - `bufsize=1` for line buffering
4. **Handle cleanup** - Stop processes on window close
5. **Hide console** - Use `CREATE_NO_WINDOW` on Windows
