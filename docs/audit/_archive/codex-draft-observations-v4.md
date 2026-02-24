# Cr├¡tica del `docs/audit/master-draft-plan.md` (Gemini Round 4)

## Verificaci├│n inicial
Le├¡ `docs/audit/master-draft-plan.md` y contrast├® con el estado real de `AG_Orquesta_Desk` sin modificar archivos.

## Fase 1 ÔÇö Cirug├¡a de desacoplamiento

- [Cr├¡tico] El plan asume un riesgo ÔÇ£zombie cloneÔÇØ por `AG_Orquesta_Desk/.git` como si a├║n fuera clon heredado de `AG_Plantilla`, pero en `.git/config` no hay evidencias de remote u origen remoto vinculante en esta ejecuci├│n. La motivaci├│n de urgencia de eliminar `.git` est├í sin sustento local y puede romper historial y trazabilidad.
- [Alto] El objetivo ÔÇ£solo `docs/`, `scripts/`, `config/`, `GEMINI.md`ÔÇØ colisiona con componentes vivos de orquestaci├│n que ya existen y son necesarios: `.subagents/`, `.agent/`, `.claude/`, `.codex/`, `.gemini/`, `.github/`, `AG_Orquesta.code-workspace`, `LICENSE`, `CHANGELOG.md`, etc. Ver `Get-ChildItem` del root y `AG_Orquesta.code-workspace`.
- [Alto] Borrar `AG_Orquesta.code-workspace` o los metadatos de agentes implica perder routing interno (`cross_task`, manifiestos, reglas y perfiles) sin plan de migraci├│n o backup.
- [Medio] Fase 1 no define una estrategia de corte/fusi├│n hist├│rica (qu├® conservar, migrar y validar). Con `.git` intacto en producci├│n, esta transici├│n debe ser expl├¡cita, no s├│lo destructiva.

## Fase 2 ÔÇö Bloqueo de gobernanza y hardening

- [Cr├¡tico] La eliminaci├│n de flags `--no-verify` est├í incompleta: adem├ís de `scripts/audit_ecosystem.py` y `scripts/propagate.py`, tambi├®n est├ín en `scripts/temp/commit_satellites.py` y hay rutas peligrosas en scripts temporales de despliegue automatizado (`scripts/temp/send_norm_tasks.py`, `scripts/temp/*.py`).
- [Cr├¡tico] Plan menciona `run_claude.ps1`/`dispatch.ps1`, pero en esa ruta de riesgo no existe `--dangerously-skip-permissions`. El riesgo real actual est├í en `.subagents/dispatch.sh`, que s├¡ ejecuta `codex exec --dangerously-bypass-approvals-and-sandbox`.
- [Alto] Retirar `--no-verify` sin dise├▒ar un camino de commit ÔÇ£policy-safeÔÇØ romper├í flujo auto-fijo: `audit_ecosystem.py` y `propagate.py` usan commits autom├íticos; si hooks de pre-commit fallan, quedan bloqueados sin salida.
- [Alto] `scripts/audit_ecosystem.py` no escanea `.sh`, `.ps1`, `.md`, `.txt`; al quitar bypasses, muchos riesgos de gobernanza quedan fuera de detecci├│n actual (dispatch scripts, validadores de seguridad en texto, scripts de infraestructura).
- [Medio] Fase 2 declara ÔÇ£fallo ruidoso + aprobaci├│n manualÔÇØ, pero no detalla c├│mo tratar casos de lectura de archivo protegido por agente/vendedor; hoy `dispatch` no tiene ese contrato de escalado expl├¡cito.

## Fase 3 ÔÇö Sincronizaci├│n y sincronizaci├│n aut├│noma

- [Cr├¡tico] `scripts/cross_task.py` actualmente **no** lee `config/project_registry.json`; usa `env_resolver.py` + escaneo de FS. La Fase 3 est├í basada en una integraci├│n que hoy no existe y por tanto no ejecutar├í como se describe.
- [Cr├¡tico] `config/project_registry.json` declara 13 proyectos (incl. `AG_Plantilla`), pero el plan trabaja con ÔÇ£12 proyectosÔÇØ, inconsistencia que afecta cobertura y m├®tricas.
- [Alto] ÔÇ£Inyecci├│n de `TASKS.md` y `tasks_awareness`ÔÇØ no coincide con implementaci├│n real: `cross_task.py` ya puede crear `docs/TASKS.md`, pero **no** inyecta bloques `tasks_awareness` en `GEMINI.md`; eso no est├í implementado ni automatizable en el bloque descrito.
- [Alto] Fase 3 no contempla scripts legacy que fuerzan topolog├¡as antiguas (`C:\_Repositorio`, `AG_Proyectos`) en `scripts/temp/send_norm_tasks.py`, `scripts/temp/commit_satellites.py`, `scripts/agent_selftest.py`.
- [Medio] `cross_task.py` no valida estado de registro vs realidad del disco (proyectos borrados/renombrados), por lo que ÔÇ£mapear 12 proyectosÔÇØ puede degradarse en ruido o omisiones.

## Fase 4 ÔÇö Auditor├¡a recursiva y fail-fast

- [Cr├¡tico] `scripts/env_resolver.py` no rompe cuando un proyecto individual falla; omite rutas/dirs faltantes y contin├║a. La propuesta de ÔÇ£crash fatalÔÇØ no coincide con comportamiento actual y sin definir recuperaci├│n puede causar paradas fuera de contexto.
- [Alto] `--no-verify` y ÔÇ£obligatorio pre-commit en cada sesi├│nÔÇØ chocan sem├ínticamente: fase 2 exige endurecer hooks, fase 4 exige un check obligatorio al final. Falta una pol├¡tica de excepci├│n para commits generados por plantillas.
- [Alto] `dispatch.ps1`/`dispatch.sh` no tienen timeout de ejecuci├│n de CLI; una llamada colgada puede congelar orquestaci├│n (riesgo de deadlock operativo en terminal recursiva).
- [Medio] Ambos dispatchers tienen ruta recursiva de ÔÇ£research fallbackÔÇØ que vuelve a invocar agente en cascada; sin circuit breaker temporal, puede producir loops de control prolongados y saturaci├│n en fallos repetidos.

## Riesgos arquitect├│nicos globales (no estrictamente por fase)

- [Cr├¡tico] La separaci├│n ÔÇ£orquestador puroÔÇØ no est├í resuelta: `AG_Orquesta_Desk` ya es n├║cleo de plantillas/gobernanza al mismo tiempo que coordinador. El plan mezcla reubicaciones sin definir l├¡mites de interfaz (qu├® funciones se quedan y qu├® migran a `AG_Plantilla`).
- [Alto] Existe deuda de hardening transversal fuera de la Fase 2 (`scripts/agent_health_check.py`, `scripts/agent_selftest.py`, `scripts/template_sync.py`) que seguir├í ejecutando l├│gica sensible aunque `--no-verify` desaparezca parcialmente.
- [Medio] El `project_registry` existe y se usa por dashboards, pero no por `cross_task`; sin un contrato ├║nico de repositorio/registro, la arquitectura queda con dos fuentes de verdad parciales.

## Recomendaci├│n breve
Antes de ejecutar Fase 2-4, alinear primero:
1) mapa de alcance real (12 vs 13 proyectos y rutas por entorno),
2) frontera funcional de orquestador/plantilla,
3) estrategia de permisos en dispatch (incluyendo `dispatch.sh`) y
4) secuencia de commit con pre-commit sin perder automatizaci├│n.  

FINALIZADO
