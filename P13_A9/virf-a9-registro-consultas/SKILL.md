---
name: virf-a9-registro-consultas
description: Gestión centralizada de consultas al equipo dueño del modelo (A9 es el único emisor, aunque la consulta la origine otro control) - redacción respondible con evidencia citada, destinatario, plazo y efecto de la no respuesta, verificación de que no esté ya respondida en el expediente, estados enviada, respondida y sin respuesta, y script de registro con detección de duplicados. Úsala en el Paso 13 (A9) y cada vez que A1-A10 generen consultas abiertas.
---

# A9 · Registro centralizado de consultas

A9 es el **único** agente que emite consultas al equipo dueño. Las demás generan borradores (`C1-…`, `C3-…`) y A9 las consolida, depura y emite.

## 1. Anatomía de una consulta válida

```markdown
**Consulta 03** (origen: C5 · destinatario: [G04])
El acta registra Tier 2 con exposición gestionada de S/ 180 MM, mientras el reporte de cartera 2026Q2 muestra S/ 640 MM.
¿Se solicitó reevaluación de tiering tras el crecimiento de exposición? (sí/no + documento)
Evidencia: Acta_Modelo_MOD-0412.docx > G03 > p.1; Reporte_Cartera_2026Q2.xlsx > Resumen > C9.
Plazo: 5 días hábiles (vence 2026-10-24).
Efecto de la no respuesta: el campo G03 se reporta como No verificable y el tiering queda observado en el informe final.
```

Siete elementos obligatorios: número · control de origen · pregunta respondible (sí/no/dato, una sola cosa) · evidencia con cita · destinatario · plazo · efecto de la no respuesta.

## 2. Antes de emitir: ¿ya está respondida?

```bash
python scripts/registro_consultas.py verificar --registro consultas.csv --texto "reevaluación de tiering exposición" --expediente /expediente/
```

Busca términos clave en el registro (consultas previas) y en los .md/.txt/.csv del expediente (minutas, respuestas por correo exportadas). Si hay coincidencias, revísalas antes de emitir: una consulta redundante deteriora la relación con el equipo y resta credibilidad.

## 3. Registrar y actualizar

```bash
python scripts/registro_consultas.py agregar --registro consultas.csv --origen C5 --destinatario G04 \
    --pregunta "¿Se solicitó reevaluación de tiering...?" --evidencia "Acta... > G03 > p.1; Reporte... > C9" \
    --plazo-dias 5 --efecto "G03 No verificable; tiering observado"
python scripts/registro_consultas.py responder --registro consultas.csv --numero 3 --respuesta "Sí, solicitud 2026-08-12" --fuente "correo riesgos@... > Re: Consulta 03 > 2026-10-20"
python scripts/registro_consultas.py vencer --registro consultas.csv --hoy 2026-10-25
python scripts/registro_consultas.py tabla --registro consultas.csv
```

Columnas: `numero, control_origen, pregunta, evidencia, destinatario, fecha_envio, plazo, estado, respuesta, fuente_respuesta, efecto_no_respuesta`.

Estados: `enviada` → `respondida` | `sin respuesta` (al vencer el plazo, `vencer` lo cambia automáticamente).

## 4. Reglas

- Respuesta verbal → pedir confirmación por correo y **citar el correo**, no la conversación.
- Consulta sin respuesta en plazo → el campo/actividad queda "No verificable" y la falta de respuesta se documenta como **riesgo de gobierno** en el informe final.
- No cerrar el control con consultas abiertas sin documentar su efecto sobre la conclusión.
- "Interpreta según lo más probable" → Gobierno no admite inferencia; ofrecer la redacción de la consulta.

## 5. Bloque (b) del entregable

```markdown
| N° | Control de origen | Pregunta | Evidencia | Destinatario | Envío | Plazo | Estado | Efecto de la no respuesta |
```
