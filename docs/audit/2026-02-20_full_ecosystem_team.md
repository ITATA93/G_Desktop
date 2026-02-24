# Auditoría Completa — AG_Orquesta_Desk (Master Orchestrator)

**Fecha**: 2026-02-20
**Ejecutor**: Agent Teams (Claude Opus 4.6 x3)
**Scope**: Proyecto completo `AG_Orquesta_Desk` + interacciones con satélites
**Commit base**: `e644eb5` (branch `master`)

---

## Resumen Ejecutivo

| Dimensión | Veredicto | Hallazgos |
|-----------|-----------|-----------|
| Calidad de Código | NEEDS_CHANGES | 4 críticos, 9 medios, 7 bajos |
| Cobertura de Tests | NEEDS_CHANGES | 0% inicial, 79 tests creados (~28%) |
| Documentación | NEEDS_CHANGES | README incorrecto, 15+ artefactos obsoletos, 14+ refs rotas |
| **Veredicto Global** | **NEEDS_CHANGES** | Acciones prioritarias requeridas antes de estabilizar |

---

## Agente 1: Code Reviewer

### Inventario de Scripts Auditados

| # | Script | Líneas | Rol | Riesgo |
|---|--------|--------|-----|--------|
| 1 | `env_resolver.py` | 301 | Detección de entorno, resolución de paths | P0 |
| 2 | `cross_task.py` | 797 | CRUD de tareas cross-repo, gestión de contador | P0 |
| 3 | `propagate.py` | 258 | Detección de drift de templates + auto-apply + git commit | P1 |
| 4 | `audit_ecosystem.py` | 735 | Escaneo de seguridad, grading de normalización | P1 |
| 5 | `ecosystem_dashboard.py` | 254 | Dashboard de salud basado en registry | P2 |
| 6 | `knowledge_sync.py` | 667 | Parsing de DEVLOG, sync de vault | P2 |
| 7 | `memory_sync.py` | 240 | Memoria transversal, dashboard de estado | P2 |
| 8 | `agent_health_check.py` | 210 | Validación de manifesto/governance | P3 |
| 9 | `agent_selftest.py` | 296 | Scoring de readiness de agentes | P3 |
| 10 | `template_sync.py` | 111 | Sync de archivos a directorios template | P2 |

### Hallazgos Críticos

#### C-01: Contraseñas reales en código fuente

- **Archivo**: `scripts/audit_ecosystem.py` (líneas 80-89)
- **Archivo**: `scripts/temp/audit_ecosystem.py` (líneas 41-43)
- **Archivo**: `scripts/temp/audit_plantilla.py` (línea 21)

```python
KNOWN_CREDENTIALS = [
    {"pattern": "dev-secret-key", "label": "default secret key", "severity": "high"},
    {"pattern": "hkEVC9AFVjFeRTkp", "label": "SIDRA DB password", "severity": "critical"},
    {"pattern": "sd260710sd", "label": "IRIS DB password", "severity": "critical"},
    {"pattern": "password123", "label": "weak password", "severity": "high"},
]
```

Contraseñas de producción de SIDRA e IRIS embebidas como literales string en el script de escaneo. Aunque el propósito es detección, esto commitea credenciales reales al repositorio Git. Cualquier persona con acceso de lectura puede extraerlas.

**Recomendación**: Reemplazar contraseñas literales con comparaciones de hash (SHA-256), o cargarlas desde un archivo de config separado en `.gitignore`.

---

#### C-02: `--no-verify` presente en `audit_ecosystem.py`

- **Archivo**: `scripts/audit_ecosystem.py` (línea 328)

```python
subprocess.run(
    ["git", "commit", "--no-verify", "-m", msg],
    cwd=project_dir,
    capture_output=True,
    timeout=10,
)
```

El FINAL-MASTER-PLAN.md marca esto como "[~] Skipped: user vetoed to avoid breaking automations." Sin embargo, `propagate.py` ya fue actualizado para remover `--no-verify` (confirmado en git diff), pero `audit_ecosystem.py` y `scripts/temp/commit_satellites.py` lo retienen. Esto crea inconsistencia: la ruta de propagación respeta pre-commit hooks, pero la ruta de auto-fix no.

**Recomendación**: Remover `--no-verify` de `audit_ecosystem.py` para ser consistente con `propagate.py`, o implementar un tag de commit seguro (ej. `[template-sync]`) que los pre-commit hooks puedan whitelist.

---

#### C-03: `scripts/temp/commit_satellites.py` — `--no-verify` + path legacy roto

- **Archivo**: `scripts/temp/commit_satellites.py` (líneas 6-12)

```python
AG_PROY = Path(r"C:\_Repositorio\AG_Proyectos")
for d in sorted(AG_PROY.iterdir()):
    ...
    subprocess.run(
        ["git", "commit", "--no-verify", "-m", "feat(tasks): ..."],
        cwd=str(d), capture_output=True, text=True
    )
```

Commitea ciegamente en cada repo satélite con `--no-verify` y usa un path hardcodeado completamente incorrecto (`C:\_Repositorio`) que no coincide con el entorno actual (`W:\Antigravity_OS`). Si el path existiera, commitearía en los repos equivocados.

**Recomendación**: Eliminar este script o migrarlo a `env_resolver.py` y remover `--no-verify`.

---

#### C-04: Archivo `.env` tracked en git

- **Archivo**: `.env`

El archivo `.env` existe en el working tree y fue parte del commit inicial. Su contenido es idéntico a `.env.example` (todos placeholders comentados). Aunque no hay secretos reales actualmente, `.env` no debería estar commiteado. Si un usuario llena API keys reales, serían staged automáticamente en el próximo `git add .`.

El `.gitignore` lista `.env` (línea 6), pero como ya fue tracked en el commit inicial, git continuará trackeándolo.

**Recomendación**: Ejecutar `git rm --cached .env` para destrackear el archivo preservándolo localmente.

---

### Hallazgos Medios

#### M-01: Corrupción UTF-8 BOM en archivos `.agent/`

**Archivos afectados**:
- `.agent/rules/project-rules.md`
- `.agent/skills/project-init.md`
- `.agent/skills/session-management.md`
- `.agent/workflows/monthly-insights.md`

El diff muestra corrupción sistemática de encoding: em-dashes convirtiéndose en `\xe2\x80\x94`, flechas en `\xe2\x86\x92`, símbolos de sección en `\xc2\xa7`. Un marcador BOM (`\xef\xbb\xbf`) fue prepended a varios archivos. Los archivos fueron re-guardados con encoding diferente (UTF-8 con BOM desde un editor Windows).

**Recomendación**: Estandarizar encoding a UTF-8 sin BOM. Usar un `.editorconfig` para enforcement.

---

#### M-02: Scripts con paths hardcodeados `C:\_Repositorio`

| Script | Path hardcodeado |
|--------|-----------------|
| `agent_selftest.py` (L22-24) | `C:\_Repositorio` |
| `memory_sync.py` (L24-26) | `C:\_Repositorio` |
| `scripts/temp/audit_ecosystem.py` (L13) | `C:\_Repositorio` |
| `scripts/temp/commit_satellites.py` (L6) | `C:\_Repositorio\AG_Proyectos` |

El entorno actual es `W:\Antigravity_OS` (confirmado via `config/environments.json`). Estos scripts NO han sido actualizados para usar `env_resolver.py` y fallarán silenciosamente o crashearán.

Scripts que SÍ fueron migrados: `propagate.py`, `cross_task.py`, `audit_ecosystem.py`, `ecosystem_dashboard.py`.

**Recomendación**: Migrar `agent_selftest.py` y `memory_sync.py` al patrón `env_resolver`. Eliminar o archivar scripts temp.

---

#### M-03: Import desprotegido en `ecosystem_dashboard.py`

- **Archivo**: `scripts/ecosystem_dashboard.py` (línea 189)

```python
from env_resolver import get_environment_id
```

Este import está dentro del cuerpo de `print_dashboard()` pero FUERA de try/except. El import al inicio del archivo (línea 24) sí está protegido, pero este no. Si `env_resolver` no está en `sys.path`, crasheará con `ImportError`.

**Recomendación**: Envolver en try/except con el patrón existente.

---

#### M-04: `knowledge_sync.py` depende de módulo inexistente `core.vault`

- **Archivo**: `scripts/knowledge_sync.py` (líneas 17-18)

```python
_sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from core.vault import KnowledgeVault
```

Importa desde `src/core/vault.py`, pero AG_Orquesta_Desk no tiene directorio `src/` (correctamente, per CLAUDE.md). Este script fue heredado de AG_Plantilla y crasheará en import.

**Recomendación**: Remover la dependencia de vault o hacer el import condicional con fallback.

---

#### M-05: `ARCHITECTURE.md` con información obsoleta

- **Archivo**: `docs/architecture/ARCHITECTURE.md`

Inconsistencias:
1. Lista todos los sub-agentes como `Vendor: Gemini`, pero `manifest.json` muestra `code-reviewer: claude`, `db-analyst: claude`, `researcher: codex`
2. Referencia invocación `gemini -a {agent} --yolo --sandbox seatbelt` (obsoleta)
3. Referencia `TODO.md` en lugar de `TASKS.md`
4. Dice "Maximum 4 agents simultaneously" pero `manifest.json` dice `max_parallel_agents: 5`

**Recomendación**: Actualizar ARCHITECTURE.md para reflejar vendors, invocación y naming actuales.

---

#### M-06: `cross_task.py` escribe a AG_Plantilla sin validación previa

- **Archivo**: `scripts/cross_task.py` (líneas 52-53)

```python
INDEX_PATH = PLANTILLA_DIR / "docs" / "TASKS_INDEX.md"
COUNTER_PATH = PLANTILLA_DIR / "data" / "task_counter.json"
```

Si AG_Plantilla no está clonado o disponible, `cross_task.py create` crasheará al intentar escribir a un path inexistente.

**Recomendación**: Agregar validación de disponibilidad de AG_Plantilla al inicio de operaciones de escritura.

---

#### M-07: `propagate.py` usa `git add .` inseguro

- **Archivo**: `scripts/propagate.py` (líneas 200-221)

La función `cmd_apply` escribe contenido template a proyectos satélite y auto-commitea via `git add . && git commit`. El `git add .` stagea TODOS los cambios del repo satélite, no solo el archivo propagado. Si un desarrollador tiene trabajo uncommitted, esto incluiría cambios no relacionados.

**Recomendación**: Cambiar `git add .` por `git add <archivo_específico>`.

---

#### M-08: GitHub Workflow eliminado sin reemplazo

- **Archivo**: `.github/workflows/release.yml` (eliminado en working tree)

El workflow de release fue eliminado. El CHANGELOG menciona CI/CD en v1.8.0 (`ci.yml`). Ahora hay cero validación automatizada. `.pre-commit-config.yaml` existe pero sin mecanismo de enforcement en CI.

**Recomendación**: Documentar la eliminación deliberada de CI/CD. Considerar workflow mínimo de lint.

---

#### M-09: `env_resolver.py` fallback puede retornar entorno inalcanzable

- **Archivo**: `scripts/env_resolver.py` (líneas 86-94)

El paso 4 (fallback) retorna cualquier entorno marcado `is_default` SIN verificar si su path existe. Si el entorno "notebook" (que es `is_default: true` con path `C:\_Repositorio`) es alcanzado como fallback, la función retorna un path inexistente.

**Recomendación**: Agregar check `base.exists()` al fallback default.

---

### Hallazgos Bajos / Sugerencias

| ID | Hallazgo |
|----|----------|
| L-01 | `TASKS_INDEX.md` duplicado en AG_Orquesta y AG_Plantilla — no está claro cuál es autoritativo |
| L-02 | `AGENTS.md` describe Codex CLI genérico, no customizado para el Orchestrator |
| L-03 | `.env` y `.env.example` contienen refs a `APP_PORT=3000`, JWT secrets — no aplican al orquestador |
| L-04 | `project-rules.md` referencia `docs/decisions/` con solo un template y un ADR heredado |
| L-05 | `session-management.md` instruye ejecutar `knowledge_sync.py` que siempre crasheará (ver M-04) |
| L-06 | `AG_Orquesta.code-workspace` no tiene sección `settings` ni `extensions` |
| L-07 | `docs/audit/` tiene 20+ reportes — los >30 días deberían archivarse per output governance |

### Observaciones Positivas

1. **Patrón env_resolver sólido** — La migración a `env_resolver.py` con try/except fallback está bien implementada en los 4 scripts principales
2. **Remoción correcta de `--no-verify` en `propagate.py`** — Ahora respeta pre-commit hooks
3. **Separación de concerns limpia** — CLAUDE.md establece correctamente que esto es un orquestador, no una aplicación
4. **`cross_task.py` bien diseñado** — Sistema de delegación con dual-write, IDs secuenciales y normalize
5. **`.gitignore` comprehensivo** — Cubre secrets, caches, databases, agent logs, temporales
6. **`project_registry.json` bien mantenido** — 13 proyectos registrados con paths relativos y categorías
7. **FINAL-MASTER-PLAN honesto** — Items saltados marcados con `[~]` y rationale documentado

---

## Agente 2: Test Writer

### Estado Inicial de Tests

**Cobertura previa: 0% CONFIRMADO.**

- Sin directorio `tests/`
- Sin `pytest.ini`, `pyproject.toml`, `setup.cfg`, ni `conftest.py`
- Sin archivos `test_*.py` o `*_test.py` en ningún lugar
- Sin `requirements.txt` ni declaraciones de dependencias de test

### Tests Creados

| Archivo | Tests | Cubre |
|---------|-------|-------|
| `tests/conftest.py` | -- | Fixtures compartidos: `tmp_ecosystem`, `environments_json`, `project_registry_json` |
| `tests/test_env_resolver.py` | 18 | `_load_config`, `_save_config`, `detect_environment` (6 casos), `get_repo_root`, `get_projects_dirs`, `list_ag_projects`, `register_environment` |
| `tests/test_cross_task.py` | 17 | `get_next_task_id` (4), `find_project_root` (4), `ensure_tasks_file`, `format_task_entry` (4), `insert_task` (3), `parse_tasks_from_file` (3) |
| `tests/test_propagate.py` | 10 | `get_all_projects`, `get_template_content` (4), `compute_drift` (3), `cmd_apply` |
| `tests/test_audit_ecosystem.py` | 23 | `is_safe_context` (8), `scan_security` (6), `grade_project` (5), `check_content_quality` (4) |
| `tests/test_ecosystem_dashboard.py` | 8 | `resolve_project_path`, `check_project_health` (4), `load_registry` (2) |
| `pytest.ini` | -- | Configuración del test runner |

**Resultado: 79 tests, todos pasando en 0.19 segundos.**

### Cobertura por Script

| Script | Funciones | Testeadas | Cobertura |
|--------|-----------|-----------|-----------|
| `env_resolver.py` | 12 | 8 | ~67% |
| `cross_task.py` | 14 | 7 | ~50% |
| `propagate.py` | 7 | 5 | ~71% |
| `audit_ecosystem.py` | 13 | 4 | ~31% |
| `ecosystem_dashboard.py` | 7 | 3 | ~43% |
| `knowledge_sync.py` | 14 | 0 | 0% |
| `memory_sync.py` | 8 | 0 | 0% |
| `agent_health_check.py` | 2 | 0 | 0% |
| `agent_selftest.py` | 8 | 0 | 0% |
| `template_sync.py` | 2 | 0 | 0% |
| `bootstrap_environment.py` | 6 | 0 | 0% |
| Scripts temp (4) | ~4 | 0 | 0% |

**Cobertura estimada: ~28% (27 de 97 funciones testeadas).**

### Paths No Testeados Prioritarios

1. **`cmd_create()` y `cmd_update()`** en `cross_task.py` — dual-write end-to-end
2. **Git auto-commit** en `propagate.py` — `git add .` + `git commit` en cada proyecto
3. **`fix_missing_files()`** en `audit_ecosystem.py` — copia desde template + git commit
4. **`memory_sync.py`** completo — paths hardcodeados impiden testing sin refactoreo
5. **`knowledge_sync.py`** funciones de parsing — import de `core.vault` bloquea

### Problemas de Testabilidad

| Problema | Scripts Afectados | Recomendación |
|----------|-------------------|---------------|
| Paths hardcodeados | `memory_sync.py`, `agent_selftest.py`, 4 scripts temp | Migrar a `env_resolver` |
| Estado global mutable | `agent_health_check.py` | Pasar `results` como parámetro |
| Import-time side effects | `knowledge_sync.py` | Hacer import lazy o guardar con try/except |
| Exception swallowing silencioso | `propagate.py:220`, `audit_ecosystem.py:334` | Loguear a stderr como mínimo |
| Input interactivo | `bootstrap_environment.py` | Flag `--non-interactive` o inyección de dependencia |

---

## Agente 3: Doc Writer

### Inventario de Documentación

| Categoría | Archivos | Estado |
|-----------|----------|--------|
| **Root docs** | CLAUDE.md, GEMINI.md, AGENTS.md, README.md, LICENSE | README incorrecto, resto OK |
| **Changelog/Devlog** | CHANGELOG.md, DEVLOG.md | Frescos (2026-02-20) |
| **Arquitectura** | `docs/architecture/ARCHITECTURE.md`, `docs/architecture/middleware.md` | Desactualizado + template artifact |
| **Standards** | `docs/standards/output_governance.md` | OK |
| **Plataforma** | `docs/PLATFORM.md`, `docs/ROUTING.md` | ROUTING tiene 7 refs de path antiguo |
| **Tasks** | `docs/TASKS.md`, `docs/TASKS_INDEX.md` | OK |
| **Auditorías** | `docs/audit/` (20+ archivos) | Necesita archivado |
| **API** | `docs/api/API.md` | Template artifact — no aplica |
| **Database** | `docs/database/DATABASE.md` | Template artifact — no aplica |
| **Observability** | `docs/observability/OBSERVABILITY.md` | Template artifact — no aplica |
| **Agent config** | `.agent/rules/`, `.agent/skills/`, `.agent/workflows/` | Encoding corrupto, refs rotas |

### Hallazgo Principal: README.md Incorrecto

El README raíz describe **AG_Plantilla** (el proyecto template) con sus directorios `_global-profile/` y `_template/`, scripts de instalación, y tipos de proyecto. **Nada de esto aplica al Master Orchestrator**. El README necesita reescritura completa.

### Documentos Template Obsoletos (Para Eliminar)

Tres subdirectorios completos + 1 archivo son residuos del origen AG_Plantilla:

- `docs/api/API.md` — Describe endpoints FastAPI, esquemas Pydantic
- `docs/database/DATABASE.md` — Describe schemas de base de datos, migraciones Alembic
- `docs/observability/OBSERVABILITY.md` — Describe métricas Prometheus, dashboards Grafana
- `docs/architecture/middleware.md` — Describe middleware de aplicación

### Referencias Cruzadas Rotas (14+)

| Documento | Referencia | Estado |
|-----------|-----------|--------|
| Múltiples docs | `src/main.py` | No existe (correcto per CLAUDE.md) |
| Múltiples docs | `src/config.py` | No existe |
| ROUTING.md (7 refs) | `C:\_Repositorio\AG_Proyectos\` | Path antiguo — ahora es `W:\Antigravity_OS\` |
| ARCHITECTURE.md | `TODO.md` | Renombrado a `TASKS.md` |
| session-management.md | `scripts/knowledge_sync.py` | Existe pero siempre crashea |

### Positivo

- CHANGELOG.md sigue formato Keep a Changelog, v1.0.0 hasta v2.6.0, con entradas del día
- DEVLOG.md refleja trabajo reciente con sesiones bien estructuradas
- `.agent/` directory bien organizado con rules, skills, workflows
- PLATFORM.md y output_governance operacionalmente valiosos
- FINAL-MASTER-PLAN honestamente trackea items saltados

---

## Plan de Acción Consolidado

### Prioridad Inmediata — Seguridad

| # | Acción | Esfuerzo |
|---|--------|----------|
| 1 | Hashear credenciales en `audit_ecosystem.py` (SHA-256) | Bajo |
| 2 | `git rm --cached .env` | Trivial |
| 3 | Eliminar `scripts/temp/commit_satellites.py` | Trivial |
| 4 | Remover `--no-verify` de `audit_ecosystem.py` | Trivial |

### Prioridad Alta — Estabilidad

| # | Acción | Esfuerzo |
|---|--------|----------|
| 5 | Migrar `agent_selftest.py` y `memory_sync.py` a `env_resolver` | Medio |
| 6 | Reescribir README.md para el Master Orchestrator | Medio |
| 7 | Eliminar docs template: `docs/api/`, `docs/database/`, `docs/observability/`, `middleware.md` | Bajo |
| 8 | Cambiar `git add .` por `git add <archivo>` en `propagate.py` | Bajo |
| 9 | Normalizar encoding UTF-8 sin BOM en archivos `.agent/` | Bajo |
| 10 | Proteger import en `ecosystem_dashboard.py:189` | Trivial |

### Prioridad Media — Calidad

| # | Acción | Esfuerzo |
|---|--------|----------|
| 11 | Actualizar ARCHITECTURE.md (vendors, max_parallel, invocación) | Medio |
| 12 | Corregir 7 refs de paths en ROUTING.md | Bajo |
| 13 | Hacer import lazy de `core.vault` en `knowledge_sync.py` | Bajo |
| 14 | Crear `requirements-dev.txt` con pytest | Trivial |
| 15 | Archivar auditorías >30 días en `docs/audit/_archive/` | Bajo |
| 16 | Agregar `.editorconfig` para estandarizar encoding | Trivial |

### Sugerencias

| # | Acción | Esfuerzo |
|---|--------|----------|
| 17 | Tests para `cmd_create`/`cmd_update` de `cross_task.py` | Medio |
| 18 | Refactorizar estado global en `agent_health_check.py` | Bajo |
| 19 | CI mínimo con GitHub Action para pytest | Bajo |
| 20 | Completar settings en `AG_Orquesta.code-workspace` | Trivial |

---

*Reporte generado por Agent Teams (Code Reviewer + Test Writer + Doc Writer) — Claude Opus 4.6*
