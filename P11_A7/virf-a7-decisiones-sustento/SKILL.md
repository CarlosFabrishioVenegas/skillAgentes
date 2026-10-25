---
name: virf-a7-decisiones-sustento
description: Inventario de decisiones metodológicas de un modelo de riesgo (técnica, variable objetivo, ventana, extremos y faltantes, segmentación, selección de variables, calibración, corte, sesgos, estabilidad), clasificación de su sustento (paper entregado, norma con artículo, práctica interna, prueba empírica, criterio experto con o sin acta), evaluación de pertinencia y rúbrica de suficiencia, con la regla de doble plano de cita. Úsala en el Paso 11 (agente A7).
---

# A7 · Decisiones metodológicas y suficiencia del sustento

A7 evalúa dos cosas **en filas distintas**: (1) suficiencia del sustento de cada decisión; (2) ejecución de las actividades/pruebas del estándar. Este skill cubre (1).

## 1. Inventario de decisiones (mínimo)

| # | Decisión | Dónde buscarla |
|---|---|---|
| D1 | Técnica de modelado (logit, scorecard, GBM, Merton, simulación histórica, Monte Carlo…) | Manual metodológico cap. modelo; código |
| D2 | Definición de la variable objetivo (default, evento) | Manual; código del target |
| D3 | Ventana de observación y de desempeño | Manual; código |
| D4 | Tratamiento de extremos y faltantes | Manual; código (`clip`, `fillna`) |
| D5 | Criterio de segmentación | Manual; código |
| D6 | Selección de variables (IV, correlación, VIF, stepwise, juicio) | Manual; anexos |
| D7 | Método de calibración (tasa central, escalamiento, Bayes, isotónica) | Manual; código |
| D8 | Criterio de corte / umbral de decisión | Manual; acta |
| D9 | Tratamiento de sesgos (selección, supervivencia, rechazados) | Manual |
| D10 | Supuestos de estabilidad (población, macro) | Manual; supuestos literales del Paso 0 |
| D11 | Overlays / ajustes discrecionales | Manual; actas |
| D12 | Escenarios macro / forward looking (si aplica) | Manual; acta del foro que los aprueba |

Por tipo de modelo agrega: VaR (método, nivel de confianza, horizonte, ventana, escalamiento √t), IRRBB (escenarios de shock, supuestos conductuales de depósitos y prepago), LaR (percentil, factores de salida), Operacional (distribuciones de frecuencia/severidad, umbral de captura).

## 2. Clasificación del sustento

| Tipo | Válido si… | Si no |
|---|---|---|
| Paper académico | Está **en la carpeta papers/** del expediente | Citado y no entregado → No verificable (la disponibilidad pública no sustituye su incorporación) |
| Norma regulatoria | Cita norma + artículo | Sin artículo → Parcialmente suficiente |
| Práctica interna documentada | Política/manual vigente con sección | — |
| Prueba empírica propia | Resultado reproducible (script + datos) | No reproducible → No verificable |
| Criterio experto | **Acta/minuta del foro** con fecha y participantes | Sin acta → No evidenciado / Insuficiente |

## 3. Pertinencia (no solo existencia)

El sustento debe corresponder a: **la técnica implementada** (no a una variante), **el tipo de cartera** (retail ≠ corporativa), **el horizonte** usado. Un paper de calibración de PD corporativa no sustenta una calibración retail sin justificar explícitamente la analogía.

## 4. Rúbrica de suficiencia

| Nivel | Criterio |
|---|---|
| Suficiente | Respaldo pertinente y verificable, aplicado con los mismos parámetros, población y ventana implementados |
| Parcialmente suficiente | Respaldo existe pero aplicado con parámetros, población o ventana distintos |
| Insuficiente | Solo criterio experto sin acta, o respaldo no pertinente |
| No verificable | Respaldo citado no entregado, o métrica no reproducible |

## 5. Regla de doble plano

Toda decisión se cita en dos planos: **dónde se declara** (manual > sección > p.N) y **dónde se sustenta** (paper > p.N, o resultados > hoja > celda). Sin cualquiera de los dos → no puede ser "Cumple".

## 6. Supuestos y su prueba (bloque b)

```markdown
| Supuesto (literal, del Paso 0) | Prueba o monitoreo asociado | Resultado | Fuente | Estado |
|---|---|---|---|---|
| "La estructura de la cartera se mantiene estable en 12 meses" | PSI de población trimestral | PSI 0,04 (2026Q2) | Seguimiento_Q2.xlsx > PSI > C8 | Probado |
| "La LGD no depende del ciclo" | — | — | — | Supuesto sin prueba → hallazgo |
```

Un supuesto declarado y nunca probado es hallazgo, aunque sea razonable.

## 7. Formato de la matriz principal

```markdown
| ID VIRF | Decisión o actividad metodológica | Sustento presentado | ¿Suficiente? | Evaluación sustentada | Fuente exacta | Acción pendiente |
```

Bloque (c) recomendaciones bibliográficas: **separado y marcado "no computable como sustento"**. Nunca mezclar con el sustento acreditado.

Interacción: "es estándar de la industria" → el estándar de la industria no es evidencia del expediente; solicitar sustento interno.
