#!/usr/bin/env python3
"""Genera la matriz técnica de 8 columnas desde 01_Control_de_datos.xlsx (A3E · VIRF).

Uso: python matriz_8_columnas.py 01_Control_de_datos.xlsx --salida matriz_8col.md
"""
import argparse
import sys

import pandas as pd

MAPA = {
    "Dentro de umbral": "Conforme",
    "Fuera de umbral": "Falló",
    "No existe según evidencia": "No existe",
}


def clasif(est):
    est = str(est)
    if est in MAPA:
        return MAPA[est]
    if est.startswith("No verificable") or est.startswith("Error"):
        return "No verificable"
    return est


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx")
    ap.add_argument("--salida", default="matriz_8col.md")
    a = ap.parse_args()
    try:
        r = pd.read_excel(a.xlsx, sheet_name="Resumen")
    except Exception as e:
        sys.exit(f"No se puede leer la hoja Resumen ({e}). Solicitar re-ejecución de A3D.")
    if r.empty:
        sys.exit("Hoja Resumen vacía: solicitar re-ejecución de A3D.")
    lin = ["| Dimensión/Regla | Estado | % Cumplimiento | ¿Existe según evidencia? | Diagnóstico con cifra | Decisión/acción | Evidencia requerida | Referencia |",
           "|---|---|---|---|---|---|---|---|"]
    desc = 0
    for i, f in r.iterrows():
        ev, inf, con = f.get("n_evaluado"), f.get("n_infractor"), f.get("n_conforme")
        cuadra = pd.notna(ev) and (inf + con == ev)
        estado = clasif(f.get("estado_tecnico"))
        existe = "Sí (control del equipo)" if str(f.get("bloque", "")).startswith("1") else "No (solo batería del validador)"
        if estado == "No existe":
            existe = "No"
        if not cuadra and estado not in ("No existe",):
            desc += 1
            diag, pct, estado = "DESCUADRE de conteos: se declara, no se interpreta", "", "No verificable"
        elif estado in ("No existe",) or ev == 0:
            diag, pct = f"Sin ejecución: {f.get('estado_tecnico')}", ""
        else:
            pct = f"{100 - float(f.get('pct') or 0):.2f} %"
            diag = (f"{int(inf):,} de {int(ev):,} infractores ({float(f.get('pct') or 0):.4f} %) vs umbral "
                    f"{f.get('umbral_pct')} % ({f.get('origen_umbral')})").replace(",", " ")
        ref = f"{a.xlsx.split('/')[-1]} > Resumen > fila {i + 2}; control {f.get('id')}"
        lin.append(f"| {f.get('dimension')} · {f.get('regla')} | {estado} | {pct} | {existe} | {diag} | <<completar>> | <<completar>> | {ref} |")
    open(a.salida, "w", encoding="utf-8").write("\n".join(lin) + "\n")
    print(f"{len(r)} controles → {a.salida} · descuadres: {desc}")
    print(r.assign(clas=r.estado_tecnico.map(clasif)).groupby("clas").size().to_string())


if __name__ == "__main__":
    main()
