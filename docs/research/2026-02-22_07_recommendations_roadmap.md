# Deep Research R-07: Recomendaciones Maestras y Roadmap 0-30-60-90

- Fecha: 2026-02-22
- Base: R-01..R-06 (auditoria local + investigacion externa oficial)
- Objetivo: plan ejecutable para actualizar, configurar y mejorar el sistema de forma no superficial

## 0) Cobertura de busqueda ejecutada

Plan original y ejecucion:

1. Busquedas planificadas: 20
2. Busquedas ejecutadas: 46

Distribucion por aspecto:

- CLIs agenticos: 12
- MCP/spec/servidores: 14
- Plataformas (NocoBase/Docker/Proxmox): 8
- Cumplimiento Chile e interoperabilidad: 7
- Seguridad/evaluacion agentica (NIST/OWASP): 5

Resultado:

- cobertura suficiente para decisiones de update/config/hardening con fuentes primarias.

## 1) Principios de ejecucion

1. Corregir primero lo que rompe seguridad o reproducibilidad.
2. Normalizar stack tecnico antes de agregar nuevas capacidades.
3. Convertir "best effort" en "controles verificables" (tests, checks, gates).
4. Mantener trazabilidad documental por protocolo de salida.

## 2) Prioridades P0-P3

## P0 (inmediato, 0-7 dias)

1. Corregir hash de credencial conocida en scanner de seguridad.
2. Corregir `dispatch-team.sh` (schema/field mismatch).
3. Corregir `auto-memory.*` (workspace root path).
4. Aplicar fallback ASCII/UTF-8 robusto en scripts CLI.
5. Restaurar documentos requeridos en AG_Orquesta_Desk:
- `docs/DEVLOG.md`
- `docs/TASKS.md`
- `docs/standards/output_governance.md`

## P1 (7-30 dias)

1. Migrar MCP deprecated:
- GitHub MCP: `@modelcontextprotocol/server-github` -> oficial GitHub MCP server
- Brave MCP: `@modelcontextprotocol/server-brave-search` -> oficial Brave MCP server
2. Crear `config/cli_versions.json` y version lock por entorno.
3. Agregar smoke tests cross-vendor (dispatch + teams + fallback).
4. Definir politica unica de sandbox/aprobaciones para Codex/Claude/Gemini.

## P2 (30-60 dias)

1. Programa de estandarizacion por drift de template (35 desviaciones actuales).
2. Subir autonomia en proyectos asistidos (AG_Notebook, AG_SV_Agent, AG_Hospital, AG_SD_Plantilla).
3. Harden de NocoBase (matriz de plugins permitidos + staging obligatorio).
4. Contract tests para Docker MCP gateway y flujos Docker tool-based.

## P3 (60-90 dias)

1. Pilotos de interoperabilidad clinica con trazabilidad normativa (Ley 21.668 + estandares MINSAL/FHIR).
2. Scorecard mensual ecosistema:
- seguridad
- autonomia
- cumplimiento
- tiempo de remediacion
3. Integrar auditoria tecnica + regulatoria en ciclo de governance trimestral.

## 3) KPIs recomendados

## Seguridad

1. 0 secretos hardcodeados detectados (critical/high).
2. 100% de checks de scanner verdes en CI.

## Operacion agentica

1. 100% de dispatch scripts funcionales en Windows y Linux.
2. 100% de comandos core sin fallos de encoding.
3. >=90/100 autonomia en todos los proyectos.

## Gobernanza

1. 0 faltantes requeridos por `audit_ecosystem.py`.
2. Drift de template <=5 archivos por ciclo.

## Compliance salud

1. Matriz normativa vigente por proyecto de salud.
2. Al menos 1 flujo interoperable auditado y documentado por trimestre.

## 4) Plan de busqueda continua (deep research ops)

Cadencia recomendada:

1. Semanal:
- CLIs (Codex, Claude, Gemini)
- MCP servers y deprecaciones
2. Quincenal:
- NocoBase, Docker, Proxmox
3. Mensual:
- Marco regulatorio Chile + guias MINSAL/FHIR

Protocolo de almacenamiento:

1. cada corrida crea un archivo en `docs/research/` con fecha y aspecto
2. actualizar `docs/research/INDEX.md`
3. consolidar recomendaciones en un reporte maestro trimestral

## 5) Riesgos si no se ejecuta este plan

1. Rotura silenciosa de orquestacion por drift de CLIs/MCP.
2. Deteccion incompleta de credenciales por deuda en scanner.
3. Incumplimiento progresivo de estandares de interoperabilidad en salud.
4. Fragmentacion de calidad entre proyectos satelite.

## 6) Fuentes primarias consolidadas

## Agentic CLIs

- https://docs.anthropic.com/en/docs/claude-code/overview
- https://docs.anthropic.com/en/release-notes/api
- https://github.com/anthropics/claude-code/releases
- https://ai.google.dev/gemini-api/docs/cli
- https://github.com/google-gemini/gemini-cli/releases
- https://openai.com/codex/
- https://developers.openai.com/codex/cli
- https://developers.openai.com/codex/cli/sandbox
- https://developers.openai.com/codex/cli/mcp
- https://developers.openai.com/codex/cli/windows

## MCP

- https://modelcontextprotocol.io/specification/2025-06-18/changelog
- https://github.com/modelcontextprotocol/servers
- https://github.com/github/github-mcp-server
- https://www.npmjs.com/package/%40modelcontextprotocol/server-github
- https://www.npmjs.com/package/%40modelcontextprotocol/server-filesystem
- https://www.npmjs.com/package/%40modelcontextprotocol/server-brave-search
- https://github.com/brave/brave-search-mcp-server
- https://github.com/docker/mcp-gateway/releases
- https://learn.microsoft.com/en-us/azure/developer/ai/streamable-http-mcp-servers

## Plataformas

- https://github.com/nocobase/nocobase/releases
- https://www.nocobase.com/en/roadmap
- https://docs.docker.com/compose/releases/release-notes/
- https://www.proxmox.com/en/about/company-details/press-releases/proxmox-virtual-environment-9-0
- https://pve.proxmox.com/wiki/Roadmap

## Cumplimiento y seguridad

- https://www.bcn.cl/historiadelaley/nc/historia-de-la-ley/7680/
- https://www.bcn.cl/historiadelaley/nc/historia-de-la-ley/16518/
- https://www.bcn.cl/historiadelaley/nc/historia-de-la-ley/16784/
- https://www.bcn.cl/leychile/navegar?idNorma=1203827
- https://interoperabilidad.minsal.cl/fhir/ig/estandares-minsal/ArchitectureIndex.html
- https://interoperabilidad.minsal.cl/FHIR/ig/guiacda/index.html
- https://www.nist.gov/itl/ai-risk-management-framework
- https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- https://owasp.org/www-project-top-10-for-large-language-model-applications/
