---
name: virf-a8-paridad-codigo-manual
description: Inventario de bloques funcionales del código (carga, validación de entrada, limpieza, transformación, cálculo, calibración, salida, publicación, control de errores), mapeo a secciones del manual en tres listas (bloques sin documentación, documentación sin bloque, bloques con parámetros distintos) y comparación parámetro por parámetro manual vs código con script, donde cualquier diferencia es No cumple con impacto cuantificado. Úsala en el Paso 12 (A8).
---

# A8 · Paridad código ↔ manual

## 1. Inventario de bloques funcionales

| Bloque | Ubicación exacta (archivo > función > líneas) | Sección del manual | Coincide | Evaluación sustentada | Fuente exacta | Acción pendiente |
|---|---|---|---|---|---|---|
| Carga | extraer.sql > líneas 1–40 | Manual > 3.2 > p.19 | Sí | | | |
| Validación de entrada | — | — | No evidenciado | Sin validaciones de entrada | | |
| Limpieza | prep.py > limpiar() > 30–70 | Manual > 3.5 > p.22 | Parcial | imputación no documentada | | |
| Transformación | … | | | | | |
| Cálculo | … | | | | | |
| Calibración | … | | | | | |
| Generación de salida | … | | | | | |
| Publicación | … | | | | | |
| Control de errores | … | | | | | |

> Para que A11 pueda rastrear cada fila al estándar, antepón a esta tabla la columna `ID VIRF` (actividad del estándar que evidencia la fila). Sin ella, el consolidador devuelve la matriz.

Produce las **tres listas**: (a) bloques sin documentación, (b) documentación sin bloque (manual describe algo que el código no hace → también hallazgo C1), (c) bloques con diferencias de parámetros.

## 2. Comparación parámetro por parámetro

1. Arma `parametros_manual.csv` desde el manual/Paso 0: `parametro,valor_manual,cita_manual,patron_codigo` (el patrón es un texto o regex para ubicarlo en el código: `corte|cutoff`).
2. Genera el inventario del código con `virf-a1-lectura-codigo-discrepancias/scripts/inventario_parametros_codigo.py` (incluido también aquí en `scripts/`).
3. Compara:

```bash
python scripts/comparar_parametros.py parametros_manual.csv parametros_codigo.csv --salida paridad.md
```

El script busca cada parámetro del manual en el inventario del código, extrae los números de la línea encontrada y marca: `Coincide`, `Difiere`, `No ubicado en código`, `Múltiples valores en código` (mismo parámetro con valores distintos en dos sitios: hallazgo por sí mismo).

## 3. Regla dura

**Cualquier diferencia entre código y manual es "No cumple", sin excepción y sin importar su magnitud aparente.** Luego cuantifica el impacto (re-ejecutar con el valor del manual y comparar outputs con `reproducir_output.py`).

Ejemplo de evaluación sustentada:
> "El código aplica un corte de score de 620 (score.py > segmentar() > línea 88) mientras el manual documenta 640 (Manual_PD.pdf > 4.3 > p.27); la diferencia reclasifica 4 128 clientes (2,7 % de la cartera) hacia el segmento de menor PD, por lo que el output del ciclo no puede considerarse concluyente hasta determinar cuál corte cuenta con aprobación."

## 4. Casos que exigen cuidado

| Caso | Tratamiento |
|---|---|
| Parámetro leído de configuración externa (tabla, JSON, YAML) | Verificar el **valor vigente en el ciclo**, no solo el mecanismo |
| Código correcto, manual desactualizado | Hallazgo en Implementación por divergencia + referencia cruzada a C1; no es observación menor |
| Dos ramas del repositorio | Validar la del pase a producción del ciclo; documentar la otra |
| Código evaluado de rama de desarrollo | Prohibido cuando el objeto es la versión productiva |
| Cambio de librería entre ciclos con efecto numérico | Exigir comparación antes/después |
| Casos límite (÷0, categoría nueva, faltante en obligatoria, volumen atípico) | Documentar qué hace el código en cada uno (línea) |

## 5. Herramienta Excel

Aplicar el mismo estándar sobre el notebook de A2 y exigir su tabla de reconciliación con tolerancia 1e-9.
