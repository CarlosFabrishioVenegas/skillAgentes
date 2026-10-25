# Fundamentos — Kick-off — Presentación de entendimiento (Alcance, Limitaciones y Flujo de Datos)

**Comunicación del entendimiento y alineamiento del kick-off**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente AK · Kick-off — Presentación de entendimiento (Alcance, Limitaciones y Flujo de Datos)  
Documento de Fundamentos · Versión 2.0 · 2026-09-14


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [Qué es el kick-off de la validación](#que-es-el-kick-off-de-la-validacion)
- [Las dos láminas del kick-off](#las-dos-laminas-del-kick-off)
- [Alcance y limitaciones: dos planos distintos](#alcance-y-limitaciones-dos-planos-distintos)
- [El flujo de datos como base común](#el-flujo-de-datos-como-base-comun)
- [Fidelidad al entendimiento y frontera con la evaluación](#fidelidad-al-entendimiento-y-frontera-con-la-evaluacion)
- [Anexo — El control dentro del flujo de validación VIRF](#anexo-el-control-dentro-del-flujo-de-validacion-virf)
- [Anexo — Semáforo de estados del sistema](#anexo-semaforo-de-estados-del-sistema)
- [Anexo — Ciclo de vida del modelo y ubicación de la validación](#anexo-ciclo-de-vida-del-modelo-y-ubicacion-de-la-validacion)
- [Ejemplo trabajado — bloque de la Lámina 2](#ejemplo-trabajado-bloque-de-la-lamina-2)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)


---

## Qué es el kick-off de la validación

El kick-off es la reunión que abre el ciclo de validación una vez producido el entendimiento del Paso 0. Su función no es evaluar el modelo, sino **alinear** al equipo dueño, al validador y a los interesados sobre una base común de hechos antes de ejecutar los seis controles. La presentación del kick-off traduce el documento de entendimiento consolidado (A4_paso0.md) a dos láminas legibles en una reunión: una de alcance y limitaciones, y otra del flujo de datos de extremo a extremo. Si la reunión parte de interpretaciones distintas del modelo, cada control heredará esa ambigüedad; por eso el kick-off fija el perímetro y el vocabulario del ciclo.

## Las dos láminas del kick-off

La presentación tiene exactamente dos láminas, y ninguna sustituye a la otra. La **Lámina 1 — Alcance y Limitaciones** delimita qué se valida y bajo qué condiciones el modelo es válido. La **Lámina 2 — Flujo de datos** muestra la cadena `Input de Datos → Tratamiento y resultado de los datos → Usuarios Finales` en tres cajas conectadas. Juntas responden a las tres preguntas que abren cualquier validación: qué hace el modelo, de dónde salen sus datos y quién usa su resultado. La presentación se entrega en un formato apto para trasladar a PowerPoint, pero su contenido —no su estética— es lo que se valida.

## Alcance y limitaciones: dos planos distintos

El **alcance** describe el propósito de negocio, el uso autorizado y el perímetro (productos, carteras o mesas a las que aplica el modelo). Las **limitaciones** describen el borde de validez: los supuestos declarados y las condiciones fuera de las cuales el modelo no debe usarse. Son planos distintos y fallan de forma distinta: un modelo puede tener un alcance claro y limitaciones mal declaradas, o viceversa. Los supuestos y las limitaciones se transcriben de forma **literal**, entre comillas, porque su redacción exacta es el criterio contra el cual el control de Usos contrastará el empleo real del modelo y el de Metodología sus condiciones de validez. Parafrasearlos desplaza ese criterio.

## El flujo de datos como base común

La Lámina 2 reconstruye la cadena del dato en tres eslabones. **Input de Datos**: de dónde salen las bases —sistemas, tablas y responsables de cada fuente principal—. **Tratamiento y resultado de los datos**: la secuencia de transformaciones (filtros, construcción de variables, cálculo, calibración) y el output que produce el modelo (curva, score, porcentaje, provisión). **Usuarios Finales**: a quién va dirigido el output, en qué foro o sistema se expone, con qué periodicidad y qué decisión se toma con él. Esta lámina es el mapa que orienta simultáneamente a Calidad de Datos (el input), a Metodología e Implementación (el tratamiento) y a Usos (los usuarios finales).

## Fidelidad al entendimiento y frontera con la evaluación

La fuente principal y suficiente de la presentación es A4_paso0.md; el kick-off no genera conocimiento nuevo, lo comunica. Cada afirmación de las dos láminas se remite al entendimiento con su cita, y todo elemento que el entendimiento no sustente se marca 'No evidenciado' en lugar de completarse. El kick-off **no emite juicios de cumplimiento** ni recomendaciones de aprobación: eso corresponde a los agentes de control A5 a A10 y al validador final A11. Si el entendimiento está rotulado 'Entendimiento parcial', la presentación lo hereda con una advertencia visible: comunicar como cerrado lo que el Paso 0 dejó abierto es el error más grave del kick-off.

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

## Ejemplo trabajado — bloque de la Lámina 2

Un eslabón correcto de la caja 'Input de Datos', con su cita al entendimiento:

> 'Input de Datos: datamart de crédito DM_CLIENTE y buró externo (score mensual). Fuente: `A4_paso0.md > 4. Inputs`.'

La afirmación remite al entendimiento y nombra la fuente concreta, de modo que la reunión pueda verificarla sin recurrir al equipo dueño.

## Glosario

| Término | Definición |
|---|---|
| **Kick-off** | Reunión que abre el ciclo de validación y alinea a las partes sobre el entendimiento. |
| **Alcance** | Propósito, uso autorizado y perímetro de aplicación del modelo. |
| **Limitación** | Condición o supuesto fuera del cual el modelo no es válido. |
| **Flujo de datos** | Cadena Input → Tratamiento y resultado → Usuarios Finales del modelo. |
| **Ancla (A4_paso0.md)** | Documento de entendimiento del Paso 0, fuente principal y suficiente del kick-off. |

## Errores frecuentes

- Emitir un juicio de cumplimiento o una recomendación de aprobación en el kick-off.
- Parafrasear los supuestos y limitaciones en lugar de transcribirlos literalmente.
- Completar una caja del flujo por analogía con otros modelos, en vez de marcar 'No evidenciado'.
- Presentar como cerrado un entendimiento rotulado 'parcial', sin la advertencia correspondiente.
- Introducir en las láminas datos que no constan en A4_paso0.md.

## Lista de verificación antes de concluir

1. ¿Ambas láminas tienen todos sus elementos citados al entendimiento?
2. ¿Los supuestos y limitaciones están entre comillas y sin parafrasear?
3. ¿La caja 'Input de Datos' nombra fuentes, sistemas y tablas concretas?
4. ¿La caja 'Usuarios Finales' indica destinatario, foro y periodicidad?
5. ¿Todo elemento sin sustento dice 'No evidenciado'?
6. ¿La presentación evita cualquier juicio de cumplimiento?


---

## Referencias

- **SR11-7** — Federal Reserve SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management (2011-04-04). *[referencia internacional canónica]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
