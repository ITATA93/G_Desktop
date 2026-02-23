# G_Desktop

> Satellite project in the Antigravity ecosystem.

**Domain:** `00_CORE`
**Status:** Active
**Orchestrator:** GEN_OS
**Prefix:** G_

## Description

Windows desktop environment organizer — configuration management, system optimization,
dotfiles, shell profiles, app launchers, and workspace automation for development workstations.

## Features

- **Desktop Configuration**: Shell profiles, terminal themes, PowerShell modules
- **Package Management**: Winget, Scoop, Chocolatey manifests and sync
- **Workspace Automation**: Window layouts, virtual desktops, hotkey configs
- **Dev Environment**: IDE settings, Git config, SSH key management, PATH optimization
- **System Tuning**: Service management, startup optimization, performance tweaks
- **Dotfile Sync**: Cross-machine configuration backup and restore

## Quick Start

```bash
# Dispatch an agent
bash .subagents/dispatch.sh reviewer "Audit this project"

# Run team workflow
bash .subagents/dispatch-team.sh code-and-review "Review recent changes"
```

## Structure

See `CLAUDE.md` for the full project structure documentation.
