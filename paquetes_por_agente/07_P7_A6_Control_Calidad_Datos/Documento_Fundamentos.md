# Fundamentos — Control de Calidad de Datos (juicio de negocio)

**BCBS 239 y materialidad del defecto de datos**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A6 · Control de Calidad de Datos (juicio de negocio)  
Documento de Fundamentos · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [Los catorce principios de BCBS 239](#los-catorce-principios-de-bcbs-239)
- [De la cifra al juicio de control](#de-la-cifra-al-juicio-de-control)
- [Gobierno del dato](#gobierno-del-dato)
- [Interacción con el evaluador técnico](#interaccion-con-el-evaluador-tecnico)
- [Anexo — El control dentro del flujo de validación VIRF](#anexo-el-control-dentro-del-flujo-de-validacion-virf)
- [Anexo — Semáforo de estados del sistema](#anexo-semaforo-de-estados-del-sistema)
- [Anexo — Ciclo de vida del modelo y ubicación de la validación](#anexo-ciclo-de-vida-del-modelo-y-ubicacion-de-la-validacion)
- [Ejemplo trabajado — evaluación con impacto](#ejemplo-trabajado-evaluacion-con-impacto)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## Los catorce principios de BCBS 239

BCBS 239 organiza catorce principios en cuatro bloques. **Gobierno e infraestructura**: Principio 1 (gobierno) y Principio 2 (arquitectura de datos e infraestructura de TI). **Capacidad de agregación**: Principio 3 (exactitud e integridad), Principio 4 (completitud), Principio 5 (oportunidad) y Principio 6 (adaptabilidad). **Prácticas de reporte**: Principios 7 a 11 (exactitud, amplitud, claridad y utilidad, frecuencia y distribución). **Revisión supervisora**: Principios 12 a 14. Los bancos de importancia sistémica global debían cumplir a partir de enero de 2016; el marco se ha extendido como buena práctica a la banca en general.

## De la cifra al juicio de control

El agente técnico (A3) entrega las cifras; este control decide si el defecto es material para el modelo. Una tasa de nulos del 7,4 % puede ser irrelevante en una variable no usada y crítica en una variable del score. El valor del control está en conectar el defecto de dato con el output del modelo: qué variable se afecta, qué peso tiene en el modelo y en qué dirección y magnitud se mueve el resultado. Sin esa conexión, el hallazgo describe un problema de base de datos, no un riesgo de modelo.

## Gobierno del dato

BCBS 239 introduce la noción de propiedad del dato (*data ownership*) y de custodia (*data stewardship*): cada campo material debe tener un responsable identificable y un control documentado. El gobierno del dato es lo que distingue una calidad accidental (los datos hoy están bien) de una calidad gestionada (existe un marco que la sostiene en el tiempo).

## Interacción con el evaluador técnico

Este agente verifica primero la integridad del insumo de A3: que las nueve dimensiones estén presentes, que cada diagnóstico traiga cifra y que cada referencia sea verificable. Si algo falta, devuelve el insumo a A3 antes de emitir juicio; no lo completa por su cuenta. Esta devolución hacia atrás preserva la trazabilidad del hallazgo hasta la medición que lo originó y evita que el juicio de negocio se construya sobre cifras incompletas.

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

## Ejemplo trabajado — evaluación con impacto

> 'La variable `ingreso_declarado` concentra el 22 % del peso del score y presenta 7,4 % de nulos imputados por mediana sin regla documentada; la imputación desplaza la media del score en +4 puntos y reclasifica 318 clientes de segmento, por lo que el defecto es material para el output y no solo para la base.'

La evaluación conecta el defecto con el peso de la variable y con el efecto cuantificado sobre el output, que es lo que la convierte en un hallazgo de riesgo de modelo.

## Glosario

| Término | Definición |
|---|---|
| **Materialidad** | Relevancia de un defecto de dato según su impacto en el output del modelo. |
| **Data ownership** | Responsabilidad formal sobre un campo o conjunto de datos. |
| **Circularidad del control** | Situación en que el control se cumple porque se eliminan los datos que lo incumplirían. |
| **Linaje** | Rastro documentado de un campo desde su origen a través de cada transformación. |
| **Marco de control** | Conjunto de control definido, umbral, responsable y periodicidad de ejecución. |

## Errores frecuentes

- Convertir la matriz de dimensiones en un puntaje agregado que oculta el defecto material.
- Aceptar la limpieza previa a la entrega como evidencia de calidad del dato.
- Declarar cumplimiento cuando el marco de control no existe, aunque los datos estén perfectos.
- Trasladar a Metodología un hallazgo que es de datos, o viceversa.
- Ignorar la ausencia de linaje en Tier 1 o Tier 2 por parecer un tema formal.

## Lista de verificación antes de concluir

1. ¿Se verificó que el insumo de A3 trae las nueve dimensiones con cifra y referencia?
2. ¿Cada defecto se tradujo a impacto sobre el output (variable, peso, dirección)?
3. ¿Se evaluó la existencia del marco de control (umbral, responsable, periodicidad)?
4. ¿Se verificó el linaje campo a campo en Tier 1 y Tier 2?
5. ¿Se detectó y trató cualquier señal de depuración previa a la entrega?
6. ¿Los hallazgos se priorizaron por materialidad y no por número?


---

## Referencias

- **BCBS239** — BCBS 239 — Principles for effective risk data aggregation and risk reporting (Comité de Basilea, ene-2013). *[referencia internacional canónica]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
