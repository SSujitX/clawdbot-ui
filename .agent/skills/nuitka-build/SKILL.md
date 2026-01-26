---
name: nuitka-build
description: Build Python/PyQt6 apps into standalone executables using Nuitka
---

# Nuitka Build Skill

Build ClawdBot UI into standalone executables for Windows and macOS using Nuitka.

## What is Nuitka?

Nuitka compiles Python code to native C executables. Benefits:
- **Faster execution** - Compiled to native code
- **No Python required** - Standalone distribution
- **PyQt6 support** - Built-in plugin
- **Cross-platform** - Windows, macOS, Linux

## Installation

```bash
pip install nuitka
```

## Local Build Commands

### Windows (Single .exe)

```bash
python -m nuitka --mode=onefile --enable-plugin=pyqt6 --windows-console-mode=disable --output-dir=dist main.py
```

### Windows (Folder distribution)

```bash
python -m nuitka --mode=standalone --enable-plugin=pyqt6 --windows-console-mode=disable --output-dir=dist main.py
```

### macOS (.app bundle)

```bash
python -m nuitka --mode=app --enable-plugin=pyqt6 --macos-app-icon=assets/clawdbot.png --output-dir=dist main.py
```

## GitHub Actions with Nuitka-Action

Use [Nuitka-Action](https://github.com/Nuitka/Nuitka-Action) for CI/CD builds.

### Workflow Structure

```yaml
- name: Build with Nuitka
  uses: Nuitka/Nuitka-Action@main
  with:
    nuitka-version: main
    script-name: main.py
    mode: onefile           # or standalone, app
    enable-plugins: pyqt6
    windows-console-mode: disable
    output-file: MyApp
```

### Key Options

| Option | Values | Description |
|--------|--------|-------------|
| `mode` | `onefile`, `standalone`, `app` | Output type |
| `enable-plugins` | `pyqt6`, `pyside6` | UI framework |
| `windows-console-mode` | `disable`, `attach` | Hide console |
| `windows-icon-from-ico` | Path | Windows .ico icon |
| `macos-app-icon` | Path | macOS .png/.icns icon |
| `output-file` | Name | Output filename |

## Current Project Workflow

Located at: `.github/workflows/build.yml`

**Triggers:**
- GitHub Release published
- Manual (`workflow_dispatch`)

**Builds:**
| Platform | Mode | Output |
|----------|------|--------|
| Windows | onefile | `ClawdBot-Control-Panel-Windows.exe` |
| macOS | app | `ClawdBot-Control-Panel-macOS.app.zip` |

**Steps:**
1. Checkout code
2. Setup Python 3.13
3. Install UV + dependencies
4. Build with Nuitka-Action
5. Upload artifacts + attach to release

## Requirements

### Windows
- Visual Studio Build Tools OR MinGW64 (auto-downloaded by Nuitka)

### macOS
- Xcode Command Line Tools
- `xcode-select --install`

### Both
- Python 3.13+
- C compiler (auto-handled in GitHub Actions)

## Common Issues

### Missing DLLs (Windows)
Use `--mode=standalone` first to debug, then switch to `--mode=onefile`.

### PyQt6 not found
Ensure `--enable-plugin=pyqt6` is set.

### Large file size
Normal for PyQt6 apps (~50-100MB). Nuitka includes Qt libraries.

### Console window appears
Add `--windows-console-mode=disable`.

## Tips

1. **Test locally first** before pushing to GitHub Actions
2. **Use standalone mode** for debugging
3. **Check build output** for missing modules
4. **Add `--show-progress`** for verbose local builds
