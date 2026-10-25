# Metodología — Validador Final (consolidación)

**Validación integral, informe y conclusión**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A11 · Validador Final (consolidación)  
Documento de Metodología · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [Control de cobertura](#control-de-cobertura)
- [La tabla de 8 columnas](#la-tabla-de-8-columnas)
- [Reglas de conclusión](#reglas-de-conclusion)
- [Trazabilidad y devolución](#trazabilidad-y-devolucion)
- [Plan de acción consolidado y anexo de trazabilidad](#plan-de-accion-consolidado-y-anexo-de-trazabilidad)
- [Anexo — Tabla maestra de umbrales cuantitativos](#anexo-tabla-maestra-de-umbrales-cuantitativos)
- [Anexo — Distinción entre tipos de insuficiencia](#anexo-distincion-entre-tipos-de-insuficiencia)
- [Ejemplo trabajado — fila de la tabla de 8 columnas](#ejemplo-trabajado-fila-de-la-tabla-de-8-columnas)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## Control de cobertura

El primer paso es la **cobertura**: se cruza la lista de actividades del estándar aplicables al tier contra las filas efectivamente recibidas. Toda actividad sin fila se incorpora como 'No evidenciado' con el agente responsable indicado. Se reporta el porcentaje de cobertura por control y global antes de la tabla. Una cobertura inferior al 100 % se concluye como 'Validación incompleta', nunca como satisfactoria: el buen resultado de lo evaluado no compensa lo no evaluado.

## La tabla de 8 columnas

El formato único de consolidación tiene ocho columnas: Ámbito; Control cuantitativo o cualitativo; Actividad (con ID); Cumple o no; Resultado (la cifra dura, sin adjetivos); Evaluación sustentada (el razonamiento y el riesgo); Fuente revisada (cita exacta); y Acción pendiente (con responsable y fecha, o 'Ninguna'). Una fila se clasifica como cuantitativa si el juicio se sostiene en una cifra, y como cualitativa si se sostiene en existencia, coherencia o suficiencia documental.

## Reglas de conclusión

Se aplican sin excepción: un 'No cumple' de severidad crítica en Implementación o Usos impide concluir 'Validación satisfactoria'; la ausencia total de evidencia de uso obliga a la recomendación de retiro, reproducida en la conclusión; una cobertura inferior al 100 % se emite como 'Validación incompleta'; una observación del ciclo anterior vencida por más de un ciclo genera un hallazgo de gobierno adicional. La conclusión se redacta en un máximo de doce líneas y **después** de la tabla, nunca antes.

## Trazabilidad y devolución

La columna de fuente conserva la cita original del agente que produjo la fila, sin abreviar, y cada fila indica su agente de origen, de modo que cualquier hallazgo pueda rastrearse hasta la evidencia. Un control sin cita exacta se devuelve, no se incorpora con la nota 'sin fuente', porque eso normalizaría el defecto. Dos agentes con estados distintos sobre el mismo hecho no se promedian: se documentan ambos y se marca 'Inconsistencia entre controles'.

## Plan de acción consolidado y anexo de trazabilidad

El validador construye el plan de acción consolidado —acción, responsable, fecha comprometida, control de origen y severidad, ordenado por fecha— y el anexo de trazabilidad con las evidencias leídas y sus hashes SHA-256, las evidencias esperadas y no recibidas, y las consultas abiertas con su estado. Registra la fecha de corte de la evidencia, para que el lector sepa hasta cuándo alcanza el juicio. Un hallazgo cuya remediación depende de otra área conserva su severidad y registra la dependencia en el plan.

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
- **SBS-053-2023** — Resolución SBS N° 00053-2023 — Reglamento de Gestión de Riesgos de Modelo (Lima, 06-01-2023; mod. Res. 3421-2023 y 3884-2024). *[validada — fuente primaria SBS]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
