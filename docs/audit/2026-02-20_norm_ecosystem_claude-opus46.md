# Auditoría de Normalización del Ecosistema Antigravity

> **Fecha:** 2026-02-20
> **Ejecutado por:** Claude Opus 4.6 (AG_Orquesta_Desk)
> **Scope:** 14 proyectos (1 orchestrator + 1 template + 12 satélites)

---

## 1. Hallazgo Principal: AG_Orquesta_Desk vs AG_Plantilla

Ambos directorios son clones del **mismo repositorio git** (`ITATA93/AG_Plantilla.git`, HEAD = `cc8cffd`), pero con roles distintos:

| Aspecto | AG_Plantilla | AG_Orquesta_Desk |
|---------|-------------|------------------|
| **Rol** | Template + codebase completo | Orchestrator (solo config + docs) |
| **Archivos en working tree** | Completo (~7,500) | Reducido (~50) |
| **`.subagents/`** | Presente | BORRADO del filesystem |
| **`src/`, `tests/`, `scripts/`** | Presentes | BORRADOS del filesystem |
| **CLAUDE.md** | Template genérico (referencia PLATFORM.md) | Reescrito como Orchestrator profile |
| **GEMINI.md** | Template genérico (referencia PLATFORM.md) | Reescrito como Master Orchestrator |

### 1.1 Problema Crítico: 7,234 archivos deleted en git

AG_Orquesta_Desk tiene **7,234 archivos marcados como `D` (deleted)** en su working tree. Esto significa que un `git add -A && git commit` desde AG_Orquesta_Desk **destruiría el repositorio** eliminando todo el código fuente, scripts, subagents y templates.

### 1.2 CLAUDE.md incompatible

- El CLAUDE.md de AG_Orquesta_Desk (leído por Claude Code) referencia `cross_task.py` en `W:\...\AG_Plantilla\scripts\` (path absoluto) y define reglas de orchestrator.
- El CLAUDE.md de AG_Plantilla (commiteado en git) referencia `PLATFORM.md`, `ROUTING.md`, `.subagents/dispatch.sh` — archivos que **no existen** en el filesystem de AG_Orquesta_Desk.

---

## 2. Normalización de AG_Plantilla (fuente de verdad)

**Score: 16/16 markers — PASS COMPLETO**

| # | Marker | Estado |
|---|--------|--------|
| 1 | `.subagents/manifest.json` v3.0 | PASS |
| 2 | `.subagents/dispatch.sh` | PASS |
| 3 | `.subagents/dispatch.ps1` | PASS |
| 4 | `CLAUDE.md` (referencia PLATFORM.md/ROUTING.md) | PASS |
| 5 | `GEMINI.md` (referencia PLATFORM.md/ROUTING.md) | PASS |
| 6 | `AGENTS.md` | PASS |
| 7 | `CHANGELOG.md` | PASS |
| 8 | `docs/TASKS.md` | PASS |
| 9 | `docs/DEVLOG.md` | PASS |
| 10 | `.gemini/brain/` | PASS |
| 11 | `.agent/rules/` | PASS |
| 12 | `.agent/workflows/` | PASS |
| 13 | `.claude/commands/` + `.claude/skills/` | PASS |
| 14 | `pyproject.toml` + `requirements.txt` | PASS |
| 15 | `.gitignore` | PASS |
| 16 | `src/` + `tests/` | PASS |

---

## 3. Normalización de AG_Orquesta_Desk

**Score: 10/17 markers (58.8%) — NO NORMALIZADO**

| # | Marker | Estado | Nota |
|---|--------|--------|------|
| 1 | `.subagents/manifest.json` | FAIL | Directorio `.subagents/` no existe |
| 2 | `.subagents/dispatch.sh` | FAIL | Directorio `.subagents/` no existe |
| 3 | `.subagents/dispatch.ps1` | FAIL | Directorio `.subagents/` no existe |
| 4 | `CLAUDE.md` | PASS | Reescrito como Orchestrator profile |
| 5 | `GEMINI.md` | PASS | Reescrito como Master Orchestrator |
| 6 | `AGENTS.md` | PASS | |
| 7 | `CHANGELOG.md` | PASS | Comparte con AG_Plantilla |
| 8 | `docs/TASKS.md` | PASS | |
| 9 | `docs/DEVLOG.md` | PASS | |
| 10 | `.gemini/brain/` | PASS | |
| 11 | `.agent/rules/` | PASS | |
| 12 | `.agent/workflows/` | PASS | |
| 13 | `.claude/commands/` + `.claude/skills/` | PASS | |
| 14 | `pyproject.toml` / `requirements.txt` | FAIL | No existen |
| 15 | `.gitignore` | PASS | |
| 16 | `src/` | FAIL | By design (orchestrator, no code) |
| 17 | `tests/` | FAIL | By design (orchestrator, no code) |

**Nota:** Los items 14/16/17 son "by design" según el GEMINI.md que establece que AG_Orquesta no es un proyecto de código. Sin embargo, los items 1-3 (`.subagents/`) son **críticos** porque tanto CLAUDE.md como GEMINI.md referencian dispatch scripts y manifest.

---

## 4. Normalización de los 12 Proyectos Satélite

### Criterios evaluados (7 markers)

1. `.subagents/manifest.json` existe
2. `.subagents/dispatch.sh` existe
3. `CLAUDE.md` o `GEMINI.md` en raíz
4. `CHANGELOG.md` existe
5. `docs/` directorio existe
6. `.gemini/brain/` directorio existe
7. `.agent/` directorio existe

### Resultados

| Proyecto | Score | Estado | Faltantes |
|----------|-------|--------|-----------|
| AG_Consultas | 7/7 | **PASS** | — |
| AG_Hospital_Organizador | 7/7 | **PASS** | — |
| AG_Informatica_Medica | 7/7 | **PASS** | — |
| AG_NB_Apps | 7/7 | **PASS** | — |
| AG_Analizador_RCE | 6/7 | FAIL | `.gemini/brain/` |
| AG_DeepResearch_Salud_Chile | 6/7 | FAIL | `.gemini/brain/` |
| AG_Lists_Agent | 6/7 | FAIL | `.gemini/brain/` |
| AG_TrakCare_Explorer | 6/7 | FAIL | `.gemini/brain/` |
| AG_Notebook | 4/7 | FAIL | manifest, dispatch, CLAUDE.md, brain |
| AG_SV_Agent | 3/7 | FAIL | manifest, dispatch, CLAUDE.md, brain, `.agent/` |
| AG_Hospital | 3/7 | FAIL | manifest, dispatch, CLAUDE.md, brain, `.agent/` |
| AG_SD_Plantilla | 3/7 | FAIL | manifest, dispatch, CLAUDE.md, brain, `.agent/` |

**Resultado global: 4/12 PASS (33%), 8/12 FAIL (67%)**

### Distribución por severidad

```
Fully normalized (7/7):  4 proyectos  ████████░░░░░░░░  33%
Minor gap (6/7):         4 proyectos  ████████░░░░░░░░  33%
Severely broken (3-4/7): 4 proyectos  ████████░░░░░░░░  33%
```

---

## 5. `project_registry.json` vs Filesystem

### Estructura real del filesystem

```
W:\Antigravity_OS\
├── 00_CORE\
│   ├── AG_Orquesta_Desk\
│   ├── AG_Plantilla\
│   ├── AG_Notebook\
│   └── AG_SV_Agent\
├── 01_HOSPITAL_PRIVADO\
│   ├── AG_Analizador_RCE\
│   ├── AG_Consultas\
│   ├── AG_DeepResearch_Salud_Chile\
│   ├── AG_Hospital\
│   ├── AG_Hospital_Organizador\
│   ├── AG_Informatica_Medica\
│   ├── AG_Lists_Agent\
│   └── AG_TrakCare_Explorer\
└── 02_HOSPITAL_PUBLICO\
    ├── AG_NB_Apps\
    └── AG_SD_Plantilla\
```

### Discrepancias en paths del registry

El registry usa `path_relative` con base `AG_Proyectos/` (ej. `AG_Proyectos/AG_Analizador_RCE`), pero:

- **`AG_Proyectos/` no existe** en el filesystem
- La estructura real usa `00_CORE/`, `01_HOSPITAL_PRIVADO/`, `02_HOSPITAL_PUBLICO/`
- Los paths relativos del registry están **completamente desactualizados**

| Proyecto | Path en Registry | Path Real |
|----------|-----------------|-----------|
| AG_Orquesta_Desk | `00_CORE/AG_Orquesta_Desk` | `00_CORE/AG_Orquesta_Desk` |
| AG_Analizador_RCE | `AG_Proyectos/AG_Analizador_RCE` | `01_HOSPITAL_PRIVADO/AG_Analizador_RCE` |
| AG_Consultas | `AG_Proyectos/AG_Consultas` | `01_HOSPITAL_PRIVADO/AG_Consultas` |
| AG_Hospital | `AG_Proyectos/AG_Hospital` | `01_HOSPITAL_PRIVADO/AG_Hospital` |
| AG_NB_Apps | `AG_Proyectos/AG_NB_Apps` | `02_HOSPITAL_PUBLICO/AG_NB_Apps` |
| AG_SD_Plantilla | `AG_Proyectos/AG_SD_Plantilla` | `02_HOSPITAL_PUBLICO/AG_SD_Plantilla` |
| *(otros 7)* | `AG_Proyectos/...` | `01_HOSPITAL_PRIVADO/...` o `00_CORE/...` |

---

## 6. Workspace File

El archivo `AG_Orquesta.code-workspace` lista 14 folders con paths relativos correctos para la estructura actual:

```
. (AG_Orquesta_Desk)
../AG_Notebook              → 00_CORE/AG_Notebook
../AG_Plantilla             → 00_CORE/AG_Plantilla
../AG_SV_Agent              → 00_CORE/AG_SV_Agent
../../01_HOSPITAL_PRIVADO/AG_*  → (8 proyectos)
../../02_HOSPITAL_PUBLICO/AG_*  → (2 proyectos)
```

El workspace file **sí refleja** la topología real. La inconsistencia está solo en `project_registry.json`.

---

## 7. Lista de Problemas por Severidad

### CRITICO

| ID | Problema | Impacto |
|----|----------|---------|
| C-01 | AG_Orquesta_Desk tiene 7,234 archivos `D` (deleted) en git | Un commit accidental destruye el repo |
| C-02 | AG_Orquesta_Desk comparte repo git con AG_Plantilla | Identidad del proyecto ambigua |

### ALTO

| ID | Problema | Impacto |
|----|----------|---------|
| H-01 | `project_registry.json` paths obsoletos (`AG_Proyectos/` no existe) | Scripts como `cross_task.py`, `audit_ecosystem.py` fallan al resolver paths |
| H-02 | 4 proyectos severamente des-normalizados (3/7): AG_SV_Agent, AG_Hospital, AG_SD_Plantilla, AG_Notebook | No pueden usar subagentes ni dispatch |
| H-03 | CLAUDE.md de AG_Orquesta_Desk referencia archivos inexistentes | Claude Code opera con instrucciones inconsistentes |

### MEDIO

| ID | Problema | Impacto |
|----|----------|---------|
| M-01 | 8/12 satélites sin `.gemini/brain/` | Memoria persistente de Gemini no funciona |
| M-02 | README.md de AG_Plantilla dice "AG_Plantilla/" en la estructura | Naming inconsistente |
| M-03 | AG_Orquesta_Desk no tiene repositorio git propio | No puede versionarse independientemente |

### BAJO

| ID | Problema | Impacto |
|----|----------|---------|
| L-01 | `AG_Plantilla.code-workspace` borrado de AG_Orquesta_Desk, reemplazado por `AG_Orquesta.code-workspace` (sin commitear) | Cosmético |
| L-02 | 29 archivos untracked en AG_Plantilla | Pendientes de commit/gitignore |

---

## 8. Recomendaciones

### Fase 1: Desacoplar AG_Orquesta_Desk (resuelve C-01, C-02, M-03)

1. Crear repositorio git independiente `ITATA93/AG_Orquesta_Desk`
2. Inicializar con solo los archivos que le pertenecen (`.agent/`, `.claude/`, `.codex/`, `.gemini/`, `docs/`, `CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, `CHANGELOG.md`, `README.md`, `.code-workspace`)
3. Eliminar el `.git` actual que comparte con AG_Plantilla

### Fase 2: Actualizar Registry (resuelve H-01)

1. Actualizar `project_registry.json` paths relativos a la estructura `00_CORE/`, `01_HOSPITAL_PRIVADO/`, `02_HOSPITAL_PUBLICO/`
2. Agregar AG_Plantilla como proyecto en el registry si no está
3. Actualizar `env_resolver.py` para usar los nuevos paths

### Fase 3: Propagar normalización (resuelve H-02, M-01)

1. Ejecutar `audit_ecosystem.py --fix` para propagar archivos faltantes desde `_template/`
2. Crear `.gemini/brain/` en los 8 proyectos que lo necesitan
3. Propagar `.subagents/manifest.json`, `dispatch.sh`, `CLAUDE.md`, `.agent/` a los 4 proyectos críticos

### Fase 4: Alinear documentación (resuelve H-03, M-02)

1. Actualizar CLAUDE.md de AG_Orquesta_Desk para no referenciar archivos que no existen
2. Actualizar README.md de AG_Plantilla
3. Commitear archivos untracked en AG_Plantilla

---

## 9. Scorecard Final

| Componente | Estado | Score |
|-----------|--------|-------|
| AG_Plantilla (template) | **NORMALIZADO** | 16/16 (100%) |
| AG_Orquesta_Desk (orchestrator) | **NO NORMALIZADO** | 10/17 (59%) |
| Satélites normalizados | 4/12 | 33% |
| Satélites parciales (6/7) | 4/12 | 33% |
| Satélites críticos (3-4/7) | 4/12 | 33% |
| Registry accuracy | **DESACTUALIZADO** | paths incorrectos |
| Workspace file accuracy | **CORRECTO** | paths válidos |

**Normalización global estimada: ~50%**

---

*Generado desde AG_Orquesta_Desk por Claude Opus 4.6*
*Archivo: `docs/audit/normalization-audit-2026-02-20.md`*
