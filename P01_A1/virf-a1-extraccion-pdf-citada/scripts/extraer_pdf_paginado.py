#!/usr/bin/env python3
"""Extrae un PDF página a página a JSONL citable (A1 · VIRF).

Uso:
    python extraer_pdf_paginado.py manual.pdf --salida corpus/manual.jsonl [--desde 1 --hasta 50]

Requiere pdfplumber (pip install pdfplumber). No modifica el PDF.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    sys.exit("Falta pdfplumber: pip install pdfplumber")

RE_TITULO = re.compile(r"^\s*((\d+(\.\d+){0,3})\.?\s+[A-ZÁÉÍÓÚÑ][^\n]{2,90})$")
RE_NUM_PAG = re.compile(r"(?:^|\s)(?:p[aá]g(?:ina)?\.?\s*)?(\d{1,4})(?:\s*(?:de|/)\s*\d{1,4})?\s*$", re.I)


def pagina_impresa(texto: str):
    lineas = [l.strip() for l in texto.strip().splitlines() if l.strip()]
    for cand in (lineas[-1:] + lineas[:1]):
        m = RE_NUM_PAG.search(cand)
        if m and len(cand) <= 25:
            return int(m.group(1))
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--salida", required=True)
    ap.add_argument("--desde", type=int, default=1)
    ap.add_argument("--hasta", type=int, default=None)
    a = ap.parse_args()

    ruta = Path(a.pdf)
    sha = hashlib.sha256(ruta.read_bytes()).hexdigest()
    Path(a.salida).parent.mkdir(parents=True, exist_ok=True)
    seccion = "(sin sección detectada)"
    n_ocr = n_tot = 0
    with pdfplumber.open(ruta) as pdf, open(a.salida, "w", encoding="utf-8") as out:
        total = len(pdf.pages)
        hasta = min(a.hasta or total, total)
        for i in range(a.desde - 1, hasta):
            pg = pdf.pages[i]
            texto = pg.extract_text() or ""
            for linea in texto.splitlines():
                m = RE_TITULO.match(linea)
                if m:
                    seccion = m.group(1).strip()
            tablas = []
            try:
                tablas = pg.extract_tables() or []
            except Exception as e:  # tabla ilegible: se reporta, no se oculta
                tablas = [[["ERROR_EXTRACCION_TABLA", str(e)]]]
            requiere_ocr = len(texto.strip()) < 30 and len(pg.images) > 0
            n_ocr += requiere_ocr
            n_tot += 1
            out.write(json.dumps({
                "archivo": ruta.name,
                "sha256": sha,
                "pagina_fisica": i + 1,
                "pagina_impresa": pagina_impresa(texto),
                "encabezado_seccion": seccion,
                "n_caracteres": len(texto),
                "requiere_ocr": requiere_ocr,
                "texto": texto,
                "tablas": tablas,
            }, ensure_ascii=False) + "\n")
    print(f"{ruta.name}: páginas {a.desde}-{hasta} de {total} | sha256={sha}")
    if n_tot and n_ocr == n_tot:
        print("PDF no extraíble — requiere OCR")
        sys.exit(2)
    if n_ocr:
        print(f"[AVISO] {n_ocr} páginas sin capa de texto (requieren OCR)")
    if hasta < total:
        print(f"[COBERTURA PARCIAL] leídas {hasta - a.desde + 1} de {total} páginas: registrar en sección 10")


if __name__ == "__main__":
    main()
