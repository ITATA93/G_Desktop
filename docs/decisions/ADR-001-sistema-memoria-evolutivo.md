# ADR-001: Estrategia de Escalabilidad del Sistema de Memoria

## Estado
Aceptado

## Contexto
El sistema Antigravity necesita gestionar dos dimensiones de escalabilidad:
1.  **Horizontal**: Crecimiento en número de proyectos (ej. 50+ apps).
2.  **Vertical (Alta Densidad)**: Profundidad de información dentro de un solo proyecto (ej. Documentación integral de un Hospital).

## Decisión
Implementaremos una estrategia dual:
1.  **Registro Ligero (JSON)** para gestión de múltiples proyectos.
2.  **Patrón "Knowledge Vault" (Wiki Markdown)** para proyectos de alta densidad.

## Racional
Para dominios complejos como un Hospital, el cuello de botella no es el almacenamiento (disco), sino la **Ventana de Contexto** del Agente. No podemos "leer todo". Necesitamos "navegar".

## Estrategia de Evolución

### Dimensión 1: Inventario de Proyectos (Horizontal)
- **Fase 1 (Actual)**: `project_registry.json`. Simple, auditable.
- **Fase 2 (>50 apps)**: Migración a SQLite.

### Dimensión 2: Documentación de Dominio (Vertical)
- **Estrategia**: Patrón **Knowledge Vault**.
- **Implementación**:
    - Descomposición en archivos atómicos (<500 líneas).
    - Indices (`README.md`) en cada carpeta actuando como mapas.
    - Metadatos YAML (Frontmatter) en cada archivo.
- **Búsqueda**: El agente utiliza los índices para encontrar la ruta al dato exacto, minimizando el consumo de tokens ("Agentic Crawling").

## Consecuencias
- Los proyectos complejos como `AG_Hospital_Organizador` deben reestructurar su carpeta `docs/` siguiendo el estándar `docs/standards/knowledge_vault_pattern.md`.
- Se evita la necesidad prematura de RAG (Vector DB) si la estructura de archivos es semánticamente sólida.
