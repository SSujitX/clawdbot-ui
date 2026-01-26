# Non-blocking command runner with real-time output streaming

from PyQt6.QtCore import QThread, pyqtSignal
import subprocess
import sys


class ProcessRunner(QThread):
    # Runs commands in background thread with live output
    
    
    output = pyqtSignal(str)
    error = pyqtSignal(str)
    started = pyqtSignal()
    finished = pyqtSignal(int)
    
    def __init__(self, command: list[str] | str, shell: bool = False, cwd: str = None, admin: bool = False):
        super().__init__()
        self.command = command
        self.shell = shell
        self.cwd = cwd
        self.admin = admin
        self.process = None
        self._stopped = False
    
    
    def _prepare_command(self):
        # Prepare command with admin elevation if needed
        cmd = self.command
        
        if not self.admin:
            return cmd
        
        # Convert to string if list
        if isinstance(cmd, list):
            cmd_str = " ".join(cmd)
        else:
            cmd_str = cmd
        
        # Windows: Use PowerShell with RunAs
        if sys.platform == "win32":
            return [
                "powershell", "-Command",
                f"Start-Process powershell -ArgumentList '-NoExit -Command {cmd_str}' -Verb RunAs -Wait"
            ]
        # macOS: Use osascript for admin prompt
        elif sys.platform == "darwin":
            return [
                "osascript", "-e",
                f'do shell script "{cmd_str}" with administrator privileges'
            ]
        # Linux: Use sudo
        else:
            return ["sudo", "-S"] + (cmd if isinstance(cmd, list) else cmd.split())
    
    def run(self):
        # Execute command and stream output
        try:
            cmd = self._prepare_command()
            startupinfo = self._get_startupinfo()
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=self.shell,
                cwd=self.cwd,
                text=True,
                bufsize=1,
                startupinfo=startupinfo,
                creationflags=self._get_creationflags()
            )
            
            self.started.emit()
            
            # Stream output line by line
            while True:
                if self._stopped:
                    self.process.terminate()
                    break
                
                line = self.process.stdout.readline()
                if not line and self.process.poll() is not None:
                    break
                if line:
                    self.output.emit(line.rstrip())
            
            exit_code = self.process.wait()
            self.finished.emit(exit_code)
            
        except Exception as e:
            self.error.emit(str(e))
            self.finished.emit(-1)
    
    def _get_startupinfo(self):
        # Hide console window on Windows
        if sys.platform == "win32":
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            return si
        return None
    
    def _get_creationflags(self):
        # Prevent new console window on Windows
        if sys.platform == "win32":
            return subprocess.CREATE_NO_WINDOW
        return 0
    
    def stop(self):
        # Gracefully stop the process
        self._stopped = True
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
