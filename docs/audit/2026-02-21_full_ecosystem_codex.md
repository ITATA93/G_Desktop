# Auditoria Integral de Proyectos Vinculados - 2026-02-21 07:37:52

> Generado desde `AG_Orquesta_Desk` usando `config/project_registry.json` + auditoria tecnica automatizada por repo.

## 1. Alcance y metodologia

- Fecha de auditoria: `2026-02-21`
- Base analizada: `w:\Antigravity_OS`
- Proyectos en registro oficial: `13`
- Proyectos auditados en total: `14`
- Criterios: estructura requerida/recomendada, seguridad, autonomia agentica, calidad documental, estado Git, senales operativas (tests/CI/tareas).

## 2. Resumen ejecutivo

- Instalados/accesibles: `14/14`
- Promedio de salud ecosistema: `87/100`
- Hallazgos de seguridad (critical/high): `0`
- Repos con arbol de trabajo sucio: `13`
- Proyectos con autonomia baja (<=2/6): `4`
- Proyectos con brechas de calidad de contenido: `7`

### 2.1 Distribucion de grades

| Grade | Cantidad |
|---|---:|
| A | 14 |
| B | 0 |
| C | 0 |
| D | 0 |
| F | 0 |

### 2.2 Estado por categoria

| Categoria | Proyectos | Instalados | Salud promedio |
|---|---:|---:|---:|
| admin | 4 | 4 | 86/100 |
| hospital-equipo | 2 | 2 | 88/100 |
| hospital-personal | 4 | 4 | 90/100 |
| personales | 1 | 1 | 94/100 |
| privado | 1 | 1 | 74/100 |
| proyectos | 2 | 2 | 88/100 |

## 3. Hallazgos priorizados

### 3.1 Criticos

- No se detectaron credenciales hardcodeadas ni findings de seguridad de severidad alta/critica en el escaneo automatizado actual.

### 3.2 Altos

- `AG_Hospital`: autonomia agentica baja (`16%`). Riesgo de ejecucion manual y baja repetibilidad operacional.
- `AG_Notebook`: autonomia agentica baja (`33%`). Riesgo de ejecucion manual y baja repetibilidad operacional.
- `AG_SD_Plantilla`: autonomia agentica baja (`16%`). Riesgo de ejecucion manual y baja repetibilidad operacional.
- `AG_SV_Agent`: autonomia agentica baja (`16%`). Riesgo de ejecucion manual y baja repetibilidad operacional.

### 3.3 Medios

- `AG_Consultas`: brechas de calidad detectadas en `gemini_keywords`.
- `AG_DeepResearch_Salud_Chile`: brechas de calidad detectadas en `gemini_keywords`.
- `AG_Hospital_Organizador`: brechas de calidad detectadas en `gemini_keywords`.
- `AG_Informatica_Medica`: brechas de calidad detectadas en `gemini_keywords`.
- `AG_Lists_Agent`: brechas de calidad detectadas en `changelog_active`.
- `AG_NB_Apps`: brechas de calidad detectadas en `gemini_keywords`.
- `AG_Orquesta_Desk`: brechas de calidad detectadas en `gemini_keywords`.

### 3.4 Bajos

- `AG_Consultas`: faltan recomendados `config/`.
- `AG_Hospital`: faltan recomendados `config/, .gemini/, .agent/`.
- `AG_Hospital_Organizador`: faltan recomendados `config/`.
- `AG_Lists_Agent`: faltan recomendados `config/`.
- `AG_NB_Apps`: faltan recomendados `config/`.
- `AG_Notebook`: faltan recomendados `config/, .gemini/`.
- `AG_SD_Plantilla`: faltan recomendados `config/, .gemini/, .agent/`.
- `AG_SV_Agent`: faltan recomendados `config/, .gemini/, .agent/`.
- `AG_TrakCare_Explorer`: faltan recomendados `config/`.

### 3.5 Higiene Git

- `AG_Plantilla`: `3` archivos con cambios locales (`3` untracked).
- `AG_Analizador_RCE`: `41` archivos con cambios locales (`41` untracked).
- `AG_Consultas`: `46` archivos con cambios locales (`34` untracked).
- `AG_DeepResearch_Salud_Chile`: `1` archivos con cambios locales (`0` untracked).
- `AG_Hospital`: `6` archivos con cambios locales (`6` untracked).
- `AG_Hospital_Organizador`: `3421` archivos con cambios locales (`46` untracked).
- `AG_Informatica_Medica`: `68` archivos con cambios locales (`58` untracked).
- `AG_Lists_Agent`: `18` archivos con cambios locales (`14` untracked).
- `AG_NB_Apps`: `65` archivos con cambios locales (`57` untracked).
- `AG_Notebook`: `5` archivos con cambios locales (`4` untracked).
- `AG_SD_Plantilla`: `5` archivos con cambios locales (`5` untracked).
- `AG_SV_Agent`: `4` archivos con cambios locales (`4` untracked).
- `AG_TrakCare_Explorer`: `17` archivos con cambios locales (`17` untracked).

### 3.6 Registro potencialmente desactualizado

- `AG_Analizador_RCE`: ultimo commit `2026-02-20` posterior a `last_update` del registro (`2026-02-17`).
- `AG_Consultas`: ultimo commit `2026-02-20` posterior a `last_update` del registro (`2026-02-17`).
- `AG_DeepResearch_Salud_Chile`: ultimo commit `2026-02-20` posterior a `last_update` del registro (`2026-02-17`).
- `AG_Hospital`: ultimo commit `2026-02-20` posterior a `last_update` del registro (`2026-02-17`).
- `AG_Hospital_Organizador`: ultimo commit `2026-02-18` posterior a `last_update` del registro (`2026-02-17`).
- `AG_Informatica_Medica`: ultimo commit `2026-02-18` posterior a `last_update` del registro (`2026-02-17`).
- `AG_Lists_Agent`: ultimo commit `2026-02-18` posterior a `last_update` del registro (`2026-02-17`).
- `AG_NB_Apps`: ultimo commit `2026-02-20` posterior a `last_update` del registro (`2026-02-17`).
- `AG_Notebook`: ultimo commit `2026-02-20` posterior a `last_update` del registro (`2026-02-17`).
- `AG_SD_Plantilla`: ultimo commit `2026-02-20` posterior a `last_update` del registro (`2026-02-17`).
- `AG_SV_Agent`: ultimo commit `2026-02-20` posterior a `last_update` del registro (`2026-02-17`).
- `AG_TrakCare_Explorer`: ultimo commit `2026-02-20` posterior a `last_update` del registro (`2026-02-17`).

## 4. Matriz consolidada por proyecto

| Proyecto | Categoria | Tipo | Grade | Salud | Req | Rec | Seg | Tests | CI | Git Dirty |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| AG_Analizador_RCE | hospital-personal | python | A | 100 | 7/7 | 7/7 | 0 | 0 | 3 | 41 |
| AG_Consultas | hospital-personal | python | A | 88 | 7/7 | 6/7 | 0 | 3 | 3 | 46 |
| AG_DeepResearch_Salud_Chile | proyectos | python | A | 88 | 7/7 | 7/7 | 0 | 170 | 20 | 1 |
| AG_Hospital | hospital-personal | documentation | A | 74 | 7/7 | 4/7 | 0 | 0 | 0 | 6 |
| AG_Hospital_Organizador | hospital-equipo | nocobase | A | 88 | 7/7 | 6/7 | 0 | 170 | 23 | 3421 |
| AG_Informatica_Medica | proyectos | documentation | A | 88 | 7/7 | 7/7 | 0 | 0 | 3 | 68 |
| AG_Lists_Agent | personales | python | A | 94 | 7/7 | 6/7 | 0 | 3 | 0 | 18 |
| AG_NB_Apps | hospital-equipo | nocobase | A | 88 | 7/7 | 6/7 | 0 | 4 | 3 | 65 |
| AG_Notebook | admin | documentation | A | 79 | 7/7 | 5/7 | 0 | 0 | 0 | 5 |
| AG_Orquesta_Desk | admin | python | A | 94 | 7/7 | 7/7 | 0 | 5 | 0 | 0 |
| AG_Plantilla | admin | template | A | 100 | 7/7 | 7/7 | 0 | 174 | 23 | 3 |
| AG_SD_Plantilla | privado | python | A | 74 | 7/7 | 4/7 | 0 | 0 | 0 | 5 |
| AG_SV_Agent | admin | infrastructure | A | 74 | 7/7 | 4/7 | 0 | 0 | 0 | 4 |
| AG_TrakCare_Explorer | hospital-personal | python | A | 100 | 7/7 | 6/7 | 0 | 0 | 3 | 17 |

## 5. Detalle completo por proyecto

### 5.1 AG_Analizador_RCE

- Ruta: `w:\Antigravity_OS\01_HOSPITAL_PRIVADO\AG_Analizador_RCE`
- Origen: Registro oficial
- Categoria/Tipo: `hospital-personal` / `python`
- Estado declarado: `active`
- Repositorio GitHub (registro): `ITATA93/AG_Analizador_RCE`
- Fechas (registro): creacion `2026-02-04` | ultimo update `2026-02-17`
- Existencia local: `SI`
- Grade/Health: `A` / `100`
- Cobertura requerida: `7/7`
- Cobertura recomendada: `7/7`
- Calidad de contenido: `100%`
- Autonomia agentica: `100%`
- Findings de seguridad: `0`
- Faltantes requeridos: ninguno
- Faltantes recomendados: ninguno
- Brechas calidad: `ninguna`
- Brechas autonomia: `ninguna`
- Git branch/head: `master` / `8822658`
- Ultimo commit: `2026-02-20T20:32:13-03:00`
- Mensaje ultimo commit: `chore: auto-fix missing files (.env.example, docs/standards/output_governance.md)`
- Upstream: `origin/master` | ahead `1` | behind `0`
- Arbol local: `41` cambios (`41` untracked)
- Conteo archivos: total `145` | markdown `52` | scripts `48`
- Evidencia QA: tests detectados `0` | workflows CI `3`
- Operacion diaria: tareas abiertas `0` | completadas `0` | referencias blocker `1`
- Actividad DEVLOG: sesiones detectadas `2`
- Riesgo sintetico: `git_dirty, sin_tests_detectados`

### 5.2 AG_Consultas

- Ruta: `w:\Antigravity_OS\01_HOSPITAL_PRIVADO\AG_Consultas`
- Origen: Registro oficial
- Categoria/Tipo: `hospital-personal` / `python`
- Estado declarado: `active`
- Repositorio GitHub (registro): `ITATA93/AG_Consultas`
- Fechas (registro): creacion `2026-02-04` | ultimo update `2026-02-17`
- Existencia local: `SI`
- Grade/Health: `A` / `88`
- Cobertura requerida: `7/7`
- Cobertura recomendada: `6/7`
- Calidad de contenido: `80%`
- Autonomia agentica: `83%`
- Findings de seguridad: `0`
- Faltantes requeridos: ninguno
- Faltantes recomendados: `config/`
- Brechas calidad: `gemini_keywords`
- Brechas autonomia: `tasks_awareness`
- Git branch/head: `main` / `fddb17cc`
- Ultimo commit: `2026-02-20T14:32:56-03:00`
- Mensaje ultimo commit: `feat(consultas): add pabellon protocolos quirurgicos query`
- Upstream: `origin/main` | ahead `0` | behind `0`
- Arbol local: `46` cambios (`34` untracked)
- Conteo archivos: total `23968` | markdown `23589` | scripts `143`
- Evidencia QA: tests detectados `3` | workflows CI `3`
- Operacion diaria: tareas abiertas `0` | completadas `0` | referencias blocker `0`
- Actividad DEVLOG: sesiones detectadas `3`
- Riesgo sintetico: `git_dirty`

### 5.3 AG_DeepResearch_Salud_Chile

- Ruta: `w:\Antigravity_OS\01_HOSPITAL_PRIVADO\AG_DeepResearch_Salud_Chile`
- Origen: Registro oficial
- Categoria/Tipo: `proyectos` / `python`
- Estado declarado: `active`
- Repositorio GitHub (registro): `ITATA93/AG_DeepResearch_Salud_Chile`
- Fechas (registro): creacion `2026-02-07` | ultimo update `2026-02-17`
- Existencia local: `SI`
- Grade/Health: `A` / `88`
- Cobertura requerida: `7/7`
- Cobertura recomendada: `7/7`
- Calidad de contenido: `80%`
- Autonomia agentica: `83%`
- Findings de seguridad: `0`
- Faltantes requeridos: ninguno
- Faltantes recomendados: ninguno
- Brechas calidad: `gemini_keywords`
- Brechas autonomia: `tasks_awareness`
- Git branch/head: `master` / `d6f182e`
- Ultimo commit: `2026-02-20T20:32:14-03:00`
- Mensaje ultimo commit: `chore: auto-fix missing files (AGENTS.md)`
- Upstream: `origin/master` | ahead `1` | behind `0`
- Arbol local: `1` cambios (`0` untracked)
- Conteo archivos: total `6956` | markdown `2706` | scripts `1897`
- Evidencia QA: tests detectados `170` | workflows CI `20`
- Operacion diaria: tareas abiertas `0` | completadas `0` | referencias blocker `0`
- Actividad DEVLOG: sesiones detectadas `4`
- Riesgo sintetico: `git_dirty`

### 5.4 AG_Hospital

- Ruta: `w:\Antigravity_OS\01_HOSPITAL_PRIVADO\AG_Hospital`
- Origen: Registro oficial
- Categoria/Tipo: `hospital-personal` / `documentation`
- Estado declarado: `active`
- Repositorio GitHub (registro): `ITATA93/AG_Hospital`
- Fechas (registro): creacion `2026-02-13` | ultimo update `2026-02-17`
- Existencia local: `SI`
- Grade/Health: `A` / `74`
- Cobertura requerida: `7/7`
- Cobertura recomendada: `4/7`
- Calidad de contenido: `100%`
- Autonomia agentica: `16%`
- Findings de seguridad: `0`
- Faltantes requeridos: ninguno
- Faltantes recomendados: `config/, .gemini/, .agent/`
- Brechas calidad: `ninguna`
- Brechas autonomia: `session_protocol, has_workflows, subagents_defined, dispatch_available, memory_structure`
- Git branch/head: `main` / `bc3e213`
- Ultimo commit: `2026-02-20T20:32:14-03:00`
- Mensaje ultimo commit: `chore: auto-fix missing files (CLAUDE.md, AGENTS.md, .env.example, docs/standards/output_governance.md)`
- Upstream: `origin/main` | ahead `1` | behind `0`
- Arbol local: `6` cambios (`6` untracked)
- Conteo archivos: total `14` | markdown `8` | scripts `0`
- Evidencia QA: tests detectados `0` | workflows CI `0`
- Operacion diaria: tareas abiertas `0` | completadas `0` | referencias blocker `1`
- Actividad DEVLOG: sesiones detectadas `2`
- Riesgo sintetico: `autonomia_baja, git_dirty, sin_ci_detectada`

### 5.5 AG_Hospital_Organizador

- Ruta: `w:\Antigravity_OS\01_HOSPITAL_PRIVADO\AG_Hospital_Organizador`
- Origen: Registro oficial
- Categoria/Tipo: `hospital-equipo` / `nocobase`
- Estado declarado: `active`
- Repositorio GitHub (registro): `ITATA93/AG_Hospital_Organizador`
- Fechas (registro): creacion `2026-02-02` | ultimo update `2026-02-17`
- Existencia local: `SI`
- Grade/Health: `A` / `88`
- Cobertura requerida: `7/7`
- Cobertura recomendada: `6/7`
- Calidad de contenido: `80%`
- Autonomia agentica: `83%`
- Findings de seguridad: `0`
- Faltantes requeridos: ninguno
- Faltantes recomendados: `config/`
- Brechas calidad: `gemini_keywords`
- Brechas autonomia: `tasks_awareness`
- Git branch/head: `master` / `fe802f4`
- Ultimo commit: `2026-02-18T13:44:08-03:00`
- Mensaje ultimo commit: `chore: cleanup pending items, archive UPDATE_TASKS.md, update TODO.md`
- Upstream: `origin/master` | ahead `0` | behind `0`
- Arbol local: `3421` cambios (`46` untracked)
- Conteo archivos: total `7026` | markdown `2727` | scripts `1932`
- Evidencia QA: tests detectados `170` | workflows CI `23`
- Operacion diaria: tareas abiertas `0` | completadas `0` | referencias blocker `0`
- Actividad DEVLOG: sesiones detectadas `5`
- Riesgo sintetico: `git_dirty`

### 5.6 AG_Informatica_Medica

- Ruta: `w:\Antigravity_OS\01_HOSPITAL_PRIVADO\AG_Informatica_Medica`
- Origen: Registro oficial
- Categoria/Tipo: `proyectos` / `documentation`
- Estado declarado: `active`
- Repositorio GitHub (registro): `ITATA93/AG_Informatica_Medica`
- Fechas (registro): creacion `2026-02-14` | ultimo update `2026-02-17`
- Existencia local: `SI`
- Grade/Health: `A` / `88`
- Cobertura requerida: `7/7`
- Cobertura recomendada: `7/7`
- Calidad de contenido: `80%`
- Autonomia agentica: `83%`
- Findings de seguridad: `0`
- Faltantes requeridos: ninguno
- Faltantes recomendados: ninguno
- Brechas calidad: `gemini_keywords`
- Brechas autonomia: `tasks_awareness`
- Git branch/head: `master` / `65da6cc`
- Ultimo commit: `2026-02-18T18:40:42-03:00`
- Mensaje ultimo commit: `feat(corpus): salud digital + gobierno digital Ã¢â‚¬â€ 4 fichas nuevas + 4 profundizadas (86Ã¢â€ â€™90)`
- Upstream: `origin/master` | ahead `0` | behind `0`
- Arbol local: `68` cambios (`58` untracked)
- Conteo archivos: total `354` | markdown `198` | scripts `38`
- Evidencia QA: tests detectados `0` | workflows CI `3`
- Operacion diaria: tareas abiertas `0` | completadas `0` | referencias blocker `0`
- Actividad DEVLOG: sesiones detectadas `3`
- Riesgo sintetico: `git_dirty`

### 5.7 AG_Lists_Agent

- Ruta: `w:\Antigravity_OS\01_HOSPITAL_PRIVADO\AG_Lists_Agent`
- Origen: Registro oficial
- Categoria/Tipo: `personales` / `python`
- Estado declarado: `active`
- Repositorio GitHub (registro): `ITATA93/AG_Lists_Agent`
- Fechas (registro): creacion `2026-02-13` | ultimo update `2026-02-17`
- Existencia local: `SI`
- Grade/Health: `A` / `94`
- Cobertura requerida: `7/7`
- Cobertura recomendada: `6/7`
- Calidad de contenido: `80%`
- Autonomia agentica: `100%`
- Findings de seguridad: `0`
- Faltantes requeridos: ninguno
- Faltantes recomendados: `config/`
- Brechas calidad: `changelog_active`
- Brechas autonomia: `ninguna`
- Git branch/head: `master` / `1de358c`
- Ultimo commit: `2026-02-18T10:30:55-03:00`
- Mensaje ultimo commit: `feat(tasks): incoming normalization tasks from AG_Plantilla`
- Upstream: `origin/master` | ahead `0` | behind `0`
- Arbol local: `18` cambios (`14` untracked)
- Conteo archivos: total `80` | markdown `31` | scripts `28`
- Evidencia QA: tests detectados `3` | workflows CI `0`
- Operacion diaria: tareas abiertas `0` | completadas `0` | referencias blocker `0`
- Actividad DEVLOG: sesiones detectadas `1`
- Riesgo sintetico: `git_dirty, sin_ci_detectada`

### 5.8 AG_NB_Apps

- Ruta: `w:\Antigravity_OS\02_HOSPITAL_PUBLICO\AG_NB_Apps`
- Origen: Registro oficial
- Categoria/Tipo: `hospital-equipo` / `nocobase`
- Estado declarado: `active`
- Repositorio GitHub (registro): `ITATA93/AG_NB_Apps`
- Fechas (registro): creacion `2026-02-04` | ultimo update `2026-02-17`
- Existencia local: `SI`
- Grade/Health: `A` / `88`
- Cobertura requerida: `7/7`
- Cobertura recomendada: `6/7`
- Calidad de contenido: `80%`
- Autonomia agentica: `83%`
- Findings de seguridad: `0`
- Faltantes requeridos: ninguno
- Faltantes recomendados: `config/`
- Brechas calidad: `gemini_keywords`
- Brechas autonomia: `tasks_awareness`
- Git branch/head: `master` / `47d23ca`
- Ultimo commit: `2026-02-20T14:33:01-03:00`
- Mensaje ultimo commit: `feat(nb-apps): add audit-entrega scripts and temp outputs`
- Upstream: `origin/master` | ahead `0` | behind `0`
- Arbol local: `65` cambios (`57` untracked)
- Conteo archivos: total `919` | markdown `252` | scripts `414`
- Evidencia QA: tests detectados `4` | workflows CI `3`
- Operacion diaria: tareas abiertas `0` | completadas `0` | referencias blocker `0`
- Actividad DEVLOG: sesiones detectadas `6`
- Riesgo sintetico: `git_dirty`

### 5.9 AG_Notebook

- Ruta: `w:\Antigravity_OS\00_CORE\AG_Notebook`
- Origen: Registro oficial
- Categoria/Tipo: `admin` / `documentation`
- Estado declarado: `active`
- Repositorio GitHub (registro): `ITATA93/AG_Notebook`
- Fechas (registro): creacion `2026-02-02` | ultimo update `2026-02-17`
- Existencia local: `SI`
- Grade/Health: `A` / `79`
- Cobertura requerida: `7/7`
- Cobertura recomendada: `5/7`
- Calidad de contenido: `100%`
- Autonomia agentica: `33%`
- Findings de seguridad: `0`
- Faltantes requeridos: ninguno
- Faltantes recomendados: `config/, .gemini/`
- Brechas calidad: `ninguna`
- Brechas autonomia: `session_protocol, subagents_defined, dispatch_available, memory_structure`
- Git branch/head: `main` / `f352810`
- Ultimo commit: `2026-02-20T20:32:13-03:00`
- Mensaje ultimo commit: `chore: auto-fix missing files (CLAUDE.md, AGENTS.md, docs/standards/output_governance.md)`
- Upstream: `origin/main` | ahead `1` | behind `0`
- Arbol local: `5` cambios (`4` untracked)
- Conteo archivos: total `143` | markdown `58` | scripts `50`
- Evidencia QA: tests detectados `0` | workflows CI `0`
- Operacion diaria: tareas abiertas `0` | completadas `0` | referencias blocker `1`
- Actividad DEVLOG: sesiones detectadas `2`
- Riesgo sintetico: `autonomia_baja, git_dirty, sin_ci_detectada`

### 5.10 AG_Orquesta_Desk

- Ruta: `w:\Antigravity_OS\00_CORE\AG_Orquesta_Desk`
- Origen: Detectado en escaneo del ecosistema
- Categoria/Tipo: `admin` / `python`
- Estado declarado: `active`
- Repositorio GitHub (registro): `ITATA93/AG_Orquesta_Desk`
- Fechas (registro): creacion `2026-02-20` | ultimo update `2026-02-20`
- Existencia local: `SI`
- Grade/Health: `A` / `94`
- Cobertura requerida: `7/7`
- Cobertura recomendada: `7/7`
- Calidad de contenido: `80%`
- Autonomia agentica: `100%`
- Findings de seguridad: `0`
- Faltantes requeridos: ninguno
- Faltantes recomendados: ninguno
- Brechas calidad: `gemini_keywords`
- Brechas autonomia: `ninguna`
- Git branch/head: `master` / `b17d855`
- Ultimo commit: `2026-02-20T22:58:00-03:00`
- Mensaje ultimo commit: `fix(audit): apply high and medium priority normalization fixes`
- Upstream: `n/a` | ahead `n/a` | behind `n/a`
- Arbol local: `0` cambios (`0` untracked)
- Conteo archivos: total `260` | markdown `151` | scripts `55`
- Evidencia QA: tests detectados `5` | workflows CI `0`
- Operacion diaria: tareas abiertas `0` | completadas `0` | referencias blocker `1`
- Actividad DEVLOG: sesiones detectadas `15`
- Riesgo sintetico: `sin_ci_detectada`

### 5.11 AG_Plantilla

- Ruta: `w:\Antigravity_OS\00_CORE\AG_Plantilla`
- Origen: Registro oficial
- Categoria/Tipo: `admin` / `template`
- Estado declarado: `active`
- Repositorio GitHub (registro): `ITATA93/AG_Plantilla`
- Fechas (registro): creacion `2026-02-02` | ultimo update `2026-02-20`
- Existencia local: `SI`
- Grade/Health: `A` / `100`
- Cobertura requerida: `7/7`
- Cobertura recomendada: `7/7`
- Calidad de contenido: `100%`
- Autonomia agentica: `100%`
- Findings de seguridad: `0`
- Faltantes requeridos: ninguno
- Faltantes recomendados: ninguno
- Brechas calidad: `ninguna`
- Brechas autonomia: `ninguna`
- Git branch/head: `master` / `72782da`
- Ultimo commit: `2026-02-20T20:59:15-03:00`
- Mensaje ultimo commit: `fix(agents): add CODEX_WORKSPACE_ROOT to allow execution across ecosystem domains`
- Upstream: `origin/master` | ahead `7` | behind `0`
- Arbol local: `3` cambios (`3` untracked)
- Conteo archivos: total `7422` | markdown `3020` | scripts `1984`
- Evidencia QA: tests detectados `174` | workflows CI `23`
- Operacion diaria: tareas abiertas `1` | completadas `16` | referencias blocker `1`
- Actividad DEVLOG: sesiones detectadas `15`
- Riesgo sintetico: `git_dirty`

### 5.12 AG_SD_Plantilla

- Ruta: `w:\Antigravity_OS\02_HOSPITAL_PUBLICO\AG_SD_Plantilla`
- Origen: Registro oficial
- Categoria/Tipo: `privado` / `python`
- Estado declarado: `active`
- Repositorio GitHub (registro): `ITATA93/AG_SD_Plantilla`
- Fechas (registro): creacion `2026-02-05` | ultimo update `2026-02-17`
- Existencia local: `SI`
- Grade/Health: `A` / `74`
- Cobertura requerida: `7/7`
- Cobertura recomendada: `4/7`
- Calidad de contenido: `100%`
- Autonomia agentica: `16%`
- Findings de seguridad: `0`
- Faltantes requeridos: ninguno
- Faltantes recomendados: `config/, .gemini/, .agent/`
- Brechas calidad: `ninguna`
- Brechas autonomia: `session_protocol, has_workflows, subagents_defined, dispatch_available, memory_structure`
- Git branch/head: `main` / `64d984b`
- Ultimo commit: `2026-02-20T20:32:14-03:00`
- Mensaje ultimo commit: `chore: auto-fix missing files (CLAUDE.md, AGENTS.md, docs/standards/output_governance.md)`
- Upstream: `origin/main` | ahead `1` | behind `0`
- Arbol local: `5` cambios (`5` untracked)
- Conteo archivos: total `76` | markdown `10` | scripts `35`
- Evidencia QA: tests detectados `0` | workflows CI `0`
- Operacion diaria: tareas abiertas `0` | completadas `0` | referencias blocker `1`
- Actividad DEVLOG: sesiones detectadas `2`
- Riesgo sintetico: `autonomia_baja, git_dirty, sin_tests_detectados, sin_ci_detectada`

### 5.13 AG_SV_Agent

- Ruta: `w:\Antigravity_OS\00_CORE\AG_SV_Agent`
- Origen: Registro oficial
- Categoria/Tipo: `admin` / `infrastructure`
- Estado declarado: `active`
- Repositorio GitHub (registro): `ITATA93/AG_SV_Agent`
- Fechas (registro): creacion `2026-02-04` | ultimo update `2026-02-17`
- Existencia local: `SI`
- Grade/Health: `A` / `74`
- Cobertura requerida: `7/7`
- Cobertura recomendada: `4/7`
- Calidad de contenido: `100%`
- Autonomia agentica: `16%`
- Findings de seguridad: `0`
- Faltantes requeridos: ninguno
- Faltantes recomendados: `config/, .gemini/, .agent/`
- Brechas calidad: `ninguna`
- Brechas autonomia: `session_protocol, has_workflows, subagents_defined, dispatch_available, memory_structure`
- Git branch/head: `main` / `668e06b`
- Ultimo commit: `2026-02-20T20:32:13-03:00`
- Mensaje ultimo commit: `chore: auto-fix missing files (CLAUDE.md, AGENTS.md, docs/standards/output_governance.md)`
- Upstream: `origin/main` | ahead `1` | behind `0`
- Arbol local: `4` cambios (`4` untracked)
- Conteo archivos: total `41` | markdown `14` | scripts `14`
- Evidencia QA: tests detectados `0` | workflows CI `0`
- Operacion diaria: tareas abiertas `0` | completadas `0` | referencias blocker `1`
- Actividad DEVLOG: sesiones detectadas `2`
- Riesgo sintetico: `autonomia_baja, git_dirty, sin_tests_detectados, sin_ci_detectada`

### 5.14 AG_TrakCare_Explorer

- Ruta: `w:\Antigravity_OS\01_HOSPITAL_PRIVADO\AG_TrakCare_Explorer`
- Origen: Registro oficial
- Categoria/Tipo: `hospital-personal` / `python`
- Estado declarado: `active`
- Repositorio GitHub (registro): `ITATA93/AG_TrakCare_Explorer`
- Fechas (registro): creacion `2026-02-17` | ultimo update `2026-02-17`
- Existencia local: `SI`
- Grade/Health: `A` / `100`
- Cobertura requerida: `7/7`
- Cobertura recomendada: `6/7`
- Calidad de contenido: `100%`
- Autonomia agentica: `100%`
- Findings de seguridad: `0`
- Faltantes requeridos: ninguno
- Faltantes recomendados: `config/`
- Brechas calidad: `ninguna`
- Brechas autonomia: `ninguna`
- Git branch/head: `main` / `7d01fdb`
- Ultimo commit: `2026-02-20T20:32:14-03:00`
- Mensaje ultimo commit: `chore: auto-fix missing files (.env.example)`
- Upstream: `origin/main` | ahead `1` | behind `0`
- Arbol local: `17` cambios (`17` untracked)
- Conteo archivos: total `3231` | markdown `69` | scripts `71`
- Evidencia QA: tests detectados `0` | workflows CI `3`
- Operacion diaria: tareas abiertas `0` | completadas `0` | referencias blocker `1`
- Actividad DEVLOG: sesiones detectadas `2`
- Riesgo sintetico: `git_dirty, sin_tests_detectados`

## 6. Plan de remediacion recomendado

1. Normalizar autonomia en proyectos manuales (`AG_Hospital`, `AG_SV_Agent`, `AG_SD_Plantilla`, `AG_Notebook`) creando `.agent/rules`, `.agent/workflows` y `.subagents/manifest.json` minimo viable.
2. Corregir brechas de `gemini_keywords` y `tasks_awareness` para mejorar adherencia de agentes a protocolos operativos.
3. Definir baseline de QA por proyecto (al menos 1 workflow CI y suite minima de tests donde aplique).
4. Establecer rutina de higiene Git diaria en repos con arbol sucio para reducir drift y riesgo de perdida de contexto.
5. Actualizar `project_registry.json` cuando la fecha real de commit sea posterior a `last_update` para preservar trazabilidad operativa.

## 7. Anexos

- Fuente principal de inventario: `config/project_registry.json`
- Scripts usados: `scripts/audit_ecosystem.py`, `scripts/ecosystem_dashboard.py`
- Nota: este informe es una auditoria estatica de estado actual (filesystem + git + estructura). No ejecuta pruebas funcionales o de integracion de cada proyecto en runtime.

