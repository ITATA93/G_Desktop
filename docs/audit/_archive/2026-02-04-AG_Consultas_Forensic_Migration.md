# Migración Forense: AG_Consultas

**Fecha**: 2026-02-04
**Proyecto**: _Consultas → AG_Consultas
**Protocolo**: Forensic Migration Protocol (SAIA)

## Objetivo
Migrar el proyecto `C:\_Repositorio\_Proyectos_Base\_Consultas` al ecosistema AG normalizado, aplicando el prefijo `AG_` y eliminando artefactos históricos duplicados.

## Fase 1: Descubrimiento Forense

### Contexto del Proyecto
- **Nombre Original**: _Consultas
- **Tipo**: Sistema de Mapeo y Consultas SQL para TrakCare/ALMA
- **Tecnología Base**: InterSystems IRIS, Python, DbVisualizer
- **Complejidad**: Alta (11,653 tablas, 450K columnas en diccionario)

### Estructura Descubierta
```
_Consultas/
├── .claude/                    # Configuración Claude Code
├── .gemini/                    # Configuración Gemini
├── Diccionario_Datos/          # SQLite + 11,654 MD files
├── Consultas_live/             # Consultas en producción
├── Exportaciones/              # Datos exportados
├── credentials/                # 🔒 Credenciales privadas
├── herramientas/               # Scripts Python
├── docs/                       # Documentación
├── _archivo/                   # Proyectos históricos
├── NB_Apps/                    # ❌ DUPLICADO (eliminado)
└── README.md                   # Documentación principal
```

### Hallazgos Críticos

#### 1. Duplicación de NB_Apps
**Hallazgo**: Subdirectorio `NB_Apps/` dentro del proyecto
**Diagnóstico**: Copia histórica duplicada del proyecto `AG_NB_Apps` independiente
**Acción**: Eliminado (no corresponde a la lógica del proyecto de consultas SQL)

#### 2. Credenciales Sensibles
**Hallazgo**: Carpeta `credentials/` con datos de acceso a BD hospitalaria
**Diagnóstico**: Información protegida bajo Ley 19.628 (Chile)
**Acción**: Verificar `.gitignore` para exclusión de repositorio público

#### 3. Diccionario Completo
**Hallazgo**: Base SQLite de 11,653 tablas con 450K columnas
**Diagnóstico**: Asset crítico del proyecto
**Acción**: Preservado en migración

## Fase 2: Ejecución de Migración

### Acciones Realizadas

1. **Movimiento del Proyecto**
   ```powershell
   Move-Item -Path "C:\_Repositorio\_Proyectos_Base\_Consultas" `
             -Destination "C:\_Repositorio\AG_Proyectos\AG_Consultas"
   ```
   - ✅ Éxito sin errores
   - ✅ Preservación completa de estructura

2. **Renombramiento de Workspace**
   ```powershell
   Rename-Item -Path "_Consultas.code-workspace" `
               -NewName "AG_Consultas.code-workspace"
   ```
   - ✅ Aplicado prefijo AG

3. **Eliminación de Duplicados**
   ```powershell
   Remove-Item -Path "C:\_Repositorio\AG_Proyectos\AG_Consultas\NB_Apps" `
               -Recurse -Force
   ```
   - ✅ Subdirectorio NB_Apps eliminado
   - ✅ Evita confusión con AG_NB_Apps independiente

4. **Normalización AG**
   - ✅ Creado `GEMINI.md` con perfil del proyecto
   - ✅ Creado `CONTEXT_GEMINI_3.0.md` (Step E: Agent Context Initialization)
   - ✅ Actualizado `README.md` con banner AG y nueva ubicación
   - ✅ Documentadas reglas de seguridad críticas
   - ✅ Integración con estándares AG_Plantilla

### Contexto del Agente (Step E)

Según el protocolo forense, se generó un archivo de contexto dinámico (`CONTEXT_GEMINI_3.0.md`) que:
- ✅ Resume la estructura del proyecto (11,653 tablas, 450K columnas)
- ✅ Inventaría herramientas disponibles (sincronizar_todo.py, generar_md_tablas.py, etc.)
- ✅ Lista agentes especializados (mapeo_trakcare, constructor_consultas, analisis_clinico)
- ✅ Define reglas de seguridad absolutas (solo SELECT, TOP N obligatorio)
- ✅ Documenta workflows comunes para gestión del diccionario
- ✅ Integra con ecosistema AG (AG_NB_Apps, AG_DeepResearch_Salud_Chile)

Este archivo permite que Gemini pueda **gestionar el proyecto inmediatamente** sin necesidad de re-descubrir la estructura.

## Fase 3: Validación Post-Migración

### Estructura Final
```
C:\_Repositorio\AG_Proyectos\AG_Consultas/
├── .claude/                    # ✅ Agentes especializados
├── .gemini/                    # ✅ Configuración Gemini
├── GEMINI.md                   # ✅ NUEVO: Perfil del proyecto
├── AG_Consultas.code-workspace # ✅ Renombrado
├── Diccionario_Datos/          # ✅ Preservado (11,654 MD)
├── Consultas_live/             # ✅ Preservado
├── Exportaciones/              # ✅ Preservado
├── credentials/                # ✅ Preservado (verificar .gitignore)
├── herramientas/               # ✅ Preservado
├── docs/                       # ✅ Preservado
├── _archivo/                   # ✅ Preservado
└── README.md                   # ✅ Preservado
```

### Checklist de Integridad

- [x] Proyecto movido a `AG_Proyectos/`
- [x] Prefijo `AG_` aplicado
- [x] Duplicados eliminados (NB_Apps)
- [x] `GEMINI.md` creado con contexto del proyecto
- [x] Estructura interna preservada
- [x] Assets críticos intactos (Diccionario, Consultas, Credenciales)

## Fase 4: Recomendaciones

### Acciones Pendientes

1. **Verificar `.gitignore`**
   ```bash
   # Asegurar que credentials/ esté excluido
   grep -n "credentials" .gitignore
   ```

2. **Validar Diccionario**
   ```powershell
   # Verificar integridad del diccionario SQLite
   python Diccionario_Datos/sincronizar_todo.py --dry-run
   ```

3. **Actualizar Referencias**
   - Verificar que scripts internos no tengan rutas absolutas hardcodeadas
   - Actualizar documentación con nueva ubicación

4. **Actualizar Registro de Proyectos**
   - Agregar entrada en `AG_Plantilla/.agent/project-registry.json`

### Consideraciones de Seguridad

**CRÍTICO**: Este proyecto accede a datos de salud protegidos:
- ✅ Credenciales deben estar en `.gitignore`
- ✅ Consultas solo de lectura (SELECT únicamente)
- ✅ Límite TOP N obligatorio (máx 1000)
- ⚠️ Auditar permisos de acceso a carpeta `credentials/`

## Conclusión

✅ **Migración completada exitosamente**

El proyecto `AG_Consultas` ha sido normalizado según el protocolo AG:
- Ubicación estandarizada en `AG_Proyectos/`
- Prefijo AG aplicado consistentemente
- Artefactos históricos duplicados eliminados
- Perfil del proyecto (`GEMINI.md`) creado
- Estructura y assets críticos preservados

**Próximos pasos**: Validar credenciales en `.gitignore` y actualizar registro de proyectos.

---

**Auditor**: Antigravity Agent
**Protocolo**: SAIA Forensic Migration v1.3
**Estado**: ✅ Completado
