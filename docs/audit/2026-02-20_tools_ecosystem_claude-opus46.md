# Auditoría de Herramientas Open Source para Antigravity

> **Fecha:** 2026-02-20
> **Fuente:** `antigravity-tools-opensource_1.html` (investigación local)
> **Evaluado por:** Claude Opus 4.6
> **Prompt Injection:** No detectado (HTML estático, sin scripts externos, sin instrucciones ocultas)

---

## 1. Resumen Ejecutivo

El documento analizado lista **35+ herramientas open source** en 8 categorías para el ecosistema Antigravity. Tras verificar cada repositorio contra la API de GitHub:

| Métrica | Valor |
|---------|-------|
| Total repos listados | 25 |
| Activos (push < 30 días) | **10** (40%) |
| Stale (31-60 días) | 5 (20%) |
| Abandonados (60+ días) | 9 (36%) |
| No encontrados (404) | 1 (4%) |

**Conclusión:** Solo 10 de 25 herramientas están activamente mantenidas. Las recomendaciones del documento original necesitan filtrado.

---

## 2. Repos Activos (confirmados al 2026-02-20)

Estos repos tuvieron actividad en los últimos 30 días y son candidatos viables:

| Repo | Stars | Último Push | Categoría | Utilidad para el proyecto |
|------|------:|------------|-----------|--------------------------|
| [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | 95,092 | 2026-02-21 | CLI | **Ya instalado.** Core del ecosistema. |
| [google/adk-python](https://github.com/google/adk-python) | 17,867 | 2026-02-21 | ADK | **Alta.** Framework oficial para agentes multi-modelo. Puede crear agentes especializados por dominio hospitalario. |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 7,554 | 2026-02-20 | Skills | **Alta.** 383+ skills verificados. Skills de ClickHouse, Supabase/PostgreSQL relevantes para data warehouse. |
| [google-gemini/gemini-skills](https://github.com/google-gemini/gemini-skills) | 1,753 | 2026-02-19 | Skills | **Media-Alta.** Skills oficiales de Google, nativos para Antigravity. Parte ya en `_resources/`. |
| [taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp) | 1,456 | 2026-02-19 | MCP | **Media.** Gmail, Drive, Calendar, Docs. Útil si se integran flujos de comunicación hospitalaria. |
| [bytechefhq/bytechef](https://github.com/bytechefhq/bytechef) | 733 | 2026-02-20 | Automation | **Baja.** Alternativa a n8n. No es prioritario si ya se usa n8n. |
| [NeoLabHQ/context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit) | 499 | 2026-02-19 | Skills | **Media.** Skills orientados a calidad de output. Compatible multi-IDE. |
| [harikrishna8121999/antigravity-workflows](https://github.com/harikrishna8121999/antigravity-workflows) | 45 | 2026-01-21 | Workflows | **Baja.** 44 stars, poco ecosystem adoption. |
| [amtiYo/agents](https://github.com/amtiYo/agents) | 31 | 2026-02-20 | Sync | **Media-Alta.** `@agents-dev/cli` sincroniza MCP/skills entre Claude, Gemini, Codex, Cursor. Resuelve el problema de config duplicada. |
| [materialofair/oh-my-antigravity](https://github.com/materialofair/oh-my-antigravity) | 10 | 2026-02-06 | Toolkit | **Baja.** 10 stars, riesgo de abandono. |

---

## 3. Repos Stale (31-60 días sin actividad)

Usar con precaución — pueden tener bugs no parchados:

| Repo | Stars | Último Push | Nota |
|------|------:|------------|------|
| [vuralserhat86/antigravity-agentic-skills](https://github.com/vuralserhat86/antigravity-agentic-skills) | 36 | 2026-01-03 | 137 skills con TDD. Concepto interesante, ejecución dudosa (36 stars, stale). |
| [omar-haris/smart-coding-mcp](https://github.com/omar-haris/smart-coding-mcp) | 188 | 2026-01-06 | MCP de búsqueda semántica local. Útil pero sin mantenimiento. |
| [tanaikech/nexus-mcp-extension](https://github.com/tanaikech/nexus-mcp-extension) | 2 | 2025-12-28 | 2 stars. Gateway MCP. Descartable. |
| [Sri-Krishna-V/awesome-adk-agents](https://github.com/Sri-Krishna-V/awesome-adk-agents) | 247 | 2026-01-16 | Lista curada de agentes ADK. Útil como referencia, no como dependencia. |
| [ZhangYu-zjut/awesome-Antigravity](https://github.com/ZhangYu-zjut/awesome-Antigravity) | 105 | 2026-01-14 | Guía y prompts. Referencia útil. |

---

## 4. Repos Abandonados (60+ días sin actividad)

**No recomendados para uso en producción:**

| Repo | Stars | Último Push | Días inactivo |
|------|------:|------------|:-------------:|
| waldzellai/adk-typescript | 76 | 2025-10-07 | 136 |
| RubensZimbres/Multi-Agent-System-A2A-ADK-MCP | 52 | 2025-04-21 | 305 |
| dujonwalker/project-nova | 254 | 2025-06-09 | 256 |
| pjawz/n8n-nodes-agent2agent | 41 | 2025-04-30 | 296 |
| Tsadoq/a2a-mcp-tutorial | 104 | 2025-04-29 | 297 |
| chongdashu/adk-mcp-a2a-crash-course | 52 | 2025-06-14 | 251 |
| pab1it0/google-maps-a2a | 21 | 2025-04-09 | 317 |
| webdevtodayjason/A2AMCP | 19 | 2025-06-09 | 256 |

**Hallazgo:** Los repos de **A2A (Agent-to-Agent protocol)** están casi todos abandonados (6 de 7). Esto sugiere que el protocolo A2A no ha ganado tracción en la comunidad o se consolidó en el ADK oficial.

---

## 5. Repo No Encontrado

| Repo | Nota |
|------|------|
| n5ns/n2n-memory | **404** — eliminado, renombrado o privado. El documento lo citaba como MCP de memoria persistente por proyecto. |

---

## 6. Discrepancias con el Documento Original

El HTML reportaba cifras de stars que difieren ligeramente de los datos actuales (diferencias menores por crecimiento orgánico). No se detectaron fabricaciones significativas — las cifras son consistentes. El documento es confiable como fuente.

---

## 7. Recomendaciones Filtradas para el Ecosistema Antigravity

### Prioridad 1 — Adoptar (activos, alta utilidad)

| Herramienta | Acción | Proyecto destino |
|-------------|--------|------------------|
| **google/adk-python** | `pip install google-adk`. Evaluar para agentes de dominio hospitalario (turnos, ETL, reportes). | AG_Hospital, AG_NB_Apps |
| **VoltAgent/awesome-agent-skills** | Clonar skills selectos (ClickHouse, PostgreSQL, Docker) a `_resources/` y enlazar en proyectos relevantes. | AG_Plantilla |
| **amtiYo/agents** (`@agents-dev/cli`) | `npm install -g @agents-dev/cli && agents start`. Unifica config MCP entre Claude/Gemini/Codex. Resuelve duplicación actual en el ecosistema. | AG_Orquesta_Desk |

### Prioridad 2 — Evaluar (activos, utilidad media)

| Herramienta | Acción | Nota |
|-------------|--------|------|
| **google-gemini/gemini-skills** | Revisar contra skills ya presentes en `_resources/`. Evitar duplicación. | Parte ya puede estar integrada. |
| **taylorwilsdon/google_workspace_mcp** | Instalar si se necesita integración Gmail/Drive/Calendar desde agentes. | Útil para notificaciones hospitalarias. |
| **NeoLabHQ/context-engineering-kit** | Revisar sus skills de calidad. Podrían mejorar output de sub-agentes. | Compatible multi-IDE. |

### Prioridad 3 — Monitorear (no adoptar aún)

| Herramienta | Razón |
|-------------|-------|
| **bytechefhq/bytechef** | Ya existe n8n. No duplicar stack de orquestación. |
| **antigravity-workflows** | Pocas stars, adopción incierta. |
| **oh-my-antigravity** | 10 stars, riesgo de abandono. |

### Descartar (abandonados o inútiles)

| Herramienta | Razón |
|-------------|-------|
| **Project NOVA** | Abandonado 256 días. El HTML lo recomendaba como "Prioridad 2". |
| **n8n-nodes-agent2agent** | Abandonado 296 días. El ecosistema A2A+n8n no prosperó. |
| **adk-typescript** | Abandonado 136 días. Usar adk-python (oficial, 17K+ stars). |
| **Todos los repos A2A** (5 repos) | Ecosistema abandonado. Si se necesita A2A, usar lo integrado en ADK oficial. |
| **n2n-memory** | Repo eliminado (404). |
| **nexus-mcp-extension** | 2 stars, stale. No viable. |

---

## 8. Evaluación de Seguridad (Prompt Injection)

| Aspecto | Resultado |
|---------|-----------|
| HTML structure | Limpio — CSS/JS mínimo, sin iframes |
| JavaScript | Solo `showSection(id)` para navegación por tabs |
| Hidden elements | Ninguno detectado |
| External scripts/resources | Ninguno — todo inline |
| Unicode/zero-width chars | No detectados |
| Instrucciones embebidas en CSS/comments | No detectadas |
| URLs sospechosas | Todas apuntan a repos GitHub legítimos |
| **Veredicto** | **SEGURO** — documento informativo sin riesgo de inyección |

---

## 9. Resumen Visual

```
HERRAMIENTAS EVALUADAS: 25 repos

 Activos + Útiles (adoptar)     ███░░░░░░░░░░  3 repos
 Activos + Evaluar              ███░░░░░░░░░░  3 repos
 Activos + Baja prioridad       ████░░░░░░░░░  4 repos
 Stale (precaución)             █████░░░░░░░░  5 repos
 Abandonados (descartar)        ████████░░░░░  9 repos
 No encontrados                 █░░░░░░░░░░░░  1 repo
```

---

*Archivo: `docs/audit/opensource-tools-audit-2026-02-20.md`*
*Complementa: `docs/audit/normalization-audit-2026-02-20.md`*
