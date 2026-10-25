#!/usr/bin/env python3
"""Compara parámetros del manual contra el inventario de parámetros del código (A8 · VIRF).

Uso:
    python comparar_parametros.py parametros_manual.csv parametros_codigo.csv --salida paridad.md

parametros_manual.csv: parametro,valor_manual,cita_manual,patron_codigo
parametros_codigo.csv: salida de inventario_parametros_codigo.py
"""
import argparse
import re
import sys

import pandas as pd

RE_NUM = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w.])")


def nums(txt):
    return [float(x) for x in RE_NUM.findall(str(txt))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manual")
    ap.add_argument("codigo")
    ap.add_argument("--tol", type=float, default=1e-9)
    ap.add_argument("--salida", default="paridad.md")
    a = ap.parse_args()
    M = pd.read_csv(a.manual)
    C = pd.read_csv(a.codigo)
    if M.empty:
        sys.exit("parametros_manual.csv vacío.")
    filas = []
    for _, p in M.iterrows():
        pat = re.compile(str(p.patron_codigo), re.I)
        hits = C[C.detalle.astype(str).str.contains(pat)]
        vm = float(str(p.valor_manual).replace(",", "."))
        if hits.empty:
            filas.append([p.parametro, p.valor_manual, p.cita_manual, "—", "—", "No ubicado en código", "No evidenciado"])
            continue
        valores = {}
        for _, h in hits.iterrows():
            for v in nums(h.detalle):
                valores.setdefault(v, []).append(f"{h.archivo} > {h.funcion} > línea {h.linea}")
        # candidato: valor más cercano al del manual
        if not valores:
            filas.append([p.parametro, p.valor_manual, p.cita_manual, "(sin literal numérico)", "; ".join(hits.archivo + " > línea " + hits.linea.astype(str))[:150], "Revisar manualmente (valor externo o calculado)", "No verificable"])
            continue
        distintos = sorted(valores)
        coincide = any(abs(v - vm) <= a.tol * max(1, abs(vm)) for v in distintos)
        cerca = min(distintos, key=lambda v: abs(v - vm))
        estado = ("Coincide" if coincide and len(distintos) == 1 else
                  "Coincide (otros literales en la misma línea: revisar)" if coincide else "Difiere")
        if len({v for v in distintos if abs(v - cerca) < 1e-12}) and len(hits) > 1 and len(distintos) > 1 and not coincide:
            estado = "Múltiples valores en código"
        vc = ", ".join(f"{v:g}" for v in distintos[:6])
        ubic = "; ".join(sorted({u for us in valores.values() for u in us}))[:200]
        filas.append([p.parametro, p.valor_manual, p.cita_manual, vc, ubic, estado,
                      "Cumple" if estado == "Coincide" else "No cumple" if estado in ("Difiere", "Múltiples valores en código") else "Revisar"])
    md = ["| Parámetro | Valor manual | Cita manual | Valor(es) en código | Ubicación en código | Resultado | Estado |",
          "|---|---|---|---|---|---|---|"]
    md += ["| " + " | ".join(map(str, f)) + " |" for f in filas]
    n_nc = sum(f[6] == "No cumple" for f in filas)
    md += ["", f"Parámetros comparados: {len(filas)} · No cumple: {n_nc} · No ubicados: {sum(f[5]=='No ubicado en código' for f in filas)}",
           "Regla: toda diferencia es No cumple; cuantificar impacto re-ejecutando con el valor del manual."]
    open(a.salida, "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
