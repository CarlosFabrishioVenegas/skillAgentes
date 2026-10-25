# Metodología — Control de Metodología

**Validación cuantitativa: VaR, IFRS 9, conductuales y métricas**

Base de Conocimiento VIRF — Validación Periódica de Modelos (MRM)  
Agente A7 · Control de Metodología  
Documento de Metodología · Versión 2.0 · 2026-09-04


---

> **Nota de validación.** Documento de conocimiento (doctrina) para un agente de validación. Las referencias a la normativa de la SBS del Perú han sido **validadas contra el texto oficial** de cada resolución (fuente primaria): Res. N° 00053-2023, N° 272-2017, N° 4906-2017, N° 6328-2009 y N° 525-2024; las demás resoluciones SBS citadas quedan validadas de forma indirecta por su cita literal en el Art. 2 de la Res. N° 00053-2023. Los marcos internacionales (SR 11-7, BCBS 239, FRTB, IFRS 9 y la literatura académica) se incluyen como **referencia conceptual canónica**, no como norma peruana. Los umbrales cuantitativos (PSI, AUC, semáforo de backtesting, etc.) son convenciones de industria que se calibran y aprueban en la política interna de validación.

## Contenido

- [VaR: metodologías y escalado](#var-metodologias-y-escalado)
- [Backtesting de VaR: Kupiec y Christoffersen](#backtesting-de-var-kupiec-y-christoffersen)
- [Expected Shortfall y FRTB](#expected-shortfall-y-frtb)
- [IFRS 9: ECL, staging y SICR](#ifrs-9-ecl-staging-y-sicr)
- [Modelos conductuales: prepago y depósitos sin vencimiento](#modelos-conductuales-prepago-y-depositos-sin-vencimiento)
- [Métricas de discriminación y calibración](#metricas-de-discriminacion-y-calibracion)
- [Reproducibilidad de métricas y muestras independientes](#reproducibilidad-de-metricas-y-muestras-independientes)
- [Anexo — Tabla maestra de umbrales cuantitativos](#anexo-tabla-maestra-de-umbrales-cuantitativos)
- [Anexo — Distinción entre tipos de insuficiencia](#anexo-distincion-entre-tipos-de-insuficiencia)
- [Ejemplo trabajado — evaluación de calibración](#ejemplo-trabajado-evaluacion-de-calibracion)
- [Glosario](#glosario)
- [Errores frecuentes](#errores-frecuentes)
- [Lista de verificación antes de concluir](#lista-de-verificacion-antes-de-concluir)
- [Referencias](#referencias)


---

## VaR: metodologías y escalado

Tres métodos. **Histórico**: percentil empírico de la distribución de P&L reevaluada; no asume normalidad pero depende de la ventana. **Paramétrico o varianza-covarianza**: `VaR = z * sigma * raiz(t)`, con z = 1.645 al 95 % y z = 2.326 al 99 %; asume normalidad y linealidad, débil ante colas gruesas y opcionalidad. **Monte Carlo**: simulación de factores, flexible pero costosa y sensible al modelo generador. Escalado temporal bajo independencia: `VaR(h dias) = VaR(1 dia) * raiz(h)`.

## Backtesting de VaR: Kupiec y Christoffersen

**Test de Kupiec** (proporción de fallos, cobertura incondicional):

```
LR_uc = -2 * ln[ ((1-p)^(N-x) * p^x) / ((1-x/N)^(N-x) * (x/N)^x) ]   ~  chi2(1)
```

con p = 1 - nivel de confianza, N observaciones y x excepciones. **Test de Christoffersen**: de independencia (LR_ind, penaliza el agrupamiento de excepciones) y de cobertura condicional `LR_cc = LR_uc + LR_ind ~ chi2(2)`. **Semáforo de Basilea** (VaR 99 %, 250 días): zona verde 0 a 4 excepciones, amarilla 5 a 9, roja 10 o más; el multiplicador de capital escala típicamente desde 3.0 hacia 4.0. Kupiec verifica el número de excepciones; Christoffersen añade que no estén agrupadas en el tiempo.

## Expected Shortfall y FRTB

Bajo FRTB (BCBS d457, enero 2019), el **Expected Shortfall al 97.5 %** reemplaza al VaR como medida de capital en el modelo interno: `ES = E[ L | L > VaR ]`, es decir, la pérdida media condicionada a superar el VaR. El ES es **coherente** (subaditivo, respeta la diversificación) y captura la severidad de la cola más allá del cuantil, corrigiendo las dos limitaciones centrales del VaR.

## IFRS 9: ECL, staging y SICR

La pérdida esperada se calcula como:

```
ECL = SUMA_t [ PD_t * LGD_t * EAD_t * factor_descuento_t ]
```

El **staging** define el alcance temporal: **Stage 1** (sin aumento significativo del riesgo, ECL a 12 meses); **Stage 2** (aumento significativo del riesgo o **SICR**, ECL *lifetime*, aún *performing*); **Stage 3** (deteriorado o en *default*, ECL lifetime con interés sobre saldo neto). El enfoque *forward-looking* pondera múltiples escenarios macroeconómicos por probabilidad. La PD es a 12 meses o *lifetime* según el stage. El criterio de SICR (transición a Stage 2) y su umbral son objeto central de validación (IFRS 9, sección 5.5; verificar el párrafo).

## Modelos conductuales: prepago y depósitos sin vencimiento

**Prepago** mediante SMM (*single monthly mortality*) y CPR (*conditional prepayment rate*): `CPR = 1 - (1 - SMM)^12`. **Depósitos sin vencimiento (NMD)**: descomposición en núcleo estable y parte volátil, asignación de perfil de vencimiento y **duración conductual**, con topes regulatorios de vencimiento medio en el marco IRRBB. La validación verifica la estabilidad del comportamiento estimado y su sensibilidad a cambios de tasa.

## Métricas de discriminación y calibración

**Discriminación**: AUC/ROC; `KS = max_x |F_no_evento(x) - F_evento(x)|`; `Gini = 2*AUC - 1`. **Calibración**: prueba de Hosmer-Lemeshow `H = SUMA_g (O_g - E_g)^2 / [E_g (1 - E_g/n_g)] ~ chi2(g-2)`, con g grupos (típicamente 10); test binomial y de Jeffreys para PD por rating. **Umbrales orientativos, a calibrar internamente**: AUC > 0.7 aceptable y > 0.8 bueno; Gini entre 0.4 y 0.6 típico en scoring minorista; KS > 0.3 razonable. Estos valores son convención de industria, no mínimos regulatorios.

## Reproducibilidad de métricas y muestras independientes

El control recalcula o solicita el script de las métricas reportadas; una métrica que no se reproduce con los datos y el código entregados es 'No verificable', y esto es más grave que una métrica baja. Verifica que la muestra de validación sea independiente de la de desarrollo: una muestra construida con la misma cosecha no acredita independencia, y el traslape se cuantifica si hay datos. Una segmentación con celdas de tamaño insuficiente se reporta con el número de observaciones por celda y su efecto sobre la estabilidad de los estimadores.

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

## Ejemplo trabajado — evaluación de calibración

> 'El sustento teórico de la calibración es pertinente, pero la tasa central usada (3,10 %) corresponde a la cosecha 2023 y no a la ventana 2024-2025 declarada en el manual; el escalamiento subestima la PD media en 34 pbs frente a la observada en el mismo período. Fuente: `Manual_v3.pdf > 5.4 > p.41`; `herramienta_pd.xlsx > Calibracion > F22`.'

La fila separa el sustento (pertinente) de la ejecución (defectuosa por usar una ventana distinta a la declarada) y cuantifica el impacto en puntos básicos.

## Glosario

| Término | Definición |
|---|---|
| **VaR / ES** | Cuantil de pérdida (VaR) y pérdida media en la cola (Expected Shortfall). |
| **Kupiec / Christoffersen** | Pruebas de backtesting: número de excepciones y su independencia temporal. |
| **ECL / staging / SICR** | Pérdida esperada, clasificación en etapas y aumento significativo del riesgo (IFRS 9). |
| **AUC / KS / Gini** | Métricas de discriminación de un modelo de clasificación. |
| **CPR / SMM** | Tasas de prepago condicional anual y mensual. |
| **Fuga de información** | Uso de datos posteriores al momento de decisión que infla el desempeño. |

## Errores frecuentes

- Aprobar una técnica por ser 'estándar de la industria' sin sustento interno documentado.
- Aceptar una métrica calculada sobre la muestra de desarrollo como evidencia de desempeño.
- Citar un paper que no corresponde a la técnica efectivamente implementada.
- Tratar como cumplimiento tácito la ausencia de un umbral de aceptación declarado.
- Mezclar en una sola fila el sustento teórico y la ejecución de la prueba.

## Lista de verificación antes de concluir

1. ¿Cada decisión metodológica tiene sustento citable y pertinente a la técnica implementada?
2. ¿Las métricas reportadas se reprodujeron con los datos y el código entregados?
3. ¿La muestra de validación es independiente de la de desarrollo?
4. ¿Se verificó ausencia de fuga de información en la construcción de variables?
5. ¿El backtesting de VaR aplicó Kupiec y Christoffersen con su resultado?
6. ¿Cada métrica se contrastó contra un umbral de aceptación declarado?


---

## Referencias

- **FRTB** — BCBS d457 — Minimum capital requirements for market risk / FRTB (ene-2019). *[referencia internacional canónica]*
- **KUPIEC1995** — Kupiec, P. (1995), Techniques for verifying the accuracy of risk measurement models, Journal of Derivatives 3(2). *[referencia internacional canónica]*
- **CHRIST1998** — Christoffersen, P. (1998), Evaluating Interval Forecasts, International Economic Review 39(4). *[referencia internacional canónica]*
- **JORION** — Jorion, P., Value at Risk: The New Benchmark for Managing Financial Risk (3.ª ed.). *[referencia internacional canónica]*
- **IFRS9** — IFRS 9 / NIIF 9 — Financial Instruments, sección 5.5 (deterioro y ECL). *[referencia internacional canónica]*
- **HOSMER** — Hosmer, D. & Lemeshow, S., Applied Logistic Regression. *[referencia internacional canónica]*

*Regla maestra de auditabilidad: ninguna afirmación de validación existe sin su fuente exacta (documento > sección > página; archivo > hoja > celda; archivo > línea).*
