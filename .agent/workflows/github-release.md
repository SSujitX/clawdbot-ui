---
description: how to use github workflows for release and building
---

# GitHub Workflows

This project uses GitHub Actions for automated releases and builds.

## Available Workflows

### 1. Build & Release (`build.yml`)

**Location:** `.github/workflows/build.yml`

**Triggers:**
- When a GitHub Release is published
- Manual trigger via `workflow_dispatch`

**What it does:**
1. Builds Windows `.exe` using Nuitka
2. Builds macOS `.app` using Nuitka
3. Uploads artifacts to the release

**To use:**
1. Go to GitHub → Releases → Draft a new release
2. Create tag (e.g., `v1.0.0`)
3. Publish release
4. Workflow automatically builds and attaches binaries

### 2. Release Drafter (`release-drafter.yml`)

**Location:** `.github/workflows/release-drafter.yml`

**Triggers:**
- Push to `master` branch
- Pull requests opened/updated

**What it does:**
- Automatically drafts release notes based on merged PRs
- Categorizes changes by labels (feature, fix, enhancement)

**Config:** `.github/release-drafter.yml`

## Manual Workflow Trigger

1. Go to GitHub → Actions
2. Select "Build & Release"
3. Click "Run workflow"
4. Select branch and run

## Labels for Release Notes

Add these labels to PRs for auto-categorization:

| Label | Category |
|-------|----------|
| `feature`, `feat` | 🚀 What's new |
| `enhancement`, `improvement` | ✨ Improvements |
| `fix`, `bug` | 🐛 No longer broken |
| `chore`, `docs`, `ci` | 🧰 Maintenance |

## Build Outputs

| Platform | File |
|----------|------|
| Windows | `ClawdBot-Control-Panel-Windows.exe` |
| macOS | `ClawdBot-Control-Panel-macOS.app.zip` |
