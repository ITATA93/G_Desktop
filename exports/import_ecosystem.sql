-- ==========================================================================
-- import_ecosystem.sql — AG_Orquesta ecosystem data for GEN_OS PostgreSQL
-- Generated: 2026-02-22
-- Source: AG_Orquesta_Desk deep research + manifest + project registry
--
-- Run: psql -d antigravity -f exports/import_ecosystem.sql
-- Or:  docker exec postgres psql -U admin -d antigravity -f /tmp/import.sql
-- ==========================================================================

BEGIN;

-- ============================================================================
-- 1. Projects — Full AG_* ecosystem (15 projects)
-- ============================================================================
INSERT INTO projects (id, name, type, path, domain, status, phase, metadata) VALUES
  ('ag-orquesta', 'AG_Orquesta_Desk', 'orchestrator', 'W:\Antigravity_OS\00_CORE\AG_Orquesta_Desk', '00_CORE', 'active', 3,
   '{"description": "Master Orchestrator — cross-project coordination, audit, template propagation", "role": "master-orchestrator", "cli_tools": ["claude", "gemini", "codex"], "agents": 7, "teams": 4}'),
  ('ag-plantilla', 'AG_Plantilla', 'template', 'W:\Antigravity_OS\00_CORE\AG_Plantilla', '00_CORE', 'active', 2,
   '{"description": "Master standardization template for all AG projects", "template_version": "2.3"}'),
  ('ag-notebook', 'AG_Notebook', 'satellite', 'W:\Antigravity_OS\00_CORE\AG_Notebook', '00_CORE', 'active', 1,
   '{"description": "Personal/professional OS in Notion", "autonomy_score": 50, "gap": "Missing local dispatch/manifest"}'),
  ('ag-sv-agent', 'AG_SV_Agent', 'satellite', 'W:\Antigravity_OS\00_CORE\AG_SV_Agent', '00_CORE', 'active', 2,
   '{"description": "Server agent for Hetzner infrastructure management", "autonomy_score": 50, "gap": "Missing local dispatch/manifest"}'),
  ('ag-analizador-rce', 'AG_Analizador_RCE', 'satellite', 'W:\Antigravity_OS\01_HOSPITAL_PRIVADO\AG_Analizador_RCE', '01_HOSPITAL_PRIVADO', 'active', 2,
   '{"description": "RCE data quality analysis and corrections", "category": "hospital-personal"}'),
  ('ag-consultas', 'AG_Consultas', 'satellite', 'W:\Antigravity_OS\01_HOSPITAL_PRIVADO\AG_Consultas', '01_HOSPITAL_PRIVADO', 'active', 2,
   '{"description": "Intelligence on TrakCare/ALMA queries", "category": "hospital-personal"}'),
  ('ag-deepresearch', 'AG_DeepResearch_Salud_Chile', 'satellite', 'W:\Antigravity_OS\01_HOSPITAL_PRIVADO\AG_DeepResearch_Salud_Chile', '01_HOSPITAL_PRIVADO', 'active', 2,
   '{"description": "Regulatory and technical health research for Chile", "category": "proyectos"}'),
  ('ag-hospital', 'AG_Hospital', 'satellite', 'W:\Antigravity_OS\01_HOSPITAL_PRIVADO\AG_Hospital', '01_HOSPITAL_PRIVADO', 'active', 1,
   '{"description": "Hospital documental hub", "category": "hospital-personal", "autonomy_score": 50, "gap": "Missing local dispatch/manifest"}'),
  ('ag-hospital-org', 'AG_Hospital_Organizador', 'satellite', 'W:\Antigravity_OS\01_HOSPITAL_PRIVADO\AG_Hospital_Organizador', '01_HOSPITAL_PRIVADO', 'active', 2,
   '{"description": "NocoBase automated administrative document organization", "category": "hospital-equipo", "type": "nocobase"}'),
  ('ag-informatica', 'AG_Informatica_Medica', 'satellite', 'W:\Antigravity_OS\01_HOSPITAL_PRIVADO\AG_Informatica_Medica', '01_HOSPITAL_PRIVADO', 'active', 2,
   '{"description": "Virtual medical informatics team and standards", "category": "proyectos"}'),
  ('ag-lists', 'AG_Lists_Agent', 'satellite', 'W:\Antigravity_OS\01_HOSPITAL_PRIVADO\AG_Lists_Agent', '01_HOSPITAL_PRIVADO', 'active', 2,
   '{"description": "Operational lists management agent", "category": "personales"}'),
  ('ag-trakcare', 'AG_TrakCare_Explorer', 'satellite', 'W:\Antigravity_OS\01_HOSPITAL_PRIVADO\AG_TrakCare_Explorer', '01_HOSPITAL_PRIVADO', 'active', 2,
   '{"description": "Hospital knowledge exploration and workflow support", "category": "hospital-personal"}'),
  ('ag-nb-apps', 'AG_NB_Apps', 'satellite', 'W:\Antigravity_OS\02_HOSPITAL_PUBLICO\AG_NB_Apps', '02_HOSPITAL_PUBLICO', 'active', 2,
   '{"description": "NocoBase apps platform for public hospital", "category": "hospital-equipo", "type": "nocobase"}'),
  ('ag-sd-plantilla', 'AG_SD_Plantilla', 'satellite', 'W:\Antigravity_OS\02_HOSPITAL_PUBLICO\AG_SD_Plantilla', '02_HOSPITAL_PUBLICO', 'active', 1,
   '{"description": "Modular template aligned to digital/health governance", "category": "privado", "autonomy_score": 50, "gap": "Missing local dispatch/manifest"}')
ON CONFLICT (id) DO UPDATE SET status = EXCLUDED.status, phase = EXCLUDED.phase, metadata = EXCLUDED.metadata;

-- ============================================================================
-- 2. Agent Prompts — 7 agents from AG_Orquesta manifest v3.0
-- ============================================================================
INSERT INTO prompts (id, version, label, type, vendor, content, changelog) VALUES
  ('system-researcher', 1, 'production', 'system', 'codex',
   'You are the Deep Research Agent. Investigate documentation, APIs, best practices with full citations. Read-only — never modify files. With 1M context, ingest full documentation sets when available. Always provide primary source URLs.',
   'From AG_Orquesta manifest v3.0 — priority 1 agent'),
  ('system-code-reviewer', 1, 'production', 'system', 'claude',
   'You are the Code Reviewer and Security Auditor. Review code for bugs, security vulnerabilities, and governance compliance. Report only — never modify. Use maximum reasoning depth for security-critical findings. Execute reviews in 3 passes: security, logic, style.',
   'From AG_Orquesta manifest v3.0 — priority 2 agent'),
  ('system-code-analyst', 1, 'production', 'system', 'gemini',
   'You are the Code Analyst. Analyze code and architecture. Read-only — never modify. With 1M context, request ALL relevant files rather than fragments. Focus on structural patterns, dependencies, and architectural coherence.',
   'From AG_Orquesta manifest v3.0 — priority 3 agent'),
  ('system-doc-writer', 1, 'production', 'system', 'gemini',
   'You are the Documentation Writer. Maintain documentation with precision. Read before modifying — never delete existing content. Follow output_governance.md: no emojis, UTF-8, structured format. Update DEVLOG.md, TASKS.md, and library entries.',
   'From AG_Orquesta manifest v3.0 — priority 4 agent'),
  ('system-test-writer', 1, 'production', 'system', 'gemini',
   'You are the Test Engineer. Create comprehensive tests with proper mocking for external dependencies. Never use real data or credentials. Cover edge cases and security scenarios. Generate both unit and integration tests.',
   'From AG_Orquesta manifest v3.0 — priority 5 agent'),
  ('system-db-analyst', 1, 'production', 'system', 'claude',
   'You are the Database Analyst. Analyze schemas, queries, and migrations. NEVER execute DELETE/DROP/UPDATE without explicit confirmation. Use maximum reasoning for schema design. Focus on performance, security, and data integrity.',
   'From AG_Orquesta manifest v3.0 — priority 6 agent'),
  ('system-deployer', 1, 'production', 'system', 'gemini',
   'You are the Deployment Engineer. Configure deployments via Docker, CI/CD, and infrastructure-as-code. Never include secrets in files — use environment variables or secret managers. Validate configurations before applying.',
   'From AG_Orquesta manifest v3.0 — priority 7 agent')
ON CONFLICT (id, version) DO NOTHING;

-- ============================================================================
-- 3. Skills — New operational skills from research R-01 to R-08
-- ============================================================================
INSERT INTO skills (id, name, description, supported_agents, vendor, version, status, skill_path, metadata) VALUES
  ('cli-version-verify', 'CLI Version Compatibility', 'Validate installed CLI versions against config/cli_versions.json approved list per environment', ARRAY['researcher', 'code-reviewer'], 'all', '1.0', 'planned',
   '.claude/commands/cli-verify.md',
   '{"trigger": "/cli-verify", "source": "R-02", "scripts": ["agent_health_check.py --verify-cli"]}'),
  ('mcp-deprecation-audit', 'MCP Deprecation Audit', 'Scan MCP configs for deprecated packages and suggest official replacements', ARRAY['code-reviewer'], 'all', '1.0', 'planned',
   '.claude/commands/mcp-audit.md',
   '{"trigger": "/mcp-audit", "source": "R-03", "deprecated": ["@modelcontextprotocol/server-github", "@modelcontextprotocol/server-brave-search"]}'),
  ('template-drift-check', 'Template Drift Check', 'Detect deviations from AG_Plantilla standard across all satellites using propagate.py', ARRAY['code-reviewer', 'lead-orchestrator'], 'all', '1.0', 'planned',
   '.claude/commands/template-drift.md',
   '{"trigger": "/template-drift", "source": "R-01", "scripts": ["propagate.py status"]}'),
  ('health-compliance-matrix', 'Health Compliance Matrix', 'Generate normative matrix per project: Chilean law, data type, technical control, audit evidence', ARRAY['researcher', 'code-reviewer'], 'all', '1.0', 'planned',
   '.claude/commands/compliance-matrix.md',
   '{"trigger": "/compliance-matrix", "source": "R-05", "laws": ["Ley 21.180", "Ley 21.663", "Ley 21.668"]}'),
  ('ecosystem-scorecard', 'Ecosystem Scorecard', 'Generate monthly scorecard: security (0 secrets), operations (dispatch functional), governance (0 doc gaps), compliance (interop audits)', ARRAY['lead-orchestrator', 'code-reviewer'], 'all', '1.0', 'planned',
   '.claude/commands/scorecard.md',
   '{"trigger": "/scorecard", "source": "R-07", "kpis": ["security", "operations", "governance", "compliance"]}'),
  ('agentic-security-eval', 'Agentic Security Evaluation', 'Run OWASP LLM Top 10 + NIST AI RMF controls audit on dispatch and tool configurations', ARRAY['code-reviewer'], 'all', '1.0', 'planned',
   '.claude/commands/security-eval.md',
   '{"trigger": "/security-eval", "source": "R-08", "frameworks": ["OWASP LLM Top 10", "NIST AI RMF 1.0"]}')
ON CONFLICT (id) DO UPDATE SET description = EXCLUDED.description, metadata = EXCLUDED.metadata;

-- ============================================================================
-- 4. Workflows — Roadmap execution phases P0-P3
-- ============================================================================
INSERT INTO workflows (id, name, owner, trigger, steps, actors, scripts, status) VALUES
  ('W-020', 'p0_emergency_fixes', 'lead-orchestrator', 'Immediate after ecosystem audit',
   '[{"id":"fix_credential_scanner","actor":"code-reviewer","action":"run_script","target":"scripts/secret_scanner.py"},{"id":"fix_dispatch_linux","actor":"deployer","action":"edit_file","target":".subagents/dispatch-team.sh"},{"id":"fix_auto_memory_path","actor":"code-analyst","action":"edit_file","target":".subagents/auto-memory.sh"},{"id":"apply_unicode_fallback","actor":"code-analyst","action":"edit_files","target":"scripts/*.py"},{"id":"restore_governance_docs","actor":"doc-writer","action":"restore_files"}]'::jsonb,
   ARRAY['code-reviewer', 'deployer', 'code-analyst', 'doc-writer'],
   ARRAY['scripts/secret_scanner.py', '.subagents/dispatch-team.sh'], 'active'),
  ('W-021', 'p1_mcp_migration', 'lead-orchestrator', 'Post P0 completion',
   '[{"id":"audit_mcp_deprecations","actor":"code-reviewer","action":"run_script","target":"scripts/mcp_audit.py"},{"id":"migrate_github_mcp","actor":"deployer","action":"edit_config"},{"id":"migrate_brave_mcp","actor":"deployer","action":"edit_config"},{"id":"create_cli_versions","actor":"code-analyst","action":"write_file","target":"config/cli_versions.json"},{"id":"add_smoke_tests","actor":"test-writer","action":"write_file"},{"id":"consolidate_policies","actor":"lead-orchestrator","action":"edit_files"}]'::jsonb,
   ARRAY['code-reviewer', 'deployer', 'code-analyst', 'test-writer', 'lead-orchestrator'],
   ARRAY['scripts/mcp_audit.py'], 'planned'),
  ('W-022', 'p2_template_standardization', 'lead-orchestrator', 'Post P1 completion',
   '[{"id":"detect_drift","actor":"code-reviewer","action":"run_script","target":"scripts/propagate.py"},{"id":"create_sync_schedule","actor":"doc-writer","action":"write_file"},{"id":"distribute_manifest","actor":"deployer","action":"copy_files"},{"id":"nocobase_hardening","actor":"code-analyst","action":"edit_config"},{"id":"docker_contract_tests","actor":"test-writer","action":"write_file"}]'::jsonb,
   ARRAY['code-reviewer', 'doc-writer', 'deployer', 'code-analyst', 'test-writer'],
   ARRAY['scripts/propagate.py'], 'planned'),
  ('W-023', 'p3_compliance_pilots', 'lead-orchestrator', 'Post P2 completion',
   '[{"id":"generate_compliance_matrix","actor":"researcher","action":"write_file"},{"id":"map_interoperability","actor":"code-analyst","action":"write_file"},{"id":"pilot_fhir_flow","actor":"deployer","action":"run_script"},{"id":"measure_quality","actor":"test-writer","action":"run_script"},{"id":"publish_report","actor":"doc-writer","action":"write_file"}]'::jsonb,
   ARRAY['researcher', 'code-analyst', 'deployer', 'test-writer', 'doc-writer'],
   ARRAY[], 'planned'),
  ('W-030', 'continuous_research_cadence', 'researcher', 'Weekly/biweekly/monthly schedule',
   '[{"id":"weekly_cli_check","actor":"researcher","action":"web_search","target":"CLI updates: Claude Code, Gemini CLI, Codex CLI"},{"id":"weekly_mcp_check","actor":"researcher","action":"web_search","target":"MCP server deprecations and updates"},{"id":"biweekly_platform_check","actor":"researcher","action":"web_search","target":"NocoBase, Docker, Proxmox releases"},{"id":"monthly_regulatory_check","actor":"researcher","action":"web_search","target":"Chile health regulations: MINSAL, FHIR updates"},{"id":"update_index","actor":"doc-writer","action":"append_file","target":"docs/research/INDEX.md"}]'::jsonb,
   ARRAY['researcher', 'doc-writer'],
   ARRAY[], 'active')
ON CONFLICT (id) DO UPDATE SET steps = EXCLUDED.steps, actors = EXCLUDED.actors, scripts = EXCLUDED.scripts, status = EXCLUDED.status;

-- ============================================================================
-- 5. Tasks — From roadmap R-07 (P0-P3 priorities)
-- ============================================================================
INSERT INTO tasks (project_id, title, description, status, priority, assigned_to, phase, tags) VALUES
  -- P0: 0-7 days
  ('ag-orquesta', 'Fix credential scanner hash', 'Patch KNOWN_CREDENTIAL_HASHES for hkEVC9AFVjFeRTkp test failure', 'backlog', 'critical', 'code-reviewer', 'P0', ARRAY['security', 'scanner', 'p0']),
  ('ag-orquesta', 'Fix dispatch-team.sh Linux schema', 'Correct agent_teams field names to match manifest.json', 'backlog', 'critical', 'deployer', 'P0', ARRAY['dispatch', 'linux', 'p0']),
  ('ag-orquesta', 'Fix auto-memory path traversal', 'Fix workspace root calculation in auto-memory.ps1 and auto-memory.sh', 'backlog', 'critical', 'code-analyst', 'P0', ARRAY['memory', 'security', 'p0']),
  ('ag-orquesta', 'Apply Unicode/ASCII fallback', 'Remove non-ASCII output or force ASCII fallback in 6 CLI scripts', 'backlog', 'high', 'code-analyst', 'P0', ARRAY['unicode', 'windows', 'p0']),
  -- P1: 7-30 days
  ('ag-orquesta', 'Migrate GitHub MCP to official', 'Replace @modelcontextprotocol/server-github with github/github-mcp-server', 'backlog', 'high', 'deployer', 'P1', ARRAY['mcp', 'migration', 'p1']),
  ('ag-orquesta', 'Migrate Brave MCP to official', 'Replace @modelcontextprotocol/server-brave-search with brave/brave-search-mcp-server', 'backlog', 'high', 'deployer', 'P1', ARRAY['mcp', 'migration', 'p1']),
  ('ag-orquesta', 'Create CLI version locks', 'Create config/cli_versions.json with approved versions per environment', 'backlog', 'medium', 'code-analyst', 'P1', ARRAY['cli', 'version-control', 'p1']),
  -- P2: 30-60 days
  ('ag-orquesta', 'Template standardization (35 deviations)', 'Run propagate.py apply --all to fix 35 template deviations across ecosystem', 'backlog', 'medium', 'lead-orchestrator', 'P2', ARRAY['templates', 'standardization', 'p2']),
  ('ag-orquesta', 'Raise autonomy in 4 projects', 'Distribute manifest.json and dispatch scripts to AG_Notebook, AG_SV_Agent, AG_Hospital, AG_SD_Plantilla', 'backlog', 'medium', 'deployer', 'P2', ARRAY['autonomy', 'dispatch', 'p2']),
  -- P3: 60-90 days
  ('ag-orquesta', 'Health compliance pilot', 'Execute interoperability pilot with regulatory traceability per Ley 21.668 + MINSAL FHIR', 'backlog', 'low', 'researcher', 'P3', ARRAY['compliance', 'health', 'fhir', 'p3'])
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 6. Deep Research Memories — 8 reports from 2026-02-22
-- ============================================================================
INSERT INTO memories (project_id, agent_id, content, memory_type, tags) VALUES
  -- R-01: Auditoria Tecnica Base
  ('ag-orquesta', 'system',
   'R-01 Audit Base (2026-02-22): P0 gaps found — credential scanner hash mismatch for hkEVC9AFVjFeRTkp, dispatch-team.sh Linux schema mismatch (agent_teams.teams vs agent_teams[]), auto-memory.ps1/sh path traversal writes outside target repo. P1: Unicode/emoji failures in 6 scripts on Windows cp1252. P2: 35 template deviations, 4 projects at 50/100 autonomy (AG_Notebook, AG_SV_Agent, AG_Hospital, AG_SD_Plantilla).',
   'research', ARRAY['audit', 'security', 'R-01', 'P0']),

  -- R-02: CLI Agentico
  ('ag-orquesta', 'system',
   'R-02 CLI Stack (2026-02-22): Three CLIs active — Claude Code (high release cadence, pin major.minor), Gemini CLI (stable vs preview channels, use stable for ops), Codex CLI (sandbox+MCP+WSL, consolidate approval policies). Action: create config/cli_versions.json with locks per environment, add --verify-cli to health check, weekly smoke tests.',
   'research', ARRAY['cli', 'orchestration', 'R-02', 'version-control']),

  -- R-03: MCP Protocol
  ('ag-orquesta', 'system',
   'R-03 MCP Servers (2026-02-22): Monolithic repo archived; vendor-maintained replacements. DEPRECATED: @modelcontextprotocol/server-github (replace with github/github-mcp-server), @modelcontextprotocol/server-brave-search (replace with brave/brave-search-mcp-server). Transport: SSE legacy, Streamable HTTP recommended. Fetch MCP needs domain allowlist. SQLite MCP maintainer status unclear.',
   'research', ARRAY['mcp', 'deprecation', 'R-03', 'P1']),

  -- R-04: Platforms
  ('ag-orquesta', 'system',
   'R-04 Platforms (2026-02-22): NocoBase v2 roadmap requires production/innovation separation + plugin compatibility matrix. Docker Compose and MCP Gateway need version pinning + contract tests. Proxmox VE9 released 2025-08-05 — pre-upgrade checklist: verified backup, canary, rollback test. Risk matrix: all High severity requiring staging.',
   'research', ARRAY['platforms', 'nocobase', 'docker', 'proxmox', 'R-04']),

  -- R-05: Salud Chile
  ('ag-orquesta', 'system',
   'R-05 Chile Health Regulatory (2026-02-22): Three laws mandate digital health: Ley 21.180 (2019, digitization), Ley 21.663 (2024-03, cybersecurity), Ley 21.668 (2024-05, clinical record interoperability). MINSAL publishes FHIR/CDA standards at interoperabilidad.minsal.cl. Affected projects: AG_Consultas, AG_Analizador_RCE, AG_TrakCare_Explorer, AG_Hospital. Roadmap: normative matrix (0-30d), FHIR profiles (30-60d), pilot (60-90d).',
   'research', ARRAY['compliance', 'chile', 'health', 'fhir', 'R-05']),

  -- R-06: Functional Map
  ('ag-orquesta', 'system',
   'R-06 Ecosystem Map (2026-02-22): 14 projects across 3 domains. 7 agents and 4 teams in manifest v3.0. 4 functional clusters: A) Orchestration (AG_Orquesta, AG_Plantilla) P0, B) NocoBase (AG_NB_Apps, AG_Hospital_Organizador) P1, C) Clinical (AG_Consultas, AG_Analizador_RCE, AG_DeepResearch, AG_TrakCare) P1-P2, D) Documentation (AG_Hospital, AG_Notebook, AG_Informatica, AG_Lists, AG_SD_Plantilla, AG_SV_Agent) P2.',
   'research', ARRAY['ecosystem', 'functional-map', 'clusters', 'R-06']),

  -- R-07: Roadmap
  ('ag-orquesta', 'system',
   'R-07 Master Roadmap (2026-02-22): 46 verified searches consolidated into 90-day plan. P0 (0-7d): fix scanner, dispatch, auto-memory, unicode. P1 (7-30d): migrate MCP, create cli_versions.json, smoke tests. P2 (30-60d): fix 35 template deviations, raise autonomy, NocoBase hardening. P3 (60-90d): health compliance pilots, monthly scorecard. KPIs: 0 secrets, 100% dispatch functional, >=90 autonomy, 0 doc gaps.',
   'research', ARRAY['roadmap', 'master-plan', 'R-07', 'kpi']),

  -- R-08: Security Framework
  ('ag-orquesta', 'system',
   'R-08 Agentic Security (2026-02-22): Operationalized OWASP LLM Top 10 + NIST AI RMF 1.0. 5-control minimum: prompt injection (delimiters+sanitization), tool exfiltration (domain allowlists), execution errors (approval policies), behavior drift (version pins+smoke tests), overreliance (human-in-the-loop). 3-stage eval: Stage 1 benchmarks (0-14d), Stage 2 attack testing (14-45d), Stage 3 risk dashboard (45-90d).',
   'research', ARRAY['security', 'owasp', 'nist', 'evaluation', 'R-08'])
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 7. Ecosystem Architecture Memory — Cross-project relationships
-- ============================================================================
INSERT INTO memories (project_id, agent_id, content, memory_type, tags) VALUES
  ('ag-orquesta', 'system',
   'AG_Orquesta_Desk manifest v3.0: 7 agents (researcher/codex P1, code-reviewer/claude P2, code-analyst/gemini P3, doc-writer/gemini P4, test-writer/gemini P5, db-analyst/claude P6, deployer/gemini P7). 4 teams: full-review (parallel: reviewer+test+doc), feature-pipeline (sequential: analyst+test+reviewer), deep-audit (parallel: reviewer+db+deployer), rapid-fix (sequential: analyst+reviewer). Supervisor: opus-4.6.',
   'semantic', ARRAY['agents', 'teams', 'manifest']),
  ('ag-orquesta', 'system',
   'Ecosystem topology (2026-02-22): 15 projects in 3 domains. 00_CORE (5): AG_Orquesta_Desk, GEN_OS, AG_Plantilla, AG_Notebook, AG_SV_Agent. 01_HOSPITAL_PRIVADO (8): AG_Analizador_RCE, AG_Consultas, AG_DeepResearch_Salud_Chile, AG_Hospital, AG_Hospital_Organizador, AG_Informatica_Medica, AG_Lists_Agent, AG_TrakCare_Explorer. 02_HOSPITAL_PUBLICO (2): AG_NB_Apps, AG_SD_Plantilla.',
   'semantic', ARRAY['topology', 'ecosystem', 'domains']),
  ('ag-orquesta', 'system',
   'Shared responsibility: AG_Orquesta owns cross_task.py (task delegation), propagate.py (template drift), audit_ecosystem.py (normalization), knowledge_sync.py (vault sync). GEN_OS owns audit_suite.py (security/compliance), workflow_engine.py (releases), secret_scanner.py (secrets), dictionary_completeness.py (living dictionary). Both have env_resolver.py and memory_sync.py — Orquesta is source-of-truth for operational versions.',
   'semantic', ARRAY['responsibility', 'shared-code', 'source-of-truth'])
ON CONFLICT DO NOTHING;

COMMIT;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================
-- Run after import to verify:
--   SELECT 'projects' as entity, count(*) FROM projects;
--   SELECT 'prompts' as entity, count(*) FROM prompts;
--   SELECT 'skills' as entity, count(*) FROM skills;
--   SELECT 'workflows' as entity, count(*) FROM workflows;
--   SELECT 'tasks' as entity, count(*) FROM tasks;
--   SELECT 'memories' as entity, count(*) FROM memories;
