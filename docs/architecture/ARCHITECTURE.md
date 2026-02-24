# Architecture — Antigravity Development Environment

## Overview

Antigravity is a multi-agent development environment that combines Gemini CLI and Claude Code for AI-assisted software development.

```text
┌────────────────────────────────────────────────────────┐
│                    ANTIGRAVITY SYSTEM                  │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌─────────────┐         ┌─────────────┐               │
│  │  Gemini CLI │◄────────► Claude Code │               │
│  │  (Orchestr) │         │ (Sub-agent) │               │
│  └──────┬──────┘         └──────┬──────┘               │
│         │                       │                      │
│         ▼                       ▼                      │
│  ┌──────────────────────────────────────┐              │
│  │         SUB-AGENTS (6)               │              │
│  ├──────────────────────────────────────┤              │
│  │ code-analyst  │ doc-writer           │              │
│  │ code-reviewer │ test-writer          │              │
│  │ db-analyst    │ deployer             │              │
│  └──────────────────────────────────────┘              │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## Components

### 1. Global Profile (`~/.gemini/`, `~/.claude/`)

Shared configuration installed in user home directory:
- Agent definitions (TOML)
- Behavioral rules (Markdown)
- Workflows (Markdown)
- Skills (Markdown)
- Commands (TOML/Markdown)

### 2. Project Template (`_template/`)

Quick-start for new projects with:
- Pre-configured Gemini and Claude settings
- Sub-agent manifest
- Documentation structure
- Standard directory layout

### 3. Sub-Agents

| Agent         | Vendor | Specialty                          |
| ------------- | ------ | ---------------------------------- |
| code-analyst  | Gemini | Code analysis, architecture review |
| doc-writer    | Gemini | Documentation maintenance          |
| code-reviewer | Claude | Code review, security audit        |
| test-writer   | Gemini | Test generation                    |
| db-analyst    | Claude | Database analysis, SQL             |
| deployer      | Gemini | CI/CD, deployment                  |
| researcher    | Codex  | Deep research and documentation    |

### 4. Delegation Protocol

```
User Request
     ”‚
     –¼
”Œ”€”€”€”€”€”€”€”€”€”€”€”€”
”‚  Trigger   ”‚”€”€–º Detect keywords matching sub-agent
”‚ Detection  ”‚
”””€”€”€”€”€”¬”€”€”€”€”€”€”˜
      ”‚
      –¼
”Œ”€”€”€”€”€”€”€”€”€”€”€”€”
”‚  Context   ”‚”€”€–º Prepare briefing with relevant files
”‚ Preparation”‚
”””€”€”€”€”€”¬”€”€”€”€”€”€”˜
      ”‚
      –¼
┌────────────┐
│ Invocation │──► ./.subagents/dispatch.ps1 {agent} "prompt"
└────────────┘
      ”‚
      –¼
”Œ”€”€”€”€”€”€”€”€”€”€”€”€”
”‚Verification”‚”€”€–º Check output, retry if needed (max 2)
”””€”€”€”€”€”€”€”€”€”€”€”€”˜
```

## Security Rules

1. **Database Safety**: Never execute DELETE, DROP, UPDATE, TRUNCATE without confirmation
2. **Sandbox Mode**: All agents run with `--sandbox seatbelt`
3. **No Credentials**: Never expose API keys or passwords in code
4. **Read First**: Always read existing code before modifying

## File Organization

```
project/
├── .gemini/           → Gemini CLI config
├── .claude/           → Claude Code config
├── .agent/            → Agent rules
├── docs/              → Documentation
├── scripts/           → Orchestration scripts (cross_task, audit)
├── config/            → Ecosystem config (environments, registry)
├── GEMINI.md          → Global Master Orchestrator rules
├── CLAUDE.md          → Claude Orchestrator rules
├── CHANGELOG.md       → Version history
└── AG_Orquesta.code-workspace  → Multi-root workspace file
```

## Workflows

### Session Start
1. Read DEVLOG.md (last entry)
2. Read TASKS.md (pending tasks)
3. Show git status and recent commits
4. Present executive summary

### Session End
1. Update DEVLOG.md with work done
2. Update TASKS.md with new tasks
3. Update CHANGELOG.md if needed
4. Commit changes with descriptive message

### Parallel Execution
- Maximum 5 agents simultaneously
- Each agent works on different files
- Results aggregated after completion
- Logs saved to `.gemini/agents/logs/`


---

## Core Concepts

# Antigravity Core Concepts & Architecture Bible

> This document serves as the **SINGLE SOURCE OF TRUTH** for the Antigravity system architecture.
> All agents (Gemini, Claude, Codex) must refer to this document for understanding system behavior.

## 0. What is Antigravity?
**Antigravity** is not just a template; it is an **Agentic Orchestration Ecosystem**.
It provides a standardized layer between the **Human Developer** and multiple **AI Vendors** (Gemini, Claude, OpenAI), ensuring:
1.  **Unified Memory**: All agents share the same context (`docs/`, `brain/`).
2.  **Shared Identity**: Agents assume roles ("Profiles") defined in `settings.json`, not random prompts.
3.  **Tool Abstraction**: Common access to filesystem, git, and execution tools via MCP.

Antigravity turns a "Chatbot" into a "Colleague" by giving it a persistent environment and strict operating rules.

## 1. The "Profile" Concept
A **Profile** is a portable configuration set that defines the * capabilities* of an agent. It is NOT the same as a VS Code Profile.

### Anatomy of a Profile
Located at `.gemini/settings.json`, it controls:
*   **Security**: Can I delete files? Can I execute code?
*   **Tools (MCP)**: Do I have access to GitHub? To the Database?
*   **Persona**: Am I a "Secure Backend Dev" or a "Creative Frontend Designer"?

### Global vs. Local Scope
1.  **Global Profile (`~/.gemini/settings.json`)**: The fallback configuration.
2.  **Local Profile (`./.gemini/settings.json`)**: The project-specific override. **Precedence: Local > Global.**

---

## 2. Intelligent Bootstrap (The "Wizard")
Antigravity moves away from manual setup towards *Intelligent Bootstrapping*.

### The Workflow
1.  **User**: Runs `init-project.ps1 "MyProject"`.
2.  **System**: Creates the scaffold (folders, git).
3.  **User**: Runs `gemini /bootstrap`.
4.  **Agent (Skill: bootstrap-project)**:
    *   Ã°Å¸€¢ÂµÃ¯Â¸ÂÃ¢‚¬ÂÃ¢„¢€šÃ¯Â¸Â **Detects**: "This is a Python/FastAPI project".
    *   Ã¢Å¡„¢Ã¯Â¸Â **Configures Agent**: Generates `.gemini/settings.json` (Backend Profile).
    *   Ã°Å¸Å½Â¨ **Configures Editor**: Generates `.vscode/extensions.json` (Python, Ruff).

---

## 3. Project Structure Standard
Every Antigravity project MUST follow this structure to be compatible with the ecosystem:

```
project-root/
”œ”€”€ .gemini/            # Agent Brain & Settings
”œ”€”€ .vscode/            # Human Editor Settings (Generated by Bootstrap)
”œ”€”€ docs/               # Project Memory (Human & AI Readable)
”‚   ”œ”€”€ architecture/   # Core Decisions (Like this file)
”‚   ”œ”€”€ plans/          # Active Implementation Plans
”‚   ”””€”€ research/       # Deep Dives
”””€”€ config/             # Application Configuration
```

## 4. Synchronization Strategy
To prevent "Configuration Drift", we use a **Template-First** approach.
*   **Master Source**: `AG_Plantilla` (The Factory).
*   **Mechanism**: `robocopy` scripts in `_template/`.
*   **Rule**: Never edit scaffolding in a derived project manually; update the template and sync.
