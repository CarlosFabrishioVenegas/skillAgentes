# Metodología — Evaluador de controles e informe de calidad de datos

**Interpretación de los controles ejecutados y redacción del informe detallado**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A3E · Evaluador de controles e informe de calidad de datos  
Documento de Metodología · Versión 2.0 · 2026-09-15


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [Del hallazgo al juicio técnico](#del-hallazgo-al-juicio-tecnico)
- [Estructura del informe detallado](#estructura-del-informe-detallado)
- [La matriz técnica de 8 columnas](#la-matriz-tecnica-de-8-columnas)
- [Reconciliación de conteos y verificación de linaje](#reconciliacion-de-conteos-y-verificacion-de-linaje)
- [Anexo — Tabla maestra de umbrales cuantitativos](#anexo-tabla-maestra-de-umbrales-cuantitativos)
- [Anexo — Distinción entre tipos de insuficiencia](#anexo-distincion-entre-tipos-de-insuficiencia)
- [Referencias cruzadas a otros controles](#referencias-cruzadas-a-otros-controles)
- [Ejemplo trabajado — fila de la matriz](#ejemplo-trabajado-fila-de-la-matriz)


---

## Del hallazgo al juicio técnico

El agente recorre la salida del notebook regla por regla y traslada cada cifra a un juicio, aplicando las cuatro insuficiencias, la materialidad y la severidad. Verifica el **linaje** de los campos implicados (un campo sin origen trazable es un hallazgo de gobierno del dato) y **reconcilia los conteos** por control (infractores + conformes = total); una descuadratura se declara y se solicita re-ejecución, no se interpreta.

## Estructura del informe detallado

El informe (A3_informe_calidad_datos.md) sigue una estructura fija: portada y metadatos (modelo, tier, ciclo, fecha de corte, insumo con su hash); **resumen ejecutivo** (controles corridos, cuántos fallaron, hallazgos críticos, estado global); **cobertura** (evaluadas frente a exigibles por tier y qué quedó sin evaluar y por qué); **hallazgos por control** (una subsección por regla, con resultado, ejemplos, causa raíz, materialidad, severidad, estado y remediación con responsable y plazo); la **matriz técnica** como anexo; las **referencias cruzadas**; la **conclusión y el plan de remediación** priorizado; y «## Brechas de evidencia».

## La matriz técnica de 8 columnas

El anexo cuantitativo es la matriz: `Dimensión/Regla | Estado | % Cumplimiento | ¿Existe según evidencia? | Diagnóstico (con cifra) | Decisión/acción | Evidencia requerida | Referencia (control > columna)`. La matriz condensa el resultado por regla; el cuerpo del informe lo narra y lo pondera. Cada fila cita el control del notebook y la columna evaluada; ninguna fila «Cumple» sin cita reproducible.

## Reconciliación de conteos y verificación de linaje

Antes de emitir cualquier estado, el agente comprueba que las cifras del notebook cuadran (los conteos reconcilian, los porcentajes se derivan de los totales declarados) y que cada campo evaluado tiene origen trazable. Una cifra que no reconcilia invalida la lectura de esa regla y se reporta como tal.

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

## Referencias cruzadas a otros controles

Un hallazgo crítico de datos invalida conclusiones aguas abajo: el informe lo marca explícitamente para Metodología (P9) e Implementación (P10), y un defecto de linaje además para Gobierno del dato (P11). La calidad de datos es el primer eslabón cuyo resultado condiciona a los demás controles; por eso el informe no vive aislado.

## Ejemplo trabajado — fila de la matriz

`| Completitud | No cumple | 92,60 % | Sí | ingreso_declarado con 7,4 % de nulos (371/5 015), variable driver del score → materialidad alta | Documentar la regla de imputación y re-ejecutar | Base previa a imputación | nb > celda 4 > Completitud |`. El estado se apoya en la cifra citada, no en un adjetivo.


---

## Referencias

- **BCBS239** — BCBS 239 — Principles for effective risk data aggregation and risk reporting (2013-01). *[referencia internacional canónica]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
