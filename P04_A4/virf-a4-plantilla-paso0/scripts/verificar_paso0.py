#!/usr/bin/env python3
"""Verifica la estructura de A4_paso0.md (VIRF · Paso 0).

Uso: python verificar_paso0.py A4_paso0.md
"""
import re
import sys

SECCIONES = list(range(0, 18))
ESTADOS_ADM = ["Python que corre sin errores", "Python con errores", "Excel con .md generado",
               "Excel sin .md", "No entregada"]


def main():
    md = open(sys.argv[1], encoding="utf-8").read()
    lineas = md.splitlines()
    presentes = {int(m.group(1)) for m in re.finditer(r"^##\s+(\d{1,2})\.", md, re.M)}
    faltan = [s for s in SECCIONES if s not in presentes]
    celdas = ev = 0
    for l in lineas:
        t = l.strip()
        if t.startswith("|") and not re.match(r"^\|\s*[-:]", t):
            cs = [c.strip() for c in t.strip("|").split("|")]
            if len(cs) > 1:
                for c in cs[1:]:
                    celdas += 1
                    ev += bool(c) and "No evidenciado" not in c
    # descontar encabezados aproximadamente: filas cuya fila siguiente es separador
    enc = 0
    for i, l in enumerate(lineas[:-1]):
        if l.strip().startswith("|") and re.match(r"^\|\s*[-:]", lineas[i + 1].strip()):
            n = len(l.strip().strip("|").split("|")) - 1
            enc += n
    celdas -= enc; ev -= enc
    pct = 100 * ev / celdas if celdas > 0 else 0
    adm = [e for e in ESTADOS_ADM if e.lower() in md.lower()]
    rotulo = lineas[0].strip().lower().startswith("entendimiento parcial") if lineas else False
    print(f"Secciones presentes: {len(presentes & set(SECCIONES))}/18" + (f" · faltan: {faltan}" if faltan else ""))
    print(f"Completitud aproximada (celdas de tablas): {pct:.1f} % ({ev}/{celdas})")
    print(f"Menciones 'No evidenciado': {md.count('No evidenciado')}")
    print(f"Estado de admisibilidad declarado: {adm or 'NO DECLARADO'}")
    ok = not faltan and len(adm) >= 1
    if pct < 80 and not rotulo:
        print("FALLA: completitud < 80 % y la primera línea no dice 'Entendimiento parcial (X % evidenciado)'")
        ok = False
    if "Brechas de evidencia" not in md:
        print("FALLA: falta '## Brechas de evidencia'"); ok = False
    print("RESULTADO:", "OK" if ok else "CORREGIR")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
