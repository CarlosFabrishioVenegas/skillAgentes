---
name: virf-a8-precondicion-reproduccion
description: Verificación de la precondición obligatoria del Control 4 (log de ejecución del ciclo, outputs con fecha y versión, corrida sin errores) y reproducción cifra a cifra de outputs publicados con los seis elementos de evidencia citable (comando, fecha, versión del código, hash del insumo, valor obtenido, valor publicado), con script de comparación por llave y tolerancia. Úsala en el Paso 12 (agente A8) antes de cualquier otro análisis de implementación.
---

# A8 · Precondición y reproducción de outputs

## 1. Precondición (si no se cumple: detenerse)

| # | Requisito | Evidencia | ✔/✘ |
|---|---|---|---|
| P1 | Log de ejecución del ciclo | archivo de log con fecha del ciclo | |
| P2 | Outputs generados con fecha y versión | nombre/metadata del output | |
| P3 | Corrida sin errores | log sin ERROR/Traceback; código de salida 0 | |
| P4 | Versión del código que corrió identificada | tag/commit/hash del script | |

Si falta cualquiera:

```markdown
**Precondición no satisfecha.** Falta:
1. Log de ejecución del ciclo 2026-06 (se esperaba en /expediente/logs/)
2. …
Puedo adelantar únicamente el inventario de bloques y el mapeo documental; los estados quedan en suspenso.
```

Corrida en la máquina local del equipo: aceptable solo con log + hash de insumos + versión; si no, "No verificable".

## 2. Reproducción

Ejecuta el código productivo (o el notebook de A2) en kernel limpio sobre los insumos del ciclo y compara con lo publicado:

```bash
python scripts/reproducir_output.py --publicado output_publicado.xlsx --reproducido output_reproducido.csv \
    --llave cod_cliente --columnas pd_12m,segmento --tol-rel 1e-6 --salida reproduccion.md
```

El script reporta: filas solo en publicado, filas solo en reproducido, por columna n° de diferencias, máxima diferencia absoluta y relativa, y totales de control (suma/promedio) de cada columna numérica. Para categorías (segmento) cuenta discrepancias.

Tolerancia: por defecto 1e-6 relativa en outputs de modelo (A2 usa 1e-9 para equivalencia Excel↔notebook). Documenta la tolerancia usada; no la ajustes para forzar coincidencia.

## 3. Los seis elementos de una reproducción citable

```markdown
| Elemento | Valor |
|---|---|
| Comando o celda ejecutada | `python run_pd.py --corte 2026-06-30` |
| Fecha de ejecución | 2026-10-17 10:42 |
| Versión del código | commit a1b2c3d (tag v3.2) |
| Hash del insumo | sha256: 7f3e… (base_2026Q2.parquet) |
| Valor obtenido | PD media 3,14 % · 1 284 330 filas |
| Valor publicado | PD media 3,14 % (Tablero Riesgos > 2026-07-03) |
```

Sin los seis → la reproducción no es citable y el control **no puede cerrarse como Cumple**, aunque coincidan las cifras.

## 4. Interpretación

| Resultado | Lectura |
|---|---|
| Coincide dentro de tolerancia | Reproducción acreditada |
| Difiere y el código tiene parámetro distinto al manual | Ver paridad de parámetros; cuantificar impacto |
| Difiere sin causa en el código | Posible ajuste manual posterior → **hallazgo crítico**: exigir evidencia y aprobación del ajuste, documentar magnitud (compartido con A10) |
| Filas perdidas entre etapas | Pérdida silenciosa de registros → **crítico**; cuantificar por etapa |
| Orquestador con reintentos | Verificar si el output final viene de una corrida parcial |

Tier 1: reproducción obligatoria. Tier 2–3: por muestreo documentado (indica qué outputs y por qué).
