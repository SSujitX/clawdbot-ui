#!/usr/bin/env python3
"""
Automatic CHANGELOG.md Generator
Generates changelog from git commits with GitHub links
"""

import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


# GitHub repository (update this if needed)
GITHUB_REPO = "SSujitX/clawdbot-ui"

# Emoji mappings for commit types
TYPE_EMOJIS = {
    "feat": "✨",
    "fix": "🐛",
    "docs": "📝",
    "style": "💄",
    "refactor": "♻️",
    "perf": "⚡",
    "test": "✅",
    "build": "👷",
    "ci": "💚",
    "chore": "🔧",
    "revert": "⏪",
}

# Type labels for changelog
TYPE_LABELS = {
    "feat": "✨ Features",
    "fix": "🐛 Bug Fixes",
    "docs": "📝 Documentation",
    "style": "💄 Styles",
    "refactor": "♻️ Code Refactoring",
    "perf": "⚡ Performance Improvements",
    "test": "✅ Tests",
    "build": "👷 Build System",
    "ci": "💚 Continuous Integration",
    "chore": "🔧 Chores",
    "revert": "⏪ Reverts",
}


def run_command(cmd: List[str]) -> str:
    """Run a shell command and return output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        sys.exit(1)


def get_latest_tag() -> str:
    """Get the latest git tag."""
    try:
        return run_command(["git", "describe", "--tags", "--abbrev=0"])
    except:
        # No tags yet
        return None


def get_commits_since_tag(tag: str = None) -> List[str]:
    """Get all commits since the given tag (or all commits if no tag)."""
    if tag:
        cmd = ["git", "log", f"{tag}..HEAD", "--pretty=format:%H|%s|%b"]
    else:
        cmd = ["git", "log", "--pretty=format:%H|%s|%b"]
    
    output = run_command(cmd)
    if not output:
        return []
    
    commits = []
    current_commit = []
    
    for line in output.split('\n'):
        if '|' in line and len(line.split('|')) >= 2:
            if current_commit:
                commits.append('|'.join(current_commit))
            current_commit = [line]
        else:
            if current_commit:
                current_commit.append(line)
    
    if current_commit:
        commits.append('|'.join(current_commit))
    
    return commits


def parse_commit(commit_str: str) -> Dict:
    """Parse a commit string into structured data."""
    parts = commit_str.split('|', 2)
    if len(parts) < 2:
        return None
    
    commit_hash = parts[0]
    subject = parts[1]
    body = parts[2] if len(parts) > 2 else ""
    
    # Parse conventional commit format: type(scope): description
    match = re.match(r'^(\w+)(?:\(([^)]+)\))?: (.+)$', subject)
    
    if not match:
        # Not a conventional commit, treat as chore
        return {
            "hash": commit_hash,
            "type": "chore",
            "scope": None,
            "description": subject,
            "body": body,
            "breaking": False,
        }
    
    commit_type = match.group(1)
    scope = match.group(2)
    description = match.group(3)
    
    # Check for breaking changes
    breaking = "BREAKING CHANGE" in body or subject.startswith(f"{commit_type}!")
    
    # Extract issue numbers from description and body
    issues = re.findall(r'#(\d+)', subject + body)
    
    return {
        "hash": commit_hash,
        "type": commit_type,
        "scope": scope,
        "description": description,
        "body": body,
        "breaking": breaking,
        "issues": issues,
    }


def group_commits_by_type(commits: List[Dict]) -> Dict[str, List[Dict]]:
    """Group commits by their type."""
    grouped = {}
    
    for commit in commits:
        if not commit:
            continue
        
        commit_type = commit["type"]
        if commit_type not in grouped:
            grouped[commit_type] = []
        
        grouped[commit_type].append(commit)
    
    return grouped


def format_commit_for_changelog(commit: Dict) -> str:
    """Format a single commit for the changelog."""
    short_hash = commit["hash"][:7]
    scope_part = f"**{commit['scope']}**: " if commit['scope'] else ""
    
    # Format description
    description = commit["description"]
    
    # Add issue links
    for issue in commit.get("issues", []):
        issue_link = f"[#{issue}](https://github.com/{GITHUB_REPO}/issues/{issue})"
        description = description.replace(f"#{issue}", issue_link)
    
    # Commit link
    commit_link = f"[{short_hash}](https://github.com/{GITHUB_REPO}/commit/{commit['hash']})"
    
    # Format: * scope: description (commit_link)
    return f"* {scope_part}{description} ({commit_link})"


def get_next_version(current_version: str, commits: List[Dict]) -> str:
    """Determine next version based on commits."""
    # Parse current version
    if not current_version:
        return "1.0.0"
    
    # Remove 'v' prefix if present
    version = current_version.lstrip('v')
    parts = version.split('.')
    
    if len(parts) != 3:
        return "1.0.0"
    
    major, minor, patch = map(int, parts)
    
    # Check for breaking changes
    has_breaking = any(c.get("breaking", False) for c in commits if c)
    has_feat = any(c.get("type") == "feat" for c in commits if c)
    
    if has_breaking:
        major += 1
        minor = 0
        patch = 0
    elif has_feat:
        minor += 1
        patch = 0
    else:
        patch += 1
    
    return f"{major}.{minor}.{patch}"


def generate_changelog_entry(version: str, commits: List[Dict], previous_version: str = None) -> str:
    """Generate a changelog entry for the given version."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Build compare link
    if previous_version:
        compare_link = f"https://github.com/{GITHUB_REPO}/compare/{previous_version}...v{version}"
        header = f"## [{version}]({compare_link}) ({today})"
    else:
        header = f"## v{version} ({today})"
    
    lines = [header, ""]
    
    # Group commits by type
    grouped = group_commits_by_type(commits)
    
    # Add sections in order
    for commit_type in ["feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert"]:
        if commit_type not in grouped:
            continue
        
        type_commits = grouped[commit_type]
        if not type_commits:
            continue
        
        # Add section header
        section_label = TYPE_LABELS.get(commit_type, commit_type.capitalize())
        lines.append(f"### {section_label}")
        lines.append("")
        
        # Add commits
        for commit in type_commits:
            lines.append(format_commit_for_changelog(commit))
        
        lines.append("")
    
    return "\n".join(lines)


def generate_full_changelog(new_version: str, new_entry: str) -> str:
    """Generate complete CHANGELOG.md content from all git tags."""
    content = ["# Changelog", "", "All notable changes to ClawdBot Control Panel will be documented in this file.", ""]
    
    # Add new version entry first
    content.extend(new_entry.split('\n'))
    content.append("")
    
    # Get all existing tags
    try:
        all_tags = run_command(["git", "tag", "-l", "--sort=-version:refname"])
        tags = [t for t in all_tags.split('\n') if t.strip() and t.startswith('v')]
    except:
        tags = []
    
    # Generate entries for each existing tag
    for tag in tags:
        tag_version = tag.lstrip('v')
        
        # Get commits for this tag
        try:
            # Find previous tag
            tag_index = tags.index(tag)
            prev_tag = tags[tag_index + 1] if tag_index + 1 < len(tags) else None
            
            # Get commits between tags
            if prev_tag:
                commit_range = f"{prev_tag}..{tag}"
            else:
                # First tag, get all commits up to it
                commit_range = tag
            
            commit_strings = run_command(["git", "log", commit_range, "--pretty=format:%H|%s|%b"]).split('\n')
            commits = [parse_commit(c) for c in commit_strings if c]
            commits = [c for c in commits if c]
            
            if commits:
                # Generate entry for this version
                tag_date = run_command(["git", "log", "-1", "--format=%ai", tag]).split()[0]
                entry = generate_changelog_entry(tag_version, commits, prev_tag)
                content.extend(entry.split('\n'))
                content.append("")
        except:
            continue
    
    return '\n'.join(content)


def update_changelog(version: str, entry: str):
    """Completely regenerate CHANGELOG.md file."""
    changelog_path = Path("CHANGELOG.md")
    
    # Generate complete changelog
    full_content = generate_full_changelog(version, entry)
    
    # Write complete file
    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"✅ Completely regenerated CHANGELOG.md with version {version}")


def main():
    """Main function."""
    print("🔍 Analyzing git commits...")
    
    # Get latest tag
    latest_tag = get_latest_tag()
    print(f"📌 Latest tag: {latest_tag or 'None (first release)'}")
    
    # Get commits since last tag
    commit_strings = get_commits_since_tag(latest_tag)
    
    if not commit_strings:
        print("⚠️  No new commits since last tag")
        return
    
    print(f"📝 Found {len(commit_strings)} commits")
    
    # Parse commits
    commits = [parse_commit(c) for c in commit_strings]
    commits = [c for c in commits if c]  # Filter None
    
    # Determine next version
    next_version = get_next_version(latest_tag, commits)
    print(f"🚀 Next version: {next_version}")
    
    # Generate changelog entry
    entry = generate_changelog_entry(next_version, commits, latest_tag)
    
    # Update CHANGELOG.md
    update_changelog(next_version, entry)
    
    print(f"\n✨ Done! Changelog updated with v{next_version}")
    print(f"\nNext steps:")
    print(f"1. Review CHANGELOG.md")
    print(f"2. git add CHANGELOG.md")
    print(f"3. git commit -m 'docs: update changelog for v{next_version}'")
    print(f"4. git push")
    print(f"5. Draft release will be auto-created!")


if __name__ == "__main__":
    main()
