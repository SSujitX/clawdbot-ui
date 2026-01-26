---
name: coding-conventions
description: Code style rules - clean, minimal, comment-first approach
---

# Coding Conventions

## Rule 1: Comment First

Before writing any code block, add a comment explaining what it does:

```python
# Initialize main window with dark theme
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
```

## Rule 2: No Extra Code

Write only what's needed. No boilerplate, no unused imports, no placeholder comments.

❌ Bad:
```python
# TODO: implement later
# This might be useful
# import something_unused
```

✅ Good:
```python
# Handle button click to start gateway
def on_start_clicked(self):
    self.start_gateway()
```

## Rule 3: Clean Folder Structure

```
src/
├── main.py           # Entry point
├── ui/
│   ├── window.py     # Main window
│   ├── terminal.py   # Log viewer
│   └── styles.py     # Dark theme CSS
├── core/
│   ├── process.py    # Command runner
│   └── gateway.py    # WebSocket client
└── utils/
    └── platform.py   # OS detection
```

## Rule 4: Simple Filenames

- Lowercase only
- Underscores for spaces
- Short and descriptive
- No prefixes like `my_`, `the_`, `base_`

✅ `terminal.py`, `process.py`, `styles.py`
❌ `MyTerminalWidget.py`, `base_process_runner.py`

## Rule 5: Verify Before Commit

Before finishing any code:
1. Check imports are used
2. Check no syntax errors
3. Check logic is correct
4. Check file paths exist

## Code Template

```python
# [Brief description of what this file does]

# Imports
from PyQt6.QtWidgets import QWidget

# [Description of class/function]
class MyClass:
    def __init__(self):
        # [What this does]
        pass
```

## Rule 6: Update Skills After Changes

After making any significant changes:
1. Update relevant skill files in `.agent/skills/`
2. Document what was changed
3. Keep skills in sync with actual code

This ensures we stay on track and remember what was done.

