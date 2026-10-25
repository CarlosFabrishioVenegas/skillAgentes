---
name: virf-ak-lamina-alcance-limitaciones
description: Redacción de la lámina 1 del kick-off de validación - Alcance (propósito de negocio, uso autorizado, perímetro de productos o carteras) y Limitaciones (supuestos y limitaciones literales entre comillas, condiciones de uso, observaciones abiertas del ciclo anterior) a partir de A4_paso0.md, con cita por punto y advertencia de base parcial. Úsala en el Paso 5 (agente AK).
---

# AK · Lámina 1 — Alcance y Limitaciones

Fuente principal y suficiente: `A4_paso0.md`. Opcionales: informe de validación anterior, evidencia de usos. Nada más.

## Dónde está cada dato en A4_paso0.md

| Elemento de la lámina | Sección del Paso 0 |
|---|---|
| Modelo, código, tipo, tier, ciclo, fecha de corte | 0 Portada |
| Propósito de negocio / decisión que soporta | 1 Resumen ejecutivo; 3 eslabón 7 |
| Uso declarado y autorizado | 6 Outputs; 12; acta citada en 2 |
| Perímetro (productos, carteras, mesas) | 1, 4 (columna variante), 7 |
| Supuestos y limitaciones | 7 (literales) |
| Observaciones abiertas | 13 |
| Base parcial | primera línea ("Entendimiento parcial…") y 14 |

## Formato

```markdown
## Kick-off — <Modelo> (<Código>) · Tier <t> · Ciclo <ciclo>
> ⚠ Base parcial: el entendimiento está al X % (A4_paso0.md > 14). Faltan: … (solo si aplica)

### Lámina 1 — Alcance y Limitaciones
**Alcance**
- Soporta <decisión de negocio> (A4_paso0.md > 1)
- Uso autorizado: <uso> (A4_paso0.md > 6)
- Perímetro: <productos/carteras> (A4_paso0.md > 4)

**Limitaciones**
- "<supuesto literal>" (A4_paso0.md > 7)
- "<limitación literal>" (A4_paso0.md > 7)
- Condición de uso válida: <…> (A4_paso0.md > 7)
- Observación previa abierta: <…> — estado <…> (Informe_Validacion_2025.pdf > 4 > p.12)
```

## Reglas

1. Cada viñeta termina con su cita `(A4_paso0.md > sección)`. Sin cita = defecto.
2. Supuestos/limitaciones: **copiar literal** del Paso 0, comillas incluidas. No resumir aunque sean largos; si son muchos, dividir en dos columnas en la PPT, no recortar texto.
3. Sin informe anterior: omitir observaciones previas y anotarlo en "Fuentes y consultas abiertas" ("No se adjuntó informe de validación anterior"). No inventar observaciones.
4. Dos usos distintos (declarado vs observado): mostrar ambos y generar consulta.
5. Si algo no consta: "No evidenciado".
6. Versión corta para la reunión: solo titulares de cada viñeta con su cita; **nunca** eliminar la caja de limitaciones.

## Ejemplo de viñeta correcta / incorrecta

- ✔ `"El modelo asume que la estructura de la cartera retail se mantiene estable en el horizonte de 12 meses" (A4_paso0.md > 7)`
- ✘ `Asume estabilidad de cartera` → parafraseado, sin comillas, sin cita.

## Fuera de alcance

Si piden opinión ("¿el modelo está bien?"): "Fuera de alcance del Kick-off; corresponde a los agentes de control A5 a A10 y al validador final A11".
