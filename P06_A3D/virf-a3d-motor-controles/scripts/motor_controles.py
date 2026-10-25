"""Motor de la batería de controles de calidad de datos (A3D · VIRF).

Ver SKILL.md para el uso. No modifica la base de entrada.
"""
from __future__ import annotations

import hashlib
import platform
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Optional

import pandas as pd

BLOQUES = {1: "Controles del equipo", 2: "Batería del validador", 3: "Controles adicionales"}


@dataclass
class Umbral:
    valor: Optional[float]          # fracción máxima de infractores (0.05 = 5 %); 0 = ninguno
    origen: Optional[str]           # cita; None o '[SUPUESTO]...' => no declarado por el banco

    @property
    def declarado(self):
        return self.origen is not None and not str(self.origen).startswith("[SUPUESTO]")


def umbral(valor, origen):
    return Umbral(valor, origen)


@dataclass
class Control:
    bloque: int
    id: str
    dimension: str
    regla: str
    fuente_regla: str
    umbral: Umbral
    infractores: Optional[Callable] = None
    columnas: list = field(default_factory=list)
    resultado_previo: Optional[dict] = None
    salida: dict = field(default_factory=dict)


class Bateria:
    def __init__(self, modelo, codigo, base: pd.DataFrame, llave, semilla=20261017):
        if base is None or len(base) == 0:
            raise ValueError("Insumo vacío: la base no tiene registros. No se produce resultado silencioso.")
        self.modelo, self.codigo, self.base, self.llave, self.semilla = modelo, codigo, base, llave, semilla
        self.controles: list[Control] = []
        self.brechas: list[dict] = []
        self.hash_base = hashlib.sha256(pd.util.hash_pandas_object(base, index=True).values.tobytes()).hexdigest()

    # --- registro -------------------------------------------------------
    def control(self, bloque, id, dimension, regla, fuente_regla, umbral, infractores, columnas=()):
        self.controles.append(Control(bloque, id, dimension, regla, fuente_regla, umbral, infractores, list(columnas)))

    def desde_regla(self, bloque, id, dimension, resultado, fuente_regla, umbral):
        """Registra el dict devuelto por reglas_ciclo_vida.* como control."""
        self.controles.append(Control(bloque, id, dimension, resultado["regla"], fuente_regla, umbral,
                                      resultado_previo=resultado))

    def control_no_existe(self, bloque, id, dimension, regla, fuente):
        c = Control(bloque, id, dimension, regla, fuente, Umbral(None, None))
        c.salida = {"n_evaluado": 0, "n_infractor": 0, "n_conforme": 0, "pct": None,
                    "estado_tecnico": "No existe según evidencia", "muestra_llaves": ""}
        self.controles.append(c)

    def brecha(self, item, evidencia_faltante, impacto):
        self.brechas.append({"item": item, "evidencia_faltante": evidencia_faltante, "impacto": impacto})

    # --- ejecución ------------------------------------------------------
    def ejecutar(self):
        llaves = self.base[self.llave].astype(str).agg("|".join, axis=1) if self.llave else self.base.index.astype(str)
        for c in self.controles:
            if c.salida:
                continue
            try:
                if c.resultado_previo is not None:
                    r = c.resultado_previo
                    n_ev, n_inf, muestra = r["n_evaluado"], r["n_infractor"], r["muestra_llaves"]
                else:
                    falt = [x for x in c.columnas if x not in self.base.columns]
                    if falt:
                        c.salida = {"n_evaluado": 0, "n_infractor": 0, "n_conforme": 0, "pct": None,
                                    "estado_tecnico": f"No verificable — columna inexistente: {falt}", "muestra_llaves": ""}
                        continue
                    m = pd.Series(c.infractores(self.base), index=self.base.index).fillna(False).astype(bool)
                    n_ev, n_inf = len(m), int(m.sum())
                    muestra = llaves[m].sort_values(kind="mergesort").head(10).tolist()
                pct = n_inf / n_ev if n_ev else 0.0
                if not c.umbral.declarado or c.umbral.valor is None:
                    est = "No verificable — umbral no declarado"
                else:
                    est = "Dentro de umbral" if pct <= c.umbral.valor else "Fuera de umbral"
                c.salida = {"n_evaluado": n_ev, "n_infractor": n_inf, "n_conforme": n_ev - n_inf,
                            "pct": round(100 * pct, 6), "estado_tecnico": est, "muestra_llaves": "; ".join(map(str, muestra))}
            except Exception as e:  # el error se reporta, no se oculta
                c.salida = {"n_evaluado": 0, "n_infractor": 0, "n_conforme": 0, "pct": None,
                            "estado_tecnico": f"Error de ejecución — {e!r}"[:250], "muestra_llaves": ""}
        return self

    def autocomprobar(self):
        filas = []
        for c in self.controles:
            s = c.salida
            ok = s["n_infractor"] + s["n_conforme"] == s["n_evaluado"]
            filas.append({"id": c.id, "evaluados": s["n_evaluado"], "infractores_mas_conformes": s["n_infractor"] + s["n_conforme"], "cuadra": ok})
        self._auto = pd.DataFrame(filas)
        if not self._auto["cuadra"].all():
            raise AssertionError(f"Descuadre de conteos en: {self._auto.loc[~self._auto.cuadra, 'id'].tolist()}")
        return self._auto

    # --- salidas --------------------------------------------------------
    def tabla(self):
        return pd.DataFrame([{
            "bloque": f"{c.bloque} · {BLOQUES[c.bloque]}", "id": c.id, "dimension": c.dimension, "regla": c.regla,
            "fuente_regla": c.fuente_regla, "columnas": ", ".join(c.columnas),
            **{k: c.salida.get(k) for k in ("n_evaluado", "n_infractor", "n_conforme", "pct")},
            "umbral_pct": None if c.umbral.valor is None else 100 * c.umbral.valor,
            "origen_umbral": c.umbral.origen or "[SUPUESTO] no declarado",
            "estado_tecnico": c.salida.get("estado_tecnico"), "muestra_llaves": c.salida.get("muestra_llaves"),
        } for c in self.controles])

    def escribir_excel(self, ruta):
        t = self.tabla()
        if 1 not in {c.bloque for c in self.controles}:
            self.brecha("Controles del equipo (bloque 1)", "Documento y/o código de controles del equipo", "No se puede evaluar el marco de control existente (C2)")
        repro = pd.DataFrame([{"modelo": self.modelo, "codigo": self.codigo, "fecha": datetime.now().isoformat(timespec="seconds"),
                               "hash_base": self.hash_base, "filas_base": len(self.base), "python": platform.python_version(),
                               "pandas": pd.__version__, "semilla": self.semilla,
                               **{f"n_bloque_{b}": int((t.bloque.str.startswith(str(b))).sum()) for b in BLOQUES}}])
        with pd.ExcelWriter(ruta) as xw:
            t.to_excel(xw, sheet_name="Resumen", index=False)
            t[t.n_infractor.fillna(0) > 0][["id", "regla", "muestra_llaves"]].to_excel(xw, sheet_name="Muestras", index=False)
            repro.to_excel(xw, sheet_name="Reproducibilidad", index=False)
            getattr(self, "_auto", self.autocomprobar()).to_excel(xw, sheet_name="Autocomprobacion", index=False)
            pd.DataFrame(self.brechas or [{"item": "Sin brechas identificadas"}]).to_excel(xw, sheet_name="Brechas", index=False)
        return ruta

    def escribir_hallazgos_md(self, ruta):
        t = self.tabla()
        lin = [f"# A3 · Hallazgos de la batería — {self.modelo} ({self.codigo})", "",
               f"Controles ejecutados: {len(t)} · Fuera de umbral: {(t.estado_tecnico == 'Fuera de umbral').sum()} · "
               f"No verificables: {t.estado_tecnico.str.startswith('No verificable').sum()} · Dentro de umbral: {(t.estado_tecnico == 'Dentro de umbral').sum()}",
               "", "| Bloque | ID | Dimensión | Regla | Evaluados | Infractores | % | Umbral (origen) | Estado técnico | Muestra |",
               "|---|---|---|---|---|---|---|---|---|---|"]
        for _, r in t.iterrows():
            lin.append(f"| {r.bloque} | {r.id} | {r.dimension} | {r.regla} | {r.n_evaluado} | {r.n_infractor} | {r.pct} | "
                       f"{r.umbral_pct} ({r.origen_umbral}) | {r.estado_tecnico} | {str(r.muestra_llaves)[:80]} |")
        lin += ["", "## Brechas de evidencia", "| Ítem | Evidencia faltante | Impacto |", "|---|---|---|"]
        lin += [f"| {b['item']} | {b['evidencia_faltante']} | {b['impacto']} |" for b in self.brechas] or ["| Sin brechas identificadas | | |"]
        open(ruta, "w", encoding="utf-8").write("\n".join(lin) + "\n")
        return ruta
