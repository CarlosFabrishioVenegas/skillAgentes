#!/usr/bin/env python3
"""Genera un notebook de diagnóstico determinista para el agente AD (VIRF).

Uso:
    python generar_notebook_diagnostico.py --prefijo 00a --tema esquema --salida 00a_Diagnostico_esquema.ipynb
    python generar_notebook_diagnostico.py --prefijo 01b --tema variables --variables ingreso_declarado,score,dias_mora --salida ...
Temas: esquema | variables | ciclo_vida | reproduccion
"""
import argparse
import json

CELDA_META = '''# === Metadatos ===
import sys, platform, datetime
import pandas as pd, numpy as np
PREFIJO = "{prefijo}"
TEMA = "{tema}"
PREGUNTAS = {preguntas!r}
print(PREFIJO, TEMA, datetime.datetime.now().isoformat(timespec="seconds"))
print("python", platform.python_version(), "| pandas", pd.__version__, "| numpy", np.__version__)'''

CELDA_CONFIG = '''# === CONFIG ===
import os, hashlib, itertools
from pathlib import Path
CONFIG = {{
    "insumo_dir": os.environ.get("VIRF_INSUMO_DIR", "datos"),
    "salida_dir": os.environ.get("VIRF_SALIDA_DIR", "salida_diagnostico"),
    "semilla": 20261017,
    "max_cols_llave": 3,
    "variables_modelo": {variables!r},
    "patron_fecha": r"(fec|fecha|date|periodo|period|mes|corte)",
    "patron_saldo": r"(saldo|balance|exposic|ead|monto|capital)",
    "patron_estado": r"(estado|status|situac|calif|bucket|stage)",
    "patron_id": r"(id|cod|codigo|cliente|cuenta|operac|contrato|nro)",
}}
Path(CONFIG["salida_dir"]).mkdir(parents=True, exist_ok=True)
ERRORES = []
RESUMEN = {{}}'''

CELDA_CARGA = '''# === Carga tolerante (solo lectura) ===
def _fila_encabezado(df_raw):
    for i in range(min(20, len(df_raw))):
        fila = df_raw.iloc[i]
        txt = fila.apply(lambda v: isinstance(v, str) and v.strip() != "").mean()
        if txt >= 0.6:
            return i
    return 0

def a_fecha(s):
    txt = s.astype(str).str.strip()
    iso = txt.str.match(r"^\\d{4}[-/]\\d{1,2}[-/]\\d{1,2}").mean() > 0.5
    return pd.to_datetime(txt, errors="coerce", dayfirst=not iso, format="mixed")

TABLAS, ARCHIVOS = {}, []
for f in sorted(Path(CONFIG["insumo_dir"]).glob("*")):
    if f.suffix.lower() not in (".csv", ".parquet", ".xlsx", ".xls", ".txt"):
        continue
    sha = hashlib.sha256(f.read_bytes()).hexdigest()
    try:
        if f.suffix.lower() in (".csv", ".txt"):
            df = pd.read_csv(f, sep=None, engine="python")
        elif f.suffix.lower() == ".parquet":
            df = pd.read_parquet(f)
        else:
            raw = pd.read_excel(f, header=None)
            h = _fila_encabezado(raw)
            df = pd.read_excel(f, header=h)
        TABLAS[f.stem] = df
        ARCHIVOS.append({"archivo": f.name, "filas": len(df), "columnas": df.shape[1], "sha256": sha})
    except Exception as e:
        ERRORES.append({"seccion": "carga", "archivo": f.name, "error": repr(e)})
if not TABLAS:
    raise ValueError(f"Insumo vacío: no hay tablas legibles en {CONFIG['insumo_dir']}. No se produce resultado.")
RESUMEN["Archivos"] = pd.DataFrame(ARCHIVOS)
RESUMEN["Archivos"]'''

CELDA_ESQUEMA = '''# === Descubrimiento de esquema ===
filas = []
for t, df in TABLAS.items():
    for c in df.columns:
        s = df[c]
        ej = s.dropna().astype(str).drop_duplicates().sort_values().head(3).tolist()
        filas.append({"tabla": t, "columna": str(c), "dtype": str(s.dtype), "pct_nulos": round(100 * s.isna().mean(), 4),
                      "n_unicos": int(s.nunique(dropna=True)), "min": s.min() if pd.api.types.is_numeric_dtype(s) else "",
                      "max": s.max() if pd.api.types.is_numeric_dtype(s) else "", "ejemplos": " | ".join(ej)})
RESUMEN["Esquema"] = pd.DataFrame(filas)
RESUMEN["Esquema"].head(50)'''

CELDA_LLAVES = '''# === Llaves candidatas (unicidad 100 %) ===
import re
filas = []
for t, df in TABLAS.items():
    cand = [c for c in df.columns if re.search(CONFIG["patron_id"], str(c), re.I) or re.search(CONFIG["patron_fecha"], str(c), re.I)]
    cand = cand[:12]
    for k in range(1, CONFIG["max_cols_llave"] + 1):
        for combo in itertools.combinations(cand, k):
            try:
                dup = int(df.duplicated(subset=list(combo)).sum())
            except Exception as e:
                ERRORES.append({"seccion": "llaves", "archivo": t, "error": repr(e)}); continue
            filas.append({"tabla": t, "llave": " + ".join(map(str, combo)), "n_columnas": k, "duplicados": dup, "unica": dup == 0})
llaves = pd.DataFrame(filas)
RESUMEN["Llaves"] = llaves.sort_values(["tabla", "unica", "n_columnas"], ascending=[True, False, True]) if len(llaves) else llaves
RESUMEN["Llaves"].head(30)'''

CELDA_TEMPORAL = '''# === Cobertura temporal ===
filas = []
for t, df in TABLAS.items():
    for c in df.columns:
        if not re.search(CONFIG["patron_fecha"], str(c), re.I):
            continue
        s = a_fecha(df[c])
        if s.notna().mean() < 0.5:
            s2 = pd.to_datetime(df[c].astype(str), format="%Y%m", errors="coerce")
            s = s2 if s2.notna().mean() > s.notna().mean() else s
        if s.notna().sum() == 0:
            continue
        meses = s.dt.to_period("M").dropna().unique()
        todos = pd.period_range(min(meses), max(meses), freq="M")
        huecos = sorted(set(map(str, todos)) - set(map(str, meses)))
        filas.append({"tabla": t, "columna": str(c), "min": s.min(), "max": s.max(), "n_meses": len(meses),
                      "meses_faltantes": ", ".join(huecos[:24]), "pct_no_parseable": round(100 * s.isna().mean(), 4)})
RESUMEN["Temporal"] = pd.DataFrame(filas)
RESUMEN["Temporal"]'''

TEMAS = {
    "esquema": None,
    "variables": '''# === Variables del modelo: presencia, nulos, rangos ===
filas = []
for v in CONFIG["variables_modelo"]:
    hallada = [(t, c) for t, df in TABLAS.items() for c in df.columns if str(c).lower() == v.lower()]
    if not hallada:
        filas.append({"variable": v, "presente": False, "tabla": "", "pct_nulos": "", "min": "", "p1": "", "p50": "", "p99": "", "max": ""})
        continue
    for t, c in hallada:
        s = TABLAS[t][c]
        num = pd.to_numeric(s, errors="coerce")
        q = num.quantile([0.01, 0.5, 0.99]) if num.notna().any() else pd.Series([None]*3, index=[0.01, 0.5, 0.99])
        filas.append({"variable": v, "presente": True, "tabla": t, "pct_nulos": round(100*s.isna().mean(), 4),
                      "min": num.min(), "p1": q[0.01], "p50": q[0.5], "p99": q[0.99], "max": num.max()})
RESUMEN["Variables"] = pd.DataFrame(filas)
RESUMEN["Variables"]''',
    "ciclo_vida": '''# === Ciclo de vida: saldos que resucitan, continuidad, transiciones ===
filas = []
for t, df in TABLAS.items():
    cid = next((c for c in df.columns if re.search(CONFIG["patron_id"], str(c), re.I)), None)
    cfe = next((c for c in df.columns if re.search(CONFIG["patron_fecha"], str(c), re.I)), None)
    csa = next((c for c in df.columns if re.search(CONFIG["patron_saldo"], str(c), re.I)), None)
    ces = next((c for c in df.columns if re.search(CONFIG["patron_estado"], str(c), re.I)), None)
    filas.append({"tabla": t, "regla": "columnas detectadas", "resultado": f"id={cid} fecha={cfe} saldo={csa} estado={ces}"})
    if not (cid and cfe):
        continue
    d = df[[x for x in [cid, cfe, csa, ces] if x]].copy()
    d["_f"] = a_fecha(d[cfe])
    d = d.sort_values([cid, "_f"])
    if csa:
        s = pd.to_numeric(d[csa], errors="coerce")
        prev = s.groupby(d[cid]).shift(1)
        resuc = int(((prev == 0) & (s > 0)).sum())
        filas.append({"tabla": t, "regla": "saldo que resucita (0 -> >0)", "resultado": resuc})
        filas.append({"tabla": t, "regla": "saldos negativos", "resultado": int((s < 0).sum())})
    m = d["_f"].dt.to_period("M")
    gap = (m.groupby(d[cid]).diff().apply(lambda x: x.n if pd.notna(x) else 1) > 1).sum()
    filas.append({"tabla": t, "regla": "operaciones con meses intermedios faltantes", "resultado": int(gap)})
    if ces:
        tr = (d[ces].astype(str).groupby(d[cid]).shift(1).fillna("INICIO") + " -> " + d[ces].astype(str)).value_counts().head(25)
        for k, v in tr.items():
            filas.append({"tabla": t, "regla": f"transición {k}", "resultado": int(v)})
RESUMEN["CicloVida"] = pd.DataFrame(filas)
RESUMEN["CicloVida"]''',
    "reproduccion": '''# === Sumas y conteos de control (comparar con output publicado) ===
filas = []
for t, df in TABLAS.items():
    filas.append({"tabla": t, "metrica": "n_filas", "valor": len(df)})
    for c in df.select_dtypes("number").columns:
        filas.append({"tabla": t, "metrica": f"suma::{c}", "valor": float(df[c].sum())})
        filas.append({"tabla": t, "metrica": f"media::{c}", "valor": float(df[c].mean())})
RESUMEN["Reproduccion"] = pd.DataFrame(filas)
# Completar a mano: valor publicado y su fuente, para que AD cite la diferencia
RESUMEN["Reproduccion"]["valor_publicado"] = ""
RESUMEN["Reproduccion"]["fuente_publicado"] = ""
RESUMEN["Reproduccion"]''',
}

CELDA_EXPORT = '''# === Escritura del resumen (siempre) ===
RESUMEN["Errores"] = pd.DataFrame(ERRORES or [{"seccion": "", "archivo": "", "error": "sin errores"}])
ruta = Path(CONFIG["salida_dir"]) / f"{PREFIJO}_resumen.xlsx"
with pd.ExcelWriter(ruta) as xw:
    pd.DataFrame({"pregunta": PREGUNTAS}).to_excel(xw, sheet_name="Preguntas", index=False)
    for k, v in RESUMEN.items():
        v2 = v.copy()
        for c in v2.select_dtypes(include=["datetimetz"]).columns:
            v2[c] = v2[c].dt.tz_localize(None)
        v2.to_excel(xw, sheet_name=k[:31], index=False)
print("Resumen escrito en", ruta)'''


def celda(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": src}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefijo", required=True)
    ap.add_argument("--tema", required=True, choices=list(TEMAS))
    ap.add_argument("--variables", default="")
    ap.add_argument("--preguntas", default="")
    ap.add_argument("--salida", required=True)
    a = ap.parse_args()
    vars_ = [v.strip() for v in a.variables.split(",") if v.strip()]
    preg = [p.strip() for p in a.preguntas.split("|") if p.strip()] or [f"Diagnóstico de {a.tema}"]
    celdas = [CELDA_META.format(prefijo=a.prefijo, tema=a.tema, preguntas=preg),
              CELDA_CONFIG.format(variables=vars_), CELDA_CARGA, CELDA_ESQUEMA, CELDA_LLAVES, CELDA_TEMPORAL]
    if TEMAS[a.tema]:
        celdas.append(TEMAS[a.tema])
    celdas.append(CELDA_EXPORT)
    nb = {"cells": [{"cell_type": "markdown", "metadata": {}, "source": f"# {a.prefijo}_Diagnostico_{a.tema}\nNotebook determinista de solo lectura generado para el agente AD (VIRF)."}]
          + [celda(c) for c in celdas],
          "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}},
          "nbformat": 4, "nbformat_minor": 5}
    with open(a.salida, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print("Notebook generado:", a.salida)


if __name__ == "__main__":
    main()
