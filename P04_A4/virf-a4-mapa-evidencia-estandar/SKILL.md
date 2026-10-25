---
name: virf-a4-mapa-evidencia-estandar
description: Lectura tolerante de Estandares_VIRF.xlsx filtrado por tier y periodicidad (detección automática de hojas, encabezados por contenido, alias de columnas, celdas combinadas) y construcción del mapa de evidencia por control C1-C6 con rutas de archivo exactas y evidencia faltante. Úsala en el Paso 4 (A4) para la sección 11 del Paso 0, y en A5-A11 cada vez que se necesite la lista de actividades exigibles por tier.
---

# A4 · Mapa de evidencia contra el estándar VIRF

## 1. Leer el estándar (el parser se adapta al estándar, no al revés)

```bash
python scripts/filtrar_estandar_virf.py Estandares_VIRF.xlsx --tier 2 --periodicidad periodica --salida actividades_tier2.csv
```

El script:
- Recorre todas las hojas y busca la fila de encabezado por contenido (alias abajo), no por posición.
- Rellena hacia abajo celdas combinadas (ámbito, control).
- Normaliza el tier ("Tier 1", "T1", "1", "Alto") y filtra las actividades aplicables al tier pedido. Si la columna de tier contiene marcas por columna (p. ej. columnas `T1`, `T2`, `T3` con "X"), también lo detecta.
- Conserva erratas del estándar tal cual (no corrige contenido institucional).
- Emite un CSV con: `id_virf, ambito, control, actividad, tier, periodicidad, hoja, fila`.

Alias reconocidos (ampliables en `ALIAS` del script):

| Campo | Alias |
|---|---|
| id_virf | id, código, cod, n°, nro, id actividad |
| ambito | ámbito, dimensión, control, pilar, componente |
| actividad | actividad, descripción, prueba, requisito, criterio |
| tier | tier, nivel, criticidad, tiering |
| periodicidad | periodicidad, tipo de validación, frecuencia |

Si el script no logra mapear una columna, lo dice y lista los encabezados encontrados: corrige el alias, no el Excel.

## 2. Construir el mapa (sección 11)

Para cada control C1–C6:

```markdown
| Control | Actividades del estándar aplicables al tier | Evidencia disponible (ruta exacta) | Evidencia faltante | Fuente exacta |
|---|---|---|---|---|
| C1 Documentación | DOC-01, DOC-02, DOC-05 (3) | /expediente/manuales/Manual_Metodologico_v3.pdf | Manual de seguimiento | Estandares_VIRF.xlsx > Documentación > filas 4–9 |
| C2 Calidad de datos | DAT-01…DAT-09 (9) | /expediente/datos/base_2026Q2.parquet; /expediente/controles/ | Diccionario de datos; responsable por campo | ... |
| C3 Metodología | ... | ... | ... | ... |
| C4 Implementación | ... | /expediente/codigo/ (Python, corre) | log de ejecución del ciclo | ... |
| C5 Gobierno | ... | /expediente/acta/Acta_MOD-0412.docx | inventario de modelos | ... |
| C6 Usos | ... | — | correos de envío; actas de comité | ... |
```

Reglas:
- Rutas **exactas** (carpeta + archivo), nunca "en la carpeta del equipo".
- Un control sin evidencia asignada es el **primer hallazgo del ciclo**: va a "Brechas de evidencia" con solicitud de re-entrega.
- Lista también las actividades por ID, no solo el conteo: A5–A10 usan esta lista como número de filas de sus matrices.

## 3. Evidencia típica esperada por control (checklist de búsqueda)

| Control | Evidencia típica |
|---|---|
| C1 | Manual metodológico, de usuario, de seguimiento, anexos, control de versiones, informe de validación anterior |
| C2 | Base de datos (previa a depuración), diccionario, catálogo de controles del equipo, linaje, responsables por campo |
| C3 | Carpeta papers/, resultados de pruebas (discriminación, calibración, estabilidad, backtesting), umbrales de aceptación |
| C4 | Código productivo, log de ejecución del ciclo, outputs con fecha y versión, registro de pase a producción |
| C5 | Acta del modelo (12 campos), inventario, criterios de tiering, registro de cambios del acta |
| C6 | Correos de envío y acuses, actas de comité con acuerdo, evidencia de publicación y consumo |

## 4. Tiering y periodicidad (sección 12)

Transcribe el tier y la periodicidad del acta con su cita y la **base de su determinación** (criterio de materialidad, exposición, complejidad). Si la base no consta: "No evidenciado" + consulta (A9 recalculará el tiering).
