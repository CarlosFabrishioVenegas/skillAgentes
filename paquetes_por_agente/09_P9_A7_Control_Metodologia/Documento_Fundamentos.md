# Fundamentos — Control de Metodología

**Validación cuantitativa: VaR, IFRS 9, conductuales y métricas**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A7 · Control de Metodología  
Documento de Fundamentos · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [Solidez conceptual y tipos de sustento](#solidez-conceptual-y-tipos-de-sustento)
- [Los tres ejes de la validación metodológica](#los-tres-ejes-de-la-validacion-metodologica)
- [Errores que invalidan una prueba](#errores-que-invalidan-una-prueba)
- [Interpretabilidad y supuestos macro](#interpretabilidad-y-supuestos-macro)
- [Anexo — El control dentro del flujo de validación VIRF](#anexo-el-control-dentro-del-flujo-de-validacion-virf)
- [Anexo — Semáforo de estados del sistema](#anexo-semaforo-de-estados-del-sistema)
- [Anexo — Ciclo de vida del modelo y ubicación de la validación](#anexo-ciclo-de-vida-del-modelo-y-ubicacion-de-la-validacion)
- [Ejemplo trabajado — evaluación de calibración](#ejemplo-trabajado-evaluacion-de-calibracion)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## Solidez conceptual y tipos de sustento

El control evalúa dos cosas distintas y en filas separadas: la **suficiencia del sustento** (si cada decisión metodológica tiene respaldo citable y pertinente) y la **ejecución de las actividades** (si las pruebas exigidas se hicieron y con qué resultado). Un modelo puede tener excelente bibliografía y no haber ejecutado el backtesting; son hallazgos distintos. El sustento se clasifica en: paper académico, norma regulatoria, práctica interna documentada, prueba empírica propia o criterio experto; este último solo se acredita si existe acta del foro que lo acordó, con fecha y participantes.

## Los tres ejes de la validación metodológica

Toda validación cuantitativa descansa en tres ejes complementarios: **discriminación** (capacidad de separar eventos de no eventos), **calibración** (correspondencia entre probabilidad estimada y frecuencia observada) y **estabilidad** (persistencia del desempeño en el tiempo). Un modelo puede discriminar bien y estar mal calibrado, o viceversa: son propiedades independientes. A ellos se suman el backtesting, el benchmarking contra modelos alternativos y el análisis de sensibilidad.

## Errores que invalidan una prueba

Una métrica calculada sobre la muestra de desarrollo no acredita desempeño fuera de muestra; la validación exige una muestra independiente. Una **fuga de información** (variables construidas con información posterior al momento de decisión) infla artificialmente el desempeño. Un **sobreajuste** se manifiesta como desempeño muy superior en desarrollo frente a validación. El control cuantifica estas brechas en lugar de tratarlas como observaciones menores.

## Interpretabilidad y supuestos macro

Además de discriminación, calibración y estabilidad, el control atiende dos frentes recurrentes: la **interpretabilidad** (una variable con relación contraintuitiva respecto del riesgo, sin explicación, genera consulta y observación) y los **supuestos macroeconómicos** (un escenario forward-looking sin dueño ni aprobación es hallazgo). Un ajuste discrecional posterior al modelo (overlay) exige su política, su cuantificación y su aprobación; un overlay no documentado es hallazgo crítico.

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

## Ejemplo trabajado — evaluación de calibración

> 'El sustento teórico de la calibración es pertinente, pero la tasa central usada (3,10 %) corresponde a la cosecha 2023 y no a la ventana 2024-2025 declarada en el manual; el escalamiento subestima la PD media en 34 pbs frente a la observada en el mismo período. Fuente: `Manual_v3.pdf > 5.4 > p.41`; `herramienta_pd.xlsx > Calibracion > F22`.'

La fila separa el sustento (pertinente) de la ejecución (defectuosa por usar una ventana distinta a la declarada) y cuantifica el impacto en puntos básicos.

## Glosario

| Término | Definición |
|---|---|
| **VaR / ES** | Cuantil de pérdida (VaR) y pérdida media en la cola (Expected Shortfall). |
| **Kupiec / Christoffersen** | Pruebas de backtesting: número de excepciones y su independencia temporal. |
| **ECL / staging / SICR** | Pérdida esperada, clasificación en etapas y aumento significativo del riesgo (IFRS 9). |
| **AUC / KS / Gini** | Métricas de discriminación de un modelo de clasificación. |
| **CPR / SMM** | Tasas de prepago condicional anual y mensual. |
| **Fuga de información** | Uso de datos posteriores al momento de decisión que infla el desempeño. |

## Errores frecuentes

- Aprobar una técnica por ser 'estándar de la industria' sin sustento interno documentado.
- Aceptar una métrica calculada sobre la muestra de desarrollo como evidencia de desempeño.
- Citar un paper que no corresponde a la técnica efectivamente implementada.
- Tratar como cumplimiento tácito la ausencia de un umbral de aceptación declarado.
- Mezclar en una sola fila el sustento teórico y la ejecución de la prueba.

## Lista de verificación antes de concluir

1. ¿Cada decisión metodológica tiene sustento citable y pertinente a la técnica implementada?
2. ¿Las métricas reportadas se reprodujeron con los datos y el código entregados?
3. ¿La muestra de validación es independiente de la de desarrollo?
4. ¿Se verificó ausencia de fuga de información en la construcción de variables?
5. ¿El backtesting de VaR aplicó Kupiec y Christoffersen con su resultado?
6. ¿Cada métrica se contrastó contra un umbral de aceptación declarado?


---

## Referencias

- **SR11-7** — Federal Reserve SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management (2011-04-04). *[referencia internacional canónica]*
- **HOSMER** — Hosmer, D. & Lemeshow, S., Applied Logistic Regression. *[referencia internacional canónica]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
