---
name: virf-a3e-insuficiencias-semaforo
description: Clasificación de cada control de calidad de datos ejecutado por A3D en una de las cuatro insuficiencias (no existe, existe pero no se ejecutó, se ejecutó y falló, no verificable) o conforme, con su acción de remediación diferenciada, traducción de estado técnico a semáforo y reconciliación de conteos antes de interpretar. Úsala en el Paso 7 (A3E) como primer paso de la evaluación.
---

# A3E · Las cuatro insuficiencias y el semáforo

Confundir "no existe" con "falló" desvía la remediación: al primero se le pide **crear** el control; al segundo, **corregir los datos**. Clasifica antes de opinar.

## Árbol de clasificación (aplicar en orden)

```
¿El insumo de A3D es legible (notebook ejecutado, Excel 01_Control_de_datos con cifras)?
 └─ No → todo el paso: "Re-ejecución requerida"; no estimar cifras.
¿infractores + conformes == evaluados?
 └─ No → "Descuadre de conteos" (se declara, no se interpreta) → No verificable.
¿El control existe en la evidencia del equipo (bloque 1) o es exigible por el estándar?
 ├─ No existe y es exigible        → INSUFICIENCIA 1: No existe        → Solicitar creación
 ├─ Existe documentado, sin corrida en el ciclo → INSUFICIENCIA 2: No se ejecutó → Exigir ejecución + evidencia
 ├─ Ejecutado, fuera de umbral     → INSUFICIENCIA 3: Falló            → Remediar datos/proceso
 ├─ Umbral [SUPUESTO], columna inexistente, base depurada → INSUFICIENCIA 4: No verificable → Declarar y pedir sustento
 └─ Ejecutado, dentro de umbral declarado → Conforme
```

## Traducción estado técnico (A3D) → semáforo de A3E

| estado_tecnico de A3D | Clasificación A3E | Semáforo | Acción |
|---|---|---|---|
| Dentro de umbral | Conforme | Verde | Ninguna; conservar evidencia |
| Fuera de umbral | Falló | Rojo (o Ámbar si materialidad baja, ver skill de materialidad) | Remediar con responsable y plazo |
| No verificable — umbral no declarado | No verificable | Gris | Formalizar umbral con fuente y fecha |
| No verificable — columna inexistente | No verificable | Gris | Confirmar esquema/nombre; re-ejecutar |
| No existe según evidencia | No existe | Rojo si exigible por tier | Solicitar diseño e implementación del control |
| Error de ejecución | No verificable | Gris | Re-ejecución tras corregir el notebook (devolver a A3D) |
| Control documentado sin resultado del ciclo | No se ejecutó | Ámbar/Rojo | Exigir ejecución y log |

El semáforo de A3E es **técnico**; los estados oficiales (Cumple, No cumple…) los asigna A6. En el informe usa: Conforme · Falló · No se ejecutó · No existe · No verificable.

## Reglas

- Ausencia de evidencia ≠ conforme. Nunca "verde" sin cifra citada.
- Umbral `[SUPUESTO]` → siempre No verificable, aunque el resultado "se vea bien".
- No recalcules a mano lo que el notebook produjo. Si sospechas un error, dilo y pide re-ejecución a A3D.
- Si dos fuentes reportan cifras distintas (notebook vs. reporte del equipo): documenta ambas y su diferencia; no elijas.

## Salida de este paso (insumo de los siguientes)

```markdown
| ID control | Dimensión | Clasificación | Cifra (evaluados / infractores / %) | Umbral (origen) | Cita | Acción tipo |
|---|---|---|---|---|---|---|
| VA-D1-03 | D1 Completitud | Falló | 1 284 330 / 95 040 / 7,40 % | 5 % (manual_controles_datos.md > 2.1) | 01_Control_de_datos.xlsx > Resumen > fila 7 | Remediar |
```
