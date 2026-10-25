#!/usr/bin/env python3
"""Lector tolerante de Estandares_VIRF.xlsx: filtra actividades por tier y periodicidad.

Uso:
    python filtrar_estandar_virf.py Estandares_VIRF.xlsx --tier 2 [--periodicidad periodica] --salida actividades.csv

Principio: el parser se adapta al estándar. Detecta hojas, encabezados por contenido,
alias de columnas y celdas combinadas. No corrige erratas del contenido.
"""
import argparse
import re
import sys
import unicodedata

import pandas as pd

ALIAS = {
    "id_virf": ["id", "codigo", "cod", "n°", "nro", "numero", "id actividad", "id virf", "item"],
    "ambito": ["ambito", "dimension", "control", "pilar", "componente", "seccion"],
    "actividad": ["actividad", "descripcion", "prueba", "requisito", "criterio", "actividades"],
    "tier": ["tier", "nivel", "criticidad", "tiering", "aplica a tier"],
    "periodicidad": ["periodicidad", "tipo de validacion", "frecuencia", "tipo validacion", "tipo"],
}
MAPA_CONTROL = {
    "C1": ["documenta"], "C2": ["dato", "calidad"], "C3": ["metodolog"],
    "C4": ["implementa"], "C5": ["gobierno", "gobernanza"], "C6": ["uso"],
}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower().strip()
    return re.sub(r"\s+", " ", s)


def campo_de(encabezado):
    e = norm(encabezado)
    for campo, alias in ALIAS.items():
        if e in alias or any(e.startswith(a) for a in alias):
            return campo
    return None


def fila_encabezado(raw):
    mejor, idx = 0, None
    for i in range(min(30, len(raw))):
        campos = {campo_de(v) for v in raw.iloc[i].tolist() if pd.notna(v)} - {None}
        if len(campos) > mejor:
            mejor, idx = len(campos), i
    return idx if mejor >= 2 else None


def tier_num(v):
    t = norm(v)
    if not t or t == "nan":
        return set()
    if "todos" in t or "all" in t:
        return {1, 2, 3}
    nums = {int(x) for x in re.findall(r"[1-3]", t)}
    if not nums:
        nums = {1} if "alto" in t else {2} if "medio" in t else {3} if "bajo" in t else set()
    if re.search(r"[1-3]\s*(a|-|–)\s*[1-3]", t):
        a, b = map(int, re.findall(r"[1-3]", t)[:2]); nums = set(range(min(a, b), max(a, b) + 1))
    return nums


def control_de(ambito):
    a = norm(ambito)
    m = re.search(r"\bc\s?([1-6])\b", a)
    if m:
        return f"C{m.group(1)}"
    for c, claves in MAPA_CONTROL.items():
        if any(k in a for k in claves):
            return c
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx")
    ap.add_argument("--tier", type=int, required=True, choices=[1, 2, 3])
    ap.add_argument("--periodicidad", default=None, help="texto a buscar, p. ej. 'periodica' o 'primera'")
    ap.add_argument("--salida", default="actividades_tier.csv")
    a = ap.parse_args()

    libro = pd.read_excel(a.xlsx, sheet_name=None, header=None, dtype=object)
    filas, diagnostico = [], []
    for hoja, raw in libro.items():
        h = fila_encabezado(raw)
        if h is None:
            diagnostico.append(f"[{hoja}] sin encabezado reconocible; encabezados vistos: {raw.head(3).values.tolist()}")
            continue
        enc = raw.iloc[h].tolist()
        cols = {}
        tier_cols = {}
        for j, v in enumerate(enc):
            c = campo_de(v) if pd.notna(v) else None
            if c and c not in cols:
                cols[c] = j
            m = re.fullmatch(r"t(ier)?\s?([1-3])", norm(v)) if pd.notna(v) else None
            if m:
                tier_cols[int(m.group(2))] = j
        cuerpo = raw.iloc[h + 1:].copy()
        for c in ("ambito", "id_virf"):
            if c in cols:
                cuerpo.iloc[:, cols[c]] = cuerpo.iloc[:, cols[c]].ffill()
        for i, r in cuerpo.iterrows():
            act = r.iloc[cols["actividad"]] if "actividad" in cols else None
            if pd.isna(act) or not str(act).strip():
                continue
            if tier_cols:
                tiers = {t for t, j in tier_cols.items() if pd.notna(r.iloc[j]) and norm(r.iloc[j]) not in ("", "no", "n/a", "-", "0")}
            elif "tier" in cols:
                tiers = tier_num(r.iloc[cols["tier"]])
            else:
                tiers = {1, 2, 3}
            per = r.iloc[cols["periodicidad"]] if "periodicidad" in cols else ""
            if a.tier not in tiers:
                continue
            if a.periodicidad and norm(a.periodicidad) not in norm(per) and norm(per) not in ("", "nan", "ambas", "todas"):
                continue
            amb = r.iloc[cols["ambito"]] if "ambito" in cols else hoja
            filas.append({"id_virf": r.iloc[cols["id_virf"]] if "id_virf" in cols else f"{hoja}-{i+1}",
                          "control": control_de(amb) or control_de(hoja), "ambito": amb, "actividad": str(act).strip(),
                          "tier": ",".join(map(str, sorted(tiers))), "periodicidad": per if pd.notna(per) else "",
                          "hoja": hoja, "fila_excel": i + 1})
    for d in diagnostico:
        print(d, file=sys.stderr)
    if not filas:
        sys.exit("ERROR: ninguna actividad mapeada. Revisar ALIAS frente a los encabezados listados arriba.")
    df = pd.DataFrame(filas)
    df.to_csv(a.salida, index=False, encoding="utf-8")
    print(f"{len(df)} actividades aplicables a Tier {a.tier} -> {a.salida}")
    print(df.groupby("control", dropna=False).size().to_string())
    sin_control = (df["control"] == "").sum()
    if sin_control:
        print(f"[AVISO] {sin_control} actividades sin control C1–C6 asignable: revisar MAPA_CONTROL")


if __name__ == "__main__":
    main()
