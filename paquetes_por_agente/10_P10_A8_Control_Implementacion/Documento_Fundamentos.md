# Fundamentos — Control de Implementación

**Verificación de que el código implementa lo documentado**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A8 · Control de Implementación  
Documento de Fundamentos · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [Implementation testing en SR 11-7](#implementation-testing-en-sr-11-7)
- [Precondición y riesgos de implementación](#precondicion-y-riesgos-de-implementacion)
- [Fidelidad frente a estilo](#fidelidad-frente-a-estilo)
- [Ramas, entornos y reproducibilidad futura](#ramas-entornos-y-reproducibilidad-futura)
- [Anexo — El control dentro del flujo de validación VIRF](#anexo-el-control-dentro-del-flujo-de-validacion-virf)
- [Anexo — Semáforo de estados del sistema](#anexo-semaforo-de-estados-del-sistema)
- [Anexo — Ciclo de vida del modelo y ubicación de la validación](#anexo-ciclo-de-vida-del-modelo-y-ubicacion-de-la-validacion)
- [Ejemplo trabajado — diferencia de parámetro](#ejemplo-trabajado-diferencia-de-parametro)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## Implementation testing en SR 11-7

SR 11-7 trata la verificación de la implementación como parte integral de la validación: comprobar que el sistema procesa las entradas y genera las salidas conforme al diseño, incluyendo integraciones, manejo de errores y controles de acceso. La pregunta rectora es directa: ¿lo que corre en producción es lo que está documentado, y puede reproducirse? El control no juzga la metodología (eso es de A7), sino su fidelidad al pasar a código.

## Precondición y riesgos de implementación

El control no inicia hasta que el modelo haya corrido y sus outputs hayan sido revisados; sin log de ejecución ni outputs del ciclo, la precondición no se satisface y el control se detiene. Los riesgos de implementación más frecuentes son las diferencias entre el entorno de desarrollo y el de producción, los errores de mapeo de datos, los redondeos intermedios, las semillas no fijadas y el desvío silencioso por cambios en las fuentes de datos.

## Fidelidad frente a estilo

El control se ocupa de la fidelidad y la reproducibilidad, no del estilo del código. Los nombres de variables, la elegancia o la modularidad solo importan cuando afectan la trazabilidad con el manual o la capacidad de reproducir el resultado. El foco está en el riesgo, no en la forma.

## Ramas, entornos y reproducibilidad futura

El control identifica qué versión corrió realmente en el ciclo: valida la rama de producción, no una rama de desarrollo, y documenta la existencia de otras. Vigila la reproducibilidad futura: una dependencia sin versión fijada o un archivo en un escritorio personal son riesgos de continuidad, no solo de estilo. Un notebook con celdas ejecutadas fuera de orden no acredita reproducibilidad; se exige ejecución limpia de principio a fin.

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

## Ejemplo trabajado — diferencia de parámetro

> 'El código aplica un corte de score de 620 mientras el manual documenta 640; la diferencia reclasifica 4 128 clientes (2,7 % de la cartera) hacia el segmento de menor PD, por lo que el output del ciclo no es concluyente hasta determinar cuál corte está aprobado. Fuente: `pipeline_pd.py > línea 193`; `Manual_v3.pdf > 6.2 > p.48`; `output_scores_2026Q2.csv`.'

La diferencia es bloqueante para el cierre porque afecta a un volumen material de clientes y su aprobación no puede determinarse.

## Glosario

| Término | Definición |
|---|---|
| **Implementation testing** | Verificación de que el sistema procesa entradas y produce salidas conforme al diseño. |
| **Precondición** | Existencia de log de ejecución y outputs revisados antes de iniciar el control. |
| **Reconciliación de output** | Comparación cifra a cifra entre el output publicado y el reproducido. |
| **Ajuste manual (overlay)** | Modificación del output posterior al cálculo del modelo; exige aprobación documentada. |
| **Descarte silencioso** | Pérdida de registros entre etapas del pipeline sin registro ni alerta. |

## Errores frecuentes

- Iniciar el control sin log de ejecución 'para avanzar mientras llega'.
- Dar por válida una diferencia de parámetro por ser 'pequeña'.
- Aceptar explicaciones verbales sobre lo que el código 'realmente hace'.
- Cerrar el control sin haber reproducido al menos un output del ciclo.
- Opinar sobre estilo del código cuando no afecta trazabilidad ni reproducibilidad.

## Lista de verificación antes de concluir

1. ¿Se verificó la precondición (log de ejecución y outputs revisados)?
2. ¿Se mapeó cada bloque de código a la sección del manual que lo describe?
3. ¿Se compararon todos los parámetros (cortes, pesos, umbrales, ventanas)?
4. ¿Se reprodujo al menos un output con sus seis elementos de acreditación?
5. ¿Se revisó la higiene con foco en riesgo (warnings, semillas, credenciales)?
6. ¿El control de cambios (versión, aprobador, fecha) está evidenciado?


---

## Referencias

- **SR11-7** — Federal Reserve SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management (2011-04-04). *[referencia internacional canónica]*
- **EUSPRIG** — European Spreadsheet Risks Interest Group (EuSpRIG) — buenas prácticas de hojas de cálculo. *[referencia internacional canónica]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
