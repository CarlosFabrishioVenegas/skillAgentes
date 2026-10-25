# Metodología — Control de Calidad de Datos (juicio de negocio)

**BCBS 239 y materialidad del defecto de datos**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A6 · Control de Calidad de Datos (juicio de negocio)  
Documento de Metodología · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [Evaluación del marco de control, no solo del resultado](#evaluacion-del-marco-de-control-no-solo-del-resultado)
- [Materialidad y priorización](#materialidad-y-priorizacion)
- [Linaje como condición](#linaje-como-condicion)
- [Reglas de estado](#reglas-de-estado)
- [Reconciliación de conteos](#reconciliacion-de-conteos)
- [Anexo — Tabla maestra de umbrales cuantitativos](#anexo-tabla-maestra-de-umbrales-cuantitativos)
- [Anexo — Distinción entre tipos de insuficiencia](#anexo-distincion-entre-tipos-de-insuficiencia)
- [Ejemplo trabajado — evaluación con impacto](#ejemplo-trabajado-evaluacion-con-impacto)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## Evaluación del marco de control, no solo del resultado

Un modelo cuyos datos están limpios pero cuyo marco de control no está documentado no cumple el control. Se evalúa si el banco definió el control, si está documentado, si tiene umbral, si tiene responsable y si se ejecuta con la periodicidad declarada. Un **umbral cumplido por construcción** —porque se eliminan los registros que lo incumplirían— es hallazgo crítico de circularidad: el control no detecta nada porque el defecto se elimina antes de medir.

## Materialidad y priorización

Los hallazgos se priorizan por materialidad, no por número de defectos: un defecto en la variable de mayor peso del score supera a diez en variables informativas. Cada hallazgo responde tres preguntas en su evaluación: qué variable se afecta, qué peso tiene esa variable en el modelo, y en qué dirección y magnitud se mueve el output. Si el peso de la variable no está documentado, es a su vez un hallazgo de Metodología y se referencia cruzadamente.

## Linaje como condición

El linaje es condición, no opcional: cada campo del modelo debe tener origen identificado (sistema, tabla, campo) y responsable. En Tier 1 y Tier 2, la ausencia de linaje es hallazgo crítico, porque impide rastrear el dato hasta su origen y verificar sus transformaciones. Un reproceso histórico que cambia datos de ciclos ya validados es hallazgo de trazabilidad y exige la política de reproceso.

## Reglas de estado

Cualquier dimensión en 'No cumple' sobre una variable usada por el modelo impide concluir 'Cumple'. Cualquier dimensión en 'No evidenciado' impide 'Cumple' y produce como mínimo 'Cumple con observación' con acción de entrega. Una base entregada ya depurada convierte las dimensiones afectadas en 'No verificable', porque el control pierde capacidad de detección; se exige la base previa a la depuración.

## Reconciliación de conteos

Cuando el conteo del notebook difiere del reporte del equipo, el agente no elige una cifra: documenta ambas, su diferencia y solicita reconciliación formal antes de continuar. Un dataset con más filas que el ciclo anterior sin explicación obliga a verificar si hubo cambio de universo; un cambio de universo no declarado es hallazgo de datos y de gobierno a la vez. Estas reconciliaciones se resuelven antes de emitir el juicio, porque una diferencia de conteo no explicada invalida cualquier conclusión de calidad.

## Anexo — Tabla maestra de umbrales cuantitativos

Referencia consolidada de los umbrales usados en el sistema. **Todos son convenciones de industria y deben calibrarse y aprobarse en la política interna de validación**; no son mínimos regulatorios salvo donde se indique.

| Métrica | Umbral / criterio | Interpretación |
|---|---|---|
| PSI | < 0.10 / 0.10–0.25 / ≥ 0.25 | estable / moderado / significativo |
| CSI | mismos cortes que PSI | por variable de entrada |
| z-score (outlier) | \|z\| > 3 | atípico univariado |
| IQR (outlier) | fuera de [Q1−1.5·IQR, Q3+1.5·IQR]; extremo 3.0·IQR | robusto ante colas |
| VaR z (95% / 99%) | 1.645 / 2.326 | factor normal |
| Semáforo Basilea (250 d) | 0–4 / 5–9 / 10+ | verde / amarillo / rojo |
| Multiplicador de capital | 3.0 → 4.0 | según zona del semáforo |
| Expected Shortfall (FRTB) | nivel 97.5% | reemplaza al VaR en IMA |
| AUC | > 0.7 aceptable; > 0.8 bueno | discriminación |
| Gini | 0.4–0.6 típico minorista | = 2·AUC − 1 |
| KS | > 0.3 razonable | separación de distribuciones |
| Tolerancia de reconciliación | rtol 1e-6 a 1e-8 | equivalencia numérica |


## Anexo — Distinción entre tipos de insuficiencia

El sistema distingue con precisión tres situaciones que producen acciones distintas y jamás deben confundirse en una misma redacción: el control o la evidencia **NO EXISTE** (nadie lo definió o no se entregó), en cuyo caso el estado es 'No evidenciado' y la acción es solicitar la entrega; el control **EXISTE PERO NO SE EJECUTÓ** en el ciclo, en cuyo caso la acción es exigir su ejecución; y el control **SE EJECUTÓ Y FALLÓ**, en cuyo caso la acción es la remediación del defecto. Confundir 'no existe' con 'falló' oculta la naturaleza del problema y desvía la remediación. A ello se suma 'No verificable', reservado para la evidencia que existe pero no es citable ni reproducible.

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
