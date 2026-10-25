---
name: virf-a3e-materialidad-causa-raiz
description: Evaluación de materialidad de fallos de calidad de datos por su impacto en el output del modelo (no por frecuencia), asignación de severidad alta, media o baja justificada, análisis de causa raíz a partir de patrones en registros infractores (por periodo, fuente, segmento, valor centinela) y verificación de linaje. Úsala en el Paso 7 (A3E) después de clasificar los controles.
---

# A3E · Materialidad, causa raíz y severidad

## 1. Materialidad: impacto en el output, no frecuencia

Para cada control que falló, responde con cifras:

| Pregunta | Fuente |
|---|---|
| ¿La columna es variable del modelo, filtro de población, llave o informativa? | A4_paso0.md > 4, 5 |
| Si es variable: ¿qué peso/importancia tiene? | Manual metodológico; coeficientes en código |
| ¿Qué % de la exposición/saldo (no solo de filas) afecta? | Base: `infractores[saldo].sum() / base[saldo].sum()` |
| ¿El defecto cambia la población del modelo (entra/sale gente)? | Filtros del código |

Matriz de materialidad:

| Rol de la columna | % exposición afectada | Materialidad |
|---|---|---|
| Variable de alto peso / target / llave / filtro | > 1 % | Alta |
| Variable de alto peso / target / llave / filtro | ≤ 1 % | Media |
| Variable de bajo peso | > 5 % | Media |
| Variable de bajo peso | ≤ 5 % | Baja |
| Informativa (no usada por el modelo) | cualquiera | Baja (documentar que no afecta el output) |

> Los cortes 1 % y 5 % son referenciales `[SUPUESTO]`: si el banco tiene política de materialidad, úsala y cítala.

## 2. Severidad (justificada en la materialidad)

| Severidad | Criterio |
|---|---|
| Alta | Materialidad alta, o defecto en llave/target, o linaje ausente en Tier 1–2 |
| Media | Materialidad media, o control inexistente en variable usada |
| Baja | Materialidad baja, o defecto formal en variable informativa |

Redacción: "Severidad alta: `dias_mora` define el target; 0,8 % de operaciones con saldo 3,2 % de la cartera tienen mora negativa."

## 3. Causa raíz a partir de los infractores

Analiza las llaves muestra y, si tienes la base, perfila los infractores contra los conformes:

```bash
python scripts/perfil_infractores.py base.parquet --llave cod_operacion,fecha_corte --infractores muestra_VA-D1-03.csv --dims fecha_corte,canal,producto,sistema_origen --salida perfil_VA-D1-03.csv
```

El script calcula, para cada dimensión, la tasa de infractores por categoría y el **lift** (tasa en la categoría / tasa global). Lift alto concentrado = pista de causa raíz.

| Patrón observado | Causa raíz probable |
|---|---|
| Concentrado en uno o pocos periodos | Cambio de proceso/carga en esa fecha; reproceso histórico |
| Concentrado en un sistema origen | Falla de interfaz o mapeo de esa fuente |
| Concentrado en un producto/canal | Regla de captura distinta; campo no obligatorio en ese canal |
| Valores centinela (0, -1, 9999, 1900-01-01) | Imputación por defecto en el ETL |
| Duplicados con mismo contenido | Doble carga / join que multiplica filas |
| Duplicados con contenido distinto | Versionado de registro sin llave de vigencia |
| Valores en otra escala (×100, ×1000) | Cambio de unidad (porcentaje vs fracción, miles) |

Reporta la causa como **probable** con la cifra que la sustenta; la causa confirmada requiere respuesta del equipo (consulta vía A9).

## 4. Linaje

Para cada campo implicado en un fallo: sistema → tabla → campo → responsable. Si falta cualquiera: hallazgo de gobierno del dato (y en Tier 1–2, crítico en A6). Cita el diccionario o "No evidenciado".
