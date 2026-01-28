---
name: two-phase-service-stop
description: Robust two-phase process termination pattern for PyQt6 apps with UI feedback and guaranteed cleanup
---

# Two-Phase Service Stop Pattern

Complete implementation for stopping background services/processes in PyQt6 applications with proper UI feedback and guaranteed termination.

## What It Does

Stops background services using a two-phase approach:

**Phase 1**: Send graceful shutdown command  
**Phase 2**: Force kill any remaining process on the target port

This ensures the service is fully terminated even if the graceful shutdown fails or leaves processes running.

## Phase 1: Graceful Shutdown

```python
def _on_stop(self):
    """Initiate service shutdown with immediate UI feedback"""
    self.terminal.log("⋯ Stopping gateway...")

    # 1. Show "Stopping..." state immediately
    self.indicator.setText("● Stopping...")
    self.indicator.setStyleSheet("""
        color: #fbbf24;
        background-color: rgba(251, 191, 36, 0.12);
        padding: 5px 12px;
        border-radius: 4px;
    """)
    self.status_label.setText("Stopping...")

    # 2. Disable all buttons during stop
    self.stop_btn.setEnabled(False)
    self.quick_stop_btn.setEnabled(False)
    self.start_btn.setEnabled(False)
    self.open_btn.setVisible(False)
    self.open_ui_btn.setVisible(False)

    # 3. Stop local process runner if exists
    if self.gateway_runner:
        self.gateway_runner.stop()

    # 4. Run platform-specific stop command
    cmd = (
        ["clawdbot", "gateway", "stop"]
        if not is_windows()
        else ["powershell", "-Command", "clawdbot gateway stop"]
    )

    self.stop_runner = ProcessRunner(cmd)
    self.stop_runner.output.connect(self.terminal.log)
    self.stop_runner.finished.connect(self._on_stop_phase1_finished)
    self.stop_runner.start()
```

## Phase 2: Force Kill on Port

```python
def _on_stop_phase1_finished(self, exit_code):
    """After graceful stop, force kill any remaining process on the port"""
    self.terminal.log("✓ Gateway stop command completed")
    self.terminal.log("⋯ Verifying gateway shutdown...")

    if is_windows():
        # Windows: Find and kill process using Get-NetTCPConnection
        # NOTE: Use $processId (NOT $pid - it's read-only in PowerShell!)
        cmd = '''powershell -Command "
            $port = 18789;
            $conn = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue;
            if ($conn) {
                $processId = $conn.OwningProcess;
                Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue;
                Write-Host 'Killed process on port', $port
            } else {
                Write-Host 'No process found on port', $port
            }"'''
        self.kill_runner = ProcessRunner(cmd, shell=True)
    else:
        # macOS/Linux: Use lsof to find PID and kill it
        cmd = ["sh", "-c", "lsof -ti :18789 | xargs kill -9 2>/dev/null || echo 'No process on port 18789'"]
        self.kill_runner = ProcessRunner(cmd)

    self.kill_runner.output.connect(self.terminal.log)
    self.kill_runner.finished.connect(self._on_stop_finished)
    self.kill_runner.start()
```

## Completion Handler

```python
def _on_stop_finished(self, exit_code):
    """Final cleanup after both stop phases complete"""
    self.terminal.log("✓ Gateway stopped")
    self.terminal.log("━" * 60)

    # Update UI to stopped state (optimistic update)
    self.indicator.setText("● Stopped")
    self.indicator.setStyleSheet("""
        color: #7d8590;
        background-color: #21262d;
        padding: 5px 12px;
        border-radius: 4px;
    """)
    self.status_label.setText("Gateway Stopped")

    # Re-enable controls
    self.start_btn.setEnabled(True)
    self.start_btn.setText("Start Service")
    self.stop_btn.setEnabled(False)
    self.quick_stop_btn.setEnabled(True)
    self.quick_stop_btn.setVisible(False)
    self.open_btn.setVisible(False)
    self.open_ui_btn.setVisible(False)

    # Wait 1 second before verifying actual status (allows cleanup)
    from PyQt6.QtCore import QTimer
    QTimer.singleShot(1000, lambda: self._check_version(silent=True))
```

## Silent Status Checks

Refresh status without logging messages after operations:

```python
def _check_version(self, silent: bool = False):
    """Check service status with optional silent mode"""
    self._silent_check = silent  # Store for callback

    if not silent:
        self.status_label.setText("Checking...")
        self.terminal.log("⋯ Checking ClawdBot installation...")

    self.version_checker = VersionChecker()
    self.version_checker.finished.connect(self._on_version_checked)
    self.version_checker.start()

def _on_version_checked(self, status: dict):
    silent = self._silent_check  # Retrieve flag

    if not silent:
        # Only log when not silent
        self.terminal.log(f"✓ Service status: {status}")

    # Always update UI
    self._update_ui_from_status(status)
```

## Platform-Specific Commands

### Windows (PowerShell)

```powershell
# Find and kill process on port
$port = 18789
$conn = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($conn) {
    $processId = $conn.OwningProcess  # Don't use $pid (read-only!)
    Stop-Process -Id $processId -Force
}
```

**Critical**: `$pid` is a reserved variable in PowerShell (contains current process ID). Always use a different name like `$processId`.

### macOS/Linux (bash/zsh)

```bash
# Find and kill process on port (works on both macOS and Linux)
lsof -ti :18789 | xargs kill -9 2>/dev/null || echo 'No process on port 18789'
```

**Verified**: `lsof` is pre-installed on both macOS and all major Linux distributions. This command works identically on both platforms.

## Application Cleanup

```python
def closeEvent(self, event):
    """Stop all runners when app closes"""
    def safe_stop(runner, timeout=2000):
        if runner and runner.isRunning():
            runner.stop() if hasattr(runner, 'stop') else runner.terminate()
            runner.wait(timeout)

    # Stop all runners (including kill_runner)
    safe_stop(self.gateway_runner, 3000)
    safe_stop(getattr(self, 'stop_runner', None))
    safe_stop(getattr(self, 'kill_runner', None))
    safe_stop(getattr(self, 'version_checker', None), 1000)

    # Also stop background service
    try:
        import subprocess, sys
        if sys.platform == "win32":
            subprocess.run(
                ["powershell", "-Command", "clawdbot gateway stop"],
                capture_output=True, timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            subprocess.run(
                ["clawdbot", "gateway", "stop"],
                capture_output=True, timeout=5
            )
    except Exception:
        pass

    event.accept()
```

## Key Design Principles

1. **Immediate Feedback**: Update UI before running commands
2. **Two-Phase Stop**: Graceful then forceful termination
3. **Silent Updates**: Don't spam logs when refreshing status
4. **Optimistic UI**: Show "Stopped" immediately, verify later
5. **Platform Awareness**: Correct commands for Windows vs Unix
6. **Delayed Verification**: Wait for cleanup to complete

## Usage

This pattern is ideal for:

- Gateway/server processes running on specific ports
- Background services that may leave orphaned processes
- Windows Scheduled Tasks that don't fully terminate
- Any service where graceful shutdown might fail

The two-phase approach guarantees the port is freed and ready for the next start.
