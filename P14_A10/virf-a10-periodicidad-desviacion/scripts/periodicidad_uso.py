#!/usr/bin/env python3
"""Cumplimiento de periodicidad de uso y días de desviación (A10 · VIRF).

Uso:
    python periodicidad_uso.py evidencias_uso.csv --periodicidad trimestral --desde 2025-10-01 --hasta 2026-09-30 \
        --plazo-dias 10 [--tipo envio] [--plazo-supuesto] --salida periodicidad.md
"""
import argparse
import sys

import pandas as pd

FREQ = {"mensual": "M", "trimestral": "Q", "semestral": "2Q", "anual": "Y"}


def periodos(desde, hasta, per):
    if per == "semestral":
        ps = pd.period_range(desde, hasta, freq="Q")
        return [p for p in ps if p.quarter in (2, 4)], "Q"
    f = {"mensual": "M", "trimestral": "Q", "anual": "Y"}[per]
    return list(pd.period_range(desde, hasta, freq=f)), f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--periodicidad", required=True, choices=list(FREQ))
    ap.add_argument("--desde", required=True)
    ap.add_argument("--hasta", required=True)
    ap.add_argument("--plazo-dias", type=int, default=10)
    ap.add_argument("--plazo-supuesto", action="store_true", help="rotula el plazo como [SUPUESTO]")
    ap.add_argument("--tipo", default="envio")
    ap.add_argument("--salida", default="periodicidad.md")
    a = ap.parse_args()
    ev = pd.read_csv(a.csv, parse_dates=["fecha"])
    ev = ev[ev["tipo"].str.lower() == a.tipo.lower()]
    if ev.empty:
        print(f"[AVISO] No hay evidencias de tipo '{a.tipo}': todos los periodos quedan sin uso.")
    ps, f = periodos(a.desde, a.hasta, a.periodicidad)
    filas = []
    for out in sorted(set(ev["output"])) or ["(sin output con evidencia)"]:
        e = ev[ev["output"] == out].sort_values("fecha")
        prev_fin = None
        for p in ps:
            ini = (prev_fin + pd.Timedelta(days=1)) if prev_fin is not None else p.start_time
            fin = p.end_time.normalize()
            limite = fin + pd.Timedelta(days=a.plazo_dias)
            sig_limite = limite + (pd.Timedelta(days=(fin - ini).days + 1))
            cand = e[(e.fecha > fin) & (e.fecha <= sig_limite)]
            if cand.empty:
                filas.append([out, str(p), limite.date(), "—", "—", "—", "Sin uso en el periodo"])
            else:
                r = cand.iloc[0]
                dias = (r.fecha.normalize() - limite).days
                filas.append([out, str(p), limite.date(), r.cita, r.fecha.date(), dias, "En plazo" if dias <= 0 else "Tardío"])
            prev_fin = fin
    md = [f"Periodicidad comprometida: {a.periodicidad} · plazo: {a.plazo_dias} días tras cierre"
          + (" [SUPUESTO]" if a.plazo_supuesto else "") + f" · tipo de evidencia: {a.tipo}", "",
          "| Output | Periodo | Fecha límite | Evidencia | Fecha | Días de desviación | Estado |", "|---|---|---|---|---|---|---|"]
    md += ["| " + " | ".join(map(str, x)) + " |" for x in filas]
    df = pd.DataFrame(filas, columns=["o", "p", "l", "e", "f", "d", "s"])
    tard = df[df.s == "Tardío"]
    md += ["", f"**Periodos evaluados:** {len(df)} · **en plazo:** {(df.s=='En plazo').sum()} · "
           f"**tardíos:** {len(tard)}" + (f" (máx. {int(tard.d.max())} días)" if len(tard) else "") +
           f" · **sin uso:** {(df.s=='Sin uso en el periodo').sum()}"]
    open(a.salida, "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
