# Fundamentos — Evaluador de controles e informe de calidad de datos

**Interpretación de los controles ejecutados y redacción del informe detallado**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A3E · Evaluador de controles e informe de calidad de datos  
Documento de Fundamentos · Versión 2.0 · 2026-09-15


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [La evaluación como interpretación de controles ejecutados](#la-evaluacion-como-interpretacion-de-controles-ejecutados)
- [Materialidad, causa raíz y severidad](#materialidad-causa-raiz-y-severidad)
- [Las cuatro insuficiencias aplicadas a datos](#las-cuatro-insuficiencias-aplicadas-a-datos)
- [Frontera: recibe de A3D, alimenta a A6](#frontera-recibe-de-a3d-alimenta-a-a6)
- [Anexo — El control dentro del flujo de validación VIRF](#anexo-el-control-dentro-del-flujo-de-validacion-virf)
- [Anexo — Semáforo de estados del sistema](#anexo-semaforo-de-estados-del-sistema)
- [Anexo — Ciclo de vida del modelo y ubicación de la validación](#anexo-ciclo-de-vida-del-modelo-y-ubicacion-de-la-validacion)
- [Ejemplo trabajado — subsección de hallazgo](#ejemplo-trabajado-subseccion-de-hallazgo)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de entregar](#lista-de-verificacion-antes-de-entregar)


---

## La evaluación como interpretación de controles ejecutados

Este agente no vuelve a medir ni a detectar: recibe los controles ya ejecutados y los hallazgos del detector A3D (Paso 5) y los convierte en un **informe detallado** que dice qué se controló, qué pasó, con qué gravedad y qué debe remediarse. Su materia prima son cifras y registros infractores; su producto es un juicio técnico trazable. Interpreta y narra con evidencia, sin recalcular a mano lo que el notebook ya produjo y sin detectar fallos nuevos.

## Materialidad, causa raíz y severidad

Dos defectos del mismo tamaño no pesan igual. La **materialidad** se fija por el impacto en el output del modelo, no por la frecuencia: un 2 % de nulos en un campo informativo y un 2 % en el saldo que alimenta la provisión tienen severidades distintas. Para cada patrón, el agente propone una **causa raíz** a partir de los ejemplos infractores (saldos que resucitan → reproceso mal aplicado; doble cancelación → carga duplicada) y asigna una **severidad** (alta, media, baja) justificada en la materialidad. Sin esa cadena impacto → causa → severidad, el hallazgo no orienta la remediación.

## Las cuatro insuficiencias aplicadas a datos

El agente distingue cuatro situaciones que disparan acciones distintas: el control **no existe** (nadie lo definió) → solicitar; **existe pero no se ejecutó** → exigir ejecución; **se ejecutó y falló** → remediar; **no verificable** (sin cita reproducible o umbral [SUPUESTO]) → declarar y pedir sustento. Confundir «no existe» con «falló» desvía por completo la remediación.

## Frontera: recibe de A3D, alimenta a A6

El agente se sitúa entre el detector A3D (Paso 5), del que recibe los controles y hallazgos, y el control de negocio de Calidad de Datos A6 (Paso 7), al que entrega el informe técnico como insumo del juicio final. No detecta (esa es la función de A3D) ni emite el veredicto de negocio del control (esa es la de A6): produce la evaluación técnica que ambos extremos necesitan.

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

## Ejemplo trabajado — subsección de hallazgo

«Regla: monotonía de amortización. Resultado: 214 operaciones (2,4 % de 8 740) con saldo creciente sin desembolso documentado. Ejemplos: op. 004512, 007781. Causa raíz probable: reproceso de refinanciados sin marca de evento. Materialidad: alta —el saldo alimenta la provisión IFRS 9—. Severidad: alta. Estado: No cumple. Remediación: corregir la marca de evento en la carga y re-ejecutar el control (Gobierno del dato, próximo cierre).»

## Errores frecuentes

Marcar «Cumple» sin cita reproducible o sobre un umbral [SUPUESTO]; recalcular a mano lo que el notebook produjo; confundir «no existe» con «falló»; dar una severidad sin justificarla en la materialidad; entregar un informe sin ejemplos de registros infractores; usar adjetivos evaluativos sin la cifra que los sustente.

## Lista de verificación antes de entregar

Cada regla del Paso 5 aparece con estado, porcentaje de cumplimiento, diagnóstico con cifra y referencia; ningún «Cumple» sin cita; los [SUPUESTO] quedan como «No verificable»; el resumen ejecutivo precede al detalle; la matriz de 8 columnas está completa; los hallazgos que afectan a otros controles llevan su referencia cruzada; hay un plan de remediación priorizado por severidad.


---

## Referencias

- **BCBS239** — BCBS 239 — Principles for effective risk data aggregation and risk reporting (2013-01). *[referencia internacional canónica]*
- **SR11-7** — Federal Reserve SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management (2011-04-04). *[referencia internacional canónica]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
