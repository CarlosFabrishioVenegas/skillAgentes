---
name: virf-a11-conclusion-plan-accion
description: Reglas de conclusión de la validación periódica (cobertura menor a 100 por ciento implica Validación incompleta, No cumple crítico en Implementación o Usos impide satisfactoria, ausencia de uso obliga a recomendar retiro, observación vencida más de un ciclo genera hallazgo de gobierno), redacción de la conclusión en máximo 12 líneas con orden fijo, plan de acción consolidado, anexo de trazabilidad y checklist de calidad antes de firmar. Úsala en el Paso 15 (A11) para cerrar el informe.
---

# A11 · Conclusión, plan de acción y firma

## 1. Reglas de conclusión (sin excepción, en este orden)

| # | Condición | Efecto |
|---|---|---|
| R1 | Cobertura < 100 % | "Validación incompleta" (nunca satisfactoria, aunque todo lo evaluado cumpla) |
| R2 | "No cumple" de severidad **crítica** en Implementación (C4) o Usos (C6) | Impide "Validación satisfactoria" |
| R3 | Ausencia total de evidencia de uso | Recomendación obligatoria de retiro, **reproducida en la conclusión** |
| R4 | Observación del ciclo anterior vencida por más de un ciclo | Hallazgo de gobierno adicional (generado por A11 si nadie lo levantó) |
| R5 | Uso satisfactorio pero sin manual vigente | No puede ser satisfactoria: riesgo de dependencia de conocimiento no documentado |
| R6 | Dos agentes con estados distintos sobre el mismo hecho | "Inconsistencia entre controles", hallazgo de proceso hasta su resolución |

Veredictos posibles: Validación satisfactoria · Validación con observaciones · Validación incompleta · Validación no satisfactoria.

## 2. Conclusión (máximo 12 líneas, orden fijo)

1. **Estado global** con su fundamento en una línea.
2. **Los tres hallazgos de mayor severidad**, cada uno con su cifra y su control de origen.
3. **Efecto concreto sobre el uso del modelo**: si sus resultados pueden seguir empleándose y bajo qué condición.
4. **Condiciones específicas y verificables** para levantar el estado observado.

Plantilla:

```markdown
Validación incompleta: cobertura de 92 % (46 de 50 actividades del Tier 2); 4 actividades de C6 sin evidencia.
1) C4 · El código aplica corte 620 vs 640 documentado; reclasifica 4 128 clientes (2,7 %) — No cumple, crítica.
2) C2 · ingreso_declarado con 7,4 % de nulos imputados sin regla; desplaza el score +4 pts y reclasifica 318 clientes — No cumple, alta.
3) C5 · Tier 2 en acta vs Tier 1 recalculado (exposición S/ 640 MM) — No cumple, alta.
Efecto: la PD puede seguir usándose para provisión solo con el corte aprobado y la reclasificación revertida.
Condiciones para levantar: (a) acta de aprobación del corte vigente; (b) regla de imputación aprobada y base corregida;
(c) reevaluación formal de tiering; (d) evidencia de envío y sustento en comité para 2026T2–T3.
```

Prohibido: frases de cortesía, valoraciones del equipo dueño, proyecciones sobre ciclos futuros, suavizar estados por plazos, presión o relación con el área. La conclusión **va después** de la tabla, nunca antes.

## 3. Plan de acción consolidado

```markdown
| Acción | Responsable | Fecha comprometida | Control de origen | Severidad |
```
Ordenado por fecha. Todas las filas con responsable y fecha; dependencias de otras áreas se anotan en la acción.

## 4. Anexo de trazabilidad y firmas

- Evidencias leídas con SHA-256 (de `hash_evidencias.py`).
- Evidencias esperadas y no recibidas.
- Consultas abiertas con su estado y efecto (del registro de A9).
- Fecha de corte de la evidencia (si se firma tras el cierre contable).
- Espacio de firma del validador y del revisor.

## 5. Checklist antes de firmar (si alguno falla, no se emite; se devuelve y se documenta la devolución)

- [ ] Cobertura reportada y coherente con el estándar filtrado por tier.
- [ ] Cada fila con estado, resultado, evaluación y fuente; ninguna fuente vacía.
- [ ] Columna de fuente conserva la cita original del agente, sin abreviar ni reescribir; cada fila con agente de origen.
- [ ] Hallazgos críticos reflejados en la conclusión.
- [ ] Recomendación de retiro reproducida si aplica R3.
- [ ] Plan de acción con responsable y fecha en todas las filas.
- [ ] Consultas abiertas con su efecto declarado.
- [ ] Anexo de trazabilidad con hashes.
- [ ] Todos los controles citan la misma versión de evidencia.

## 6. Interacción

- "Emite aunque la cobertura esté incompleta, vence el plazo" → se emite rotulado "Validación incompleta", con la lista de actividades no evaluadas y el motivo.
- "Fusiona hallazgos para acortar" → la fusión rompe la trazabilidad al estándar; ofrecer un resumen ejecutivo separado que no reemplaza la tabla.
