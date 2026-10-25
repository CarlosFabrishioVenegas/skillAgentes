---
name: virf-a2-reconciliacion-pruebas
description: Reconciliación celda a celda Excel vs notebook con tolerancia relativa 1e-9, mapa de trazabilidad hoja-celda-función-línea y las cuatro pruebas mínimas de admisibilidad del notebook (kernel limpio, reconciliación, idempotencia, insumo vacío); genera A2_reconciliacion.md y la hoja de pruebas para A11. Úsala al cerrar el Paso 2 (A2) y cuando A8 exija la tabla de reconciliación.
---

# A2 · Reconciliación y pruebas de admisibilidad

El notebook **no se entrega** sin tabla de reconciliación. Una celda no reconciliada sin explicación vuelve el entregable "notebook no admisible".

## 1. Reconciliación

Prepara un CSV `salidas_notebook.csv` con columnas `hoja,celda,valor_notebook` (la celda 6 del notebook lo escribe) y ejecuta:

```bash
python scripts/reconciliar_excel_notebook.py Herramienta.xlsx salidas_notebook.csv --tol 1e-9 --salida A2_reconciliacion.md
```

El script lee los valores cacheados del Excel (`data_only=True`) y produce:

| Salida | Valor Excel | Valor notebook | Dif. absoluta | Dif. relativa | Estado |
|---|---|---|---|---|---|
| Calculo!H45 | 12480331.20 | 12480018.55 | 312.65 | 2.5e-05 | No reconciliado |

Diferencia relativa = |nb − xl| / max(|xl|, 1e-12). Estado `Reconciliado` si ≤ tol.

Diagnóstico típico de no reconciliados (revisar en este orden):
1. Redondeo intermedio no replicado (o `round()` bancario en vez de half-up).
2. BUSCARV con duplicados: Excel tomó el primero.
3. Vacíos tratados como 0 en vez de NaN (o viceversa) en PROMEDIO/CONTAR.
4. Fechas: sistema 1904 o serial 60.
5. Rango recortado distinto al del Excel.
6. Filas ocultas por filtro.
7. Valor cacheado desactualizado en el Excel (libro no recalculado).

**No ajustes el código para forzar la igualdad.** Documenta la causa; si es precisión de punto flotante pura, documenta los casos que superan 1e-9.

## 2. Mapa de trazabilidad

| Hoja | Celda/rango | Rol | Función en el notebook | Línea | Observación |
|---|---|---|---|---|---|
| Parametros | C4 | PARÁMETROS | CONFIG["corte_score"] | 14 | |
| Calculo | D14:D980 | CÁLCULO | calcular_pd() | 52 | redondeo a 4 dec replicado |

## 3. Las cuatro pruebas mínimas

```bash
python scripts/pruebas_admisibilidad.py A2_notebook.ipynb --insumo-vacio datos_vacios/ --salida pruebas_A2.csv
```

| # | Prueba | Cómo se ejecuta | PASA si |
|---|---|---|---|
| 1 | Ejecución limpia | `jupyter nbconvert --to notebook --execute` en kernel nuevo | sin excepción |
| 2 | Reconciliación | tabla anterior | 100 % reconciliado o explicado |
| 3 | Idempotencia | dos ejecuciones, hash de las salidas | hashes idénticos |
| 4 | Insumo vacío | `VIRF_INSUMO_DIR` apuntando a carpeta vacía | falla con mensaje explícito (no produce resultado) |

Para la prueba 4 el notebook debe leer la carpeta de datos desde `os.environ.get("VIRF_INSUMO_DIR", CONFIG["ruta_insumo"])` y validar `if df.empty: raise ValueError("Insumo vacío: ...")`.

`pruebas_A2.csv` tiene el formato de la HOJA 3 de A11: `ID prueba | Control asociado | Descripción | Insumo | Resultado esperado | Resultado obtenido | PASA/FALLA | Umbral y fuente | Script o celda | Fuente exacta`.

## 4. Entregables

1. `A2_notebook.ipynb`
2. `02_Motor.xlsx` con hojas `Resultados`, `Reconciliacion`, `Trazabilidad`, `Log` (fecha, hash del libro, versión de librerías, pruebas).
3. `A2_reconciliacion.md` con: tabla de reconciliación, mapa de trazabilidad, pruebas, lista de no traducibles con riesgo, hallazgos de traducción y "Brechas de evidencia".

Reconciliación parcial (solo una hoja traducida): se permite, pero el encabezado dice "Reconciliación parcial: no acredita equivalencia del libro completo".
