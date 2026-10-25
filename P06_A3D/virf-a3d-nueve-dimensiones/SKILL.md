---
name: virf-a3d-nueve-dimensiones
description: Catálogo de las nueve dimensiones de calidad de datos para la batería del validador (completitud, unicidad, validez, exactitud, consistencia, integridad referencial, oportunidad, razonabilidad y estabilidad, trazabilidad) con la prueba pandas de cada una, la métrica que devuelve y el umbral con su origen. Úsala en el Paso 6 (A3D) para construir el bloque 2 de la batería, y en A3E/A6 para interpretar sus resultados.
---

# A3D · Las nueve dimensiones

> Si `Estandares_VIRF.xlsx` nombra o agrupa las dimensiones de otra forma, **prevalece el estándar**: renombra las filas y conserva las pruebas. Esta lista es la referencia operativa, alineada a BCBS 239 (exactitud, integridad, completitud, oportunidad, adaptabilidad) y a las prácticas DAMA.

Cada control devuelve siempre: `n_evaluado`, `n_infractor`, `pct_infractor`, `muestra_llaves` (hasta 10, orden determinista), `umbral`, `origen_umbral`, `estado`.

| # | Dimensión | Pregunta | Prueba típica (pandas) | Umbral |
|---|---|---|---|---|
| D1 | Completitud | ¿Faltan valores obligatorios o registros esperados? | `df[c].isna()`; conteo vs. población esperada por periodo | Del diccionario/catálogo; si no hay: `[SUPUESTO]` |
| D2 | Unicidad | ¿Hay duplicados de la llave de negocio? | `df.duplicated(llave, keep=False)` | 0 duplicados (la llave es por definición única) |
| D3 | Validez | ¿Los valores pertenecen al dominio/formato? | `~df[c].isin(catalogo)`; regex de formato; tipos | Catálogo oficial |
| D4 | Exactitud | ¿Coincide con la fuente autorizada? | Conciliación de totales vs. contable/fuente (`abs(suma_base − suma_fuente)/suma_fuente`) | Tolerancia declarada por el banco |
| D5 | Consistencia | ¿Los campos son coherentes entre sí y entre tablas? | `fecha_desembolso <= fecha_corte`; `saldo <= monto_original`; mismo cliente con mismo segmento | Regla de negocio (0 infractores) |
| D6 | Integridad referencial | ¿Toda FK existe en su maestro? | `~df.fk.isin(maestro.pk)`; `merge(..., indicator=True)` | 0 huérfanos |
| D7 | Oportunidad | ¿El dato corresponde al corte y llegó a tiempo? | `max(fecha) == fecha_corte`; desfase entre fecha de carga y corte | Calendario de cierre |
| D8 | Razonabilidad y estabilidad | ¿Rangos y distribución son plausibles y estables? | Rangos/signos; PSI por variable vs. periodo anterior; outliers (IQR/percentiles) | PSI: 0,10 / 0,25 solo si el banco los declara; si no `[SUPUESTO]` |
| D9 | Trazabilidad (linaje) | ¿Cada campo tiene origen y responsable? | Cruce columnas del modelo vs. diccionario (sistema, tabla, campo, responsable) | 100 % de variables del modelo con linaje |

## Notas de implementación

- **D1:** distingue nulo real de valores centinela (`0`, `-1`, `9999`, `""`, `"NULL"`, `1900-01-01`). Cuenta ambos por separado y reporta la regla de centinela usada.
- **D2:** reporta `n_grupos_duplicados` además de filas afectadas.
- **D4:** si no se entregó fuente de conciliación → estado `No verificable` (no "Cumple").
- **D8 PSI:**
  ```python
  def psi(base, actual, bins=10):
      cortes = np.unique(np.quantile(base.dropna(), np.linspace(0, 1, bins + 1)))
      b = np.histogram(base.dropna(), cortes)[0] / base.notna().sum()
      a = np.histogram(actual.dropna().clip(cortes[0], cortes[-1]), cortes)[0] / actual.notna().sum()
      b, a = np.clip(b, 1e-6, None), np.clip(a, 1e-6, None)
      return float(((a - b) * np.log(a / b)).sum())
  ```
- **D9:** es la entrada directa del "linaje" de A3E y A6; una variable del modelo sin origen es hallazgo de gobierno del dato.

## Umbrales: regla dura

Umbral = valor declarado por el banco con su fuente (`manual_controles_datos.md > sección`, catálogo, diccionario). Si no existe, el control **se ejecuta igual** pero su estado es `No verificable` y el umbral se rotula `[SUPUESTO] <valor> (referencia, no del banco)`. Nunca inventes un umbral y lo presentes como del banco.

## Base depurada

Si el equipo entregó la base ya limpia, el control pierde capacidad de detección: ejecuta, registra "base entregada depurada" y solicita la base previa (A6 marcará "No verificable").
