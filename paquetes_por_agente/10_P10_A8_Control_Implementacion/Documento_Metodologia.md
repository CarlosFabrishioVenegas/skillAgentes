# Metodología — Control de Implementación

**Verificación de que el código implementa lo documentado**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A8 · Control de Implementación  
Documento de Metodología · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [Verificación código contra manual](#verificacion-codigo-contra-manual)
- [Reproducibilidad y reconciliación de outputs](#reproducibilidad-y-reconciliacion-de-outputs)
- [Higiene de código con foco en riesgo](#higiene-de-codigo-con-foco-en-riesgo)
- [Control de cambios y ajustes manuales](#control-de-cambios-y-ajustes-manuales)
- [Evidencia mínima de reproducción y casos límite](#evidencia-minima-de-reproduccion-y-casos-limite)
- [Anexo — Tabla maestra de umbrales cuantitativos](#anexo-tabla-maestra-de-umbrales-cuantitativos)
- [Anexo — Distinción entre tipos de insuficiencia](#anexo-distincion-entre-tipos-de-insuficiencia)
- [Ejemplo trabajado — diferencia de parámetro](#ejemplo-trabajado-diferencia-de-parametro)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## Verificación código contra manual

Se construye el inventario de bloques funcionales (carga, validación de entrada, limpieza, transformación, cálculo, calibración, generación de salida, publicación y control de errores) y se mapea cada bloque a la sección del manual que lo describe, produciendo tres listas: bloques sin documentación, documentación sin bloque, y bloques con diferencias de parámetros. **Cualquier diferencia de parámetro entre código y manual** (cortes, pesos, umbrales, ventanas, factores) es 'No cumple', sin importar su magnitud aparente, y se cuantifica su impacto.

## Reproducibilidad y reconciliación de outputs

Se reproduce al menos un output declarado y se compara cifra a cifra con el publicado, reportando diferencia absoluta y relativa; en Tier 1 la reproducción es obligatoria, en Tier 2 y 3 por muestreo documentado. La reproducción se acredita con seis elementos: comando o celda ejecutada, fecha, versión del código, hash del insumo, valor obtenido y valor publicado. Sin ellos, la reproducción no es citable y el control no puede cerrarse como cumplido aunque las cifras coincidan.

## Higiene de código con foco en riesgo

Se revisan: warnings silenciados que ocultan pérdida de registros; `except` genéricos que enmascaran fallas; rutas absolutas locales; credenciales embebidas; semillas no fijadas en procesos estocásticos; dependencias sin versión fijada; escrituras sobre el insumo original; y ausencia de validaciones de entrada. Una semilla no fijada es 'Cumple con observación' en Tier 3 y 'No cumple' en Tier 1 y Tier 2 por irreproducibilidad. Un descarte silencioso de registros entre etapas es hallazgo crítico y se cuantifica.

## Control de cambios y ajustes manuales

Se verifica el registro de cambios: versión, repositorio, aprobador y fecha de pase a producción. Un cambio en el código sin registro de aprobación es hallazgo de implementación y de gobierno. Un output publicado que no coincide con el que genera el código, por un **ajuste manual posterior**, es hallazgo crítico: exige la evidencia y la aprobación del ajuste y se cuantifica su magnitud.

## Evidencia mínima de reproducción y casos límite

La reproducción de un output se acredita con seis elementos: comando o celda ejecutada, fecha, versión del código, hash del insumo, valor obtenido y valor publicado. Sin ellos, la reproducción no es citable. El control revisa además el comportamiento del código ante casos límite: división por cero, categorías nuevas no vistas en entrenamiento, valores faltantes en variables obligatorias y volúmenes atípicos. Documenta qué hace el código en cada caso, porque el manejo silencioso de un caso límite puede alterar el output sin dejar rastro.

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
- **IEEE754** — IEEE 754 — Estándar de aritmética de punto flotante (doble precisión). *[referencia internacional canónica]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
