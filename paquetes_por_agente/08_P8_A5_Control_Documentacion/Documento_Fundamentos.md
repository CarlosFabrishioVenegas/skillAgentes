# Fundamentos — Control de Documentación

**Estándar y gobierno de la documentación de modelos**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A5 · Control de Documentación  
Documento de Fundamentos · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [El estándar de documentación de SR 11-7](#el-estandar-de-documentacion-de-sr-11-7)
- [Los tres atributos que se evalúan por separado](#los-tres-atributos-que-se-evaluan-por-separado)
- [Documentación como control de continuidad](#documentacion-como-control-de-continuidad)
- [Documentación y continuidad del modelo](#documentacion-y-continuidad-del-modelo)
- [Anexo — El control dentro del flujo de validación VIRF](#anexo-el-control-dentro-del-flujo-de-validacion-virf)
- [Anexo — Semáforo de estados del sistema](#anexo-semaforo-de-estados-del-sistema)
- [Anexo — Ciclo de vida del modelo y ubicación de la validación](#anexo-ciclo-de-vida-del-modelo-y-ubicacion-de-la-validacion)
- [Ejemplo trabajado — fila de la matriz documental](#ejemplo-trabajado-fila-de-la-matriz-documental)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## El estándar de documentación de SR 11-7

SR 11-7 exige documentación suficiente para que un tercero independiente entienda, evalúe y replique el modelo sin recurrir a su desarrollador. La documentación no es un subproducto administrativo: es el soporte de la auditabilidad y la condición para el *effective challenge*. Un modelo bien construido pero mal documentado es, a efectos de validación, un modelo no verificable, y el riesgo de modelo asociado a la dependencia de conocimiento no documentado (por ejemplo, un único desarrollador que 'sabe cómo funciona') es material.

## Los tres atributos que se evalúan por separado

El control evalúa tres atributos que fallan de forma independiente y no deben confundirse en un solo juicio: **completitud** (el contenido existe), **vigencia** (corresponde a la versión productiva declarada en el acta y evidenciada por el código) y **coherencia** (no contradice a otras fuentes). Una documentación de excelente calidad que describe una versión distinta a la productiva es 'No cumple', porque no acredita lo que corre en producción; la calidad del contenido no compensa la falta de vigencia.

## Documentación como control de continuidad

La documentación cumple además una función de continuidad operativa: un modelo cuyo conocimiento reside solo en la memoria del desarrollador es frágil ante su rotación. Por eso el control observa no solo la existencia del contenido, sino su carácter formal (versionado, fechado, aprobado), que es lo que permite que otra persona retome el modelo.

## Documentación y continuidad del modelo

Más allá del cumplimiento formal, la documentación es un control de continuidad: un modelo cuyo conocimiento reside en una sola persona es frágil ante su rotación, y esa fragilidad es un riesgo de modelo que el control debe señalar. Una conclusión de validación no puede ser satisfactoria si el modelo funciona pero carece de manual vigente, porque el riesgo de dependencia de conocimiento no documentado permanece.

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

## Ejemplo trabajado — fila de la matriz documental

| ID VIRF | Actividad | Documento | Estado | Sustento | Fuente | Acción |
|---|---|---|---|---|---|---|
| ACT-DOC-04 | Documentar la ventana de desempeño | Manual metodológico | Cumple con observación | El manual define 12 meses y el acta 18; coexisten sin conciliación | `Manual_v3.pdf > 3.1 > p.14` vs. `Acta_MOD-0412.docx > uso > p.2` | Emitir manual v3.1 con la conciliación — 2026-09-30 |


## Glosario

| Término | Definición |
|---|---|
| **Vigencia documental** | Correspondencia entre la versión documentada y la versión productiva del modelo. |
| **Ubicación no formal** | Contenido que existe solo en PPT, correo u otro soporte no versionado. |
| **Cierre de observación** | Subsanación acreditada con evidencia nueva citada, no con una declaración verbal. |
| **Control de versiones** | Registro de versión, autor, fecha y aprobación de cada documento. |
| **Cobertura documental** | Porcentaje de actividades del estándar efectivamente evidenciadas. |

## Errores frecuentes

- Dar por cubierta una actividad porque 'el equipo lo explicó en la reunión', sin documento formal.
- Cerrar una observación previa por declaración del equipo, sin manual actualizado.
- Marcar 'Cumple' una documentación de mayor calidad que corresponde a otra versión del modelo.
- Consolidar varias actividades del estándar en una sola fila de la matriz.
- Emitir el control como satisfactorio con cobertura documental inferior al 100 %.

## Lista de verificación antes de concluir

1. ¿La matriz tiene una fila por actividad de Documentación aplicable al tier?
2. ¿Se evaluaron por separado completitud, vigencia y coherencia?
3. ¿Se contrastó la versión documentada contra la productiva del acta y del código?
4. ¿Las observaciones del ciclo anterior tienen evidencia de cierre citada?
5. ¿Los defectos formales (sin versión, sin fecha, anexos faltantes) están listados?
6. ¿La cobertura de actividades alcanza el 100 %?


---

## Referencias

- **SR11-7** — Federal Reserve SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management (2011-04-04). *[referencia internacional canónica]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
