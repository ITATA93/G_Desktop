# Ecosystem Security & Normalization Audit Report  
Scope: 12-project normalization/security health report (2026-02-17 snapshot) + known backlog findings.  
Constraint: **no code changes**.

## Executive Assessment

The ecosystem is in a **high-risk normalization state**: only 5/12 projects are in A-status, 4 are D, and 1 is F. Security-wise, one project (`AG_Consultas`) has hardcoded credentials and is therefore the immediate highest-impact risk despite acceptable overall operational grade. The remaining projects show broad governance and autonomy debt that weakens security posture indirectly (lack of lifecycle control, inconsistent agent behavior, poor auditability).

Current posture is fragmented by design, not isolated incidents. Treat this as a **systemic governance and secret-management failure**.

## High-Confidence Critical Findings

| Finding | Evidence | Severity | Why this is critical |
|---|---|---|---|
| Exposed production credentials in repository | `AG_Consultas\.vscode\settings.json` contains IRIS/SIDRA passwords; same credentials repeated across 5 lines plus 3 legacy scripts | Critical | Immediate confidentiality breach; direct DB compromise risk, lateral movement via reused DB creds, and long-lived credential lifespan |
| Legacy/archived artifact retaining secrets | `_archivo_Mapeo_Anterior_2026-01-30\scripts_anteriores\*.py` includes DB password assignments | Critical | Secret retention outside active code paths defeats ÔÇ£dead codeÔÇØ assumptions and can be reactivated or abused later |
| Secrets embedded in IDE config | Credentials in `.vscode` (not runtime config) | High | IDE settings are commonly shared, synced, and copied; this increases exfiltration probability and accidental disclosure |
| Known unresolved `--dangerously-skip-permissions` in dispatch pipeline (backlog H-01) | explicit backlog item | High | Breaks least-privilege controls and policy enforcement; single-step bypass class vulnerability |
| Known unresolved `eval` in `health-check.sh` (backlog M-01) | explicit backlog item | High | Runtime command injection vector under malformed/untrusted input assumptions |
| Known unresolved input echo of agent responses (backlog H-02) | explicit backlog item | High | Potential credential/tokens/session data leakage and response tampering confidence loss |

## Security Pattern Analysis

1. **Single-source secrets are reused and embedded directly**
   - `AG_Consultas` shows same IRIS password repeated across multiple config lines and scripts (`sd260710sd`), indicating copy/paste propagation and likely environment-wide reuse.
   - Reuse makes containment impossible after one leak and increases blast radius.

2. **No clear secure secret boundary**
   - `.env.example` absent in several projects.
   - `.env` governance and central secret store policy appear inconsistent; this pushes teams toward inline configuration.
   - Missing `.gitignore` coverage in projects increases chance of committing accidental secrets and machine-specific config.

3. **Backlog indicates known exploit paths are deferred**
   - Remaining critical/high backlog items are foundational hardening controls (permissions bypass, unsafe evaluation, auth enforcement, response sanitation).
   - Deferring these while normalizing documents gives a false sense of readiness.

## Systemic Architectural Flaws Affecting Security

## 1) Normalization contract is not operationalized
- Projects do not share a guaranteed baseline.
- Required governance files are absent in 4 D-rated and 2 C-rated projects; optional standards are missing broadly.
- Security controls are therefore de facto project-local and inconsistent; this is architecture-level policy drift.

## 2) Autonomy architecture is incomplete, not enforced
- Most projects lack:
  - `session_protocol`
  - `has_workflows`
  - `subagents_defined`
  - `dispatch_available`
  - `memory_structure`
  - `tasks_awareness`
- This means systems are not reliably self-healing, not consistently discoverable, and not deterministic under incident pressure.

## 3) Task/governance lifecycle is broken in half the stack
- `NO-TASKS` on 6 of 12 projects (plus several partials) means patch tracking and operational state cannot be correlated.
- `devlog_has_entries`, `tasks_unified`, and `changelog_active` gaps impede post-incident retrospectives and vulnerability regression tracking.

## 4) Auditability gaps increase risk of silent reintroduction
- Quality/autonomy are scored, but no enforcement for ÔÇ£must passÔÇØ gates.
- Current state encourages partial remediation that improves score without fixing latent exploit surfaces.

## 5) Security scanning maturity is likely uneven
- Only one project surfaced with 8 critical findings, but known backlog and missing controls suggest incomplete scanning coverage.
- High confidence that more issues exist in D/C projects because required docs are absent and workflows appear incomplete, limiting automated checks and PR gating.

---

## Autonomy Gap Criticality (Normalization Impact)

| Gap | Security Consequence |
|---|---|
| Missing `tasks_awareness` | Security fixes may be unscheduled, duplicated, or dropped. |
| Missing `dispatch_available` | Manual operations dominate; incident response and mitigations are slower/inconsistent. |
| Missing `memory_structure` | No reliable cross-session context; repeated mistakes and missed rollback conditions. |
| Missing `session_protocol` | No standardized incident handling sequence; high variance in operator behavior. |
| Missing `subagents_defined` | No clear ownership boundaries; weak blast containment and accountability. |

---

## Project-Level Risk Snapshot

| Project | Health | Security findings | Governance posture |
|---|---:|---|---|
| AG_Consultas | 48/100 (A) | **8 critical secrets** | Major security debt; optional AGENTS/config missing only; security risk dominates |
| AG_Analizador_RCE | 16/100 (D) | 0 reported | Fails required governance baseline; autonomy/manual posture |
| AG_Hospital | 10/100 (D) | 0 reported | Missing required core files (including README/.gitignore/docs); weak containment |
| AG_SV_Agent | 16/100 (D) | 0 reported | Severe governance debt; manual-only/autonomy absent |
| AG_TrakCare_Explorer | 10/100 (D) | 0 reported | Missing core files and `.gitignore`; high operational risk |
| AG_SD_Plantilla | 36/100 (C) | 0 reported | Partial governance; no devlog/tasks/changelog readiness |
| AG_Notebook | 36/100 (C) | 0 reported | Missing required docs; manual-only posture |
| Others (A-group) | 88/100 | 0 reported | Better posture but still autonomy gap (`tasks_awareness`) and AGENTS inconsistencies |

---

## Recommended Normalization Strategy (Non-Code, Process-Control Focus)

## Phase 0 ÔÇö Immediate Containment (0ÔÇô7 days, P0/P1)
1. Rotate and revoke exposed credentials in `AG_Consultas` immediately.
2. Remove all hardcoded secrets from tracked files and backup folders.
3. Add emergency secret-fix policy: no commit containing password-like patterns or DB URI credentials.
4. Block production execution paths from using `--dangerously-skip-permissions`.
5. Patch `health-check.sh` and `agent_service.py` according to backlog priorities.

## Phase 1 ÔÇö Baseline Enforcement (1ÔÇô3 weeks)
1. Define and version-control a mandatory `ecosystem project contract` of required files and sections.
2. Enforce required-file checks in CI for all projects (new PR fails if missing).
3. Enforce secret scanning + `gitignore`/env policy checks uniformly across all 12 repositories.
4. Standardize `.env` handling: template-only `.env.example`, no secrets in repository paths like `.vscode`, backups, or docs.

## Phase 2 ÔÇö Autonomy Recovery (3ÔÇô6 weeks)
1. Implement workflow + dispatch + memory + subagent skeleton in every project.
2. Normalize task awareness by integrating unified task schemas and requiring `docs/TASKS.md` + update cycle.
3. Require session protocol + changelog + devlog per change.
4. Introduce periodic ÔÇ£security posture sweepÔÇØ against all projects, not just critical ones.

## Phase 3 ÔÇö Verification & Regression Control (6+ weeks)
1. Quarterly normalization audit with same scoring rubric and enforced remediation SLA.
2. Security regression gates: any new critical finding blocks deployment.
3. Annual purge policy for historical/backups containing secrets.
4. Separate security baseline from code quality baseline, but gate both.

## Highest-Priority Remediation Order (Risk-Ordered)

1. AG_Consultas credential exfiltration chain (P0).
2. `--dangerously-skip-permissions`, `eval`, and response echo backlog items (P0).
3. `AG_Hospital`, `AG_TrakCare_Explorer`, `AG_SV_Agent`, `AG_Analizador_RCE` normalization to restore minimum required contract (P1).
4. Remaining C/D projects to A-grade baseline and full autonomy controls (P2).

## Final Judgment

This is not a ÔÇ£few weak spotsÔÇØ issue. The ecosystem shows a **governance decomposition pattern** where some projects are operationally functional but security-unreliable, while others are both insecure and un-governed. The highest immediate risk is active credential exposure; the highest strategic risk is that only a minority of projects satisfy mandatory structure, making repeatable security enforcement impossible without hardening normalization as an enforced platform contract.
