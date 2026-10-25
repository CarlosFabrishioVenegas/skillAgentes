#!/usr/bin/env python3
"""Escáner de riesgos de implementación en código de modelos (A8 · VIRF).

Uso: python escanear_riesgos_codigo.py <carpeta_codigo> --salida riesgos_codigo.csv
Detecta R01–R10 (ver SKILL.md). No transcribe secretos: los enmascara.
"""
import argparse
import ast
import csv
import json
import re
import sys
from pathlib import Path

RUTA_LOCAL = re.compile(r"([A-Za-z]:\\\\?Users|/home/|/Users/|Desktop|Escritorio|OneDrive|Documents\\\\|Mis documentos)", re.I)
CREDENCIAL = re.compile(r"(password|passwd|pwd|secret|token|api[_-]?key)\s*[:=]\s*['\"][^'\"]{3,}['\"]|(uid|user id)=[^;]+;\s*(pwd|password)=[^;]+", re.I)
ALEATORIO = {"rand", "randn", "randint", "choice", "shuffle", "permutation", "sample", "random", "uniform", "normal"}
NECESITA_SEMILLA = {"train_test_split", "RandomForestClassifier", "RandomForestRegressor", "GradientBoostingClassifier",
                    "KMeans", "XGBClassifier", "LGBMClassifier", "StratifiedKFold", "KFold", "ShuffleSplit"}
LECTURA = {"read_csv", "read_excel", "read_parquet", "read_sql", "read_pickle"}
ESCRITURA = {"to_csv", "to_excel", "to_parquet", "to_sql", "to_pickle"}
FILTRO = {"dropna", "drop_duplicates", "query"}


def enmascarar(s):
    return re.sub(r"(['\"])([^'\"]{2})[^'\"]*([^'\"]{1})(['\"])", r"\1\2***\3\4", s)


class V(ast.NodeVisitor):
    def __init__(self, archivo, celda, add):
        self.archivo, self.celda, self.add = archivo, celda, add
        self.func = ["<módulo>"]
        self.semilla_global = False
        self.lecturas, self.escrituras = {}, {}
        self.tiene_validacion = False

    def _a(self, n, cod, msg, sev):
        self.add(self.archivo, self.celda, self.func[-1] + "()", getattr(n, "lineno", 0), cod, msg, sev)

    def visit_FunctionDef(self, n):
        self.func.append(n.name); self.generic_visit(n); self.func.pop()
    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ExceptHandler(self, n):
        desnudo = n.type is None
        generico = isinstance(n.type, ast.Name) and n.type.id in ("Exception", "BaseException")
        solo_pass = all(isinstance(b, (ast.Pass, ast.Continue)) for b in n.body)
        if desnudo or (generico and solo_pass):
            self._a(n, "R01", "Excepción genérica que puede ocultar fallas" + (" (except: pass)" if solo_pass else ""), "Media/Alta")
        self.generic_visit(n)

    def visit_Assert(self, n):
        self.tiene_validacion = True; self.generic_visit(n)

    def visit_Raise(self, n):
        self.tiene_validacion = True; self.generic_visit(n)

    def visit_Call(self, n):
        nombre = n.func.attr if isinstance(n.func, ast.Attribute) else getattr(n.func, "id", "")
        src = ast.unparse(n)
        if nombre == "filterwarnings" and "ignore" in src:
            self._a(n, "R02", "Warnings silenciados", "Media")
        if nombre in ("seed",) or any(k.arg in ("random_state", "seed") for k in n.keywords):
            self.semilla_global = True
        if nombre in ALEATORIO and re.search(r"(np\.random|random\.)", src) and "default_rng(" not in src:
            self._a(n, "R05", f"Llamada aleatoria sin generador sembrado: {src[:80]}", "Alta (T1–T2)")
        if nombre in NECESITA_SEMILLA and not any(k.arg == "random_state" for k in n.keywords):
            self._a(n, "R05", f"{nombre} sin random_state", "Alta (T1–T2)")
        if nombre == "default_rng" and not n.args and not n.keywords:
            self._a(n, "R05", "default_rng() sin semilla", "Alta (T1–T2)")
        if nombre in LECTURA and n.args and isinstance(n.args[0], ast.Constant):
            self.lecturas[str(n.args[0].value)] = n.lineno
        if nombre in ESCRITURA and n.args and isinstance(n.args[0], ast.Constant):
            self.escrituras[str(n.args[0].value)] = n.lineno
        if nombre in FILTRO or (nombre == "merge" and any(k.arg == "how" and ast.unparse(k.value).strip("'\"") == "inner" for k in n.keywords)) \
                or (nombre == "merge" and not any(k.arg == "how" for k in n.keywords)):
            self._a(n, "R09", f"Operación que puede descartar registros sin conteo: {src[:80]}", "Revisar")
        self.generic_visit(n)

    def visit_Assign(self, n):
        s = ast.unparse(n)
        if "chained_assignment" in s and "None" in s:
            self._a(n, "R02", "Aviso de chained assignment desactivado", "Media")
        self.generic_visit(n)

    def visit_Constant(self, n):
        if isinstance(n.value, str) and RUTA_LOCAL.search(n.value):
            self._a(n, "R03", f"Ruta absoluta local: {n.value[:80]}", "Media")
        self.generic_visit(n)


def analizar(texto, archivo, celda, add):
    for i, l in enumerate(texto.splitlines(), 1):
        if CREDENCIAL.search(l):
            add(archivo, celda, "", i, "R04", "Posible credencial embebida: " + enmascarar(l.strip())[:100], "Alta")
    try:
        t = ast.parse(texto)
    except SyntaxError as e:
        add(archivo, celda, "", e.lineno or 0, "ERROR", f"No parsea: {e.msg}", "Revisar"); return None
    v = V(archivo, celda, add); v.visit(t)
    for ruta, ln in v.escrituras.items():
        if ruta in v.lecturas:
            add(archivo, celda, "", ln, "R07", f"Escritura sobre ruta leída: {ruta}", "Alta")
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ruta")
    ap.add_argument("--salida", default="riesgos_codigo.csv")
    a = ap.parse_args()
    raiz = Path(a.ruta)
    filas = []
    add = lambda ar, ce, fu, li, co, de, se: filas.append({"archivo": ar, "celda": ce, "funcion": fu, "linea": li, "codigo": co, "detalle": de, "severidad_sugerida": se})
    archivos = [raiz] if raiz.is_file() else sorted(x for x in raiz.rglob("*") if x.suffix in (".py", ".ipynb", ".sql"))
    validacion = False
    for f in archivos:
        txt = f.read_text(encoding="utf-8", errors="replace")
        if f.suffix == ".py":
            v = analizar(txt, f.name, "", add); validacion |= bool(v and v.tiene_validacion)
        elif f.suffix == ".ipynb":
            nb = json.loads(txt)
            cnts = [c.get("execution_count") for c in nb.get("cells", []) if c.get("cell_type") == "code"]
            ej = [c for c in cnts if c is not None]
            if ej and (ej != sorted(ej) or None in cnts[: len(cnts) - cnts[::-1].index(ej[-1]) if ej else 0]):
                add(f.name, "", "", 0, "R08", f"Celdas ejecutadas fuera de orden o intercaladas sin ejecutar: {cnts[:20]}", "Reproducibilidad no acreditada")
            for i, c in enumerate(nb.get("cells", []), 1):
                if c.get("cell_type") == "code":
                    src = "\n".join("" if l.lstrip().startswith(("%", "!")) else l for l in "".join(c.get("source", [])).splitlines())
                    v = analizar(src, f.name, i, add); validacion |= bool(v and v.tiene_validacion)
        else:
            for i, l in enumerate(txt.splitlines(), 1):
                if CREDENCIAL.search(l):
                    add(f.name, "", "(sql)", i, "R04", "Posible credencial: " + enmascarar(l.strip())[:100], "Alta")
    reqs = list(raiz.rglob("requirements*.txt")) + list(raiz.rglob("environment*.yml")) + list(raiz.rglob("pyproject.toml")) if raiz.is_dir() else []
    if not reqs:
        add("(proyecto)", "", "", 0, "R06", "No hay archivo de dependencias (requirements/environment/pyproject)", "Media")
    for r in reqs:
        if r.suffix == ".txt":
            for i, l in enumerate(r.read_text(errors="replace").splitlines(), 1):
                l = l.strip()
                if l and not l.startswith(("#", "-")) and "==" not in l:
                    add(r.name, "", "", i, "R06", f"Dependencia sin versión fijada: {l}", "Media")
    if not validacion and archivos:
        add("(proyecto)", "", "", 0, "R10", "No se encontraron validaciones de entrada (assert/raise)", "Media")
    if not archivos:
        sys.exit("No se encontró código (.py/.ipynb/.sql).")
    with open(a.salida, "w", newline="", encoding="utf-8") as o:
        w = csv.DictWriter(o, fieldnames=list(filas[0].keys()) if filas else ["archivo"]); w.writeheader(); w.writerows(filas)
    cont = {}
    for r in filas:
        cont[r["codigo"]] = cont.get(r["codigo"], 0) + 1
    print(f"{len(archivos)} archivos · {len(filas)} hallazgos → {a.salida}")
    for k in sorted(cont):
        print(f"  {k}: {cont[k]}")


if __name__ == "__main__":
    main()
