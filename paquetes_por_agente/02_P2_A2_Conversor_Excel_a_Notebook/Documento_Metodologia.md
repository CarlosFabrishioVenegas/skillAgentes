# Metodología — Conversor de herramienta Excel a notebook

**Reproducibilidad y riesgo de hoja de cálculo**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A2 · Conversor de herramienta Excel a notebook  
Documento de Metodología · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [Inventario y clasificación del libro](#inventario-y-clasificacion-del-libro)
- [Equivalencias funcionales Excel a Python](#equivalencias-funcionales-excel-a-python)
- [Reconciliación numérica con tolerancia](#reconciliacion-numerica-con-tolerancia)
- [Pruebas mínimas del notebook y golden set](#pruebas-minimas-del-notebook-y-golden-set)
- [Casos borde de traducción](#casos-borde-de-traduccion)
- [Anexo — Tabla maestra de umbrales cuantitativos](#anexo-tabla-maestra-de-umbrales-cuantitativos)
- [Anexo — Distinción entre tipos de insuficiencia](#anexo-distincion-entre-tipos-de-insuficiencia)
- [Ejemplo trabajado — fila de reconciliación](#ejemplo-trabajado-fila-de-reconciliacion)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## Inventario y clasificación del libro

El primer paso es inventariar el libro: hojas, rangos con nombre, tablas, conexiones externas, macros VBA, formato condicional que implique lógica y celdas protegidas. Cada hoja se clasifica en ENTRADA (datos crudos), PARÁMETROS (constantes, umbrales), CÁLCULO (fórmulas), SALIDA (resultado publicado) o AUXILIAR. Las hojas ocultas se procesan igual y se marcan, porque suelen contener parámetros vivos. Una macro VBA cuyo código no puede leerse se reporta como 'lógica no accesible' y se marca como riesgo de implementación alto, no se omite.

## Equivalencias funcionales Excel a Python

El mapeo preserva la semántica exacta:

| Excel | Python | Cuidado |
|---|---|---|
| `BUSCARV` / `INDEX-MATCH` | `pandas.merge` / `.map` | validar cardinalidad (1:1, 1:N) |
| `SUMAR.SI.CONJUNTO` | `groupby` filtrado | respetar criterios múltiples |
| `SUMAPRODUCTO` | `numpy.dot` | alinear dimensiones |
| tablas dinámicas | `pivot_table` | comparar totales y celdas internas |
| `Solver` | `scipy.optimize` | fijar método y tolerancia |
| `SI.ERROR` | `try/except` o `fillna(valor exacto)` | nunca rellenar con 0 por omisión |
| `XNPV` / `XIRR` | `numpy-financial` / propia | verificar convención de fechas |


## Reconciliación numérica con tolerancia

La aritmética de punto flotante IEEE 754 de doble precisión ofrece del orden de 15 a 17 dígitos decimales significativos y **no garantiza igualdad exacta bit a bit**. La reconciliación se hace con tolerancia combinada absoluta y relativa:

```
|a - b|  <=  atol + rtol * |b|
```

con `rtol` del orden de 1e-6 a 1e-8 según la materialidad de la cifra. Toda celda de salida del Excel se compara contra el resultado del notebook; cualquier diferencia que supere la tolerancia se marca 'no reconciliada' y se investiga (causa frecuente: redondeo en una celda intermedia). La tolerancia se documenta y se aprueba con el dueño del modelo.

## Pruebas mínimas del notebook y golden set

Antes de sustituir el legado se congela un conjunto de casos de prueba ('golden set') con sus resultados conocidos y se verifica que la nueva implementación los reproduce dentro de tolerancia. El notebook debe superar además cuatro pruebas: ejecución limpia de principio a fin en un kernel reiniciado; reconciliación de todas las salidas; idempotencia (dos ejecuciones consecutivas dan resultados idénticos); y prueba de insumo vacío (falla con mensaje explícito, no produce un resultado silencioso). El redondeo se replica en el mismo punto del cálculo que el Excel.

## Casos borde de traducción

Fórmulas matriciales o de arreglo dinámico se traducen con operaciones vectorizadas y se verifican celda a celda, no solo por el agregado. Las fórmulas dependientes de la fecha del sistema (HOY, AHORA) se parametrizan en la configuración y se documenta que el resultado del Excel varía por día. Un libro con filtros aplicados al momento de la entrega obliga a verificar si el cálculo depende de las filas visibles: si es así, es un riesgo de implementación alto. El formato de número que oculta decimales en pantalla no altera el valor almacenado, con el que siempre se trabaja.

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

## Ejemplo trabajado — fila de reconciliación

La tabla de reconciliación evidencia la equivalencia numérica:

| Salida | Valor Excel | Valor notebook | Dif. abs. | Dif. rel. | Estado |
|---|---|---|---|---|---|
| PD media cartera | 0.031400 | 0.031400 | 0.000000 | 0.0e+00 | Reconciliado |
| Provisión total | 12 480 331.20 | 12 480 018.55 | 312.65 | 2.5e-05 | No reconciliado — revisar redondeo en `Calculo > H45` |

La segunda fila no cierra dentro de tolerancia y obliga a investigar el punto de redondeo antes de aceptar el notebook como equivalente.

## Glosario

| Término | Definición |
|---|---|
| **Cálculo endurecido** | Valor pegado como texto en una celda donde debería existir una fórmula; rompe la reproducibilidad. |
| **Reconciliación** | Comparación cifra a cifra entre la salida del Excel y la del notebook dentro de una tolerancia. |
| **Golden set** | Conjunto congelado de casos de prueba con resultados conocidos para verificar la equivalencia. |
| **Idempotencia** | Propiedad de que ejecutar dos veces el mismo proceso produzca el mismo resultado. |
| **Tolerancia (atol/rtol)** | Margen absoluto y relativo admitido al comparar dos números en punto flotante. |

## Errores frecuentes

- Traducir `SI.ERROR` rellenando con 0 por omisión, lo que oculta pérdidas de registros o divisiones inválidas.
- Refactorizar la lógica de negocio o renombrar variables de forma que se pierda la trazabilidad con la hoja.
- Omitir hojas ocultas o auxiliares por parecer irrelevantes, cuando contienen parámetros vivos.
- Entregar el notebook sin la tabla de reconciliación o con salidas 'no reconciliadas' sin explicación.
- Recortar rangos que apuntan a filas vacías sin anotar el cambio, alterando promedios y conteos.

## Lista de verificación antes de concluir

1. ¿El notebook ejecuta limpio de principio a fin en un kernel reiniciado?
2. ¿Existe tabla de reconciliación y todas las salidas cierran dentro de tolerancia?
3. ¿Cada parámetro y función lleva comentario con su celda de origen?
4. ¿La semilla aleatoria está fijada y declarada?
5. ¿Las hojas ocultas y las macros VBA quedaron inventariadas y evaluadas?
6. ¿La tolerancia de reconciliación fue aprobada por el dueño del modelo?


---

## Referencias

- **IEEE754** — IEEE 754 — Estándar de aritmética de punto flotante (doble precisión). *[referencia internacional canónica]*
- **EUSPRIG** — European Spreadsheet Risks Interest Group (EuSpRIG) — buenas prácticas de hojas de cálculo. *[referencia internacional canónica]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
