---
name: virf-a4-plantilla-paso0
description: Plantilla obligatoria de 17 secciones de A4_paso0.md (fuente única de verdad del ciclo de validación), regla de exhaustividad, cálculo del porcentaje de completitud, estado de admisibilidad de la herramienta, guion de infografía de una página con pie de citas y verificador de secciones. Úsala en el Paso 4 (agente A4, Paso 0) para redactar y auditar el entendimiento consolidado.
---

# A4 · Plantilla del Paso 0

A4_paso0.md se re-adjunta como ancla en A5–A11. Criterio de éxito: un validador que solo lea este documento puede (a) explicar el modelo de punta a punta, (b) ejecutar la herramienta, (c) saber dónde está cada evidencia y cuál falta, y (d) iniciar los seis controles sin preguntar al equipo dueño.

**Exhaustividad:** sin límite de longitud. Si dudas entre incluir u omitir un dato evidenciado, inclúyelo.

## Plantilla

```markdown
<!-- si completitud < 80 %: primera línea "Entendimiento parcial (X % evidenciado)" -->
# Paso 0 — Entendimiento consolidado · <Modelo> (<Código>)

## 0. Portada
| Campo | Valor | Fuente exacta |
|---|---|---|
| Modelo | | |
| Código de inventario | | |
| Tipo | Crédito/IFRS9 · Mercado/VaR · ALM/IRRBB · LaR · Operacional · Conductual | |
| Tier | | |
| Ciclo | | |
| Fecha de corte | | |
| % completitud del entendimiento | X % (N/M campos) | cálculo sección 14 |
| ESTADO DE ADMISIBILIDAD | (ver sección 8) | |

## 1. Resumen ejecutivo
## 2. Identidad y versión (fuentes y discrepancias de versión)
## 3. Cadena del modelo end-to-end (doble cita)
## 4. Inputs
| Variable | Origen (sistema/tabla) | Frecuencia | Responsable | Fuente exacta |
## 5. Transformaciones y lógica de cálculo (código real vs. manual)
## 6. Outputs
| Output | Descripción | Destinatario | Canal | Periodicidad | Fuente exacta |
## 7. Supuestos y limitaciones (LITERALES, con cita)
## 8. Estado de admisibilidad de la herramienta
## 9. Discrepancias entre fuentes (manual/acta/código/minutas) → consultas
## 10. Discrepancias DOCUMENTACIÓN ↔ CÓDIGO
| Elemento | Qué dice el manual (cita) | Qué hace el código (cita) | Impacto | Control afectado |
## 11. Mapa de evidencia por control
| Control | Actividades del estándar aplicables al tier | Evidencia disponible (ruta exacta) | Evidencia faltante | Fuente exacta |
## 12. Tiering y periodicidad declarados (y base de su determinación)
## 13. Observaciones abiertas del ciclo anterior
| Observación | Estado | Evidencia de cierre |
## 14. Completitud + consultas abiertas numeradas
## 15. Guion de la infografía (una página)
## 16. Brechas de evidencia
| Ítem esperado | Estado (ausente/parcial) | Evidencia faltante | Documento que debía contenerla | Impacto |
**Solicitud de re-entrega:** ...
## 17. Anexo de trazabilidad (documentos leídos con SHA-256; esperados y no recibidos)
```

Ninguna sección puede faltar. Sin evidencia: "No evidenciado". Sección 9/10 sin hallazgos: "Sin discrepancias identificadas".

## Estado de admisibilidad (sección 8 y portada)

Exactamente uno:

| Estado | Evidencia que lo sustenta | Efecto |
|---|---|---|
| Python que corre sin errores | log de ejecución + hash de insumo + output | A8 puede iniciar |
| Python con errores | traza del error | A8 en precondición no satisfecha |
| Excel con .md generado (A2) | A2_reconciliacion.md con 100 % reconciliado | A8 trabaja sobre notebook de A2 |
| Excel sin .md | libro sin traducción | A8 bloqueado hasta A2 |
| No entregada | — | hallazgo C4 desde el Paso 0 |

Si el código corre pero su output no coincide con el publicado: declararlo aquí ("corre, output no coincide: dif X") — condiciona A8 y A10.

## Cálculo de completitud

Campos evaluables = todas las celdas de las tablas de secciones 0, 2, 4, 6, 12 + cada eslabón de la sección 3 + cada control de la sección 11. Completitud = evidenciados / evaluables. Muestra el cálculo (N/M).

```bash
python scripts/verificar_paso0.py A4_paso0.md
```

Revisa que estén las 18 secciones (0–17), cuenta "No evidenciado", calcula la completitud sobre tablas y verifica que la primera línea tenga el rótulo si < 80 %.

## Guion de la infografía (sección 15)

Cinco bloques, cada uno con su número de cita al pie:

| Bloque | Contenido | Regla |
|---|---|---|
| (a) Cadena del modelo | 5–7 cajas: input → transformación → cálculo → calibración → output → publicación → decisión | eslabón roto en rojo con "No evidenciado" |
| (b) Tiering y periodicidad | tier, periodicidad, fecha de última validación | |
| (c) Outputs y destinatarios | output → área → foro | |
| (d) Semáforo de observaciones previas | abiertas/cerradas/vencidas | solo si hay informe anterior |
| (e) Pie de fuentes | [1]…[n] | cada número = una cita de este documento |

Regla de cierre: recorre cada elemento gráfico y confirma que está en el documento. Un dato que solo está en la infografía es un defecto.

## Prohibido

Infografía sin documento; declaraciones verbales como hechos; adjetivos evaluativos sin cifra; abreviar por longitud; condicionar la entrega a recibir más archivos.
