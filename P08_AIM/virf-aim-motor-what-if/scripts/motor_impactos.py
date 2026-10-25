"""Motor what-if de impactos monetarios (AIM · VIRF).

Cuantifica magnitud(base) vs magnitud(base corregida) por escenario, con rango de sensibilidad.
No modifica la base de entrada (cada escenario recibe una copia).
"""
from __future__ import annotations

import hashlib
import platform
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Optional

import pandas as pd


def ecl_simple(d: pd.DataFrame, pd_col="pd", lgd_col="lgd", ead_col="ead") -> float:
    """ECL 12m = Σ PD × LGD × EAD (forma general; usar la del equipo si existe)."""
    return float((d[pd_col].astype(float) * d[lgd_col].astype(float) * d[ead_col].astype(float)).sum())


@dataclass
class Escenario:
    id: str
    hallazgo: str
    control: str
    canal: str
    central: Callable
    bajo: Optional[Callable] = None
    alto: Optional[Callable] = None
    nota_sensibilidad: str = ""


class MotorImpactos:
    def __init__(self, modelo, codigo, moneda, base, magnitud: Callable, nombre_magnitud, origen_magnitud, semilla=20261017):
        if base is None or len(base) == 0:
            raise ValueError("Insumo vacío: no hay base sobre la cual cuantificar impactos.")
        self.modelo, self.codigo, self.moneda = modelo, codigo, moneda
        self.base, self.magnitud = base, magnitud
        self.nombre_magnitud, self.origen_magnitud, self.semilla = nombre_magnitud, origen_magnitud, semilla
        self.supuestos: dict[str, dict] = {}
        self.escenarios: list[Escenario] = []
        self.conjuntos: list[tuple[str, list[str]]] = []
        self.resultados = None

    def supuesto(self, nombre, valor, fuente):
        self.supuestos[nombre] = {"valor": valor, "fuente": fuente,
                                  "es_supuesto": (fuente is None) or str(fuente).startswith("[SUPUESTO]")}

    def s(self, nombre):
        if nombre not in self.supuestos:
            raise KeyError(f"Supuesto no declarado: {nombre}. Declararlo con su fuente antes de usarlo.")
        return self.supuestos[nombre]["valor"]

    def escenario(self, **kw):
        self.escenarios.append(Escenario(**kw))

    def escenario_conjunto(self, id, ids):
        self.conjuntos.append((id, ids))

    def _eval(self, f):
        if f is None:
            return None
        return self.magnitud(f(self.base.copy()))

    def ejecutar(self):
        base_val = self.magnitud(self.base.copy())
        filas = []
        for e in self.escenarios:
            c, b, a = self._eval(e.central), self._eval(e.bajo), self._eval(e.alto)
            filas.append({"id": e.id, "hallazgo": e.hallazgo, "control": e.control, "canal": e.canal,
                          f"{self.nombre_magnitud} base": base_val, f"{self.nombre_magnitud} corregida": c,
                          "delta": c - base_val, "delta_pct": 100 * (c - base_val) / base_val if base_val else None,
                          "delta_bajo": None if b is None else b - base_val, "delta_alto": None if a is None else a - base_val,
                          "lectura": ("el defecto subestima" if c > base_val else "el defecto sobreestima" if c < base_val else "sin efecto"),
                          "nota_sensibilidad": e.nota_sensibilidad})
        for cid, ids in self.conjuntos:
            fs = [e.central for e in self.escenarios if e.id in ids]
            def comp(d, fs=fs):
                for f in fs:
                    d = f(d)
                return d
            c = self._eval(comp)
            filas.append({"id": cid, "hallazgo": "Escenario conjunto: " + ", ".join(ids), "control": "Total",
                          "canal": "Correcciones simultáneas", f"{self.nombre_magnitud} base": base_val,
                          f"{self.nombre_magnitud} corregida": c, "delta": c - base_val,
                          "delta_pct": 100 * (c - base_val) / base_val if base_val else None,
                          "delta_bajo": None, "delta_alto": None, "lectura": "total válido (sin doble conteo)", "nota_sensibilidad": ""})
        self.resultados = pd.DataFrame(filas)
        self.base_val = base_val
        return self.resultados

    def escribir_excel(self, ruta):
        if self.resultados is None:
            self.ejecutar()
        r = self.resultados
        indiv = r[r.control != "Total"]
        por_control = indiv.groupby("control", as_index=False)[["delta", "delta_bajo", "delta_alto"]].sum(min_count=1)
        total = pd.DataFrame([{"concepto": "Suma simple de deltas (cota referencial; puede haber doble conteo)", "delta": indiv.delta.sum()}]
                             + [{"concepto": f"{x.hallazgo}", "delta": x.delta} for x in r[r.control == "Total"].itertuples()])
        sup = pd.DataFrame([{"supuesto": k, **v} for k, v in self.supuestos.items()] or [{"supuesto": "(ninguno)"}])
        repro = pd.DataFrame([{"modelo": self.modelo, "codigo": self.codigo, "moneda": self.moneda,
                               "magnitud": self.nombre_magnitud, "origen_magnitud": self.origen_magnitud,
                               "hash_base": hashlib.sha256(pd.util.hash_pandas_object(self.base, index=True).values.tobytes()).hexdigest(),
                               "fecha": datetime.now().isoformat(timespec="seconds"), "python": platform.python_version(),
                               "pandas": pd.__version__, "semilla": self.semilla}])
        with pd.ExcelWriter(ruta) as xw:
            r.to_excel(xw, sheet_name="Resumen", index=False)
            por_control.to_excel(xw, sheet_name="PorControl", index=False)
            total.to_excel(xw, sheet_name="Total", index=False)
            sup.to_excel(xw, sheet_name="Supuestos", index=False)
            repro.to_excel(xw, sheet_name="Reproducibilidad", index=False)
        return ruta
