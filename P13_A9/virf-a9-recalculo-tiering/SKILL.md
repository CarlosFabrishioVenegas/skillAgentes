---
name: virf-a9-recalculo-tiering
description: Recálculo independiente del tier del modelo con los criterios vigentes del banco (materialidad o exposición, criticidad regulatoria, complejidad, alcance de uso), con script configurable por archivo JSON de criterios, regla de propagación cuando el output alimenta un modelo de mayor tier, comparación con el tier del acta y efecto del desfase sobre las actividades exigibles en la validación. Úsala en el Paso 13 (A9).
---

# A9 · Recálculo de tiering

Un tiering desactualizado es hallazgo de severidad alta: determina qué actividades eran exigibles **en esta misma validación**.

## 1. Criterios: siempre los del banco

Carga los criterios vigentes en `criterios_tiering.json` con su fuente. Ejemplo de estructura (los valores son ilustrativos; reemplázalos por los de la política):

```json
{
  "fuente": "Politica_Tiering_Modelos_v2.pdf > 3.1 > p.6",
  "criterios": {
    "exposicion_mm": {"peso": 0.4, "cortes": [100, 500], "puntajes": [1, 2, 3]},
    "criticidad_regulatoria": {"peso": 0.3, "mapa": {"ninguna": 1, "reporte": 2, "capital_o_provision": 3}},
    "complejidad": {"peso": 0.2, "mapa": {"baja": 1, "media": 2, "alta": 3}},
    "alcance_uso": {"peso": 0.1, "mapa": {"informativo": 1, "decision_area": 2, "decision_institucional": 3}}
  },
  "tier_por_puntaje": [[2.4, 1], [1.7, 2], [0, 3]]
}
```

Si el banco no entregó criterios: el script corre con el archivo que le des, pero el resultado se rotula `[SUPUESTO] criterios no entregados` y el campo G03 queda **No verificable** (no "No cumple").

## 2. Ejecutar

```bash
python scripts/recalcular_tiering.py criterios_tiering.json --exposicion_mm 640 --criticidad_regulatoria capital_o_provision \
    --complejidad media --alcance_uso decision_institucional --tier_acta 2 --tier_consumidor 1
```

Salida: puntaje por criterio, puntaje total, tier recalculado, tier por propagación, tier final, comparación con el acta.

## 3. Propagación

Si el output del modelo alimenta a otro de tier más exigente (`--tier_consumidor`), el tier efectivo es `min(tier_calculado, tier_consumidor)` (1 = más exigente). Un modelo declarado de bajo impacto que alimenta un Tier 1 debe reevaluarse → hallazgo.

## 4. Bloque (a) del entregable

```markdown
| Criterio | Valor evidenciado | Fuente del valor | Puntaje | Peso |
|---|---|---|---|---|
| Exposición | S/ 640 MM | Reporte_Cartera_2026Q2.xlsx > Resumen > C9 | 3 | 0,4 |
| … | | | | |
**Tier recalculado:** 1 · **Tier del acta (G03):** 2 · **Resultado:** No cumple — tiering desactualizado.
**Efecto en esta validación:** las actividades exigibles a Tier 1 no incluidas en el alcance (N actividades: IDs …) quedan "No evidenciado" y se reportan a A11.
```

## 5. Casos borde

| Caso | Tratamiento |
|---|---|
| Tier correcto según el acta pero criterios del banco desactualizados | Hallazgo de **marco**, no del modelo; observación de proceso |
| Cambio de tier aprobado pero no reflejado en el estándar aplicado | Reportar desfase y efecto sobre actividades exigibles |
| Exposición creció mucho desde la aprobación | Consulta: ¿se solicitó reevaluación? (ver ejemplo de consulta en el registro) |
