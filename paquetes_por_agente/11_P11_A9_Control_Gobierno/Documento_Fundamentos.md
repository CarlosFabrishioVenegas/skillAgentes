# Fundamentos — Control de Gobierno

**Gobierno de riesgo de modelo y tres líneas de defensa**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A9 · Control de Gobierno  
Documento de Fundamentos · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [Las tres líneas de defensa](#las-tres-lineas-de-defensa)
- [Inventario, materialidad y tiering](#inventario-materialidad-y-tiering)
- [Coherencia sobre existencia](#coherencia-sobre-existencia)
- [Propagación del tiering y aprobaciones válidas](#propagacion-del-tiering-y-aprobaciones-validas)
- [Anexo — El control dentro del flujo de validación VIRF](#anexo-el-control-dentro-del-flujo-de-validacion-virf)
- [Anexo — Semáforo de estados del sistema](#anexo-semaforo-de-estados-del-sistema)
- [Anexo — Ciclo de vida del modelo y ubicación de la validación](#anexo-ciclo-de-vida-del-modelo-y-ubicacion-de-la-validacion)
- [Ejemplo trabajado — consulta de gobierno](#ejemplo-trabajado-consulta-de-gobierno)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## Las tres líneas de defensa

El gobierno del riesgo de modelo se estructura en tres líneas. La **primera** es el negocio y los dueños del modelo, que asumen el riesgo y responden por el desarrollo y el uso correcto. La **segunda** es la función de gestión del riesgo de modelo y la validación independiente, que ejerce el *effective challenge* y no reporta al desarrollo. La **tercera** es la auditoría interna, que evalúa la efectividad del marco en su conjunto. La segregación entre *model owner*, *developer* y *validator* es condición de independencia; cuando la misma persona o área desarrolla y valida, el challenge pierde objetividad y constituye hallazgo.

## Inventario, materialidad y tiering

El marco exige un **inventario de modelos** completo y actualizado, y una clasificación por materialidad (**tiering**) que gradúa la intensidad y la frecuencia de la validación. El tiering no es una etiqueta administrativa: determina qué actividades del estándar son exigibles en cada validación. Un tiering desactualizado respecto de la exposición real del modelo es hallazgo de gobierno de severidad alta, porque significa que la validación en curso pudo haberse hecho con el conjunto equivocado de actividades exigibles.

## Coherencia sobre existencia

El criterio del control no es la existencia formal del acta, sino su **coherencia** con la realidad técnica evidenciada por los controles previos. Un acta completa pero desalineada —por ejemplo, que declara una exposición muy inferior a la real, o un uso distinto al observado— es un hallazgo, porque la gestión del riesgo se apoya en información que no corresponde al modelo real.

## Propagación del tiering y aprobaciones válidas

El gobierno vigila dos situaciones sutiles: la **propagación del tiering** —un modelo de bajo impacto cuyo output alimenta a un modelo Tier 1 debe reevaluarse por propagación— y la **validez de las aprobaciones** —un acta aprobada por alguien sin facultad para hacerlo es hallazgo aunque su contenido sea correcto—. La rendición de cuentas exige un propietario único e identificable; dos propietarios declarados en documentos distintos bloquean la responsabilidad y obligan a consulta inmediata.

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
- **SBS-272-2017** — Resolución SBS N° 272-2017 — Reglamento de Gobierno Corporativo y de la Gestión Integral de Riesgos (Lima, 18-01-2017; vigente 01-04-2018). *[validada — fuente primaria SBS]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
