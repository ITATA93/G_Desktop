# Reporte de Migración Forense: NB_Apps

**Fecha:** 2026-02-04
**Origen:** `C:\_Repositorio\_Proyectos_Base\_Consultas\NB_Apps`
**Solicitante:** Usuario (Antigravity Agent)
**Contexto:** Protocolo SAIA / Migración a AG_Plantilla

## 1. Resumen Ejecutivo
El directorio `NB_Apps` constituye un repositorio activo de desarrollo (v2.0.0, actualizado Enero 2026) enfocado en la gestión de instancias NocoBase (MIRA, UGCO, BUHO) para el Hospital de Ovalle. Contiene infraestructura crítica de scripts en TypeScript y documentación extensa. No clasifica como "Legacy Muerto", sino como "Infraestructura Activa".

## 2. Inventario Forense
Se realizó un escaneo no destructivo excluyendo `node_modules`.

**Estadísticas de Archivos:**
| Extensión | Cantidad | Categoría                    |
| --------- | -------- | ---------------------------- |
| .md       | 166      | Documentación                |
| .ts       | 159      | Código Fuente (TypeScript)   |
| .json     | 146      | Configuración/Datos          |
| .js       | 142      | Código Compilado/Scripts     |
| .py       | 9        | Legacy Scripts               |
| .xlsx     | 7        | Datasets/Reportes            |
| .env      | 2        | **SEGURIDAD (Credenciales)** |
| .pdf      | 1        | Documentación Binaria        |
| **Total** | **~680** |                              |

**Estructura Crítica Identificada:**
- `Apps/UGCO`: Aplicación Oncológica (Activa).
- `Apps/BUHO`: Aplicación Gestión Clínica (En desarrollo).
- `shared/scripts`: Colección core de utilidades de administración NocoBase.
- `.claude/skills`: Integración avanzada con Agentes IA.

## 3. Análisis de Riesgos

### 🔴 Seguridad
- **Archivos Confidenciales**: Se detectaron 2 archivos `.env`.
  - Acción Requerida: Verificar si contienen claves reales o son templates. Si contienen credenciales reales, **NO** deben ser subidos a repositorios públicos ni expuestos en logs.
- **Autorización**: El proyecto contiene scripts de manipulación de roles y permisos (`manage-permissions.ts`).

### 🟠 Integridad
- **Dependencias**: El proyecto depende de `npm install`. Moverlo requiere asegurar que la integridad de `package-lock.json` y `node_modules` se mantenga o se regenere.
- **Git Repository**: Contiene carpeta `.git`. Moverlo implica migrar el historial o convertirlo en Submódulo.

## 4. Propuesta de Migración

Dada la naturaleza "Activa" del proyecto, se desaconseja un archivado plano (Zip/SAIA Cold Storage). Se recomiendan las siguientes estrategias:

### Estrategia A: Federación (Recomendada)
Mantener el repositorio en su ubicación actual o moverlo a una ubicación dedicada a "Proyectos Activos" (no Base), y linkearlo simbólicamente o referenciarlo en `AG_Plantilla`.

### Estrategia B: Integración Monorepo
Mover `NB_Apps` dentro de `AG_Plantilla/external/` o `AG_Plantilla/projects/` para centralizar la gestión bajo el paraguas de Antigravity.
- **Ventaja**: Un solo entorno de Agente.
- **Riesgo**: Conflictos de `tsconfig`, `package.json` y linter.

### Estrategia C: Archivo Snapshot (A petición "Forense")
Sí el objetivo es congelar este estado como evidencia o backup antes de una reingeniería mayor:
1. Generar hash SHA-256 de todos los archivos críticos.
2. Copiar a `Unified_Archive/2026/NB_Apps_Snapshot_20260204`.
3. Eliminar `node_modules` antes de copiar para ahorrar espacio.

## 5. Ejecución: Estrategia B (Migración y Normalización)

**Estado:** ✅ COMPLETADO (2026-02-04)

1. **Migración Física**: Se generó una copia del proyecto en `C:\_Repositorio\AG_Proyectos\AG_NB_Apps`.
   - Se excluyó `node_modules` para limpieza.
   - Se excluyó `.git` para permitir un nuevo historial o submodulado limpio (según necesidad futura).
2. **Normalización**:
   - Renombrado a `AG_NB_Apps` para cumplir norma `AG_*`.
   - Actualizado `package.json` (`name: "ag-nb-apps"`).
3. **Seguridad**: Se copió manualmente el archivo `.env` (con claves reales) tras verificar que `.gitignore` lo protege en la nueva ubicación.
4. **Registro**: Se ha actualizado el registro en `docs/imported/2026-02-04_NB_Apps.md` apuntando a la nueva ubicación.

## 6. Próximos Pasos (Usuario)
- Ejecutar `npm install` en la nueva ubicación `C:\_Repositorio\AG_Proyectos\AG_NB_Apps`.
- Validar funcionamiento de scripts desde la nueva ruta.
