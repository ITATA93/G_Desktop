---
title: Script Registry
version: "2.0"
last_updated: "2026-03-01"
---

# Script Registry — G_Desktop

Complete inventory of all scripts, modules, and automation tools in the project.
Total: 87 registered entries across 8 categories.

---

## 1. Agent & Dispatch Scripts (`.gemini/scripts/`, `.subagents/`)

| # | Script | Path | Language | Description |
|---|--------|------|----------|-------------|
| 1 | `deep-research.sh` | `.gemini/scripts/deep-research.sh` | Shell | Executes Gemini Deep Research via API. Requires `GEMINI_API_KEY`. Outputs results to `docs/research/`. |
| 2 | `parallel-agents.sh` | `.gemini/scripts/parallel-agents.sh` | Shell | Launches sub-agents in parallel. Accepts task/agent pairs, logs results to `.gemini/agents/logs/`. |
| 3 | `auto-memory.sh` | `.subagents/auto-memory.sh` | Shell | Automatically updates DEVLOG.md after team execution to capture session outcomes. |
| 4 | `auto-memory.ps1` | `.subagents/auto-memory.ps1` | PowerShell | Windows version of `auto-memory.sh`. |
| 5 | `dispatch.sh` | `.subagents/dispatch.sh` | Shell | Multi-vendor subagent dispatcher. Selects and invokes the correct vendor CLI (Gemini/Claude/Codex) for a given agent. Usage: `./dispatch.sh <agent_name> "<prompt>"`. |
| 6 | `dispatch.ps1` | `.subagents/dispatch.ps1` | PowerShell | Windows version of `dispatch.sh`. |
| 7 | `dispatch-team.sh` | `.subagents/dispatch-team.sh` | Shell | Agent Team orchestrator. Executes a group of agents sequentially or in parallel based on `manifest.json`. Usage: `./dispatch-team.sh <team_name> "<prompt>"`. |
| 8 | `dispatch-team.ps1` | `.subagents/dispatch-team.ps1` | PowerShell | Windows version of `dispatch-team.sh`. |
| 9 | `safe-write.sh` | `.subagents/safe-write.sh` | Shell | Output governance file creator. Ensures files are created in allowed target directories matching Antigravity standards. |
| 10 | `safe-write.ps1` | `.subagents/safe-write.ps1` | PowerShell | Windows version of `safe-write.sh`. |

## 2. Active Python Scripts (`scripts/`)

| # | Script | Path | Language | Description |
|---|--------|------|----------|-------------|
| 11 | `agent_health_check.py` | `scripts/agent_health_check.py` | Python | Validates all agent definitions: manifest existence, definition files, governance references, vendor configs, teams, dispatch scripts, and skills. Usage: `python scripts/agent_health_check.py`. |
| 12 | `agent_selftest.py` | `scripts/agent_selftest.py` | Python | Verifies each project has infrastructure for autonomous agent work. Checks dispatch, workflows, memory, and governance. Computes a 0-100 readiness score. Usage: `python scripts/agent_selftest.py [--project G_X]`. |
| 13 | `audit_ecosystem.py` | `scripts/audit_ecosystem.py` | Python | Context-aware normalization audit of all AG projects. Detects real hardcoded credentials, checks required/recommended files, content quality, and autonomy readiness. Supports `--fix` for auto-remediation. Usage: `python scripts/audit_ecosystem.py [--report] [--project G_X] [--fix]`. |
| 14 | `cross_task.py` | `scripts/cross_task.py` | Python | Cross-workspace task delegation system. Creates, lists, updates, and tracks tasks spanning multiple AG projects. Dual-writes to source (outgoing) and target (incoming) TASKS.md. Usage: `python cross_task.py create/list/update/dashboard/normalize/check/stale`. |
| 15 | `ecosystem_dashboard.py` | `scripts/ecosystem_dashboard.py` | Python | Category-aware dashboard for the full AG ecosystem. Groups projects by category, shows health indicators, supports environment-specific views and JSON output. Usage: `python ecosystem_dashboard.py [--category X] [--json]`. |
| 16 | `env_resolver.py` | `scripts/env_resolver.py` | Python | Central environment resolver replacing all hardcoded paths. Auto-detects current environment by probing filesystem or reading `AG_ENV`. Provides `get_repo_root()`, `get_projects_dirs()`, `get_plantilla_dir()`, `list_ag_projects()`. Usage: `python env_resolver.py [--register] [--list]`. |
| 17 | `knowledge_sync.py` | `scripts/knowledge_sync.py` | Python | Structured knowledge extraction from DEVLOG.md and TASKS.md. Generates context snapshots, updates memory index, syncs to SQLite vault, manages team context, and compacts DEVLOG archives. Usage: `python scripts/knowledge_sync.py [--snapshot] [--index] [--devlog] [--query] [--compact] [--team-context]`. |
| 18 | `memory_sync.py` | `scripts/memory_sync.py` | Python | Transversal memory system. Collects project status across all AG projects and generates a unified ecosystem dashboard at `docs/ecosystem-status.md`. Usage: `python scripts/memory_sync.py sync/dashboard/full`. |
| 19 | `propagate.py` | `scripts/propagate.py` | Python | Template propagation engine. Detects "template drift" between `_template/workspace/` and project files. Can preview diffs and apply approved changes across all AG projects. Usage: `python scripts/propagate.py status/diff/apply`. |
| 20 | `template_sync.py` | `scripts/template_sync.py` | Python | Syncs core files from project root to `_global-profile/` and `_template/workspace/`. Supports dry-run preview. Usage: `python scripts/template_sync.py [--apply]`. |

## 3. Active TypeScript Scripts (`scripts/`)

| # | Script | Path | Language | Description |
|---|--------|------|----------|-------------|
| 21 | `backup-notion.ts` | `scripts/backup-notion.ts` | TypeScript | Backs up all Notion databases to timestamped JSON files in `reports/backups/`. Copies manifest and config alongside data. Requires `NOTION_TOKEN`. Usage: `npx tsx scripts/backup-notion.ts`. |
| 22 | `validate-manifest.ts` | `scripts/validate-manifest.ts` | TypeScript | Validates `manifests/nos.yaml` against `src/config.ts`. Checks DB key alignment, property types, and relation integrity. Usage: `npx tsx scripts/validate-manifest.ts`. |

## 4. Active Shell/PowerShell Scripts (`scripts/`)

| # | Script | Path | Language | Description |
|---|--------|------|----------|-------------|
| 23 | `mcp_governance.ps1` | `scripts/mcp_governance.ps1` | PowerShell | Governance pre-execution hook (guardrail). Scans input for destructive patterns (DROP, DELETE, rm -rf) before allowing execution by dispatchers or MCP tools. |
| 24 | `migrate_ecosystem.ps1` | `scripts/migrate_ecosystem.ps1` | PowerShell | Ecosystem migrator. Migrates flat workspace into the Star Topology domain architecture. |
| 25 | `run-consensus.ps1` | `scripts/run-consensus.ps1` | PowerShell | Runs a Consensus Panel (Mixture of Experts). Executes a turn-based discussion workflow using Gemini, Claude, and Codex to arrive at peer-reviewed technical solutions. |
| 26 | `safe-write.ps1` | `scripts/safe-write.ps1` | PowerShell | Output governance hook. Validates output paths against `docs/standards/output_governance.md` rules and auto-creates missing directories. |
| 27 | `safe-write.sh` | `scripts/safe-write.sh` | Shell | Linux/macOS version of `safe-write.ps1`. |
| 28 | `sync-knowledge.ps1` | `scripts/sync-knowledge.ps1` | PowerShell | Promotes deep research documents to global Gemini Knowledge Items. Windows version. |
| 29 | `sync-knowledge.sh` | `scripts/sync-knowledge.sh` | Shell | Promotes deep research documents to global Gemini Knowledge Items. Linux/macOS version. |
| 30 | `sync-skills.ps1` | `scripts/sync-skills.ps1` | PowerShell | Consolidates and synchronizes Antigravity skills across all vendor directories (`.gemini`, `.claude`, `.codex`) from the universal repository (`.subagents/skills`). |

## 5. Setup Scripts (`scripts/setup/`)

| # | Script | Path | Language | Description |
|---|--------|------|----------|-------------|
| 31 | `backup-config.ps1` | `scripts/setup/backup-config.ps1` | PowerShell | Creates a timestamped backup of Antigravity configuration files (`.gemini/`, `.claude/`, instruction files) before major changes. |
| 32 | `bootstrap_environment.ps1` | `scripts/setup/bootstrap_environment.ps1` | PowerShell | Interactive step-by-step environment setup guide for new machines. Run after cloning G_Plantilla. Supports `--DryRun`. |
| 33 | `bootstrap_environment.py` | `scripts/setup/bootstrap_environment.py` | Python | Cross-platform version of the environment bootstrap. Interactive step-by-step setup requiring git, python, and 7z. |
| 34 | `health-check.ps1` | `scripts/setup/health-check.ps1` | PowerShell | Checks the health of Antigravity installation and configuration. Verifies required tools, files, and configurations. |
| 35 | `health-check.sh` | `scripts/setup/health-check.sh` | Shell | Linux/macOS version of `health-check.ps1`. |
| 36 | `sync-global.ps1` | `scripts/setup/sync-global.ps1` | PowerShell | Synchronizes workspace configuration with global profile (`_global-profile/`). Optionally installs to `~/.gemini/`. |

## 6. Source Modules (`src/`)

| # | Module | Path | Language | Description |
|---|--------|------|----------|-------------|
| 37 | `config.ts` | `src/config.ts` | TypeScript | Centralized configuration for the NOs (Notion Operating System). All database IDs, API endpoints, rate limits, file paths, and constants. |
| 38 | `index.ts` | `src/index.ts` | TypeScript | Unified CLI entry point for the NOs system. Commander-based CLI with commands for deploy, sync, seed. |
| 39 | `deploy.ts` | `src/core/deploy.ts` | TypeScript | Core deployment script. Handles Notion property updates and relation creation from `manifests/nos.yaml`. |
| 40 | `seed.ts` | `src/core/seed.ts` | TypeScript | Seed data generator. Creates master areas, subcategories, projects, and entities in Notion databases. |
| 41 | `setup.ts` | `src/core/setup.ts` | TypeScript | Initial database setup. Creates Notion databases from manifest schema definitions with property mapping. |
| 42 | `templates.ts` | `src/core/templates.ts` | TypeScript | Template definitions for NOs databases. Defines standard block structures and page templates for specific use cases. |
| 43 | `canvas.ts` | `src/sync/canvas.ts` | TypeScript | Canvas LMS unified sync. Syncs courses to `DB_CANVAS_COURSES` and assignments to `DB_MASTER_TASKS` in Notion. Requires `CANVAS_TOKEN`. |
| 44 | `helpers.ts` | `src/utils/helpers.ts` | TypeScript | Utility functions: retry with exponential backoff, rate limiting, and common helpers for Notion API calls. |

## 7. Test Files (`tests/`)

| # | Test | Path | Language | Description |
|---|------|------|----------|-------------|
| 45 | `conftest.py` | `tests/conftest.py` | Python | Pytest configuration and shared fixtures for Python test suite. |
| 46 | `helpers.test.ts` | `tests/helpers.test.ts` | TypeScript | Vitest unit tests for `src/utils/helpers.ts` (retry logic, rate limiter). |
| 47 | `test_audit_ecosystem.py` | `tests/test_audit_ecosystem.py` | Python | Tests for `scripts/audit_ecosystem.py` — normalization checks, security scanning, grading. |
| 48 | `test_audit_ecosystem_meta.py` | `tests/test_audit_ecosystem_meta.py` | Python | Meta-tests ensuring the audit script itself passes its own quality checks. |
| 49 | `test_cross_task.py` | `tests/test_cross_task.py` | Python | Tests for `scripts/cross_task.py` — task creation, listing, updating, delegation. |
| 50 | `test_ecosystem_dashboard.py` | `tests/test_ecosystem_dashboard.py` | Python | Tests for `scripts/ecosystem_dashboard.py` — health checks, dashboard output. |
| 51 | `test_env_resolver.py` | `tests/test_env_resolver.py` | Python | Tests for `scripts/env_resolver.py` — environment detection, path resolution, registration. |
| 52 | `test_propagate.py` | `tests/test_propagate.py` | Python | Tests for `scripts/propagate.py` — template drift detection, diff, apply. |

## 8. Archived Scripts (`scripts/archive/`)

Legacy one-off diagnostic and migration scripts for Notion. **Not part of the main CLI.**
See [LEGACY_SCRIPTS.md](../../LEGACY_SCRIPTS.md) for usage notes.

| # | Script | Path | Language | Description |
|---|--------|------|----------|-------------|
| 53 | `add-missing-properties.ts` | `scripts/archive/add-missing-properties.ts` | TypeScript | Adds missing properties to the Knowledge Base database in Notion. |
| 54 | `analyze-bd-paginas.ts` | `scripts/archive/analyze-bd-paginas.ts` | TypeScript | Analyzes the BD_Paginas database structure and content. |
| 55 | `analyze-config-complete.ts` | `scripts/archive/analyze-config-complete.ts` | TypeScript | Complete analysis of the Config database with all properties. |
| 56 | `analyze-config-db.ts` | `scripts/archive/analyze-config-db.ts` | TypeScript | Basic analysis of the Config database schema. |
| 57 | `analyze-config-deep.ts` | `scripts/archive/analyze-config-deep.ts` | TypeScript | Deep analysis of Config database including nested pages. |
| 58 | `analyze-config-with-pagination.ts` | `scripts/archive/analyze-config-with-pagination.ts` | TypeScript | Config database analysis with paginated queries for large datasets. |
| 59 | `analyze-overlaps.ts` | `scripts/archive/analyze-overlaps.ts` | TypeScript | Detects overlapping entries across Notion databases. |
| 60 | `analyze-schemas.ts` | `scripts/archive/analyze-schemas.ts` | TypeScript | Compares schemas across multiple Notion databases. |
| 61 | `analyze-source-schemas.ts` | `scripts/archive/analyze-source-schemas.ts` | TypeScript | Analyzes source database schemas for migration planning. |
| 62 | `analyze-tipos.ts` | `scripts/archive/analyze-tipos.ts` | TypeScript | Analyzes the legacy "Tipos" taxonomy in Notion. |
| 63 | `check-duplicates.ts` | `scripts/archive/check-duplicates.ts` | TypeScript | Checks for duplicate entries across Notion databases. |
| 64 | `check-knowledge-schema.ts` | `scripts/archive/check-knowledge-schema.ts` | TypeScript | Validates the Knowledge Base database schema against expected structure. |
| 65 | `check-tasks-schema.ts` | `scripts/archive/check-tasks-schema.ts` | TypeScript | Validates the Tasks database schema against expected structure. |
| 66 | `compare-schemas.ts` | `scripts/archive/compare-schemas.ts` | TypeScript | Side-by-side comparison of source and target database schemas. |
| 67 | `create-granular-infra.ts` | `scripts/archive/create-granular-infra.ts` | TypeScript | Creates granular infrastructure entries in Notion (v1). |
| 68 | `create-granular-infra-v3.ts` | `scripts/archive/create-granular-infra-v3.ts` | TypeScript | Creates granular infrastructure entries in Notion (v3, refined). |
| 69 | `create-subcategories.ts` | `scripts/archive/create-subcategories.ts` | TypeScript | Creates subcategory entries in the Notion taxonomy. |
| 70 | `delete-incorrect-migrations.ts` | `scripts/archive/delete-incorrect-migrations.ts` | TypeScript | Removes incorrectly migrated entries from Notion databases. |
| 71 | `extract-legacy.ts` | `scripts/archive/extract-legacy.ts` | TypeScript | Extracts legacy data from old Notion databases for migration. |
| 72 | `find-config-databases.ts` | `scripts/archive/find-config-databases.ts` | TypeScript | Discovers configuration databases in the Notion workspace. |
| 73 | `find-core-dbs.ts` | `scripts/archive/find-core-dbs.ts` | TypeScript | Locates core NOs databases by name/structure. |
| 74 | `find-libros-videos.ts` | `scripts/archive/find-libros-videos.ts` | TypeScript | Searches for book and video entries across Notion databases. |
| 75 | `find-parent-id.ts` | `scripts/archive/find-parent-id.ts` | TypeScript | Finds the parent page ID for a given Notion page. |
| 76 | `find-root-page.ts` | `scripts/archive/find-root-page.ts` | TypeScript | Locates the NOs root page in the Notion workspace. |
| 77 | `fix-phase2-tasks.ts` | `scripts/archive/fix-phase2-tasks.ts` | TypeScript | Fixes task entries created during Phase 2 of migration. |
| 78 | `get-complete-counts.ts` | `scripts/archive/get-complete-counts.ts` | TypeScript | Retrieves complete page counts from all Notion databases. |
| 79 | `map-accessible-notion.ts` | `scripts/archive/map-accessible-notion.ts` | TypeScript | Maps all Notion pages accessible to the integration token. |
| 80 | `map-all-databases.ts` | `scripts/archive/map-all-databases.ts` | TypeScript | Inventories all databases in the Notion workspace. |
| 81 | `map-migration-entries.ts` | `scripts/archive/map-migration-entries.ts` | TypeScript | Maps entries across source and target databases for migration tracking. |
| 82 | `migrate-library.ts` | `scripts/archive/migrate-library.ts` | TypeScript | Migrates library entries to the Knowledge Base (v1). |
| 83 | `migrate-library-v2.ts` | `scripts/archive/migrate-library-v2.ts` | TypeScript | Migrates library entries to the Knowledge Base (v2, improved). |
| 84 | `migrate-phase1.ts` | `scripts/archive/migrate-phase1.ts` | TypeScript | Phase 1 migration: core taxonomy and area structure. |
| 85 | `migrate-phase2.ts` | `scripts/archive/migrate-phase2.ts` | TypeScript | Phase 2 migration: tasks, projects, and entity data. |
| 86 | `migrate-phase3.ts` | `scripts/archive/migrate-phase3.ts` | TypeScript | Phase 3 migration: library, videotheque, and knowledge items. |
| 87 | `migrate-videotheque-v2.ts` | `scripts/archive/migrate-videotheque-v2.ts` | TypeScript | Migrates video collection entries to Knowledge Base (v2). |
| 88 | `nos.py` | `scripts/archive/nos.py` | Python | Legacy Python CLI for NOs operations (Canvas sync, backup). Superseded by `src/index.ts`. |
| 89 | `quick-setup.ts` | `scripts/archive/quick-setup.ts` | TypeScript | Quick one-time setup script for initial Notion database creation. |
| 90 | `search-all-databases.ts` | `scripts/archive/search-all-databases.ts` | TypeScript | Full-text search across all Notion databases. |

---

## Summary by Language

| Language | Active | Archive | Tests | Total |
|----------|--------|---------|-------|-------|
| Python | 10 | 1 | 7 | 18 |
| TypeScript | 10 | 27 | 1 | 38 |
| Shell (bash) | 9 | 0 | 0 | 9 |
| PowerShell | 11 | 0 | 0 | 11 |
| **Total** | **40** | **28** | **8** | **76** |

> Note: Source modules (`src/`) counted as active TypeScript. Dispatch scripts have both
> `.sh` and `.ps1` variants. See `Makefile` for common build/lint/test targets.
