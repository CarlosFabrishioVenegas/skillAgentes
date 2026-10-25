---
name: virf-aim-motor-what-if
description: Motor what-if reutilizable que cuantifica en la moneda del modelo el impacto de cada hallazgo de calidad de datos - escenario base vs escenario corregido, diferencia absoluta y relativa, agregación por control y total, rango de sensibilidad bajo, central y alto - reutilizando primero el Excel o .py de impactos del equipo y escribiendo 03_Impactos.xlsx. Úsala en el Paso 8 (AIM) para construir Motor_Impactos.py.
---

# AIM · Motor what-if

## 1. Primero el material del equipo

1. ¿Entregaron Excel/código de impactos? → verificar que corre (o que el Excel reconcilia), citar origen y **usar su función de magnitud**.
2. Si no corre: reportarlo en brechas y construir la función mínima con el canal del skill `virf-aim-canales-impacto`, rotulada "construida por el validador".

Nunca omitas la reutilización cuando el material existe.

## 2. Uso del motor

```python
from motor_impactos import MotorImpactos, ecl_simple

M = MotorImpactos(modelo="PD Retail", codigo="MOD-0412", moneda="PEN", base=base,
                  magnitud=lambda d: ecl_simple(d, pd_col="pd_12m", lgd_col="lgd", ead_col="ead"),
                  nombre_magnitud="ECL 12m", origen_magnitud="Excel_Impactos_equipo.xlsx > Calculo > F2:F9000")

M.supuesto("lgd_sin_garantia", 0.45, fuente="Manual LGD > 3.2 > p.14")
M.supuesto("tasa_impositiva", 0.295, fuente="[SUPUESTO] no está en el expediente")

# Escenario = transformación que corrige el defecto, con variantes de sensibilidad
M.escenario(id="IMP-01", hallazgo="H-03 colateral faltante", control="C2",
            canal="LGD sin colateral → con colateral",
            central=lambda d: d.assign(lgd=d.lgd.where(d.colateral.notna(), M.s("lgd_sin_garantia"))),
            bajo=lambda d: d.assign(lgd=d.lgd.where(d.colateral.notna(), 0.35)),
            alto=lambda d: d.assign(lgd=d.lgd.where(d.colateral.notna(), 0.60)),
            nota_sensibilidad="LGD 35 %/45 %/60 %: rango de la política de LGD (cita)")

M.ejecutar()
M.escribir_excel("salida/03_Impactos.xlsx")
```

## 3. Qué produce 03_Impactos.xlsx

| Hoja | Contenido |
|---|---|
| `Resumen` | por escenario: hallazgo, control, canal, magnitud base, magnitud corregida (central), Δ absoluto, Δ %, Δ bajo, Δ alto |
| `PorControl` | agregación por control C1–C6 |
| `Total` | suma de Δ (con advertencia: los escenarios pueden solaparse; ver abajo) y escenario conjunto si se definió |
| `Supuestos` | nombre, valor, fuente, `[SUPUESTO]` sí/no |
| `Reproducibilidad` | hash base, fecha, versiones, semilla |

## 4. Agregación: evitar doble conteo

Los Δ individuales no son aditivos si dos hallazgos tocan las mismas operaciones. Por eso:
- Reporta la suma simple como "cota referencial".
- Si hay solapamiento, define un escenario **conjunto** (`M.escenario_conjunto([...])`) que aplique todas las correcciones a la vez; ese es el total válido.

## 5. Signo y lectura

Δ = magnitud corregida − magnitud base. Positivo = el defecto **subestima** la magnitud (p. ej. provisión insuficiente). Escríbelo así en el resumen: "El defecto subestima la ECL en S/ 1,24 MM (rango 0,98–1,61 MM)".

## Prohibido

Inventar tasas o factores sin marcarlos; concluir cumplimiento; re-ejecutar los controles de datos; entregar cifras sin supuesto y fuente.
