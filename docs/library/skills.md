---
depends_on:
  - .subagents/skills/deep-research.md
  - .subagents/skills/project-init.md
  - .subagents/skills/project-memory.md
  - .subagents/skills/help.md
  - docs/standards/quality_contracts.md
impacts:
  - docs/standards/output_governance.md
---

# Skills Library

> **Version:** 1.0 | **Last updated:** 2026-02-22
> **Source of truth:** `.subagents/skills/`, `.claude/skills/`, `.gemini/skills/`
> **Standard:** `docs/standards/quality_contracts.md` (QC-S rubric)

## Registered Skills

| ID | Skill | Primary Location | Vendor Mirrors | Quality Contract | Status |
|----|-------|-----------------|----------------|-----------------|--------|
| SK-001 | deep-research | `.subagents/skills/deep-research.md` | `.claude/skills/`, `.gemini/skills/` | QC-S001..S007 + custom | active |
| SK-002 | project-init | `.subagents/skills/project-init.md` | `.claude/skills/`, `.gemini/skills/` | QC-S001..S007 | active |
| SK-003 | project-memory | `.subagents/skills/project-memory.md` | `.claude/skills/`, `.gemini/skills/` | QC-S001..S007 | active |
| SK-004 | help | `.subagents/skills/help.md` | `.claude/skills/`, `.gemini/skills/` | QC-S001..S007 | active |

## Skill Summary

### SK-001: Deep Research
- **Purpose:** Execute comprehensive multi-source research with citations
- **Trigger:** `/research`, ad-hoc research request
- **Output:** `docs/research/{DATE}_{topic}.md` with INDEX update
- **Custom QC:** >= 5 primary sources, sources < 90 days, actionable recommendations

### SK-002: Project Init
- **Purpose:** Initialize new project with standard directory structure
- **Trigger:** `/project:init`
- **Output:** Full project scaffold (.gemini/, .claude/, .agent/, .subagents/, docs/)
- **Custom QC:** All required dirs created, manifest.json valid, governance files present

### SK-003: Project Memory
- **Purpose:** Persistent memory management across sessions
- **Trigger:** `/memory:sync`, auto-load at session start
- **Output:** Updates to DEVLOG.md, TASKS.md, memory index
- **Custom QC:** No data loss on sync, append-only for DEVLOG

### SK-004: Help
- **Purpose:** User guide and system assistance
- **Trigger:** `/help`, `@Ayuda`
- **Output:** Interactive help summary from GUIDE.md
- **Custom QC:** References current manifest.json, lists available agents

## Vendor Parity

All skills exist in 3 locations for cross-vendor compatibility:
1. `.subagents/skills/` — Universal (source of truth)
2. `.claude/skills/` — Claude Code mirror
3. `.gemini/skills/` — Gemini CLI mirror

When updating a skill, update all 3 locations in the same commit.

## Adding a New Skill

1. Create `.subagents/skills/{skill-name}.md` with frontmatter including `quality_contract`
2. Mirror to `.claude/skills/` and `.gemini/skills/`
3. Add entry to this registry with ID `SK-{NNN}`
4. Quality contract must follow `docs/standards/quality_contracts.md` QC-S rubric
5. Test the skill at least once before marking status as `active`
