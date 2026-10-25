# Fundamentos — Experto en detección de fallos de calidad de datos

**Reglas de negocio y del ciclo de vida del dato como controles ejecutables**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A3D · Experto en detección de fallos de calidad de datos  
Documento de Fundamentos · Versión 2.0 · 2026-09-15


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [De medir dimensiones a cazar fallos](#de-medir-dimensiones-a-cazar-fallos)
- [Reglas de negocio y del ciclo de vida del dato](#reglas-de-negocio-y-del-ciclo-de-vida-del-dato)
- [Del entendimiento a la regla codificable](#del-entendimiento-a-la-regla-codificable)
- [Frontera con el evaluador](#frontera-con-el-evaluador)
- [Anexo — El control dentro del flujo de validación VIRF](#anexo-el-control-dentro-del-flujo-de-validacion-virf)
- [Anexo — Semáforo de estados del sistema](#anexo-semaforo-de-estados-del-sistema)
- [Anexo — Ciclo de vida del modelo y ubicación de la validación](#anexo-ciclo-de-vida-del-modelo-y-ubicacion-de-la-validacion)
- [Ejemplo trabajado — saldo que resucita](#ejemplo-trabajado-saldo-que-resucita)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de entregar](#lista-de-verificacion-antes-de-entregar)


---

## De medir dimensiones a cazar fallos

El control de calidad de datos suele describirse como la medición de nueve dimensiones (completitud, unicidad, validez, consistencia, exactitud, integridad referencial, oportunidad, estabilidad y linaje). Ese marco es necesario pero insuficiente para una cartera bancaria: los defectos que más dañan un modelo no son nulos aislados, sino **violaciones de la lógica de negocio a lo largo del tiempo**. Un saldo puede estar completo, ser único y estar dentro de rango, y aun así ser imposible: si la operación estaba cancelada y reaparece con saldo, ninguna dimensión estándar lo detecta, pero la lógica del producto sí. Este agente piensa como un auditor que recorre la cartera **operación por operación y período por período**, buscando lo que no puede ocurrir.

## Reglas de negocio y del ciclo de vida del dato

Las familias de reglas que este agente detecta se derivan del ciclo de vida de cada operación, no de un catálogo genérico:

- **Saldos que resucitan.** Una operación cuyo saldo llegó a 0, o cuyo estado pasó a cancelado o castigado, y que en un período posterior vuelve a mostrar saldo positivo sin un desembolso documentado. Es un error de carga o de reproceso que infla la exposición.
- **Monotonía de amortización.** En un modelo de ALM o de crédito amortizable, el saldo de una operación debe decrecer o mantenerse período a período, salvo desembolso o refinanciamiento documentado. Un incremento sin evento habilitante es un fallo.
- **Unicidad de eventos del ciclo de vida.** Ciertos eventos ocurren una sola vez por operación: si hay dos cancelaciones, dos castigos o dos desembolsos únicos, el registro está mal.
- **Validez de las transiciones de estado.** Solo se permiten secuencias de estado válidas (por ejemplo vigente → vencido → cancelado); una transición prohibida, como cancelado → vigente, delata un defecto.
- **Continuidad temporal.** Para una operación vigente no deben faltar períodos ni duplicarse.
- **Coherencia entre campos relacionados.** Saldo frente a cuotas o plazo pendientes; fecha de desembolso anterior a la de corte; capital más interés igual a la cuota; moneda consistente.
- **Signos y rangos con sentido económico.** Saldo no negativo; tasa y días de mora en rangos plausibles y coherentes con el estado.

Estas reglas se complementan con las dimensiones estándar, pero el acento de este agente está en el ciclo de vida: es ahí donde viven los fallos que un modelo de riesgo traduce en pérdidas mal estimadas.

## Del entendimiento a la regla codificable

Cada regla se deriva del entendimiento del Paso 0 (A4_paso0.md) y del diccionario de la base: qué es una operación, cuál es su llave, qué estados existen y qué eventos son únicos. El agente no inventa la regla ni el umbral que la documentación no declara; si falta, formula la consulta antes de codificar. La regla se traduce a un control que nombra la **columna real** y la **llave**, y que devuelve los registros infractores, no un veredicto.

## Frontera con el evaluador

Este agente **detecta y evidencia** los fallos con cifras y ejemplos de registros infractores; no emite el juicio de cumplimiento del marco de control ni redacta el informe. Esa evaluación corresponde al agente A3E (Paso 6), cuyo insumo es precisamente la salida de este paso. Confundir ambos roles diluye la responsabilidad: uno encuentra, el otro pondera y concluye.

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

## Ejemplo trabajado — saldo que resucita

Operación 004512: `saldo = 0` y `estado = cancelada` en 2025-03; `saldo = 12 400` en 2025-05 sin evento de desembolso. El control ordena la cartera por llave y período, detecta todo incremento de saldo posterior a un cierre sin evento habilitante y devuelve las llaves infractoras. Resultado: 37 operaciones con el mismo patrón (0,42 % de 8 740). El hallazgo se entrega con la cifra y la muestra de registros, para que el evaluador determine su materialidad.

## Errores frecuentes

Describir una dimensión sin codificar el control que la verifica; inventar el umbral o la columna que la regla no declara; devolver un veredicto de cumplimiento en lugar de la lista de infractores; entregar sin una muestra de registros que evidencie el fallo; producir un resultado silencioso ante un insumo vacío en vez de fallar con mensaje; un control cuya suma de infractores y conformes no reconcilia con el total.

## Lista de verificación antes de entregar

Cada regla de ciclo de vida aplicable está codificada y nombra su columna y llave; los umbrales están en CONFIG con su origen; cada control devuelve nº evaluado, nº infractor, % y muestra de llaves; el notebook corre limpio en kernel reiniciado, es idempotente y falla ante insumo vacío; infractores + conformes = total por control; lo faltante está en «## Brechas de evidencia».


---

## Referencias

- **BCBS239** — BCBS 239 — Principles for effective risk data aggregation and risk reporting (2013-01). *[referencia internacional canónica]*
- **SR11-7** — Federal Reserve SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management (2011-04-04). *[referencia internacional canónica]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
