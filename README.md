# G_Desktop

> Satellite project in the Antigravity ecosystem.

**Domain:** `00_CORE`
**Status:** Active
**Orchestrator:** GEN_OS
**Prefix:** G_

## Proposito

Organizador del entorno de escritorio Windows para estaciones de desarrollo.
Gestiona configuracion de sistema, dotfiles, perfiles de shell, lanzadores de
aplicaciones y automatizacion del workspace de desarrollo.

## Arquitectura

```
G_Desktop/
  manifests/
    nos.yaml            # Schema de bases de datos Notion
  scripts/
    backup-notion.ts    # Backup de datos Notion
    validate-manifest.ts # Validacion de manifiestos
  prompts/              # Prompts reutilizables
  assets/               # Recursos estaticos
  docs/                 # Documentacion y estandares
  reports/              # Reportes generados
  logs/                 # Logs de ejecucion
  exports/              # Datos exportados
```

## Features

- **Desktop Configuration**: Shell profiles, terminal themes, PowerShell modules
- **Package Management**: Winget, Scoop, Chocolatey manifests and sync
- **Workspace Automation**: Window layouts, virtual desktops, hotkey configs
- **Dev Environment**: IDE settings, Git config, SSH key management, PATH optimization
- **System Tuning**: Service management, startup optimization, performance tweaks
- **Dotfile Sync**: Cross-machine configuration backup and restore

## Uso con Gemini CLI

```bash
# Iniciar sesion
gemini

# Auditar configuracion del desktop
gemini -p "Analiza los scripts de configuracion y sugiere mejoras"

# Validar manifiestos
npx tsx scripts/validate-manifest.ts
```

## Scripts Disponibles

```bash
# Validar manifiestos de Notion
npx tsx scripts/validate-manifest.ts

# Backup de datos Notion
npx tsx scripts/backup-notion.ts

# Dispatch de agente revisor
bash .subagents/dispatch.sh reviewer "Audit this project"

# Team workflow
bash .subagents/dispatch-team.sh code-and-review "Review recent changes"
```

## Configuracion

| Archivo | Proposito |
|---------|-----------|
| `GEMINI.md` | Instrucciones para Gemini CLI |
| `CLAUDE.md` | Instrucciones para Claude Code |
| `AGENTS.md` | Instrucciones para Codex CLI |
| `.gemini/settings.json` | Config de Gemini |
| `package.json` | Dependencias y scripts npm |
| `manifests/nos.yaml` | Schema de Notion OS |

## Contraparte AG

Derivado de `AG_Orquesta_Desk`. Misma funcionalidad de dominio con
infraestructura de agentes actualizada al estandar G_ multi-vendor.

## Licencia

MIT
