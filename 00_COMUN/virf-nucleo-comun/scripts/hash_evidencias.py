#!/usr/bin/env python3
"""Calcula SHA-256 de evidencias para el anexo de trazabilidad VIRF.

Uso:
    python hash_evidencias.py <ruta> [<ruta> ...] --salida evidencias_hash.csv

Cada ruta puede ser archivo o carpeta (se recorre recursivamente).
No modifica ningún archivo de entrada.
"""
import argparse
import csv
import hashlib
import os
import sys
from datetime import datetime
from pathlib import Path

TIPOS = {
    ".pdf": "PDF", ".docx": "Word", ".doc": "Word", ".xlsx": "Excel", ".xlsm": "Excel (macros)",
    ".xls": "Excel", ".csv": "Datos", ".parquet": "Datos", ".py": "Código", ".sql": "Código",
    ".ipynb": "Notebook", ".pptx": "Presentación", ".msg": "Correo", ".eml": "Correo",
    ".md": "Markdown", ".json": "Config", ".txt": "Texto",
}


def sha256(path: Path, bloque: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(bloque), b""):
            h.update(chunk)
    return h.hexdigest()


def recorrer(rutas):
    for r in rutas:
        p = Path(r)
        if p.is_file():
            yield p
        elif p.is_dir():
            for q in sorted(p.rglob("*")):
                if q.is_file() and not q.name.startswith("~$"):
                    yield q
        else:
            print(f"[AVISO] No existe: {r}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rutas", nargs="+")
    ap.add_argument("--salida", default="evidencias_hash.csv")
    a = ap.parse_args()
    filas = []
    for p in recorrer(a.rutas):
        st = p.stat()
        filas.append({
            "archivo": str(p),
            "tipo": TIPOS.get(p.suffix.lower(), p.suffix.lower() or "sin extensión"),
            "bytes": st.st_size,
            "sha256": sha256(p),
            "fecha_modificacion": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
        })
    if not filas:
        sys.exit("ERROR: no se encontró ningún archivo; no se genera tabla vacía silenciosa.")
    with open(a.salida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    print(f"{len(filas)} evidencias registradas en {a.salida}")
    print("| Archivo | Tipo | SHA-256 |\n|---|---|---|")
    for r in filas:
        print(f"| {os.path.basename(r['archivo'])} | {r['tipo']} | {r['sha256']} |")


if __name__ == "__main__":
    main()
