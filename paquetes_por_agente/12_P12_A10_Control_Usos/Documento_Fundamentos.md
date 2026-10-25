# Fundamentos — Control de Usos

**Use test y uso efectivo del modelo**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A10 · Control de Usos  
Documento de Fundamentos · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [El use test de Basilea](#el-use-test-de-basilea)
- [Uso efectivo frente a uso declarado](#uso-efectivo-frente-a-uso-declarado)
- [Niveles de uso](#niveles-de-uso)
- [Usos regulatorios y modelos encadenados](#usos-regulatorios-y-modelos-encadenados)
- [Anexo — El control dentro del flujo de validación VIRF](#anexo-el-control-dentro-del-flujo-de-validacion-virf)
- [Anexo — Semáforo de estados del sistema](#anexo-semaforo-de-estados-del-sistema)
- [Anexo — Ciclo de vida del modelo y ubicación de la validación](#anexo-ciclo-de-vida-del-modelo-y-ubicacion-de-la-validacion)
- [Ejemplo trabajado — uso con observación](#ejemplo-trabajado-uso-con-observacion)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## El use test de Basilea

El *use test* proviene del marco IRB de Basilea: las estimaciones internas (PD, LGD, EAD) y, por extensión, los outputs de los modelos deben **usarse efectivamente en la gestión** —originación, fijación de límites, pricing, provisiones y capital— y no solo para el cálculo regulatorio. Un modelo cuyo output no se usa, o se usa fuera de su propósito documentado, genera riesgo de modelo sin beneficio de gestión: consume recursos de validación, ocupa un lugar en el inventario y crea una falsa sensación de cobertura.

## Uso efectivo frente a uso declarado

El control verifica que el uso real coincida con el uso declarado en el acta. Un uso distinto al autorizado es hallazgo, aunque exista evidencia abundante de uso, porque implica emplear el modelo fuera del alcance aprobado; por ejemplo, un modelo informativo usado para decidir límites excede su alcance y comparte el hallazgo con Gobierno. La correspondencia entre uso real y uso autorizado es tan importante como la existencia misma del uso.

## Niveles de uso

El uso se acredita en dos niveles que no se sustituyen: el **operativo** (el output llega al área usuaria y se emplea en su proceso) y el de **gobierno** (el output se sustenta en el foro comprometido, con decisión o toma de conocimiento registrada). Un uso operativo acreditado sin sustento en el foro de gobierno deja las decisiones sin validación del órgano autorizado y se reporta como observación.

## Usos regulatorios y modelos encadenados

No todo uso es una decisión de negocio: un modelo de uso regulatorio acredita su uso por el reporte remitido al supervisor, y un modelo cuyo output alimenta a otro modelo acredita su uso por la evidencia de consumo del modelo aguas abajo, identificado por su código de inventario. El control cuantifica los períodos sin uso: un uso interrumpido durante parte del período es incumplimiento parcial, no cumplimiento, y se reporta con los días o trimestres sin evidencia.

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

## Ejemplo trabajado — uso con observación

> 'El envío existe y está acusado dentro del plazo trimestral, pero la periodicidad comprometida exige sustento en el Comité de Riesgos y la última presentación registrada es de noviembre de 2025; el uso está acreditado en el nivel operativo y no en el de gobierno. Fuente: `mgomez@banco.pe > Curva PD 2026Q2 > 2026-07-08`; `Comité de Riesgos > acta 118 > agenda`.'

El hallazgo distingue el uso operativo (acreditado) del de gobierno (pendiente), que es la clave del control.

## Glosario

| Término | Definición |
|---|---|
| **Use test** | Exigencia de que los outputs del modelo se usen efectivamente en la gestión. |
| **Cadena de uso** | Secuencia generación→envío→acuse→foro→decisión que evidencia el uso. |
| **Uso operativo / de gobierno** | Uso en el proceso del área usuaria / sustento en el foro comprometido. |
| **Retiro del inventario** | Baja de un modelo sin uso efectivo demostrable. |
| **Alcance autorizado** | Uso para el que el modelo fue aprobado, según el acta. |

## Errores frecuentes

- Acreditar uso por la mera existencia del output, sin cadena de envío y sustento.
- Considerar el envío interno entre miembros del equipo desarrollador como evidencia de uso.
- Omitir la recomendación de retiro cuando no hay uso, por no generar fricción con el área.
- Aceptar un uso distinto al declarado sin generar el hallazgo compartido con Gobierno.
- Dar por acreditado un uso publicado en tablero sin evidencia de consumo.

## Lista de verificación antes de concluir

1. ¿Se reconstruyó la cadena de uso completa para cada output declarado?
2. ¿El uso real coincide con el uso declarado en el acta?
3. ¿Las fechas de envío respetan la periodicidad, con los días de desviación cuantificados?
4. ¿La cifra publicada coincide con la generada por la herramienta?
5. ¿Se acreditó tanto el uso operativo como el de gobierno?
6. ¿Ante ausencia de uso, se emitió la recomendación formal de retiro?


---

## Referencias

- **BASEL-IRB** — Basel Framework — Internal Ratings-Based approach y use test. *[referencia internacional canónica]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
