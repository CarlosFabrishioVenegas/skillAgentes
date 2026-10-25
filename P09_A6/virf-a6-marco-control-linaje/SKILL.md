---
name: virf-a6-marco-control-linaje
description: Evaluación de la existencia y efectividad del marco de control de datos del modelo (definido, documentado, con umbral, con responsable, ejecutado con la periodicidad declarada, con alerta y destinatario) y verificación de linaje campo por campo (sistema, tabla, campo, responsable) contra el diccionario, con script que cruza variables del modelo vs diccionario. Úsala en el Paso 9 (A6) junto con la rúbrica de estados.
---

# A6 · Marco de control y linaje

Un modelo con datos limpios **sin marco de control documentado no cumple** el Control 2: la limpieza de hoy no garantiza la de mañana.

## 1. Los siete atributos del marco (por control del equipo)

| # | Atributo | Evidencia esperada | Si falta |
|---|---|---|---|
| M1 | Definido | Regla de negocio escrita | Control inexistente → No cumple |
| M2 | Documentado | manual_controles_datos.md / catálogo con sección | No cumple (Tier 1–2) |
| M3 | Con umbral | Valor + fecha de declaración | No verificable; si se fijó tras el resultado → hallazgo de gobierno |
| M4 | Con responsable | Rol/área nominal | Observación (crítico si Tier 1) |
| M5 | Ejecutado con la periodicidad declarada | Logs/fechas de ejecución del ciclo | "Existe pero no se ejecutó" |
| M6 | Con alerta y destinatario | Correo/ticket/tablero que avisa al incumplir | Observación de efectividad |
| M7 | Con revisión independiente | Ejecutor ≠ dueño del dato o revisión 2.ª línea | Observación de independencia (Tier 1) |

Tabla de salida auxiliar:

```markdown
| Control del equipo | M1 | M2 | M3 | M4 | M5 | M6 | M7 | Conclusión del marco | Fuente |
|---|---|---|---|---|---|---|---|---|---|
| EQ-01 Nulos ingreso | ✔ | ✔ (manual > 2.1) | ✔ 5 % (2025-03-10) | ✔ Gob. Datos | ✘ última corrida 2025-12 | ✘ | ✘ | Existe, no se ejecutó en el ciclo | … |
```

## 2. Linaje campo por campo

```bash
python scripts/cruce_linaje.py --variables variables_modelo.csv --diccionario diccionario_datos.xlsx --salida linaje.csv
```

- `variables_modelo.csv`: una columna `variable` (de A4_paso0.md > 4).
- El diccionario se lee tolerante: busca columnas con alias (`campo|variable|nombre`, `sistema|fuente|origen`, `tabla|entidad`, `responsable|owner|custodio`).
- Resultado por variable: `presente_en_diccionario`, `sistema`, `tabla`, `campo`, `responsable`, `linaje_completo` (los cuatro presentes), `faltantes`.

Lectura:
- `linaje_completo = False` en variable del modelo → hallazgo; en Tier 1–2 **crítico**.
- Variable no presente en el diccionario → No evidenciado (y hallazgo de documentación del dato).
- Coincidencia por nombre aproximado: el script la marca `coincidencia_aproximada` → confirmar, no asumir.

## 3. Población de medición

Verifica que A3 midió sobre **la misma población** que usa el modelo (mismos filtros del código). Si A3 midió la base completa y el modelo filtra, los % no son comparables → No verificable hasta re-medir sobre la población del modelo.
