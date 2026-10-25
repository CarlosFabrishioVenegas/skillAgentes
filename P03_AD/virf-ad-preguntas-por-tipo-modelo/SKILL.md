---
name: virf-ad-preguntas-por-tipo-modelo
description: Banco de preguntas materiales de diagnóstico por tipo de modelo bancario (Crédito/IFRS 9, Mercado/VaR, ALM/IRRBB, Liquidez/LaR, Operacional, Conductual) y su mapeo a controles C1-C6, para decidir qué instrumentar en cada ronda y cuándo una incógnita es material. Úsala en el Paso 3 (AD) al planificar la ronda 1 y al decidir si seguir iterando.
---

# AD · Preguntas materiales por tipo de modelo

Ronda 1 siempre: esquema, llaves, granularidad, cobertura temporal, presencia de variables del modelo. Desde la ronda 2, elige solo las preguntas abiertas de la tabla del tipo correspondiente.

## Crédito / IFRS 9 (PD, LGD, EAD, provisiones)

| Q | Pregunta | Control | Señal en datos |
|---|---|---|---|
| CR1 | ¿La definición de default del código coincide con la del manual (días de mora, refinanciado, castigo)? | C3, C4 | conteo de defaults por regla alternativa |
| CR2 | ¿Hay saldos que reaparecen tras cancelación o castigo? | C2 | 0 → >0 por operación |
| CR3 | ¿El saldo amortiza monótonamente en productos de cuota fija? | C2 | incrementos sin desembolso |
| CR4 | ¿Las transiciones de etapa (stage 1/2/3) son válidas (no 3→1 sin cura documentada)? | C2, C3 | matriz de transición |
| CR5 | ¿La ventana de desempeño en datos es la declarada? | C3 | meses entre observación y desempeño |
| CR6 | ¿Cuántas operaciones carecen de garantía/valor de colateral para LGD? | C2 | nulos en colateral |
| CR7 | ¿Las variables macro (forward looking) tienen fuente y fecha de escenario? | C3, C5 | columnas de escenario |
| CR8 | ¿La provisión recalculada coincide con la publicada? | C4, C6 | suma de control |

## Mercado / VaR

| Q | Pregunta | Control | Señal |
|---|---|---|---|
| MV1 | ¿Las series de precios/factores tienen huecos, precios repetidos (stale) o saltos sin evento? | C2 | días consecutivos con mismo precio |
| MV2 | ¿La ventana histórica usada es la declarada (p. ej. 250 días)? | C3, C4 | n observaciones |
| MV3 | ¿El backtesting cuenta excepciones con el P&L correcto (hipotético vs real)? | C3 | columnas P&L |
| MV4 | ¿Las posiciones del cálculo coinciden con las del cierre contable? | C2, C4 | conciliación |
| MV5 | ¿El nivel de confianza y el horizonte implementados son los declarados? | C4 | parámetros |

## ALM / IRRBB

| Q | Pregunta | Control | Señal |
|---|---|---|---|
| AL1 | ¿Todos los productos tienen bucket de repricing asignado? | C2 | nulos en bucket |
| AL2 | ¿Los depósitos sin vencimiento usan el supuesto conductual declarado (core/no core)? | C3 | proporción asignada |
| AL3 | ¿Las curvas de tasas tienen la fecha de corte del cálculo? | C2 | fecha de curva |
| AL4 | ¿Los escenarios de shock aplicados son los regulatorios vigentes? | C3, C5 | magnitudes de shock |

## Liquidez / LaR

| Q | Pregunta | Control | Señal |
|---|---|---|---|
| LQ1 | ¿Los flujos tienen fecha y signo coherentes (entradas +, salidas −)? | C2 | signos |
| LQ2 | ¿Los haircuts/factores de salida son los declarados? | C3, C4 | parámetros |
| LQ3 | ¿El percentil/nivel de confianza del LaR coincide con el manual? | C4 | |

## Operacional

| Q | Pregunta | Control | Señal |
|---|---|---|---|
| OP1 | ¿La base de eventos tiene duplicados por evento (mismo evento, varias líneas)? | C2 | unicidad de evento |
| OP2 | ¿Fecha de ocurrencia ≤ fecha de descubrimiento ≤ fecha de registro? | C2 | coherencia temporal |
| OP3 | ¿Las recuperaciones están netas o brutas según el manual? | C3 | columnas |
| OP4 | ¿Hay umbral mínimo de captura y se respeta? | C2, C3 | montos < umbral |

## Conductual (prepago, renovación, deserción)

| Q | Pregunta | Control | Señal |
|---|---|---|---|
| CO1 | ¿El evento conductual está definido igual en datos y manual? | C3 | conteo por definición |
| CO2 | ¿Hay censura correctamente tratada (operaciones vivas al corte)? | C3 | fechas fin |
| CO3 | ¿La tasa observada reciente difiere de la calibrada? | C3 | tasa por cosecha |

## Regla de materialidad para decidir parar

Una pregunta deja de ser material si: (a) ya se respondió con cifra citada; (b) la variable o regla no interviene en el output; o (c) su respuesta no cambiaría el estado de ningún control. Cuando todas las preguntas abiertas cumplen (b) o (c), cierra.
