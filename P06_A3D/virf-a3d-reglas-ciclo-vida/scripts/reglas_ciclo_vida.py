"""Reglas de ciclo de vida del dato para bases en panel (A3D · VIRF).

Todas las funciones son deterministas, no modifican el DataFrame de entrada
y devuelven un dict estándar con n_evaluado, n_infractor, pct, muestra_llaves.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

MUESTRA = 10


def _exigir(df, cols):
    falt = [c for c in cols if c and c not in df.columns]
    if falt:
        raise KeyError(f"Columnas no existen en la base: {falt}")


def _res(regla, n_eval, mask_inf, llaves, detalle=""):
    n_inf = int(mask_inf.sum())
    muestra = llaves[mask_inf].astype(str).drop_duplicates().head(MUESTRA).tolist() if n_inf else []
    return {"regla": regla, "n_evaluado": int(n_eval), "n_infractor": n_inf,
            "pct": round(100 * n_inf / n_eval, 6) if n_eval else 0.0, "muestra_llaves": muestra, "detalle": detalle}


def a_fecha(s):
    """Convierte a fecha detectando formato ISO (AAAA-MM-DD) vs día primero (DD/MM/AAAA)."""
    txt = s.astype(str).str.strip()
    iso = txt.str.match(r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}").mean() > 0.5
    return pd.to_datetime(txt, errors="coerce", dayfirst=not iso, format="mixed")


def _ordenar(df, id_, fecha):
    d = df.copy()
    d["_f"] = a_fecha(d[fecha])
    return d.sort_values([id_, "_f"], kind="mergesort")


def saldo_resucita(df, id_, fecha, saldo):
    _exigir(df, [id_, fecha, saldo])
    d = _ordenar(df, id_, fecha)
    s = pd.to_numeric(d[saldo], errors="coerce")
    prev = s.groupby(d[id_]).shift(1)
    inf = (prev.fillna(np.nan) <= 0) & (s > 0)
    llaves = d[id_].astype(str) + "@" + d[fecha].astype(str)
    return _res("Saldo que resucita tras llegar a 0", prev.notna().sum(), inf, llaves)


def amortizacion_monotona(df, id_, fecha, saldo, desembolso=None, tolerancia=0.0):
    _exigir(df, [id_, fecha, saldo, desembolso])
    d = _ordenar(df, id_, fecha)
    s = pd.to_numeric(d[saldo], errors="coerce")
    diff = s.groupby(d[id_]).diff()
    inf = diff > tolerancia
    if desembolso:
        inf &= ~(pd.to_numeric(d[desembolso], errors="coerce").fillna(0) > 0)
    llaves = d[id_].astype(str) + "@" + d[fecha].astype(str)
    return _res("Saldo aumenta sin desembolso (amortización no monótona)", diff.notna().sum(), inf, llaves,
                f"tolerancia={tolerancia}")


def unicidad_eventos(df, llave_evento):
    _exigir(df, llave_evento)
    inf = df.duplicated(subset=llave_evento, keep=False)
    llaves = df[llave_evento].astype(str).agg("|".join, axis=1)
    return _res(f"Unicidad de evento por {llave_evento}", len(df), inf, llaves,
                f"grupos duplicados={int(df[inf].groupby(llave_evento).ngroups) if inf.any() else 0}")


def transiciones_invalidas(df, id_, fecha, estado, permitidas):
    _exigir(df, [id_, fecha, estado])
    d = _ordenar(df, id_, fecha)
    e = d[estado].astype(str)
    prev = e.groupby(d[id_]).shift(1)
    pares = list(zip(prev, e))
    inf = pd.Series([p == p and p is not None and (p, a) not in permitidas for p, a in pares], index=d.index)
    llaves = d[id_].astype(str) + "@" + d[fecha].astype(str) + ":" + prev.astype(str) + "->" + e
    conteo = pd.Series([f"{p}->{a}" for p, a in pares], index=d.index)[inf].value_counts().head(10).to_dict()
    return _res("Transición de estado no permitida", prev.notna().sum(), inf, llaves, f"top={conteo}")


def continuidad_temporal(df, id_, fecha, freq="M"):
    _exigir(df, [id_, fecha])
    d = _ordenar(df, id_, fecha)
    p = d["_f"].dt.to_period(freq)
    salto = p.groupby(d[id_]).diff().apply(lambda x: x.n if pd.notna(x) else 1)
    inf = salto > 1
    llaves = d[id_].astype(str) + "@" + d[fecha].astype(str)
    return _res("Periodos intermedios faltantes en operación viva", len(d), inf, llaves)


def coherencia_campos(df, expr, descripcion):
    ok = df.eval(expr)
    inf = ~ok.fillna(False).astype(bool)
    llaves = df.index.to_series().astype(str)
    return _res(f"Coherencia: {descripcion}", len(df), inf, llaves, f"expr: {expr}")


def signos_rangos(df, col, minimo=None, maximo=None):
    _exigir(df, [col])
    s = pd.to_numeric(df[col], errors="coerce")
    inf = pd.Series(False, index=df.index)
    if minimo is not None:
        inf |= s < minimo
    if maximo is not None:
        inf |= s > maximo
    return _res(f"Rango de {col} en [{minimo}, {maximo}]", int(s.notna().sum()), inf & s.notna(),
                df.index.to_series().astype(str))


def orden_fechas(df, cols):
    _exigir(df, cols)
    f = [a_fecha(df[c]) for c in cols]
    inf = pd.Series(False, index=df.index)
    for a, b in zip(f, f[1:]):
        inf |= (a > b) & a.notna() & b.notna()
    return _res(f"Orden de fechas {' <= '.join(cols)}", len(df), inf, df.index.to_series().astype(str))
