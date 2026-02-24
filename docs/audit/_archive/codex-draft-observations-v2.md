# Cr├¡tica t├®cnica al `docs/audit/master-draft-plan.md`

Le├¡ el plan y lo contrast├® con el estado real del repositorio en los archivos de orquestaci├│n, registry, resolutor y scripts de auditor├¡a.  
Conclusi├│n corta: **el borrador mezcla hallazgos reales con premisas falsas y asunciones no implementadas**; no es seguro ejecutarlo tal cual.

## 0) Riesgo global del documento

| Riesgo | Observaci├│n | Severidad | Impacto |
|---|---|---|---|
| Falsa premisa de identidad | El plan parte de que AG_Orquesta_Desk es ÔÇ£clone zombieÔÇØ de AG_Plantilla | Alta | Puede disparar cambios destructivos (e.g. `git init` con p├®rdida de historial) |
| Suposici├│n de alcance incompleto | Varias acciones est├ín sobre una porci├│n del sistema y omiten scripts/paths alternos | Alta | Debilita la efectividad y puede generar fallos en cadena |
| Falta de plan de implementaci├│n de fallback | Varias recomendaciones eliminan controles sin definir c├│mo preservar el flujo | Alta | Bloqueos operativos (hooks, commits, sincronizaciones parciales) |

---

## 1) Fase 1 ÔÇö Cirug├¡a de desacoplamiento (desacoplar repo)

1. **Premisa central incorrecta sobre ÔÇ£git compartidoÔÇØ**  
   El plan insiste en destruir `.git` y re-inicializar, asumiendo riesgo de que un commit borre AG_Plantilla por ser clon. Sin evidencia de remote/parent compartido en el estado actual del repo (`.git/config`), esta fase es **estructuralmente riesgosa y destructiva**.  
   **Archivo:** `docs/audit/master-draft-plan.md`, `.git/config`, `docs/audit/claude-draft-observations-v2.md`  
   **Recomendaci├│n:** No ejecutar reinit de `.git` sin verificar trazabilidad remota y objetivo expl├¡cito de migraci├│n.

2. **Alcance de ÔÇ£solo docs/scripts/configÔÇØ incoherente con el runtime real**  
   El orquestador depende de `.agent`, `.claude`, `.codex`, `.gemini`, `.subagents`, `_template`, `.github` y artefactos de plantilla/dispatch. Reducir a solo esos 3 dirs rompe invocaci├│n y gobernanza de agentes, workflows y perfiles.  
   **Archivo:** `Get-ChildItem` raiz, `.subagents/manifest.json`, `README.md`, `scripts/agent_health_check.py`  
   **Riesgo:** Operatividad degradada y fallos de dispatch/gobernanza.

3. **La ÔÇ£prohibici├│n de c├│digoÔÇØ es excesiva y ambigua**  
   La propuesta de borrar pipelines de CI/CD que compilan puede eliminar calidad-gates del propio orquestador (lint validaciones, validaci├│n de JSON, saneamiento de scripts), sin alternativa equivalente.  
   **Archivo:** `.pre-commit-config.yaml`, `docs/audit/master-draft-plan.md`  
   **Riesgo:** Riesgo de regresi├│n de calidad y p├®rdida de observabilidad de cambios.

4. **Conteo de proyectos inconsistentes**  
   Plan habla de ÔÇ£12 proyectosÔÇØ, pero `config/project_registry.json` declara 13 (`ag_plantilla` + 12 sat├®lites). Dise├▒ar fase por conteo errado ya invalida alcance y planificaci├│n.  
   **Archivo:** `config/project_registry.json`  
   **Recomendaci├│n:** Resolver primero cardinalidad real y criterios de inclusi├│n (incluye/excluye AG_Plantilla).

---

## 2) Fase 2 ÔÇö Hardening y seguridad

1. **ÔÇ£Quitar `--no-verify`ÔÇØ est├í bien en intenci├│n, mal formulado en alcance**  
   No hay `--no-verify` en `run_claude.ps1` ni en `dispatch.ps1`, por lo que esa parte es incorrecta para esos archivos.  
   **Archivo:** `scripts/temp/run_claude.ps1`, `.subagents/dispatch.ps1`  
   **Riesgo:** Falsa sensaci├│n de correcci├│n sin efecto real.

2. **Falta de cobertura real de bypasses**  
   Se omite que `scripts/temp/commit_satellites.py` tambi├®n usa `--no-verify` y hardcodea `C:\_Repositorio\AG_Proyectos`; hay m├ís superficies de bypass en scripts de automatizaci├│n.  
   **Archivo:** `scripts/temp/commit_satellites.py`  
   **Riesgo:** Persisten commits sin hook en rutas sat├®lite.

3. **El problema de bypass de seguridad s├¡ existe, pero necesita compensaci├│n operativa**  
   Remover `--no-verify` en `audit_ecosystem.py` y `propagate.py` sin dise├▒ar ruta de commit permitida bajo hooks provocar├í deadlocks operativos (commit bloqueado por calidad).  
   **Archivo:** `scripts/audit_ecosystem.py`, `scripts/propagate.py`  
   **Recomendaci├│n:** definir `pre-commit` por etapa/flag de excepci├│n antes de eliminar bypass.

4. **Falsa localizaci├│n de `--dangerously-skip-permissions`**  
   El riesgo mencionado en plan apunta a ps1; el bypass actual fuerte est├í en `.subagents/dispatch.sh` con `--dangerously-bypass-approvals-and-sandbox` para Codex (normal y fallback final).  
   **Archivo:** `.subagents/dispatch.sh`  
   **Riesgo:** Plan ignora vector real de escalado de capacidades.

5. **Backlog de hardening incompleto**  
   La parte de rotaci├│n de credenciales en AG_Consultas no especifica propietario, flujo CI/CD, ni secretos manager; queda declarativa sin ejecuci├│n real.  
   **Archivo:** `docs/audit/master-draft-plan.md`, `AG_Consultas/herramientas/python/db_config.py` (mencionado)  
   **Riesgo:** Riesgo de seguridad no resuelto, solo listado.

---

## 3) Fase 3 ÔÇö Sincronizaci├│n de autonom├¡a (cross-task + registry + inject)

1. **ÔÇ£Usar `cross_task.py` para leer `project_registry.json`ÔÇØ es incorrecta hoy**  
   `cross_task.py` no consume registry; opera por `env_resolver` + recorrido de filesystem (`get_projects_dirs()` + `list_ag_projects()`).  
   **Archivo:** `scripts/cross_task.py`, `scripts/env_resolver.py`  
   **Riesgo:** Fase 3 es no ejecutable con ese contrato.

2. **Inconsistencia de conteo y alcance**  
   El plan asume 12 proyectos y limita intervenci├│n a 01_HOSPITAL_PRIVADO / 02_HOSPITAL_PUBLICO, pero omite AG_Plantilla, AG_Notebook y AG_SV_Agent (siempre presentes en workspace).  
   **Archivo:** `config/project_registry.json`, `config/environments.json`, `scripts/env_resolver.py`  
   **Riesgo:** Cobertura parcial con falsos negativos de automatizaci├│n.

3. **Inyecci├│n masiva en `GEMINI.md` sin garant├¡a de idempotencia**  
   No define merge idempotente ni detecci├│n de bloque existente/adversarial en `docs/TASKS.md` y `GEMINI.md`.  
   **Archivo:** `scripts/cross_task.py`  
   **Riesgo:** Corrupci├│n de instrucciones por escritura repetida o conflicto sem├íntico.

4. **Desalineaci├│n con descubrimiento previo de archivos obsoletos**  
   `config/project_registry.json` y topolog├¡a del filesystem no coinciden con paths hist├│ricos (`AG_Proyectos`) en varios entornos/scripts.  
   **Archivo:** `config/environments.json`, `config/project_registry.json`, `scripts/cross_task.py`, `scripts/audit_ecosystem.py`, `scripts/propagate.py`  
   **Riesgo:** Sincronizaci├│n a blancos equivocados o silenciosa.

---

## 4) Fase 4 ÔÇö Auditor├¡a recursiva y fail-fast

1. **ÔÇ£Fail fastÔÇØ localizado mal y con cobertura parcial**  
   `env_resolver.py` ya arroja error si no resuelve entorno, pero en listas de proyecto puede degradarse silenciosamente por rutas inexistentes (`if domain_dir.exists():`), y el plan no lo cierra con validaci├│n expl├¡cita del target cr├¡tico (AG_Consultas).  
   **Archivo:** `scripts/env_resolver.py`  
   **Riesgo:** Fallo de cobertura no determin├¡stico.

2. **`pre-commit run --all-files` al final de cada subagente es costoso y arriesgado**  
   En repos grandes/heterog├®neos esto puede demorar extremo, romper flujos por hooks de formateo y crear bloqueo de sesi├│n por herramientas faltantes.  
   **Archivo:** `.pre-commit-config.yaml`, `scripts/agent_selftest.py`  
   **Riesgo:** Sesiones de orquestaci├│n inestables y cuello de botella operativo.

3. **No se cubren deadlocks/tiempos de ejecuci├│n de dispatcher**  
   Ni fase 3 ni fase 4 mencionan timeouts en llamadas a CLI. `.subagents/dispatch.ps1` y `.subagents/dispatch.sh` no fijan l├¡mites de tiempo; en fallback recursivo esto puede congelar orquestaci├│n.  
   **Archivo:** `.subagents/dispatch.ps1`, `.subagents/dispatch.sh`  
   **Riesgo:** Bloqueos en cadena ante vendor colgado o salida an├│mala.

4. **Contradicci├│n operativa con fase 2**  
   Fase 2 exige endurecer sin `--no-verify`; fase 4 exige pre-commit completo por sesi├│n. Falta la capa de pol├¡tica que permita ambos sin bloqueo total.  
   **Archivo:** `docs/audit/master-draft-plan.md` (Fase 2 y Fase 4)  
   **Riesgo:** Par├ílisis por ÔÇ£falla por dise├▒oÔÇØ.

---

## Omisiones transversales cr├¡ticas (no menores)

1. `scripts/propagate.py` y `scripts/audit_ecosystem.py` tienen fallback hardcodeado a `C:\_Repositorio`, y `scripts/temp/commit_satellites.py` tambi├®n. Esto contradice el entorno actual (`W:\Antigravity_OS`) y puede dejar fases de automatizaci├│n sin efecto real.  
   **Archivo:** `scripts/propagate.py`, `scripts/audit_ecosystem.py`, `scripts/env_resolver.py`, `config/environments.json`, `scripts/temp/commit_satellites.py`

2. Los cambios automatizados en `propagate.py` hacen `git add .` (staging indiscriminado) y usan bandera acumulativa de cambios (`applied`) entre proyectos, lo que puede commitear estado no asociado al objetivo actual.  
   **Archivo:** `scripts/propagate.py`

3. El plan no exige endurecer `except Exception: pass` ni validar `returncode` en subprocesses de Git/IO, lo que enmascara fallos reales de commit y deja ÔÇ£├®xito aparenteÔÇØ.  
   **Archivo:** `scripts/audit_ecosystem.py`, `scripts/propagate.py`

---

## Veredicto final

El plan no es aprobado en estado actual: requiere **reescritura por fases de implementaci├│n** antes de ejecuci├│n, especialmente en:  
1) validaci├│n real de estado de `.git` e historial, 2) correcci├│n de paths/registro (`project_registry` + `env_resolver`), 3) tratamiento real de `dispatch.sh` y bypasses, y 4) estrategia expl├¡cita de `pre-commit` sin romper la automatizaci├│n.

La cr├¡tica principal es: hay hallazgos v├ílidos, pero la propuesta asume demasiado, omite componentes vivos del sistema y ordena cambios potencialmente destructivos sin orden operativo verificable.

FINALIZADO
