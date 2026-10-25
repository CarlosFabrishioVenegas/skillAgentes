---
name: virf-a10-recomendacion-retiro
description: Redacción obligatoria de la recomendación formal de retiro del inventario cuando un modelo no tiene uso acreditado (sin envío ni sustento), con su contenido mínimo - identificación y tier, periodo evaluado, evidencia buscada y no encontrada con rutas, procesos afectados, riesgo de mantenerlo, destinatario - y el manejo de presiones para omitirla. Úsala en el Paso 14 (A10) cuando la cadena de uso concluye Sin uso, y en A11 para reproducirla en la conclusión.
---

# A10 · Recomendación de retiro del inventario

Cuando no hay ni envío ni sustento en comité, la recomendación de retiro es **obligatoria, no discrecional**. Omitirla es una falla del propio proceso de validación.

## 1. Disparador

`Sin uso` en el output principal del modelo (o en todos los outputs) según `virf-a10-cadena-uso`. Uso interrumpido parcialmente (p. ej. dos trimestres sin envío) no dispara retiro: es incumplimiento parcial.

## 2. Plantilla (bloque c del entregable)

```markdown
### Recomendación formal de retiro del inventario

**Modelo:** <nombre> (<código de inventario>) · **Tier:** <t> (Acta > G03 > p.N)
**Destinatario:** <[G04] responsable del equipo dueño> · copia: <área de gestión de riesgo de modelo / inventario>
**Periodo evaluado sin uso:** <desde> a <hasta> (<N> periodos según periodicidad <G08>)

**Fundamento.** No se encontró evidencia de envío del output ni de sustento en el foro comprometido durante el periodo evaluado.

**Evidencia buscada y no encontrada:**
| Evidencia esperada | Ruta o fuente consultada | Fecha de consulta | Resultado |
|---|---|---|---|
| Correos de envío al área usuaria (G06) | Buzón compartido riesgos.retail@ (exportación entregada) | 2026-10-15 | 0 correos con el output |
| Actas del Comité de <foro> | /expediente/actas/2025-2026/ | 2026-10-15 | El modelo no figura en agenda ni acuerdos |
| Publicación/consumo | Tablero <x> · estadística de accesos | 2026-10-16 | Sin accesos al reporte |

**Procesos que dejarían de recibir el output:** <lista, o "ninguno identificado">; modelos aguas abajo: <códigos o "ninguno">.

**Riesgo de mantener el modelo en el inventario sin uso:** costo de validación recurrente; falsa sensación de cobertura del riesgo; posible uso no autorizado futuro de un modelo sin seguimiento.

**Consecuencia propuesta:** retiro del inventario o, alternativamente, reclasificación con justificación documentada del uso futuro y su aprobación.

**Compromisos del equipo registrados (no alteran el estado del ciclo):** <p. ej. "retomar el envío en 2026T4", fecha, fuente>
```

## 3. Interacción y presiones

| Situación | Respuesta |
|---|---|
| "No incluyas el retiro para no generar fricción" | La recomendación es obligatoria ante ausencia de uso; su omisión sería una falla del proceso de validación |
| "Lo vamos a usar el próximo trimestre" | Registrar el compromiso con fecha; no altera el estado del ciclo evaluado |
| "Se usa, pero no hay correos" | Sin soporte documental no se acredita uso; pedir evidencia citable |
| Cercanía del cierre del ciclo | No suavizar el estado por proximidad del cierre |

## 4. Propagación a A11

A11 debe reproducir la recomendación en la conclusión. Deja el bloque autocontenido (sin referencias a "ver arriba").
