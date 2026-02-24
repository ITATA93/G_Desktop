# Draft Master Plan (Gemini Judge - Round 3 Synthesis)
**Objetivo:** Síntesis Exhaustiva de las Auditorías V1 y V2.0 de la Tríada (Gemini, Claude, Codex) con integración de la Directriz Maestra ("AG_Orquesta_Desk como Orquestador Maestro Puro").

---

## 1. Análisis Profundo del Estado Actual (Consolidación de la Tríada)

### 1.1 La Falla Fundamental: El Orquestador Zombie (Hallazgo Crítico de Claude)
El problema más grave detectado estructuralmente es la identidad del orquestador mismo. `AG_Orquesta_Desk` fue instanciado como un clon directo del repositorio `AG_Plantilla`. Para "limpiarlo", se borraron ~7,200 archivos de código, pero **la carpeta `.git` original sigue presente**.
*   **Riesgo Catastrófico:** Git sigue trackeando esos 7,200 archivos como "eliminados". Si en el orquestador se ejecuta un `git commit -a`, se propagará la eliminación masiva hacia el repositorio origen (`AG_Plantilla`), destruyendo el código fuente de toda la organización.
*   **Veredicto de la Directriz Maestra:** Esto da la razón absoluta a la idea del usuario. El orquestador no puede compartir ADN con la plantilla. Debe ser un repositorio autónomo.

### 1.2 Brecha Crítica de Autonomía y Enrutamiento (Hallazgo de Codex y Gemini)
El 85% del ecosistema (11 de 12 proyectos satélite) está "sordo" ante el orquestador.
*   **Falla de Discovery:** Los proyectos como `AG_TrakCare_Explorer`, `AG_Hospital`, y `AG_Notebook` carecen de los archivos de gobernanza requeridos (`TASKS.md` y un `GEMINI.md` con bloques de *tasks_awareness*).
*   **Efecto Cascada:** Cuando `AG_Orquesta_Desk` usa `dispatch.ps1` para delegar tareas, los subagentes aterrizan en los directorios satélites sin contexto ni instrucciones de sistema (`GEMINI.md`). Actúan a ciegas.

### 1.3 Exposición Activa de Credenciales (Hallazgo de Claude)
A pesar de las políticas teóricas, Claude descubrió que `AG_Consultas/herramientas/python/db_config.py` y ciertos scripts de Caprini tienen hardcodeadas credenciales de la base de datos de producción (IRIS/LIVE-CLOV y SIDRA).
*   **Agravante:** El script `audit_ecosystem.py` en el Orquestador frecuentemente utiliza el flag `--no-verify`, permitiendo saltarse los pre-commits de TruffleHog (el detector de secretos). La gobernanza está desactivada por defecto para "facilitar" la ejecución.

### 1.4 Ambigüedad y Falsos Positivos (Hallazgo de Codex)
El script de resolución de entorno (`env_resolver.py`) está diseñado para suprimir errores. Si la unidad `W:\` no responde, o si una carpeta de proyecto fue renombrada, el script simplemente salta el proyecto en vez de alertar `[CRITICAL: PATH UNREACHABLE]`. Esto está generando puntuaciones de "normalización" falsas.

---

## 2. El Plan Maestro Arquitectónico: Desacoplamiento y Reestructuración

Para cumplir la exigencia de que `AG_Orquesta_Desk` sea un **Orquestador Maestro Puro**, debemos aislar la Lógica (Orquesta) de la Implementación (Plantilla y Satélites).

### Fase 1: Cirugía de Desacoplamiento (Repositorio Control)
1.  **Destrucción del ADN Clonado:** Eliminar inmediatamente y de forma manual la carpeta `W:\Antigravity_OS\00_CORE\AG_Orquesta_Desk\.git`.
2.  **Inicialización Limpia:** Ejecutar `git init` en `AG_Orquesta_Desk`.
3.  **Contrato de Archivos Estricto:** Este repositorio solo podrá contener:
    *   `/docs/` (Para reportes, auditorías, y master `TASKS.md`).
    *   `/scripts/` (Para wrappers de orquestación pura: `dispatch.ps1`, `audit_ecosystem.py`).
    *   `/config/` (Para el `project_registry.json`).
    *   `GEMINI.md` (Para definir la identidad del Global Brain).
4.  **Prohibición de Código:** Cualquier pipeline de CI/CD que compile código (`ci.yml`, `security.yml` basado en Python) debe ser borrado de Orquesta.

### Fase 2: Bloqueo de Gobernanza y Hardening (Capa de Seguridad)
1.  **Eliminación de Bypasses:** Purgar permanentemente el parámetro `--no-verify` de `propagate.py`, `audit_ecosystem.py` y cualquier macro del Orquestador.
2.  **Aislamiento de Dispatcher:** Remover el flag `--dangerously-skip-permissions` de `run_claude.ps1` y `dispatch.ps1`. Si un agente requiere permisos para leer un archivo bloqueado, debe fallar ruidosamente y solicitar aprobación manual, jamás escalar privilegios por defecto.
3.  **Rotación Forzada:** Se deben limpiar todos los repositorios detectados con credenciales (como `AG_Consultas`).

### Fase 3: La Gran Sincronización (Inyección de Autonomía)
1.  **Actualización del Registry:** El Orquestador usará `cross_task.py` para leer el `project_registry.json` y mapear los 12 proyectos.
2.  **Propagación de Archivos Base:** El Orquestador empujará y forzará la creación de `TASKS.md` en la raíz de todos los proyectos de `01_HOSPITAL_PRIVADO` y `02_HOSPITAL_PUBLICO`.
3.  **Inyección del Sistema Nervioso:** El Orquestador inyectará el bloque `tasks_awareness` en los respectivos archivos `GEMINI.md` de cada proyecto satélite. Esto les enseñará a escuchar las directivas delegadas.

### Fase 4: Bucle de Auditoría Recursiva (Fail Fast)
1.  **Modificación de `env_resolver.py`:** Cambiar su comportamiento "Silencioso" por "Estricto". Si `AG_Consultas` no puede ser accedido, el script entero debe crashear emitiendo un código de error fatal (exit 1).
2.  **Auditorías Automáticas:** Cada sesión de trabajo de un Sub-agente debe terminar ejecutando una verificación local (`pre-commit run --all-files`) en el directorio que acaba de modificar antes de devolver el control al Master Orchestrator.

---
**Petición para la Tríada:**
Claude y Codex: Exijan mejoras a este borrador. Buscad fallos de permisos en Windows Subsystem, deadlocks en llamadas de terminal recursivas entre los proyectos, y vacíos lógicos en la Sincronización (Fase 3). Destrocen la propuesta en busca de robustez.
FINALIZADO
