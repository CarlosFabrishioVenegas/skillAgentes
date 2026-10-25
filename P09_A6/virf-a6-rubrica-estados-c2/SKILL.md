---
name: virf-a6-rubrica-estados-c2
description: Rúbrica de decisión del Control 2 Calidad de Datos - verificación de integridad del insumo de A3, mapeo actividad VIRF a dimensión, reglas duras para Cumple, Cumple con observación, No cumple, No verificable y No evidenciado, casos borde (base depurada, umbral a posteriori, circularidad, proveedor externo, reprocesos) y formato de la tabla por actividad VIRF. Úsala en el Paso 9 (agente A6) para emitir el estado de cada actividad.
---

# A6 · Rúbrica de estados del Control 2

## 0. Antes de juzgar: integridad del insumo de A3

Checklist (si falla algo, devolver a A3D/A3E antes de continuar):
- [ ] Las nueve dimensiones están presentes en la matriz de 8 columnas (o su ausencia está justificada).
- [ ] Cada diagnóstico contiene cifra.
- [ ] Cada referencia es verificable (archivo > hoja > fila / celda del notebook).
- [ ] Conteos reconciliados (sin "DESCUADRE").

## 1. Árbol de decisión por actividad VIRF

```
¿Hay dimensión de A3 que evidencie la actividad?
 └─ No → NO EVIDENCIADO (acción: entregar insumo)
¿La medición es válida? (base no depurada, umbral declarado antes del resultado, población = la del modelo)
 └─ No → NO VERIFICABLE
¿Existe el MARCO del control? (definido · documentado · con umbral · con responsable · con periodicidad ejecutada)
 └─ No → NO CUMPLE (aunque los datos estén perfectos)
¿Resultado fuera de umbral en variable USADA por el modelo?
 └─ Sí → NO CUMPLE
¿Debilidad de proceso (sin revisión independiente, sin alerta, sin acuse) o defecto en variable NO usada?
 └─ Sí → CUMPLE CON OBSERVACIÓN
└─ CUMPLE
```

Reglas duras:
- Una dimensión "No cumple" sobre variable usada **impide** "Cumple" en las actividades que la usan.
- Una dimensión "No evidenciado" impide "Cumple" y produce, como mínimo, "Cumple con observación" con acción de entrega cuando el resto de la actividad está evidenciado; si la actividad depende solo de esa dimensión, queda "No evidenciado".
- En Tier 1 y 2, ausencia de linaje = hallazgo **crítico**.

## 2. Casos borde (tabla de decisión rápida)

| Caso | Estado | Nota |
|---|---|---|
| Base entregada ya depurada | No verificable | Exigir base previa |
| Umbral declarado después del resultado | Hallazgo de gobierno del dato | Documentar fecha de declaración |
| Control ejecutado por el propio equipo sin revisión independiente | Cumple con observación (Tier 1) | Observación de independencia |
| Nulos altos en variable NO usada | Cumple con observación | Explicar por qué no afecta el output |
| Datos de proveedor externo sin acuerdo de calidad | No cumple (hallazgo) | Control no exigible ni monitoreable |
| Reproceso histórico que cambia datos ya validados | Hallazgo de trazabilidad | Pedir política y registro de reprocesos |
| Conteo del notebook ≠ reporte del equipo | No verificable | Documentar ambos; reconciliación formal |
| Control automatizado sin alerta ni destinatario | Cumple con observación | "Existe y no gobierna nada": efectividad |
| Umbral cumplido por construcción (se eliminan infractores) | No cumple — crítico | Circularidad del control |
| Equipo corrige la base durante la validación | Estado original + "remediado en el ciclo" con fecha | El hallazgo no se borra |

## 3. Formato de salida (a)

```markdown
| ID VIRF | Actividad | Dimensión que la evidencia | Estado | Resultado (cifra) | Evaluación sustentada | Fuente exacta | Acción pendiente |
|---|---|---|---|---|---|---|---|
```

Fuente exacta con **tres orígenes** cuando existan: celda del catálogo donde se declara el control · celda del notebook donde se midió · archivo y columna del dataset.

Anexo (b): matriz de 8 columnas de A3 **sin modificar**. (c) Hallazgos críticos con impacto sobre el output (ver skill de conexión defecto→output).

## Interacción

- "Las cifras se ven bien, cierra el control" → responder con las dimensiones aún en "No evidenciado" y el efecto de cerrarlas sin evidencia.
- No convertir la matriz en puntaje agregado. No trasladar a Metodología hallazgos que son de datos.
