# Ecosystem Deep Review â€” Pre-Upgrade Audit

**Date**: 2026-02-07
**Auditor**: Antigravity Architect
**Scope**: All 8 AG projects in `C:\_Repositorio\AG_Proyectos`
**Objective**: Identify what each project needs before propagating Opus 4.6 improvements

---

## 1. Executive Summary

| #   | Project                         | Type           | GEMINI.md         | CLAUDE.md             | .subagents/ | Hygiene               | Priority |
| --- | ------------------------------- | -------------- | ----------------- | --------------------- | ----------- | --------------------- | -------- |
| 1   | **AG_Notebook**                 | Hub Central    | âš ï¸ v2.0 (outdated) | âš ï¸ v2.0 (generic)      | âœ… Has       | âš ï¸ Legacy files        | ðŸ”´ HIGH   |
| 2   | **AG_Hospital_Organizador**     | SAIA Engine    | âš ï¸ v2.0 (outdated) | âš ï¸ v2.0 (generic copy) | âœ… Has       | ðŸ”´ Dirty root          | ðŸ”´ HIGH   |
| 3   | **AG_DeepResearch_Salud_Chile** | Research CLI   | âš ï¸ v2.0 (outdated) | âœ… Has (custom)        | âœ… Has       | âš ï¸ Debug files in root | ðŸŸ¡ MEDIUM |
| 4   | **AG_SD_Plantilla**             | Chile Template | âœ… Custom (domain) | âœ… Has (custom)        | âœ… Has       | âœ… Clean               | ðŸŸ¢ LOW    |
| 5   | **AG_SV_Agent**                 | Infra Hub      | âœ… Custom (domain) | âŒ Missing             | âŒ Missing   | âš ï¸ NUL file, root MD   | ðŸŸ¡ MEDIUM |
| 6   | **AG_Analizador_RCE**           | Data CLI       | âœ… Custom (domain) | âŒ Missing             | âŒ Missing   | âœ… Clean               | ðŸŸ¢ LOW    |
| 7   | **AG_Consultas**                | SQL Mapping    | âœ… Custom (domain) | âŒ Missing             | âŒ Missing   | âš ï¸ nul, debug_sync.log | ðŸŸ¡ MEDIUM |
| 8   | **AG_NB_Apps**                  | NocoBase Mgmt  | âŒ Missing         | âŒ Missing             | âŒ Missing   | ðŸ”´ Very dirty root     | ðŸ”´ HIGH   |

---

## 2. Per-Project Findings

### 2.1 AG_Notebook (Hub Central) â€” ðŸ”´ HIGH PRIORITY

**Role**: Central workspace and origin of all AG templates/profiles.

**GEMINI.md Issues**:
- âŒ Claude described as "Task tool, paralelizaciÃ³n, MCP" (old v2.0)
- âŒ Codex described as "Degradado" (should be "Casi Full")
- âŒ No effort mapping in classifier
- âŒ No Agent Teams section
- âŒ Missing NIVEL 3 Agent Teams parallel option

**CLAUDE.md Issues**:
- âš ï¸ Generic workspace copy (not customized for Hub role)
- âŒ No Opus 4.6 commands (/team-review, /insights-review)
- âŒ No Context Management section
- âŒ No effort controls documentation
- âŒ "6 sub-agentes" should be "7" (missing researcher)

**_global-profile/GEMINI.md**: Same outdated v2.0 content (needs sync).
**_template/workspace/GEMINI.md**: Same outdated v2.0 content (needs sync).

**Hygiene Issues**:
- âš ï¸ `CLAUDE_LEGACY.md` (2190 bytes) â€” legacy file, should archive
- âš ï¸ `GEMINI_LEGACY.md` (3025 bytes) â€” legacy file, should archive
- âš ï¸ `MIGRATION_REPORT.md` in root â€” should move to `docs/audit/`
- âš ï¸ `genesis_files.json` (60KB), `ia_alfred_files.json` (42KB), `wsls_files.json` (65KB) â€” large JSON files in root
- âœ… Has `.subagents/`, `.agent/`, good base structure

**Recommended Actions**:
1. Update GEMINI.md with Opus 4.6 (vendor table, classifier, Agent Teams)
2. Update CLAUDE.md with new commands and Context Management
3. Sync `_global-profile/GEMINI.md` and `_template/workspace/GEMINI.md`
4. Move legacy `.md` files to `docs/audit/` or archive
5. Move large JSON files to `_resources/` or `data/`

---

### 2.2 AG_Hospital_Organizador (SAIA) â€” ðŸ”´ HIGH PRIORITY

**Role**: Hospital document organization system (SAIA engine).

**GEMINI.md Issues**:
- âŒ Exact generic copy from template â€” NOT customized for SAIA purpose
- âŒ Same outdated vendor table (v2.0)
- âŒ No project-specific identity section
- âŒ Title still says "Profile Global de Antigravity" (not project-specific)

**CLAUDE.md Issues**:
- âŒ Exact generic copy from AG_Notebook â€” NOT customized
- âŒ "This workspace is for configuration management" â€” WRONG for this project
- âŒ References `_global-profile/` and `_template/` which don't apply here
- âŒ No Opus 4.6 features

**Hygiene Issues** (SEVERE):
- ðŸ”´ `debug_planner.py` (505 bytes) in root â€” move to `scripts/temp/`
- ðŸ”´ `saia_cli.py` (3868 bytes) in root â€” should be in `src/`
- ðŸ”´ `migration_proposal.yaml` (5MB!) in root â€” should be in `docs/plans/` or `_resources/`
- ðŸ”´ `install-global.ps1`, `install-global.sh` in root â€” belong in `scripts/`
- ðŸ”´ `UPDATE_TASKS.md` in root â€” should be `docs/TASKS.md`
- âš ï¸ `_Audit/` and `_Estructura_Final_SAIA/` dirs â€” non-standard naming
- âš ï¸ `scandata/` dir â€” should be in `data/`

**Recommended Actions**:
1. Rewrite GEMINI.md with SAIA-specific identity and purpose
2. Rewrite CLAUDE.md with SAIA-specific context
3. Clean root: move files to proper directories
4. Rename non-standard dirs to AG conventions
5. Update with Opus 4.6 vendor information

---

### 2.3 AG_DeepResearch_Salud_Chile â€” ðŸŸ¡ MEDIUM PRIORITY

**Role**: Deep Research CLI for Chilean health normative auditing.

**GEMINI.md Issues**:
- âŒ Generic copy â€” NOT customized for Deep Research purpose
- âŒ Same outdated vendor table (v2.0)
- âŒ Title says "Profile Global de Antigravity"

**CLAUDE.md**: âœ… Has custom content (8012 bytes, same as Hub template)

**Hygiene Issues**:
- âš ï¸ `debug_ddgs.py` (557 bytes) in root â€” move to `scripts/temp/`
- âš ï¸ `debug_search.py` (531 bytes) in root â€” move to `scripts/temp/`
- âš ï¸ `codex_output.txt` (2124 bytes) in root â€” move to `logs/`
- âš ï¸ `research_results.txt` (2040 bytes) in root â€” move to `data/`
- âš ï¸ `install-global.ps1`, `install-global.sh` in root â€” belong in `scripts/`
- âš ï¸ `TASKS.md` in root â€” should be `docs/TASKS.md`
- âœ… Has `.subagents/`, `.agent/`, `.codex/` â€” good tooling setup

**Recommended Actions**:
1. Rewrite GEMINI.md with DeepResearch-specific identity
2. Update vendor table and classifier with Opus 4.6
3. Move debug/temp files out of root
4. Move TASKS.md to docs/

---

### 2.4 AG_SD_Plantilla â€” ðŸŸ¢ LOW PRIORITY

**Role**: Template for Chilean digital government apps.

**GEMINI.md**: âœ… Fully custom (334 lines, domain-specific, excellent quality)
**CLAUDE.md**: âœ… Has custom content (11197 bytes)

**Structure**: âœ… Clean â€” `.subagents/`, well-organized

**Issues**:
- âš ï¸ `MIGRATION_SUMMARY.md`, `NEXT_STEPS.md`, `USO_AUTONOMO.md` in root â€” borderline, but acceptable for template project
- âš ï¸ No Opus 4.6 vendor information (but this project has its own domain-specific GEMINI.md, so not directly applicable)
- âš ï¸ Missing `.agent/`, `.gemini/`, `.codex/` directories
- âš ï¸ Missing `CHANGELOG.md` version header (has v1.0.0 inline)

**Recommended Actions**:
1. Add Opus 4.6 note to CLAUDE.md if it references vendors
2. No major changes needed â€” this is a domain-specific template

---

### 2.5 AG_SV_Agent â€” ðŸŸ¡ MEDIUM PRIORITY

**Role**: Multi-agent infrastructure orchestration hub.

**GEMINI.md**: âœ… Excellent custom content (321 lines, domain-specific, well-structured)
**CLAUDE.md**: âŒ Missing entirely

**Structure Issues**:
- âŒ No `.subagents/manifest.json` â€” agents defined in `agents/` and `config/agents.yaml` instead
- âŒ No `.agent/` directory (rules/workflows)

**Hygiene Issues**:
- âš ï¸ `NUL` file (75 bytes) in root â€” Windows artifact, delete
- âš ï¸ `EXECUTION_REPORT_FINAL.md` in root â€” move to `reports/`
- âš ï¸ `SV_Promox.code-workspace` â€” typo in name ("Promox" â†’ "Proxmox")
- âš ï¸ `CONTEXT_GEMINI_3.0.md` (15KB) in root â€” acceptable (context file)
- âš ï¸ Orchestrator uses `claude-opus-4-5` (line 14) â€” should update to `opus-4.6`

**Recommended Actions**:
1. Create CLAUDE.md with project-specific context
2. Delete NUL file
3. Move EXECUTION_REPORT_FINAL.md to reports/
4. Fix workspace file name typo
5. Update model reference from `opus-4-5` to `opus-4.6`

---

### 2.6 AG_Analizador_RCE â€” ðŸŸ¢ LOW PRIORITY

**Role**: Offline clinical data analyzer (CSV â†’ Reports).

**GEMINI.md**: âœ… Excellent custom content (281 lines, domain-specific)
**CLAUDE.md**: âŒ Missing (but has 10 Claude Skills in `.claude/settings.json`)

**Structure**: âœ… Mostly clean â€” proper `data/`, `output/`, `config/` separation

**Issues**:
- âŒ No tests (acknowledged in GEMINI.md as "Ãrea de mejora futura")
- âŒ No `.subagents/`, `.agent/` directories
- âŒ No CLAUDE.md to document the 10 Claude Skills
- âš ï¸ Missing `.gemini/` directory
- âœ… Security: `.gitignore` properly excludes CSVs and outputs

**Recommended Actions**:
1. Create CLAUDE.md documenting the 10 Claude Skills
2. No urgent Opus 4.6 changes needed (domain-specific GEMINI.md)

---

### 2.7 AG_Consultas â€” ðŸŸ¡ MEDIUM PRIORITY

**Role**: SQL mapping and query system for TrakCare/ALMA.

**GEMINI.md**: âœ… Custom content (130 lines, domain-specific)
**CLAUDE.md**: âŒ Missing (but has Claude agents in `.claude/agents/`)

**Hygiene Issues**:
- ðŸ”´ `nul` file in root â€” Windows artifact, delete
- âš ï¸ `debug_sync.log` (15KB) in root â€” should be in `logs/`
- âš ï¸ `.clauderc` (4586 bytes) in root â€” legacy config
- âš ï¸ `AG_Consultas.code-workspace` â€” acceptable

**Recommended Actions**:
1. Delete `nul` file
2. Move `debug_sync.log` to `logs/` or delete
3. Create CLAUDE.md documenting the 3 Claude agents
4. Evaluate if `.clauderc` should be migrated to `.claude/settings.json`

---

### 2.8 AG_NB_Apps â€” ðŸ”´ HIGH PRIORITY

**Role**: NocoBase management scripts and apps.

**GEMINI.md**: âŒ Missing entirely
**CLAUDE.md**: âŒ Missing entirely
**CHANGELOG.md**: âŒ Missing

**Hygiene Issues** (SEVERE):
- ðŸ”´ No GEMINI.md â€” agent has NO context about this project
- ðŸ”´ `route_names.txt`, `routes_dump.txt` in root â€” move to `data/` or `logs/`
- ðŸ”´ `schema_onco_casos.txt`, `schema_schedule.txt` in root â€” move to `docs/` or `data/`
- ðŸ”´ `validation_debug.txt`, `validation_output.txt`, `validation_output_utf8.txt` in root â€” move to `logs/`
- ðŸ”´ `AGENT_START_PROMPT.md`, `CONTRIBUTING.md`, `VALIDATION_SUMMARY.md` in root â€” review placement
- âš ï¸ `NB_Apps.code-workspace` â€” legacy name (not AG_ prefixed)
- âš ï¸ `MIRA/` directory â€” non-standard name (clinical management module)
- âœ… Has `package.json`, `tsconfig.json`, `node_modules/` â€” Node.js project

**Recommended Actions**:
1. Create GEMINI.md with NocoBase-specific identity
2. Create CLAUDE.md with API management context
3. Create CHANGELOG.md
4. Clean root: move all .txt files to appropriate dirs
5. Rename workspace file to AG_NB_Apps.code-workspace

---

## 3. Cross-Cutting Issues

### 3.1 GEMINI.md Versions

| Version                 | Projects                                                      | Description                                                 |
| ----------------------- | ------------------------------------------------------------- | ----------------------------------------------------------- |
| **v2.0 (generic)**      | AG_Notebook, AG_Hospital_Organizador, AG_DeepResearch         | Outdated vendor table, no effort mapping, Codex "Degradado" |
| **v3.0 (AG_Plantilla)** | AG_Plantilla only                                             | Updated with Opus 4.6, Agent Teams, effort mapping          |
| **Custom (domain)**     | AG_SV_Agent, AG_Analizador_RCE, AG_Consultas, AG_SD_Plantilla | Project-specific, no vendor table to update                 |

### 3.2 CLAUDE.md Status

| Status            | Projects                                                 |
| ----------------- | -------------------------------------------------------- |
| **Has + Updated** | AG_Plantilla (reference)                                 |
| **Has + Generic** | AG_Notebook, AG_Hospital_Organizador                     |
| **Has + Custom**  | AG_DeepResearch, AG_SD_Plantilla                         |
| **Missing**       | AG_SV_Agent, AG_Analizador_RCE, AG_Consultas, AG_NB_Apps |

### 3.3 Root Hygiene Score

| Score           | Projects                                                       |
| --------------- | -------------------------------------------------------------- |
| âœ… Clean         | AG_SD_Plantilla, AG_Analizador_RCE                             |
| âš ï¸ Minor issues  | AG_Notebook, AG_DeepResearch                                   |
| ðŸ”´ Needs cleanup | AG_Hospital_Organizador, AG_SV_Agent, AG_Consultas, AG_NB_Apps |

---

## 4. Recommended Execution Order

### Phase 1: Critical (Hub + Dirty Projects)
1. **AG_Notebook** â€” Update GEMINI.md v3.0, sync _global-profile and _template
2. **AG_NB_Apps** â€” Create GEMINI.md and CLAUDE.md from scratch
3. **AG_Hospital_Organizador** â€” Rewrite GEMINI.md with SAIA identity, clean root

### Phase 2: Medium (Vendor Updates + Cleanup)
4. **AG_DeepResearch** â€” Update GEMINI.md vendor section, clean debug files
5. **AG_SV_Agent** â€” Create CLAUDE.md, clean root, update model reference
6. **AG_Consultas** â€” Create CLAUDE.md, clean root

### Phase 3: Polish (Already Good)
7. **AG_Analizador_RCE** â€” Create CLAUDE.md (optional)
8. **AG_SD_Plantilla** â€” Minor Opus 4.6 notes (optional)

---

## 5. Metrics

- **Total projects reviewed**: 8
- **GEMINI.md missing**: 1 (AG_NB_Apps)
- **CLAUDE.md missing**: 4 (AG_SV_Agent, AG_Analizador_RCE, AG_Consultas, AG_NB_Apps)
- **Outdated vendor tables**: 3 (AG_Notebook, AG_Hospital_Organizador, AG_DeepResearch)
- **Root hygiene violations**: 20+ files across 4 projects
- **Estimated effort**: 2-3 hours for Phases 1-2, <30 min for Phase 3

---

**Status**: REVIEW COMPLETE â€” Awaiting approval to proceed
