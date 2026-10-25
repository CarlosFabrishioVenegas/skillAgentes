---
name: virf-a5-severidad-observaciones-previas
description: Asignación de severidad crítica, alta, media o baja a hallazgos documentales según el efecto sobre la capacidad de un tercero de reconstruir y auditar el modelo, verificación del cierre documental de observaciones de la validación anterior, tratamiento de casos borde (PPT de comité, documentos confidenciales, dos versiones, funcionalidad documentada inexistente) y referencias cruzadas a C4 y C5. Úsala en el Paso 10 (A5) al cerrar la matriz.
---

# A5 · Severidad, observaciones previas y casos borde

## 1. Severidad (por efecto en la auditabilidad, no por esfuerzo de remediación)

| Severidad | Criterio | Ejemplos |
|---|---|---|
| Crítica | Un tercero no puede reconstruir el modelo productivo | Sin manual metodológico; documentación de otra versión del modelo en producción |
| Alta | Componente productivo sin documentar; observación documental previa no cerrada | Calibración sin descripción; observación 2025-03 "documentar imputación" sigue abierta |
| Media | Falta versionado, autor o fecha; contenido en documento no formal | Metodología solo en PPT del comité |
| Baja | Erratas, numeración, formato | Tabla numerada dos veces |

## 2. Cierre de observaciones de la validación anterior

```markdown
| Observación previa | Fecha | Compromiso | Estado declarado por el equipo | Evidencia documental de cierre | Estado verificado |
|---|---|---|---|---|---|
| OBS-2025-04 Documentar regla de imputación | 2025-05 | 2025-12 | Cerrada | Manual v3.2 > 3.5 > p.23 | Cerrada |
| OBS-2025-07 Actualizar ventana | 2025-05 | 2025-09 | Cerrada | No se ubicó sección actualizada | No cerrada (Alta) |
```

Regla: **declarada cerrada sin manual actualizado = no cerrada.** Vencida por más de un ciclo → A11 genera hallazgo de gobierno adicional (anótalo como referencia).

## 3. Casos borde

| Caso | Tratamiento |
|---|---|
| Manual completo sin fecha ni versión | Tier 3: Cumple con observación · Tier 1–2: No cumple |
| Contenido correcto en documento no formal (PPT del comité) | Acreditar contenido + observación "ubicación no formal; una presentación no sustituye a un manual" |
| Dos versiones del mismo manual | Evaluar la más reciente; reportar riesgo de control documental; pedir retiro de la obsoleta |
| Manual describe funcionalidad que el código no implementa | Hallazgo de Documentación ("documenta lo inexistente") + referencia cruzada a C4 |
| Documentación excelente de un componente que ya no existe | Hallazgo por documentación desactualizada |
| Firma electrónica sin sello de fecha verificable | Solicitar evidencia del flujo de aprobación |
| Secciones "confidencial" no entregadas | No verificable + solicitud formal de acceso; nunca Cumple por confianza |
| Anexo en imagen (tabla escaneada) | No verificable hasta recibir fuente editable |
| Capturas como única evidencia de un cálculo | Cumple con observación (no reproducible) |
| Actividad no aplicable al tipo de modelo | No aplica **con cita** de la regla del estándar |

## 4. Referencias cruzadas obligatorias

| Hallazgo de C1 | Referenciar a |
|---|---|
| Manual ≠ código | C4 Implementación (A8) |
| Versión documentada ≠ acta | C5 Gobierno (A9) |
| Limitaciones del manual ≠ acta | C5 Gobierno (A9) |
| Supuesto documentado sin prueba | C3 Metodología (A7) |

La fila se conserva en C1 con la nota "ver también Cx": no se traslada ni se borra.

## 5. Consultas

A5 redacta las consultas (respondibles con sí/no/dato, con cita de la evidencia que las origina), pero las **emite A9**. Entrégalas en la sección "Consultas abiertas" con el prefijo `C1-`.
