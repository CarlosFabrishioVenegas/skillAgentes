---
name: virf-a1-extraccion-pdf-citada
description: Extracción página a página de manuales PDF/Word de un modelo bancario con cita exacta (sección y página), detección de PDF escaneado sin capa de texto, reconstrucción de tablas partidas, lectura por bloques de PDFs de más de 300 páginas y hash SHA-256. Úsala en el Paso 1 (agente A1) antes de llenar la plantilla de entendimiento.
---

# A1 · Extracción citada de manuales

Objetivo: convertir cada PDF/Word del modelo en un **corpus paginado y citable** sobre el cual se llena la plantilla `entendimiento_<codigo>.md`. Este skill no interpreta: solo localiza, transcribe y cita.

## Flujo

1. **Inventario e identidad.** Para cada archivo registra: nombre, código de inventario, versión, fecha, marca "borrador/draft". Si el código o el nombre del modelo no coincide con el indicado, **excluye** el archivo y repórtalo ("Documento de otro modelo: <archivo>, código <X>").
2. **Extracción paginada.** Ejecuta:
   ```bash
   python scripts/extraer_pdf_paginado.py <archivo.pdf> --salida corpus/<archivo>.jsonl
   ```
   Cada línea del JSONL contiene: `pagina_fisica`, `pagina_impresa` (si se detecta), `encabezado_seccion` (último título detectado), `texto`, `n_caracteres`, `tablas` (lista de tablas en filas).
3. **Detección de escaneo.** Si una página tiene < 30 caracteres de texto y contiene imágenes, el script la marca `requiere_ocr: true`. Si **todas** las páginas lo requieren: devuelve `PDF no extraíble — requiere OCR` y detén ese archivo. No inventes contenido.
4. **Numeración.** Usa la página impresa cuando el script la detecte en el pie o encabezado; si no, cita `p.N (física)`. Nunca mezcles ambas sin indicarlo.
5. **Tablas partidas.** Si una tabla termina al pie de página y la siguiente página empieza con filas sin encabezado y el mismo número de columnas, únelas y cita el rango `pp.N–M`.
6. **PDFs > 300 páginas.** Procesa por bloques de 50 páginas (`--desde`, `--hasta`) y registra en la sección 10 el rango efectivamente leído. Nunca declares cobertura total sin haberla recorrido.
7. **Word (.docx).** Convierte primero a PDF o extrae con python-docx; Word no tiene páginas fijas, así que cita por `archivo > título de sección > párrafo N` y anótalo como cita sin página.
8. **Hash.** Registra el SHA-256 de cada documento procesado (`virf-nucleo-comun/scripts/hash_evidencias.py`).

## Búsqueda de campos en el corpus

Para cada campo de la plantilla, busca con varias formulaciones (sinónimos en español bancario):

| Campo | Términos a buscar |
|---|---|
| Variable objetivo | default, incumplimiento, mora > 90, variable dependiente, target, evento |
| Ventana de desempeño | ventana, horizonte, período de observación, performance window |
| Fuentes de datos | datamart, tabla, origen, sistema fuente, DM_, TB_ |
| Frecuencia | mensual, trimestral, diario, periodicidad, frecuencia de actualización |
| Supuestos | supuesto, se asume, hipótesis, asumimos |
| Limitaciones | limitación, restricción, no aplica a, fuera de alcance, no considera |
| Calibración | calibración, tasa central, escalamiento, anclaje, central tendency |
| Outputs | resultado, salida, se publica, se reporta, se envía |

Regístrala igualmente cuando aparezca solo en el manual de usuario (cítalo y anótalo: afecta el control de Documentación) o solo en un diagrama ("solo aparece en diagrama, sin descripción textual").

## Fórmulas

Transcribe tal cual entre backticks, sin "corregir" notación. Si hay símbolos no definidos, genera consulta abierta con la lista de símbolos.

## Errores frecuentes a evitar

- Citar "Manual metodológico" sin sección ni página.
- Resumir un supuesto en vez de transcribirlo literal entre comillas.
- Tomar la primera página de una tabla partida como si fuera la tabla completa.
- Mezclar dos variantes del modelo (retail/PYME): usa columna "variante".
