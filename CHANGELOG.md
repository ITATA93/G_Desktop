---
depends_on: []
impacts: []
---

# Changelog — G_Desktop

All notable changes to this project will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Governance audit: docs/TODO.md created
- Gemini settings.json verified
- README.md enhanced with architecture and usage docs
- `.env.example` expanded with all configuration keys (Notion, Canvas, GitHub, Gemini, Brave, AG_ENV)
- `Makefile` created with targets: help, install, build, dev, lint, type-check, test, validate, audit, health, backup, clean, sync-knowledge, sync-memory, sync-templates
- `docs/library/scripts.md` rewritten with full documentation of 90 scripts across 8 categories (agent/dispatch, Python, TypeScript, shell, setup, src modules, tests, archive)

## [0.1.0] — 2026-02-23

### Added
- Initial project creation based on G_Notebook infrastructure.
- Full multi-vendor dispatch: .subagents/, .claude/, .codex/, .gemini/, .agent/.
- Governance standards: docs/standards/.
- CI/CD workflows: .github/workflows/.
- Desktop-focused identity: Windows environment organization and configuration.
