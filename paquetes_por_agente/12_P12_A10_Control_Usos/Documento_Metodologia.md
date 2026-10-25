# Metodología — Control de Usos

**Use test y uso efectivo del modelo**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A10 · Control de Usos  
Documento de Metodología · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [La cadena de uso](#la-cadena-de-uso)
- [Periodicidad y trazabilidad de la cifra](#periodicidad-y-trazabilidad-de-la-cifra)
- [Retiro del inventario](#retiro-del-inventario)
- [Trazabilidad de la cifra publicada](#trazabilidad-de-la-cifra-publicada)
- [Anexo — Tabla maestra de umbrales cuantitativos](#anexo-tabla-maestra-de-umbrales-cuantitativos)
- [Anexo — Distinción entre tipos de insuficiencia](#anexo-distincion-entre-tipos-de-insuficiencia)
- [Ejemplo trabajado — uso con observación](#ejemplo-trabajado-uso-con-observacion)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## La cadena de uso

Para cada output declarado se reconstruye la cadena completa: **generación → envío → recepción acusada → sustento en el foro → decisión o toma de conocimiento registrada**. El eslabón donde la cadena se rompe es el hallazgo. Cada output se evalúa por separado: un modelo puede tener uso acreditado para su curva y no para su tabla de sensibilidades. La evidencia admisible es documental —correos con acuse, actas de comité con número y acuerdo, evidencia de publicación con constancia de consumo—; la afirmación del equipo dueño, sin soporte, no acredita uso.

## Periodicidad y trazabilidad de la cifra

Se verifica que las fechas de envío respeten la periodicidad comprometida, cuantificando los días de desviación. Se verifica también que la cifra publicada coincida con la generada por la herramienta; si difiere, hay ajuste manual no documentado y se escala como hallazgo crítico compartido con Implementación. Un output publicado en un tablero sin evidencia de consumo no acredita uso: se solicita estadística de accesos o confirmación del área usuaria.

## Retiro del inventario

Cuando no existe ni envío ni sustento en comité, el uso se declara **no satisfactorio** y se emite la recomendación formal de retiro del inventario. La recomendación incluye: identificación del modelo y su tier; período evaluado sin uso; evidencia buscada y no encontrada, con las rutas consultadas; procesos que dejarían de recibir el output; riesgo de mantener el modelo; y destinatario formal. Esta recomendación es obligatoria ante la ausencia de uso, no discrecional: su omisión sería una falla del propio proceso de validación.

## Trazabilidad de la cifra publicada

El control verifica que la cifra efectivamente enviada al usuario coincida con la generada por la herramienta del modelo. Si difiere, hay un ajuste manual no documentado entre el cálculo y la publicación, y se escala como hallazgo crítico compartido con Implementación. Envíos existentes pero con archivos que no se pueden abrir o están vacíos no acreditan entrega efectiva; un área usuaria que declara no utilizar el output aunque lo recibe deja el uso sin acreditar, y esa declaración se documenta con su fuente.

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

## Ejemplo trabajado — uso con observación

> 'El envío existe y está acusado dentro del plazo trimestral, pero la periodicidad comprometida exige sustento en el Comité de Riesgos y la última presentación registrada es de noviembre de 2025; el uso está acreditado en el nivel operativo y no en el de gobierno. Fuente: `mgomez@banco.pe > Curva PD 2026Q2 > 2026-07-08`; `Comité de Riesgos > acta 118 > agenda`.'

El hallazgo distingue el uso operativo (acreditado) del de gobierno (pendiente), que es la clave del control.

## Glosario

| Término | Definición |
|---|---|
| **Use test** | Exigencia de que los outputs del modelo se usen efectivamente en la gestión. |
| **Cadena de uso** | Secuencia generación→envío→acuse→foro→decisión que evidencia el uso. |
| **Uso operativo / de gobierno** | Uso en el proceso del área usuaria / sustento en el foro comprometido. |
| **Retiro del inventario** | Baja de un modelo sin uso efectivo demostrable. |
| **Alcance autorizado** | Uso para el que el modelo fue aprobado, según el acta. |

## Errores frecuentes

- Acreditar uso por la mera existencia del output, sin cadena de envío y sustento.
- Considerar el envío interno entre miembros del equipo desarrollador como evidencia de uso.
- Omitir la recomendación de retiro cuando no hay uso, por no generar fricción con el área.
- Aceptar un uso distinto al declarado sin generar el hallazgo compartido con Gobierno.
- Dar por acreditado un uso publicado en tablero sin evidencia de consumo.

## Lista de verificación antes de concluir

1. ¿Se reconstruyó la cadena de uso completa para cada output declarado?
2. ¿El uso real coincide con el uso declarado en el acta?
3. ¿Las fechas de envío respetan la periodicidad, con los días de desviación cuantificados?
4. ¿La cifra publicada coincide con la generada por la herramienta?
5. ¿Se acreditó tanto el uso operativo como el de gobierno?
6. ¿Ante ausencia de uso, se emitió la recomendación formal de retiro?


---

## Referencias

- **BASEL-IRB** — Basel Framework — Internal Ratings-Based approach y use test. *[referencia internacional canónica]*
- **SBS-053-2023** — Resolución SBS N° 00053-2023 — Reglamento de Gestión de Riesgos de Modelo (Lima, 06-01-2023; mod. Res. 3421-2023 y 3884-2024). *[validada — fuente primaria SBS]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
