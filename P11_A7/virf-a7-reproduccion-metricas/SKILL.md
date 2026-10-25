---
name: virf-a7-reproduccion-metricas
description: Reproducción independiente de métricas de desempeño de modelos de riesgo y tabla obligatoria métrica, valor reportado, valor reproducido, umbral declarado, fuente del umbral, estado - discriminación (AUC, Gini, KS), estabilidad (PSI, CSI), calibración (binomial por grado, Jeffreys, Hosmer-Lemeshow, Brier, tasa observada vs esperada) y backtesting de VaR (Kupiec, Christoffersen, semáforo de excepciones). Úsala en el Paso 11 (A7).
---

# A7 · Reproducción de métricas

Métrica que no se reproduce con los datos y el código entregados es **No verificable**, y eso es más grave que una métrica baja.

## Uso del script

```bash
# Crédito: discriminación + calibración + estabilidad
python scripts/metricas_validacion.py credito --datos validacion.parquet --y default_12m --score pd_estimada \
    --grado rating --base desarrollo.parquet --vars ingreso,antiguedad,score --reportadas reportadas.csv --salida metricas.csv

# Mercado: backtesting de VaR
python scripts/metricas_validacion.py var --datos backtest.csv --pnl pnl_hipotetico --var var_99 --nivel 0.99 --reportadas reportadas.csv --salida metricas.csv
```

`reportadas.csv`: `metrica,valor_reportado,umbral,fuente_umbral,fuente_reportado` (lo que dice el informe del equipo). El script completa `valor_reproducido`, `diferencia` y `estado`.

## Métricas implementadas

| Familia | Métrica | Notas |
|---|---|---|
| Discriminación | AUC, Gini = 2·AUC − 1, KS | Requiere `y` binaria y score/PD (mayor = más riesgo) |
| Estabilidad | PSI del score; CSI por variable | Deciles de la base de desarrollo |
| Calibración | Tasa observada vs PD media (global y por grado); binomial exacta por grado (p-valor una cola); intervalo de Jeffreys (Beta(d+½, n−d+½)); Hosmer-Lemeshow (10 grupos); Brier | Binomial/Jeffreys asumen independencia de defaults: anotarlo |
| Backtesting VaR | N° excepciones; Kupiec POF (LR, p-valor); Christoffersen independencia (LR, p-valor); zona del semáforo (verde 0–4, amarilla 5–9, roja ≥10 para 250 obs. al 99 %) | La zona solo se usa si el marco del banco la adopta |

## Tabla obligatoria (núcleo cuantitativo del control)

```markdown
| Métrica | Valor reportado | Valor reproducido | Umbral declarado | Fuente del umbral | Estado |
|---|---|---|---|---|---|
| Gini (validación OOT) | 0,58 | 0,571 | ≥ 0,45 | Política_Modelos.pdf > 4.2 > p.9 | Cumple |
| PSI score | 0,07 | 0,068 | < 0,10 | [SUPUESTO] no declarado | No verificable |
| Binomial grado B5 | p=0,12 | p=0,031 | p ≥ 0,05 | Manual > 6.3 > p.40 | No cumple |
```

Reglas:
- Diferencia reportado vs reproducido: si |dif| > 0,005 en AUC/Gini/KS o el estado cambia → hallazgo de reproducibilidad (explicar causa: población, ventana, versión del score).
- Sin umbral declarado → "No verificable" y solicitar formalización. **No es cumplimiento tácito.**
- No reproducible (sin datos/código) → columna "no reproducible — <causa>".
- Calcula sobre la **población y ventana declaradas**; si el equipo usó otra, repórtalo como hallazgo (A7 coherencia interna).

## Referencias conceptuales (para el bloque de recomendaciones, no como sustento)

Kupiec (1995) POF; Christoffersen (1998) independencia; BCBS (1996) marco de backtesting con semáforo; para calibración de PD, literatura de tests binomiales y de Jeffreys (usados por supervisores europeos). Solo se acreditan si están en papers/ del expediente.
