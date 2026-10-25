---
name: virf-aim-supuestos-sensibilidad
description: Registro y control de supuestos del análisis de impactos (tasas, factores, horizontes, tipo de cambio, tasa impositiva) con fuente o rótulo SUPUESTO, verificación de que el material de impactos del equipo corre y reconcilia antes de reutilizarlo, diseño de rangos de sensibilidad bajo-central-alto y redacción de la sección de resultados sin juicio de cumplimiento. Úsala en el Paso 8 (AIM) antes de publicar cifras.
---

# AIM · Supuestos, reutilización y sensibilidad

## 1. Registro de supuestos (obligatorio para cada número que no sale de la base)

| Supuesto | Valor | Fuente | ¿[SUPUESTO]? | Usado en |
|---|---|---|---|---|
| LGD sin garantía | 45 % | Manual_LGD.pdf > 3.2 > p.14 | No | IMP-01 |
| Tasa impositiva | 29,5 % | [SUPUESTO] no está en el expediente | Sí | Total neto |
| Tipo de cambio | 3,75 | Base > columna tc_cierre (fecha de corte) | No | Conversión USD |

Reglas:
- Fuente válida: manual, código o Excel del equipo, política, norma con artículo, o la propia base (columna y fecha).
- Sin fuente → `[SUPUESTO]` y además va a "Brechas de evidencia" con la solicitud del dato al equipo.
- Nunca una cifra en el informe sin su fila en este registro.

## 2. Verificar el material del equipo antes de reutilizarlo

| Material | Verificación | Si falla |
|---|---|---|
| Excel de impactos | Recalcular sus salidas con el notebook o reconciliar con `virf-a2-reconciliacion-pruebas` | Reportar; usar la fórmula como referencia citada, no sus cifras |
| Código .py | Ejecutar en kernel limpio con la base del ciclo | Reportar traza; construir función mínima |
| Supuestos dentro del material | Pasarlos al registro con cita a la celda/línea | — |

Cita del origen siempre: `Excel_Impactos.xlsx > Calculo > F2:F9000` o `impactos.py > calcular_ecl() > línea 40`.

## 3. Diseñar la sensibilidad

El rango debe reflejar **incertidumbre real**, no simetría arbitraria:

| Fuente de incertidumbre | Cómo fijar bajo/alto |
|---|---|
| Valor imputado desconocido | Percentiles 25/75 de la variable en registros sanos comparables |
| Parámetro con política | Mínimo/máximo de la política |
| Parámetro sin política | ±1 desviación estándar histórica, rotulado [SUPUESTO] |
| Clasificación ambigua (stage, categoría) | Mejor caso / peor caso de reclasificación |

Si no hay base para un rango, reporta solo el central y escribe "sin sustento para rango de sensibilidad".

## 4. Redacción de resultados

```markdown
## Resultados (moneda: PEN; fecha de corte: 2026-06-30)
| ID | Hallazgo | Canal | Base | Corregida | Δ | Δ % | Rango Δ | Supuestos clave |
**Total válido (escenario conjunto):** Δ = S/ X (rango ...). La suma simple S/ Y sobreestima por doble conteo en N operaciones.
**Lectura:** "El defecto H-03 subestima la ECL 12m en S/ 1,24 MM (2,1 %), rango S/ 0,98–1,61 MM según LGD 35–60 %."
```

Prohibido: "impacto no material", "aceptable", "cumple". La materialidad la juzgan A6/A11 con estas cifras.
