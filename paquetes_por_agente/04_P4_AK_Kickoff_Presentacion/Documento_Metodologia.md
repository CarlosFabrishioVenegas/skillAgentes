# Metodología — Kick-off — Presentación de entendimiento (Alcance, Limitaciones y Flujo de Datos)

**Comunicación del entendimiento y alineamiento del kick-off**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente AK · Kick-off — Presentación de entendimiento (Alcance, Limitaciones y Flujo de Datos)  
Documento de Metodología · Versión 2.0 · 2026-09-14


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [Estructura de la presentación de dos láminas](#estructura-de-la-presentacion-de-dos-laminas)
- [Lámina 1 — Alcance y Limitaciones](#lamina-1-alcance-y-limitaciones)
- [Lámina 2 — Flujo de datos (Input → Tratamiento → Usuarios)](#lamina-2-flujo-de-datos-input-tratamiento-usuarios)
- [Derivación desde A4_paso0.md y fuentes opcionales](#derivacion-desde-a4-paso0-md-y-fuentes-opcionales)
- [Reglas de cita y de no evidenciado en la presentación](#reglas-de-cita-y-de-no-evidenciado-en-la-presentacion)
- [Anexo — Tabla maestra de umbrales cuantitativos](#anexo-tabla-maestra-de-umbrales-cuantitativos)
- [Anexo — Distinción entre tipos de insuficiencia](#anexo-distincion-entre-tipos-de-insuficiencia)
- [Ejemplo trabajado — bloque de la Lámina 1](#ejemplo-trabajado-bloque-de-la-lamina-1)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)


---

## Estructura de la presentación de dos láminas

El entregable es un archivo Markdown apto para PowerPoint (`AK_kickoff_presentacion.md`) con un encabezado de identificación (modelo, código, tipo, tier, ciclo y fecha de corte tomados del anclaje) y exactamente dos láminas. No se añaden láminas de conclusión ni de recomendación: la presentación comunica el entendimiento, no lo evalúa. El orden es fijo: primero Alcance y Limitaciones, luego el Flujo de datos.

## Lámina 1 — Alcance y Limitaciones

La lámina se divide en dos bloques. **Alcance**: el propósito de negocio (qué decisión soporta el modelo), el uso declarado y autorizado, y el perímetro (productos, carteras o mesas). Cada punto lleva su cita al entendimiento. **Limitaciones**: la transcripción literal, entre comillas, de los supuestos y limitaciones declarados, más las condiciones de uso válidas; si se adjuntó el informe de la validación anterior, se añaden las observaciones abiertas relevantes con su estado. Los supuestos no se reformulan: su redacción exacta es objeto de validación posterior.

## Lámina 2 — Flujo de datos (Input → Tratamiento → Usuarios)

La lámina se representa como una tabla de tres cajas conectadas por flechas:

| Input de Datos | → | Tratamiento y resultado de los datos | → | Usuarios Finales |
|---|---|---|---|---|
| fuentes, sistemas y tablas de origen (cita) | → | transformaciones y output producido (cita) | → | destinatario, foro/sistema y periodicidad (cita) |

Debajo de la tabla se colocan notas por caja cuando el detalle no cabe en la celda. Si falta información para una caja, se dice explícitamente en esa caja con 'No evidenciado'; no se rellena por analogía.

## Derivación desde A4_paso0.md y fuentes opcionales

La fuente principal y suficiente es A4_paso0.md: la presentación puede construirse solo con él. De forma **opcional**, si se adjuntan, se usan el informe de la validación anterior (para las observaciones abiertas de la Lámina 1) y la evidencia de usos (acta, correos, actas de comité) para precisar los usuarios finales. No se incorpora ninguna fuente que no se haya adjuntado, ni conocimiento general sobre cómo 'suelen' funcionar estos modelos.

## Reglas de cita y de no evidenciado en la presentación

Cada afirmación de las dos láminas lleva su cita entre paréntesis, remitida al entendimiento: `(A4_paso0.md > sección)`. Cuando se usa el informe anterior o la evidencia de usos, se cita el documento correspondiente. Un punto sin cita es un defecto del entregable. Los supuestos y limitaciones van entre comillas y con su cita, sin reformular. La presentación se cierra con una nota de fuentes usadas y las consultas abiertas que la reunión de kick-off debería resolver.

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

> **Nota para el kick-off.** El agente de Kick-off **no aplica** estos umbrales ni emite juicios cuantitativos; la tabla se incluye únicamente como referencia común del sistema, para que los términos que aparezcan en el entendimiento (PSI, backtesting, AUC) se lean con el mismo significado en la reunión.

## Anexo — Distinción entre tipos de insuficiencia

El sistema distingue con precisión tres situaciones que producen acciones distintas y jamás deben confundirse en una misma redacción: el control o la evidencia **NO EXISTE** (nadie lo definió o no se entregó), en cuyo caso el estado es 'No evidenciado' y la acción es solicitar la entrega; el control **EXISTE PERO NO SE EJECUTÓ** en el ciclo, en cuyo caso la acción es exigir su ejecución; y el control **SE EJECUTÓ Y FALLÓ**, en cuyo caso la acción es la remediación del defecto. Confundir 'no existe' con 'falló' oculta la naturaleza del problema y desvía la remediación. A ello se suma 'No verificable', reservado para la evidencia que existe pero no es citable ni reproducible.

## Ejemplo trabajado — bloque de la Lámina 1

Un punto de limitaciones correctamente transcrito:

> **Limitaciones** — "El modelo asume estabilidad de los patrones de prepago observados en 2022-2024 y no es válido bajo cambios estructurales de tasa" (`A4_paso0.md > 7. Supuestos y limitaciones`).

La cita es literal, entre comillas y con su fuente, de modo que el control de Metodología pueda contrastar el supuesto contra su prueba.

## Glosario

| Término | Definición |
|---|---|
| **Lámina 1** | Alcance y Limitaciones del modelo. |
| **Lámina 2** | Flujo de datos Input → Tratamiento y resultado → Usuarios Finales. |
| **Nota de fuentes** | Cierre de la presentación con los documentos usados y las consultas abiertas. |
| **Fuente suficiente** | A4_paso0.md; basta por sí solo para construir ambas láminas. |
| **Fuente opcional** | Informe anterior y evidencia de usos, si se adjuntan. |

## Errores frecuentes

- Añadir una tercera lámina de conclusión o de recomendación de aprobación.
- Reformular los supuestos en vez de transcribirlos literalmente entre comillas.
- Usar la evidencia de usos como si fuera obligatoria cuando no se adjuntó.
- Declarar usuarios, foros o periodicidades que no constan en la evidencia.
- Entregar la presentación sin la nota de fuentes o con puntos sin cita.

## Lista de verificación antes de concluir

1. ¿El encabezado toma modelo, código, tipo, tier, ciclo y fecha del anclaje?
2. ¿La Lámina 1 separa alcance de limitaciones, con supuestos literales?
3. ¿La Lámina 2 tiene las tres cajas con su cita y sin cajas rellenadas por analogía?
4. ¿Se usaron solo A4_paso0.md y, si se adjuntaron, las fuentes opcionales?
5. ¿La presentación cierra con la nota de fuentes y las consultas abiertas?
6. ¿No hay ningún juicio de cumplimiento en toda la presentación?


---

## Referencias

- **SR11-7** — Federal Reserve SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management (2011-04-04). *[referencia internacional canónica]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
