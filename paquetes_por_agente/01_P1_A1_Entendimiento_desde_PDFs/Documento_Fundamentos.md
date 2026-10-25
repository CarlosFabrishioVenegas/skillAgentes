# Fundamentos — Generador de entendimiento desde PDFs

**Documentación y entendimiento de modelos**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A1 · Generador de entendimiento desde PDFs  
Documento de Fundamentos · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [Qué es el entendimiento de un modelo](#que-es-el-entendimiento-de-un-modelo)
- [Manual metodológico frente a manual de usuario](#manual-metodologico-frente-a-manual-de-usuario)
- [El principio de replicabilidad independiente](#el-principio-de-replicabilidad-independiente)
- [Tratamiento de los supuestos y las limitaciones](#tratamiento-de-los-supuestos-y-las-limitaciones)
- [Relación con los demás controles](#relacion-con-los-demas-controles)
- [Anexo — El control dentro del flujo de validación VIRF](#anexo-el-control-dentro-del-flujo-de-validacion-virf)
- [Anexo — Semáforo de estados del sistema](#anexo-semaforo-de-estados-del-sistema)
- [Anexo — Ciclo de vida del modelo y ubicación de la validación](#anexo-ciclo-de-vida-del-modelo-y-ubicacion-de-la-validacion)
- [Ejemplo trabajado — fila de tabla de inputs](#ejemplo-trabajado-fila-de-tabla-de-inputs)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## Qué es el entendimiento de un modelo

El entendimiento de un modelo es la reconstrucción, por un tercero independiente, de la cadena completa que va del dato de entrada a la decisión de negocio. No es un resumen ni una glosa: es la evidencia de que el modelo puede explicarse y, en principio, replicarse sin recurrir a su desarrollador. Bajo SR 11-7, la documentación de un modelo debe ser suficiente para que un revisor competente lo entienda, lo evalúe y lo reproduzca; el entendimiento es la materialización de ese criterio.

La cadena canónica tiene seis eslabones que el agente reconstruye en orden: (1) propósito de negocio; (2) inputs (datos, supuestos y parámetros); (3) transformación (metodología, ecuaciones y algoritmos); (4) outputs (estimaciones y métricas); (5) uso (decisiones, límites y reportes que consumen el output); y (6) limitaciones y condiciones de uso válidas. Un entendimiento es completo solo cuando ningún eslabón queda sin evidencia citable; un eslabón sin fuente se muestra roto de forma explícita, con el estado 'No evidenciado'.

## Manual metodológico frente a manual de usuario

Son documentos distintos, con propósitos distintos, y ambos son objeto de validación. El **manual metodológico** expone el fundamento teórico y su justificación de negocio, la derivación matemática, los supuestos y su sustento, las alternativas consideradas y descartadas, los datos de desarrollo (fuente, ventana temporal, criterio de muestreo), la calibración, las pruebas de desempeño y, de forma explícita, las limitaciones y usos válidos. El **manual de usuario** describe la operación: entradas y salidas, frecuencia de ejecución, interpretación de resultados, controles operativos y procedimientos de escalamiento y de anulación manual (*overrides*).

La distinción importa para el control de Documentación: un contenido metodológico que solo existe en una presentación de comité o en un correo acredita el contenido, pero introduce una observación por ubicación no formal, porque una presentación no sustituye a un manual versionado.

## El principio de replicabilidad independiente

El criterio rector es la autosuficiencia documental. Si el validador debe preguntar al desarrollador para completar la cadena, la documentación es insuficiente por definición, aunque el contenido faltante 'sea obvio' para quien construyó el modelo. Esto obliga a declarar los supuestos implícitos, a fechar y versionar cada documento, y a mantener una **matriz de trazabilidad** que conecte cada input con la transformación que lo consume y con el output que produce. La replicabilidad no exige que el validador recalcule todo, sino que **podría** hacerlo con lo entregado.

## Tratamiento de los supuestos y las limitaciones

Los supuestos y las limitaciones son el material más sensible del entendimiento y se transcriben de forma **literal**, entre comillas, con su cita. Parafrasearlos altera el criterio contra el que se contrastará el uso del modelo en el control de Usos y las condiciones de validez en el de Metodología. Un supuesto declarado pero nunca probado es un hallazgo latente que el agente deja visible; una limitación omitida en la documentación es un defecto de mayor gravedad que una limitación mal redactada, porque oculta el perímetro de validez del modelo.

## Relación con los demás controles

El entendimiento que produce este agente es el insumo común de los seis controles: el mapa de evidencia orienta a Documentación sobre qué manuales existen, a Metodología sobre qué papers se entregaron, a Implementación sobre el estado de la herramienta, a Gobierno sobre los campos del acta y a Usos sobre los outputs y sus destinatarios. Un entendimiento pobre degrada a todos los controles aguas abajo; por eso su completitud se mide y se reporta, y por debajo del 80 % el entregable se rotula 'Entendimiento parcial' y activa la re-entrega.

## Anexo — El control dentro del flujo de validación VIRF

Cada control convive con los demás dentro de un flujo ordenado. Antes del análisis hay cuatro etapas previas: la **reunión de entendimiento** (E1), donde el equipo dueño explica el modelo; la **entrega inicial de insumos** (E2), con inventario y hash de cada archivo; el **kick-off** (E3), que fija responsables y el deadline del requerimiento; y el **requerimiento formal** (E4), que consolida el expediente. Sobre ellas se construye el **Paso 0** (E0): el documento de entendimiento y la infografía que sirven de base común a los seis controles.

Los seis controles se ejecutan con reglas de precedencia. **Calidad de Datos** se evalúa primero, porque un hallazgo crítico de datos invalida las conclusiones de Metodología y de Implementación. **Implementación** no inicia antes de que el modelo haya corrido y sus outputs se hayan revisado. **Gobierno** requiere los resultados técnicos de los controles previos para contrastar el acta contra la realidad. **Usos** puede recomendar el retiro del modelo del inventario si no acredita uso efectivo. El **Validador Final** consolida todo en la tabla de 8 columnas.

## Anexo — Semáforo de estados del sistema

Todos los controles comparten un mismo conjunto de estados, y ninguno inventa estados intermedios:

| Estado | Definición | Efecto |
|---|---|---|
| Cumple | Evidencia completa, citada y consistente | Sin acción pendiente |
| Cumple con observación | Evidencia existe pero incompleta, desactualizada o ambigua | Acción con fecha |
| No cumple | La evidencia contradice lo declarado o el control falla | Hallazgo con severidad |
| No evidenciado | No se entregó evidencia del control | Hallazgo; nunca es cumplimiento |
| No verificable | Hay evidencia pero no es citable ni reproducible | Requiere re-entrega |
| No aplica | La actividad no corresponde al tier o al tipo de modelo | Se cita la regla que exime |

La ausencia de evidencia nunca se interpreta como cumplimiento, y 'No aplica' sin cita de la regla que lo exime está prohibido.

## Anexo — Ciclo de vida del modelo y ubicación de la validación

Todo modelo atraviesa un ciclo de vida con etapas diferenciadas, y la validación acompaña varias de ellas. En el **desarrollo** se construye la metodología, se selecciona la muestra y se calibra; la validación evalúa aquí la solidez conceptual. En la **implementación** el modelo pasa a código productivo; la validación verifica la fidelidad y la reproducibilidad. En el **uso** el output alimenta decisiones; la validación comprueba el uso efectivo y su alcance autorizado. En el **monitoreo** se vigila el desempeño en el tiempo mediante estabilidad y backtesting. Finalmente, en el **retiro** el modelo sale del inventario cuando deja de usarse o de ser apropiado.

La validación periódica —el objeto de este sistema— se sitúa después de la validación inicial y se repite con una frecuencia que depende del tier. No es un acto único: cada ciclo revalida que el modelo sigue siendo apropiado, que su documentación permanece vigente, que sus datos conservan calidad y que su uso continúa siendo efectivo. Un modelo que aprobó su validación inicial puede degradarse por deriva de datos, cambio de entorno o pérdida de uso, y es la validación periódica la que detecta esa degradación antes de que se materialice en pérdidas.

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
- **SBS-053-2023** — Resolución SBS N° 00053-2023 — Reglamento de Gestión de Riesgos de Modelo (Lima, 06-01-2023; mod. Res. 3421-2023 y 3884-2024). *[validada — fuente primaria SBS]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
