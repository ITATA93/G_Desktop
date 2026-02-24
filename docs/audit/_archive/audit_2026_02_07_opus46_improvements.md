# Evaluación de Mejoras — Claude Opus 4.6 para AG_Plantilla

**Fecha**: 2026-02-07
**Modelo evaluado**: Claude Opus 4.6 (lanzado 2026-02-05)
**Proyecto**: AG_Plantilla v1.2.1
**Auditor**: Antigravity Architect

---

## Resumen Ejecutivo

Claude Opus 4.6 introduce **6 mejoras mayores** que impactan directamente al ecosistema Antigravity. Este reporte evalúa cada una contra el estado actual de AG_Plantilla y propone acciones concretas, priorizadas por impacto.

| #   | Mejora Opus 4.6             | Estado en AG_Plantilla | Impacto | Prioridad |
| --- | --------------------------- | ---------------------- | ------- | --------- |
| 1   | Agent Teams (paralelos)     | ❌ No implementado      | 🔴 Alto  | P0        |
| 2   | Effort Controls (4 niveles) | ⚠️ Parcial (solo Codex) | 🔴 Alto  | P0        |
| 3   | Adaptive Thinking           | ❌ No implementado      | 🟡 Medio | P1        |
| 4   | Context Compaction API      | ❌ No implementado      | 🟡 Medio | P1        |
| 5   | 1M Context Window (beta)    | ❌ No configurado       | 🟡 Medio | P1        |
| 6   | 128K Output Tokens          | ❌ No configurado       | 🟢 Bajo  | P2        |
| 7   | `/insights` command         | ❌ No documentado       | 🟡 Medio | P1        |
| 8   | `/debug` command            | ❌ No documentado       | 🟢 Bajo  | P2        |
| 9   | `--from-pr` workflow        | ❌ No integrado         | 🟢 Bajo  | P2        |
| 10  | Streaming obligatorio       | ⚠️ No validado          | 🔴 Alto  | P0        |

---

## 1. 🔴 P0 — Agent Teams (Trabajo en Paralelo)

### Qué es
Opus 4.6 permite a Claude Code crear **equipos de agentes** que trabajan en paralelo bajo un agente supervisor. El lead agent puede crear múltiples sub-agentes, cada uno con su propia sesión, coordinándose autónomamente.

### Estado actual en AG_Plantilla
- El `manifest.json` define 7 agentes, pero **la ejecución es secuencial**.
- Claude ya soportaba `allow_parallel: true` en `claude_config`, pero no había soporte real del modelo para coordinación multi-agente.
- El dispatcher (`dispatch.sh`) es single-agent.

### Mejoras propuestas

#### 1.1 Actualizar `manifest.json` con configuración de Agent Teams
```json
{
  "agent_teams": {
    "enabled": true,
    "max_parallel_agents": 5,
    "supervisor_model": "opus-4.6",
    "coordination_mode": "autonomous"
  }
}
```

#### 1.2 Crear perfiles de equipo predefinidos
```json
{
  "teams": {
    "full-review": {
      "agents": ["code-reviewer", "test-writer", "doc-writer"],
      "mode": "parallel",
      "use_case": "Revisión completa pre-merge"
    },
    "feature-pipeline": {
      "agents": ["code-analyst", "test-writer", "code-reviewer"],
      "mode": "sequential",
      "use_case": "Pipeline TDD completo"
    },
    "deep-audit": {
      "agents": ["code-reviewer", "db-analyst", "deployer"],
      "mode": "parallel",
      "use_case": "Auditoría profunda de proyecto"
    }
  }
}
```

#### 1.3 Nuevo comando Claude: `/team-review`
Crear `.claude/commands/team-review.md` que invoque el equipo `full-review` en paralelo.

### Archivos a modificar
- `.subagents/manifest.json` — Agregar sección `agent_teams`
- `.claude/commands/team-review.md` — Nuevo comando
- `CLAUDE.md` — Documentar Agent Teams
- `GEMINI.md` — Actualizar capacidades de Claude

---

## 2. 🔴 P0 — Effort Controls (4 Niveles)

### Qué es
Opus 4.6 introduce un parámetro `effort` con 4 niveles: **low**, **medium**, **high** (default), **max**. Esto controla cuánto "piensa" el modelo antes de responder, balanceando inteligencia vs. costo vs. velocidad.

### Estado actual en AG_Plantilla
- Solo Codex tiene `effort` configurado en el manifest (`high`, `xhigh`, `medium`).
- Claude **no tiene** configuración de effort en `claude_config`.
- El clasificador de complejidad (NIVEL 1/2/3) **no mapea** a niveles de effort.

### Mejoras propuestas

#### 2.1 Mapeo Complejidad → Effort
```
┌──────────────────────────────────────────────────┐
│        MAPEO CLASIFICADOR → EFFORT               │
├──────────────────────────────────────────────────┤
│  NIVEL 1 (Directo)    → effort: "low"            │
│  NIVEL 2 (1 agente)   → effort: "high"           │
│  NIVEL 3 (Pipeline)   → effort: "max"            │
│                                                   │
│  Tareas de seguridad  → effort: "max" (override)  │
│  Documentación        → effort: "medium"           │
└──────────────────────────────────────────────────┘
```

#### 2.2 Actualizar `claude_config` en manifest.json
```json
"claude_config": {
  "model": "opus-4.6",
  "effort": "high",
  "allow_parallel": true,
  "adaptive_thinking": true
}
```

#### 2.3 Actualizar effort por agente
| Agente        | Effort actual (Codex) | Effort propuesto (Claude) |
| ------------- | --------------------- | ------------------------- |
| code-analyst  | high                  | high                      |
| code-reviewer | high                  | **max**                   |
| test-writer   | high                  | high                      |
| doc-writer    | medium                | **medium**                |
| db-analyst    | xhigh                 | **max**                   |
| deployer      | high                  | high                      |
| researcher    | xhigh                 | **max**                   |

### Archivos a modificar
- `.subagents/manifest.json` — Agregar `effort` a cada `claude_config`
- `GEMINI.md` — Documentar mapeo complejidad→effort
- `.subagents/schema.json` — Añadir `effort` al schema

---

## 3. 🟡 P1 — Adaptive Thinking

### Qué es
El modelo decide **dinámicamente** cuándo usar razonamiento extendido (extended thinking). Reemplaza el enfoque binario (thinking on/off) por uno contextual inteligente.

### Estado actual en AG_Plantilla
- `thinking_mode: true` está hardcodeado en `gemini_config` para algunos agentes.
- No hay configuración equivalente para Claude.

### Mejoras propuestas

#### 3.1 Agregar `adaptive_thinking` al manifest
```json
"claude_config": {
  "model": "opus-4.6",
  "adaptive_thinking": true,
  "effort": "high"
}
```

#### 3.2 Documentar cuándo forzar thinking
- **Siempre forzar** (`effort: "max"`): code-reviewer, db-analyst, researcher
- **Adaptativo** (default): code-analyst, test-writer, deployer
- **Mínimo** (`effort: "low"`): doc-writer para tareas simples

### Archivos a modificar
- `.subagents/manifest.json`
- `.subagents/schema.json`

---

## 4. 🟡 P1 — Context Compaction API

### Qué es
Cuando la conversación se acerca al límite de tokens, Claude **resume automáticamente** el contexto antiguo, generando un bloque compactado que preserva la información crítica. Se activa al ~75% del context window.

### Estado actual en AG_Plantilla
- No hay configuración de compaction.
- Las sesiones largas pierden contexto sin aviso.
- El `memory_sync.py` hace sync manual, pero no maneja compaction de sesión.

### Mejoras propuestas

#### 4.1 Agregar instrucciones de compaction a CLAUDE.md
```markdown
## Context Management
- Use `/compact` command proactively when working on long sessions
- Focus compaction on: "Preserve architecture decisions and file paths"
- CLAUDE.md serves as persistent context that survives compaction
```

#### 4.2 Nuevo workflow: session-aware compaction
Crear `.agent/workflows/long-session.md` con pasos para gestionar sesiones largas:
1. Al detectar sesión > 30 min, recomendar `/compact`
2. Antes de compactar, guardar estado en `docs/DEVLOG.md`
3. Post-compaction: re-leer `CLAUDE.md` y `GEMINI.md`

### Archivos a modificar/crear
- `CLAUDE.md` — Sección Context Management
- `.agent/workflows/long-session.md` — Nuevo workflow

---

## 5. 🟡 P1 — 1M Context Window

### Qué es
Opus 4.6 soporta **1 millón de tokens** de contexto (beta), sin degradación ("context rot"). Permite procesar codebases enteros, documentación extensa, o múltiples papers de investigación.

### Estado actual en AG_Plantilla
- No hay configuración que aproveche el contexto extendido.
- Los agentes no saben que pueden recibir archivos masivos.

### Mejoras propuestas

#### 5.1 Actualizar instrucciones de agentes
Agregar al briefing de `code-analyst` y `researcher`:
```
Tienes acceso a 1M tokens de contexto.
Para análisis de codebase completo, solicita TODOS los archivos relevantes.
No trabajes con fragmentos parciales cuando el contexto completo está disponible.
```

#### 5.2 Habilitar premium pricing awareness
Documentar en el manifest que requests > 200K tokens usan pricing premium ($10/M input vs $5/M input).

### Archivos a modificar
- `.subagents/manifest.json` — Agregar `context_window` a vendor config
- `CLAUDE.md` — Documentar pricing tiers

---

## 6. 🟡 P1 — `/insights` Command

### Qué es
Nuevo comando que analiza el historial de uso de los últimos 30 días y genera un **reporte HTML interactivo** con:
- Patrones de uso por proyecto
- Herramientas más utilizadas
- Puntos de fricción
- Sugerencias personalizadas

### Estado actual en AG_Plantilla
- No documentado en comandos disponibles.
- Los comandos Claude actuales son: `/project-status`, `/quick-review`, `/update-docs`, `/create-tests`, `/help`.

### Mejoras propuestas

#### 6.1 Documentar en CLAUDE.md
Agregar `/insights` a la tabla de comandos disponibles.

#### 6.2 Crear workflow de análisis periódico
```markdown
## Workflow: Monthly Insights Review
1. Run `/insights` at end of each month
2. Save report to `docs/audit/insights-YYYY-MM.html`
3. Review friction points and apply optimizations
```

### Archivos a modificar
- `CLAUDE.md` — Agregar comando a la tabla
- `.agent/workflows/monthly-insights.md` — Nuevo workflow

---

## 7. 🟢 P2 — 128K Output Tokens

### Qué es
Opus 4.6 permite salidas de hasta **128K tokens** (antes 64K). Requiere streaming obligatorio para requests con `max_tokens` altos.

### Impacto en AG_Plantilla
- Relevante para generación de documentación extensa, reportes de auditoría, y análisis de codebase completo.
- El streaming obligatorio puede afectar scripts que usen la API directamente.

### Mejora propuesta
- Documentar el requerimiento de streaming en la sección de API de CLAUDE.md.
- Validar que ningún script del proyecto use llamadas API síncronas con `max_tokens > 64K`.

---

## 8. 🟢 P2 — `/debug` Command y `--from-pr`

### `/debug`
Permite inspeccionar el estado de la sesión activa. Útil para troubleshooting.

### `--from-pr`
Resume sesiones vinculadas a un PR específico de GitHub. Facilita workflows de code review.

### Mejora propuesta
- Documentar ambos en `CLAUDE.md`.
- Integrar `--from-pr` con el workflow de code review existente.

---

## 9. 🔴 P0 — Streaming Obligatorio (Breaking Change)

### Qué es
Para requests con `max_tokens` altos, los SDKs ahora **requieren streaming** para prevenir timeouts HTTP. Se usa `.stream()` con `.get_final_message()`.

### Impacto en AG_Plantilla
- Si algún script o integración usa llamadas síncronas a la API de Claude, **podría romper**.
- Revisar: `src/services/`, `scripts/`, y cualquier integración API.

### Mejora propuesta
- Auditar todos los scripts que llaman a la API de Claude.
- Migrar a patrón streaming donde sea necesario.
- Agregar test de integración para validar streaming.

---

## 10. Actualización del Manifest de Vendors

### Estado actual
```json
"vendors": {
  "available": ["gemini", "claude", "codex"],
  "default": "gemini",
  "codex_partial": true
}
```

### Propuesta actualizada
```json
"vendors": {
  "available": ["gemini", "claude", "codex"],
  "default": "gemini",
  "codex_partial": true,
  "claude_capabilities": {
    "model": "opus-4.6",
    "context_window": "1M (beta)",
    "max_output_tokens": 128000,
    "effort_levels": ["low", "medium", "high", "max"],
    "adaptive_thinking": true,
    "agent_teams": true,
    "compaction_api": true,
    "streaming_required": true,
    "commands": ["/insights", "/debug", "/compact"],
    "pricing": {
      "standard": {"input": "$5/M", "output": "$25/M"},
      "premium_200k_plus": {"input": "$10/M", "output": "$37.50/M"}
    }
  }
}
```

---

## Plan de Implementación Propuesto

### Fase 1 — P0 (Semana 1)
| Tarea                        | Archivos                              | Estimado |
| ---------------------------- | ------------------------------------- | -------- |
| Agent Teams config           | manifest.json, schema.json, CLAUDE.md | 2h       |
| Effort Controls mapping      | manifest.json, GEMINI.md              | 1h       |
| Streaming audit              | src/services/, scripts/               | 1h       |
| Nuevo comando `/team-review` | .claude/commands/                     | 30min    |

### Fase 2 — P1 (Semana 2)
| Tarea                    | Archivos                     | Estimado |
| ------------------------ | ---------------------------- | -------- |
| Adaptive Thinking config | manifest.json                | 30min    |
| Compaction workflow      | .agent/workflows/, CLAUDE.md | 1h       |
| Context 1M documentation | manifest.json, CLAUDE.md     | 30min    |
| `/insights` integration  | CLAUDE.md, workflows/        | 1h       |

### Fase 3 — P2 (Semana 3)
| Tarea                       | Archivos      | Estimado |
| --------------------------- | ------------- | -------- |
| 128K output docs            | CLAUDE.md     | 15min    |
| `/debug` y `--from-pr` docs | CLAUDE.md     | 15min    |
| Vendor manifest update      | manifest.json | 30min    |
| Update CHANGELOG.md         | CHANGELOG.md  | 15min    |

---

## Conclusión

Claude Opus 4.6 representa un **salto significativo** para el ecosistema Antigravity. Las 3 mejoras de mayor impacto son:

1. **Agent Teams** — Habilita la ejecución paralela real de sub-agentes, algo que el sistema ya tenía diseñado conceptualmente pero no podía ejecutar.
2. **Effort Controls** — Permite alinear el clasificador de complejidad (NIVEL 1/2/3) con niveles reales del modelo, optimizando costo y tiempo.
3. **Streaming obligatorio** — Requiere auditoría inmediata para evitar breaking changes.

**Recomendación**: Implementar Fase 1 de inmediato y actualizar la versión del proyecto a **v1.3.0**.

---
**Status**: PENDING REVIEW
**Next Action**: Aprobación del usuario para proceder con Fase 1
