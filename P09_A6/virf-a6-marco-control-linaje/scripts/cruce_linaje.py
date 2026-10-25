#!/usr/bin/env python3
"""Cruza variables del modelo contra el diccionario de datos para verificar linaje (A6 · VIRF).

Uso:
    python cruce_linaje.py --variables variables_modelo.csv --diccionario diccionario.xlsx --salida linaje.csv
"""
import argparse
import difflib
import re
import sys
import unicodedata

import pandas as pd

ALIAS = {
    "campo": ["campo", "variable", "nombre", "columna", "atributo", "field"],
    "sistema": ["sistema", "fuente", "origen", "aplicativo", "source"],
    "tabla": ["tabla", "entidad", "vista", "table", "datamart"],
    "responsable": ["responsable", "owner", "custodio", "dueno", "steward", "area responsable"],
}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower().strip()
    return re.sub(r"[\s_\-]+", "_", s)


def leer_diccionario(ruta):
    hojas = pd.read_excel(ruta, sheet_name=None, header=None, dtype=str) if ruta.endswith((".xlsx", ".xls")) else {"csv": pd.read_csv(ruta, header=None, dtype=str)}
    for hoja, raw in hojas.items():
        for i in range(min(25, len(raw))):
            fila = [norm(x) for x in raw.iloc[i].tolist()]
            mapa = {}
            for campo, al in ALIAS.items():
                for j, v in enumerate(fila):
                    if any(v == norm(a) or v.startswith(norm(a)) for a in al):
                        mapa.setdefault(campo, j)
            if "campo" in mapa and len(mapa) >= 2:
                cuerpo = raw.iloc[i + 1:]
                df = pd.DataFrame({k: cuerpo.iloc[:, j].values for k, j in mapa.items()})
                df["_hoja"], df["_fila"] = hoja, range(i + 2, i + 2 + len(df))
                return df.dropna(subset=["campo"])
    sys.exit("No se encontró encabezado de diccionario reconocible (alias: campo/sistema/tabla/responsable).")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variables", required=True)
    ap.add_argument("--diccionario", required=True)
    ap.add_argument("--salida", default="linaje.csv")
    a = ap.parse_args()
    vars_ = pd.read_csv(a.variables)["variable"].dropna().astype(str).tolist()
    dic = leer_diccionario(a.diccionario)
    dic["_k"] = dic["campo"].map(norm)
    filas = []
    for v in vars_:
        k = norm(v)
        hit = dic[dic["_k"] == k]
        tipo = "exacta"
        if hit.empty:
            cerca = difflib.get_close_matches(k, dic["_k"].tolist(), n=1, cutoff=0.85)
            hit = dic[dic["_k"].isin(cerca)]
            tipo = "coincidencia_aproximada" if not hit.empty else "no_presente"
        if hit.empty:
            filas.append({"variable": v, "presente_en_diccionario": False, "tipo_coincidencia": tipo,
                          "linaje_completo": False, "faltantes": "todo", "fuente": a.diccionario})
            continue
        h = hit.iloc[0]
        falt = [c for c in ("sistema", "tabla", "responsable") if c not in h or pd.isna(h.get(c)) or not str(h.get(c)).strip()]
        filas.append({"variable": v, "presente_en_diccionario": True, "tipo_coincidencia": tipo,
                      "campo_diccionario": h["campo"], "sistema": h.get("sistema"), "tabla": h.get("tabla"),
                      "responsable": h.get("responsable"), "linaje_completo": not falt and tipo == "exacta",
                      "faltantes": ", ".join(falt), "fuente": f"{a.diccionario} > {h['_hoja']} > fila {h['_fila']}"})
    out = pd.DataFrame(filas)
    out.to_csv(a.salida, index=False)
    n = len(out)
    print(f"Variables del modelo: {n} · linaje completo: {int(out.linaje_completo.sum())} "
          f"({100*out.linaje_completo.mean():.1f} %) · no presentes: {int((~out.presente_en_diccionario).sum())} · "
          f"aproximadas (confirmar): {int((out.tipo_coincidencia=='coincidencia_aproximada').sum())}")


if __name__ == "__main__":
    main()
