# Metodología — Entendimiento inicial (Paso 0)

**Taxonomía de modelos financieros y de riesgo**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A4 · Entendimiento inicial (Paso 0)  
Documento de Metodología · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [Caracterización de un modelo en el Paso 0](#caracterizacion-de-un-modelo-en-el-paso-0)
- [Reconciliación de fuentes y discrepancias](#reconciliacion-de-fuentes-y-discrepancias)
- [Mapa de evidencia por control](#mapa-de-evidencia-por-control)
- [Guion de la infografía](#guion-de-la-infografia)
- [Dependencias y cambios en el ciclo](#dependencias-y-cambios-en-el-ciclo)
- [Anexo — Tabla maestra de umbrales cuantitativos](#anexo-tabla-maestra-de-umbrales-cuantitativos)
- [Anexo — Distinción entre tipos de insuficiencia](#anexo-distincion-entre-tipos-de-insuficiencia)
- [Ejemplo trabajado — eslabón de la cadena del modelo](#ejemplo-trabajado-eslabon-de-la-cadena-del-modelo)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## Caracterización de un modelo en el Paso 0

Cada modelo se caracteriza por cinco atributos: **propósito** (qué decisión soporta), **inputs** (datos, supuestos, parámetros), **outputs** (qué produce), **uso** (para qué está autorizado) y **limitaciones** (perímetro de validez). El entregable reconstruye la cadena `input → transformación → output → publicación → decisión` en una sola secuencia con la cita de cada eslabón, y declara el **estado de admisibilidad de la herramienta** (Python que corre sin errores; Python con errores; Excel con su `.md`; Excel sin `.md`; no entregada), pues ese estado condiciona el inicio del control de Implementación.

## Reconciliación de fuentes y discrepancias

Antes de redactar, el agente reconcilia las fuentes: qué dice el manual, qué dice el acta y qué dijo el equipo en la reunión de entendimiento. Toda discrepancia se documenta y se convierte en consulta abierta; no se elige una versión en silencio. Una declaración verbal que no consta en ningún documento se registra como 'declaración verbal en reunión del <fecha>, sin sustento documental' y genera consulta, sin elevarse a hecho documentado.

## Mapa de evidencia por control

El Paso 0 produce un **mapa de evidencia** que asigna a cada control (C1 a C6) la evidencia disponible y la faltante, con rutas de archivo exactas. Ese mapa es el contrato de entrada de los seis controles y el insumo de la primera re-entrega. Si un control no tiene ninguna evidencia asignada, ese vacío es el primer hallazgo del ciclo y debe activar la re-entrega antes de avanzar.

## Guion de la infografía

La infografía de una página resume cinco bloques obligatorios: la cadena del modelo en un eje horizontal; el tiering y la periodicidad; los outputs y sus destinatarios; el semáforo de observaciones abiertas del ciclo anterior; y el pie con las fuentes citadas y numeradas. La infografía no puede contener ningún dato que no esté en el documento de entendimiento; antes de entregar, el agente recorre cada elemento gráfico y confirma su respaldo textual.

## Dependencias y cambios en el ciclo

El Paso 0 documenta las dependencias del modelo aguas arriba (qué lo alimenta) y aguas abajo (qué consume su output, identificado por código de inventario), porque el impacto de un hallazgo se propaga por esa cadena. Documenta también qué cambió respecto del ciclo anterior (recalibración, cambio de variables) y con qué aprobación: un cambio sin aprobación es hallazgo de gobierno que debe señalarse desde el inicio, no descubrirse al final.

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

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
