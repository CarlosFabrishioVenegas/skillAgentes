---
name: virf-a5-matriz-documental
description: Construcción de la matriz de completitud documental del Control 1 - una fila por actividad VIRF de Documentación aplicable al tier, evaluación separada de completitud, vigencia y coherencia, contraste de la versión documentada con la productiva del acta y del código, cálculo de cobertura, rúbrica de estados y formato de salida con ID de actividad. Úsala en el Paso 10 (agente A5).
---

# A5 · Matriz documental del Control 1

Pregunta rectora: **¿todo componente del modelo en producción tiene contrapartida documental vigente, versionada y coherente?**

## 1. Filas = actividades del estándar

Obtén la lista con `virf-a4-mapa-evidencia-estandar/scripts/filtrar_estandar_virf.py --tier <t>` y filtra `control == C1`. Ese número de actividades es el número de filas. No agregues ni quites; no consolides varias actividades en una fila.

## 2. Tres atributos, evaluados por separado

| Atributo | Pregunta | Falla típica |
|---|---|---|
| COMPLETITUD | ¿El contenido que pide la actividad existe? | Sección ausente, "por definir", anexo no entregado |
| VIGENCIA | ¿Corresponde a la versión productiva? | Manual de v3.0 con producción en v3.2; sin fecha ni versión |
| COHERENCIA | ¿No contradice al acta, al código ni a otros manuales? | Ventana 12 m en manual vs 18 m en acta |

Registra los tres en la evaluación sustentada: `Completitud: sí (cita) · Vigencia: no (versión 3.0 vs productiva 3.2) · Coherencia: n/a`.

## 3. Versión documentada vs productiva

Contrasta con: acta (versión productiva declarada) y código (tag/CHANGELOG/fecha de pase). **Documentación de otra versión = No cumple**, aunque sea de mejor calidad.

## 4. Rúbrica de estados

| Estado | Cuándo |
|---|---|
| Cumple | Cubierta por documento vigente, versionado, coherente con código y acta, citable con sección y página |
| Cumple con observación | Contenido presente con defecto formal: sin versión/fecha (solo Tier 3), documento no formal (PPT), referencia rota, captura de pantalla como única evidencia |
| No cumple | Contenido ausente cuando el estándar lo exige; documentación de versión distinta a la productiva; sin fecha ni versión en Tier 1–2 |
| No verificable | Documento existe pero no se entregó, es confidencial no entregado, o ilegible/no editable |
| No evidenciado | Ningún documento aborda la actividad |
| No aplica | Solo con cita de la regla del estándar que exime |

## 5. Formato de salida

```markdown
# Control 1 · Documentación — <Modelo> (<Código>) · Tier <t>
**Cobertura:** X de N actividades evidenciadas (Y %) · **Semáforo:** <verde/ámbar/rojo/gris>
<!-- si cobertura parcial por pedido del validador: "Cobertura parcial: evaluadas M de N (Z %)" -->

| ID VIRF | Actividad esperada | Documento que la cubre | Estado | Sustento del estado | Fuente exacta | Acción pendiente |
|---|---|---|---|---|---|---|

## Hallazgos (ordenados por severidad)
## Referencias cruzadas (C4 Implementación, C5 Gobierno)
## Consultas abiertas (para emitir vía A9)
## Brechas de evidencia
```

Semáforo: verde solo con 100 % de cobertura y sin "No cumple"; con cobertura < 100 % nunca es satisfactorio.

## Ejemplo de sustento correcto

"La ventana de desempeño está definida como 12 meses en el manual (Manual_PD.pdf > 3.4 > p.15), mientras el acta declara 18 meses para la versión productiva (Acta_MOD-0412.docx > Ventana de desempeño > p.2); ambas cifras coexisten sin nota de conciliación, por lo que no es posible acreditar qué documenta la producción."

## Interacción

- "El equipo lo explicó en la reunión" → la explicación verbal no es documentación; ofrecer registrarla como consulta abierta.
- Prohibido: "documentación adecuada", "suficientemente detallada" sin evidencia en la misma fila; cerrar observación previa por declaración del equipo.
