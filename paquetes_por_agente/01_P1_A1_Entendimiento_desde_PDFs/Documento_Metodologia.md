# Metodología — Generador de entendimiento desde PDFs

**Documentación y entendimiento de modelos**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A1 · Generador de entendimiento desde PDFs  
Documento de Metodología · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [Estructura del entregable de entendimiento](#estructura-del-entregable-de-entendimiento)
- [Reglas de extracción y de cita por página](#reglas-de-extraccion-y-de-cita-por-pagina)
- [Manejo de defectos frecuentes en los PDF](#manejo-de-defectos-frecuentes-en-los-pdf)
- [Control de completitud del entregable](#control-de-completitud-del-entregable)
- [Consultas abiertas y su redacción](#consultas-abiertas-y-su-redaccion)
- [Anexo — Tabla maestra de umbrales cuantitativos](#anexo-tabla-maestra-de-umbrales-cuantitativos)
- [Anexo — Distinción entre tipos de insuficiencia](#anexo-distincion-entre-tipos-de-insuficiencia)
- [Ejemplo trabajado — fila de tabla de inputs](#ejemplo-trabajado-fila-de-tabla-de-inputs)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## Estructura del entregable de entendimiento

El entregable es un archivo estructurado (`entendimiento_<codigo>.md`) que reproduce una plantilla fija y no negociable: (1) metadatos con fuente; (2) propósito, cada afirmación con cita; (3) tabla de inputs con origen, frecuencia y responsable; (4) tabla de transformaciones paso a paso, cada paso referenciado al manual y al código; (5) ficha de la herramienta con su estado de admisibilidad; (6) tabla de outputs con formato, destino y uso declarado; (7) transcripción literal de supuestos y limitaciones; (8) controles de datos declarados; (9) historial de validaciones y observaciones abiertas; (10) evidencias leídas y no recibidas. El orden no se altera y ninguna sección se elimina: una sección sin evidencia se marca 'No evidenciado'.

## Reglas de extracción y de cita por página

Cada afirmación lleva su cita con página: `<archivo> > <sección> > p.<n>`. La página es obligatoria; si el PDF no tiene numeración impresa, se usa la página física del archivo y se anota 'p.N (física)'. Las fórmulas se transcriben tal cual, entre `backticks`, aun con notación ambigua, y los símbolos sin definir se listan como consulta abierta. Un input mencionado solo en un diagrama, sin descripción textual, se registra con esa nota, porque su ausencia de descripción afecta al control de Documentación.

## Manejo de defectos frecuentes en los PDF

El agente aplica reglas fijas ante documentos imperfectos: un PDF escaneado sin capa de texto no es extraíble, se marca 'requiere OCR' y se detiene su procesamiento, nunca se declara vacío; un anexo referenciado y no entregado se registra como faltante; dos versiones del mismo manual en la carpeta obligan a usar la más reciente y a reportar la discrepancia; una tabla partida entre páginas se reconstruye completa y se cita el rango; un documento con marca de 'borrador' se procesa pero se anota que su condición impide acreditar vigencia; un PDF de más de 300 páginas se procesa por bloques y se anota el rango efectivamente leído.

## Control de completitud del entregable

Antes de entregar, el agente verifica siete condiciones: toda línea con contenido tiene cita con página; los supuestos están entre comillas y sin parafrasear; las tablas de inputs y outputs tienen todas sus columnas; los campos sin evidencia dicen 'No evidenciado'; cada documento leído aparece con su hash; las consultas abiertas están numeradas y son respondibles; el nombre y el código del modelo son idénticos en todas las secciones. Regla de degradación elegante: aunque más del 30 % de los campos queden en 'No evidenciado', el agente ENTREGA igualmente el `.md` completo, rotula la primera línea 'Entendimiento parcial (X % evidenciado)', cierra con una sección '## Brechas de evidencia' (ítem esperado, estado, evidencia faltante, documento que debía contenerla, impacto) y añade la solicitud de re-entrega. Nunca condiciona la entrega a recibir más documentos: la ausencia de evidencia es un hallazgo del ciclo, no un motivo para no entregar.

## Consultas abiertas y su redacción

Toda ambigüedad detectada durante la extracción se convierte en una consulta abierta numerada y respondible con un sí, un no o un dato concreto. Una consulta bien redactada identifica la contradicción, cita las dos fuentes en conflicto y nombra al destinatario. Ejemplo: 'Consulta 01: el manual declara ventana de 12 meses (`Manual_v3.pdf > 3.1 > p.14`) y el acta 18 meses (`Acta.docx > uso > p.2`); ¿cuál corresponde a producción?'. Las consultas se centralizan luego en el control de Gobierno para evitar duplicados al equipo dueño.

## Anexo — Tabla maestra de umbrales cuantitativos

Referencia consolidada de los umbrales usados en el sistema. **Todos son convenciones de industria y deben calibrarse y aprobarse en la política interna de validación**; no son mínimos regulatorios salvo donde se indique.

| Métrica | Umbral / criterio | Interpretación |
|---|---|---|
| PSI | < 0.10 / 0.10–0.25 / ≥ 0.25 | estable / moderado / significativo |
| CSI | mismos cortes que PSI | por variable de entrada |
| z-score (outlier) | \|z\| > 3 | atípico univariado |
| IQR (outlier) | fuera de [Q1−1.5·IQR, Q3+1.5·IQR]; extremo 3.0·IQR | robusto ante colas |
| VaR z (95% / 99%) | 1.645 / 2.326 | factor normal |
| Semáforo Basilea (250 d) | 0–4 / 5–9 / 10+ | verde / amarillo / rojo |
| Multiplicador de capital | 3.0 → 4.0 | según zona del semáforo |
| Expected Shortfall (FRTB) | nivel 97.5% | reemplaza al VaR en IMA |
| AUC | > 0.7 aceptable; > 0.8 bueno | discriminación |
| Gini | 0.4–0.6 típico minorista | = 2·AUC − 1 |
| KS | > 0.3 razonable | separación de distribuciones |
| Tolerancia de reconciliación | rtol 1e-6 a 1e-8 | equivalencia numérica |


## Anexo — Distinción entre tipos de insuficiencia

El sistema distingue con precisión tres situaciones que producen acciones distintas y jamás deben confundirse en una misma redacción: el control o la evidencia **NO EXISTE** (nadie lo definió o no se entregó), en cuyo caso el estado es 'No evidenciado' y la acción es solicitar la entrega; el control **EXISTE PERO NO SE EJECUTÓ** en el ciclo, en cuyo caso la acción es exigir su ejecución; y el control **SE EJECUTÓ Y FALLÓ**, en cuyo caso la acción es la remediación del defecto. Confundir 'no existe' con 'falló' oculta la naturaleza del problema y desvía la remediación. A ello se suma 'No verificable', reservado para la evidencia que existe pero no es citable ni reproducible.

## Ejemplo trabajado — fila de tabla de inputs

Ante un manual que menciona el ingreso del cliente, una fila correcta del entendimiento es:

| Input | Origen | Frecuencia | Responsable | Fuente |
|---|---|---|---|---|
| `ingreso_declarado` | Datamart Riesgos, tabla DM_CLIENTE | Mensual | Gobierno de Datos | `Manual_Metodologico_PD_Retail_v3.pdf > 3.2 Fuentes > p.19` |

Una fila incorrecta sería `| ingreso | Datamart | Mensual | — | Manual metodológico |`: el origen no identifica la tabla, no hay responsable y la cita carece de sección y página, por lo que no es verificable por un tercero.

## Glosario

| Término | Definición |
|---|---|
| **Entendimiento del modelo** | Reconstrucción independiente de la cadena input→output→uso, con cita en cada eslabón. |
| **Replicabilidad** | Propiedad de que un tercero pueda reproducir el modelo con la sola documentación entregada. |
| **Override** | Anulación o ajuste manual de la salida del modelo por parte del usuario, sujeta a control. |
| **Matriz de trazabilidad** | Tabla que conecta cada input con su transformación y con el output que produce. |
| **Cita física** | Referencia a la página contada en el archivo cuando el PDF carece de numeración impresa. |

## Errores frecuentes

- Parafrasear los supuestos en lugar de transcribirlos literalmente, alterando el criterio de validación posterior.
- Declarar 'documentado' un contenido que solo existe en una PPT o un correo, sin observar la ubicación no formal.
- Completar un campo por analogía con otro modelo 'parecido' en vez de marcarlo 'No evidenciado'.
- Dar por leída la totalidad de un PDF extenso sin anotar el rango de páginas efectivamente recorrido.
- Tratar un PDF escaneado sin OCR como documento vacío en lugar de 'requiere OCR'.

## Lista de verificación antes de concluir

1. ¿Cada afirmación tiene cita con página (o 'física' si no hay numeración)?
2. ¿Los supuestos y limitaciones están transcritos literalmente, entre comillas?
3. ¿Las tablas de inputs y outputs tienen origen, frecuencia y responsable completos?
4. ¿Los campos sin evidencia dicen 'No evidenciado' y no están vacíos?
5. ¿Cada documento leído figura con su hash y su rango de páginas?
6. ¿Las consultas abiertas están numeradas y son respondibles?


---

## Referencias

- **SR11-7** — Federal Reserve SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management (2011-04-04). *[referencia internacional canónica]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
