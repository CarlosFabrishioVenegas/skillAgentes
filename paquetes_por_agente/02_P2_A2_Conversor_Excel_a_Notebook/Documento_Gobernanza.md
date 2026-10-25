# Estándares de gobernanza — Conversor de herramienta Excel a notebook

**Reproducibilidad y riesgo de hoja de cálculo**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A2 · Conversor de herramienta Excel a notebook  
Documento de Gobernanza · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [SR 11-7: el estándar maestro de gestión del riesgo de modelo](#sr-11-7-el-estandar-maestro-de-gestion-del-riesgo-de-modelo)
- [BCBS 239: agregación de datos de riesgo y calidad del dato](#bcbs-239-agregacion-de-datos-de-riesgo-y-calidad-del-dato)
- [Marco regulatorio peruano (SBS) — validado contra fuente primaria](#marco-regulatorio-peruano-sbs-validado-contra-fuente-primaria)
- [Las tres líneas de defensa y la segregación de funciones](#las-tres-lineas-de-defensa-y-la-segregacion-de-funciones)
- [Aplicación a la conversión de herramientas](#aplicacion-a-la-conversion-de-herramientas)
- [Doctrina de citación y auditabilidad](#doctrina-de-citacion-y-auditabilidad)
- [Escala de severidad de hallazgos](#escala-de-severidad-de-hallazgos)
- [Anexo — Re-validación por tier y expectativas supervisoras](#anexo-re-validacion-por-tier-y-expectativas-supervisoras)
- [Anexo — Documentación de la propia validación](#anexo-documentacion-de-la-propia-validacion)
- [Anexo — El Reglamento SBS de Gestión de Riesgos de Modelo (Res. N° 00053-2023)](#anexo-el-reglamento-sbs-de-gestion-de-riesgos-de-modelo-res-n-00053-2023)
- [Referencias](#referencias)


---

## SR 11-7: el estándar maestro de gestión del riesgo de modelo

La *Supervisory Guidance on Model Risk Management* (SR 11-7 de la Reserva Federal, publicada el 4 de abril de 2011, y su norma gemela OCC Bulletin 2011-12) es la referencia internacional de la que derivan la mayoría de los marcos internos de validación, incluido el peruano. Define un **modelo** como todo método cuantitativo, sistema o enfoque que aplica teorías, técnicas y supuestos estadísticos, económicos o financieros para transformar datos de entrada en estimaciones cuantitativas. Define el **riesgo de modelo** como el potencial de consecuencias adversas derivadas de decisiones basadas en modelos incorrectos o mal usados, y reconoce dos fuentes: (i) errores fundamentales que producen salidas inexactas respecto del propósito de diseño, y (ii) uso incorrecto o inapropiado del modelo.

El guidance ordena la validación en **tres componentes** que deben estar todos presentes:

1. **Evaluación de la solidez conceptual** (*conceptual soundness*): juzga la calidad del diseño y la construcción, la lógica de la metodología, la razonabilidad de los supuestos y la pertinencia de los datos de desarrollo. Incluye la revisión de la evidencia documental y de la literatura que respalda cada decisión.
2. **Monitoreo continuo** (*ongoing monitoring*): confirma que el modelo se implementó adecuadamente y que sigue siendo apropiado en el tiempo. Comprende la *process verification* (el modelo procesa las entradas y genera las salidas conforme al diseño) y el *benchmarking* (comparación contra modelos o datos alternativos).
3. **Análisis de resultados** (*outcomes analysis*): compara las salidas del modelo con los resultados efectivamente observados. El *backtesting* es su forma cuantitativa más común.

Sobre estos tres componentes se sostiene el principio rector: el **effective challenge**, entendido como el cuestionamiento crítico y objetivo ejercido por partes con **competencia** (conocimiento técnico suficiente), **independencia** (ausencia de conflicto respecto del desarrollo) e **influencia** (autoridad para forzar cambios). Sin los tres atributos, el challenge es cosmético. El guidance exige además un **inventario de modelos** completo, documentación suficiente para la **replicación independiente**, y una clasificación por riesgo y materialidad (*tiering*) que gradúe la intensidad y la frecuencia de la validación.

## BCBS 239: agregación de datos de riesgo y calidad del dato

El documento *Principles for effective risk data aggregation and risk reporting* del Comité de Basilea (BCBS 239, enero de 2013) fija catorce principios que, aunque nacieron para los bancos de importancia sistémica global (que debían cumplirlos desde enero de 2016), se han convertido en el estándar de facto de calidad y gobierno del dato de riesgo. Se agrupan en cuatro bloques más la revisión supervisora:

**Gobierno e infraestructura.** Principio 1 (Gobierno): la agregación de datos y el reporte se sujetan a un marco de gobierno robusto, con responsabilidad del Directorio y la Alta Dirección. Principio 2 (Arquitectura de datos e infraestructura de TI): diseño, mantenimiento y controles que soporten la agregación tanto en condiciones normales como de estrés.

**Capacidad de agregación de datos de riesgo.** Principio 3 (**Exactitud e integridad**): los datos agregados deben ser precisos y confiables, con conciliación y controles automatizados que minimicen el error manual. Principio 4 (**Completitud**): capacidad de capturar y agregar todos los datos materiales de riesgo del grupo. Principio 5 (**Oportunidad**): generación de datos agregados a tiempo, en especial en estrés. Principio 6 (**Adaptabilidad**): capacidad de producir agregaciones ad hoc ante nuevas necesidades y escenarios.

**Prácticas de reporte.** Principios 7 a 11: exactitud del reporte; amplitud (*comprehensiveness*, cubrir todas las áreas de riesgo materiales); claridad y utilidad (reportes comprensibles y accionables); frecuencia adecuada; y distribución a las partes correctas preservando la confidencialidad.

**Revisión supervisora.** Principios 12 a 14: revisión periódica por el supervisor, acciones correctivas y medidas prudenciales, y cooperación entre supervisores.

Para la validación de modelos, BCBS 239 convierte la calidad de datos en un requisito de gobierno auditable: cada defecto de dato debe poder evaluarse por su **materialidad** (impacto en el output del modelo) y todo campo debe tener **linaje** trazable desde el sistema origen.

## Marco regulatorio peruano (SBS) — validado contra fuente primaria

La Superintendencia de Banca, Seguros y AFP (SBS) del Perú cuenta con regulación específica de riesgo de modelo. Las referencias de este marco han sido **validadas contra el texto oficial** de cada resolución (fuente primaria).

**Resolución SBS N° 00053-2023 — Reglamento de Gestión de Riesgos de Modelo** (Lima, 6 de enero de 2023; modificada por las Resoluciones N° 3421-2023 y N° 3884-2024). Es la norma central del proyecto. Define el riesgo de modelo como *la posibilidad de pérdidas o consecuencias adversas derivadas de debilidades en el desarrollo, validación, implementación, uso y seguimiento de los modelos* (Art. 3.1), y la validación como *la revisión independiente del desarrollo, implementación y uso del modelo* (Art. 2, lit. ff). Obliga a: un **inventario de modelos** permanentemente actualizado (Art. 5, remisión anual vía SUCAVE); la **categorización** por materialidad, uso y complejidad, aprobada por el comité de riesgos de modelo (Art. 6); la **validación inicial y periódica** (Art. 20), donde la periódica incluye la validación del uso, la revisión de la categoría y la razonabilidad de los forzajes (*overrides*); la **réplica completa** obligatoria para los modelos de las categorías de mayor riesgo (Art. 20.2.1 y 25.3); y el **Comité de Riesgos de Modelo** con reunión trimestral mínima (Art. 10-11). Su aplicación es gradual y se extiende, según el tipo de riesgo y la categoría, **hasta el 31 de mayo de 2026** (Art. Quinto, tabla sustituida por la Res. N° 3884-2024).

**Resolución SBS N° 272-2017 — Reglamento de Gobierno Corporativo y de la Gestión Integral de Riesgos** (Lima, 18 de enero de 2017; vigente desde el 1 de abril de 2018, reemplaza a la Res. N° 37-2008). Establece la gestión integral de riesgos, la tipología de riesgos (Art. 23), la unidad de riesgos independiente (Art. 24-26), el comité de riesgos (Art. 11-12) y el informe anual de riesgos (Art. 27).

**Resolución SBS N° 4906-2017 — Reglamento para la Gestión del Riesgo de Mercado** (Lima, 20 de diciembre de 2017; vigente desde el 1 de junio de 2018). Exige el modelo interno de VaR por varianza-covarianza, simulación histórica o Montecarlo, con reporte de VaR, SVaR, CVaR y SCVaR (Art. 25); pruebas de estrés y **backtesting trimestrales** (Art. 26-27); y validación de los modelos internos por una unidad independiente (Art. 29). El requerimiento patrimonial por riesgo de mercado se rige por la **Resolución SBS N° 6328-2009**, con factores de ajuste actualizados por la **Resolución N° 525-2024**.

El propio Art. 2 de la Res. N° 00053-2023 cita literalmente el resto del marco sectorial, lo que confirma su numeración: riesgo de crédito (Res. N° 3780-2011), liquidez (Res. N° 9075-2012), operacional (Res. N° 2116-2009), patrimonio por crédito (Res. N° 14354-2009) y auditoría interna (Res. N° 11699-2008).

## Las tres líneas de defensa y la segregación de funciones

El gobierno del riesgo de modelo se organiza en tres líneas de defensa con responsabilidades diferenciadas. La **primera línea** es el negocio y los **dueños del modelo** (*model owners*) y sus **desarrolladores** (*developers*): asumen el riesgo, construyen el modelo y responden por su uso correcto y por la calidad de la documentación. La **segunda línea** es la función de gestión del riesgo de modelo y la **validación independiente**: ejerce el effective challenge, no reporta al desarrollo y tiene autoridad para observar y bloquear. La **tercera línea** es la **auditoría interna**: no revalida modelo por modelo, sino que evalúa la efectividad del marco de gestión del riesgo de modelo en su conjunto.

La **segregación de funciones** entre *model owner*, *developer* y *validator* es condición de independencia: cuando la misma persona o la misma área desarrolla y valida, el challenge pierde objetividad y constituye un hallazgo de gobierno. En modelos de mayor materialidad (Tier 1), la independencia debe ser estricta; en tiers menores puede admitirse una independencia funcional con controles compensatorios, siempre documentados.

## Aplicación a la conversión de herramientas

SR 11-7 trata la verificación de la implementación como parte de la validación. Para este agente, eso significa que el notebook resultante debe demostrar equivalencia con la herramienta productiva mediante una tabla de reconciliación, y que toda diferencia numérica no explicada es un hallazgo de implementación. La herramienta Excel, mientras no tenga su equivalente reproducible, mantiene un riesgo de modelo que el marco obliga a mitigar.

## Doctrina de citación y auditabilidad

Todo el conocimiento de esta base está redactado para ser citable, y el agente que lo consume hereda la obligación de citar su fuente en cada afirmación. La regla maestra no admite excepción: **ninguna afirmación de validación existe sin su fuente exacta.** Los formatos de cita son: documento PDF o Word como `<archivo> > <sección> > p.<n>`; hoja de cálculo como `<archivo> > <hoja> > <celda o rango>`; código como `<archivo> > <función>() > línea <n>`; correo como `<remitente> > <asunto> > <fecha>`; acta de comité como `<comité> > acta <n> > acuerdo <n>`.

Consecuencias operativas: un hallazgo sin cita verificable no puede marcarse 'Cumple'; se marca 'No verificable'. La ausencia de evidencia es un hallazgo en sí misma y se registra como 'No evidenciado', nunca se interpreta como cumplimiento. Está prohibido inferir, completar o estimar un dato ausente. Toda duda de interpretación se escala como consulta formal, nunca se resuelve en silencio.

## Escala de severidad de hallazgos

Cada hallazgo se clasifica por su efecto sobre la fiabilidad y el uso del modelo, no por el esfuerzo de su remediación:

| Severidad | Definición | Efecto sobre la conclusión |
|---|---|---|
| Crítica | Impide o condiciona el uso del modelo, o afecta el output publicado | Bloquea la conclusión de 'Validación satisfactoria' |
| Alta | Afecta la confiabilidad del modelo sin invalidar su uso inmediato | Exige remediación con fecha comprometida |
| Media | Afecta la auditabilidad o la trazabilidad | Acción pendiente con plazo |
| Baja | Defecto formal sin impacto en el resultado | Mejora recomendada |

Cada hallazgo lleva dueño, plazo y estado, y se referencia cruzadamente cuando toca a más de un control.

## Anexo — Re-validación por tier y expectativas supervisoras

La frecuencia y profundidad de la validación se gradúan por el tier del modelo. Un modelo de mayor materialidad (Tier 1) exige la validación de todas las actividades del estándar, replicación independiente de los outputs y re-validación con la periodicidad más corta; un Tier 2 admite replicación por muestreo y una periodicidad intermedia; un Tier 3 se concentra en el núcleo mínimo (documentación, calidad de datos, gobierno y usos) con revisión focalizada. El tiering, por tanto, no solo clasifica: determina el alcance exigible de la validación en curso.

Las expectativas supervisoras convergentes (SR 11-7, y la normativa SBS de riesgo de modelo) incluyen: un inventario corporativo completo; documentación suficiente para la replicación independiente; validación independiente **previa al uso** del modelo; un órgano de gobierno —como el Comité de Riesgos de Modelo— que evalúe periódicamente el marco; y evidencia de *effective challenge* con competencia, independencia e influencia. La validación no es un acto único: es un ciclo que acompaña toda la vida del modelo.

## Anexo — Documentación de la propia validación

La validación produce su propia evidencia auditable. El expediente de validación conserva: las matrices por control con sus citas; el informe consolidado con la tabla de 8 columnas y la conclusión; el plan de acción con responsables y fechas; el registro de consultas al equipo dueño; y el anexo de trazabilidad con los hashes SHA-256 de las evidencias leídas. Este expediente permite que un tercero —auditoría interna o el supervisor— reconstruya cómo se llegó a la conclusión, qué se revisó y qué quedó pendiente. La cadena de custodia de la evidencia es parte integral del gobierno del riesgo de modelo.

## Anexo — El Reglamento SBS de Gestión de Riesgos de Modelo (Res. N° 00053-2023)

Este anexo resume, con cita al articulado validado contra el texto oficial, las obligaciones del reglamento que rige directamente el trabajo de validación en el Perú.

**Ciclo de vida y definiciones (Art. 2-3).** El reglamento estructura el modelo en tres componentes —entrada, procesamiento y resultados (Art. 2, lit. k)— y ordena su ciclo en cinco fases: desarrollo, validación, implementación, uso y seguimiento (Art. 3.1). La validación es la revisión independiente del desarrollo, la implementación y el uso; la réplica es la reproducción del desarrollo a partir de su documentación de sustento (Art. 2, lit. aa, ff).

**Inventario y categorización (Art. 5-6).** Toda empresa mantiene un inventario de modelos actualizado, que remite anualmente vía SUCAVE (Anexo A). Cada modelo se categoriza por materialidad, uso y complejidad; la categoría determina el alcance y la frecuencia del seguimiento y de la validación periódica, y si se exige réplica completa.

**Segregación de funciones (Art. 12-13).** Los desarrolladores deben ser independientes de las unidades de negocio; los validadores, independientes de los desarrolladores, de los usuarios y de los encargados de la implementación (Art. 12.2-12.3). El validador debe tener al menos el mismo nivel organizacional que el desarrollador (Art. 13.2).

**Documentación de sustento (Art. 14-15).** Comprende como mínimo los informes de desarrollo, implementación, validación y seguimiento, más actas de comités, bases de datos, diccionarios de datos, códigos de programación e informes de aseguramiento de la calidad de los datos, con historial de versiones y fechas.

**Validación (Art. 20).** Distingue validación inicial (previa al uso, del desarrollo y de la implementación) y validación periódica (según categoría). La periódica incluye la validación del uso —verificar que el modelo se emplee conforme a lo aprobado—, la revisión de la categoría de riesgo y la evaluación de la razonabilidad de los forzajes. Para las categorías de mayor riesgo, la validación incluye la réplica completa del modelo.

**Seguimiento (Art. 21-22).** Exige indicadores de calidad con umbrales, alertas, backtesting, análisis de sensibilidad, seguimiento de forzajes y, en modelos de inteligencia artificial, la evaluación del sobreajuste (Art. 16.2 y 22.1, lit. j).

**Modelos de terceros (Art. 23-25).** El desarrollo, la validación y la implementación pueden tercerizarse, pero el seguimiento lo realiza la empresa (Art. 23.1), que asume plena responsabilidad del riesgo de modelo asociado (Art. 24.1); para las categorías de mayor riesgo se exige réplica completa o, ante limitantes de propiedad intelectual, técnicas alternativas como benchmarking (Art. 25.3).


---

## Referencias

- **SR11-7** — Federal Reserve SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management (2011-04-04). *[referencia internacional canónica]*
- **SBS-053-2023** — Resolución SBS N° 00053-2023 — Reglamento de Gestión de Riesgos de Modelo (Lima, 06-01-2023; mod. Res. 3421-2023 y 3884-2024). *[validada — fuente primaria SBS]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
