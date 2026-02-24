Now I have all the context needed. Here is my expert critique:

---

# Reporte de Cr├¡tica Experta ÔÇö Draft Master Plan (Gemini R3)

**Revisor**: Claude Opus 4.6 (Experto Auditor, Round 4)
**Fecha**: 2026-02-20
**Documento revisado**: `docs/audit/master-draft-plan.md`

---

## Veredicto General

El Draft Master Plan es una s├¡ntesis competente que identifica correctamente los problemas de alto nivel. Sin embargo, contiene **errores f├ícticos**, **omisiones de seguridad graves**, **secuenciaci├│n peligrosa**, y **propuestas operativamente imposibles** en su forma actual. Lo que sigue es una cr├¡tica destructiva fase por fase.

---

## Cr├¡tica de la Secci├│n 1: An├ílisis del Estado Actual

### 1.1 "El Orquestador Zombie" ÔÇö Parcialmente Incorrecto

**Lo que dice el plan**: *"Si se ejecuta `git commit -a`, se propagar├í la eliminaci├│n masiva hacia el repositorio origen (AG_Plantilla), destruyendo el c├│digo fuente."*

**Realidad verificada**: El repositorio `.git` de AG_Orquesta_Desk **no tiene remote configurado**. Revis├® `.git/config` directamente y no existe secci├│n `[remote "origin"]`. Un `git commit -a` en el orquestador **NO puede propagarse a AG_Plantilla** porque no hay push target. El riesgo no es "catastr├│fico" como se describe ÔÇö es un riesgo de **poluci├│n del historial local** y confusi├│n operativa, no de destrucci├│n remota.

**Falla del plan**: Se basa en un diagn├│stico exagerado para justificar la Fase 1. La justificaci├│n es correcta (el orquestador debe ser limpio), pero el escenario apocal├¡ptico es falso. Esto debilita la credibilidad del documento ante stakeholders t├®cnicos.

### 1.2 "85% del ecosistema est├í sordo" ÔÇö Correcto pero Superficial

El diagn├│stico es preciso: 11/12 proyectos carecen de `tasks_awareness` en su GEMINI.md, y 10/12 fallan el check de `gemini_keywords`. Sin embargo, **el plan no menciona que `cross_task.py` tambi├®n tiene fallback a `C:\_Repositorio`** (l├¡neas 36-49). Si el `env_resolver` import falla, `cross_task.py` buscar├í proyectos en una ruta que no existe en el entorno desktop (`W:\Antigravity_OS`). La sincronizaci├│n propuesta en la Fase 3 fallar├¡a silenciosamente en exactamente el entorno donde se necesita ejecutar.

### 1.3 "Exposici├│n de Credenciales" ÔÇö Correcto pero Incompleto

El plan menciona `AG_Consultas/herramientas/python/db_config.py` y "scripts de Caprini". Pero **omite que las contrase├▒as est├ín tambi├®n en `.vscode/settings.json`** ÔÇö 4 instancias de `sd260710sd` (IRIS) y 1 de `hkEVC9AFVjFeRTkp` (SIDRA). Los archivos `.vscode/settings.json` son particularmente peligrosos porque suelen quedar fuera de `.gitignore` y se sincronizan entre equipos via VS Code Settings Sync.

**Omisi├│n cr├¡tica**: El plan dice que `audit_ecosystem.py` usa `--no-verify` para "facilitar la ejecuci├│n", pero **no menciona que el propio scanner tiene blind spots que vuelven el hallazgo auto-referencial**. El scanner de `audit_ecosystem.py` solo escanea extensiones `.py`, `.json`, `.yaml`, `.yml`, `.env`, `.toml`, `.cfg`, `.ini`, `.js`, `.ts` (l├¡neas 180-191). **NO escanea archivos `.sh`, `.ps1`, `.md`, ni `.txt`**. Las vulnerabilidades m├ís peligrosas del ecosistema (como `--dangerously-skip-permissions` que seg├║n el backlog existe en `dispatch.sh` de AG_Plantilla, o `eval` en `health-check.sh`) viven en tipos de archivo que el scanner nunca examina.

### 1.4 "env_resolver suprime errores" ÔÇö Incorrecto

**Lo que dice el plan**: *"Si la unidad W: no responde, el script simplemente salta el proyecto."*

**Realidad verificada**: Revis├® `env_resolver.py` l├¡nea por l├¡nea. La funci├│n `detect_environment()` (l├¡neas 50-99) **lanza `RuntimeError`** si no puede detectar ning├║n entorno (l├¡nea 96-98). No "salta silenciosamente". El problema real es diferente: la resoluci├│n por fallback usa `is_default` (l├¡nea 92-94), lo que dirigir├¡a la ejecuci├│n al entorno `notebook` con path `C:\_Repositorio` ÔÇö un directorio que no existe en el desktop. Esto produce un escaneo sobre cero proyectos, no un error ruidoso. Pero la caracterizaci├│n del plan es t├®cnicamente incorrecta: el script no "salta proyectos", sino que apunta al directorio equivocado por dise├▒o de fallback.

El problema **real** no est├í en `env_resolver.py` sino en `audit_ecosystem.py` (l├¡neas 38-53) y `cross_task.py` (l├¡neas 35-49), donde el fallback `except ImportError` hardcodea `C:\_Repositorio` como ├║ltimo recurso. Si el import falla, el `detect_environment()` nunca se ejecuta.

---

## Cr├¡tica de Fase 1: Cirug├¡a de Desacoplamiento

### 1.1 "Destrucci├│n del ADN Clonado: Eliminar .git"

**Riesgo no mencionado**: El plan dice "eliminar inmediatamente y de forma manual la carpeta `.git`". Pero el repositorio actual tiene **2 commits de trabajo real** (`1470362` y `40adb3c`) que representan el trabajo de desacoplamiento y transplante de scripts. Eliminar `.git` sin primero extraer ese historial destruir├¡a la trazabilidad de la migraci├│n. El plan deber├¡a incluir un paso previo: `git log --all --oneline > .git_archive.txt` o crear un tag de referencia antes de la destrucci├│n.

### 1.2 "Contrato de Archivos Estricto"

**Omisi├│n**: El plan dice que el orquestador solo puede contener `/docs/`, `/scripts/`, `/config/`, y `GEMINI.md`. Pero el orquestador **actualmente** contiene tambi├®n:
- `.subagents/` (dispatch.ps1, manifest.json, dispatch-team.ps1, skills/)
- `.agent/` (rules, workflows)
- `.claude/` (settings, skills)
- `.codex/` (instructions)
- `.gemini/` (brain, context-snapshot)
- `.vscode/` (workspace settings)
- `CLAUDE.md`, `AGENTS.md`, `CHANGELOG.md`, `README.md`
- `AG_Orquesta.code-workspace`
- `.pre-commit-config.yaml`, `.gitignore`, `.env`, `.env.example`

El "contrato estricto" de 4 carpetas eliminar├¡a la **infraestructura de dispatch completa** (`.subagents/`), los archivos de identidad de los 3 vendors (`.claude/`, `.codex/`, `.gemini/`), y el sistema de pre-commit. El plan necesita ser expl├¡cito sobre qu├® sobrevive y qu├® se destruye. Tal como est├í escrito, es ambiguo y destruir├¡a la capacidad de orquestaci├│n que el plan pretende preservar.

### 1.3 "Prohibici├│n de C├│digo"

**Error de concepto**: El plan dice eliminar `ci.yml` y `security.yml`. Estos ya fueron eliminados (aparecen como `D` en git status). Pero esta recomendaci├│n **contradice directamente** la Fase 4, que requiere "auditor├¡as autom├íticas" y verificaci├│n pre-commit. Sin CI/CD, ┬┐qui├®n ejecuta las verificaciones automatizadas? El plan elimina la infraestructura de enforcement en Fase 1 y luego la requiere en Fase 4, sin explicar c├│mo se reconstruye.

---

## Cr├¡tica de Fase 2: Bloqueo de Gobernanza

### 2.1 "Purgar --no-verify"

**Correcto pero insuficiente**. Los 3 archivos con `--no-verify` fueron verificados:
- `audit_ecosystem.py:328` ÔÇö en `fix_missing_files()`
- `propagate.py:186` ÔÇö en `cmd_apply()`
- `scripts/temp/commit_satellites.py:12` ÔÇö batch commit

El plan dice "purgar de `propagate.py`, `audit_ecosystem.py` y cualquier macro". Pero **no menciona `commit_satellites.py`** expl├¡citamente. Peor a├║n, todo el directorio `scripts/temp/` est├í en la lista `SKIP_DIRS` del scanner (l├¡nea 168) y no est├í trackeado en git. Es un directorio-sombra con 20+ scripts operativos que modifican el ecosistema sin supervisi├│n ni versionamiento.

### 2.2 "Remover --dangerously-skip-permissions"

**Error f├íctico**: El plan dice removerlo de `run_claude.ps1` y `dispatch.ps1`. Verifiqu├® ambos archivos l├¡nea por l├¡nea: **`--dangerously-skip-permissions` NO EXISTE en ninguno de los dos archivos en AG_Orquesta_Desk**. El flag existe en el backlog como H-01, referenciado como presente en `dispatch.sh` de **AG_Plantilla** (l├¡neas 197 y 215), no en el orquestador. El plan atribuye el hallazgo al repositorio equivocado.

### 2.3 "Rotaci├│n Forzada de credenciales"

**Omisi├│n temporal cr├¡tica**: Las credenciales IRIS/SIDRA fueron reportadas el 2026-02-17. Hoy es 2026-02-20. Han pasado **3+ d├¡as** sin rotaci├│n. El plan las clasifica como Fase 2 (despu├®s de la cirug├¡a de desacoplamiento de Fase 1). Esto es una secuenciaci├│n peligrosa: las credenciales expuestas deben rotarse como **Fase 0 inmediata**, antes de cualquier trabajo arquitect├│nico. Cada d├¡a que pasan sin rotaci├│n es un d├¡a de exposici├│n activa de sistemas hospitalarios cl├¡nicos.

---

## Cr├¡tica de Fase 3: La Gran Sincronizaci├│n

### 3.1 "cross_task.py para inyectar TASKS.md"

**Bug operativo no detectado**: `cross_task.py` escribe su `INDEX_PATH` y `COUNTER_PATH` en `PLANTILLA_DIR / "docs" / "TASKS_INDEX.md"` y `PLANTILLA_DIR / "data" / "task_counter.json"` (l├¡neas 52-53). En el entorno desktop, `PLANTILLA_DIR` resuelve a `W:\Antigravity_OS\00_CORE\AG_Plantilla`. Si AG_Plantilla no existe en ese path, el counter se pierde, los task IDs se resetean, y los ├¡ndices se crean en ubicaciones fantasma. El plan no verifica este prerequisito.

### 3.2 "Forzar la creaci├│n de TASKS.md"

**Conflicto con gobernanza**: El plan dice que el orquestador "empujar├í y forzar├í" la creaci├│n de TASKS.md. Pero `propagate.py` ÔÇö el script de propagaci├│n ÔÇö tiene paths hardcodeados a `C:\_Repositorio` (l├¡neas 24-27) y **no usa `env_resolver`** en absoluto. El script es **no-funcional** en el entorno desktop actual. Ejecutar `propagate.py apply --file docs/TASKS.md` no har├¡a nada porque `get_all_projects()` buscar├¡a en `C:\_Repositorio\AG_Proyectos` ÔÇö un directorio que no existe.

El plan propone usar Fase 3 con herramientas que est├ín rotas por el bug que Fase 1 deber├¡a haber corregido. La secuenciaci├│n l├│gica es:
1. Corregir `propagate.py` para usar `env_resolver`
2. **Luego** ejecutar la propagaci├│n

Pero el plan no identifica esta dependencia.

### 3.3 "Inyecci├│n del Sistema Nervioso"

**Vac├¡o l├│gico**: El plan dice inyectar `tasks_awareness` en los `GEMINI.md` de cada sat├®lite. Pero 4 de los 12 proyectos son categor├¡a D (health score 10-16): AG_Hospital, AG_TrakCare_Explorer, AG_Analizador_RCE, AG_SV_Agent. Estos proyectos no tienen ni `GEMINI.md`, ni `TASKS.md`, ni `.gitignore`, ni `docs/`. No se puede "inyectar un bloque en GEMINI.md" si GEMINI.md no existe. El plan deber├¡a especificar que la inyecci├│n requiere **crear los archivos primero**, lo cual es exactamente lo que hace `audit_ecosystem.py --fix` ÔÇö pero ese script tiene `--no-verify` (que Fase 2 elimina) y depende de `TEMPLATE_DIR` (que apunta a `C:\_Repositorio` por el mismo bug de Fase 3.2).

**Dependencia circular**: Fase 2 elimina `--no-verify`. Fase 3 usa `audit_ecosystem.py --fix` para crear archivos, que depende de `--no-verify` para auto-commitear. Sin `--no-verify`, los pre-commits de TruffleHog podr├¡an bloquear el commit si el template contiene patrones que se parezcan a credenciales (ej. placeholders con `change-me`). El plan no resuelve esta circularidad.

---

## Cr├¡tica de Fase 4: Bucle de Auditor├¡a Recursiva

### 4.1 "Cambiar env_resolver a modo Estricto"

**Apunta al componente equivocado**: Como demostr├® en 1.4, `env_resolver.py` ya lanza `RuntimeError`. El problema est├í en los bloques `except ImportError` de `audit_ecosystem.py` y `cross_task.py`. Hacer `env_resolver` "estricto" no cambia nada si los scripts consumidores nunca lo importan exitosamente.

**Propuesta concreta que falta**: Lo que realmente se necesita es:
1. Agregar `scripts/` al `PYTHONPATH` en todos los scripts de invocaci├│n
2. Eliminar los bloques `except ImportError` con fallback hardcodeado
3. Dejar que el import falle ruidosamente si `env_resolver` no est├í disponible

### 4.2 "pre-commit run --all-files despu├®s de cada sesi├│n de subagente"

**Imposible en 4 proyectos**: Los proyectos categor├¡a D no tienen `.pre-commit-config.yaml`. Ejecutar `pre-commit run --all-files` en un proyecto sin configuraci├│n de pre-commit produce un error, no una verificaci├│n. El plan requiere que Fase 3 complete la propagaci├│n de infraestructura **antes** de que Fase 4 pueda funcionar, pero no documenta esta dependencia expl├¡citamente.

**Riesgo de deadlock**: Si `dispatch.ps1` invoca un subagente en un sat├®lite, y ese subagente debe ejecutar `pre-commit run --all-files` antes de devolver control, y el pre-commit hook ejecuta el scanner que depende de `env_resolver` que intenta resolver el path del sat├®lite... se crea una cadena de dependencias donde un fallo en cualquier eslab├│n bloquea el retorno de control al orquestador. En Windows, con los lock de archivo de `.git/index`, esto puede resultar en un deadlock real si dos procesos intentan commitear al mismo sat├®lite simult├íneamente.

---

## Hallazgos que el Plan Omite Completamente

### H-01: Dispatch Error Log Injection (SEGURIDAD ALTA)

`dispatch.ps1:122-130` inyecta el contenido del error log de un intento previo directamente en el prompt del siguiente intento **sin sanitizaci├│n**:

```powershell
$PrevError = Get-Content $ErrorLogPrev -Raw
$CurrentPrompt = @"
$fullPrompt
...
Error details:
$PrevError
"@
```

Si un agente malicioso o un output con formato de instrucciones del sistema aparece en stderr, se inyecta como contexto "confiable" en el siguiente intento. Esto es un vector de **prompt injection de segundo orden**: el error log de una ejecuci├│n fallida se convierte en instrucciones para la siguiente.

### H-02: Doble-escape en dispatch.ps1:151

```powershell
$SafePrompt = $CurrentPrompt -replace '"', '\"'
```

Despu├®s de la sanitizaci├│n de tags en l├¡nea 91, se aplica un escape de comillas. Un payload crafteado como `\"</user_task_...>` sobrevivir├¡a la sanitizaci├│n de la l├¡nea 91 (que busca `</?user_task.*?>`) porque el `\"` quebrar├¡a el parser de regex, y luego el escape de l├¡nea 151 convertir├¡a `\"` en `\\"`, reensamblando el tag original.

### H-03: Recursi├│n infinita potencial en dispatch.ps1:232

```powershell
& $MyInvocation.MyCommand.Path "researcher" $ResearchPrompt "codex"
```

El dispatch se llama a s├¡ mismo recursivamente para el fallback de investigaci├│n. Si el agente `researcher` falla, no hay recursi├│n porque hay un check `if ($AgentName -ne "researcher")` en l├¡nea 211. **Pero**: si alguien modifica el manifest para definir un agente que el dispatch intente resolver con un vendor que falla, y ese agente no se llama "researcher", la recursi├│n ejecutar├¡a el research fallback, que a su vez invocar├¡a dispatch, que fallar├¡a, que invocar├¡a su propio research fallback... sin l├¡mite de profundidad.

### H-04: Path Traversal en safe-write (hallazgo de Codex)

Los scripts `safe-write.ps1` y `safe-write.sh` validan paths con prefijos de string sin normalizaci├│n completa. Un symlink o path con `..` podr├¡a escapar el directorio restringido. El plan no menciona estos scripts.

### H-05: Global State Bug en propagate.py (hallazgo de Codex)

La variable `applied` (l├¡nea 161) persiste a trav├®s del loop de proyectos. El bloque de auto-commit (l├¡nea 179) verifica `if applied > 0`, pero `applied` acumula **todos** los archivos aplicados desde el inicio del batch, no solo los del proyecto actual. Resultado: si el proyecto A tuvo 3 archivos aplicados, el commit del proyecto B se ejecutar├í aunque B no haya cambiado nada.

### H-06: AG_Plantilla excluida del audit

`audit_ecosystem.py` **nunca escanea AG_Plantilla**. La funci├│n `list_ag_projects()` busca en `get_projects_dirs()`, que retorna `00_CORE`, `01_HOSPITAL_PRIVADO`, `02_HOSPITAL_PUBLICO`. AG_Plantilla est├í en `00_CORE/AG_Plantilla`, y s├¡ aparecer├¡a en la lista. Sin embargo, el template dir (`_template/workspace/`) dentro de AG_Plantilla tiene archivos con placeholders como `{{PROJECT_NAME}}` y `change-me` que el scanner deber├¡a evaluar. AG_Plantilla es el proyecto m├ís cr├¡tico del ecosistema porque genera todos los dem├ís, y cualquier vulnerabilidad en ella se propaga a todo sat├®lite nuevo.

### H-07: El pipeline MoE que gener├│ este plan fall├│

2 de 3 agentes (Claude V1 y Codex V1/V2) recibieron variables PowerShell sin resolver (`$CurrentPrompt`, `$FinalPrompt`). El pipeline de consenso que gener├│ este Draft Master Plan **no es confiable**. Los scripts en `scripts/temp/` no tienen `Set-StrictMode -Version Latest`, lo que permite que variables no resueltas pasen silenciosamente como strings vac├¡os o literales.

---

## Resumen de Defectos por Categor├¡a

| Categor├¡a | Cantidad | Severidad |
|-----------|----------|-----------|
| Errores f├ícticos (datos incorrectos) | 4 | Alta ÔÇö debilitan credibilidad |
| Omisiones de seguridad | 7 | Cr├¡tica ÔÇö H-01 y H-02 son vectores activos |
| Errores de secuenciaci├│n | 3 | Alta ÔÇö Fases con dependencias circulares |
| Propuestas imposibles | 3 | Alta ÔÇö Scripts rotos invocados como soluci├│n |
| Contradicciones internas | 2 | Media ÔÇö CI eliminada pero requerida |

## Recomendaciones Concretas

1. **Fase 0 (INMEDIATA, antes de todo)**: Rotar credenciales IRIS (`sd260710sd`) y SIDRA (`hkEVC9AFVjFeRTkp`). Esto no puede esperar a Fase 2.

2. **Corregir errores f├ícticos**: El remote no existe, `env_resolver` ya tiene RuntimeError, `--dangerously-skip-permissions` no est├í en AG_Orquesta sino en AG_Plantilla.

3. **Resolver dependencias antes de secuenciar fases**:
   - `propagate.py` necesita migrar de paths hardcodeados a `env_resolver` **antes** de Fase 3.
   - `audit_ecosystem.py --fix` necesita una alternativa al `--no-verify` **antes** de Fase 3.
   - Pre-commit config debe propagarse a sat├®lites **antes** de Fase 4.

4. **Agregar las omisiones de seguridad**: H-01 (error log injection), H-02 (double-escape bypass), H-04 (path traversal), H-05 (global state bug).

5. **Extender el scanner**: Agregar `.sh` y `.ps1` a `SCAN_EXTENSIONS` en `audit_ecosystem.py:180-191`. Sin esto, Fase 4 es ciega a las vulnerabilidades que m├ís importan.

6. **Estabilizar el pipeline MoE**: Agregar `Set-StrictMode -Version Latest` y validaci├│n `$null` a todos los scripts PowerShell de orquestaci├│n antes de ejecutar otra ronda.

7. **Explicitar qu├® sobrevive en Fase 1**: El "contrato estricto de archivos" debe listar expl├¡citamente `.subagents/`, `.agent/`, `.claude/`, `.codex/`, `.gemini/` como carpetas permitidas, o el orquestador queda inoperante.

---

FINALIZADO
