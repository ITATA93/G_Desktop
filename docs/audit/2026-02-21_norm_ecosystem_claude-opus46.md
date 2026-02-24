# Evaluación Contrastada de Auditorías de Ecosistema

**Fecha de Evaluación**: 2026-02-21
**Objetivo**: Contrastar punto a punto los 3 reportes generados hoy para el ecosistema Antigravity OS y extraer la VERDADERA lista de tareas pendientes.

## 1. Archivos Analizados
1. `AUDITORIA_GLOBAL_ECOSISTEMA_2026-02-21.md`: Reporte profundo generado por 14 sub-agentes. Identifica problemas cualitativos, de código (tests, dependencias) y vulnerabilidades (API Keys).
2. `2026-02-21-ecosystem-audit.md`: Reporte ejecutivo generado en esta sesión. Se centra en el governance estructural, confirmando que las vulnerabilidades de FS (credenciales git) fueron subsanadas en su totalidad.
3. `2026-02-21_auditoria_proyectos_vinculados_full.md`: Reporte de métricas duras (salud 87/100). Profundiza en autonomía agentica, higiene git y sincronización con el `project_registry.json`.

---

## 2. Contraste Punto a Punto y Estado Real

### A. Seguridad y Credenciales 🛡️
- **Reportado en Global**: API Key de Gemini listada en `.env` en `AG_Hospital_Organizador` (Severidad Crítica).
- **Reportado en Full/Ecosystem**: 0 hallazgos de seguridad detectados por el escáner.
- **Veredicto Real**: El problema de hardcoding/tracked objects fue subsanado (los passwords y keys en texto plano fueron borrados), PERO la acción de mitigación en la nube (Rotar la clave explícitamente en Google Cloud Console) debe mantenerse como preventiva si dicha clave estuvo commiteada/expuesta al subirse.
- **Problema Arquitectónico**: "Sin autenticación API en `AG_SV_Agent`" (reportado en Global). El escáner regex no lo detecta porque es un fallo de diseño, no una credencial escrita. **[PENDIENTE]**

### B. Higiene de Repositorios (Git) 🌿
- **Reportado en Global**: 12 proyectos con archivos sin trackear (sobre todo `.agent/`, `.claude/`, etc).
- **Reportado en Full**: Confirma que 13 de los 14 repositorios tienen un "árbol sucio" (dirty tree). Por ejemplo, `AG_Hospital_Organizador` lista 3421 cambios/46 untracked.
- **Veredicto Real**: Las herramientas de normalización (Template sync y fixes) actualizaron archivos, pero NO los commitearon automáticamente. Esto es un riesgo inminente de perder el estado sincronizado. **[PENDIENTE URGETE]**

### C. Autonomía Agéntica 🤖
- **Reportado en Full**: Solo reportado aquí. Menciona que `AG_Hospital`, `AG_Notebook`, `AG_SD_Plantilla`, `AG_SV_Agent` tienen una autonomía muy baja (<= 16-33%). Faltan protocolos de sesión, definición de subagentes y workflows en las carpetas `.agent/` o `.subagents/`.
- **Veredicto Real**: Proyectos que no son de código activo tienden a ignorar esto, pero si se espera que Master Orchestrator pueda delegar tareas allí, la autonomía debe elevarse. **[PENDIENTE]**

### D. Governance Estructural vs Calidad 📄
- **Reportado en Ecosystem**: 100% de cumplimiento en existencia de archivos requeridos (7/7).
- **Reportado en Full**: Identifica que, aunque los archivos (ej. `GEMINI.md`) existen, su calidad interna es insuficiente (faltan las `gemini_keywords` obligatorias o la `tasks_awareness`).
- **Veredicto Real**: Se copiaron templates de `GEMINI.md` pero quizás no contienen la matriz de delegación o las instrucciones vitales requeridas por el escáner de calidad. **[PENDIENTE]**

### E. Integridad de Código y Dependencias ⚙️
- **Reportado en Global**: `AG_Analizador_RCE` falla porque requiere `pandas` y `numpy` que no están en su `requirements.txt`.
- **Reportado en Global & Full**: La cobertura de pruebas (Test Coverage) es del 0% en la mayoría absoluta del ecosistema (10 de 14 proyectos no tienen tests detectados).
- **Veredicto Real**: Añadir las dependencias faltantes es un arreglo rápido y vital que se esquivó en la normalización estructural. Escribir tests para 10 proyectos es una tarea épica que debe agregarse al Backlog. **[PENDIENTE]**

### F. Desincronización del project_registry.json 🕒
- **Reportado en Full**: La fecha de `last_update` (2026-02-17 en su mayoría) es anticuada frente a los commits físicos en los módulos (2026-02-20).
- **Veredicto Real**: El Orquestador o el proceso manual olvidó actualizar sistemáticamente el registry cada vez que intervino las carpetas satélites. **[PENDIENTE]**

---

## 3. Lista Definitiva de Tareas PENDIENTES (Next Steps Actuables)

Para llevar el ecosistema de un 87% de salud "virtual" a un 100% de solidez real, se debe ejecutar el siguiente backlog en orden de prioridad:

### 🔴 PRIORIDAD ALTA (Bloqueantes Operativos y Seguridad)
- [ ] **Rotar Gemini API Key**: Revocar manualmente en consola GCP la clave de `AG_Hospital_Organizador` por protocolo de seguridad ante previas exposiciones.
- [ ] **Actualizar Requirements (`AG_Analizador_RCE`)**: Agregar `pandas` y `numpy` a su `requirements.txt`.
- [ ] **Commit Masivo de Normalización (Git Hygiene)**: Hacer `git add .` y `git commit -m "chore: ecosystem normalization sync"` en los 13 repositorios satélites que quedaron sucios tras las auditorías y fixes.
- [ ] **Sincronizar `project_registry.json`**: Actualizar la propiedad `last_update` de los 14 proyectos con la fecha de hoy (`2026-02-21`) para curar la desincronización reportada.

### 🟡 PRIORIDAD MEDIA (Gobernanza y Calidad Interna)
- [ ] **Corregir Calidad de `GEMINI.md`**: Actualizar el contenido de los `GEMINI.md` en los 7 repositorios que fallaron la validación de *gemini_keywords* (especialmente inyectar la tabla de complejidad hibrida y reglas asolutas).
- [ ] **Autonomía Mínima Viable**: Establecer la estructura `.agent/` (rules, workflows) y `.subagents/manifest.json` en los repositorios de baja autonomía (`AG_Hospital`, `AG_Notebook`, `AG_SD_Plantilla`, `AG_SV_Agent`).
- [ ] **Faltantes Recomendados**: Asegurar la creación de la carpeta `config/` en los proyectos que carecen de ella (ej. `AG_Consultas`, `AG_Hospital_Organizador`, `AG_Lists_Agent`, `AG_NB_Apps`, `AG_TrakCare_Explorer`).

### 🔵 PRIORIDAD BAJA / BACKLOG (Evolución de Arquitectura)
- [ ] **Auth en AG_SV_Agent**: Implementar protección JWT o API Keys en los endpoints del sistema base para remediar el hallazgo de seguridad arquitectónica.
- [ ] **Test Coverage Campaign**: Delegar de forma cross-repositorio a agentes *test-writer* el levantamiento de tests básicos (`pytest` / `vitest`) para los 10 proyectos en 0%.
- [ ] **Consolidar Scripts Caprini (`AG_Consultas`)**: Limpiar las mútliples versiones (v, v2, v3) identificadas.
