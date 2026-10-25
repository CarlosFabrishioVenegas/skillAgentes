---
name: virf-a2-inventario-excel
description: Inventario forense de una herramienta de modelo en Excel (.xlsx/.xlsm) antes de traducirla a Python - hojas visibles y ocultas, rangos con nombre, macros VBA, conexiones externas, fórmulas volátiles HOY/AHORA/ALEATORIO, valores pegados donde se espera fórmula, filtros activos, sistema de fechas 1900/1904 y clasificación de hojas en ENTRADA, PARÁMETROS, CÁLCULO, SALIDA o AUXILIAR. Úsala al inicio del Paso 2 (A2).
---

# A2 · Inventario del libro Excel

Antes de traducir una sola fórmula, levanta el inventario. La mitad de las diferencias de reconciliación se explican por algo que estaba en el libro y no se vio: una hoja oculta con parámetros, un valor pegado, un filtro activo.

## Ejecución

```bash
python scripts/inventario_excel.py Herramienta_PD_2026.xlsm --salida inventario/
```

Genera:
- `inventario_hojas.csv`: hoja, visibilidad (visible/hidden/veryHidden), dimensiones, n° fórmulas, n° constantes, rol sugerido, filtro activo.
- `inventario_nombres.csv`: rangos con nombre y su destino.
- `formulas.csv`: hoja, celda, fórmula, funciones usadas, referencias a otras hojas, volátil (sí/no).
- `alertas.csv`: riesgos detectados con severidad.
- `resumen.md`: tabla lista para pegar en `A2_reconciliacion.md`.

## Clasificación de hojas (heurística, confirmar a mano)

| Rol | Señal |
|---|---|
| ENTRADA | Mayoría de constantes, muchas filas, encabezado tipo tabla |
| PARÁMETROS | Pocas celdas, constantes numéricas con etiqueta a la izquierda, rangos con nombre |
| CÁLCULO | Mayoría de fórmulas que referencian otras hojas |
| SALIDA | Fórmulas finales, pocas filas, formato de reporte, referenciada por nadie |
| AUXILIAR | Tablas de búsqueda, catálogos, listas de validación |

## Alertas que el script levanta y su tratamiento

| Alerta | Severidad | Tratamiento en A2 |
|---|---|---|
| `vbaProject.bin` presente | Alta | Si no se puede leer el código VBA: "Lógica en VBA no accesible", riesgo de implementación alto. Si se puede (olevba), transcribirlo como anexo. |
| Conexión externa (`externalLinks`, `connections.xml`) | Alta | Stub que falle explícitamente en el notebook; nunca datos simulados. |
| Hoja oculta / muy oculta | Media | Procesar igual y marcar; suele tener parámetros vivos. |
| Fórmula volátil (HOY, AHORA, ALEATORIO, DESREF, INDIRECTO) | Media | Parametrizar fecha/semilla en CONFIG; documentar variabilidad. |
| Constante numérica en columna mayoritariamente de fórmulas | Alta | "Cálculo endurecido (hardcoded)": rompe reproducibilidad. |
| Autofiltro activo | Alta si el cálculo usa SUBTOTAL/AGREGAR | Verificar dependencia de filas visibles. |
| Rango de referencia muy por encima de la última fila con datos (A1:A100000) | Baja | Recortar al rango con datos y anotar. |
| `date1904=True` | Media | Ajustar conversión de fechas (+1462 días). |
| Referencia circular / cálculo iterativo habilitado | Alta | Detener y reportar; replicar iteraciones solo si el libro las habilita. |
| Formato de número que oculta decimales | Baja | Trabajar con valor almacenado, no mostrado. |

## Reglas

- No abras y guardes el libro original: trabaja sobre una copia (`openpyxl` con `read_only`/`data_only` según el paso). Guardar con openpyxl elimina macros y valores cacheados.
- Lee dos veces: `data_only=False` (fórmulas) y `data_only=True` (últimos valores calculados por Excel = valores de referencia para reconciliar). Si los valores cacheados son `None`, el libro nunca se recalculó tras guardarse: pide al equipo que lo abra, recalcule y guarde.
- Registra el SHA-256 del libro en la celda 1 del notebook.
