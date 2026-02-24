# Deep Research R-02: CLI Agentico (Codex, Claude Code, Gemini CLI)

- Fecha: 2026-02-22
- Objetivo: validar estado vigente de CLIs principales del ecosistema para actualizar configuracion y reducir drift

## 1) Resumen ejecutivo

La triada de CLIs sigue activa y evolucionando, pero con velocidades distintas:

1. Claude Code: release cadence alta y cambios frecuentes en workflow.
2. Gemini CLI: release cadence alta con diferencias entre "latest stable" y "preview".
3. Codex CLI: documentacion robusta de sandbox/aprobaciones/MCP/windows, con foco fuerte en ejecucion controlada.

Implicacion para Antigravity: no conviene operar por "latest" implicito; se requiere pinning y smoke tests por vendor.

## 2) Hallazgos por CLI

## 2.1 Claude Code

Se confirma:

- Documentacion oficial activa de CLI, workflows y herramientas.
- Release notes de API Anthropic mantienen seccion de Claude Code.
- Repositorio oficial de releases con tags recientes (ejemplo observado: `v2.0.74` con fecha 2025-11-22).

Riesgo:

- cambios rapidos en flags/comportamiento pueden romper dispatchers sin version lock.

Recomendacion:

- pin por version mayor+minor para entornos productivos y actualizar en ventana semanal controlada.

## 2.2 Gemini CLI

Se confirma:

- Documentacion oficial activa en Google AI docs.
- Releases en repo oficial `google-gemini/gemini-cli` con actividad reciente.
- Coexistencia de canal estable y preview (ejemplo observado: `0.29.5` stable, `0.30.0-preview`).

Riesgo:

- adoptar preview en pipeline operativo puede introducir cambios no estabilizados.

Recomendacion:

- usar stable para ejecucion diaria y preview solo en rama de validacion.

## 2.3 Codex CLI

Se confirma:

- Documentacion oficial de OpenAI para Codex y CLI.
- Documentacion separada para:
  - sandbox
  - MCP
  - Windows (flujo con WSL)
- enfoque explicito en control de ejecucion y politicas de aprobacion.

Riesgo:

- configuraciones inconsistentes de sandbox/aprobaciones entre proyectos pueden generar comportamiento no reproducible.

Recomendacion:

- consolidar politica de aprobaciones/sandbox por entorno (desktop/notebook/server) y versionarla.

## 3) Impacto en tu stack de orquestacion

Problema actual observado:

- scripts de dispatch mezclan supuestos de CLI y no tienen validacion formal de compatibilidad de flags por version.

Mejora propuesta:

1. Definir `compatibility matrix` por vendor CLI.
2. Ejecutar smoke tests automáticos:
- `dispatch` simple por agente
- `dispatch-team` en modo sequential y parallel
- `research fallback`
3. Fallar rapido si version detectada no esta en lista aprobada.

## 4) Checklist de hardening CLI

1. Crear `config/cli_versions.json` con versiones aprobadas por entorno.
2. Agregar comando `scripts/agent_health_check.py --verify-cli` (nuevo).
3. Implementar control de compatibilidad por flags antes de invocar cada CLI.
4. Registrar fecha de validacion por vendor en `config/research_topics.yaml`.

## 5) Fuentes primarias

- Anthropic Claude Code docs: https://docs.anthropic.com/en/docs/claude-code/overview
- Anthropic API release notes (incluye Claude Code): https://docs.anthropic.com/en/release-notes/api
- Claude Code releases: https://github.com/anthropics/claude-code/releases
- Gemini CLI docs: https://ai.google.dev/gemini-api/docs/cli
- Gemini CLI releases: https://github.com/google-gemini/gemini-cli/releases
- OpenAI Codex product page: https://openai.com/codex/
- OpenAI Codex CLI docs: https://developers.openai.com/codex/cli
- OpenAI Codex CLI sandbox: https://developers.openai.com/codex/cli/sandbox
- OpenAI Codex CLI MCP: https://developers.openai.com/codex/cli/mcp
- OpenAI Codex CLI Windows: https://developers.openai.com/codex/cli/windows

