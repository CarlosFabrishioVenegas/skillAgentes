#!/usr/bin/env python3
"""Verifica las 7 condiciones de calidad de entendimiento_<codigo>.md (A1 · VIRF).

Uso:
    python verificar_entendimiento.py entendimiento_MOD-0412.md --codigo MOD-0412
Sale con código 1 si alguna condición falla.
"""
import argparse
import re
import sys

RE_CITA = re.compile(r"p{1,2}\.\s?\d+|línea\s+\d+|No evidenciado|texto proporcionado en sesión", re.I)
RE_HASH = re.compile(r"\b[0-9a-f]{64}\b")
RE_COD = re.compile(r"\b[A-Z]{2,5}-\d{2,6}\b")
NO_CODIGO = {"SHA-256", "SHA-1", "ISO-8601", "UTF-8", "IFRS-9", "BCBS-239", "SR-11"}


def secciones(md):
    partes, actual = {}, "_preambulo"
    for l in md.splitlines():
        m = re.match(r"^##\s+(\d+)\.", l)
        if m:
            actual = m.group(1)
        elif l.startswith("## "):
            actual = l[3:].strip()
        partes.setdefault(actual, []).append(l)
    return partes


def filas_tabla(lineas):
    out = []
    for l in lineas:
        if l.strip().startswith("|") and not re.match(r"^\|\s*-", l.strip()):
            out.append([c.strip() for c in l.strip().strip("|").split("|")])
    return out[1:] if out else []  # sin encabezado


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md")
    ap.add_argument("--codigo", required=True)
    a = ap.parse_args()
    md = open(a.md, encoding="utf-8").read()
    sec = secciones(md)
    res = []

    # 1 citas
    sin_cita = []
    for k in ("1", "2", "5"):
        for f in filas_tabla(sec.get(k, [])):
            if any(f) and not RE_CITA.search(" ".join(f)):
                sin_cita.append(f"sec {k}: {f[0]}")
    res.append(("Toda línea con contenido tiene cita con página", not sin_cita, sin_cita[:5]))

    # 2 supuestos literales
    malos = [l for k in ("6", "7") for l in sec.get(k, [])
             if l.strip().startswith("-") and "No evidenciado" not in l and '"' not in l and "“" not in l]
    res.append(("Supuestos/limitaciones entre comillas", not malos, malos[:5]))

    # 3 columnas completas
    def ncols(k):
        f = [l for l in sec.get(k, []) if l.strip().startswith("|")]
        return {len(l.strip().strip("|").split("|")) for l in f}
    ok3 = len(ncols("2")) <= 1 and len(ncols("5")) <= 1 and ncols("2") and ncols("5")
    res.append(("Tablas de inputs/outputs con todas sus columnas", bool(ok3), [f"sec2={ncols('2')} sec5={ncols('5')}"]))

    # 4 sin celdas vacías
    vacias = [f"sec {k}: {f[0] or '(vacía)'}" for k in ("1", "2", "5")
              for f in filas_tabla(sec.get(k, [])) if any(c == "" for c in f)]
    res.append(("Sin campos vacíos (usar 'No evidenciado')", not vacias, vacias[:5]))

    # 5 hashes
    traz = "\n".join(sec.get("10", []))
    docs = [f for f in filas_tabla(sec.get("10", [])) if f and f[0].lower().endswith((".pdf", ".docx", ".xlsx", ".py", ".sql", ".ipynb"))]
    sin_hash = [d[0] for d in docs if not RE_HASH.search(" ".join(d))]
    res.append(("Cada documento leído con SHA-256", bool(docs) and not sin_hash, sin_hash[:5] or (["no hay documentos listados"] if not docs else [])))

    # 6 consultas numeradas
    f9 = filas_tabla(sec.get("9", []))
    no_num = [f[0] for f in f9 if f and not re.match(r"^\d+$", f[0])]
    res.append(("Consultas abiertas numeradas", not no_num, no_num[:5]))

    # 7 código consistente
    codigos = set(RE_COD.findall(md))
    otros = sorted(c for c in codigos if c != a.codigo and c not in NO_CODIGO)
    res.append(("Código del modelo idéntico en todo el documento", a.codigo in md and not otros, otros[:5]))

    ok = sum(r[1] for r in res)
    for i, (n, b, det) in enumerate(res, 1):
        print(f"[{'OK' if b else 'FALLA'}] {i}. {n}" + ("" if b else f" -> {det}"))
    nev = md.count("No evidenciado")
    print(f"\nResultado: {ok}/7 · menciones 'No evidenciado': {nev}")
    sys.exit(0 if ok == 7 else 1)


if __name__ == "__main__":
    main()
