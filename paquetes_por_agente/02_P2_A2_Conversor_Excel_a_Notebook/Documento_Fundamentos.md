# Fundamentos — Conversor de herramienta Excel a notebook

**Reproducibilidad y riesgo de hoja de cálculo**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A2 · Conversor de herramienta Excel a notebook  
Documento de Fundamentos · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [El riesgo de la hoja de cálculo](#el-riesgo-de-la-hoja-de-calculo)
- [Reproducibilidad como criterio de validación](#reproducibilidad-como-criterio-de-validacion)
- [Principio de fidelidad, no de mejora](#principio-de-fidelidad-no-de-mejora)
- [Frontera entre traducción y validación](#frontera-entre-traduccion-y-validacion)
- [Anexo — El control dentro del flujo de validación VIRF](#anexo-el-control-dentro-del-flujo-de-validacion-virf)
- [Anexo — Semáforo de estados del sistema](#anexo-semaforo-de-estados-del-sistema)
- [Anexo — Ciclo de vida del modelo y ubicación de la validación](#anexo-ciclo-de-vida-del-modelo-y-ubicacion-de-la-validacion)
- [Ejemplo trabajado — fila de reconciliación](#ejemplo-trabajado-fila-de-reconciliacion)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## El riesgo de la hoja de cálculo

Las hojas de cálculo son la herramienta de modelado más extendida y, a la vez, una de las más frágiles. La evidencia recopilada por el European Spreadsheet Risks Interest Group (EuSpRIG) documenta que una fracción elevada de las hojas complejas contiene errores materiales, y que el riesgo crece con las fórmulas anidadas, las referencias manuales, las celdas de cálculo endurecido (valores pegados donde debería haber fórmula), las hojas ocultas con parámetros vivos y la ausencia de control de versiones.

La migración a un notebook de Python no es una mejora estética: convierte un artefacto opaco y difícil de auditar en uno versionable, testeable y reproducible, que es precondición para los controles de Implementación y de Calidad de Datos. Un Excel no reproducible es un modelo que no puede validarse con garantías.

## Reproducibilidad como criterio de validación

Un modelo es reproducible cuando, con los mismos insumos, produce los mismos resultados en cualquier entorno y momento. Esto exige entornos deterministas (versiones de librerías fijadas en un archivo de requisitos), **semilla aleatoria declarada** en todo proceso estocástico (Monte Carlo, bootstrap), y separación estricta entre datos, lógica y parámetros de configuración. Sin reproducibilidad, ninguna conclusión de validación es defendible ante un tercero, porque no puede distinguirse un resultado del modelo de un artefacto del entorno.

## Principio de fidelidad, no de mejora

La conversión replica la producción, no la corrige. Si el Excel calcula algo de forma discutible, el notebook lo replica idénticamente y lo reporta como observación; la validación evalúa lo que existe en producción, no lo que debería existir. Introducir 'mejoras' durante la traducción rompe la equivalencia, contamina el juicio y hace imposible la reconciliación. El agente que 'arregla' una fórmula deja de estar validando el modelo real.

## Frontera entre traducción y validación

Este agente traduce y reconcilia, pero no emite el juicio de Implementación: ese juicio corresponde al control C4, que consume el notebook y su tabla de reconciliación. La frontera es importante: el conversor reporta lo no traducible (macros VBA, conexiones externas) como riesgo, y deja constancia de las diferencias no reconciliadas, pero es el control de Implementación quien decide si esas diferencias son hallazgos que bloquean el cierre. Separar ambos roles preserva la trazabilidad.

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

## Ejemplo trabajado — fila de reconciliación

La tabla de reconciliación evidencia la equivalencia numérica:

| Salida | Valor Excel | Valor notebook | Dif. abs. | Dif. rel. | Estado |
|---|---|---|---|---|---|
| PD media cartera | 0.031400 | 0.031400 | 0.000000 | 0.0e+00 | Reconciliado |
| Provisión total | 12 480 331.20 | 12 480 018.55 | 312.65 | 2.5e-05 | No reconciliado — revisar redondeo en `Calculo > H45` |

La segunda fila no cierra dentro de tolerancia y obliga a investigar el punto de redondeo antes de aceptar el notebook como equivalente.

## Glosario

| Término | Definición |
|---|---|
| **Cálculo endurecido** | Valor pegado como texto en una celda donde debería existir una fórmula; rompe la reproducibilidad. |
| **Reconciliación** | Comparación cifra a cifra entre la salida del Excel y la del notebook dentro de una tolerancia. |
| **Golden set** | Conjunto congelado de casos de prueba con resultados conocidos para verificar la equivalencia. |
| **Idempotencia** | Propiedad de que ejecutar dos veces el mismo proceso produzca el mismo resultado. |
| **Tolerancia (atol/rtol)** | Margen absoluto y relativo admitido al comparar dos números en punto flotante. |

## Errores frecuentes

- Traducir `SI.ERROR` rellenando con 0 por omisión, lo que oculta pérdidas de registros o divisiones inválidas.
- Refactorizar la lógica de negocio o renombrar variables de forma que se pierda la trazabilidad con la hoja.
- Omitir hojas ocultas o auxiliares por parecer irrelevantes, cuando contienen parámetros vivos.
- Entregar el notebook sin la tabla de reconciliación o con salidas 'no reconciliadas' sin explicación.
- Recortar rangos que apuntan a filas vacías sin anotar el cambio, alterando promedios y conteos.

## Lista de verificación antes de concluir

1. ¿El notebook ejecuta limpio de principio a fin en un kernel reiniciado?
2. ¿Existe tabla de reconciliación y todas las salidas cierran dentro de tolerancia?
3. ¿Cada parámetro y función lleva comentario con su celda de origen?
4. ¿La semilla aleatoria está fijada y declarada?
5. ¿Las hojas ocultas y las macros VBA quedaron inventariadas y evaluadas?
6. ¿La tolerancia de reconciliación fue aprobada por el dueño del modelo?


---

## Referencias

- **EUSPRIG** — European Spreadsheet Risks Interest Group (EuSpRIG) — buenas prácticas de hojas de cálculo. *[referencia internacional canónica]*
- **SR11-7** — Federal Reserve SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management (2011-04-04). *[referencia internacional canónica]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
