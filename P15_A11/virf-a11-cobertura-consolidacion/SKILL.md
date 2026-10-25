---
name: virf-a11-cobertura-consolidacion
description: Consolidación de las matrices de los seis controles (A5 a A10) y la matriz de A3 - control de cobertura contra las actividades VIRF aplicables al tier, normalización al semáforo oficial, clasificación cuantitativo o cualitativo, deduplicación con referencia cruzada, detección de filas sin cita, inconsistencias entre controles y No aplica sin regla, con script que lee las tablas Markdown de cada control. Úsala en el Paso 15 (agente A11) antes de redactar la conclusión.
---

# A11 · Cobertura y consolidación

A11 no revalida: **integra**. Si un control llega incompleto se devuelve a su agente; completarlo aquí destruiría la trazabilidad.

## 1. Ejecutar la consolidación

```bash
python scripts/consolidar_controles.py --actividades actividades_tier.csv \
    --controles A5_control_documentacion.md A6_control_datos.md A7_control_metodologia.md \
                A8_control_implementacion.md A9_control_gobierno.md A10_control_usos.md \
    --salida consolidado.csv --reporte consolidacion.md
```

- `actividades_tier.csv`: salida de `filtrar_estandar_virf.py` (lista oficial de actividades aplicables).
- El script extrae de cada .md la tabla que tiene columna "ID VIRF"; si no la encuentra, toma la matriz por su encabezado ("Campo del acta", "Output", "Bloque de código") y **devuelve** la matriz al agente pidiendo la columna ID VIRF.
- La cobertura se mide por actividad del estándar (con el control de la actividad), no por filas: una referencia cruzada en otro control no duplica cobertura.

Reporta:
1. **Cobertura** por control y global (actividades con fila / aplicables). Actividad sin fila → se agrega como "No evidenciado" con el agente responsable.
2. **Estados no oficiales** (p. ej. "Parcial", "OK", porcentajes) → señalados para devolver.
3. **Filas sin fuente exacta** → devolver al agente (no incorporar con "sin fuente").
4. **"No aplica" sin cita de regla** → reclasificado a "No evidenciado" y devuelto.
5. **Duplicados** (misma actividad o mismo hecho en dos controles) → conservar en el control de origen; referencia cruzada en el otro.
6. **Inconsistencias** (mismo ID con estados distintos en dos controles) → "Inconsistencia entre controles", hallazgo de proceso.
7. **Versiones de evidencia** distintas citadas por los controles (mismo archivo con hash distinto) → inconsistencia de proceso.

## 2. Semáforo oficial (único admitido)

Cumple · Cumple con observación · No cumple · No evidenciado · No verificable · No aplica. Sin intermedios, sin porcentajes por actividad.

## 3. Cuantitativo vs cualitativo

| Tipo | El juicio se sostiene en… |
|---|---|
| Cuantitativo | cifra, métrica o umbral |
| Cualitativo | existencia, coherencia o suficiencia documental |

El script lo sugiere (si la columna Resultado contiene números/%, cuantitativo); confírmalo. Todo cuantitativo debe tener su prueba en la HOJA 3: sin prueba, no puede cerrarse como Cumple.

## 4. Severidad

| Severidad | Criterio |
|---|---|
| Crítica | Impide concluir o afecta el output publicado |
| Alta | Afecta la confiabilidad del modelo |
| Media | Afecta la auditabilidad |
| Baja | Formal |

Orden: por ámbito (C1…C6) y, dentro, por severidad.

## 5. Casos borde

| Caso | Tratamiento |
|---|---|
| Hallazgo crítico remediado en el ciclo | Fila "No cumple — remediado en el ciclo" + evidencia y fecha; nunca convertir en Cumple |
| Equipo pide ajustar redacción | Se pueden precisar hechos con evidencia nueva citada; **no** suavizar el estado |
| Observación del ciclo anterior vencida por más de un ciclo | A11 genera hallazgo de gobierno adicional si nadie lo levantó |
| Hallazgo crítico cuya remediación depende de otra área | Conservar severidad; registrar dependencia en el plan de acción |
| Informe firmado tras el cierre contable | Registrar fecha de corte de la evidencia |
