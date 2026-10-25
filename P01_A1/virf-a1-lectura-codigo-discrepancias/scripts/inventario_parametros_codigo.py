#!/usr/bin/env python3
"""Inventario de parámetros y operaciones sensibles en código de modelos (A1/A4/A8 · VIRF).

Uso:
    python inventario_parametros_codigo.py <carpeta_o_archivo> --salida parametros_codigo.csv

Lee .py, .ipynb y .sql. Para Python usa AST (cita función y línea exactas).
"""
import argparse
import ast
import csv
import json
import re
import sys
from pathlib import Path

OPS = {"fillna", "replace", "clip", "dropna", "drop_duplicates", "merge", "query", "where",
       "read_sql", "read_csv", "read_excel", "read_parquet", "to_csv", "to_excel", "to_sql",
       "seed", "cut", "qcut", "round", "astype"}
SQL_PATRONES = [
    (re.compile(r"\bFROM\s+([\w\.\[\]]+)", re.I), "fuente_sql"),
    (re.compile(r"\bJOIN\s+([\w\.\[\]]+)", re.I), "join_sql"),
    (re.compile(r"\bWHERE\b(.+)", re.I), "filtro_sql"),
    (re.compile(r"\bCOALESCE\s*\((.+?)\)", re.I), "imputacion_sql"),
    (re.compile(r"\bINSERT\s+INTO\s+([\w\.\[\]]+)", re.I), "salida_sql"),
    (re.compile(r"[<>]=?\s*(-?\d+(?:\.\d+)?)"), "umbral_sql"),
]


class Visitante(ast.NodeVisitor):
    def __init__(self, archivo, desfase=0, celda=None):
        self.archivo, self.desfase, self.celda = archivo, desfase, celda
        self.func = ["<módulo>"]
        self.filas = []

    def _add(self, nodo, tipo, detalle):
        self.filas.append({
            "archivo": self.archivo, "celda": self.celda if self.celda is not None else "",
            "funcion": self.func[-1] + "()", "linea": nodo.lineno + self.desfase,
            "tipo": tipo, "detalle": detalle[:200],
        })

    def visit_FunctionDef(self, n):
        self.func.append(n.name); self.generic_visit(n); self.func.pop()
    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Assign(self, n):
        if isinstance(n.value, ast.Constant) and isinstance(n.value.value, (int, float)) and not isinstance(n.value.value, bool):
            for t in n.targets:
                self._add(n, "parametro_literal", f"{ast.unparse(t)} = {n.value.value}")
        elif isinstance(n.value, (ast.Dict, ast.List, ast.Tuple)):
            nums = [c.value for c in ast.walk(n.value) if isinstance(c, ast.Constant) and isinstance(c.value, (int, float))]
            if nums:
                self._add(n, "parametro_coleccion", ast.unparse(n)[:200])
        self.generic_visit(n)

    def visit_Compare(self, n):
        consts = [c for c in [n.left, *n.comparators] if isinstance(c, ast.Constant) and isinstance(c.value, (int, float))]
        if consts:
            self._add(n, "umbral_comparacion", ast.unparse(n))
        self.generic_visit(n)

    def visit_Call(self, n):
        nombre = n.func.attr if isinstance(n.func, ast.Attribute) else getattr(n.func, "id", "")
        if nombre in OPS:
            self._add(n, f"op_{nombre}", ast.unparse(n))
        for kw in n.keywords:
            if kw.arg in ("random_state", "seed"):
                self._add(n, "semilla", f"{kw.arg}={ast.unparse(kw.value)}")
        self.generic_visit(n)


def analizar_py(texto, archivo, celda=None):
    try:
        arbol = ast.parse(texto)
    except SyntaxError as e:
        return [{"archivo": archivo, "celda": celda or "", "funcion": "", "linea": e.lineno or 0,
                 "tipo": "ERROR_SINTAXIS", "detalle": str(e)}]
    v = Visitante(archivo, celda=celda)
    v.visit(arbol)
    return v.filas


def analizar_sql(texto, archivo):
    filas = []
    for i, l in enumerate(texto.splitlines(), 1):
        for rx, tipo in SQL_PATRONES:
            for m in rx.finditer(l):
                filas.append({"archivo": archivo, "celda": "", "funcion": "(sql)", "linea": i,
                              "tipo": tipo, "detalle": l.strip()[:200]})
    return filas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ruta")
    ap.add_argument("--salida", default="parametros_codigo.csv")
    a = ap.parse_args()
    p = Path(a.ruta)
    archivos = [p] if p.is_file() else sorted(x for x in p.rglob("*") if x.suffix in (".py", ".ipynb", ".sql"))
    filas = []
    for f in archivos:
        txt = f.read_text(encoding="utf-8", errors="replace")
        if f.suffix == ".py":
            filas += analizar_py(txt, f.name)
        elif f.suffix == ".sql":
            filas += analizar_sql(txt, f.name)
        else:
            nb = json.loads(txt)
            for i, c in enumerate(nb.get("cells", []), 1):
                if c.get("cell_type") == "code":
                    src = "".join(c.get("source", []))
                    src = "\n".join("" if l.lstrip().startswith(("%", "!")) else l for l in src.splitlines())
                    filas += analizar_py(src, f.name, celda=i)
    if not filas:
        sys.exit("ERROR: no se encontraron elementos; revisar ruta o lenguaje del código.")
    with open(a.salida, "w", newline="", encoding="utf-8") as o:
        w = csv.DictWriter(o, fieldnames=list(filas[0].keys()))
        w.writeheader(); w.writerows(filas)
    resumen = {}
    for r in filas:
        resumen[r["tipo"]] = resumen.get(r["tipo"], 0) + 1
    print(f"{len(archivos)} archivos · {len(filas)} elementos -> {a.salida}")
    for k, v in sorted(resumen.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
