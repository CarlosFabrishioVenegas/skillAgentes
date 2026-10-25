# Metodología — Control de Documentación

**Estándar y gobierno de la documentación de modelos**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A5 · Control de Documentación  
Documento de Metodología · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [Checklist de completitud documental](#checklist-de-completitud-documental)
- [Defectos formales que rompen la auditabilidad](#defectos-formales-que-rompen-la-auditabilidad)
- [Cierre de observaciones previas](#cierre-de-observaciones-previas)
- [Estados y severidad](#estados-y-severidad)
- [Referencias cruzadas a otros controles](#referencias-cruzadas-a-otros-controles)
- [Anexo — Tabla maestra de umbrales cuantitativos](#anexo-tabla-maestra-de-umbrales-cuantitativos)
- [Anexo — Distinción entre tipos de insuficiencia](#anexo-distincion-entre-tipos-de-insuficiencia)
- [Ejemplo trabajado — fila de la matriz documental](#ejemplo-trabajado-fila-de-la-matriz-documental)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## Checklist de completitud documental

El manual completo cubre nueve bloques: (1) propósito y alcance; (2) datos, con fuentes, definiciones y evaluación de calidad; (3) metodología y supuestos; (4) calibración; (5) pruebas de desempeño; (6) limitaciones y usos válidos; (7) controles y gobierno; (8) historial de cambios y versionado; (9) resultados de la validación previa. La ausencia de cualquiera de estos bloques, cuando el estándar lo exige para el tier, genera hallazgo. El control produce una matriz con una fila por actividad de Documentación del estándar VIRF; el número de filas lo fija el estándar, no el validador.

## Defectos formales que rompen la auditabilidad

Se marcan como defecto: secciones en blanco o con 'por definir' o 'pendiente'; anexos referenciados y no entregados; gráficos sin fuente; tablas sin unidad; ausencia de control de versiones, de autor o de fecha de aprobación; referencias cruzadas rotas. Un manual sin fecha ni versión se marca 'Cumple con observación' en Tier 3 y 'No cumple' en Tier 1 y Tier 2, porque impide acreditar vigencia. Contenido correcto ubicado en un documento no formal (una PPT de comité) acredita el contenido pero genera observación por ubicación.

## Cierre de observaciones previas

El control verifica el cierre documental de las observaciones de la validación anterior. Una observación declarada 'cerrada' sin manual actualizado que lo evidencie **no está cerrada**: la declaración del equipo sin evidencia adjunta se clasifica 'Vigente en plazo' o 'Vencida' según la fecha comprometida. Una observación vencida por más de un ciclo se escala a hallazgo de gobierno.

## Estados y severidad

Estados posibles: Cumple; Cumple con observación (contenido presente con defecto formal); No cumple (contenido ausente exigido, o versión distinta a la productiva); No verificable (documento existe pero no fue entregado o es ilegible); No evidenciado (no hay documento que aborde la actividad). La severidad se asigna por el efecto sobre la capacidad de un tercero de reconstruir y auditar el modelo, no por el esfuerzo de remediación: la ausencia del manual metodológico es crítica; una errata de numeración es baja.

## Referencias cruzadas a otros controles

El control marca los hallazgos documentales con impacto en otros controles mediante referencia cruzada: un manual que documenta una funcionalidad que el código no implementa es hallazgo de Documentación (documenta lo inexistente) y se referencia a Implementación; contenido metodológico que solo existe en una PPT es hallazgo de ubicación y se referencia a Metodología. La referencia cruzada conserva el hallazgo en su control de origen y evita la doble contabilidad en la consolidación final.

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

## Ejemplo trabajado — fila de la matriz documental

| ID VIRF | Actividad | Documento | Estado | Sustento | Fuente | Acción |
|---|---|---|---|---|---|---|
| ACT-DOC-04 | Documentar la ventana de desempeño | Manual metodológico | Cumple con observación | El manual define 12 meses y el acta 18; coexisten sin conciliación | `Manual_v3.pdf > 3.1 > p.14` vs. `Acta_MOD-0412.docx > uso > p.2` | Emitir manual v3.1 con la conciliación — 2026-09-30 |


## Glosario

| Término | Definición |
|---|---|
| **Vigencia documental** | Correspondencia entre la versión documentada y la versión productiva del modelo. |
| **Ubicación no formal** | Contenido que existe solo en PPT, correo u otro soporte no versionado. |
| **Cierre de observación** | Subsanación acreditada con evidencia nueva citada, no con una declaración verbal. |
| **Control de versiones** | Registro de versión, autor, fecha y aprobación de cada documento. |
| **Cobertura documental** | Porcentaje de actividades del estándar efectivamente evidenciadas. |

## Errores frecuentes

- Dar por cubierta una actividad porque 'el equipo lo explicó en la reunión', sin documento formal.
- Cerrar una observación previa por declaración del equipo, sin manual actualizado.
- Marcar 'Cumple' una documentación de mayor calidad que corresponde a otra versión del modelo.
- Consolidar varias actividades del estándar en una sola fila de la matriz.
- Emitir el control como satisfactorio con cobertura documental inferior al 100 %.

## Lista de verificación antes de concluir

1. ¿La matriz tiene una fila por actividad de Documentación aplicable al tier?
2. ¿Se evaluaron por separado completitud, vigencia y coherencia?
3. ¿Se contrastó la versión documentada contra la productiva del acta y del código?
4. ¿Las observaciones del ciclo anterior tienen evidencia de cierre citada?
5. ¿Los defectos formales (sin versión, sin fecha, anexos faltantes) están listados?
6. ¿La cobertura de actividades alcanza el 100 %?


---

## Referencias

- **SR11-7** — Federal Reserve SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management (2011-04-04). *[referencia internacional canónica]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
