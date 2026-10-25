#!/usr/bin/env python3
"""Recalcula el tier de un modelo con criterios configurables (A9 · VIRF).

Uso:
    python recalcular_tiering.py criterios.json --exposicion_mm 640 --criticidad_regulatoria capital_o_provision \
        --complejidad media --alcance_uso decision_institucional --tier_acta 2 [--tier_consumidor 1]
Cualquier criterio del JSON se pasa como --<nombre> <valor>.
"""
import argparse
import json
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("criterios")
    ap.add_argument("--tier_acta", type=int, required=True)
    ap.add_argument("--tier_consumidor", type=int, default=None)
    conocidos, resto = ap.parse_known_args()
    cfg = json.load(open(conocidos.criterios, encoding="utf-8"))
    valores = {resto[i].lstrip("-"): resto[i + 1] for i in range(0, len(resto) - 1, 2)}
    fuente = cfg.get("fuente") or "[SUPUESTO] criterios no entregados"
    total, filas, faltan = 0.0, [], []
    for nombre, c in cfg["criterios"].items():
        if nombre not in valores:
            faltan.append(nombre); continue
        v = valores[nombre]
        if "cortes" in c:
            x = float(v)
            idx = sum(x > k for k in c["cortes"])
            p = c["puntajes"][idx]
        else:
            if v not in c["mapa"]:
                sys.exit(f"Valor '{v}' no válido para {nombre}; opciones: {list(c['mapa'])}")
            p = c["mapa"][v]
        total += p * c["peso"]
        filas.append((nombre, v, p, c["peso"]))
    if faltan:
        print(f"[AVISO] Criterios sin valor evidenciado: {faltan} → tier No verificable")
    tier_calc = next(t for umbral, t in cfg["tier_por_puntaje"] if total >= umbral)
    tier_final = min(tier_calc, conocidos.tier_consumidor) if conocidos.tier_consumidor else tier_calc
    print(f"Fuente de criterios: {fuente}")
    print("| Criterio | Valor | Puntaje | Peso |\n|---|---|---|---|")
    for f in filas:
        print(f"| {f[0]} | {f[1]} | {f[2]} | {f[3]} |")
    print(f"\nPuntaje total: {total:.3f} → Tier calculado: {tier_calc}")
    if conocidos.tier_consumidor:
        print(f"Propagación por modelo consumidor Tier {conocidos.tier_consumidor} → Tier efectivo: {tier_final}")
    if faltan or fuente.startswith("[SUPUESTO]"):
        estado = "No verificable"
    else:
        estado = "Cumple" if tier_final == conocidos.tier_acta else "No cumple — tiering desactualizado"
    print(f"Tier del acta (G03): {conocidos.tier_acta} → Estado: {estado}")
    if tier_final < conocidos.tier_acta:
        print("Efecto: actividades exigibles al tier más exigente no incluidas en el alcance → 'No evidenciado' en A11.")


if __name__ == "__main__":
    main()
