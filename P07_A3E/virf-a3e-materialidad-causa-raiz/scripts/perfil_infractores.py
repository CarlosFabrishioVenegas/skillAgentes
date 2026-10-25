#!/usr/bin/env python3
"""Perfila registros infractores vs. conformes por dimensión (lift) para causa raíz (A3E · VIRF).

Uso:
    python perfil_infractores.py base.parquet --llave cod_operacion,fecha_corte \
        --infractores muestra.csv --dims fecha_corte,producto,sistema_origen [--saldo saldo_capital] --salida perfil.csv
o, si el infractor se define por expresión:
    python perfil_infractores.py base.csv --expr "ingreso_declarado.isna()" --dims ... --salida perfil.csv
"""
import argparse
import sys

import pandas as pd


def leer(r):
    return pd.read_parquet(r) if r.endswith(".parquet") else pd.read_excel(r) if r.endswith((".xlsx", ".xls")) else pd.read_csv(r, sep=None, engine="python")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("--llave", default=None)
    ap.add_argument("--infractores", default=None, help="CSV con columnas de la llave")
    ap.add_argument("--expr", default=None, help="expresión pandas evaluada con df.eval(engine='python')")
    ap.add_argument("--dims", required=True)
    ap.add_argument("--saldo", default=None)
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--salida", default="perfil_infractores.csv")
    a = ap.parse_args()
    df = leer(a.base)
    if df.empty:
        sys.exit("Insumo vacío.")
    if a.expr:
        m = pd.Series(df.eval(a.expr, engine="python"), index=df.index).fillna(False).astype(bool)
    else:
        ll = a.llave.split(",")
        inf = leer(a.infractores)[ll].astype(str).drop_duplicates()
        k = df[ll].astype(str).agg("|".join, axis=1)
        m = k.isin(inf.agg("|".join, axis=1))
    tasa_global = m.mean()
    if tasa_global == 0:
        sys.exit("No hay infractores en la base con la definición dada.")
    filas = []
    for d in a.dims.split(","):
        if d not in df.columns:
            print(f"[AVISO] dimensión {d} no existe", file=sys.stderr); continue
        g = df.assign(_inf=m).groupby(df[d].astype(str), dropna=False)
        t = g["_inf"].agg(["sum", "count", "mean"]).rename(columns={"sum": "n_infractor", "count": "n_total", "mean": "tasa"})
        t["lift"] = t["tasa"] / tasa_global
        t["pct_de_infractores"] = 100 * t["n_infractor"] / m.sum()
        if a.saldo and a.saldo in df.columns:
            sal = pd.to_numeric(df[a.saldo], errors="coerce")
            t["pct_saldo_infractor"] = 100 * sal[m].groupby(df.loc[m, d].astype(str)).sum() / sal.sum()
        t = t.sort_values(["pct_de_infractores", "lift"], ascending=False).head(a.top).reset_index().rename(columns={d: "categoria"})
        t.insert(0, "dimension", d)
        filas.append(t)
    out = pd.concat(filas, ignore_index=True)
    out.to_csv(a.salida, index=False)
    print(f"Tasa global de infractores: {100*tasa_global:.4f} % ({int(m.sum())} de {len(df)})")
    if a.saldo and a.saldo in df.columns:
        s = pd.to_numeric(df[a.saldo], errors="coerce")
        print(f"% de {a.saldo} afectado: {100*s[m].sum()/s.sum():.4f} %")
    print(out[out.lift >= 2].to_string(index=False) if (out.lift >= 2).any() else "Sin concentraciones con lift >= 2")


if __name__ == "__main__":
    main()
