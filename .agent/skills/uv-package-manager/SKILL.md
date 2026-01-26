---
name: uv-package-manager
description: Fast Python package manager - uv commands for project management
---

# UV Package Manager

UV is an extremely fast Python package manager written in Rust.

## Project Commands

```bash
# Initialize new project
uv init

# Initialize with specific Python version
uv init --python 3.14
```

## Package Management

```bash
# Add a package
uv add package-name

# Add multiple packages
uv add pyqt6 websockets asyncio

# Add dev dependency
uv add --dev pytest black

# Remove package
uv remove package-name

# Sync dependencies (install from pyproject.toml)
uv sync
```

## Running Scripts

```bash
# Run Python file
uv run main.py

# Run with arguments
uv run main.py --arg value

# Run module
uv run -m pytest
```

## Virtual Environment

```bash
# Create venv (auto-created on uv sync)
uv venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate
```

## Lock File

```bash
# Generate/update lock file
uv lock

# Install from lock
uv sync --frozen
```

## Project Structure

```
project/
├── pyproject.toml    # Project config + dependencies
├── uv.lock           # Lock file (auto-generated)
├── .venv/            # Virtual environment
└── src/              # Source code
```

## pyproject.toml Example

```toml
[project]
name = "clawdbot-ui"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "pyqt6>=6.6.0",
    "websockets>=12.0",
    "asyncio>=3.4.3",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8.0.0",
    "black>=24.0.0",
]
```

## Key Benefits

- ⚡ 10-100x faster than pip
- 🔒 Deterministic lock files
- 🐍 Python version management
- 📦 Drop-in pip replacement
