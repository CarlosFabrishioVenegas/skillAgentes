---
name: virf-ad-protocolo-rondas
description: Protocolo de autodiagnóstico iterativo por rondas - encabezado ESTADO ITERAR o COMPLETO, libro de lo que ya sé y lo que aún no sé, nomenclatura 00x/01x/02x, criterio de parada autodeclarado (sin incógnitas materiales, rendimientos decrecientes o tope de 5 rondas) y plantillas de Diagnostico_rN.md y Diagnostico_Final.md. Úsala en el Paso 3 (agente AD) en cada invocación.
---

# AD · Protocolo de rondas

AD instrumenta el modelo; no lo juzga. Cada invocación es una ronda. El humano ejecuta los notebooks y devuelve los Excel de resumen.

## 1. Determinar la ronda

| Situación al invocar | Acción |
|---|---|
| No hay `*_resumen.xlsx` adjuntos | Ronda 1 → generar `00a_…`, `00b_…` |
| Hay resúmenes de la ronda N | Leerlos, actualizar el libro de conocimiento, decidir ITERAR o COMPLETO |
| Faltan resúmenes de algún notebook de la ronda N | No avanzar esa pregunta: listar el notebook pendiente y pedirlo; las demás preguntas sí avanzan |

Nomenclatura: ronda 1 → prefijo `00`, ronda 2 → `01`, ronda 3 → `02`… Cada notebook: `<prefijo><letra>_Diagnostico_<tema>.ipynb` y su resumen `<prefijo><letra>_resumen.xlsx`.

## 2. Encabezado obligatorio de cada respuesta

```markdown
ESTADO: ITERAR (ronda 2)          | o |  ESTADO: COMPLETO (tras ronda 3)

### Lo que ya sé
| # | Hecho | Fuente (resumen > hoja > celda) | Pregunta que responde |
|---|---|---|---|
| H1 | La base tiene 1 284 330 filas y llave (cod_cliente, periodo) única | 00a_resumen.xlsx > Esquema > B3 | Q1 |

### Lo que aún no sé
| # | Pregunta | Por qué es material | Control que la necesita | Notebook de esta ronda |
|---|---|---|---|---|
| Q4 | ¿Hay saldos que reaparecen tras cancelación? | Afecta EAD y provisión | C2, C4 | 01a_Diagnostico_ciclo_vida |
```

## 3. Qué preguntas son materiales

Material = su respuesta cambia lo que un control C1–C6 concluiría o cómo debe ejecutarse. Ejemplos:

- Esquema real (columnas, tipos, llave, granularidad, cobertura temporal) → siempre material en ronda 1.
- Población: ¿coincide con la declarada en el manual? (conteos por periodo, segmento).
- Variables del modelo: ¿existen todas en la base con el nombre del código? ¿nulos, rangos?
- Output: ¿el código reproduce el output publicado? (conteo y suma de control).
- Ciclo de vida: saldos, estados, transiciones (crédito); posiciones, precios (mercado).

No material: curiosidades estadísticas que no mueven ningún control, gráficos decorativos, refinamientos de un hecho ya establecido.

## 4. Criterio de parada (justificar siempre)

Cerrar con `ESTADO: COMPLETO` cuando se cumple una de:
1. **Condición principal:** puedes describir los datos de extremo a extremo (origen → transformación → output) para los seis controles sin incógnitas materiales.
2. **Rendimientos decrecientes:** la última ronda no aportó ningún hecho material nuevo.
3. **Salvaguarda:** se completó la ronda 5.

En los casos 2 y 3, las incógnitas que quedan van a `## Brechas de evidencia` del Diagnostico_Final.md.

Nunca cerrar con una pregunta material abierta salvo por 2 o 3 (y entonces declararla). Nunca iterar "por si acaso".

## 5. Plantilla Diagnostico_rN.md

```markdown
# Diagnóstico ronda N — <modelo> (<código>)
ESTADO: ITERAR (ronda N)
## Lo que ya sé (acumulado)
## Lo que aún no sé
## Notebooks de esta ronda
| Notebook | Pregunta(s) | Qué escribe en el resumen | Cómo ejecutarlo |
## Justificación de seguir iterando
```

## 6. Plantilla Diagnostico_Final.md (insumo de A4)

```markdown
# Diagnóstico final — <modelo> (<código>)
ESTADO: COMPLETO (tras ronda N) — motivo de cierre: <principal | rendimientos decrecientes | tope 5 rondas>
## 1. Esquema real de los datos (por tabla)
## 2. Población y cobertura temporal
## 3. Variables del modelo: presencia, nulos, rangos
## 4. Reproducción del output (conteos y sumas de control)
## 5. Comportamiento de ciclo de vida
## 6. Hechos relevantes por control (C1–C6)
## 7. Índice de resúmenes (archivo · hoja · SHA-256)
## Brechas de evidencia
```

Al cerrar, consolida los resúmenes de todas las rondas en `00_Diagnostico.xlsx` (una hoja por notebook + hoja `Indice`).
