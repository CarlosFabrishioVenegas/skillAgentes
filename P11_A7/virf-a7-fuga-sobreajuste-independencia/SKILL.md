---
name: virf-a7-fuga-sobreajuste-independencia
description: Pruebas de coherencia interna de la metodología - fuga de información (variables construidas con información posterior al momento de decisión), sobreajuste (brecha de desempeño desarrollo vs validación), independencia de la muestra de validación (traslape de cosechas y clientes), tamaño de celdas de segmentación, overlays discrecionales, supuestos macro sin dueño y cambios de metodología sin análisis comparativo. Úsala en el Paso 11 (A7) para los hallazgos de coherencia.
---

# A7 · Fuga, sobreajuste e independencia

## 1. Fuga de información (leakage)

Una variable con fuga usa información **posterior** al momento de la decisión. Señales y pruebas:

| Señal | Prueba |
|---|---|
| Variable con fecha de cálculo > fecha de observación | Comparar `fecha_variable` vs `fecha_observacion` en la base |
| AUC univariado sospechosamente alto (> 0,85 en una sola variable de comportamiento) | Calcular AUC por variable; revisar construcción |
| Variables "post-evento" (n° de gestiones de cobranza, castigo, refinanciación posterior) | Revisar diccionario y código de construcción |
| Agregados calculados sobre la ventana de desempeño | Revisar ventanas en el código (`rolling`, `groupby` con fechas) |

```python
auc_univ = {c: max(auc(y, x), 1 - auc(y, x)) for c, x in X.items()}   # auc() de metricas_validacion.py
sospechosas = {c: v for c, v in auc_univ.items() if v > 0.85}
```

## 2. Sobreajuste

| Métrica | Desarrollo | Validación OOT | Brecha | Lectura |
|---|---|---|---|---|
| Gini | 0,71 | 0,52 | 0,19 | Hallazgo metodológico (no observación menor) |

Si el equipo solo reporta métricas sobre la muestra de desarrollo: **hallazgo por ausencia de validación fuera de muestra**; cuantifica la diferencia si hay datos. El umbral de brecha aceptable debe ser del banco; si no existe, reporta la brecha con cifra y pide formalización.

## 3. Independencia de la muestra de validación

```python
traslape_clientes = len(set(dev.cliente) & set(val.cliente)) / len(set(val.cliente))
traslape_cosechas = sorted(set(dev.cosecha) & set(val.cosecha))
```

- Misma cosecha en desarrollo y validación → independencia no acreditada; cuantificar traslape.
- Validación "fuera de tiempo" (OOT) que comparte periodos con desarrollo → no es OOT.

## 4. Segmentación y celdas pequeñas

Reporta n y n° de eventos por celda. Celdas con pocos eventos producen estimadores inestables: muéstralo con el intervalo de Jeffreys por celda (ancho del IC). Si el banco no fija un mínimo, reporta cifras y pide criterio; no inventes un umbral.

## 5. Backtesting y marco propio

- Backtesting con ventana **más corta** que la declarada → hallazgo por incumplimiento del propio marco, aunque el resultado sea favorable.
- Modelo "sin cambios" en el ciclo → las actividades periódicas del estándar igual deben ejecutarse.

## 6. Cambios de metodología

Cambio en el ciclo sin análisis de impacto comparativo (versión anterior vs nueva sobre la misma población) → hallazgo. Exige la tabla: métrica · versión anterior · versión nueva · misma población (sí/no).

## 7. Overlays y escenarios macro

| Elemento | Exigir | Sin ello |
|---|---|---|
| Overlay / ajuste discrecional | Política, cuantificación, aprobación (acta) | Hallazgo **crítico** |
| Variable macro proyectada | Sustento del escenario y quién lo aprueba | Supuesto macro sin dueño → hallazgo |

## 8. Interpretabilidad

Variable con relación contraintuitiva respecto del riesgo (p. ej. a mayor mora histórica, menor PD) sin explicación → consulta abierta (vía A9) + observación de interpretabilidad.
