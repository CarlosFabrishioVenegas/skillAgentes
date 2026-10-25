#!/usr/bin/env python3
"""Compara output publicado vs reproducido por llave y columnas (A8 · VIRF).

Uso:
    python reproducir_output.py --publicado pub.xlsx --reproducido rep.csv --llave cod_cliente \
        --columnas pd_12m,segmento --tol-rel 1e-6 --salida reproduccion.md
"""
import argparse
import hashlib
import sys

import numpy as np
import pandas as pd


def leer(r):
    return pd.read_parquet(r) if r.endswith(".parquet") else pd.read_excel(r) if r.endswith((".xlsx", ".xls")) else pd.read_csv(r, sep=None, engine="python")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--publicado", required=True)
    ap.add_argument("--reproducido", required=True)
    ap.add_argument("--llave", required=True)
    ap.add_argument("--columnas", required=True)
    ap.add_argument("--tol-rel", type=float, default=1e-6)
    ap.add_argument("--salida", default="reproduccion.md")
    a = ap.parse_args()
    ll, cols = a.llave.split(","), a.columnas.split(",")
    P, R = leer(a.publicado), leer(a.reproducido)
    if P.empty or R.empty:
        sys.exit("Insumo vacío en publicado o reproducido.")
    for nombre, df in (("publicado", P), ("reproducido", R)):
        dup = df.duplicated(ll).sum()
        if dup:
            print(f"[AVISO] {dup} llaves duplicadas en {nombre}")
    M = P[ll + cols].merge(R[ll + cols], on=ll, how="outer", suffixes=("_pub", "_rep"), indicator=True)
    solo_pub, solo_rep = int((M._merge == "left_only").sum()), int((M._merge == "right_only").sum())
    B = M[M._merge == "both"]
    filas, ok = [], True
    for c in cols:
        p, r = B[f"{c}_pub"], B[f"{c}_rep"]
        if pd.api.types.is_numeric_dtype(p) and pd.api.types.is_numeric_dtype(r):
            da = (r - p).abs()
            dr = da / p.abs().clip(lower=1e-12)
            n_dif = int((dr > a.tol_rel).sum())
            filas.append([c, "numérica", len(B), n_dif, f"{da.max():.6g}", f"{dr.max():.2e}",
                          f"{P[c].sum():.6g} / {R[c].sum():.6g}", f"{P[c].mean():.6g} / {R[c].mean():.6g}"])
        else:
            n_dif = int((p.astype(str) != r.astype(str)).sum())
            filas.append([c, "categórica", len(B), n_dif, "", "", "", ""])
        ok &= n_dif == 0
    ok &= solo_pub == 0 and solo_rep == 0
    h = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()
    md = [f"## Reproducción de outputs (tolerancia relativa {a.tol_rel:g})", "",
          f"- Publicado: {a.publicado} (sha256 {h(a.publicado)[:16]}…) · filas {len(P)}",
          f"- Reproducido: {a.reproducido} (sha256 {h(a.reproducido)[:16]}…) · filas {len(R)}",
          f"- Llaves solo en publicado: {solo_pub} · solo en reproducido: {solo_rep}", "",
          "| Columna | Tipo | Filas comparadas | N° diferencias | Máx dif. abs | Máx dif. rel | Suma pub / rep | Media pub / rep |",
          "|---|---|---|---|---|---|---|---|"]
    md += ["| " + " | ".join(map(str, f)) + " |" for f in filas]
    md += ["", f"**Resultado:** {'Reproducido dentro de tolerancia' if ok else 'NO reproducido — investigar parámetros, ajustes manuales o pérdida de registros'}",
           "", "Completar los seis elementos: comando, fecha, versión del código, hash del insumo, valor obtenido, valor publicado."]
    open(a.salida, "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
