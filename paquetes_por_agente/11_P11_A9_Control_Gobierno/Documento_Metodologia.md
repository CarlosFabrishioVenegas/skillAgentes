# Metodología — Control de Gobierno

**Gobierno de riesgo de modelo y tres líneas de defensa**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A9 · Control de Gobierno  
Documento de Metodología · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [Verificación campo por campo](#verificacion-campo-por-campo)
- [Recálculo del tiering](#recalculo-del-tiering)
- [Gestión centralizada de consultas](#gestion-centralizada-de-consultas)
- [Roles, segregación e inventario](#roles-segregacion-e-inventario)
- [Registro de cambios del acta y roles](#registro-de-cambios-del-acta-y-roles)
- [Anexo — Tabla maestra de umbrales cuantitativos](#anexo-tabla-maestra-de-umbrales-cuantitativos)
- [Anexo — Distinción entre tipos de insuficiencia](#anexo-distincion-entre-tipos-de-insuficiencia)
- [Ejemplo trabajado — consulta de gobierno](#ejemplo-trabajado-consulta-de-gobierno)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## Verificación campo por campo

El control recorre los campos del acta evaluando cuatro atributos por campo: **presente**, **legible**, **vigente** y **coherente** con la evidencia técnica de los controles C1 a C4. Un campo vacío es 'No evidenciado', nunca 'No aplica', salvo que el estándar lo exima expresamente y se cite la regla. Cada fila cita el acta (documento > campo > página) y la evidencia técnica contrastada; una fila que solo cita el acta no acredita coherencia.

## Recálculo del tiering

El control recalcula el tiering con los criterios vigentes (materialidad o exposición, criticidad regulatoria, complejidad y alcance de uso) y lo compara con el registrado. Si difiere, es hallazgo de severidad alta. Un modelo de bajo impacto cuyo output alimenta a un modelo Tier 1 debe reevaluarse por propagación. Una aprobación del tier por alguien sin facultad es hallazgo aunque el valor del tier sea correcto.

## Gestión centralizada de consultas

Toda ambigüedad se convierte en **consulta formal** al responsable del equipo dueño, con pregunta concreta y respondible, evidencia que la origina con su cita, destinatario, plazo y efecto de la no respuesta sobre la conclusión. El control nunca resuelve la ambigüedad por inferencia. Este agente centraliza las consultas del ciclo, aunque las origine otro control, para evitar preguntas duplicadas al equipo dueño; una consulta redundante deteriora la relación y resta credibilidad al proceso.

## Roles, segregación e inventario

Se verifica la independencia entre desarrollador, propietario, usuario y validador cuando el estándar exige segregación. Se contrasta el acta con el inventario: un modelo con acta vigente pero ausente del inventario, o en estado 'en revisión' del inventario pero en uso productivo, es hallazgo crítico, porque el estado registrado no refleja la realidad operativa.

## Registro de cambios del acta y roles

El control revisa el registro de cambios del acta: quién modificó qué y cuándo; un campo modificado sin traza es hallazgo. Verifica la segregación entre desarrollador, propietario, usuario y validador cuando el estándar exige independencia. Un acta actualizada durante la validación en curso obliga a validar sobre la versión vigente al inicio del ciclo y a reportar el cambio con sus fechas. Un propietario que ya no trabaja en el banco deja al modelo sin responsable efectivo y es hallazgo de gobierno.

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

## Ejemplo trabajado — consulta de gobierno

> 'Consulta 03: el acta registra Tier 2 con exposición gestionada de S/ 180 MM, mientras el reporte de cartera 2026Q2 muestra S/ 640 MM, umbral que según los criterios vigentes corresponde a Tier 1. ¿Se solicitó reevaluación de tiering tras el crecimiento? Evidencia: `Acta_MOD-0412.docx > tiering > p.1`; `Reporte_Cartera_2026Q2.xlsx > Resumen > C9`. Plazo: 5 días. Sin respuesta, el campo se reporta No verificable y el tiering queda observado.'

La consulta es concreta, cita su evidencia y declara el efecto de la falta de respuesta.

## Glosario

| Término | Definición |
|---|---|
| **Tres líneas de defensa** | Negocio (1ª), gestión de riesgo y validación (2ª), auditoría interna (3ª). |
| **Tiering** | Clasificación del modelo por materialidad que gradúa la intensidad de la validación. |
| **Segregación de funciones** | Separación entre quien desarrolla, quien posee, quien usa y quien valida el modelo. |
| **Inventario de modelos** | Registro corporativo completo de los modelos y su estado. |
| **Consulta formal** | Pregunta escrita al equipo dueño ante una ambigüedad, con plazo y efecto declarado. |

## Errores frecuentes

- Completar un campo del acta con información tomada de otro documento en vez de marcarlo incompleto.
- Resolver una ambigüedad del acta por inferencia en lugar de escalarla como consulta.
- Omitir el recálculo del tiering por considerarlo evidente.
- Marcar 'No aplica' un campo vacío sin citar la regla del estándar que lo exime.
- Cerrar el control con consultas abiertas sin declarar su efecto sobre la conclusión.

## Lista de verificación antes de concluir

1. ¿Se evaluó cada campo del acta por presente, legible, vigente y coherente?
2. ¿Se recalculó el tiering con los criterios vigentes y se comparó con el registrado?
3. ¿Cada fila cita el acta y la evidencia técnica contrastada?
4. ¿Las ambigüedades se convirtieron en consultas formales con plazo y efecto?
5. ¿Se verificó la segregación de funciones y la consistencia con el inventario?
6. ¿Las consultas del ciclo se centralizaron para evitar duplicados?


---

## Referencias

- **SR11-7** — Federal Reserve SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management (2011-04-04). *[referencia internacional canónica]*
- **SBS-053-2023** — Resolución SBS N° 00053-2023 — Reglamento de Gestión de Riesgos de Modelo (Lima, 06-01-2023; mod. Res. 3421-2023 y 3884-2024). *[validada — fuente primaria SBS]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
