---
name: virf-a3d-reglas-ciclo-vida
description: Librería de reglas de ciclo de vida del dato para bases de riesgo bancario en panel (operación por periodo) - saldos que resucitan, monotonía de amortización, unicidad de eventos, transiciones de estado inválidas, continuidad temporal, coherencia entre campos, signos y rangos - con funciones pandas deterministas que devuelven conteo, porcentaje y muestra de llaves. Úsala en el Paso 6 (A3D) para el bloque 2 de la batería.
---

# A3D · Reglas de ciclo de vida

Implementadas en `scripts/reglas_ciclo_vida.py`. Cada función recibe un DataFrame en panel y nombres de columna **reales** (descubiertos por AD o por el esquema), y devuelve un dict estándar:

```python
{"regla": str, "n_evaluado": int, "n_infractor": int, "pct": float, "muestra_llaves": list, "detalle": str}
```

| Función | Regla de negocio (lenguaje natural) | Aplica a |
|---|---|---|
| `saldo_resucita(df, id, fecha, saldo)` | Una operación con saldo 0 o cancelada no vuelve a tener saldo > 0 | Crédito, ALM |
| `amortizacion_monotona(df, id, fecha, saldo, desembolso=None)` | En cuota fija el saldo no aumenta salvo desembolso/refinanciación | Crédito |
| `unicidad_eventos(df, llave_evento)` | Un evento (default, castigo, pérdida) ocurre una vez por operación | Crédito, Operacional |
| `transiciones_invalidas(df, id, fecha, estado, permitidas)` | Solo transiciones de la matriz permitida (p. ej. castigo es absorbente) | Crédito, IFRS 9 |
| `continuidad_temporal(df, id, fecha)` | Una operación viva aparece en todos los periodos entre su primer y último registro | Panel |
| `coherencia_campos(df, expr, descripcion)` | Expresión booleana que debe cumplirse (p. ej. `fecha_desembolso <= fecha_corte`) | Todos |
| `signos_rangos(df, col, minimo=None, maximo=None)` | Valores dentro de rango y signo esperado (VaR ≥ 0, PD ∈ [0,1]) | Todos |
| `orden_fechas(df, cols)` | Fechas en orden lógico (ocurrencia ≤ descubrimiento ≤ registro) | Operacional |

## Uso

```python
import sys; sys.path.append("scripts")
import reglas_ciclo_vida as rcv
r = rcv.saldo_resucita(base, "cod_operacion", "fecha_corte", "saldo_capital")
r = rcv.transiciones_invalidas(base, "cod_operacion", "fecha_corte", "stage",
        permitidas={("1","1"),("1","2"),("2","1"),("2","2"),("2","3"),("3","3"),("3","2")})
r = rcv.coherencia_campos(base, "saldo_capital <= monto_desembolsado * 1.0001", "Saldo no excede el monto desembolsado")
```

## Reglas de rigor

- **Columnas reales:** nunca nombres supuestos. Si la columna no existe, la función lanza `KeyError` con mensaje: el notebook lo captura y registra el control como `No verificable — columna <x> no existe`.
- **Determinismo:** orden por `(id, fecha)` antes de `shift`; muestra = primeras 10 llaves en orden.
- **Matriz de transiciones permitidas:** debe venir del manual/política. Si no está declarada → `[SUPUESTO]` y el estado queda `No verificable`.
- **Tolerancias numéricas** (p. ej. 1.0001 en el ejemplo): declarar su origen; si es tuya, `[SUPUESTO]`.
- Los infractores se reportan, no se corrigen: el notebook no modifica la base.

## Elegir reglas por tipo de modelo

| Tipo | Reglas mínimas |
|---|---|
| Crédito / IFRS 9 | resucita, amortización, unicidad de default, transiciones de stage, continuidad, signos (PD, LGD ∈ [0,1], EAD ≥ 0) |
| Mercado / VaR | continuidad de series, precios repetidos (stale), signos (VaR ≥ 0), coherencia posición–cierre contable |
| ALM / IRRBB | coherencia fechas de repricing ≥ corte, signos de flujos, bucket asignado |
| Operacional | unicidad de evento, orden de fechas, monto bruto ≥ recuperación |
| Conductual | coherencia de censura (fecha fin ≥ fecha inicio), unicidad de evento |
