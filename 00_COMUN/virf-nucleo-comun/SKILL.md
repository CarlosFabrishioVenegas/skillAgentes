---
name: virf-nucleo-comun
description: Reglas transversales del Marco Operativo VIRF que todo agente (A1 a A11) debe aplicar - formato de cita documental y de código, semáforo oficial de estados, sección de brechas de evidencia, adjetivos prohibidos y hash SHA-256 de evidencias. Úsala en cualquier paso del workflow de validación de modelos antes de emitir un entregable.
---

# Núcleo común VIRF

Este skill fija las convenciones que comparten los 15 agentes del workflow. Si un skill específico del agente contradice algo de aquí, prevalece el skill específico solo en lo que dice expresamente; en todo lo demás rige este núcleo.

## 1. Formatos de cita (obligatorios)

| Tipo de evidencia | Formato | Ejemplo |
|---|---|---|
| Documento (PDF/Word) | `archivo > sección > p.N` | `Manual_Metodologico_PD_Retail_v3.pdf > 3.2 Fuentes > p.19` |
| PDF sin numeración impresa | `archivo > sección > p.N (física)` | `Anexo_B.pdf > Tabla 4 > p.7 (física)` |
| Tabla partida entre páginas | `archivo > sección > pp.N–M` | `Manual.pdf > 5.1 Variables > pp.22–24` |
| Código | `archivo > función() > línea N` | `calc_pd.py > escalar_pd() > línea 118` |
| Excel | `libro > hoja > celda o rango` | `Herramienta_PD_2026.xlsx > Calculo > D14:D980` |
| Notebook | `notebook > celda N > línea N` | `A3_controles_calidad.ipynb > celda 12 > línea 4` |
| Correo | `remitente > asunto > fecha` | `riesgos.retail@... > Envío curva PD > 2026-07-03` |
| Comité | `comité > acta N > acuerdo N` | `Comité de Riesgos > acta 14 > acuerdo 3` |
| Publicación | `ruta o tablero > fecha de actualización > evidencia de consumo` | |
| Texto pegado en el chat | `texto proporcionado en sesión, sin archivo fuente` | cita débil: debe reemplazarse antes del cierre |
| Declaración verbal | `Declaración verbal en reunión del <fecha>, sin sustento documental` | nunca se eleva a hecho |

Regla de oro: **una línea con contenido sin cita es un defecto del entregable.** Antes de responder, recorre el borrador y busca líneas sin cita.

## 2. Semáforo oficial de estados

Solo estos seis estados. No crear intermedios ni porcentajes por actividad.

| Estado | Cuándo |
|---|---|
| Cumple | Evidencia citable, vigente y coherente; dentro de umbral declarado |
| Cumple con observación | Evidencia presente con defecto de forma o de proceso que no altera el output |
| No cumple | Evidencia contradice la exigencia, o la exigencia no se satisface |
| No evidenciado | No hay insumo que aborde la actividad |
| No verificable | El insumo existe pero no se entregó, es ilegible, no reproducible, o el umbral es [SUPUESTO] |
| No aplica | Solo con cita de la regla del estándar que exime; sin cita se reclasifica a No evidenciado |

Reglas duras:
- La ausencia de evidencia **nunca** es "Cumple".
- Un umbral no declarado por el banco se marca `[SUPUESTO]` y el resultado queda "No verificable".
- Un hallazgo remediado durante el ciclo conserva su estado original con la nota "remediado en el ciclo" y la fecha.

## 3. Sección obligatoria de cierre: Brechas de evidencia

Todo entregable termina con:

```markdown
## Brechas de evidencia
| Ítem esperado | Estado (ausente/parcial) | Evidencia faltante | Documento que debía contenerla | Impacto | Control afectado |
|---|---|---|---|---|---|

**Solicitud de re-entrega:** <lista numerada de lo que debe entregar el equipo dueño, con destinatario>
```

Si no hay brechas, la sección aparece igual con "Sin brechas identificadas".

## 4. Degradación elegante

Ningún agente condiciona su entrega a recibir más archivos. Si falta evidencia: entrega con lo sustentable, rotula la primera línea (p. ej. `Entendimiento parcial (64 % evidenciado)`) y llena "Brechas de evidencia".

## 5. Lenguaje

- Prohibidos sin cifra en la misma frase: robusto, adecuado, sólido, razonable, suficientemente detallado, documentación adecuada.
- No traducir "probablemente" en "sí".
- No completar por analogía con otros modelos ni con "la práctica de la industria".
- Las consultas abiertas se numeran y deben poder responderse con sí, no o un dato.

## 6. Hash de evidencias

Toda evidencia leída se registra con su SHA-256. Usa `scripts/hash_evidencias.py`:

```bash
python scripts/hash_evidencias.py <carpeta_o_archivos...> --salida evidencias_hash.csv
```

Produce `archivo | tipo | bytes | sha256 | fecha_modificacion`. Esa tabla alimenta la sección de trazabilidad de A1, A4 y la HOJA 4 de A11.

## 7. Frontera entre agentes (para no invadir)

| Agente | Hace | No hace |
|---|---|---|
| A1, A2, AD, A4, AK | Extraer, traducir, instrumentar, consolidar entendimiento | Juzgar cumplimiento |
| A3D | Detectar y ejecutar controles de datos | Interpretar severidad, juicio C2 |
| A3E | Interpretar cifras de A3D, severidad, remediación | Detectar fallos nuevos, juicio C2 |
| AIM | Cuantificar impacto monetario | Juzgar cumplimiento |
| A5–A10 | Juicio de cada control C1–C6 | Consolidar |
| A9 | Único que emite consultas al equipo dueño | Resolver ambigüedades por inferencia |
| A11 | Integrar, cobertura, conclusión | Revalidar o completar controles ajenos |

Si te piden algo fuera de tu frontera: "Fuera de alcance de <agente>; corresponde a <agente correcto>".
