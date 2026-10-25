#!/usr/bin/env python3
"""Pruebas mínimas de admisibilidad de un notebook VIRF (A2, A3D, AD, AIM).

Uso:
    python pruebas_admisibilidad.py notebook.ipynb --salidas-dir salida/ --insumo-vacio datos_vacios/ --salida pruebas.csv

1) ejecución limpia en kernel nuevo; 2) idempotencia (hash de salidas en 2 corridas);
3) insumo vacío -> debe fallar con mensaje explícito. La reconciliación (prueba 2 de A2) se ejecuta aparte.
El notebook debe leer VIRF_INSUMO_DIR y VIRF_SALIDA_DIR de variables de entorno.
Requiere: jupyter nbconvert, nbclient.
"""
import argparse
import csv
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def ejecutar(nb, env_extra, timeout):
    env = os.environ.copy(); env.update(env_extra)
    tmp = tempfile.mkdtemp()
    cmd = [sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute",
           f"--ExecutePreprocessor.timeout={timeout}", "--output-dir", tmp, str(nb)]
    p = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return p.returncode, re.sub(r"\x1b\[[0-9;]*m", "", (p.stderr or ""))[-1500:]


def hash_contenido(f):
    """Hash del contenido: para .xlsx se hashean los valores (los metadatos de fecha del archivo cambian en cada corrida)."""
    if f.suffix.lower() in (".xlsx", ".xlsm"):
        import pandas as pd
        hojas = pd.read_excel(f, sheet_name=None)
        return "".join(k + v.to_csv(index=False) for k, v in sorted(hojas.items())).encode()
    return f.read_bytes()


def hash_dir(d):
    h = hashlib.sha256()
    for f in sorted(Path(d).rglob("*")):
        if f.is_file() and f.suffix.lower() not in (".log", ".ipynb"):
            h.update(f.name.encode()); h.update(hash_contenido(f))
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("notebook")
    ap.add_argument("--salidas-dir", default=None, help="carpeta donde el notebook escribe; se usa VIRF_SALIDA_DIR")
    ap.add_argument("--insumo-vacio", default=None)
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--salida", default="pruebas.csv")
    a = ap.parse_args()
    nb = Path(a.notebook)
    filas = []

    s1, s2 = tempfile.mkdtemp(), tempfile.mkdtemp()
    rc, err = ejecutar(nb, {"VIRF_SALIDA_DIR": s1}, a.timeout)
    filas.append(("P-01", "Ejecución limpia en kernel reiniciado", "sin excepción",
                  "OK" if rc == 0 else f"ERROR: {err.splitlines()[-1] if err else rc}", rc == 0))
    if rc == 0:
        rc2, _ = ejecutar(nb, {"VIRF_SALIDA_DIR": s2}, a.timeout)
        h1, h2 = hash_dir(s1), hash_dir(s2)
        filas.append(("P-02", "Idempotencia (dos corridas, hash de salidas)", "hashes idénticos",
                      f"{h1[:12]} vs {h2[:12]}", rc2 == 0 and h1 == h2 and h1 != hashlib.sha256().hexdigest()))
    if a.insumo_vacio:
        Path(a.insumo_vacio).mkdir(parents=True, exist_ok=True)
        rc3, err3 = ejecutar(nb, {"VIRF_INSUMO_DIR": a.insumo_vacio, "VIRF_SALIDA_DIR": tempfile.mkdtemp()}, a.timeout)
        err3 = re.sub(r"\x1b\[[0-9;]*m", "", err3)
        ultimo = err3.strip().splitlines()[-1] if err3.strip() else ""
        filas.append(("P-03", "Insumo vacío falla con mensaje explícito", "falla con mensaje",
                      ultimo[:200] or "terminó sin error (resultado silencioso)", rc3 != 0 and bool(ultimo)))
    for d in (s1, s2):
        shutil.rmtree(d, ignore_errors=True)

    with open(a.salida, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ID prueba", "Control asociado", "Descripción de la prueba", "Insumo/dataset", "Resultado esperado",
                    "Resultado obtenido", "PASA / FALLA", "Umbral y su fuente", "Script o celda", "Fuente exacta"])
        for i, d, esp, obt, ok in filas:
            w.writerow([i, "C4", d, nb.name, esp, obt, "PASA" if ok else "FALLA", "n/a (prueba binaria)",
                        "pruebas_admisibilidad.py", nb.name])
    for i, d, esp, obt, ok in filas:
        print(f"[{'PASA' if ok else 'FALLA'}] {i} {d}: {obt}")
    admisible = all(r[4] for r in filas)
    print("Notebook admisible" if admisible else "notebook no admisible")
    sys.exit(0 if admisible else 1)


if __name__ == "__main__":
    main()
