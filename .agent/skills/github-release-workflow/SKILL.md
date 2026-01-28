---
name: github-release-workflow
description: Complete GitHub Actions workflow for automated releases with CHANGELOG-based versioning
---

# GitHub Release Workflow

Automated release workflow using GitHub Actions that builds cross-platform binaries and publishes them when a release is published.

## Overview

This workflow consists of 4 interconnected GitHub Actions workflows:

```
┌─────────────────────────────────────────────────────────────┐
│                        Push to master                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  1. auto-draft-release.yml                                   │
│  • Reads version from CHANGELOG.md                           │
│  • Extracts release notes                                    │
│  • Creates/updates draft release                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ (Manual: Publish release on GitHub)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  2. publish.yml                                              │
│  • Triggered when release is published                       │
│  • Extracts version from tag                                 │
│  • Orchestrates parallel builds                              │
└─────────┬────────────────────────────────┬──────────────────┘
          │                                │
          ▼                                ▼
┌──────────────────────┐      ┌───────────────────────────┐
│  3a. build-windows   │      │  3b. build-macos          │
│  • PyInstaller exe   │      │  • PyInstaller .app       │
│  • Uploads artifact  │      │  • Uploads artifact       │
└──────────┬───────────┘      └───────────┬───────────────┘
           │                               │
           └───────────┬───────────────────┘
                       ▼
          ┌────────────────────────────────┐
          │  4. upload-assets.yml          │
          │  • Downloads artifacts         │
          │  • Uploads to release          │
          └────────────────────────────────┘
```

## Workflow Files

### 1. Auto-Draft Release (`auto-draft-release.yml`)

**Purpose:** Automatically create draft releases from CHANGELOG.md

**Triggers:**

```yaml
on:
  push:
    branches:
      - master
```

**What it does:**

1. Reads `CHANGELOG.md`
2. Extracts latest version (e.g., `## v1.0.2`)
3. Extracts release notes between version headers
4. Creates or updates a draft release with:
   - Tag: `v1.0.2`
   - Name: `v1.0.2`
   - Body: Release notes from CHANGELOG

**Key steps:**

```yaml
- name: Extract latest version from CHANGELOG
  run: |
    VERSION=$(grep -m 1 "^## " CHANGELOG.md | sed -E 's/^## \[?v?([0-9]+(\.[0-9]+)+).*/\1/')
    TAG_NAME="v$VERSION"
    echo "version=$VERSION" >> $GITHUB_OUTPUT
    echo "tag=$TAG_NAME" >> $GITHUB_OUTPUT

- name: Extract release notes from CHANGELOG
  run: |
    # Extract content between current version and next version header
    CURRENT_VERSION_LINE=$(grep -n "^## .*$VERSION" CHANGELOG.md | head -1 | cut -d: -f1)
    NEXT_VERSION_LINE=$(tail -n +$((CURRENT_VERSION_LINE + 1)) CHANGELOG.md | grep -n "^## " | head -1 | cut -d: -f1)
    # Extract and save release notes

- name: Create or update draft release
  uses: softprops/action-gh-release@v2
  with:
    tag_name: ${{ steps.version.outputs.tag }}
    name: ${{ steps.version.outputs.tag }}
    body: ${{ steps.changelog.outputs.notes }}
    draft: true
```

**CHANGELOG.md Format:**

```markdown
# Changelog

## v1.0.2

- Fixed gateway stop button UI issues
- Added dynamic port detection
- Improved error handling

## v1.0.1

- Initial release
```

### 2. Publish Release (`publish.yml`)

**Purpose:** Orchestrate builds when release is published

**Triggers:**

```yaml
on:
  release:
    types: [published]
```

**What it does:**

1. Extracts version from release tag (`v1.0.2` → `1.0.2`)
2. Calls `build-windows.yml` in parallel
3. Calls `build-macos.yml` in parallel
4. Calls `upload-assets.yml` after builds complete

**Key structure:**

```yaml
jobs:
  setup:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.get_version.outputs.version }}
      tag_name: ${{ steps.get_version.outputs.tag_name }}
    steps:
      - name: Extract version from release tag
        run: |
          tag_name="${{ github.event.release.tag_name }}"
          version="${tag_name#v}"  # Remove 'v' prefix
          echo "version=$version" >> $GITHUB_OUTPUT

  build-windows:
    needs: setup
    uses: ./.github/workflows/build-windows.yml # Reusable workflow
    with:
      version: ${{ needs.setup.outputs.version }}

  build-macos:
    needs: setup
    uses: ./.github/workflows/build-macos.yml
    with:
      version: ${{ needs.setup.outputs.version }}

  upload-assets:
    needs: [setup, build-windows, build-macos]
    uses: ./.github/workflows/upload-assets.yml
    with:
      version: ${{ needs.setup.outputs.version }}
      tag_name: ${{ needs.setup.outputs.tag_name }}
```

### 3a. Build Windows (`build-windows.yml`)

**Purpose:** Build Windows executable using PyInstaller

**Type:** Reusable workflow (`workflow_call`)

**Inputs:**

- `version`: Version string (e.g., `1.0.2`)

**What it does:**

1. Checkout code
2. Install Python 3.13
3. Install dependencies (PyQt6, PyInstaller, Pillow)
4. Build with PyInstaller:
   ```bash
   pyinstaller --name "ClawdBot-Control-Panel" \
     --onefile --windowed \
     --icon="assets/clawdbot.png" \
     --add-data="assets;assets" \
     main.py
   ```
5. Rename: `ClawdBot-Control-Panel.exe` → `ClawdBot-Control-Panel-v1.0.2-Windows.exe`
6. Upload artifact

**Key steps:**

```yaml
- name: Install dependencies
  run: |
    pip install pyqt6 websockets pyinstaller pillow

- name: Build Windows executable
  run: |
    pyinstaller --name "ClawdBot-Control-Panel" \
      --onefile --windowed \
      --icon="assets/clawdbot.png" \
      --add-data="assets;assets" \
      --noconfirm --clean main.py

- name: Rename executable
  run: |
    $version = "${{ inputs.version }}"
    Move-Item "dist\ClawdBot-Control-Panel.exe" "dist\ClawdBot-Control-Panel-v$version-Windows.exe"

- name: Upload artifact
  uses: actions/upload-artifact@v4
  with:
    name: windows-exe
    path: dist/*.exe
    retention-days: 1
```

### 3b. Build macOS (`build-macos.yml`)

**Purpose:** Build macOS application using PyInstaller

**Type:** Reusable workflow (`workflow_call`)

**Inputs:**

- `version`: Version string (e.g., `1.0.2`)

**What it does:**

1. Checkout code
2. Install Python 3.13
3. Install dependencies (PyQt6, PyInstaller, Pillow)
4. Build with PyInstaller:
   ```bash
   pyinstaller --name "ClawdBot-Control-Panel" \
     --windowed \
     --icon="assets/clawdbot.png" \
     --add-data="assets:assets" \
     main.py
   ```
   Note: `--add-data` uses `:` on macOS/Linux, `;` on Windows
5. Create zip: `ClawdBot-Control-Panel-v1.0.2-macOS.zip`
6. Upload artifact

**Key steps:**

```yaml
- name: Install dependencies
  run: |
    pip install pyqt6 websockets pyinstaller pillow

- name: Build macOS app
  run: |
    pyinstaller --name "ClawdBot-Control-Panel" \
      --windowed \
      --icon="assets/clawdbot.png" \
      --add-data="assets:assets" \
      --noconfirm --clean main.py

- name: Create macOS zip
  run: |
    version="${{ inputs.version }}"
    cd dist
    zip -r "ClawdBot-Control-Panel-v$version-macOS.zip" "ClawdBot-Control-Panel.app"

- name: Upload artifact
  uses: actions/upload-artifact@v4
  with:
    name: macos-app
    path: dist/*.zip
```

### 4. Upload Assets (`upload-assets.yml`)

**Purpose:** Download artifacts and upload to release

**Type:** Reusable workflow (`workflow_call`)

**Inputs:**

- `version`: Version string
- `tag_name`: Full tag (e.g., `v1.0.2`)

**What it does:**

1. Download Windows artifact (from `build-windows`)
2. Download macOS artifact (from `build-macos`)
3. Upload all files to the release

**Key steps:**

```yaml
- name: Download Windows artifact
  uses: actions/download-artifact@v4
  with:
    name: windows-exe
    path: dist/

- name: Download macOS artifact
  uses: actions/download-artifact@v4
  with:
    name: macos-app
    path: dist/

- name: Upload assets to release
  uses: softprops/action-gh-release@v2
  with:
    tag_name: ${{ inputs.tag_name }}
    files: |
      dist/*.exe
      dist/*.zip
    fail_on_unmatched_files: true
```

## Release Process

### Step 1: Update CHANGELOG.md

```markdown
# Changelog

## v1.0.3

- New feature
- Bug fix
- Improvement

## v1.0.2

- Previous changes
```

### Step 2: Commit and Push

```bash
git add CHANGELOG.md
git commit -m "chore: release v1.0.3"
git push origin master
```

**Result:** Draft release `v1.0.3` is automatically created on GitHub

### Step 3: Review Draft Release

1. Go to GitHub → Releases
2. Find draft release `v1.0.3`
3. Review release notes
4. Edit if needed

### Step 4: Publish Release

Click "Publish release" button

**Result:**

- `publish.yml` triggers
- Windows build starts (parallel)
- macOS build starts (parallel)
- Both builds complete
- Artifacts uploaded to release
- Release now has:
  - `ClawdBot-Control-Panel-v1.0.3-Windows.exe`
  - `ClawdBot-Control-Panel-v1.0.3-macOS.zip`

## File Structure

```
.github/workflows/
├── auto-draft-release.yml    # Auto-create drafts from CHANGELOG
├── publish.yml                # Main orchestration
├── build-windows.yml          # Windows build (reusable)
├── build-macos.yml            # macOS build (reusable)
└── upload-assets.yml          # Upload artifacts (reusable)

CHANGELOG.md                   # Source of truth for versions
```

## Key Patterns

### 1. Reusable Workflows

Use `workflow_call` for modular, reusable workflows:

```yaml
# In publish.yml
build-windows:
  uses: ./.github/workflows/build-windows.yml
  with:
    version: ${{ needs.setup.outputs.version }}

# In build-windows.yml
on:
  workflow_call:
    inputs:
      version:
        required: true
        type: string
```

### 2. Parallel Builds

Windows and macOS builds run in parallel for speed:

```yaml
build-windows:
  needs: setup
  uses: ./.github/workflows/build-windows.yml

build-macos:
  needs: setup
  uses: ./.github/workflows/build-macos.yml

upload-assets:
  needs: [setup, build-windows, build-macos] # Wait for both
```

### 3. Artifact Passing

Build artifacts are uploaded then downloaded:

```yaml
# In build-windows.yml
- uses: actions/upload-artifact@v4
  with:
    name: windows-exe
    path: dist/*.exe
    retention-days: 1 # Auto-delete after 1 day

# In upload-assets.yml
- uses: actions/download-artifact@v4
  with:
    name: windows-exe
    path: dist/
```

### 4. CHANGELOG-Based Versioning

Single source of truth in CHANGELOG.md:

- No manual version input
- No version files to maintain
- Release notes automatically extracted

## Permissions

Required in workflow files:

```yaml
permissions:
  contents: write # Needed to create releases and upload assets
```

## Dependencies

Required in both build workflows:

```yaml
pip install pyqt6 websockets pyinstaller pillow
```

**Why Pillow?** PyInstaller needs it to convert PNG icons to platform-specific formats (ICNS on macOS, ICO on Windows).

## Troubleshooting

### Draft release not created

- Check CHANGELOG.md has `## v1.0.0` format
- Ensure push to `master` branch
- Check Actions logs for errors

### Build failed on macOS

- Ensure Pillow is installed
- Check icon path is correct
- Verify `add-data` uses `:` separator

### Assets not uploaded

- Check artifact names match between build and upload workflows
- Verify file patterns (`*.exe`, `*.zip`)
- Check `retention-days` hasn't expired

### Wrong version in filename

- Verify version extracted correctly in setup job
- Check CHANGELOG.md format
- Review version passing between workflows

## Benefits

✅ **Automated**: Push to master → Draft created automatically  
✅ **Consistent**: CHANGELOG is single source of truth  
✅ **Fast**: Parallel builds (Windows + macOS)  
✅ **Modular**: Reusable workflows for each platform  
✅ **Clean**: Artifacts auto-deleted after 1 day  
✅ **Reliable**: Built and uploaded in one workflow run

## Example Complete Flow

1. Developer updates `CHANGELOG.md`:

   ```markdown
   ## v1.0.4

   - Added feature X
   ```

2. Developer pushes to master:

   ```bash
   git push origin master
   ```

3. GitHub Actions:
   - ✅ Draft release `v1.0.4` created

4. Maintainer publishes release on GitHub

5. GitHub Actions:
   - ✅ Windows exe built (5-10 min)
   - ✅ macOS app built (5-10 min)
   - ✅ Both uploaded to release

6. Users download:
   - `ClawdBot-Control-Panel-v1.0.4-Windows.exe`
   - `ClawdBot-Control-Panel-v1.0.4-macOS.zip`
