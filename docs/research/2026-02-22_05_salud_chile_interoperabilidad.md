# Deep Research R-05: Marco Regulatorio Chile e Interoperabilidad en Salud

- Fecha: 2026-02-22
- Objetivo: consolidar normativa y estandares tecnicos relevantes para actualizar sistemas de salud del ecosistema

## 1) Leyes y marcos normativos clave

## 1.1 Ley 21.180 (Transformacion Digital del Estado)

Hallazgo:

- Publicada el 2019-11-11 en BCN.

Implicacion:

- refuerza exigencia de procesos y tramites digitalizados, trazables y con estandares de interoperabilidad en sector publico.

## 1.2 Ley 21.663 (Marco de Ciberseguridad)

Hallazgo:

- Publicada el 2024-03-26.

Implicacion:

- obliga fortalecer gobierno de riesgos ciber, controles de seguridad y capacidad de respuesta ante incidentes en organizaciones sujetas.

## 1.3 Ley 21.668 (Interoperabilidad de fichas clinicas)

Hallazgo:

- Publicada el 2024-05-28.
- modifica Ley 20.584 para reforzar interoperabilidad de fichas clinicas.

Implicacion:

- proyectos que gestionan datos clinicos (consultas, trazabilidad, apps hospitalarias) deben alinearse a intercambio e integracion interoperable de informacion.

## 2) Estandares MINSAL de interoperabilidad

Hallazgos:

1. Existe arquitectura de estandares para interoperabilidad en salud digital desde MINSAL.
2. El marco explicita uso de estandares y su mantenimiento/revision periodica.
3. Se publica guia FHIR para CDA en portal oficial de interoperabilidad.
4. Se registran actividades de ecosystem alignment (ej. Connectathon Chile FHIR 2025).

Implicacion:

- no basta cumplir leyes a nivel documental; se requiere plan tecnico de adopcion de estandares (perfilado FHIR, mapeos semanticos, trazabilidad de versiones).

## 3) Riesgos de no alineacion en el ecosistema

1. Riesgo legal: incumplimiento regulatorio por falta de interoperabilidad demostrable.
2. Riesgo tecnico: integraciones heterogeneas sin contrato semantico estandar.
3. Riesgo operativo: duplicidad de datos y flujos manuales en clinica/gestion.

## 4) Recomendaciones de implementacion (tecnico-legal)

## Fase A (0-30 dias)

1. Crear matriz normativa por proyecto:
- ley aplicable
- tipo de dato
- control tecnico requerido
2. Definir data classification clinica/no clinica por app.
3. Establecer policy minima de seguridad para agentes que tocan datos de salud.

## Fase B (30-60 dias)

1. Levantar mapa de interoperabilidad:
- origen de datos
- transformaciones
- destino
- trazabilidad
2. Seleccionar perfiles FHIR minimos para pilotos de intercambio.
3. Incorporar controles de auditoria y logging alineados a marco legal.

## Fase C (60-90 dias)

1. Ejecutar piloto interoperable en 1-2 flujos de alto impacto.
2. Medir latencia, calidad y completitud del intercambio.
3. Emitir informe de cumplimiento tecnico-regulatorio trimestral.

## 5) Checklist minimo por proyecto de salud

1. Inventario de datos sensibles.
2. Politica de acceso por rol.
3. Registro de intercambio interoperable.
4. Politica de retencion y trazabilidad.
5. Evidencia auditable de controles de seguridad.

## 6) Fuentes primarias

- Ley 21.180 (historia y publicacion): https://www.bcn.cl/historiadelaley/nc/historia-de-la-ley/7680/
- Ley 21.663 (historia y publicacion): https://www.bcn.cl/historiadelaley/nc/historia-de-la-ley/16518/
- Ley 21.668 (historia y publicacion): https://www.bcn.cl/historiadelaley/nc/historia-de-la-ley/16784/
- Ley 21.668 en LeyChile (idNorma 1203827): https://www.bcn.cl/leychile/navegar?idNorma=1203827
- Arquitectura de estandares MINSAL: https://interoperabilidad.minsal.cl/fhir/ig/estandares-minsal/ArchitectureIndex.html
- Guia CDA/FHIR MINSAL: https://interoperabilidad.minsal.cl/FHIR/ig/guiacda/index.html
- Connectathon Chile FHIR 2025 (MINSAL): https://interoperabilidad.minsal.cl/FHIR/ig/guiacda/index.html

