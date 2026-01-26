---
name: clawdbot-cli
description: Complete ClawdBot CLI command reference for all operations
---

# ClawdBot CLI

ClawdBot is an AI agent framework with multi-channel messaging support. This skill covers all CLI commands.

## Installation

```bash
# One-liner install
curl -fsSL https://clawd.bot/install.sh | bash  # macOS/Linux
iwr -useb https://clawd.bot/install.ps1 | iex   # Windows

# Or via npm
npm install -g clawdbot
```

## Core Commands

### Gateway Management
```bash
clawdbot gateway              # Start gateway server (default port 18789)
clawdbot gateway --port 3000  # Custom port
clawdbot gateway stop         # Stop running gateway
clawdbot health --json        # Check gateway status
clawdbot dashboard            # Get dashboard URL with auth token
```

### Version & Updates
```bash
clawdbot --version            # Show installed version
clawdbot update               # Update to latest version
clawdbot uninstall --all --yes # Remove completely
clawdbot reset --yes          # Reset workspace and config
```

### Skills Management
```bash
clawdbot skills               # List available skills
clawdbot skills enable spotify   # Enable a skill
clawdbot skills disable spotify  # Disable a skill
```

## Configuration

Config file: `~/.clawdbot/clawdbot.json`

**Key settings**:
```json
{
  "workspace": "~/clawdbot-workspace",
  "gateway": {
    "port": 18789,
    "enabled": true
  },
  "channels": {
    "whatsapp": { "enabled": false },
    "telegram": { "enabled": false },
    "discord": { "enabled": false }
  },
  "model": "claude-sonnet-4"
}
```

## Workspace Structure

```
~/clawdbot-workspace/
├── AGENTS.md          # Agent definitions
├── SOUL.md            # System personality
├── memory/            # Conversation memory
├── skills/            # Custom skills (SKILL.md format)
└── data/              # Agent data storage
```

## Multi-Channel Support

Supported platforms:
- **WhatsApp** (via whatsapp-web.js)
- **Telegram** (via Bot API)  
- **Discord** (via discord.js)
- **Slack** (via Bolt)
- **SMS** (via Twilio)
- **CLI** (built-in terminal interface)

Enable in `clawdbot.json` → channels → {platform} → enabled: true

## Gateway Architecture

ClawdBot uses a WebSocket gateway for real-time communication:

```
┌─────────────┐     WebSocket      ┌──────────────┐
│  UI/Client  │ ←─────────────────→ │   Gateway    │
└─────────────┘   Port 18789       └──────────────┘
                                           │
                                           ↓
                                    ┌──────────────┐
                                    │   Channels   │
                                    │   • WhatsApp │
                                    │   • Telegram │
                                    │   • Discord  │
                                    └──────────────┘
```

**WebSocket Protocol**:
```json
// Request
{
  "type": "req",
  "id": "unique-id",
  "method": "send_message",
  "params": { "channel": "whatsapp", "text": "Hello" }
}

// Response
{
  "type": "res",
  "id": "unique-id",
  "result": { "success": true }
}
```

## Built-in Tools

ClawdBot agents have access to:

- **exec**: Run shell commands
- **browser**: Headless browser automation
- **canvas**: Generate images/UI mockups
- **nodes**: File system operations
- **search**: Web search integration

Tools are auto-available to agents, no manual config needed.

## Skills System

Skills extend agent capabilities. Format: `SKILL.md` with YAML frontmatter.

**Example skill**:
```markdown
---
name: spotify-control
description: Control Spotify playback
---

# Spotify Control

Commands:
- `play {song}` - Play a song
- `pause` - Pause playback
- `next` - Skip to next track
```

Place in `workspace/skills/` to auto-load.

## Platform-Specific Notes

**Windows**:
- Uses PowerShell for commands
- Install path: `%USERPROFILE%\.clawdbot\`
- Requires admin for gateway (elevated prompt)

**macOS/Linux**:
- Uses bash/zsh
- Install path: `~/.clawdbot/`
- May need `sudo` for gateway on port < 1024

## Common Issues

**Gateway won't start**:
- Check port not in use: `lsof -i :18789` (macOS/Linux)
- Run as admin (Windows) or sudo (Unix)

**Commands not found**:
- Ensure npm global bin in PATH
- Restart terminal after install
- Check: `npm config get prefix`

**Update fails**:
- Run: `npm cache clean --force`
- Then: `npm update -g clawdbot`
