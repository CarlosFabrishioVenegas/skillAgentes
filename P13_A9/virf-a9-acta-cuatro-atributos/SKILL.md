---
name: virf-a9-acta-cuatro-atributos
description: Revisión campo por campo del acta del modelo (campos G01 a G12) con cuatro atributos - presente, legible, vigente y coherente con la evidencia técnica de C1 a C4 -, contraste de cada campo con su contraparte técnica, consistencia acta vs inventario, vigencia de la aprobación, roles y segregación de funciones, registro de cambios del acta y rúbrica de coherencia. Úsala en el Paso 13 (agente A9).
---

# A9 · Acta del modelo: cuatro atributos por campo

Criterio: no la existencia formal del acta, sino su **coherencia con la realidad técnica** evidenciada por C1–C4. Un acta completa pero desalineada es hallazgo de severidad alta.

## 1. Los doce campos

El significado exacto de cada campo `[SUPUESTO-G01]…[SUPUESTO-G12]` lo fija la plantilla de acta del banco: cárgalo en `campos_acta.csv` (`campo,descripcion,contraparte_tecnica`). Las instrucciones del marco ya fijan estos cinco:

| Campo | Contenido | Contraparte técnica a contrastar |
|---|---|---|
| G03 | Tier asignado | Recálculo de tiering (skill `virf-a9-recalculo-tiering`) |
| G04 | Responsable del equipo dueño / destinatario de consultas | Organigrama vigente; autoría del código |
| G06 | Área usuaria | Evidencia de uso de A10 |
| G08 | Periodicidad comprometida | Fechas reales de seguimiento y de envío (A10) |
| G10 | Uso declarado | Uso observado (A10) |

Para el resto, usa la contraparte natural: versión ↔ código y manual (C1, C4); desarrollador ↔ autoría del código; limitaciones ↔ hallazgos de Metodología (C3); fecha de aprobación ↔ periodicidad (G08).

## 2. Matriz de salida

```markdown
| Campo del acta | Valor registrado | ¿Completo y vigente? | Contraste con evidencia técnica | Estado | Fuente exacta | Consulta o acción pendiente |
|---|---|---|---|---|---|---|
| G08 Periodicidad | Trimestral | Completo · vigente | Envíos 2026: 03-ene, 05-abr, — (jul sin envío) (A10_control_usos.md > b) | No cumple | Acta_MOD-0412.docx > G08 > p.1; A10 > tabla b | Consulta 05 |
```

> Para que A11 pueda rastrear cada fila al estándar, antepón a esta tabla la columna `ID VIRF` (actividad del estándar que evidencia la fila). Sin ella, el consolidador devuelve la matriz.

Cada fila cita el acta **y** la evidencia contrastada. Una fila que solo cita el acta no acredita coherencia.

## 3. Rúbrica de coherencia

| Estado | Criterio |
|---|---|
| Cumple | Presente, vigente y coherente con C1–C4 |
| Cumple con observación | Imprecisión que no altera la gestión (nombre de área desactualizado por reorganización ya formalizada) |
| No cumple | Desalineado con la evidencia técnica; aprobación vencida; tiering incorrecto según criterios vigentes |
| No verificable | Consulta enviada y no respondida en plazo |
| No evidenciado | Campo vacío (nunca "No aplica" salvo regla del estándar citada) |

## 4. Verificaciones transversales

| Verificación | Hallazgo si falla |
|---|---|
| Aprobación vigente frente a G08 | Aprobación vencida → No cumple |
| Acta ↔ inventario de modelos | Modelo con acta y fuera del inventario (o viceversa) → **crítico** |
| Estado del inventario vs uso real | "En revisión" pero en uso productivo → **crítico** |
| Firma del acta con facultad para el tier | Aprobación no válida aunque el contenido sea correcto |
| Registro de cambios del acta | Campo modificado sin traza → hallazgo |
| Propietario vigente | Ya no está en el banco o cambió de área → modelo sin responsable efectivo |
| Dos propietarios en documentos distintos | Consulta inmediata (bloquea rendición de cuentas) |
| Acta actualizada durante la validación | Validar sobre la versión vigente al inicio; reportar el cambio con fechas |

## 5. Roles y segregación (bloque c)

```markdown
| Rol | Persona/área | Fuente | ¿Independiente de…? |
|---|---|---|---|
| Desarrollador | | | |
| Propietario | | | |
| Usuario | | | |
| Validador | | | Desarrollador y propietario (exigido por el estándar) |
```

Misma persona/área en roles que el estándar exige independientes → hallazgo.

## Prohibido

Completar campos con información de otros documentos (si el acta no lo dice, el acta está incompleta); resolver ambigüedades por inferencia; omitir el recálculo de tiering "por evidente".
