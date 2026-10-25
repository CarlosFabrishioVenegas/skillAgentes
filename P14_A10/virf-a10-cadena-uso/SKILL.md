---
name: virf-a10-cadena-uso
description: Reconstrucción de la cadena de uso por cada output del modelo (generación, envío, recepción acusada, sustento en foro, decisión o acción) identificando el eslabón roto, verificación de correspondencia del uso real con el uso declarado del acta, calidad del sustento en comité, trazabilidad de la cifra publicada vs la generada, formatos de cita de correo, comité y publicación, y rúbrica de acreditación de uso. Úsala en el Paso 14 (agente A10).
---

# A10 · Cadena de uso por output

Este control decide si el modelo tiene razón de existir. Cada output se evalúa **por separado**: la curva puede tener uso acreditado y la tabla de sensibilidades no.

## 1. Cadena por output

```
Generación → Envío → Recepción acusada → Sustento en foro → Decisión/acción registrada
```

| Output | Generación | Envío | Acuse | Sustento en foro | Decisión | Eslabón roto |
|---|---|---|---|---|---|---|
| Curva PD | log 2026-07-01 | riesgos.retail@ > "Curva PD jun-26" > 2026-07-03 | provisiones@ > "RE: Curva…" > 2026-07-03 | Comité Provisiones > acta 07 > acuerdo 2 | Aprobada para provisión jul-26 | — |
| Tabla sensibilidades | log 2026-07-01 | — | — | — | — | **Envío** |

Formatos de cita:
- Correo: `remitente > asunto > fecha`
- Comité: `comité > acta N > acuerdo N`
- Publicación: `ruta o tablero > fecha de actualización > evidencia de consumo`

La cita debe permitir a un tercero recuperar la evidencia sin pedirla al equipo.

## 2. Qué acredita y qué no

| Evidencia | ¿Acredita? |
|---|---|
| Output generado (existe el archivo) | No acredita uso |
| Correo interno entre miembros del equipo desarrollador | No |
| Correo al área usuaria sin acuse | Parcial (Cumple con observación en Tier 1–2) |
| Publicación en tablero sin estadística de accesos | No; pedir accesos o confirmación del área usuaria |
| Lámina en presentación sin acuerdo en acta | No basta: debe constar acuerdo, decisión o toma de conocimiento |
| Comité que difirió el punto | No acredita; citar el acta del diferimiento |
| Reporte regulatorio remitido (modelo de uso regulatorio) | Sí: citar envío y periodo |
| Consumo por modelo aguas abajo (código de inventario) | Sí, con evidencia de consumo |
| Archivo enviado vacío o que no abre | No acredita entrega efectiva |
| Área usuaria declara no usar el output aunque lo recibe | No acreditado; documentar la declaración con su fuente |

## 3. Correspondencia con el uso declarado ([G10]) y área ([G06])

- Uso real distinto al autorizado → hallazgo aunque haya mucho uso (empleo fuera de alcance).
- Uso de **mayor impacto** que el autorizado (informativo usado para decidir límites) → **crítico**, compartido con Gobierno.
- Uso por un área distinta a G06 → documentar uso real + hallazgo de gobierno por desalineación con el acta.

## 4. Trazabilidad de la cifra

Compara la cifra enviada/publicada con la generada por la herramienta (usa la reproducción de A8). Si difiere: ajuste manual no documentado → **crítico**, compartido con Implementación.

## 5. Rúbrica

| Estado | Criterio |
|---|---|
| Uso satisfactorio | Cadena completa, dentro de la periodicidad |
| Uso satisfactorio con observación | Cadena completa con desvío de plazo, o sin acuse en tiers que lo exigen |
| Uso no satisfactorio | Cadena rota en cualquier eslabón sin justificación documentada |
| Sin uso | Ni envío ni sustento → **recomendación obligatoria de retiro** |

## 6. Formato de salida

```markdown
| Output | Destinatario | Evidencia de envío | Evidencia de sustento en foro | ¿Uso satisfactorio? | Evaluación sustentada | Fuente exacta | Acción pendiente |
```

> Para que A11 pueda rastrear cada fila al estándar, antepón a esta tabla la columna `ID VIRF` (actividad del estándar que evidencia la fila). Sin ella, el consolidador devuelve la matriz.

Ejemplo de evaluación sustentada:
> "El envío existe y está acusado dentro del plazo trimestral, pero la periodicidad comprometida exige sustento en el Comité de Riesgos y la última presentación registrada es de noviembre de 2025; el uso está acreditado en el nivel operativo y no en el de gobierno, por lo que las decisiones basadas en la curva carecen de validación del foro autorizado."
