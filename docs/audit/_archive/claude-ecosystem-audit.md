I now have complete data. Here is the comprehensive audit report.

---

# Antigravity Ecosystem ÔÇö Normalization & Security Audit Report

**Date**: 2026-02-20
**Auditor**: Senior Ecosystem Architect (Claude Opus 4.6)
**Scope**: 12 AG projects, 1 orchestrator, 3 organizational domains
**Ecosystem Average Health**: **51/100** (Critical threshold)

---

## 1. Executive Summary

The Antigravity ecosystem is in a **structurally fragile state**. While 5 of 12 projects achieve A-grade normalization, the remaining 7 projects have compounding deficiencies that create systemic risk. One project (AG_Consultas) is actively leaking production database credentials. Four projects are D-grade with near-zero autonomy infrastructure. The orchestrator itself has deleted its CI/CD pipelines and uses `--no-verify` in automated commits, creating a governance enforcement vacuum.

**Headline numbers**:
- **8 CRITICAL** credential exposures (AG_Consultas ÔÇö unresolved)
- **4 backlog security items** remain open from the 2026-02-17 remediation session
- **26 missing required files** across the ecosystem
- **6/12 projects** have no task management system (NO-TASKS)
- **5/12 projects** operate in fully manual mode (no dispatch, no session protocol, no memory)
- **CI/CD deleted** from the orchestrator ÔÇö zero automated enforcement gates

---

## 2. Critical Security Findings

### 2.1 AG_Consultas: Active Credential Exposure (SEVERITY: CRITICAL)

**This is the single highest-risk item in the ecosystem.** AG_Consultas has 8 instances of hardcoded production database passwords across two vectors:

| Vector | File | Credential | Instances |
|--------|------|-----------|-----------|
| IDE config | `.vscode/settings.json` | IRIS password `sd260710sd` | 4 |
| IDE config | `.vscode/settings.json` | SIDRA password `hkEVC9AFVjFeRTkp` | 1 |
| Legacy archive | `_archivo_*/scripts_anteriores/*.py` | IRIS password `sd260710sd` | 3 |

**Why this is worse than it appears**:

1. **`.vscode/settings.json` is a collaboration vector.** This file is designed to be shared across team environments. If AG_Consultas is ever onboarded to a second developer, the credentials propagate automatically.

2. **The "archive" directory creates false safety.** The `_archivo_Mapeo_Anterior_2026-01-30/` directory signals "old, inert code." But the credentials inside are **the same active production passwords** ÔÇö `sd260710sd` appears identically in both the archive and the current IDE config. A directory rename does not deactivate a password.

3. **The audit scanner's own SKIP_DIRS includes `"tests"` and `"temp"`** (`audit_ecosystem.py:156-169`). While this reduces false positives, it means any credentials that migrate into test fixtures or temp scripts become invisible to the scanner. The scanner also skips `community/` third-party code ÔÇö a known supply-chain attack surface.

4. **Blast radius**: These passwords provide direct database access to IRIS (clinical/hospital system, user `18233087-6`) and SIDRA (SQL Server, user `sidra`). Compromise of either grants access to **medical records infrastructure**.

**Verdict**: Credential rotation for both IRIS and SIDRA should have been executed on 2026-02-17 when the exposure was first identified. The 3-day gap since discovery without rotation is itself a finding.

### 2.2 Backlog Items: 4 Open Security Findings (SEVERITY: HIGH)

The 2026-02-17 session identified 13 security findings, fixed 12, and explicitly deferred 4 to backlog. All 4 remain open:

| ID | Finding | Location | Risk |
|----|---------|----------|------|
| H-01 | `--dangerously-skip-permissions` in dispatch | AG_Plantilla `.subagents/dispatch.sh:L197,215` | Agent runs with zero permission gates; combined with prompt injection = arbitrary filesystem ops |
| H-02 | Agent response reflects user input | AG_Plantilla `agent_service.py:L84` | Data echo enables reflected XSS, credential leakage in logs |
| M-01 | `eval` in health-check.sh | AG_Plantilla `scripts/setup/health-check.sh:L38` | Command injection if check conditions ever become dynamic |
| M-02 | API auth bypassed in development mode | AG_Plantilla `src/main.py:L49` | Dev server exposed on network = unauthenticated API access |

**Critical observation**: H-01 and the dispatch prompt injection vulnerability (C-01, already partially remediated in AG_Orquesta's `dispatch.ps1` with stochastic boundaries) form a **compound attack chain**. The AG_Orquesta dispatcher now wraps user input in `<user_task_{guid}>` tags and sanitizes embedded tags (`dispatch.ps1:86-91`). But **AG_Plantilla's `dispatch.sh` still uses raw concatenation** (`FULL_PROMPT="$INSTRUCTIONS\n---\nTask: $PROMPT"`), and combined with `--dangerously-skip-permissions`, this means: injected prompt ÔåÆ full filesystem access ÔåÆ credential exfiltration.

### 2.3 `--no-verify` in Automated Scripts (SEVERITY: HIGH)

Three scripts in the orchestrator bypass pre-commit hooks:

| File | Line | Context |
|------|------|---------|
| `scripts/audit_ecosystem.py` | 329 | Auto-fix commit: `git commit --no-verify` |
| `scripts/propagate.py` | 186 | Template sync commit: `git commit --no-verify` |
| `scripts/temp/commit_satellites.py` | 12 | Satellite normalization: `git commit --no-verify` |

The pre-commit config includes `detect-private-key` and `check-added-large-files` hooks. Using `--no-verify` on automated commits means **the exact scripts that propagate files across the ecosystem bypass the security hooks designed to catch credential leaks during propagation**. This is a self-defeating pattern: the audit tool's auto-fix mode can commit credentials because it skips the credential-detection hooks.

### 2.4 CI/CD Deletion (SEVERITY: HIGH)

Both `.github/workflows/ci.yml` and `.github/workflows/security.yml` are marked as **deleted** in git status. The orchestrator ÔÇö the central governance hub ÔÇö has no automated enforcement. This means:

- No automated credential scanning on push
- No automated normalization checks on PR
- No security scanning pipeline
- All enforcement relies on manual execution of `audit_ecosystem.py`

---

## 3. Systemic Architectural Flaws

### 3.1 The Normalization Contract is Declarative, Not Enforced

The ecosystem defines a clear normalization standard: 7 required files, 7 recommended files, structured task management, session protocols, and content quality gates. The tooling to audit this (`audit_ecosystem.py`, `cross_task.py`) exists and is well-built.

**But there is no enforcement mechanism.** The contract is aspirational:

- No CI/CD runs the audit on commit or PR
- No pre-commit hook validates normalization
- The `--fix` mode auto-creates files but commits them with `--no-verify`
- Projects can remain D-grade indefinitely with zero consequence

**Result**: 5 projects achieved A-grade because their maintainers actively adopted the standard. The other 7 didn't because nothing forced them to. This is a governance architecture failure, not a documentation failure.

### 3.2 Bimodal Ecosystem: "Normalized" vs. "Abandoned"

The health distribution reveals a stark bimodal split:

```
88-100: ÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûê  5 projects (A-grade)
36-48:  ÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûê              3 projects (B/C-grade)
10-16:  ÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûê          4 projects (D/F-grade)
```

There is no middle ground ÔÇö projects either have full infrastructure (88+ health) or nearly none (10-16 health). This indicates the normalization effort was applied as a batch operation to willing projects, rather than being structurally embedded in project creation.

The 4 lowest-scoring projects share identical gaps:

| Project | Health | Missing Everything |
|---------|--------|--------------------|
| AG_Hospital | 10 | No gitignore, no README, no docs, no GEMINI, no CLAUDE, no agents, no dispatch, no session protocol, no memory |
| AG_TrakCare_Explorer | 10 | Same profile |
| AG_Analizador_RCE | 16 | All autonomy at 0/6 |
| AG_SV_Agent | 16 | All autonomy at 0/6 |

**These projects exist outside the governance system entirely.** They have git repos but no agent infrastructure, no task tracking, no session continuity. Any work done in these projects has no audit trail and no cross-project visibility.

### 3.3 Task Management Fragmentation

**6 of 12 projects have NO-TASKS** ÔÇö they lack a `docs/TASKS.md` with the unified Incoming/Outgoing/Completed structure. The `cross_task.py` system is designed to delegate tasks across projects, but it cannot delegate to a project that has no task intake structure.

This creates a **dead-letter problem**: the orchestrator can issue normalization tasks (via `send_norm_tasks.py`), but half the projects have no inbox to receive them. The cross-task system's `stale` detection will flag these tasks as overdue, but there's no mechanism to force resolution.

### 3.4 Environment Resolution Fragility

`env_resolver.py` has a fallback path (`audit_ecosystem.py:40-53`) that defaults to `C:\_Repositorio` when the resolver can't be imported. The active environment is `desktop` with base path `W:\Antigravity_OS`. This means:

- If `audit_ecosystem.py` is run without `env_resolver` in the Python path (e.g., from a fresh shell, a CI runner, or a different machine), it scans the wrong directory tree entirely
- The audit would report zero projects and zero findings ÔÇö a **false-negative silence** that looks like a clean bill of health

### 3.5 Scanner Blind Spots

The security scanner in `audit_ecosystem.py` has intentional exclusions that create exploitable gaps:

| Exclusion | Rationale | Risk |
|-----------|-----------|------|
| `SKIP_DIRS: "tests"` | Avoid test dummy passwords | Real credentials in test fixtures invisible |
| `SKIP_DIRS: "temp"` | Audit tooling directory | Scripts in `scripts/temp/` with passwords unscanned |
| `SKIP_DIRS: "community"` | Third-party code | Supply-chain injected credentials invisible |
| `SCAN_EXTENSIONS` whitelist | Performance | `.sh`, `.ps1`, `.md`, `.txt` files never scanned |
| `SAFE_LINE_PATTERNS: "^\s*#"` | Skip comments | `# password: realpassword123` would be skipped |
| `SAFE_LINE_PATTERNS: _template` | Template files | Any file with `_template` in path is immune |

Most critically: **`.sh` and `.ps1` files are not in SCAN_EXTENSIONS.** The `--dangerously-skip-permissions` flags, hardcoded paths, and the `eval` vulnerability all live in shell/PowerShell scripts that the scanner will never examine.

---

## 4. Autonomy Architecture Analysis

### 4.1 The Autonomy Spectrum

The audit measures 6 autonomy dimensions per project. The ecosystem breaks down as:

| Autonomy Level | Projects | Characteristics |
|----------------|----------|-----------------|
| **Auto (5-6/6)** | 5 | Full agent infrastructure; can self-heal, track work, maintain memory |
| **Semi (3-4/6)** | 0 | ÔÇö (no projects occupy this middle ground) |
| **Manual (0-2/6)** | 7 | No dispatch, no session protocol, no memory; agents start from zero every session |

The same bimodal split from section 3.2 appears here. There are no "partially autonomous" projects. This indicates the autonomy infrastructure is an all-or-nothing package (likely propagated from AG_Plantilla's `_template/`), not a modular system where projects can adopt individual capabilities incrementally.

### 4.2 The `tasks_awareness` Gap

**11 of 12 projects** fail the `tasks_awareness` check, which requires GEMINI.md to reference "tasks". This is the single most pervasive autonomy gap. Without it, AI agents working in a project don't know to check `docs/TASKS.md` at session start ÔÇö meaning:

- Cross-project delegated tasks are never picked up
- Session protocol step 1 ("Read TASKS.md") has no trigger in the agent's instruction file
- The entire cross-task orchestration system is effectively disabled at the leaf level

### 4.3 `gemini_keywords` Quality Gate

**10 of 12 projects** fail the `gemini_keywords` content quality check (GEMINI.md must contain 3+ of: "absolute rules", "complexity", "sub-agent", "commit"). This suggests either:
- GEMINI.md files were created as stubs during batch normalization
- The keyword list represents the AG_Plantilla standard but was never propagated as content

Either way, the result is the same: agents operating in 10/12 projects lack the governance instructions that constrain their behavior. The "absolute rules" keyword is particularly concerning ÔÇö its absence means agents may not be bound to the "never create files in root" and "never commit secrets" directives.

---

## 5. Orchestrator Self-Assessment

### 5.1 AG_Orquesta Itself

The orchestrator has solid tooling (`cross_task.py`, `audit_ecosystem.py`, `env_resolver.py`, multi-vendor dispatch with prompt injection mitigation). However:

- **CI/CD deleted**: No automated enforcement
- **Branch divergence**: Working on `master` but main branch is `main` ÔÇö unclear merge strategy
- **Untracked audit files**: `docs/audit/claude-ecosystem-audit.md`, `codex-ecosystem-audit.md`, `gemini-ecosystem-audit.md` are untracked ÔÇö audit history is not version-controlled
- **`scripts/temp/` accumulation**: 8 files in `scripts/temp/` including `audit_prompt.txt`, `consensus_prompt.txt` ÔÇö operational detritus that should be committed or purged
- **dispatch.ps1 remediated but dispatch.sh not verified**: The PowerShell dispatcher has stochastic boundaries; the Bash dispatcher's state in AG_Plantilla is unknown from this scope

### 5.2 Workspace Registry Drift

`project_registry.json` lists 13 projects (including AG_Plantilla and AG_Orquesta). The audit scans 12 projects. AG_Plantilla is excluded from the audit but is the source of template propagation and contains the 4 open security backlog items. **The template project is exempt from the audit it generates.** This is a governance blind spot ÔÇö the most security-critical project (it defines the dispatch scripts, API config, and all default security patterns) is never audited by the ecosystem scanner.

---

## 6. Prioritized Remediation Roadmap

### Phase 0: Emergency (0-48 hours)

| # | Action | Target | Rationale |
|---|--------|--------|-----------|
| 1 | **Rotate IRIS password** (`sd260710sd`) | IRIS DB infrastructure | Exposed 3+ days; hospital system access |
| 2 | **Rotate SIDRA password** (`hkEVC9AFVjFeRTkp`) | SIDRA SQL Server | Exposed across 2 projects even after partial remediation |
| 3 | **Remove `.vscode/settings.json` from AG_Consultas git tracking** | AG_Consultas | `git rm --cached .vscode/settings.json` + add to `.gitignore` |
| 4 | **Delete `_archivo_Mapeo_Anterior_2026-01-30/`** | AG_Consultas | Dead code containing live credentials |

### Phase 1: Structural Security (1-2 weeks)

| # | Action | Target | Rationale |
|---|--------|--------|-----------|
| 5 | Remove `--dangerously-skip-permissions` from AG_Plantilla dispatch scripts | AG_Plantilla | H-01: blocks compound attack chain |
| 6 | Remove `--no-verify` from all automated commit scripts | AG_Orquesta | Restores pre-commit hook enforcement |
| 7 | Add `.sh` and `.ps1` to `SCAN_EXTENSIONS` in `audit_ecosystem.py` | AG_Orquesta | Closes scanner blind spot on shell scripts |
| 8 | Restore CI/CD pipelines (`.github/workflows/`) | AG_Orquesta | Reestablish automated enforcement gates |
| 9 | Include AG_Plantilla in the ecosystem audit scope | AG_Orquesta | Template project must not be exempt |

### Phase 2: Normalization Enforcement (2-4 weeks)

| # | Action | Target | Rationale |
|---|--------|--------|-----------|
| 10 | Propagate GEMINI.md with full governance keywords to all 12 projects | Ecosystem-wide | Closes `gemini_keywords` gap (10/12 projects) |
| 11 | Add `tasks_awareness` block to all GEMINI.md files | Ecosystem-wide | Enables cross-task delegation (11/12 projects) |
| 12 | Run `cross_task.py normalize` for 4 D-grade projects | AG_Hospital, AG_TrakCare_Explorer, AG_Analizador_RCE, AG_SV_Agent | Bootstraps minimum governance |
| 13 | Create pre-commit hook for credential scanning (beyond `detect-private-key`) | AG_Plantilla template | Catches known credential patterns at commit time |
| 14 | Fix env_resolver fallback to fail loudly instead of scanning wrong directory | AG_Orquesta | Prevents false-negative audit silence |

### Phase 3: Autonomy Recovery (4-8 weeks)

| # | Action | Target | Rationale |
|---|--------|--------|-----------|
| 15 | Deploy session-protocol + dispatch to 7 manual-mode projects | 7 projects | Enables self-healing, audit-trail, cross-session memory |
| 16 | Implement `--fix` mode as CI step (not manual invocation) | AG_Orquesta CI | Makes normalization continuous, not episodic |
| 17 | Quarterly credential rotation policy + audit cycle | Ecosystem governance | Prevents 3-day exposure gaps from recurring |

---

## 7. Systemic Recommendations

1. **Shift from "audit and fix" to "prevent and enforce."** The current model discovers problems after the fact. Pre-commit hooks, CI gates, and template-time enforcement would prevent D-grade projects from ever existing.

2. **Eliminate the bimodal split.** The all-or-nothing autonomy package should be decomposed into incremental modules. A project should be able to adopt task management without needing a full dispatch pipeline.

3. **Audit the auditor.** AG_Plantilla generates the security patterns, dispatch scripts, and default configurations for the entire ecosystem, yet it is excluded from the ecosystem audit. This is the single most important coverage gap to close.

4. **Version-control audit artifacts.** The three audit reports (`claude-ecosystem-audit.md`, `codex-ecosystem-audit.md`, `gemini-ecosystem-audit.md`) sitting as untracked files represent institutional knowledge at risk of loss.

5. **Treat `.vscode/` as untrusted.** Add `.vscode/` to the global `.gitignore` template in AG_Plantilla. IDE configuration files are a recurring credential vector across this ecosystem.

---

**End of Report**

*Generated by Master Orchestrator ÔÇö AG_Orquesta_Desk, 2026-02-20*
