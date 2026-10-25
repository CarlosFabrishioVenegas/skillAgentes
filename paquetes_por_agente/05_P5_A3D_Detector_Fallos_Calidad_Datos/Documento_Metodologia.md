# Metodología — Experto en detección de fallos de calidad de datos

**Reglas de negocio y del ciclo de vida del dato como controles ejecutables**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A3D · Experto en detección de fallos de calidad de datos  
Documento de Metodología · Versión 2.0 · 2026-09-15


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [Arquitectura del notebook detector](#arquitectura-del-notebook-detector)
- [Catálogo de reglas y su implementación](#catalogo-de-reglas-y-su-implementacion)
- [Llave de operación, orden temporal y ventanas](#llave-de-operacion-orden-temporal-y-ventanas)
- [Anexo — Tabla maestra de umbrales cuantitativos](#anexo-tabla-maestra-de-umbrales-cuantitativos)
- [Anexo — Distinción entre tipos de insuficiencia](#anexo-distincion-entre-tipos-de-insuficiencia)
- [Auto-verificación y reproducibilidad](#auto-verificacion-y-reproducibilidad)
- [La salida: hallazgos con registros infractores](#la-salida-hallazgos-con-registros-infractores)
- [Ejemplo trabajado — doble cancelación](#ejemplo-trabajado-doble-cancelacion)


---

## Arquitectura del notebook detector

El notebook (A3_controles_calidad.ipynb) se organiza en celdas fijas: portada con metadatos y hash SHA-256 del insumo (nº de filas y columnas, período, llave); un bloque **CONFIG** con umbrales y la matriz de transiciones de estado permitidas, cada uno con su origen; carga y ordenamiento de la base por llave y período; una función pura por regla, que devuelve el `DataFrame` de infractores; ejecución; la tabla resumen de hallazgos; y el bloque de reproducibilidad. Cada bloque de código va precedido de una celda markdown que explica la regla y cita su fuente.

## Catálogo de reglas y su implementación

Cada regla se implementa como una condición booleana sobre la base ordenada por operación y período:

- Saldo que resucita: dentro de cada llave, marcar los períodos con `saldo > 0` posteriores a un período con `saldo == 0` o `estado ∈ {cancelada, castigada}` sin un evento de desembolso entre ambos.
- Monotonía: `saldo[t] > saldo[t-1]` sin evento habilitante en `t`.
- Unicidad de eventos: `conteo(evento) por llave > 1` para eventos declarados únicos.
- Transiciones: el par `(estado[t-1], estado[t])` no pertenece a la matriz de transiciones permitidas.
- Continuidad: huecos o duplicados en la serie de períodos por llave.
- Coherencia: cada relación entre campos como una condición (`fecha_desembolso <= fecha_corte`, `capital + interes == cuota`, etc.).
- Signos y rangos: `saldo < 0`, `tasa ∉ [lo, hi]`, `dias_mora < 0`.

## Llave de operación, orden temporal y ventanas

La correcta detección depende de una llave de operación bien definida y de un ordenamiento estable por período. Las reglas de ciclo de vida operan sobre desplazamientos temporales (`shift`) dentro de cada grupo; por eso el notebook agrupa por llave y ordena por fecha de corte antes de aplicar cualquier regla. Las ventanas de referencia (para estabilidad, por ejemplo) se declaran en CONFIG.

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

## Auto-verificación y reproducibilidad

El notebook prueba su propio trabajo: por cada control, `infractores + conformes = total`; una corrida en kernel reiniciado produce el mismo resultado (idempotencia); un insumo vacío falla con un mensaje explícito en vez de un resultado silencioso. Toda semilla se fija y se declara; no hay dependencia de la fecha del sistema sin parametrizar; no se escribe sobre el insumo. El bloque final registra versión, fecha de ejecución, semilla y los hashes de insumo y salida.

## La salida: hallazgos con registros infractores

El entregable A3_hallazgos.md documenta, por regla: descripción, columna(s) y llave, umbral y su origen, nº evaluado, nº infractor, porcentaje de incumplimiento y una tabla de **ejemplos de registros infractores** (llave más los valores que evidencian el fallo y el período). El diagnóstico siempre lleva la cifra; nunca un adjetivo sin dato. Un umbral no declarado deja el control en «No verificable» o marcado [SUPUESTO].

## Ejemplo trabajado — doble cancelación

Regla de unicidad de cancelación: `df.groupby('id_operacion')['evento'].apply(lambda s: (s=='cancelacion').sum())`. Operaciones con conteo mayor que 1 son infractoras. Resultado: 12 operaciones con dos cancelaciones (0,14 % de 8 740); ejemplos de llaves 007781, 009003. Causa probable a verificar por el evaluador: carga duplicada del archivo de eventos.


---

## Referencias

- **BCBS239** — BCBS 239 — Principles for effective risk data aggregation and risk reporting (2013-01). *[referencia internacional canónica]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
