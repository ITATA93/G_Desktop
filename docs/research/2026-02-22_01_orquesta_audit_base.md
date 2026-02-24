# Deep Research R-01: Auditoria Tecnica Base de AG_Orquesta_Desk

- Fecha: 2026-02-22
- Tipo: Baseline tecnico local previo a recomendaciones
- Objetivo: establecer estado real del orquestador y del ecosistema antes de definir mejoras

## 1) Metodo de auditoria

Se ejecutaron y contrastaron los siguientes chequeos locales:

- `python scripts/agent_health_check.py`
- `.venv\Scripts\python.exe -m pytest -q`
- `python scripts/audit_ecosystem.py`
- `python scripts/agent_selftest.py` (con `PYTHONUTF8=1`)
- `python scripts/propagate.py status` (con `PYTHONUTF8=1`)
- lectura estructural de `.subagents/manifest.json`, dispatchers, skills y config

## 2) Hallazgos principales

## 2.1 Hallazgos P0 (bloqueantes operativos)

1. Falla de test de seguridad en scanner de credenciales:
- sintoma: falla en `tests/test_audit_ecosystem.py::test_detects_known_credential`
- impacto: reduce confianza en deteccion de secretos hardcodeados
- evidencia: hash esperado para `hkEVC9AFVjFeRTkp` no coincide con hash en `KNOWN_CREDENTIAL_HASHES`

2. Mismatch de schema en dispatcher Linux de equipos:
- `dispatch-team.sh` consulta `agent_teams[]` y campo `execution`
- manifest actual usa `agent_teams.teams` y `mode`
- impacto: teams en Linux no confiables sin parche

3. Bug de path en auto-memory:
- `auto-memory.ps1` y `auto-memory.sh` calculan workspace root subiendo 2 niveles
- impacto: posibilidad de escribir `docs/DEVLOG.md` fuera del repo objetivo

## 2.2 Hallazgos P1 (alto impacto)

1. Fragilidad por Unicode/emoji en consola Windows (cp1252):
- scripts afectados: `agent_selftest.py`, `env_resolver.py`, `memory_sync.py`, `ecosystem_dashboard.py`, `propagate.py`, `cross_task.py`
- impacto: comandos centrales fallan en entornos corporativos Windows sin UTF-8 global

2. Desalineacion documental en AG_Orquesta_Desk:
- `audit_ecosystem.py --project AG_Orquesta_Desk` reporta faltantes requeridos (`docs/DEVLOG.md`, `docs/TASKS.md`) y recomendado (`docs/standards/output_governance.md`)
- impacto: disminuye score operacional y dificulta trazabilidad

## 2.3 Hallazgos P2 (mejora estructural)

1. Drift de template extendido (35 desviaciones reportadas en ecosistema):
- incluye `GEMINI.md`, `.gitignore`, y `docs/standards/output_governance.md`
- impacto: divergencia de comportamiento entre satelites

2. Autonomia asistida en varios proyectos:
- score 50/100 en `AG_Notebook`, `AG_SV_Agent`, `AG_Hospital`, `AG_SD_Plantilla`
- factor principal: ausencia de `.subagents/manifest` y dispatch local completo

## 3) Diagnostico de madurez actual

Estado mixto:

- Fortalezas:
  - `agent_health_check.py` pasa 50/50 en este repo
  - ecosistema promedio alto en auditoria estructural (A mayoritario)
  - manifest multi-vendor y teams definidos con prioridades claras
- Debilidades:
  - robustez operativa inconsistente entre OS
  - deuda tecnica puntual en seguridad scanner
  - gobernanza documental incompleta en el orquestador actual

## 4) Recomendaciones inmediatas (pre-web roadmap)

1. Parchear `KNOWN_CREDENTIAL_HASHES` y re-ejecutar pytest.
2. Corregir `dispatch-team.sh` al schema real de `manifest.json`.
3. Corregir calculo de root en `auto-memory.*`.
4. Eliminar output no-ASCII en CLIs o forzar fallback ASCII por defecto.
5. Restaurar `docs/DEVLOG.md`, `docs/TASKS.md`, y `docs/standards/output_governance.md` en AG_Orquesta_Desk.

## 5) Evidencia local usada

- `scripts/audit_ecosystem.py`
- `scripts/agent_selftest.py`
- `scripts/propagate.py`
- `scripts/env_resolver.py`
- `.subagents/dispatch-team.sh`
- `.subagents/dispatch-team.ps1`
- `.subagents/auto-memory.ps1`
- `.subagents/auto-memory.sh`
- `tests/test_audit_ecosystem.py`

