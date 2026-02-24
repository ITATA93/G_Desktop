# Research Index

> Protocol: `docs/standards/output_governance.md` (referencia operativa usada desde AG_Plantilla v2.0)
> Last updated: 2026-02-22
> Scope: AG_Orquesta_Desk + ecosistema Antigravity (15 proyectos registrados)

## Research Reports

| ID | File | Aspecto | Estado | Validado hasta | Resultado clave |
|---|---|---|---|---|---|
| R-01 | `docs/research/2026-02-22_01_orquesta_audit_base.md` | Auditoria tecnica base (scripts/tests/gobernanza) | Complete | 2026-02-22 | Se detectan gaps P0 en robustez operativa de scripts y test de seguridad |
| R-02 | `docs/research/2026-02-22_02_cli_agentic_stack.md` | CLIs agenticos (Codex, Claude Code, Gemini CLI) | Complete | 2026-02-22 | Stack vigente pero sin pinning y con riesgo de drift de flags/config |
| R-03 | `docs/research/2026-02-22_03_mcp_servers_and_protocol.md` | MCP (spec, transportes, servidores) | Complete | 2026-02-22 | Se confirma deprecacion de servidores MCP usados en config actual |
| R-04 | `docs/research/2026-02-22_04_platforms_nocobase_docker_proxmox.md` | Plataformas (NocoBase, Docker, Proxmox) | Complete | 2026-02-22 | Requiere plan de upgrade controlado y hardening por plataforma |
| R-05 | `docs/research/2026-02-22_05_salud_chile_interoperabilidad.md` | Normativa Chile + interoperabilidad salud | Complete | 2026-02-22 | Ley 21.668 y estandares MINSAL obligan estrategia tecnico-legal formal |
| R-06 | `docs/research/2026-02-22_06_apps_and_agents_function_map.md` | Mapa funcional de apps, agentes y sistemas agenticos | Complete | 2026-02-22 | Se prioriza refuerzo en 4 proyectos con autonomia asistida |
| R-07 | `docs/research/2026-02-22_07_recommendations_roadmap.md` | Recomendaciones y roadmap maestro | Complete | 2026-02-22 | Plan 0-30-60-90 dias con entregables y KPIs |
| R-08 | `docs/research/2026-02-22_08_agentic_security_and_eval_framework.md` | Seguridad y evaluacion continua de sistemas agenticos | Complete | 2026-02-22 | Se define matriz de controles basada en OWASP/NIST aplicable al ecosistema |
| R-09 | `docs/research/2026-02-22_09_benchmark_evidence_agent_assignment.md` | Benchmarks independientes y asignacion vendor-agente | Complete | 2026-02-22 | Manifest v3.2: Claude 4/7, Gemini 2/7, Codex 1/7. Incluye Gemini 3.1 Pro (Feb 19), 15+ benchmarks independientes, context windows, suscripciones |

## Research Protocol Used

1. Auditar primero el estado local (scripts, tests, manifest, salud ecosistema).
2. Investigar por aspecto con fuentes primarias y vigentes.
3. Separar hallazgos por dominio (CLI, MCP, plataforma, compliance, apps/agentes).
4. Emitir recomendaciones accionables con prioridad y ventana temporal.
5. Registrar fuentes en cada reporte.

## Source Priority Rules (aplicadas)

1. Documentacion oficial del vendor o proyecto.
2. Repositorios oficiales (releases/changelog).
3. Publicaciones regulatorias oficiales (BCN/MINSAL/NIST/OWASP).
4. Fuentes secundarias solo para contexto, no para decisiones criticas.

## Next Refresh Window

- Cadencia recomendada: semanal para CLI/MCP, quincenal para plataformas, mensual para compliance.
- Proxima fecha sugerida: 2026-03-01.
