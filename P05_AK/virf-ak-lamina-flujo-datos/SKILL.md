---
name: virf-ak-lamina-flujo-datos
description: Redacción de la lámina 2 del kick-off - flujo de tres cajas Input de Datos, Tratamiento y resultado de los datos, Usuarios Finales - con fuentes, sistemas y tablas concretas, secuencia real de transformaciones y output efectivo, destinatarios, foro o sistema y periodicidad, más la nota de fuentes, consultas abiertas y la rúbrica de siete puntos. Úsala en el Paso 5 (agente AK).
---

# AK · Lámina 2 — Flujo de datos

## Mapeo de cajas a A4_paso0.md

| Caja | Contenido mínimo | Secciones del Paso 0 |
|---|---|---|
| Input de Datos | Fuente → sistema → tabla de cada input principal + responsable | 4 Inputs, 3 eslabón 1 |
| Tratamiento y resultado | Filtros → construcción de variables → cálculo → calibración → output (curva, score, %, provisión) | 3 eslabones 2–5, 5 |
| Usuarios Finales | Área destinataria, foro/sistema donde se expone, periodicidad, decisión tomada; modelo aguas abajo por código | 6 Outputs, 3 eslabones 6–7, 12 |

## Formato

```markdown
### Lámina 2 — Flujo de datos
| Input de Datos | → | Tratamiento y resultado de los datos | → | Usuarios Finales |
|---|---|---|---|---|
| DM_RIESGOS.DM_CLIENTE (Gobierno de Datos), DM_OPERACION (TI Riesgos) (A4_paso0.md > 4) | → | 1) Filtro antigüedad ≥ 6 m 2) Imputación ingreso 3) Score logístico 11 var 4) Escalamiento a tasa central → PD por cliente (A4_paso0.md > 3, 5) | → | Riesgo de Crédito Retail · Tablero Riesgos + Comité de Provisiones · mensual · insumo de provisión IFRS 9; alimenta MOD-0533 (A4_paso0.md > 6) |

**Notas de la caja Input de Datos:** …
**Notas de la caja Tratamiento y resultado:** …
**Notas de la caja Usuarios Finales:** …

### Fuentes y consultas abiertas
- Documentos usados: A4_paso0.md (SHA-256 …); [informe anterior]; [evidencia de usos]
- Consultas abiertas para el kick-off:
  1. ¿… ? (A4_paso0.md > 14, consulta N)
```

## Reglas de redacción por caja

- **Input:** nombres de tablas/sistemas concretos. "Datamart de riesgos" sin tabla no basta → completa con la tabla del Paso 0 o marca "tabla No evidenciada".
- **Tratamiento:** secuencia real del código (sección 5 del Paso 0), no la del manual cuando difieren; si difieren, menciona "ver discrepancia N" y lleva la discrepancia a consultas.
- **Usuarios Finales:** a quién, dónde, cada cuánto. Sin evidencia de usos: usar solo el uso declarado del acta que conste en el Paso 0; si tampoco consta, "No evidenciado" + consulta.
- Caja incompleta: dilo en la propia caja ("Destinatario: No evidenciado").

## Consultas para el kick-off

Prioriza las que la reunión puede cerrar en el momento: versión productiva, cortes divergentes, usuarios reales, foro de sustento, periodicidad. Formato respondible (sí/no/dato).

## Rúbrica antes de entregar (las siete deben ser sí)

1. Ambas láminas con todos sus elementos citados.
2. Supuestos y limitaciones literales entre comillas.
3. Caja Input con fuentes, sistemas y tablas concretas.
4. Caja Tratamiento con la secuencia real y el output efectivo.
5. Caja Usuarios con destinatario, foro/sistema y periodicidad.
6. Todo elemento sin sustento dice "No evidenciado".
7. Nombre, código, tipo y tier coinciden con el anclaje (portada del Paso 0).

Interacción: "rellenar como sea" → devolver lista de faltantes. Texto pegado en el chat → cita "texto en sesión, sin archivo fuente" (débil).
