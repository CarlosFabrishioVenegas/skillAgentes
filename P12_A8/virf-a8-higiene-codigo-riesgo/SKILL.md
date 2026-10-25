---
name: virf-a8-higiene-codigo-riesgo
description: Revisión de higiene del código de modelos con foco en riesgo de implementación y no en estilo - excepciones genéricas que ocultan fallas, warnings silenciados, rutas absolutas locales, credenciales embebidas, procesos aleatorios sin semilla, dependencias sin versión fijada, escritura sobre insumos, notebooks ejecutados fuera de orden, filtros que descartan registros en silencio - con escáner automático, severidades del Control 4 y registro de control de cambios. Úsala en el Paso 12 (A8).
---

# A8 · Higiene del código (riesgo, no estilo)

No opines sobre nombres de variables ni elegancia salvo que afecten trazabilidad o reproducibilidad.

## Escáner

```bash
python scripts/escanear_riesgos_codigo.py <carpeta_codigo> --salida riesgos_codigo.csv
```

| Código | Riesgo | Detección | Severidad C4 |
|---|---|---|---|
| R01 | `except:` desnudo o `except Exception: pass` | AST | Media (Alta si envuelve cálculo/carga) |
| R02 | Warnings silenciados (`warnings.filterwarnings("ignore")`, `pd.options.mode.chained_assignment=None`) | AST/regex | Media |
| R03 | Ruta absoluta local (`C:\Users\…`, `/home/…`, `Desktop`, `Escritorio`, `OneDrive`) | regex | Media; continuidad operativa si es escritorio personal |
| R04 | Credencial embebida (`password=`, `pwd=`, tokens, cadenas de conexión con usuario y clave) | regex | Alta (y reportar a seguridad; no transcribir el secreto en el informe) |
| R05 | Aleatoriedad sin semilla (`np.random.*`, `random.*`, `sample(`, `train_test_split`, modelos sklearn sin `random_state`) | AST | Alta en Tier 1–2 / Observación en Tier 3 |
| R06 | Dependencias sin versión fijada (`requirements.txt` sin `==`, ausencia de archivo de entorno) | archivo | Media (todos los tiers) |
| R07 | Escritura sobre ruta de lectura (mismo archivo en `read_*` y `to_*`) | AST | Alta |
| R08 | Notebook con `execution_count` fuera de orden o celdas sin ejecutar intercaladas | JSON | Reproducibilidad no acreditada |
| R09 | Filtros/`dropna`/`inner merge` sin conteo antes/después | AST | Revisar: posible pérdida silenciosa (crítico si se confirma) |
| R10 | Sin validaciones de entrada (no hay `assert`/`raise` en la carga) | AST | Media |

El escáner propone; tú confirmas cada hallazgo leyendo la línea. Cita `archivo > función() > línea N`.

## Pérdida silenciosa de registros (R09 confirmado)

Mide filas por etapa:

```python
conteos = {"carga": len(df0), "tras_filtro_antiguedad": len(df1), "tras_merge_buro": len(df2), "salida": len(out)}
```

Toda caída no explicada por una regla documentada → **crítico**: cuantificar registros y exposición perdidos.

## Severidad (Control 4)

| Severidad | Casos |
|---|---|
| Crítica | Parámetro divergente que altera el output; ajuste manual posterior no documentado; pérdida silenciosa de registros; output del ciclo no reproducible |
| Alta | Bloque sin documentación; sin control de cambios; semilla no fijada en Tier 1–2; credenciales embebidas; escritura sobre insumo |
| Media | Dependencias sin versión; rutas locales; validaciones de entrada ausentes |
| Baja | Código muerto; comentarios desactualizados sin efecto en el cálculo |

## Control de cambios del ciclo (bloque c)

| Cambio | Versión | Repositorio/ubicación | Aprobador | Fecha de pase a producción | Evidencia |
|---|---|---|---|---|---|

Cambio en el código sin registro de aprobación → hallazgo de implementación **y** de gobierno (referencia a A9).

## Complemento recomendado

Para análisis estático más profundo, `bandit` (seguridad Python) y `detect-secrets` (secretos) son herramientas abiertas; los skills `static-analysis` y `differential-review` del repositorio trailofbits/skills también aplican (ver guía de repositorios).
