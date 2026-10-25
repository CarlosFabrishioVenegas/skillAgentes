---
name: virf-a3e-informe-calidad-datos
description: Estructura y redacción del informe A3_informe_calidad_datos.md - resumen ejecutivo, cobertura frente a lo exigible por tier, hallazgos por control con cifra, ejemplos infractores, causa raíz, materialidad, severidad y remediación con responsable y plazo, matriz técnica anexa de 8 columnas generada desde 01_Control_de_datos.xlsx, referencias cruzadas y plan priorizado. Úsala en el Paso 7 (A3E) para redactar el entregable.
---

# A3E · Informe de calidad de datos

## 1. Generar el esqueleto desde el Excel de A3D

```bash
python scripts/matriz_8_columnas.py 01_Control_de_datos.xlsx --salida matriz_8col.md
```

Lee la hoja `Resumen`, reconcilia conteos y produce la matriz anexa de 8 columnas con las columnas que son cifra ya llenas; las de juicio (`Decisión/acción`, `Evidencia requerida`) quedan con marcador `<<completar>>` para que las redactes tú. Si la reconciliación falla en algún control, el script lo marca `DESCUADRE` y no rellena su diagnóstico.

## 2. Matriz técnica de 8 columnas (anexo; formato fijo)

| Dimensión/Regla | Estado | % Cumplimiento | ¿Existe según evidencia? | Diagnóstico con cifra | Decisión/acción | Evidencia requerida | Referencia |
|---|---|---|---|---|---|---|---|
| D1 Completitud · ingreso_declarado | Falló | 92,60 % | Sí (control EQ-01 del equipo) | 95 040 de 1 284 330 nulos (7,40 %) > umbral 5 % (manual_controles_datos.md > 2.1) | Remediar captura en canal digital; documentar regla de imputación | Base corregida + regla de imputación aprobada | 01_Control_de_datos.xlsx > Resumen > fila 7; A3_controles_calidad.py > celda 9 |

% Cumplimiento = 100 − % infractor. `¿Existe según evidencia?`: Sí (cita del control del equipo) / No (solo batería del validador).

## 3. Estructura del informe

```markdown
# Informe de calidad de datos — <Modelo> (<Código>) · Ciclo <c>
## 1. Resumen ejecutivo
Controles corridos: N (equipo n1 · validador n2 · adicionales n3). Fallaron: f. No verificables: v. No existen: e.
Hallazgos críticos: <lista con cifra>. Estado global técnico: <Conforme | Con fallos materiales | No concluyente>.
## 2. Cobertura
| Exigibles por tier (estándar) | Evaluados | Sin evaluar | Motivo |
## 3. Hallazgos por control
### H-01 · <título con cifra>
- Qué se controló: <regla> (fuente)
- Resultado: <evaluados / infractores / %> vs umbral <x> (origen)
- Ejemplos infractores: <5–10 llaves>
- Causa raíz probable: <patrón + cifra de lift>
- Materialidad: <rol de la variable, % exposición>
- Severidad: Alta/Media/Baja — <justificación>
- Estado: Falló / No se ejecutó / No existe / No verificable
- Remediación: <acción> · Responsable: <área/rol> · Plazo: <fecha o días>
## 4. Referencias cruzadas
- Metodología (P11/A7): <hallazgos que afectan target, pesos, calibración>
- Implementación (P12/A8): <filtros/imputaciones del código involucrados>
- Gobierno del dato (P13/A9): <linaje y responsables faltantes>
## 5. Conclusión y plan de remediación priorizado
| # | Acción | Control | Severidad | Responsable | Plazo |
## Anexo A · Matriz técnica de 8 columnas
## Brechas de evidencia
```

## 4. Reglas de redacción

- Cada hallazgo cita el control del notebook y la columna evaluada.
- Ejemplos de registros infractores obligatorios en cada hallazgo que falló (sin ellos el informe se rechaza).
- Sin adjetivos sin cifra: no "calidad aceptable"; sí "97,8 % de completitud frente a umbral de 95 %".
- Responsable y plazo: si no los conoces, "Responsable: a definir por el equipo dueño (consulta vía A9)". No inventes nombres.
- No emitas "Cumple/No cumple": eso es de A6 (Paso 9).
- Siempre entregas: si falta insumo, marca pendiente y pide re-ejecución en "Brechas de evidencia".
