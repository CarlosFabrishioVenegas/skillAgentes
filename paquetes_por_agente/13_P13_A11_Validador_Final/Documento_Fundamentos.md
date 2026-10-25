# Fundamentos — Validador Final (consolidación)

**Validación integral, informe y conclusión**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A11 · Validador Final (consolidación)  
Documento de Fundamentos · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [Los tres componentes de la validación integral](#los-tres-componentes-de-la-validacion-integral)
- [Effective challenge como principio rector](#effective-challenge-como-principio-rector)
- [Integrar, no revalidar](#integrar-no-revalidar)
- [Manejo de inconsistencias y hallazgos remediados](#manejo-de-inconsistencias-y-hallazgos-remediados)
- [Anexo — El control dentro del flujo de validación VIRF](#anexo-el-control-dentro-del-flujo-de-validacion-virf)
- [Anexo — Semáforo de estados del sistema](#anexo-semaforo-de-estados-del-sistema)
- [Anexo — Ciclo de vida del modelo y ubicación de la validación](#anexo-ciclo-de-vida-del-modelo-y-ubicacion-de-la-validacion)
- [Ejemplo trabajado — fila de la tabla de 8 columnas](#ejemplo-trabajado-fila-de-la-tabla-de-8-columnas)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## Los tres componentes de la validación integral

SR 11-7 define la validación como la conjunción de tres componentes que deben estar todos presentes: la **evaluación de la solidez conceptual** (juzga la calidad del diseño y la construcción); el **monitoreo continuo** (*process verification* y *benchmarking*, confirma que el modelo sigue siendo apropiado); y el **análisis de resultados** u *outcomes analysis* (incluye el backtesting, compara predicciones con resultados observados). Un informe que omite un componente no es una validación completa, aunque los otros dos estén bien ejecutados.

## Effective challenge como principio rector

El *effective challenge* es el cuestionamiento crítico y objetivo por partes con competencia, independencia e influencia, es decir, con la autoridad para forzar cambios. La consolidación no suaviza estados por plazos, por presión del equipo o por relación con el área; hacerlo vulnera el principio que da valor a la validación. El validador puede precisar hechos con evidencia nueva citada, pero no puede suavizar un estado.

## Integrar, no revalidar

El validador final integra lo que los otros agentes produjeron; no vuelve a la evidencia primaria. Si un control llega incompleto o sin cita, se devuelve a su agente en lugar de completarlo, porque completarlo por cuenta propia destruiría la trazabilidad del hallazgo hasta su origen. Si el validador puede ir a la fuente, es señal de que un control quedó incompleto.

## Manejo de inconsistencias y hallazgos remediados

Al consolidar, el validador no promedia ni elige entre dos estados distintos sobre el mismo hecho: documenta ambos y marca 'Inconsistencia entre controles' como hallazgo de proceso. Un hallazgo crítico remediado durante la validación conserva su fila con estado 'No cumple — remediado en el ciclo', con la evidencia y la fecha de remediación; no se elimina ni se convierte en 'Cumple', porque el registro del defecto y su corrección es parte de la trazabilidad.

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

## Ejemplo trabajado — fila de la tabla de 8 columnas

| Ámbito | Tipo | Actividad | Cumple | Resultado | Evaluación | Fuente | Acción |
|---|---|---|---|---|---|---|---|
| Implementación | Cuantitativo | ACT-IMP-09 — parámetros implementados vs documentados | No cumple | Corte 620 vs 640; 4 128 clientes (2,7 %) | Diferencia no aprobada que reclasifica segmento de riesgo; bloquea el cierre | `pipeline_pd.py > línea 193`; `Manual_v3.pdf > 6.2 > p.48` | Alinear código y manual — 2026-09-20. Bloqueante |


## Glosario

| Término | Definición |
|---|---|
| **Solidez conceptual** | Evaluación de la calidad del diseño y la construcción del modelo. |
| **Outcomes analysis** | Comparación de las salidas del modelo con los resultados observados (backtesting). |
| **Effective challenge** | Cuestionamiento crítico por partes con competencia, independencia e influencia. |
| **Cobertura** | Porcentaje de actividades del estándar aplicables efectivamente evaluadas. |
| **Tabla de 8 columnas** | Formato único de consolidación de los seis controles. |

## Errores frecuentes

- Emitir la conclusión antes de la tabla, o suavizar un estado por consideraciones de plazo.
- Completar por cuenta propia un control incompleto en vez de devolverlo a su agente.
- Concluir 'satisfactoria' con cobertura inferior al 100 %.
- Promediar o elegir entre dos estados distintos sobre el mismo hecho.
- Fusionar hallazgos para acortar el informe, rompiendo la trazabilidad al estándar.

## Lista de verificación antes de concluir

1. ¿Se reportó la cobertura por control y global antes de la tabla?
2. ¿Toda actividad sin fila se incorporó como 'No evidenciado'?
3. ¿Cada fila tiene estado, resultado, evaluación y fuente con cita?
4. ¿Se aplicaron las reglas de conclusión sin suavizar estados?
5. ¿Los controles sin cita se devolvieron a su agente?
6. ¿La conclusión se redactó después de la tabla, en máximo doce líneas?


---

## Referencias

- **SR11-7** — Federal Reserve SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management (2011-04-04). *[referencia internacional canónica]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
