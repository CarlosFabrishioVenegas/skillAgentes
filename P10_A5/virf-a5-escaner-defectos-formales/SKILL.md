---
name: virf-a5-escaner-defectos-formales
description: Escáner automático de defectos formales que rompen la auditabilidad de manuales PDF y Word - textos por definir o pendiente o TBD, secciones vacías, ausencia de versión, fecha, autor o aprobación, marcas de borrador, anexos referenciados no entregados, figuras y tablas sin fuente, tablas sin unidad, capturas de pantalla como evidencia y duplicidad de versiones en la carpeta. Úsala en el Paso 10 (A5) antes de llenar la matriz documental.
---

# A5 · Escáner de defectos formales

```bash
python scripts/escanear_defectos_formales.py <carpeta_manuales> --entregados <carpeta_expediente> --salida defectos_formales.csv
```

## Qué detecta

| Código | Defecto | Cómo | Severidad por defecto |
|---|---|---|---|
| F01 | Texto de relleno: "por definir", "pendiente", "TBD", "TODO", "completar", "xxx", "[insertar" | regex por página | Media |
| F02 | Sección vacía: título seguido inmediatamente de otro título | secuencia de títulos | Media |
| F03 | Sin versión | no aparece `versi[oó]n\s*\d` ni `v\d+(\.\d+)` en las 3 primeras páginas | Media (Tier 3) / No cumple (Tier 1–2) |
| F04 | Sin fecha | sin fecha reconocible en las 3 primeras páginas | ídem F03 |
| F05 | Sin autor / aprobador | no aparece "elaborado por", "autor", "aprobado por", "revisado por" | Media |
| F06 | Marca de borrador | "borrador", "draft", "versión preliminar" | Alta (impide acreditar vigencia) |
| F07 | Anexo referenciado no entregado | "Anexo X" citado y sin archivo cuyo nombre contenga "anexo X" en `--entregados` | Alta |
| F08 | Figura/tabla sin fuente | "Figura/Gráfico/Tabla N" sin "Fuente:" en la misma página | Baja |
| F09 | Captura de pantalla como evidencia | página con imagen grande y < 200 caracteres de texto | Observación (no reproducible) |
| F10 | Varias versiones del mismo documento | nombres que difieren solo en versión/fecha | Media (control documental; pedir retiro de la obsoleta) |
| F11 | Control de cambios ausente | no aparece "control de cambios", "historial de versiones" | Media |

Cada fila del CSV: `archivo · pagina · codigo · defecto · evidencia (fragmento ≤ 120 caracteres) · severidad_sugerida`.

## Cómo usar el resultado

- No es el juicio: es insumo. El estado de cada actividad lo decides con la rúbrica de `virf-a5-matriz-documental`.
- Revisa los falsos positivos de F01 (p. ej. "pendiente" en "pendiente de la curva"): el CSV trae el fragmento para confirmarlo.
- F03/F04 en Tier 1–2: pasan a "No cumple" por impedir acreditar vigencia.
- F07: cada anexo faltante va a "Brechas de evidencia" con su nombre exacto.
- F09: acreditar con observación ("la captura no es reproducible").

Documentos Word: el script lee párrafos y tablas con python-docx; cita por número de párrafo (Word no tiene páginas fijas) y lo indica en la columna `pagina` como `§N`.
