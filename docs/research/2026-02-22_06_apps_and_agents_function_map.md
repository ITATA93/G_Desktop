# Deep Research R-06: Mapa Funcional de Apps, Sistemas Agenticos y Agentes

- Fecha: 2026-02-22
- Objetivo: aterrizar el deep research al inventario real de proyectos y agentes del ecosistema

## 1) Inventario funcional de apps (registro oficial)

Fuente local: `config/project_registry.json` + lectura de README/GEMINI por proyecto.

| Proyecto | Categoria | Tipo | Funcion principal sintetizada |
|---|---|---|---|
| AG_Plantilla | admin | template | plantilla maestra de estandarizacion y orquestacion |
| AG_Orquesta_Desk | admin | python | orquestador central de auditoria, tasks y coordinacion multi-proyecto |
| AG_Notebook | admin | documentation | sistema operativo personal/profesional en Notion |
| AG_SV_Agent | admin | infrastructure | bootstrap de plataforma local-first con agentes persistentes |
| AG_Analizador_RCE | hospital-personal | python | analisis de calidad de datos RCE y correcciones |
| AG_Consultas | hospital-personal | python | inteligencia de consultas sobre TrakCare/ALMA |
| AG_DeepResearch_Salud_Chile | proyectos | python | investigacion normativa y tecnica de salud en Chile |
| AG_Hospital | hospital-personal | documentation | hub documental hospitalario |
| AG_Hospital_Organizador | hospital-equipo | nocobase | organizacion automatizada de documentos administrativos |
| AG_Informatica_Medica | proyectos | documentation | equipo virtual de informatica medica y estandares |
| AG_Lists_Agent | personales | python | agente de gestion de listas operativas |
| AG_NB_Apps | hospital-equipo | nocobase | plataforma de apps NocoBase para hospital publico |
| AG_SD_Plantilla | privado | python | plantilla modular alineada a gobierno digital/salud |
| AG_TrakCare_Explorer | hospital-personal | python | exploracion/soporte de conocimiento hospitalario y flujos |

## 2) Sistemas agenticos definidos en AG_Orquesta_Desk

Fuente local: `.subagents/manifest.json`

## Agentes

| Agente | Vendor default | Prioridad | Trigger principal | Rol operativo |
|---|---|---:|---|---|
| researcher | codex | 1 | research/documentation/API reference | investigacion profunda con citacion |
| code-reviewer | claude | 2 | review/audit/security | auditoria de calidad y seguridad |
| code-analyst | gemini | 3 | analyze/architecture | analisis estructural de codigo |
| doc-writer | gemini | 4 | docs/changelog/readme | mantenimiento documental |
| test-writer | gemini | 5 | test/coverage | generacion de pruebas |
| db-analyst | claude | 6 | database/sql/schema | analisis de BD con restricciones de seguridad |
| deployer | gemini | 7 | deploy/docker/cicd | soporte a despliegue e infraestructura |

## Teams

| Team | Modo | Agentes | Uso |
|---|---|---|---|
| full-review | parallel | code-reviewer, test-writer, doc-writer | revision pre-merge integral |
| feature-pipeline | sequential | code-analyst, test-writer, code-reviewer | pipeline TDD |
| deep-audit | parallel | code-reviewer, db-analyst, deployer | auditoria full-stack |
| rapid-fix | sequential | code-analyst, code-reviewer | diagnostico/correccion rapida |

## 3) Gap map funcional (apps x capacidades agenticas)

## 3.1 Gaps de autonomia

Según `agent_selftest.py`:

- 50/100: `AG_Notebook`, `AG_SV_Agent`, `AG_Hospital`, `AG_SD_Plantilla`
- principal brecha: ausencia de `dispatch` y `manifest` local en esos repos.

## 3.2 Gaps de gobernanza

Según `audit_ecosystem.py`:

- `AG_Orquesta_Desk` con faltantes requeridos (`docs/DEVLOG.md`, `docs/TASKS.md`) y recomendado (`docs/standards/output_governance.md`).

## 3.3 Gaps de estandarizacion

Según `propagate.py status`:

- drift en 35 archivos entre plantilla y satelites, con foco en `GEMINI.md`, `.gitignore`, `output_governance`.

## 4) Priorizacion por cluster funcional

## Cluster A: Orquestacion central

Proyectos:

- AG_Orquesta_Desk
- AG_Plantilla

Prioridad:

- P0 inmediato para robustez de scanner seguridad, dispatch-team linux y Unicode-safe CLI.

## Cluster B: Plataformas hospitalarias NocoBase

Proyectos:

- AG_NB_Apps
- AG_Hospital_Organizador

Prioridad:

- P1 para upgrade governance de plugins/versions y hardening de workflow.

## Cluster C: Datos clinicos y consultas

Proyectos:

- AG_Consultas
- AG_Analizador_RCE
- AG_DeepResearch_Salud_Chile
- AG_TrakCare_Explorer

Prioridad:

- P1/P2 para alineacion interoperable y trazabilidad normativa.

## Cluster D: Documentacion y soporte

Proyectos:

- AG_Hospital
- AG_Notebook
- AG_Informatica_Medica
- AG_Lists_Agent
- AG_SD_Plantilla
- AG_SV_Agent

Prioridad:

- P2 para subir autonomia y homogeneidad de estandares.

## 5) Recomendaciones por tipo de app

1. `python`:
- reforzar testing/security gates
- version pinning de CLIs/MCP
2. `nocobase`:
- control estricto de plugins y migraciones
- staging obligatorio
3. `documentation`:
- generar evidencias operativas (task protocol, devlog, readiness)
4. `infrastructure`:
- hardening de secretos, permisos y runbooks de rollback
5. `template`:
- mantener como source of truth y reducir excepciones por proyecto

## 6) Evidencia local usada

- `config/project_registry.json`
- `.subagents/manifest.json`
- `scripts/agent_selftest.py`
- `scripts/audit_ecosystem.py`
- `scripts/propagate.py`

