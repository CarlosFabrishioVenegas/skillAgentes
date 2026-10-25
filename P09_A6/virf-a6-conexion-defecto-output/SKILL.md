---
name: virf-a6-conexion-defecto-output
description: Método para conectar cada defecto de calidad de datos con el output del modelo respondiendo tres preguntas (qué variable se afecta, qué peso tiene en el modelo, en qué dirección y magnitud se mueve el output), priorización por materialidad y redacción de evaluaciones sustentadas con cifra, usando los resultados de A3E y AIM. Úsala en el Paso 9 (A6) para la sección de hallazgos críticos y la columna Evaluación sustentada.
---

# A6 · Del defecto de dato al riesgo de modelo

Sin esta conexión, el hallazgo describe un problema de base de datos, no un riesgo de modelo.

## Las tres preguntas (obligatorias por hallazgo)

| Pregunta | Dónde encontrar la respuesta |
|---|---|
| 1. ¿Qué variable se afecta y cuántos registros/qué exposición? | A3_informe_calidad_datos.md (hallazgo) · perfil de infractores |
| 2. ¿Qué peso tiene la variable en el modelo? | Manual metodológico (importancia, coeficiente, WoE/IV) · código (`coef_`, tabla de puntajes) · A4_paso0.md > 5 |
| 3. ¿Dirección y magnitud del movimiento del output? | 03_Impactos.xlsx (AIM) · si no hay, estimación declarada como no disponible |

Si el peso **no está documentado**: además del hallazgo de datos, referencia cruzada a Metodología (A7) "peso de variable no documentado". No lo trasladas: lo referencias.

Si la magnitud no es estimable: dilo y explica por qué ("no hay valor real para los nulos imputados ni escenario de AIM").

## Peso de la variable cuando solo tienes el modelo

- Regresión logística/lineal: contribución estandarizada = |coef × desv. estándar de la variable| / Σ|coef × desv.|.
- Scorecard: rango de puntos de la variable / rango total de puntos.
- Árboles/boosting: importancia por ganancia o SHAP medio (solo si el equipo lo entregó o lo reproduce A7).

Cita el método usado; si el cálculo es tuyo, decláralo.

## Priorización

Un defecto en la variable de mayor peso supera a diez defectos en variables informativas. Ordena los hallazgos críticos por: (1) afecta target/llave/filtro de población, (2) peso de la variable × % exposición afectada, (3) Δ monetario de AIM.

## Plantilla de evaluación sustentada

> "`<variable>` concentra el `<peso>` del score y presenta `<% y n>` de `<defecto>` `<tratamiento actual>`; `<efecto en output con cifra>` (`<fuente AIM o cálculo>`), por lo que el defecto es material para el output y no solo para la base."

Ejemplos:
- ✔ "`ingreso_declarado` concentra el 22 % del peso del score y presenta 7,4 % de nulos imputados por mediana sin regla documentada; la imputación desplaza la media del score en +4 puntos y reclasifica 318 clientes de segmento (03_Impactos.xlsx > Resumen > IMP-02), por lo que el defecto es material para el output."
- ✔ "`telefono_secundario` tiene 31 % de nulos, pero no es variable del modelo ni filtro (A4_paso0.md > 4): Cumple con observación; no afecta el output."
- ✘ "La calidad de los datos es adecuada en general." (sin cifra, adjetivo prohibido)

## Hallazgos críticos (salida c)

```markdown
| # | Hallazgo | Variable | Peso | Afectación | Δ output (AIM) | Estado | Severidad | Fuente |
|---|---|---|---|---|---|---|---|---|
```
