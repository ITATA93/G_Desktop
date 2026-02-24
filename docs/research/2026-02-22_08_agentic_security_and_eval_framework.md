# Deep Research R-08: Seguridad y Evaluacion para Sistemas Agenticos

- Fecha: 2026-02-22
- Objetivo: convertir buenas practicas de seguridad/evaluacion en controles aplicables al ecosistema Antigravity

## 1) Baselines externos relevantes

## 1.1 OWASP Top 10 for LLM Applications

Aporta taxonomy practica de riesgos en apps con LLM:

- prompt injection
- sensitive information disclosure
- supply chain
- excessive agency
- overreliance

Uso recomendado en Antigravity:

- como lista minima de amenazas en diseño y auditoria de agentes.

## 1.2 NIST AI RMF 1.0

Aporta marco de gestion de riesgo de IA:

- Govern
- Map
- Measure
- Manage

Uso recomendado en Antigravity:

- mapear controles tecnicos de agentes a funciones RMF y medir madurez por proyecto.

## 1.3 NIST AI RMF - Generative AI Profile

Aporta perfil especifico para sistemas GenAI:

- controles de seguridad
- controles de calidad de output
- evaluacion continua de riesgo y desempeño

Uso recomendado en Antigravity:

- extender auditoria actual para incluir riesgo de alucinacion, uso incorrecto de herramientas y seguridad de prompts.

## 2) Matriz de controles propuesta (aplicable ya)

| Riesgo | Control tecnico | Donde implementarlo |
|---|---|---|
| Prompt injection | delimitadores + sanitizacion + classification pre-tool | `.subagents/dispatch.*` |
| Exfiltracion por herramientas | allowlist de dominios y paths | config MCP + wrappers de tools |
| Errores en ejecucion autonoma | aprobaciones por tipo de accion | policy de dispatch/vendor |
| Drift de comportamiento | pinning de versiones + smoke tests | `config/` + CI |
| Sobreconfianza en output | human-in-the-loop para acciones criticas | workflows de auditoria/deploy |

## 3) Gaps actuales frente a esta matriz

Hallazgos del baseline local:

1. El scanner de credenciales falla un test clave.
2. Existe mismatch de schema en dispatcher Linux.
3. Varios comandos fallan por encoding en Windows.
4. Hay drift de plantilla significativo.

Interpretacion:

- el ecosistema ya tiene controles buenos, pero la confiabilidad operacional no es uniforme; ese es el riesgo dominante actual.

## 4) Framework minimo de evaluacion continua (propuesto)

## 4.1 Indicadores de seguridad

1. Secret detection pass rate.
2. Numero de paquetes MCP deprecados en uso.
3. Tasa de ejecuciones con fallback forzado.

## 4.2 Indicadores de calidad agentica

1. Tool usage accuracy (invocaciones exitosas / invocaciones totales).
2. Task completion without human correction.
3. Regression rate despues de upgrade CLI/MCP.

## 4.3 Indicadores de gobernanza

1. Cumplimiento output governance por repo.
2. Drift de template por ciclo.
3. Cobertura de documentos requeridos de operacion.

## 5) Plan de implementacion de evals

## Etapa 1 (0-14 dias)

1. Formalizar benchmark de scripts core.
2. Agregar job de compatibilidad CLI/MCP por entorno.
3. Activar reporte semanal automatizado.

## Etapa 2 (14-45 dias)

1. Incluir pruebas de ataques de prompt injection en dispatch.
2. Medir tasa de falsos positivos/negativos del scanner de credenciales.
3. Implementar scoring compuesto por proyecto.

## Etapa 3 (45-90 dias)

1. Publicar dashboard de riesgo agentico por dominio.
2. Integrar decisiones de remediacion en TASKS cross-project.
3. Auditar trimestralmente contra NIST RMF + OWASP LLM Top 10.

## 6) Fuentes primarias

- OWASP LLM Top 10 Project: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- OWASP LLM prompt injection risk category: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- NIST AI RMF 1.0: https://www.nist.gov/itl/ai-risk-management-framework
- NIST Generative AI Profile: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence

