---
name: virf-a4-cadena-doble-cita
description: Construcción de la cadena del modelo end-to-end (input, transformación, cálculo, calibración, output, publicación, decisión de negocio) con doble cita documental y de código por eslabón, reconciliación previa de todas las fuentes (manual, acta, código, minutas) y tabla de discrepancias documentación-código con impacto y control afectado. Úsala en el Paso 4 (A4) para las secciones 3, 5, 9 y 10 del Paso 0.
---

# A4 · Cadena del modelo con doble cita

## 1. Reconciliar antes de escribir

Construye primero una matriz de hechos por fuente. No escribas la cadena hasta tenerla.

| Hecho | Manual (cita) | Acta (cita) | Código (cita) | Minuta/reunión (cita) | ¿Coinciden? |
|---|---|---|---|---|---|
| Versión productiva | v3.1 (Manual > portada > p.1) | v3.2 (Acta > Versión > p.1) | tag v3.2 (repo > CHANGELOG > línea 4) | — | No → consulta |
| Ventana de desempeño | 12 m (Manual > 3.4 > p.15) | 18 m (Acta > Ventana de desempeño > p.2) | 12 (target.py > construir_target() > línea 33) | — | No → consulta |

Si no coinciden: se registra en sección 9 (entre fuentes) o 10 (doc ↔ código) y se genera consulta. **Nunca elijas en silencio.**

Declaración verbal sin documento: `Declaración verbal en reunión del <fecha>, sin sustento documental` → consulta, no hecho.

## 2. Plantilla de la cadena (sección 3)

```markdown
| # | Eslabón | Qué ocurre | Cita documental | Cita de código | Estado |
|---|---|---|---|---|---|
| 1 | Input | Extracción mensual de DM_CLIENTE y DM_OPERACION | Manual > 3.2 > p.19 | extraer.sql > línea 12 | Evidenciado |
| 2 | Transformación | Filtro de clientes con antigüedad ≥ 6 m; imputación de ingreso por mediana | Manual > 3.5 > p.22 | prep.py > limpiar() > línea 40–58 | Evidenciado |
| 3 | Cálculo | Score logístico con 11 variables | Manual > 4.1 > p.25 | score.py > puntuar() > línea 20 | Evidenciado |
| 4 | Calibración | Escalamiento a tasa central 3,10 % | Manual > 4.6 > p.31 | calib.py > escalar() > línea 9 | Evidenciado |
| 5 | Output | PD por cliente y segmento | Manual > 5 > p.35 | export.py > línea 70 | Evidenciado |
| 6 | Publicación | Tablero Riesgos + correo mensual | Manual usuario > 2 > p.4 | — | Parcial (sin código de publicación) |
| 7 | Decisión de negocio | Insumo de provisión IFRS 9 | Acta > G10 > p.2 | — | No evidenciado (sin evidencia de consumo) |
```

Cada eslabón: doble cita cuando exista. Eslabón sin evidencia: se muestra roto, no se omite.

## 3. Lógica de código (sección 5)

Por cada script/notebook:

```markdown
### prep.py
- Propósito: …
- Inputs: … (línea) · Outputs: … (línea)
- Parámetros implementados: corte_antiguedad=6 (línea 41), imputación mediana (línea 52)
- Contraste con manual: coincide / difiere (ver sección 10, fila N)
```

Usa `virf-a1-lectura-codigo-discrepancias/scripts/inventario_parametros_codigo.py` para no olvidar parámetros.

## 4. Tabla documentación ↔ código (sección 10)

| Elemento | Qué dice el manual (cita) | Qué hace el código (cita) | Impacto | Control afectado |
|---|---|---|---|---|
| Corte de score | 640 (Manual > 4.3 > p.27) | 620 (score.py > segmentar() > línea 88) | Reclasificación de segmento; cuantificar en A8 | C4, C1 |

Categorías a revisar siempre: cortes, pesos/coeficientes, umbrales, filtros de población, imputaciones, ventanas, factores de calibración, catálogos/mapeos, rutas de fuente.

"Impacto" en el Paso 0 es descriptivo (qué afectaría), no cuantificado: la cuantificación es de A8/AIM.

## 5. Casos borde que afectan la cadena

- Dos herramientas (desarrollo y producción): documentar ambas, declarar cuál se valida y con qué evidencia de que está en producción.
- Modelo que alimenta otro modelo: eslabón 7 apunta al código de inventario del modelo consumidor.
- Componente tercerizado (buró, motor externo): marcar frontera "caja negra contractual" en el eslabón.
- Cambio en el ciclo (recalibración, nuevas variables): anotar qué cambió y con qué aprobación; sin aprobación → hallazgo de gobierno señalable desde el Paso 0.
- Modelo heredado sin autor: "autoría no determinable con la evidencia entregada".
