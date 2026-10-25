---
name: virf-aim-canales-impacto
description: Catálogo de canales de impacto que traducen un defecto de datos en movimiento monetario de magnitudes de negocio - pérdida esperada y provisión IFRS 9, VaR y cargo de capital de mercado, RWA y capital, P&L, EVE y NII en IRRBB, brecha de liquidez - con la fórmula de cada canal, qué variable mueve el defecto y cómo cuantificar base vs defecto. Úsala en el Paso 8 (agente AIM) para decidir cómo valorar cada hallazgo material de A3E.
---

# AIM · Canales de impacto

Un hallazgo sin canal de impacto describe un problema de base de datos; con canal, describe un riesgo de modelo con monto. Para cada hallazgo material del Paso 7 define: **variable afectada → magnitud que mueve → fórmula → monto base vs monto con defecto.**

## 1. Crédito / IFRS 9

Pérdida esperada por operación (forma general):

```
ECL_12m = PD_12m × LGD × EAD                         (stage 1)
ECL_lt  = Σ_t  PD_marginal_t × LGD_t × EAD_t × DF_t  (stage 2 y 3)
```

| Defecto típico | Variable | Canal | Cómo cuantificar |
|---|---|---|---|
| Mora mal calculada / transición de stage inválida | stage | 12m ↔ lifetime | Recalcular ECL con stage corregido en las operaciones infractoras |
| Nulos imputados en variable del score | score → PD | PD por cliente | Recalcular PD con valor real (si existe) o con escenarios de imputación alternativos |
| Colateral faltante | LGD | LGD sin garantía | ECL con LGD con vs sin colateral |
| Duplicados de operación | EAD | Doble conteo | Restar ECL de duplicados |
| Saldo que resucita | EAD | Exposición fantasma | ECL de la exposición resucitada |
| Default mal definido | target → calibración | PD media | Re-escalar a la tasa central con target corregido (pedir a A7 si aplica) |

Si el modelo usa provisiones regulatorias (tasas por categoría de riesgo del deudor), el canal es la **reclasificación de categoría**: Δprovisión = Σ saldo × (tasa_categoría_corregida − tasa_categoría_actual). Cita la tabla de tasas del manual o de la norma vigente con su artículo; si no está en el expediente, `[SUPUESTO]`.

## 2. Mercado / VaR

| Defecto | Canal | Cuantificación |
|---|---|---|
| Precios repetidos (stale) | volatilidad subestimada | VaR con serie corregida o con precios de fuente alternativa |
| Huecos en serie | ventana efectiva menor | VaR con ventana completa |
| Posición duplicada/faltante | exposición | VaR con cartera conciliada contra contabilidad |
| P&L incorrecto en backtesting | n° de excepciones | Recuento de excepciones → cambio de zona (si el marco usa semáforo de backtesting) → multiplicador de capital |

Cargo de capital (cuando aplique el enfoque de modelos internos): `max(VaR_t−1, m × VaR_promedio_60d)`; `m` y su recargo por excepciones deben venir del marco del banco; si no, `[SUPUESTO]`.

## 3. Capital / RWA

```
ΔCapital requerido = ΔRWA × ratio_de_capital_requerido
```
El ratio debe citarse (política interna o norma vigente). Defectos típicos: ponderador mal asignado, EAD inflado, mitigantes no reconocidos.

## 4. P&L

- Δprovisión → gasto de provisiones del periodo (impacto directo antes de impuestos).
- Si el banco quiere neto: Δ × (1 − tasa impositiva) con tasa citada.
- Valoración: Δprecio × posición.

## 5. ALM / IRRBB

```
ΔEVE = Σ_buckets  flujo_b × (DF_b(shock) − DF_b(base))
ΔNII = Σ_buckets  gap_repricing_b × Δtasa × fracción_del_año_remanente_b
```
Defectos: bucket mal asignado, depósitos sin vencimiento con supuesto conductual erróneo, curva de fecha incorrecta.

## 6. Liquidez / LaR

Δbrecha por bucket = flujo corregido − flujo actual; impacto en ratios (LCR/indicadores internos) = recalcular con flujos corregidos y factores citados.

## 7. Operacional

Duplicados de eventos o recuperaciones mal netadas → Δpérdida agregada → Δcapital si el método de capital usa la base de pérdidas.

## Regla de oro

Cada fórmula se usa **solo si es la del modelo/banco** (manual o código del equipo, citado). Las de este skill son la forma general para cuando debes construir el canal; en ese caso el canal se declara "construido por el validador" y sus parámetros no citados van como `[SUPUESTO]`.
