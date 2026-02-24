# Deep Research R-03: MCP (Protocolo y Servidores)

- Fecha: 2026-02-22
- Objetivo: validar compatibilidad MCP real contra `config/mcp_servers.yaml` para evitar deprecaciones silenciosas

## 1) Resumen ejecutivo

El stack MCP actual del ecosistema necesita actualizacion dirigida:

1. Hay deprecaciones confirmadas en paquetes usados hoy.
2. El ecosistema MCP migro desde un repositorio monolitico a mantenedores por servidor.
3. El transporte recomendado evoluciono y requiere revisar implementaciones antiguas.

## 2) Estado del protocolo MCP

Hallazgos clave:

1. Existe changelog formal del spec MCP (baseline relevante: 2025-06-18).
2. El repositorio `modelcontextprotocol/servers` fue archivado, con migracion hacia repos mantenidos por cada propietario de servidor.
3. En ecosistema SDK se observa movimiento desde SSE a Streamable HTTP como direccion recomendada (SSE queda por compatibilidad).

Implicacion:

- configuraciones heredadas de "servidores comunitarios legacy" tienen alto riesgo de quedar sin soporte.

## 3) Analisis de servidores declarados en tu config

Archivo analizado: `config/mcp_servers.yaml`

## 3.1 GitHub MCP

Estado actual en config:

- `@modelcontextprotocol/server-github`

Evidencia externa:

- el paquete npm `@modelcontextprotocol/server-github` aparece deprecado y direcciona al servidor oficial `github-mcp-server`.
- existe repositorio oficial activo: `github/github-mcp-server`.

Recomendacion:

- migrar a servidor oficial de GitHub MCP y actualizar runbook de autenticacion.

## 3.2 Brave Search MCP

Estado actual en config:

- `@modelcontextprotocol/server-brave-search`

Evidencia externa:

- paquete npm deprecado.
- Brave mantiene repo oficial `brave/brave-search-mcp-server` con notas de migracion (1.x a 2.x) y cambio de default a `stdio`.

Recomendacion:

- migrar al servidor oficial de Brave y revisar transport/config de compatibilidad.

## 3.3 Filesystem MCP

Estado actual en config:

- `@modelcontextprotocol/server-filesystem`

Evidencia externa:

- paquete npm con publicaciones recientes (senal de mantenimiento activo).

Recomendacion:

- mantener, pero restringir roots por entorno (least privilege).

## 3.4 SQLite MCP

Estado actual en config:

- `@modelcontextprotocol/server-sqlite`

Riesgo:

- sin evidencia robusta de roadmap de mantenimiento al mismo nivel que servidores oficiales nuevos.

Recomendacion:

- validar mantenedor activo antes de llevarlo a produccion; si no hay mantenimiento claro, reemplazar por alternativa propia controlada.

## 3.5 Fetch MCP

Estado actual en config:

- `@modelcontextprotocol/server-fetch`

Riesgo:

- fetch sin filtro puede ampliar superficie de exfiltracion y prompt injection indirecta.

Recomendacion:

- habilitar allowlist de dominios por entorno y loggear URL de entrada/salida.

## 3.6 Docker MCP

Estado actual en config:

- `@modelcontextprotocol/server-docker`

Evidencia externa:

- Docker mantiene iniciativa MCP propia (`docker/mcp-gateway`) con releases activos.

Recomendacion:

- evaluar convergencia al stack oficial Docker MCP (gateway/toolkit) para reducir dependencia de implementaciones legacy.

## 4) Riesgos tecnicos priorizados

1. Paquetes deprecados en runtime sin alarma.
2. Deriva de transporte (SSE/Streamable HTTP) no reflejada en checklist operativo.
3. Permisos excesivos de filesystem/fetch si no se segmentan por entorno.

## 5) Plan de migracion MCP (propuesto)

## Fase 1 (0-7 dias)

1. Inventario de todos los servidores MCP por proyecto.
2. Marcar deprecados y estado de mantenimiento.
3. Definir baseline de transporte y auth por vendor.

## Fase 2 (7-21 dias)

1. Migrar GitHub MCP a oficial.
2. Migrar Brave MCP a oficial.
3. Añadir tests de conectividad y contrato para cada servidor.

## Fase 3 (21-45 dias)

1. Endurecer filesystem y fetch con allowlists.
2. Revisar estrategia SQLite MCP.
3. Integrar auditoria MCP automatica en health-check.

## 6) Fuentes primarias

- MCP spec changelog: https://modelcontextprotocol.io/specification/2025-06-18/changelog
- MCP servers (estado de archivo/migracion): https://github.com/modelcontextprotocol/servers
- GitHub MCP server oficial: https://github.com/github/github-mcp-server
- npm deprecacion `@modelcontextprotocol/server-github`: https://www.npmjs.com/package/%40modelcontextprotocol/server-github
- npm `@modelcontextprotocol/server-filesystem`: https://www.npmjs.com/package/%40modelcontextprotocol/server-filesystem
- npm deprecacion `@modelcontextprotocol/server-brave-search`: https://www.npmjs.com/package/%40modelcontextprotocol/server-brave-search
- Brave MCP server oficial: https://github.com/brave/brave-search-mcp-server
- Docker MCP gateway: https://github.com/docker/mcp-gateway/releases
- Azure MCP transport guidance (SSE legacy / Streamable HTTP): https://learn.microsoft.com/en-us/azure/developer/ai/streamable-http-mcp-servers

