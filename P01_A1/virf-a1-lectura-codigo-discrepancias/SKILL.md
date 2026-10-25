---
name: virf-a1-lectura-codigo-discrepancias
description: Lectura del código productivo de un modelo (.py, .sql, .ipynb) para extraer parámetros, filtros, cortes, pesos e imputaciones con cita archivo-función-línea, y registro de discrepancias documentación-código y manual-acta como consultas abiertas respondibles. Úsala en el Paso 1 (A1) y como apoyo del Paso 0 (A4) cuando el entendimiento debe medir el código además de los manuales.
---

# A1 · Lectura de código y registro de discrepancias

El código es fuente de entendimiento de **primer orden**: lo que corre es lo que se valida. Este skill extrae del código los mismos elementos que pide la plantilla y los contrasta con los manuales.

## 1. Inventario automático de parámetros

```bash
python scripts/inventario_parametros_codigo.py <carpeta_codigo> --salida parametros_codigo.csv
```

Recorre `.py`, `.ipynb` (celdas de código) y `.sql` y lista, con archivo, función y línea:
- Literales numéricos asignados o comparados (`corte = 640`, `df[df.score >= 620]`, `WHERE dias_mora > 90`).
- Llamadas a `fillna`, `replace`, `clip`, `dropna`, `drop_duplicates`, `merge`, `query`, `np.where`.
- Lectura de tablas/archivos (`read_sql`, `read_csv`, `FROM schema.tabla`).
- Semillas (`random_state`, `np.random.seed`).

El inventario es insumo: no lo pegues completo en el .md; usa las filas que corresponden a parámetros del modelo.

## 2. Qué buscar y dónde se registra

| Elemento | En el código | En el .md |
|---|---|---|
| Fuentes | `FROM`, `read_sql`, rutas | Sección 2, columna Origen |
| Filtros de población | `WHERE`, `query`, máscaras | Sección 3 |
| Imputaciones | `fillna`, `COALESCE` | Sección 3 (registrar valor exacto) |
| Cortes y umbrales | comparaciones con literales | Secciones 3–4 |
| Pesos / coeficientes | listas, dicts, `coef_` cargados | Sección 3 |
| Calibración | tasa central, factores | Sección 4 |
| Salidas | `to_csv`, `to_excel`, `INSERT INTO` | Sección 5 |

## 3. Tabla de discrepancias

Cada vez que el manual y el código (o el manual y el acta) difieran:

```markdown
| N° | Elemento | Qué dice el manual (cita) | Qué hace el código (cita) | Tipo | Consulta |
|---|---|---|---|---|---|
| 3 | Corte de score | 640 (Manual_PD.pdf > 4.3 > p.27) | 620 (scoring.py > segmentar() > línea 88) | Documentación↔código | ¿Cuál de los dos cortes está aprobado para producción: 640 o 620? |
```

Tipos válidos: `Documentación↔código`, `Manual↔acta`, `Manual metodológico↔manual de usuario`, `Versión`, `Nombre de variable`.

No decidas cuál vale. No evalúes impacto (eso es de A8/A7). Solo registra con doble cita.

## 4. Redacción de consultas abiertas

Una consulta válida:
- Es respondible con sí, no o un dato.
- Cita la evidencia que la origina.
- Pregunta una sola cosa.

| Mal | Bien |
|---|---|
| ¿Pueden explicar la segmentación? | ¿El corte vigente de segmentación es 620 o 640? |
| ¿Los datos son de calidad? | ¿Existe una regla documentada para imputar `ingreso_declarado` con la mediana? (sí/no + documento) |

## 5. Casos borde

- Notebook con salidas guardadas: el valor en la salida no prueba el valor vigente; cita la línea de código, no la salida.
- Parámetro leído desde config externa (JSON/YAML/tabla): registra la ruta y el valor del archivo entregado, y anota "valor externo, verificar vigencia en el ciclo".
- SQL dinámico con concatenación: transcribe la plantilla y marca "parámetros resueltos en tiempo de ejecución".
- Código de una rama distinta a la productiva: no lo uses como fuente; regístralo y pide la versión productiva.
