#!/usr/bin/env python3
"""Reproduce métricas de validación de modelos de riesgo (A7 · VIRF).

Subcomandos:
  credito  --datos val.parquet --y default --score pd [--grado rating] [--base dev.parquet --vars a,b] [--reportadas r.csv]
  var      --datos bt.csv --pnl pnl --var var_99 --nivel 0.99 [--reportadas r.csv]
Salida: CSV con metrica, valor_reproducido, [valor_reportado, umbral, fuente_umbral, estado]
"""
import argparse
import sys

import numpy as np
import pandas as pd
from scipy import stats


def leer(r):
    return pd.read_parquet(r) if r.endswith(".parquet") else pd.read_excel(r) if r.endswith((".xlsx", ".xls")) else pd.read_csv(r, sep=None, engine="python")


# ---------- discriminación ----------
def auc(y, s):
    y, s = np.asarray(y), np.asarray(s, float)
    r = stats.rankdata(s)
    n1, n0 = y.sum(), len(y) - y.sum()
    if n1 == 0 or n0 == 0:
        return np.nan
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def ks(y, s):
    y, s = np.asarray(y), np.asarray(s, float)
    return float(stats.ks_2samp(s[y == 1], s[y == 0]).statistic)


# ---------- estabilidad ----------
def psi(base, actual, bins=10):
    base, actual = pd.Series(base).dropna().astype(float), pd.Series(actual).dropna().astype(float)
    cortes = np.unique(np.quantile(base, np.linspace(0, 1, bins + 1)))
    if len(cortes) < 3:
        return np.nan
    cortes[0], cortes[-1] = -np.inf, np.inf
    b = np.histogram(base, cortes)[0] / len(base)
    a = np.histogram(actual, cortes)[0] / len(actual)
    b, a = np.clip(b, 1e-6, None), np.clip(a, 1e-6, None)
    return float(((a - b) * np.log(a / b)).sum())


# ---------- calibración ----------
def hosmer_lemeshow(y, p, g=10):
    d = pd.DataFrame({"y": y, "p": p}).dropna()
    d["g"] = pd.qcut(d.p.rank(method="first"), g, labels=False)
    t = d.groupby("g").agg(n=("y", "size"), o=("y", "sum"), e=("p", "sum"))
    hl = (((t.o - t.e) ** 2) / (t.e * (1 - t.e / t.n))).sum()
    return float(hl), float(1 - stats.chi2.cdf(hl, g - 2))


def calibracion_por_grado(y, p, grado):
    d = pd.DataFrame({"y": y, "p": p, "g": grado}).dropna()
    filas = []
    for g, t in d.groupby("g"):
        n, k, pd_m = len(t), int(t.y.sum()), float(t.p.mean())
        pval = float(stats.binom.sf(k - 1, n, pd_m)) if n else np.nan  # P(X >= k): subestimación de PD
        lo, hi = stats.beta.ppf([0.025, 0.975], k + 0.5, n - k + 0.5)
        filas.append({"grado": g, "n": n, "defaults": k, "tasa_observada": k / n, "pd_media": pd_m,
                      "binomial_pvalor_cola_sup": pval, "jeffreys_ic95_inf": lo, "jeffreys_ic95_sup": hi,
                      "pd_dentro_jeffreys": lo <= pd_m <= hi})
    return pd.DataFrame(filas)


# ---------- backtesting VaR ----------
def kupiec(x, n, p):
    if x == 0:
        lr = -2 * n * np.log(1 - p)
    elif x == n:
        lr = -2 * n * np.log(p)
    else:
        ph = x / n
        lr = -2 * ((n - x) * np.log(1 - p) + x * np.log(p) - (n - x) * np.log(1 - ph) - x * np.log(ph))
    return float(lr), float(1 - stats.chi2.cdf(lr, 1))


def christoffersen(exc):
    e = np.asarray(exc, int)
    a, b = e[:-1], e[1:]
    n00, n01 = int(((a == 0) & (b == 0)).sum()), int(((a == 0) & (b == 1)).sum())
    n10, n11 = int(((a == 1) & (b == 0)).sum()), int(((a == 1) & (b == 1)).sum())
    p01 = n01 / (n00 + n01) if n00 + n01 else 0
    p11 = n11 / (n10 + n11) if n10 + n11 else 0
    p = (n01 + n11) / max(n00 + n01 + n10 + n11, 1)
    def ll(q, k0, k1):
        return (k0 * np.log(1 - q) if k0 and q < 1 else 0) + (k1 * np.log(q) if k1 and q > 0 else 0)
    lr = -2 * (ll(p, n00 + n10, n01 + n11) - ll(p01, n00, n01) - ll(p11, n10, n11))
    return float(lr), float(1 - stats.chi2.cdf(lr, 1))


def zona_semaforo(x, n):
    # Zonas BCBS para 250 obs al 99 %; para otros n se escala proporcionalmente (anotar)
    f = n / 250
    return "verde" if x <= 4 * f else "amarilla" if x <= 9 * f else "roja"


def comparar(res, reportadas):
    if reportadas is None:
        res["estado"] = "Sin valor reportado para comparar"
        return res
    r = leer(reportadas)
    out = res.merge(r, on="metrica", how="outer")
    def est(row):
        if pd.isna(row.get("valor_reproducido")):
            return "No verificable — no reproducible"
        u, fu = row.get("umbral"), str(row.get("fuente_umbral", ""))
        if pd.isna(u) or not fu or fu.startswith("[SUPUESTO]") or fu == "nan":
            return "No verificable — umbral no declarado"
        u = str(u).strip()
        v = float(row["valor_reproducido"])
        op, num = (u[:2], u[2:]) if u[:2] in (">=", "<=") else (u[:1], u[1:]) if u[:1] in "<>" else (">=", u)
        num = float(num.replace(",", "."))
        ok = {">=": v >= num, "<=": v <= num, ">": v > num, "<": v < num}[op]
        return "Cumple" if ok else "No cumple"
    out["estado"] = out.apply(est, axis=1)
    if "valor_reportado" in out:
        out["diferencia"] = pd.to_numeric(out["valor_reproducido"], errors="coerce") - pd.to_numeric(out["valor_reportado"], errors="coerce")
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="modo", required=True)
    c = sub.add_parser("credito")
    c.add_argument("--datos", required=True); c.add_argument("--y", required=True); c.add_argument("--score", required=True)
    c.add_argument("--grado"); c.add_argument("--base"); c.add_argument("--vars", default="")
    c.add_argument("--reportadas"); c.add_argument("--salida", default="metricas.csv")
    v = sub.add_parser("var")
    v.add_argument("--datos", required=True); v.add_argument("--pnl", required=True); v.add_argument("--var", required=True)
    v.add_argument("--nivel", type=float, default=0.99); v.add_argument("--reportadas"); v.add_argument("--salida", default="metricas.csv")
    a = ap.parse_args()
    d = leer(a.datos)
    if d.empty:
        sys.exit("Insumo vacío.")
    filas = []
    if a.modo == "credito":
        y = pd.to_numeric(d[a.y], errors="coerce"); s = pd.to_numeric(d[a.score], errors="coerce")
        m = y.notna() & s.notna(); y, s = y[m].astype(int), s[m]
        A = auc(y, s)
        filas += [{"metrica": "AUC", "valor_reproducido": A}, {"metrica": "Gini", "valor_reproducido": 2 * A - 1},
                  {"metrica": "KS", "valor_reproducido": ks(y, s)},
                  {"metrica": "Tasa observada", "valor_reproducido": float(y.mean())},
                  {"metrica": "PD media", "valor_reproducido": float(s.mean())},
                  {"metrica": "Brier", "valor_reproducido": float(((s - y) ** 2).mean())}]
        hl, hp = hosmer_lemeshow(y, s)
        filas += [{"metrica": "Hosmer-Lemeshow", "valor_reproducido": hl}, {"metrica": "Hosmer-Lemeshow p-valor", "valor_reproducido": hp}]
        if a.base:
            b = leer(a.base)
            filas.append({"metrica": "PSI score", "valor_reproducido": psi(b[a.score], d[a.score])})
            for x in [z for z in a.vars.split(",") if z]:
                if x in b and x in d:
                    filas.append({"metrica": f"CSI {x}", "valor_reproducido": psi(b[x], d[x])})
        if a.grado:
            cal = calibracion_por_grado(y, s, d.loc[m, a.grado])
            cal.to_csv(a.salida.replace(".csv", "_calibracion_grado.csv"), index=False)
            for r in cal.itertuples():
                filas.append({"metrica": f"Binomial grado {r.grado}", "valor_reproducido": r.binomial_pvalor_cola_sup})
    else:
        pnl = pd.to_numeric(d[a.pnl], errors="coerce"); var = pd.to_numeric(d[a.var], errors="coerce").abs()
        m = pnl.notna() & var.notna(); pnl, var = pnl[m], var[m]
        exc = (pnl < -var).astype(int)
        n, x = len(exc), int(exc.sum()); p = 1 - a.nivel
        lk, pk = kupiec(x, n, p); lc, pc = christoffersen(exc.values)
        filas += [{"metrica": "Observaciones", "valor_reproducido": n}, {"metrica": "Excepciones", "valor_reproducido": x},
                  {"metrica": "Kupiec LR", "valor_reproducido": lk}, {"metrica": "Kupiec p-valor", "valor_reproducido": pk},
                  {"metrica": "Christoffersen LR", "valor_reproducido": lc}, {"metrica": "Christoffersen p-valor", "valor_reproducido": pc},
                  {"metrica": "Zona semáforo (referencial)", "valor_reproducido": np.nan, "nota": zona_semaforo(x, n)}]
    res = comparar(pd.DataFrame(filas), a.reportadas)
    res.to_csv(a.salida, index=False)
    print(res.to_string(index=False))


if __name__ == "__main__":
    main()
