---
name: virf-a2-traduccion-formulas-python
description: Equivalencias exactas de funciones de Excel (BUSCARV, SI.ERROR, SUMAR.SI.CONJUNTO, REDONDEAR, fechas, fórmulas matriciales, tablas dinámicas) a pandas/numpy, orden de traducción por grafo de dependencias, réplica de redondeo half-up de Excel y estructura obligatoria del notebook (CONFIG con celda de origen, funciones puras, exportación fechada). Úsala en el Paso 2 (A2) al escribir el notebook equivalente.
---

# A2 · Traducción de fórmulas Excel → Python

Principio: **replicar, no mejorar.** Si el Excel calcula algo de forma discutible, se replica idéntico y se registra como observación de traducción.

## 1. Orden de traducción

Traduce por grafo de dependencias (hojas PARÁMETROS → ENTRADA → CÁLCULO → SALIDA), no por orden visual. Con `formulas.csv` del inventario:

```python
import networkx as nx, pandas as pd
f = pd.read_csv("inventario/formulas.csv")
G = nx.DiGraph()
for _, r in f.iterrows():
    for h in str(r.hojas_referenciadas).split(";"):
        if h and h != "nan" and h != r.hoja:
            G.add_edge(h, r.hoja)
ciclos = list(nx.simple_cycles(G))   # si hay: detener y reportar
orden = list(nx.topological_sort(G))
```

Para dependencias celda a celda finas, la librería `formulas` (pip `formulas`) o `pycel` construyen el grafo real y sirven además como oráculo independiente para reconciliar.

## 2. Tabla de equivalencias (las que más fallan)

| Excel | Python correcto | Trampa |
|---|---|---|
| `BUSCARV(x;T;k;FALSO)` | `df.merge(T, on=..., how="left", validate="many_to_one")` | Duplicados en la tabla de búsqueda: Excel toma el **primero**; `validate` lo detecta. Si el libro depende de "el primero", usar `T.drop_duplicates(keep="first")` y anotarlo. |
| `BUSCARV(...;VERDADERO)` (aproximada) | `pd.merge_asof(sorted, ..., direction="backward")` | Requiere orden ascendente igual que Excel. |
| `SI.ERROR(expr;v)` | `try/except` o `.fillna(v)` con el **valor exacto** del Excel | Nunca 0 por omisión. Distinguir #N/D de #DIV/0!. |
| `SUMAR.SI.CONJUNTO` | `df.loc[m1 & m2, col].sum()` o `groupby` | Criterios texto con comodines `*`/`?` → `str.match`; Excel no distingue mayúsculas. |
| `CONTAR.SI` | `(cond).sum()` | Excel cuenta "1" texto y 1 número distinto según criterio. |
| `PROMEDIO` | `s.mean()` | Excel ignora texto y vacíos; pandas ignora NaN: verificar que vacíos sean NaN y no 0. |
| `REDONDEAR(x;n)` | `redondear_excel(x, n)` (abajo) | `round()` de Python es redondeo bancario: 2.5→2. Excel: 2.5→3. |
| `TRUNCAR` | `np.trunc(x*10**n)/10**n` | |
| `ENTERO(x)` | `np.floor(x)` | Para negativos ENTERO(-2.5) = -3. |
| `ALEATORIO()` | `np.random.default_rng(CONFIG["semilla"])` | Imposible reproducir el valor del Excel: reconciliar sobre estadísticos, declarar. |
| `HOY()` | `CONFIG["fecha_corte"]` | Documentar que el Excel varía por día. |
| Fecha serial | `pd.to_datetime(n, unit="D", origin="1899-12-30")` | Sistema 1904: origin "1904-01-01". Serial 60 = 29/02/1900 inexistente. |
| `FECHA.MES(f;n)` | `f + pd.DateOffset(months=n)` | |
| `FIN.MES` | `f + pd.offsets.MonthEnd(n)` | Verificar n=0 cuando f ya es fin de mes. |
| `SUMAPRODUCTO` | `(a*b).sum()` | Booleanos en Excel con `--`. |
| Matricial / arreglo dinámico | operación vectorizada | Verificar celda a celda, no solo el total. |
| Tabla dinámica | `pivot_table` / `groupby` | Comparar totales + 3 celdas internas al azar (semilla fija). |
| `SUBTOTAL(9;...)`/`AGREGAR` | Depende de filas visibles | Si el libro tiene filtro: riesgo de implementación alto. |
| `TEXTO(x;"0.00")` | f-string | Si luego se usa como número, replicar el redondeo implícito. |

```python
from decimal import Decimal, ROUND_HALF_UP
def redondear_excel(x, n=0):
    """Replica REDONDEAR de Excel (half away from zero)."""
    if x is None or (isinstance(x, float) and x != x):
        return x
    q = Decimal(1).scaleb(-n)
    return float(Decimal(repr(x)).quantize(q, rounding=ROUND_HALF_UP))
```

Vectorizado: `s.map(lambda v: redondear_excel(v, 2))`. Redondea **en el mismo punto** donde el Excel redondea la celda intermedia.

## 3. Estructura obligatoria del notebook

```text
Celda 1  Metadatos: modelo, código, libro origen, SHA-256 del libro, fecha, versión de Python y librerías
Celda 2  CONFIG = { "corte_score": 640,  # origen: Herramienta.xlsx > Parametros > C4 ... }
Celda 3  Carga de datos (solo lectura; stub que falla si hay conexión externa no entregada)
Celda 4  Funciones de cálculo puras (DataFrame -> DataFrame), cada una con '# origen: hoja > rango'
Celda 5  Ejecución en orden de dependencias
Celda 6  Reconciliación (ver skill virf-a2-reconciliacion-pruebas)
Celda 7  Exportación a salida/AAAAMMDD_HHMM/ (02_Motor.xlsx con resultados y log), nunca sobre el insumo
```

Convenciones: un solo CONFIG; ninguna constante dentro de funciones sin comentario de origen; semilla declarada; no renombrar variables si rompe la trazabilidad con la hoja (usar el nombre del encabezado del Excel en snake_case y mantener un dict de equivalencia).

## 4. Stub para fuentes no entregadas

```python
def cargar_conexion_externa():
    raise FileNotFoundError(
        "Fuente externa no entregada: Herramienta.xlsx > conexión 'DM_CLIENTE'. "
        "No se simulan datos. Solicitar extracción al equipo dueño.")
```

## 5. Hallazgos de traducción

Registra todo lo que replicaste sin estar de acuerdo:

| N° | Hoja > celda | Comportamiento del Excel | Por qué es discutible | Replicado | Control afectado |
|---|---|---|---|---|---|
