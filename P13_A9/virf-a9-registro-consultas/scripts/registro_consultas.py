#!/usr/bin/env python3
"""Registro centralizado de consultas al equipo dueño (A9 · VIRF).

Subcomandos: agregar | responder | vencer | verificar | tabla  (ver SKILL.md)
"""
import argparse
import csv
import re
import sys
import unicodedata
from datetime import date, timedelta
from pathlib import Path

CAMPOS = ["numero", "control_origen", "pregunta", "evidencia", "destinatario", "fecha_envio", "plazo",
          "estado", "respuesta", "fuente_respuesta", "efecto_no_respuesta"]


def norm(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()


def leer(r):
    p = Path(r)
    return list(csv.DictReader(open(p, encoding="utf-8"))) if p.exists() else []


def guardar(r, filas):
    with open(r, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS); w.writeheader(); w.writerows(filas)


def habiles(desde, n):
    d = desde
    while n > 0:
        d += timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("agregar")
    for c in ("registro", "origen", "destinatario", "pregunta", "evidencia", "efecto"):
        g.add_argument(f"--{c}", required=True)
    g.add_argument("--plazo-dias", type=int, default=5)
    g.add_argument("--fecha", default=date.today().isoformat())
    r = sub.add_parser("responder")
    r.add_argument("--registro", required=True); r.add_argument("--numero", required=True)
    r.add_argument("--respuesta", required=True); r.add_argument("--fuente", required=True)
    v = sub.add_parser("vencer")
    v.add_argument("--registro", required=True); v.add_argument("--hoy", default=date.today().isoformat())
    ve = sub.add_parser("verificar")
    ve.add_argument("--registro", required=True); ve.add_argument("--texto", required=True); ve.add_argument("--expediente", default=None)
    t = sub.add_parser("tabla")
    t.add_argument("--registro", required=True)
    a = ap.parse_args()
    filas = leer(a.registro)

    if a.cmd == "agregar":
        p = a.pregunta.strip()
        if not p.endswith("?") and "?" not in p:
            sys.exit("La pregunta debe ser respondible (sí/no/dato) y terminar en '?'.")
        if len(re.findall(r"\?", p)) > 1:
            print("[AVISO] La consulta contiene más de una pregunta: dividirla.")
        n = max([int(f["numero"]) for f in filas] or [0]) + 1
        f0 = date.fromisoformat(a.fecha)
        filas.append({"numero": n, "control_origen": a.origen, "pregunta": p, "evidencia": a.evidencia,
                      "destinatario": a.destinatario, "fecha_envio": f0.isoformat(), "plazo": habiles(f0, a.plazo_dias).isoformat(),
                      "estado": "enviada", "respuesta": "", "fuente_respuesta": "", "efecto_no_respuesta": a.efecto})
        guardar(a.registro, filas); print(f"Consulta {n:02d} registrada (vence {filas[-1]['plazo']}).")
    elif a.cmd == "responder":
        for f in filas:
            if str(f["numero"]) == str(int(a.numero)):
                if "verbal" in norm(a.fuente) or "reunion" in norm(a.fuente):
                    print("[AVISO] Respuesta verbal: solicitar confirmación por correo y citar el correo.")
                f.update(estado="respondida", respuesta=a.respuesta, fuente_respuesta=a.fuente)
        guardar(a.registro, filas); print("Actualizado.")
    elif a.cmd == "vencer":
        hoy = date.fromisoformat(a.hoy); n = 0
        for f in filas:
            if f["estado"] == "enviada" and date.fromisoformat(f["plazo"]) < hoy:
                f["estado"] = "sin respuesta"; n += 1
        guardar(a.registro, filas); print(f"{n} consultas pasan a 'sin respuesta' → campos 'No verificable' + riesgo de gobierno.")
    elif a.cmd == "verificar":
        terms = [w for w in re.findall(r"\w{5,}", norm(a.texto))]
        hits = [f for f in filas if sum(w in norm(f["pregunta"]) for w in terms) >= max(1, len(terms) // 2)]
        for f in hits:
            print(f"Registro · consulta {f['numero']} [{f['estado']}]: {f['pregunta'][:120]} → {f['respuesta'][:80]}")
        if a.expediente:
            for p in Path(a.expediente).rglob("*"):
                if p.suffix.lower() in (".md", ".txt", ".csv") and p.is_file():
                    txt = norm(p.read_text(errors="replace"))
                    k = sum(w in txt for w in terms)
                    if k >= max(1, len(terms) // 2):
                        print(f"Expediente · {p} ({k}/{len(terms)} términos)")
        if not hits:
            print("Sin coincidencias en el registro.")
    else:
        print("| N° | Origen | Pregunta | Evidencia | Destinatario | Envío | Plazo | Estado | Efecto de la no respuesta |")
        print("|---|---|---|---|---|---|---|---|---|")
        for f in filas:
            print(f"| {int(f['numero']):02d} | {f['control_origen']} | {f['pregunta']} | {f['evidencia']} | {f['destinatario']} | "
                  f"{f['fecha_envio']} | {f['plazo']} | {f['estado']} | {f['efecto_no_respuesta']} |")


if __name__ == "__main__":
    main()
