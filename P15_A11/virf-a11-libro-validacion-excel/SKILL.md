---
name: virf-a11-libro-validacion-excel
description: Construcción del libro final Validacion_codigo_ciclo.xlsx con las siete hojas obligatorias (Resumen, Controles, Pruebas, Evidencia, Brechas, Plan de acción, Conclusión) más la hoja Observaciones del entregable, enlaces control-prueba-evidencia, regla de que todo control cuantitativo tenga su prueba, formato y modo alternativo en tablas Markdown pegables cuando el entorno no genera binarios (Copilot Studio). Úsala en el Paso 15 (A11) para el entregable de cierre.
---

# A11 · Libro de validación

## 1. Generar el libro

```bash
python scripts/construir_libro_validacion.py --codigo MOD-0412 --ciclo 2026 \
    --consolidado consolidado.csv --pruebas pruebas_*.csv --evidencias evidencias_hash.csv \
    --plan plan_accion.csv --conclusion conclusion.md --salida Validacion_MOD-0412_2026.xlsx [--markdown]
```

Insumos:
| Insumo | Viene de |
|---|---|
| consolidado.csv | `consolidar_controles.py` (+ columnas severidad, accion, responsable, fecha que completas) |
| pruebas_*.csv | A2 (`pruebas_admisibilidad.py`, reconciliación), A3D (Resumen del Excel de controles), A7 (`metricas_validacion.py`), A8 (`reproducir_output.py`) normalizados al formato HOJA 3 |
| evidencias_hash.csv | `hash_evidencias.py` (núcleo común) + columna `controles` |
| plan_accion.csv | acción, responsable, fecha, control_origen, severidad |
| conclusion.md | ≤ 12 líneas (skill `virf-a11-conclusion-plan-accion`) |

`--markdown` emite además cada hoja como tabla bajo `=== HOJA N: <nombre> ===` con la nota inicial "Copiar cada bloque HOJA N a una pestaña homónima del libro Validacion_<codigo>.xlsx" (modo Copilot Studio).

## 2. Hojas y columnas

| Hoja | Columnas |
|---|---|
| 1 Resumen | veredicto global · semáforo por control C1–C6 · cobertura por control y global |
| 2 Controles | ID VIRF · Ámbito · Actividad · Estado · Resultado · Evaluación sustentada · Fuente exacta · Severidad · Acción pendiente · Responsable · Fecha comprometida · **ID prueba(s)** · **Evidencia(s)** |
| 3 Pruebas | ID prueba · Control asociado · Descripción · Insumo/dataset · Resultado esperado · Resultado obtenido · PASA/FALLA · Umbral y su fuente · Script o celda · Fuente exacta |
| 4 Evidencia | Archivo · Tipo · Hash SHA-256 · Fecha · Control(es) que sustenta |
| 5 Brechas | Ítem · Control · Estado · Evidencia faltante · Impacto · Acción de subsanación |
| 6 Plan de acción | Acción · Responsable · Fecha · Control de origen · Severidad (ordenado por fecha) |
| 7 Conclusión | conclusión (≤ 12 líneas) + firmas validador y revisor |
| Observaciones | Ámbito · Riesgo · Sustentación · Observaciones · Recomendaciones · Responsable/Fecha |

> El marco define siete hojas en las instrucciones de A11 y menciona además una hoja «Observaciones» en el entregable; el script genera ambas para no perder ninguna. Si el banco decide unificar, basta con omitir una.

## 3. Reglas que el script verifica

- Toda fila cuantitativa de la HOJA 2 con estado "Cumple" debe tener al menos un ID de prueba existente en la HOJA 3; si no, el script la marca en rojo y lista el incumplimiento (no puede cerrarse como Cumple).
- Ninguna fila con fuente vacía.
- Brechas = todas las filas "No evidenciado"/"No verificable" de la HOJA 2.
- Veredicto: aplica las reglas de conclusión (ver skill de conclusión); si cobertura < 100 % → "Validación incompleta".
- Plan de acción con responsable y fecha en todas las filas (vacíos se marcan).

## 4. Formato

Encabezados con relleno, filtros, columnas ajustadas, estados coloreados (Cumple verde, Cumple con observación ámbar, No cumple rojo, No evidenciado/No verificable gris), paneles inmovilizados. Para formatos avanzados (gráficos, validaciones de datos) el skill oficial `xlsx` de anthropics/skills complementa.
