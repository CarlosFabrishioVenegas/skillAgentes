---
name: virf-a1-plantilla-entendimiento
description: Plantilla oficial del archivo entendimiento_codigo.md (secciones 1 a 10) con el mapeo de cada campo a las dimensiones VIRF C1-C6, reglas de llenado, rótulo de entendimiento parcial y verificador automático de las siete condiciones de calidad antes de entregar. Úsala en el Paso 1 (A1) para estructurar y auditar el .md de entendimiento.
---

# A1 · Plantilla de entendimiento y control de calidad

## Plantilla (no reordenar, no agregar secciones)

```markdown
<!-- Si < 70 % evidenciado, primera línea: "Entendimiento parcial (X % evidenciado)" -->
# Entendimiento del modelo <NOMBRE> (<CODIGO>)

## 1. Identificación
| Campo | Valor | Fuente exacta | Dimensión VIRF |
|---|---|---|---|
| Nombre del modelo | | | C5 |
| Código de inventario | | | C5 |
| Versión vigente | | | C1/C5 |
| Fecha del documento | | | C1 |
| Tipo de modelo | | | C3 |
| Propietario / desarrollador | | | C5 |
| Tier declarado | | | C5 |
| Periodicidad declarada | | | C5/C6 |

## 2. Inputs
| Variable | Variante | Origen (sistema/tabla) | Frecuencia | Responsable | Nombre en herramienta | Fuente exacta | Dimensión |
|---|---|---|---|---|---|---|---|

## 3. Transformaciones y cálculo
<!-- secuencia numerada; fórmulas entre backticks; cita por paso -->

## 4. Calibración
## 5. Outputs
| Output | Descripción | Destino | Frecuencia | Responsable | Fuente exacta | Dimensión |
|---|---|---|---|---|---|---|

## 6. Supuestos (LITERALES)
- "<texto exacto>" (archivo > sección > p.N)

## 7. Limitaciones (LITERALES)
## 8. Uso declarado y usuarios
## 9. Discrepancias y consultas abiertas
| N° | Discrepancia | Fuente A | Fuente B | Consulta (sí/no/dato) |
|---|---|---|---|---|

## 10. Trazabilidad
### Documentos leídos
| Archivo | Versión | Fecha | Páginas leídas | SHA-256 |
### Documentos esperados y no recibidos
### Campos "No evidenciado"
| Campo | Documento que se esperaba que lo contuviera |

## Conteo
Campos completos: N · Campos "No evidenciado": N · Consultas abiertas: N · % evidenciado: X %

## Brechas de evidencia
```

## Mapeo campo → dimensión VIRF (por qué importa cada campo)

| Sección | Alimenta a | Por qué |
|---|---|---|
| 1 Identificación | A5 (C1), A9 (C5) | Vigencia y coherencia versión acta–manual–código |
| 2 Inputs | A3D/A6 (C2), A8 (C4) | Linaje, responsable por campo, equivalencia de nombres |
| 3–4 Transformaciones y calibración | A7 (C3), A8 (C4) | Parámetros a contrastar con el código |
| 5 Outputs | A10 (C6) | Cadena de uso por output |
| 6–7 Supuestos/limitaciones | A7 (C3), A9 (C5) | Cada supuesto requiere prueba o monitoreo |
| 8 Uso | A10 (C6), A9 (C5) | Uso declarado vs. observado |

Si el validador pide priorizar: entrega primero 2, 3 y 5.

## Reglas de llenado

- Campo sin evidencia → literal `No evidenciado` + fila en sección 10. Nunca vacío.
- Supuestos y limitaciones: entre comillas, sin parafrasear. Si no hay: `No evidenciado` (la sección no se elimina).
- Manual vs. acta en contradicción → registrar ambas, marcar "Discrepancia manual vs. acta", consulta abierta. No decidir.
- Nombres distintos entre manual y herramienta → columna "Nombre en herramienta".
- Versiones sucesivas en un capítulo → vigente por fecha; anteriores como historia.

## Verificación antes de entregar

```bash
python scripts/verificar_entendimiento.py entendimiento_<codigo>.md --codigo <CODIGO>
```

El script comprueba las siete condiciones:
1. Toda línea de tabla con contenido tiene cita con página (`p.N`) o marca `No evidenciado`.
2. Los ítems de supuestos/limitaciones están entre comillas.
3. Tablas de inputs y outputs con todas sus columnas.
4. No hay celdas vacías en campos obligatorios.
5. Cada documento leído tiene SHA-256 de 64 hex.
6. Consultas abiertas numeradas.
7. El código del modelo es idéntico en todas sus menciones.

No entregues hasta que reporte `7/7`. Si falla, corrige y vuelve a ejecutar. Calcula y rotula el % evidenciado aunque esté bajo: entregar siempre.
