---
name: virf-a3d-motor-controles
description: Motor de ejecución de la batería de calidad de datos en tres bloques (controles del equipo traducidos fielmente, batería del validador, controles adicionales), con registro de controles desde reglas de negocio en lenguaje natural, CONFIG con origen de cada umbral, autocomprobación de conteos y escritura de 01_Control_de_datos.xlsx que incluye lo que está bien. Úsala en el Paso 6 (A3D) para armar y correr A3_controles_calidad.py.
---

# A3D · Motor de controles

## Principio

Los controles nacen de **reglas de negocio en lenguaje natural** ("no debe existir VaR negativo") y se traducen a código (`base[base["var"] < 0]`). Cada control conserva la regla textual que lo originó y su fuente.

## Estructura del script (`scripts/motor_controles.py` + tu archivo de controles)

```python
from motor_controles import Bateria, umbral
B = Bateria(modelo="PD Retail", codigo="MOD-0412", base=base, llave=["cod_operacion", "fecha_corte"])

# Bloque 1 — Controles del equipo (traducción fiel; si el control tiene un defecto, se reporta, no se corrige)
B.control(bloque=1, id="EQ-01", dimension="D1 Completitud",
          regla="El ingreso declarado no puede estar vacío",
          fuente_regla="manual_controles_datos.md > 2.1",
          umbral=umbral(0.05, "manual_controles_datos.md > 2.1 (máx. 5 % nulos)"),
          infractores=lambda d: d["ingreso_declarado"].isna(),
          columnas=["ingreso_declarado"])

# Bloque 2 — Batería del validador (nueve dimensiones + ciclo de vida)
B.control(bloque=2, id="VA-D2-01", dimension="D2 Unicidad", regla="La llave operación-periodo es única",
          fuente_regla="Diccionario > llave", umbral=umbral(0, "definición de llave"),
          infractores=lambda d: d.duplicated(["cod_operacion", "fecha_corte"], keep=False),
          columnas=["cod_operacion", "fecha_corte"])
B.desde_regla(bloque=2, id="VA-CV-01", dimension="Ciclo de vida", resultado=rcv.saldo_resucita(base, ...),
              fuente_regla="[SUPUESTO] regla del validador", umbral=umbral(0, None))

# Bloque 3 — Controles adicionales propuestos
B.control(bloque=3, id="AD-01", ...)

B.ejecutar()
B.autocomprobar()            # infractores + conformes == evaluados, por control
B.escribir_excel("salida/01_Control_de_datos.xlsx")
B.escribir_hallazgos_md("salida/A3_hallazgos.md")
```

## Estados que asigna el motor (técnicos, no juicio de negocio)

| Situación | estado_tecnico |
|---|---|
| Columna no existe | `No verificable — columna inexistente` |
| Umbral `[SUPUESTO]` o sin origen | `No verificable — umbral no declarado` |
| % infractor ≤ umbral | `Dentro de umbral` |
| % infractor > umbral | `Fuera de umbral` |
| Error de ejecución | `Error de ejecución — <mensaje>` |
| Control del equipo no entregado | fila `No existe según evidencia` |

El juicio (Cumple/No cumple) lo emite A6. A3D no usa esas palabras.

## Excel 01_Control_de_datos.xlsx

Hojas:
- `Resumen`: una fila por control (**incluye los que están dentro de umbral**): bloque, id, dimensión, regla, fuente_regla, columnas, n_evaluado, n_infractor, n_conforme, %, umbral, origen_umbral, estado_tecnico, muestra_llaves.
- `Muestras`: hasta 10 llaves por control infractor.
- `Reproducibilidad`: fecha, hash de la base, versión de Python/pandas, semilla, n° de controles por bloque.
- `Autocomprobacion`: control | evaluados | infractores + conformes | ¿cuadra?
- `Brechas`: insumos faltantes (documento/código del equipo, diccionario, fuente de conciliación).

## Autocomprobaciones obligatorias

1. `infractores + conformes == evaluados` en cada control (descuadre → error visible).
2. Kernel reiniciado: ver `virf-a2-reconciliacion-pruebas/scripts/pruebas_admisibilidad.py`.
3. Insumo vacío falla: `Bateria(base=vacía)` lanza `ValueError("Insumo vacío…")`.

## Si falta el documento/código del equipo

Se entrega igual la batería del validador; el bloque 1 aparece con una fila "Controles del equipo no entregados" y la brecha se registra. Nunca se omite el bloque 1 cuando sí se entregó.
