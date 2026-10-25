---
name: virf-ad-notebook-diagnostico
description: Plantilla de notebook de diagnóstico determinista que descubre el esquema real sin asumir columnas, perfila llaves, granularidad, nulos, rangos y cobertura temporal, no modifica los datos y escribe siempre su Excel de resumen; incluye el generador de notebooks por ronda. Úsala en el Paso 3 (AD) para producir cada 00x/01x_Diagnostico.ipynb.
---

# AD · Notebook de diagnóstico

## Reglas de construcción (todas obligatorias)

1. **Descubre, no asumas.** El notebook nunca referencia una columna que no haya listado primero. Las columnas candidatas se detectan por patrón de nombre y por tipo, y el resultado de la detección se escribe en el resumen.
2. **Determinista.** Semilla fija para cualquier muestreo; orden estable (`sort_values` antes de `head`).
3. **Solo lectura.** No escribe sobre la carpeta de insumo; salida en `VIRF_SALIDA_DIR`.
4. **Siempre escribe su resumen**, aun si una sección falla (try/except por sección que registra el error en la hoja `Errores`).
5. **Corre en kernel limpio.** Sin dependencias de variables de otra sesión.
6. **Falla explícito con insumo vacío.**

## Generar los notebooks de una ronda

```bash
python scripts/generar_notebook_diagnostico.py --prefijo 00a --tema esquema --salida 00a_Diagnostico_esquema.ipynb
python scripts/generar_notebook_diagnostico.py --prefijo 01a --tema ciclo_vida --salida 01a_Diagnostico_ciclo_vida.ipynb
```

Temas incluidos: `esquema` (ronda 1), `variables` (presencia/nulos/rangos de una lista de variables del modelo), `ciclo_vida` (saldos, estados, continuidad), `reproduccion` (conteos y sumas de control vs output publicado). Puedes añadir celdas específicas a la pregunta de la ronda; respeta la estructura.

## Estructura del notebook generado

| Celda | Contenido |
|---|---|
| 1 | Metadatos: pregunta(s) Q de la ronda, fecha, versión de librerías |
| 2 | CONFIG: `VIRF_INSUMO_DIR`, `VIRF_SALIDA_DIR`, semilla, patrones de detección |
| 3 | Carga tolerante: lee todos los .csv/.parquet/.xlsx de la carpeta; registra SHA-256 de cada archivo |
| 4 | Descubrimiento de esquema: columnas, dtypes, % nulos, n únicos, ejemplos |
| 5 | Detección de llaves candidatas (combinaciones de 1–3 columnas con unicidad 100 %) |
| 6 | Detección de columnas de fecha/periodo y cobertura temporal (min, max, huecos) |
| 7 | Sección del tema (variables / ciclo de vida / reproducción) |
| 8 | Escritura de `<prefijo>_resumen.xlsx` con hojas `Esquema`, `Llaves`, `Temporal`, `<Tema>`, `Archivos`, `Errores` |

## Lectura del resumen (lo que AD cita)

Cita como `00a_resumen.xlsx > Esquema > fila N`. Cada hecho que pase a "Lo que ya sé" debe tener esa cita.

## Errores comunes

- Detectar llave por nombre (`id`) sin verificar unicidad.
- Leer el Excel con encabezado en fila 1 cuando el título ocupa las primeras filas: el generador busca la fila de encabezado por contenido (primera fila con ≥ 60 % de celdas de texto no vacías).
- Muestras aleatorias sin semilla: rompen la idempotencia.
