---
name: virf-ak-kickoff-a-pptx
description: Conversión del Markdown del kick-off (AK_kickoff_presentacion.md) a un PowerPoint de dos láminas más portada y lámina de fuentes con python-pptx, conservando citas como notas al pie, el flujo de tres cajas con flechas y la advertencia de base parcial. Úsala en el Paso 5 (AK) cuando el validador necesite la presentación lista para la reunión.
---

# AK · Del Markdown al PowerPoint

El agente produce Markdown; este skill lo convierte en `.pptx` sin perder citas.

## Uso

```bash
python scripts/kickoff_md_a_pptx.py AK_kickoff_presentacion.md --salida AK_kickoff.pptx [--plantilla plantilla_banco.pptx]
```

- Con `--plantilla`, usa los layouts del archivo del banco (título y título+contenido). Sin plantilla, genera un diseño sobrio 16:9.
- Genera 4 láminas: Portada · Alcance y Limitaciones · Flujo de datos · Fuentes y consultas abiertas.
- Las citas `(A4_paso0.md > …)` se mueven a un pie numerado [1]…[n] en cada lámina para que el cuerpo sea legible, sin perder ninguna.
- Si el Markdown trae la advertencia "Base parcial", aparece como banda superior en la portada y en la lámina 1.

## Qué espera el parser

El formato de salida definido en las instrucciones de AK:
- `## Kick-off — …` (título)
- `### Lámina 1 — Alcance y Limitaciones` con bloques `**Alcance**` y `**Limitaciones**` y viñetas `- `
- `### Lámina 2 — Flujo de datos` con la tabla de 5 columnas (`Input | → | Tratamiento | → | Usuarios`) y las tres "Notas de la caja …"
- `### Fuentes y consultas abiertas`

Si una sección falta, el script la crea con "No evidenciado" y lo avisa en consola: nunca descarta contenido en silencio.

## Revisión visual

Después de generar, convierte a imagen para revisar desbordes (texto que no cabe):

```bash
soffice --headless --convert-to pdf AK_kickoff.pptx && pdftoppm -png -r 60 AK_kickoff.pdf revision
```

Si un bloque desborda: el script ya reduce la fuente hasta 11 pt; si aun así no cabe, divide limitaciones en una lámina 1b en vez de recortar texto (los supuestos son literales).

Para diseño más elaborado, el skill oficial `pptx` de anthropics/skills cubre plantillas y layouts avanzados.
