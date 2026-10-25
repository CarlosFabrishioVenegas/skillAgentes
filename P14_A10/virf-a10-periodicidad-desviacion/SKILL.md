---
name: virf-a10-periodicidad-desviacion
description: Cálculo del cumplimiento de la periodicidad comprometida en el acta - fechas esperadas de envío y sustento según frecuencia mensual, trimestral, semestral o anual, días de desviación por periodo, periodos sin uso (incumplimiento parcial), envíos tardíos antes del cierre de la validación - con script que cruza la evidencia de envíos contra el calendario esperado. Úsala en el Paso 14 (A10) para el bloque b del entregable.
---

# A10 · Periodicidad y días de desviación

La desviación se reporta **como cifra** (días), nunca como "a tiempo"/"tarde" sin número.

## 1. Insumo

`evidencias_uso.csv` (una fila por envío o sustento):

```text
output,tipo,fecha,cita
Curva PD,envio,2026-01-05,riesgos.retail@ > Curva PD dic-25 > 2026-01-05
Curva PD,comite,2026-01-20,Comité Provisiones > acta 01 > acuerdo 3
Curva PD,envio,2026-04-08,...
```

## 2. Ejecutar

```bash
python scripts/periodicidad_uso.py evidencias_uso.csv --periodicidad trimestral --desde 2025-10-01 --hasta 2026-09-30 \
    --plazo-dias 10 --tipo envio --salida periodicidad.md
```

- `--periodicidad`: mensual | trimestral | semestral | anual (de [G08]).
- `--plazo-dias`: días tras el cierre del periodo en que debe enviarse (del acta o manual; si no consta, `[SUPUESTO]` y se rotula).
- Para cada periodo del rango calcula: fecha límite, primera evidencia del periodo, días de desviación (positivo = atraso), estado.

## 3. Lectura

| Situación | Tratamiento |
|---|---|
| Evidencia dentro del plazo | En plazo (0 días o negativo) |
| Evidencia tardía | Uso satisfactorio con observación por oportunidad; reportar días |
| Periodo sin evidencia | **Incumplimiento parcial**: cuantificar periodos sin uso; no es cumplimiento |
| Enviado tras el plazo pero antes del cierre de la validación | Se acredita con observación, indicando días de atraso |
| Equipo anuncia que retomará el uso | Registrar compromiso con fecha; no altera el estado del ciclo evaluado |

## 4. Bloque (b) del entregable

```markdown
| Output | Periodo | Fecha límite | Evidencia | Fecha | Días de desviación | Estado |
|---|---|---|---|---|---|---|
| Curva PD | 2026T2 | 2026-07-10 | riesgos.retail@ > … | 2026-07-03 | −7 | En plazo |
| Curva PD | 2026T3 | 2026-10-10 | — | — | — | Sin uso en el periodo |
**Periodos evaluados:** 4 · **en plazo:** 2 · **tardíos:** 1 (máx. 23 días) · **sin uso:** 1
```

Repetir con `--tipo comite` cuando la periodicidad comprometida exige sustento en foro.
