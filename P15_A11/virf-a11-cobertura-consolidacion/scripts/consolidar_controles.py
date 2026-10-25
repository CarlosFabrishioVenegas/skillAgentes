#!/usr/bin/env python3
"""Consolida matrices de control (A5–A10) contra las actividades VIRF aplicables (A11 · VIRF).

Uso:
    python consolidar_controles.py --actividades actividades_tier.csv --controles A5.md A6.md ... \
        --salida consolidado.csv --reporte consolidacion.md
"""
import argparse
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd

OFICIALES = ["Cumple", "Cumple con observación", "No cumple", "No evidenciado", "No verificable", "No aplica"]
AGENTE_CONTROL = {"A5": "C1", "A6": "C2", "A7": "C3", "A8": "C4", "A9": "C5", "A10": "C6"}
ENCABEZADOS = ("id virf", "campo del acta", "output", "bloque de codigo")
RE_CITA = re.compile(r"(p{1,2}\.\s?\d+|línea\s+\d+|>\s*\w|celda|fila\s+\d+|acta\s+\d+|acuerdo)", re.I)


def norm(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower().strip()


def normalizar_estado(v):
    t = norm(v)
    t = re.sub(r"\s*[—-]\s*remediado.*", "", t)
    for o in sorted(OFICIALES, key=len, reverse=True):
        if t.startswith(norm(o)):
            return o, norm(v) != norm(o) and "remediado" not in norm(v)
    if "uso satisfactorio con observacion" in t:
        return "Cumple con observación", False
    if "uso satisfactorio" in t:
        return "Cumple", False
    if "uso no satisfactorio" in t or "sin uso" in t:
        return "No cumple", False
    return None, True


def tablas_md(texto):
    lin, tablas, actual = texto.splitlines(), [], []
    for l in lin + [""]:
        if l.strip().startswith("|"):
            actual.append(l.strip())
        elif actual:
            tablas.append(actual); actual = []
    out = []
    for t in tablas:
        if len(t) < 3:
            continue
        enc = [c.strip() for c in t[0].strip("|").split("|")]
        filas = [[c.strip() for c in r.strip("|").split("|")] for r in t[2:]]
        out.append(pd.DataFrame([f + [""] * (len(enc) - len(f)) for f in filas], columns=enc))
    return out


def col(df, *claves):
    for c in df.columns:
        if any(k in norm(c) for k in claves):
            return c
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--actividades", required=True)
    ap.add_argument("--controles", nargs="+", required=True)
    ap.add_argument("--salida", default="consolidado.csv")
    ap.add_argument("--reporte", default="consolidacion.md")
    a = ap.parse_args()
    act = pd.read_csv(a.actividades, dtype=str)
    filas, devoluciones = [], []
    for ruta in a.controles:
        nombre = Path(ruta).stem
        ag = re.match(r"(A\d+)", nombre)
        ag = ag.group(1) if ag else nombre
        ctrl = AGENTE_CONTROL.get(ag, "")
        tabs = tablas_md(Path(ruta).read_text(encoding="utf-8"))
        t = next((d for d in tabs if any("id virf" in norm(c) for c in d.columns)), None)
        if t is None:
            t = next((d for d in tabs if any(norm(d.columns[0]).startswith(e) for e in ENCABEZADOS)), None)
            if t is not None:
                devoluciones.append((ag, "-", "Matriz sin columna 'ID VIRF': filas no rastreables al estándar (agregar la columna)"))
        if t is None:
            devoluciones.append((ag, "-", "No se encontró la matriz principal del control")); continue
        c_id = next((c for c in t.columns if "id virf" in norm(c)), t.columns[0])
        c_est = col(t, "estado", "cumple", "satisfactorio", "coincide", "suficiente")
        c_fte = col(t, "fuente exacta", "fuente revisada", "fuente")
        c_res = col(t, "resultado", "sustento del estado", "evaluacion")
        c_act = col(t, "actividad", "decision", "campo", "output", "bloque")
        for _, r in t.iterrows():
            est_raw = r[c_est] if c_est else ""
            est, irregular = normalizar_estado(est_raw)
            fte = r[c_fte] if c_fte else ""
            if irregular:
                devoluciones.append((ag, r[c_id], f"Estado no oficial: '{est_raw}'"))
            if not fte or not RE_CITA.search(fte):
                devoluciones.append((ag, r[c_id], "Fila sin fuente exacta citable"))
            if est == "No aplica" and not re.search(r"(regla|exime|exento|art)", norm(r.to_string())):
                devoluciones.append((ag, r[c_id], "No aplica sin cita de la regla que exime → reclasificado a No evidenciado"))
                est = "No evidenciado"
            res = r[c_res] if c_res else ""
            filas.append({"id_virf": r[c_id], "control": ctrl, "agente_origen": ag, "actividad": r[c_act] if c_act else "",
                          "estado": est or "No evidenciado", "estado_original": est_raw,
                          "tipo": "Cuantitativo" if re.search(r"\d+([.,]\d+)?\s*%|\b\d{2,}\b", str(res)) else "Cualitativo",
                          "resultado": res, "fuente_exacta": fte, "remediado_en_ciclo": "remediado" in norm(est_raw)})
    C = pd.DataFrame(filas)
    # cobertura
    ids_recibidos = set(C.id_virf.astype(str)) if len(C) else set()
    faltan = act[~act.id_virf.astype(str).isin(ids_recibidos)]
    for _, r in faltan.iterrows():
        filas.append({"id_virf": r.id_virf, "control": r.get("control", ""), "agente_origen": f"(sin fila; responsable {next((k for k,v in AGENTE_CONTROL.items() if v==r.get('control')), '?')})",
                      "actividad": r.actividad, "estado": "No evidenciado", "estado_original": "", "tipo": "", "resultado": "",
                      "fuente_exacta": "Incorporado por A11 por falta de fila", "remediado_en_ciclo": False})
    C = pd.DataFrame(filas)
    # inconsistencias
    inc = C[C.id_virf.isin(act.id_virf)].groupby("id_virf").estado.nunique()
    inconsist = inc[inc > 1].index.tolist()
    C["inconsistencia"] = C.id_virf.isin(inconsist)
    C.to_csv(a.salida, index=False)
    aplic = act.groupby("control").size()
    recibidos = set(C.loc[~C.agente_origen.str.startswith("(sin fila"), "id_virf"].astype(str))
    cub = act.assign(_c=act.id_virf.astype(str).isin(recibidos)).groupby("control")._c.sum()
    md = ["# Consolidación A11", "", "## Cobertura", "| Control | Aplicables | Con fila | Cobertura |", "|---|---|---|---|"]
    for c_, n in aplic.items():
        k = int(cub.get(c_, 0)); md.append(f"| {c_} | {n} | {k} | {100*k/n:.1f} % |")
    tot_k = int(cub.sum()); tot_n = int(aplic.sum())
    md += [f"| **Global** | {tot_n} | {tot_k} | **{100*tot_k/max(tot_n,1):.1f} %** |", "",
           "Regla: cobertura < 100 % ⇒ conclusión 'Validación incompleta'." if tot_k < tot_n else "Cobertura completa.", "",
           "## Semáforo por control", C.pivot_table(index="control", columns="estado", values="id_virf", aggfunc="count", fill_value=0).to_markdown() if len(C) else "",
           "", "## Devoluciones a agentes", "| Agente | Fila | Motivo |", "|---|---|---|"]
    md += [f"| {g} | {i} | {m} |" for g, i, m in devoluciones] or ["| — | — | Sin devoluciones |"]
    md += ["", "## Inconsistencias entre controles", ", ".join(map(str, inconsist)) or "Ninguna"]
    Path(a.reporte).write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:12 + len(aplic)]))
    print(f"Devoluciones: {len(devoluciones)} · Inconsistencias: {len(inconsist)} · Actividades agregadas como No evidenciado: {len(faltan)}")


if __name__ == "__main__":
    main()
