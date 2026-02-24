Now I have all the context. Here is the consolidated report.

---

# Reporte de Auditor├¡a Consolidado V2.0 ÔÇö Ecosistema Antigravity

**Fecha**: 2026-02-20
**Auditor**: Master Orchestrator (Claude Opus 4.6)
**Fuentes**: Gemini V1/V2, Claude V1, Codex V1/V2 (con verificaci├│n independiente de c├│digo)
**Alcance**: 13 proyectos AG (12 sat├®lites + 1 orquestador) + pipeline de dispatch + tooling de auditor├¡a
**Health Promedio del Ecosistema**: **51/100** (Umbral Cr├¡tico)

---

## 0. Meta-Hallazgo: Fallo del Pipeline de Consenso

Antes del an├ílisis t├®cnico, un hallazgo estructural sobre el propio proceso de auditor├¡a:

**2 de 3 agentes auditores fallaron por resoluci├│n de variables en los scripts de dispatch.**

- **Claude (V1)**: Recibi├│ `$CurrentPrompt` literal en lugar del prompt resuelto. El script `dispatch.ps1:119` asigna `$CurrentPrompt = $fullPrompt`, pero los scripts de lanzamiento en `scripts/temp/run_claude.ps1` no inyectaron correctamente la variable.
- **Codex (V1/V2)**: Recibi├│ `$FinalPrompt` literal. El bloque de fallback research (`dispatch.ps1:236-246`) construye `$FinalPrompt` pero los scripts `run_codex.ps1` y `run_codex_review.ps1` usaron la variable sin expandirla.

**Impacto**: Solo Gemini ejecut├│ correctamente, produciendo un reporte superficial de 14 l├¡neas. El protocolo Mixture-of-Experts se degrad├│ a un single point of analysis. Esto invalida la premisa del consenso multi-agente.

**Causa ra├¡z**: Los scripts en `scripts/temp/` son oneshots manuales que construyen prompts con interpolaci├│n de strings PowerShell pero sin validaci├│n de que las variables est├®n definidas. No hay `Set-StrictMode` ni verificaci├│n de `$null`.

---

## 1. Hallazgos Cr├¡ticos de Seguridad

### SEC-01: Credenciales de Producci├│n Expuestas (CRITICAL ÔÇö P0)

**Proyecto**: AG_Consultas
**Estado**: SIN REMEDIAR desde 2026-02-17 (3+ d├¡as de exposici├│n conocida)

| Vector | Archivo | Credencial | Instancias |
|--------|---------|------------|------------|
| IDE config | `.vscode/settings.json` | IRIS password `sd260710sd` | 4 |
| IDE config | `.vscode/settings.json` | SIDRA password `hkEVC9AFVjFeRTkp` | 1 |
| Archivo legacy | `_archivo_*/scripts_anteriores/*.py` | IRIS password `sd260710sd` | 3 |

**An├ílisis de blast radius**:
- **IRIS**: Sistema cl├¡nico hospitalario, usuario `18233087-6`. Acceso directo a registros m├®dicos.
- **SIDRA**: SQL Server, usuario `sidra`. Infraestructura de datos de salud.
- `.vscode/settings.json` es un vector de propagaci├│n: se copia autom├íticamente al onboardear nuevos desarrolladores.
- El directorio `_archivo_Mapeo_Anterior_2026-01-30/` crea falsa seguridad ÔÇö las credenciales adentro son id├®nticas a las activas.

**Veredicto**: La rotaci├│n de credenciales debi├│ ejecutarse el 2026-02-17. Cada d├¡a adicional de exposici├│n es un hallazgo en s├¡ mismo.

### SEC-02: Cadena de Ataque Compuesta ÔÇö Prompt Injection + Permisos Sin Restricci├│n (HIGH)

Existe una cadena de ataque de 3 eslabones entre AG_Plantilla y AG_Orquesta:

1. **AG_Plantilla `dispatch.sh`**: Concatena input de usuario sin sanitizar (`FULL_PROMPT="$INSTRUCTIONS\n---\nTask: $PROMPT"`). Sin boundaries estoc├ísticos.
2. **AG_Plantilla `dispatch.sh`**: Usa `--dangerously-skip-permissions` (backlog H-01). El agente ejecuta con acceso total al filesystem.
3. **Resultado**: Prompt inyectado ÔåÆ acceso filesystem sin restricciones ÔåÆ exfiltraci├│n de credenciales.

**Contraste**: AG_Orquesta `dispatch.ps1` ya implementa mitigaci├│n (boundaries estoc├ísticos con GUID en l├¡neas 86-91, sanitizaci├│n de tags en l├¡nea 91). **Pero AG_Plantilla no fue remediado.** El template que genera los dispatch scripts de todos los proyectos sat├®lite sigue siendo vulnerable.

### SEC-03: `--no-verify` en Scripts Automatizados (HIGH)

Tres scripts del orquestador bypasean pre-commit hooks:

| Archivo | L├¡nea | Contexto |
|---------|-------|----------|
| `scripts/audit_ecosystem.py` | 329 | Auto-fix commit |
| `scripts/propagate.py` | 186 | Template sync commit |
| `scripts/temp/commit_satellites.py` | 12 | Normalizaci├│n satelital |

El pre-commit config incluye `detect-private-key` y `check-added-large-files`. Usar `--no-verify` en commits automatizados significa que **los scripts que propagan archivos a trav├®s del ecosistema bypasean los hooks dise├▒ados para detectar fugas de credenciales durante la propagaci├│n**. Patr├│n autodestructivo.

### SEC-04: CI/CD Eliminado (HIGH)

Ambos workflows (`.github/workflows/ci.yml` y `security.yml`) est├ín **borrados** seg├║n git status. El orquestador ÔÇö el hub central de gobernanza ÔÇö no tiene enforcement automatizado:

- Cero escaneo de credenciales en push
- Cero verificaci├│n de normalizaci├│n en PR
- Cero pipeline de seguridad
- Todo depende de ejecuci├│n manual de `audit_ecosystem.py`

### SEC-05: Backlog de Seguridad Abierto (HIGH ÔÇö 4 items)

De la sesi├│n 2026-02-17: 13 hallazgos encontrados, 12 remediados, 4 diferidos. Todos siguen abiertos:

| ID | Hallazgo | Ubicaci├│n | Riesgo |
|----|----------|-----------|--------|
| H-01 | `--dangerously-skip-permissions` en dispatch | AG_Plantilla `dispatch.sh:L197,215` | Agente sin permission gates; combinado con prompt injection = operaciones arbitrarias en filesystem |
| H-02 | Response refleja input del usuario | AG_Plantilla `agent_service.py:L84` | XSS reflejado, fuga de credenciales en logs |
| M-01 | `eval` en health-check.sh | AG_Plantilla `scripts/setup/health-check.sh:L38` | Command injection si las condiciones se vuelven din├ímicas |
| M-02 | Auth API bypaseada en dev mode | AG_Plantilla `src/main.py:L49` | Servidor dev expuesto en red = API sin autenticaci├│n |

---

## 2. Puntos Ciegos del Scanner

El scanner de seguridad (`audit_ecosystem.py`) tiene exclusiones intencionales que crean gaps explotables:

| Exclusi├│n | Riesgo Concreto |
|-----------|-----------------|
| `SKIP_DIRS: "tests"` | Credenciales reales en test fixtures ser├¡an invisibles |
| `SKIP_DIRS: "temp"` | 30 archivos en `scripts/temp/` nunca escaneados (incluyendo scripts con paths hardcodeados) |
| `SKIP_DIRS: "community"` | Vectore de supply-chain: credenciales inyectadas en c├│digo tercero invisibles |
| `SCAN_EXTENSIONS` no incluye `.sh`, `.ps1`, `.md`, `.txt` | Los flags `--dangerously-skip-permissions`, paths hardcodeados, y el `eval` vulnerable viven en archivos que el scanner **nunca examina** |
| `SAFE_LINE_PATTERNS: "^\s*#"` | `# password: realpassword123` ser├¡a ignorado |
| `SAFE_LINE_PATTERNS: _template` | Cualquier archivo con `_template` en el path es inmune |
| `SKIP_FILE_PATTERNS: "audit_ecosystem"` | El scanner se excluye a s├¡ mismo ÔÇö razonable, pero el `KNOWN_CREDENTIALS` registry dentro contiene los passwords en plaintext como strings de b├║squeda |

**Hallazgo m├ís grave**: `.sh` y `.ps1` no est├ín en `SCAN_EXTENSIONS`. Todo el dispatch pipeline, toda la infraestructura de shells, es invisible para el scanner.

---

## 3. Fallas Arquitect├│nicas Sist├®micas

### 3.1 El Contrato de Normalizaci├│n es Declarativo, No Enforced

El ecosistema define un est├índar claro: 7 archivos requeridos, 7 recomendados, gesti├│n de tareas estructurada, protocolos de sesi├│n, y gates de calidad de contenido. El tooling para auditar esto existe y est├í bien construido.

**Pero no hay mecanismo de enforcement:**
- No hay CI/CD que ejecute la auditor├¡a en commit o PR
- No hay pre-commit hook que valide normalizaci├│n
- El modo `--fix` auto-crea archivos pero los commitea con `--no-verify`
- Los proyectos pueden permanecer D-grade indefinidamente sin consecuencia

**Resultado**: 5 proyectos lograron A-grade porque sus mantenedores adoptaron activamente el est├índar. Los otros 7 no lo hicieron porque nada los oblig├│. Esto es un fallo de arquitectura de gobernanza, no de documentaci├│n.

### 3.2 Ecosistema Bimodal: "Normalizado" vs. "Abandonado"

```
88-100: ÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûê  5 proyectos (A-grade)
36-48:  ÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûê              3 proyectos (B/C-grade)  
10-16:  ÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûêÔûê          4 proyectos (D/F-grade)
```

No hay t├®rmino medio. Los proyectos o tienen infraestructura completa (88+ health) o casi ninguna (10-16). La infraestructura de autonom├¡a es un paquete todo-o-nada (propagado desde `AG_Plantilla/_template/`), no un sistema modular donde los proyectos puedan adoptar capacidades incrementalmente.

Los 4 peores comparten perfil id├®ntico:

| Proyecto | Health | Perfil |
|----------|--------|--------|
| AG_Hospital | 10 | Sin gitignore, sin README, sin docs, sin GEMINI, sin CLAUDE, sin agentes, sin dispatch, sin session protocol, sin memoria |
| AG_TrakCare_Explorer | 10 | Mismo perfil |
| AG_Analizador_RCE | 16 | Autonom├¡a 0/6 |
| AG_SV_Agent | 16 | Autonom├¡a 0/6 |

**Estos proyectos existen fuera del sistema de gobernanza completamente.** Tienen repos git pero cero infraestructura de agentes, cero tracking de tareas, cero continuidad de sesi├│n.

### 3.3 Gesti├│n de Tareas Fragmentada ÔÇö Problema de Dead-Letter

**6 de 12 proyectos tienen NO-TASKS.** El sistema `cross_task.py` est├í dise├▒ado para delegar tareas entre proyectos, pero no puede delegar a un proyecto que no tiene estructura de intake. `send_norm_tasks.py` puede emitir tareas de normalizaci├│n, pero la mitad de los proyectos no tienen buz├│n para recibirlas.

### 3.4 `tasks_awareness`: El Gap M├ís Pervasivo

**11 de 12 proyectos** fallan la verificaci├│n de `tasks_awareness` (GEMINI.md debe referenciar "tasks"). Sin esto, los agentes AI trabajando en un proyecto no saben que deben revisar `docs/TASKS.md` al inicio de sesi├│n. El sistema completo de orquestaci├│n cross-task est├í efectivamente deshabilitado a nivel de hoja.

### 3.5 `gemini_keywords`: Gate de Calidad Vac├¡o

**10 de 12 proyectos** fallan el check de `gemini_keywords` (GEMINI.md debe contener 3+ de: "absolute rules", "complexity", "sub-agent", "commit"). Agentes operando en 10/12 proyectos carecen de las instrucciones de gobernanza que restringen su comportamiento. La ausencia de "absolute rules" significa que los agentes podr├¡an no estar bound a directivas como "nunca crear archivos en root" y "nunca commitear secrets".

### 3.6 Fragilidad de Resoluci├│n de Entorno

`env_resolver.py` tiene un fallback path (`audit_ecosystem.py:40-53`) que defaultea a `C:\_Repositorio` cuando el resolver no puede importarse. El entorno activo es `desktop` con base path `W:\Antigravity_OS`. Si `audit_ecosystem.py` se ejecuta sin `env_resolver` en el Python path (shell nuevo, CI runner, otra m├íquina), escanea el directorio incorrecto completamente. La auditor├¡a reportar├¡a cero proyectos y cero hallazgos ÔÇö un **silencio falso-negativo** que parece un certificado de salud limpio.

Adem├ís, `propagate.py` tiene el path `C:\_Repositorio` hardcodeado en l├¡nea 24-27 sin ning├║n fallback ni env_resolver. Si se ejecuta en el entorno desktop actual (`W:\Antigravity_OS`), simplemente no encontrar├í nada.

### 3.7 AG_Plantilla: Auditee Exento

`project_registry.json` lista 13 proyectos. La auditor├¡a escanea 12. **AG_Plantilla est├í excluido de la auditor├¡a que genera.** Este es el proyecto m├ís security-critical del ecosistema (define dispatch scripts, API config, y todos los patrones de seguridad por defecto) y nunca es auditado por el scanner.

---

## 4. Hallazgos Espec├¡ficos del Dispatch Pipeline

### 4.1 Doble Escape Inseguro (dispatch.ps1:151)

```powershell
$SafePrompt = $CurrentPrompt -replace '"', '\"'
claude -p "$SafePrompt" 2> $ErrorLog.FullName
```

El prompt ya fue sanitizado en l├¡nea 91 (`-replace "</?user_task.*?>", "[REDACTED_TAG]"`), pero luego se aplica un escape de comillas dobles que podr├¡a romper la sanitizaci├│n si el prompt contiene secuencias como `\"<user_task...>`. El orden de operaciones es: sanitize ÔåÆ escape ÔåÆ invoke. Un payload crafted con `\"` prefijado podr├¡a sobrevivir la sanitizaci├│n.

### 4.2 Error Log como Canal de Inyecci├│n (dispatch.ps1:128-130)

```powershell
$PrevError = Get-Content $ErrorLogPrev -Raw
$CurrentPrompt = @"
$fullPrompt
---
SYSTEM NOTE: Your previous attempt failed...
Error details:
$PrevError
"@
```

El contenido del error log del intento anterior se inyecta directamente en el prompt del retry sin sanitizaci├│n. Si un agente malicioso (o un error crafted) produce output que contiene instrucciones de sistema, estas se inyectan como contexto "confiable" en el retry. Mismo patr├│n en el research fallback (l├¡neas 216-228, 236-246).

### 4.3 Research Fallback Recursivo (dispatch.ps1:232)

```powershell
& $MyInvocation.MyCommand.Path "researcher" $ResearchPrompt "codex"
```

El dispatch se invoca recursivamente. Si el agente "researcher" tampoco existe o tambi├®n falla, no hay protecci├│n contra recursi├│n infinita (solo se salva porque el agente "researcher" no matchea en la condici├│n `$AgentName -ne "researcher"` de l├¡nea 211). Pero si el manifiesto define un agente llamado "researcher" que a su vez falla, el fallback intentar├¡a invocar al researcher de nuevo.

### 4.4 `scripts/temp/` como Shadow Operations Center

30 archivos en `scripts/temp/`, incluyendo:
- `commit_satellites.py`: Commitea en todos los repos sat├®lite con `--no-verify` (y usa path hardcodeado `C:\_Repositorio` que no funciona en el entorno actual)
- `audit_ecosystem.py` (copia separada del principal)
- 8+ scripts de lanzamiento PowerShell para el pipeline MoE
- Prompts de auditor├¡a en plaintext

Este directorio est├í en `SKIP_DIRS` del scanner, es untracked en git, y contiene scripts operativos que modifican el ecosistema. Es un punto ciego total.

---

## 5. Tabla Consolidada de Riesgo por Proyecto

| Proyecto | Health | Sec | Gobernanza | Autonom├¡a | Riesgo Dominante |
|----------|--------|-----|------------|-----------|------------------|
| AG_Consultas | 48 | **8 CRITICAL** | A-struct / F-sec | Parcial | Credenciales activas expuestas |
| AG_Hospital | 10 | 0 reportados | D | Manual (0/6) | Invisible al orquestador |
| AG_TrakCare_Explorer | 10 | 0 reportados | D | Manual (0/6) | Sin .gitignore, sin contenci├│n |
| AG_Analizador_RCE | 16 | 0 reportados | D | Manual (0/6) | Autonom├¡a cero |
| AG_SV_Agent | 16 | 0 reportados | D | Manual (0/6) | Gobernanza ausente |
| AG_SD_Plantilla | 36 | 0 reportados | C | Manual | Sin devlog/tasks/changelog |
| AG_Notebook | 36 | 0 reportados | C | Manual | Sin docs requeridos |
| AG_Plantilla | N/A | **4 backlog HIGH** | Excluido | Auto | Template vulnerable propaga a todo el ecosistema |
| A-group (5) | 88+ | 0 reportados | A | Auto | Gap en `tasks_awareness` |

---

## 6. Roadmap de Remediaci├│n Priorizado

### Fase 0: Emergencia (0-48 horas)

| # | Acci├│n | Target | Justificaci├│n |
|---|--------|--------|---------------|
| 1 | **Rotar password IRIS** (`sd260710sd`) | Infraestructura IRIS DB | Exposici├│n 3+ d├¡as; acceso a sistema hospitalario |
| 2 | **Rotar password SIDRA** (`hkEVC9AFVjFeRTkp`) | SIDRA SQL Server | Exposici├│n confirmada en 2 proyectos |
| 3 | `git rm --cached .vscode/settings.json` + agregar a `.gitignore` | AG_Consultas | Eliminar vector de propagaci├│n IDE |
| 4 | Eliminar `_archivo_Mapeo_Anterior_2026-01-30/` | AG_Consultas | C├│digo muerto con credenciales vivas |
| 5 | Remover `--dangerously-skip-permissions` de AG_Plantilla dispatch | AG_Plantilla | Bloquear cadena de ataque compuesta SEC-02 |

### Fase 1: Seguridad Estructural (1-2 semanas)

| # | Acci├│n | Target | Justificaci├│n |
|---|--------|--------|---------------|
| 6 | Eliminar `--no-verify` de todos los scripts automatizados | AG_Orquesta | Restaurar enforcement de pre-commit hooks |
| 7 | Agregar `.sh`, `.ps1`, `.md`, `.txt` a `SCAN_EXTENSIONS` | `audit_ecosystem.py` | Cerrar punto ciego del scanner en shell scripts |
| 8 | Restaurar CI/CD pipelines (`.github/workflows/`) | AG_Orquesta | Reestablecer gates automatizados |
| 9 | Incluir AG_Plantilla en el scope de auditor├¡a | `audit_ecosystem.py` | Template no debe ser exento |
| 10 | Arreglar fallback de `env_resolver` para fallar ruidosamente | `audit_ecosystem.py:40` | Prevenir silencio falso-negativo |
| 11 | Arreglar paths hardcodeados `C:\_Repositorio` en `propagate.py` | `propagate.py:24-27` | Script no funciona en entorno actual |
| 12 | Agregar `.vscode/` al `.gitignore` template en AG_Plantilla | AG_Plantilla | IDE config es vector recurrente de credenciales |
| 13 | Sanitizar error logs antes de inyectarlos en retry prompts | `dispatch.ps1:128` | Cerrar canal de inyecci├│n indirecta |

### Fase 2: Normalizaci├│n Enforced (2-4 semanas)

| # | Acci├│n | Target | Justificaci├│n |
|---|--------|--------|---------------|
| 14 | Propagar GEMINI.md con keywords de gobernanza completos a los 12 proyectos | Ecosystem-wide | Cierra gap `gemini_keywords` (10/12 proyectos) |
| 15 | Agregar bloque `tasks_awareness` a todos los GEMINI.md | Ecosystem-wide | Habilita delegaci├│n cross-task (11/12 proyectos) |
| 16 | Ejecutar normalizaci├│n para los 4 proyectos D-grade | AG_Hospital, AG_TrakCare_Explorer, AG_Analizador_RCE, AG_SV_Agent | Bootstrap de gobernanza m├¡nima |
| 17 | Crear pre-commit hook espec├¡fico para patrones de credenciales conocidos | AG_Plantilla template | Catch credenciales en commit time (m├ís all├í de `detect-private-key`) |
| 18 | Purgar o commitear `scripts/temp/` | AG_Orquesta | Eliminar shadow ops center no versionado |
| 19 | Agregar `Set-StrictMode -Version Latest` a todos los scripts PowerShell | AG_Orquesta + AG_Plantilla | Prevenir fallos silenciosos por variables no resueltas |

### Fase 3: Recuperaci├│n de Autonom├¡a (4-8 semanas)

| # | Acci├│n | Target | Justificaci├│n |
|---|--------|--------|---------------|
| 20 | Deploy session-protocol + dispatch a los 7 proyectos manual-mode | 7 proyectos | Habilitar self-healing, audit trail, memoria cross-sesi├│n |
| 21 | Implementar modo `--fix` como step de CI (no invocaci├│n manual) | AG_Orquesta CI | Normalizaci├│n continua, no epis├│dica |
| 22 | Modularizar paquete de autonom├¡a | AG_Plantilla template | Permitir adopci├│n incremental (tasks sin dispatch, memoria sin workflows) |
| 23 | Pol├¡tica de rotaci├│n trimestral de credenciales | Gobernanza | Prevenir gaps de exposici├│n de 3+ d├¡as |
| 24 | Validar dispatch pipeline end-to-end antes de cada ejecuci├│n MoE | AG_Orquesta | Prevenir el meta-fallo de variable resolution que invalid├│ esta auditor├¡a |

---

## 7. Recomendaciones Sist├®micas

1. **Pasar de "auditar y reparar" a "prevenir y enforcer."** El modelo actual descubre problemas despu├®s del hecho. Pre-commit hooks, CI gates, y enforcement a nivel de template prevendr├¡an que proyectos D-grade existan.

2. **Auditar al auditor.** AG_Plantilla genera los patrones de seguridad, dispatch scripts, y configuraciones por defecto para todo el ecosistema, pero est├í excluido de la auditor├¡a. Este es el gap de cobertura m├ís importante a cerrar.

3. **Eliminar la brecha bimodal.** El paquete de autonom├¡a todo-o-nada debe descomponerse en m├│dulos incrementales. Un proyecto deber├¡a poder adoptar gesti├│n de tareas sin necesitar un pipeline de dispatch completo.

4. **Tratar `.vscode/` como untrusted.** Es un vector recurrente de credenciales en este ecosistema. Debe ir en `.gitignore` global.

5. **Version-controlar artefactos de auditor├¡a.** Los reportes sentados como archivos untracked representan conocimiento institucional en riesgo de p├®rdida.

6. **Arreglar el pipeline MoE antes de usarlo en producci├│n.** El fallo de 2/3 agentes por variables PowerShell no resueltas demuestra que el pipeline de consenso multi-agente no est├í listo para producci├│n. Sin `Set-StrictMode`, los scripts fallan silenciosamente.

7. **Separar baseline de seguridad del baseline de calidad de c├│digo.** Ambos deben ser gates, pero la seguridad nunca deber├¡a ser diferida por deuda de normalizaci├│n.

---

## 8. Juicio Final

Este ecosistema exhibe un **patr├│n de descomposici├│n de gobernanza** donde algunos proyectos son operacionalmente funcionales pero inseguros, mientras otros son tanto inseguros como no gobernados. El riesgo inmediato m├ís alto es la exposici├│n activa de credenciales hospitalarias. El riesgo estrat├®gico m├ís alto es que solo una minor├¡a de proyectos satisface la estructura mandatoria, haciendo imposible el enforcement de seguridad repetible sin endurecer la normalizaci├│n como contrato de plataforma enforced.

El hecho de que el propio proceso de auditor├¡a multi-agente fall├│ (2/3 agentes recibieron variables sin resolver) es un s├¡ntoma del mismo problema: infraestructura de orquestaci├│n que funciona en el camino feliz pero falla silenciosamente en producci├│n.

---

*Generado por Master Orchestrator ÔÇö AG_Orquesta_Desk, 2026-02-20*
*Consolidaci├│n de: Gemini V1/V2, Claude V1, Codex V1/V2 + verificaci├│n independiente de c├│digo*

FINALIZADO
