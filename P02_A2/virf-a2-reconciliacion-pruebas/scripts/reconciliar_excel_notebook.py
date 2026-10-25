#!/usr/bin/env python3
"""Reconcilia salidas del notebook contra valores cacheados del Excel (A2 · VIRF).

Uso:
    python reconciliar_excel_notebook.py libro.xlsx salidas_notebook.csv --tol 1e-9 --salida A2_reconciliacion.md

salidas_notebook.csv: columnas hoja,celda,valor_notebook[,etiqueta]
"""
import argparse
import csv
import math
import sys

import openpyxl


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("libro")
    ap.add_argument("salidas_csv")
    ap.add_argument("--tol", type=float, default=1e-9)
    ap.add_argument("--salida", default="A2_reconciliacion.md")
    a = ap.parse_args()
    wb = openpyxl.load_workbook(a.libro, data_only=True, read_only=True)
    filas = list(csv.DictReader(open(a.salidas_csv, encoding="utf-8")))
    if not filas:
        sys.exit("ERROR: salidas_notebook.csv vacío; no hay nada que reconciliar.")
    res, n_ok = [], 0
    for r in filas:
        xl = wb[r["hoja"]][r["celda"]].value
        nb = r["valor_notebook"]
        x, n = num(xl), num(nb)
        if x is None or n is None:
            igual = str(xl).strip() == str(nb).strip()
            da = dr = ""
            estado = "Reconciliado (texto)" if igual else ("Sin valor cacheado en Excel" if xl is None else "No reconciliado (texto)")
        else:
            da = abs(n - x)
            dr = da / max(abs(x), 1e-12)
            igual = dr <= a.tol or (math.isnan(x) and math.isnan(n))
            estado = "Reconciliado" if igual else "No reconciliado"
        n_ok += estado.startswith("Reconciliado")
        res.append((r.get("etiqueta") or f"{r['hoja']}!{r['celda']}", xl, nb,
                    f"{da:.6g}" if da != "" else "", f"{dr:.1e}" if dr != "" else "", estado))
    md = [f"## Reconciliación Excel ↔ notebook (tolerancia relativa {a.tol:g})", "",
          f"Celdas reconciliadas: {n_ok}/{len(res)} ({100*n_ok/len(res):.1f} %)", "",
          "| Salida | Valor Excel | Valor notebook | Dif. absoluta | Dif. relativa | Estado |", "|---|---|---|---|---|---|"]
    md += [f"| {s} | {x} | {n} | {da} | {dr} | {e} |" for s, x, n, da, dr, e in res]
    if n_ok < len(res):
        md += ["", "> Existen celdas no reconciliadas: documentar causa por celda (redondeo, BUSCARV con duplicados, "
               "vacíos vs 0, fechas, filtros, valor cacheado desactualizado). Sin explicación: notebook no admisible."]
    open(a.salida, "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md[:3]))
    sys.exit(0 if n_ok == len(res) else 1)


if __name__ == "__main__":
    main()
