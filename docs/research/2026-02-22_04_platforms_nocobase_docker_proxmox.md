# Deep Research R-04: Plataformas (NocoBase, Docker, Proxmox)

- Fecha: 2026-02-22
- Objetivo: identificar cambios vigentes en plataformas base del ecosistema para upgrade seguro

## 1) NocoBase (AG_NB_Apps, AG_Hospital_Organizador)

## Estado observado

1. Releases activas en repo oficial (incluyendo ramas beta recientes).
2. Roadmap publico con foco en NocoBase v2 y extensibilidad empresarial.

## Implicaciones

1. Proyectos en NocoBase deben separar plan de estabilidad (produccion) y plan de innovacion (labs/v2).
2. No mezclar plugins experimentales con flujos clinicos productivos sin entorno de staging.

## Recomendaciones

1. Definir matriz de plugins permitidos/prohibidos por dominio (hospital privado/publico).
2. Implementar smoke tests post-upgrade de:
- autenticacion/roles
- workflows criticos
- exportaciones/reportes
3. Mantener bitacora de compatibilidad plugin-version por cada app NocoBase.

## 2) Docker + Compose + MCP Docker

## Estado observado

1. Docker mantiene notas de version de Compose en docs oficiales.
2. Docker MCP gateway presenta releases recientes y cambios breaking en versiones previas.

## Implicaciones

1. Integraciones agenticas sobre Docker necesitan control de version y pruebas de contrato.
2. Cambios de output en gateway pueden romper automatizaciones parser-dependientes.

## Recomendaciones

1. Pin de version de Compose en CI/CD de proyectos criticos.
2. Version lock y contract test para Docker MCP gateway.
3. Regla obligatoria: no permitir agentes con permisos de Docker en entornos no aislados.

## 3) Proxmox VE (infraestructura)

## Estado observado

1. Proxmox VE 9.0 fue publicado (2025-08-05) con base Debian 13.
2. Proxmox mantiene roadmap oficial (VE9.x planificado, incluyendo 9.1).

## Implicaciones

1. Saltar mayor version sin precheck rompe continuidad de infraestructura agentica.
2. Se requiere runbook de backup/rollback por cluster antes de upgrade mayor.

## Recomendaciones

1. Ejecutar readiness checklist pre-VE9:
- backup verificado
- compatibilidad de storage/network/plugins
- prueba de restauracion
2. Ventana de upgrade por lotes (canary -> parcial -> completo).
3. Post-upgrade audit de seguridad y disponibilidad.

## 4) Matriz de riesgo de upgrade por plataforma

| Plataforma | Riesgo principal | Severidad | Mitigacion prioritaria |
|---|---|---|---|
| NocoBase | incompatibilidad de plugins | Alta | staging + smoke tests funcionales |
| Docker MCP | cambios de contrato de salida | Alta | version pin + contract tests |
| Docker Compose | drift entre entornos | Media | lock de version en CI |
| Proxmox VE9 | indisponibilidad por upgrade mayor | Alta | canary + rollback verificado |

## 5) Fuentes primarias

- NocoBase releases: https://github.com/nocobase/nocobase/releases
- NocoBase roadmap: https://www.nocobase.com/en/roadmap
- Docker Compose release notes: https://docs.docker.com/compose/releases/release-notes/
- Docker MCP gateway releases: https://github.com/docker/mcp-gateway/releases
- Proxmox VE 9 release announcement: https://www.proxmox.com/en/about/company-details/press-releases/proxmox-virtual-environment-9-0
- Proxmox roadmap: https://pve.proxmox.com/wiki/Roadmap

