# Fundamentos — Entendimiento inicial (Paso 0)

**Taxonomía de modelos financieros y de riesgo**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A4 · Entendimiento inicial (Paso 0)  
Documento de Fundamentos · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [Value at Risk (VaR)](#value-at-risk-var)
- [ALM y Liquidity at Risk (LaR)](#alm-y-liquidity-at-risk-lar)
- [Modelos conductuales (behavioral)](#modelos-conductuales-behavioral)
- [Modelos IFRS 9](#modelos-ifrs-9)
- [Consecuencias de una mala tipificación](#consecuencias-de-una-mala-tipificacion)
- [Anexo — El control dentro del flujo de validación VIRF](#anexo-el-control-dentro-del-flujo-de-validacion-virf)
- [Anexo — Semáforo de estados del sistema](#anexo-semaforo-de-estados-del-sistema)
- [Anexo — Ciclo de vida del modelo y ubicación de la validación](#anexo-ciclo-de-vida-del-modelo-y-ubicacion-de-la-validacion)
- [Ejemplo trabajado — eslabón de la cadena del modelo](#ejemplo-trabajado-eslabon-de-la-cadena-del-modelo)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## Value at Risk (VaR)

El VaR estima la pérdida potencial máxima de una cartera a un horizonte y nivel de confianza dados; formalmente, es el cuantil de la distribución de pérdidas: `P(L > VaR_alpha) = 1 - alpha`. Sus inputs son los factores de mercado (tasas, precios, spreads, volatilidades) y las posiciones; su output es una cifra de pérdida a un percentil. Se usa para límites de trading y para el requerimiento de capital por riesgo de mercado. Su **limitación** esencial es doble: no describe la severidad de la cola más allá del cuantil, y en general no es subaditivo (el VaR de una cartera puede exceder la suma de los VaR de sus partes), lo que motiva su complemento con el Expected Shortfall.

## ALM y Liquidity at Risk (LaR)

Los modelos de gestión de activos y pasivos (**ALM**) proyectan flujos contractuales y conductuales sobre curvas de tasas para medir el riesgo estructural de balance. Sus outputs son las brechas de liquidez y de tasa, y la sensibilidad del **margen financiero (NII)** y del **valor económico del patrimonio (EVE)** ante movimientos de tasas. Se usan en la gestión de balance y en el riesgo de tasa del *banking book* (IRRBB). El **LaR** cuantifica el riesgo de liquidez bajo escenarios de estrés, estimando la posible salida neta de fondos en un horizonte.

## Modelos conductuales (behavioral)

Modelan el comportamiento del cliente para asignar vencimientos efectivos donde el contrato no los fija o el cliente puede desviarse de ellos: **prepago** de créditos, **depósitos sin vencimiento (NMD)** y *runoff* de carteras. Producen perfiles de vencimiento y **duración conductual** que alimentan el ALM. Su limitación central es la dependencia de la estabilidad de los patrones históricos: un cambio de entorno (tasas, competencia, digitalización) puede quebrar el comportamiento observado y volver el modelo procíclico.

## Modelos IFRS 9

Estiman la **pérdida crediticia esperada (ECL)** a partir de la probabilidad de incumplimiento (PD), la severidad (LGD) y la exposición al incumplimiento (EAD), con enfoque prospectivo (*forward-looking*) que incorpora escenarios macroeconómicos. Su output son las provisiones por pérdida esperada que impactan directamente los estados financieros y la gestión del riesgo de crédito. La clasificación en etapas (staging) determina si la pérdida se mide a 12 meses o a toda la vida del instrumento.

## Consecuencias de una mala tipificación

Tipificar mal un modelo en el Paso 0 propaga el error a todo el ciclo: un modelo de mercado tratado como de crédito recibiría las actividades equivocadas del estándar, y un modelo conductual no reconocido perdería la validación de su estabilidad de comportamiento. Por eso el Paso 0 caracteriza el tipo con precisión y declara las dependencias aguas arriba y abajo: si el output alimenta a otro modelo, el impacto de un hallazgo se propaga y debe señalarse desde el inicio.

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

## Ejemplo trabajado — eslabón de la cadena del modelo

Un eslabón correcto de transformación, con cita en ambas fuentes:

> 'Se excluyen clientes con menos de 6 meses de antigüedad (112 340 de 1 240 118 registros, 9,1 %) antes del cálculo del score. Fuente: `Manual_Metodologico_PD_Retail_v3.pdf > 4.1 > p.22`; `pipeline_pd.py > filtrar_universo() > línea 88`.'

El eslabón cita la regla en el manual y su realización en el código, de modo que el control de Implementación pueda contrastar ambos.

## Glosario

| Término | Definición |
|---|---|
| **VaR** | Value at Risk: cuantil de pérdida a un horizonte y nivel de confianza dados. |
| **NII / EVE** | Margen financiero neto y valor económico del patrimonio; métricas de riesgo de tasa. |
| **NMD** | Non-maturity deposits: depósitos sin vencimiento contractual definido. |
| **Duración conductual** | Vencimiento efectivo estimado a partir del comportamiento observado, no del contrato. |
| **Estado de admisibilidad** | Clasificación de la herramienta que condiciona el inicio del control de Implementación. |

## Errores frecuentes

- Rellenar vacíos con conocimiento general de cómo 'suelen' funcionar estos modelos en la banca.
- Convertir una declaración verbal del equipo en un hecho documentado del entendimiento.
- Entregar la infografía sin el documento, o con datos que no aparecen en el documento.
- Omitir el estado de admisibilidad de la herramienta, dejando sin base al control de Implementación.
- Declarar el modelo 'entendido' con completitud inferior al 80 % en lugar de 'Entendimiento parcial'.

## Lista de verificación antes de concluir

1. ¿La cadena input→output→uso está completa y con cita en cada eslabón?
2. ¿Se declaró el estado de admisibilidad de la herramienta?
3. ¿La tabla de discrepancias entre manual, acta y minutas está resuelta o escalada?
4. ¿El mapa de evidencia asigna documentos a los seis controles con rutas exactas?
5. ¿La infografía respeta la regla de no contener datos ausentes del documento?
6. ¿La completitud del entendimiento alcanza al menos el 80 %?


---

## Referencias

- **JORION** — Jorion, P., Value at Risk: The New Benchmark for Managing Financial Risk (3.ª ed.). *[referencia internacional canónica]*
- **IFRS9** — IFRS 9 / NIIF 9 — Financial Instruments, sección 5.5 (deterioro y ECL). *[referencia internacional canónica]*
- **BASEL-IRB** — Basel Framework — Internal Ratings-Based approach y use test. *[referencia internacional canónica]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
