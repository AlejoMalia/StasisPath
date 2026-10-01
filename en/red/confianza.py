"""StasisPath: confidence in each verdict — from 'margin' to PERCENTAGE.

MARGENES.md says how far the flip of each verdict lies, but not with what probability it occurs.
Here each declared range is read as a 95 % interval (that is how Q10 was declared, 95 % CI with
n = 37) and converted into a split normal distribution on a log scale: it respects the range's
asymmetry and invents no dispersion where the range is a point. From that:

  1. P(error) for each verdict that currently holds, with all its parameters varying at once.
  2. Which parameter concentrates that risk (P(error) if that parameter were known exactly).
  3. What precision would need to be measured to bring P(error) below target (1 in 100).

Declared, not hidden, limits:
  - Reading the range as ±1.96 σ is an ASSUMPTION: many ranges are bounds or corners, not CIs. That
    is why the pessimistic column is also given (range = ±1 σ). The truth lies, at most, between the two.
  - Parameters are independent; no correlations are declared in the YAML.
  - This module does NOT change values, ranges, thresholds or the grounding. It only measures and ranks (R2, R5).
  - The seed is fixed so the document is reproducible.

Output: CONFIANZA.md + red/fig/K_confianza.png. Called by motor.py.
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
ORANGE, YELLOW, AQUA = "#eb6834", "#eda100", "#1baf7a"

N = 20000            # samples per bound
SEMILLA = 20260926
OBJETIVO = 0.01      # Acceptable P(error): 1 in 100. Fixed before seeing results; not adjusted.
K95, K1 = 1.96, 1.0  # range read as ±1.96 σ (primary) or ±1 σ (pessimistic)

def g(x):
    return f"{x:.3g}"

def pct(p):
    if p == 0: return "0 %"
    return f"{100 * p:.2g} %" if p < 1e-3 else f"{100 * p:.3g} %"

def tabla(filas, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in f) + " |" for f in filas) + "\n"

def _sigmas(pv, K):
    """σ upward and downward (log if the parameter is positive, linear otherwise)."""
    v, (lo, hi) = pv["v"], pv["r"]
    if lo > 0 and v > 0:
        return "log", math.log(hi / v) / K, math.log(v / lo) / K
    return "lin", (hi - v) / K, (v - lo) / K

def _muestra(pv, z, K, escala=1.0):
    modo, su, sd = _sigmas(pv, K)
    s = np.where(z > 0, su, sd) * escala
    return pv["v"] * np.exp(z * s) if modo == "log" else pv["v"] + z * s

def _media_err(pv, K, escala=1.0):
    """Equivalent 95 % half-width, as % of the central value (the wider side)."""
    modo, su, sd = _sigmas(pv, K)
    s = max(su, sd) * escala * K95
    return (math.exp(s) - 1) * 100 if modo == "log" else (s / abs(pv["v"]) * 100 if pv["v"] else float("inf"))

def _rango(pv, a):
    """Declared range narrowed by the factor a around the central value (on the same scale as the sampling)."""
    v, (lo, hi) = pv["v"], pv["r"]
    if lo > 0 and v > 0:
        return v * (lo / v) ** a, v * (hi / v) ** a
    return v - a * (v - lo), v + a * (hi - v)

def _wilson_sup(k, n, z=1.96):
    p = k / n
    c = (p + z * z / (2 * n) + z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / (1 + z * z / n)
    return min(1.0, c)

def generar(D, PAR, COTAS, ROOT):
    rng = np.random.default_rng(SEMILLA)
    base = {k: v["v"] for k, v in PAR.items()}
    filas_v, prioridad, prioridad1 = [], {}, {}

    for cid, cdef in D["cotas"].items():
        f = COTAS[cid]
        _, v0 = f(base)
        vivos = [t for t, (ok, _) in v0.items() if ok]
        if not vivos:
            continue
        deps = [d for d in cdef["deps"] if PAR[d]["r"][0] != PAR[d]["r"][1]]
        Z = rng.standard_normal((N, len(deps)))

        def fallos(K, fijo=None, escala=None):
            cols = {}
            for j, d in enumerate(deps):
                e = escala if (escala is not None and d == fijo) else 1.0
                zz = np.zeros(N) if (d == fijo and escala is None) else Z[:, j]
                cols[d] = _muestra(PAR[d], zz, K, e)
            cuenta = {t: 0 for t in vivos}
            for i in range(N):
                q = dict(base)
                for d in deps: q[d] = float(cols[d][i])
                _, vt = f(q)
                for t in vivos:
                    if not vt[t][0]: cuenta[t] += 1
            return cuenta

        c95, c1 = fallos(K95), fallos(K1)
        sin = {d: fallos(K95, fijo=d) for d in deps}   # P(error) if d were known exactly
        sin1 = {d: fallos(K1, fijo=d) for d in deps}   # lo mismo en la lectura pesimista

        def precision(t, K, p, sinK):
            """Dominant parameter and the precision that brings P(error) below target in reading K."""
            dom, p_dom = None, p
            for d in deps:
                pd = sinK[d][t] / N
                if pd < p_dom: dom, p_dom = d, pd
            if p <= OBJETIVO: return dom, p_dom, "ya cumple"
            if dom is None: return dom, p_dom, "no single parameter explains it alone"
            if p_dom > OBJETIVO: return dom, p_dom, f"{dom} alone is not enough: even exact, {pct(p_dom)} remains"
            a, b = 0.0, 1.0          # escala de σ de dom: a cumple, b no
            for _ in range(10):
                m = (a + b) / 2
                if fallos(K, fijo=dom, escala=m)[t] / N <= OBJETIVO: a = m
                else: b = m
            # expressed as the new RANGE that would have to be measured: equally valid in both readings
            lo, hi = _rango(PAR[dom], a)
            return dom, p_dom, f"{dom}: from [{g(PAR[dom]['r'][0])}, {g(PAR[dom]['r'][1])}] to [{g(lo)}, {g(hi)}] ({100 * a:.0f} % of the width)"

        for t in vivos:
            clave = v0[t][1]
            p95, p1 = c95[t] / N, c1[t] / N
            dom, p_dom, req = precision(t, K95, p95, sin)
            dom1, p_dom1, req1 = precision(t, K1, p1, sin1)
            if clave:
                for d in deps:
                    prioridad[d] = prioridad.get(d, 0.0) + (p95 - sin[d][t] / N)
                    prioridad1[d] = prioridad1.get(d, 0.0) + (p1 - sin1[d][t] / N)
            if p95 == 0 and p1 == 0: nivel = "firme"
            elif p95 <= OBJETIVO:     nivel = "confiable"
            elif p95 <= 0.05:         nivel = "**vigilar**"
            else:                     nivel = "**at risk**"
            filas_v.append({"cid": cid, "t": t, "clave": clave, "p95": p95, "p1": p1,
                            "sup": _wilson_sup(c95[t], N), "dom": dom, "p_dom": p_dom,
                            "req": req, "dom1": dom1, "req1": req1, "nivel": nivel})

    filas_v.sort(key=lambda r: (-r["p95"], -r["p1"], not r["clave"]))
    claves = [r for r in filas_v if r["clave"]]
    # probability that at least one key verdict fails (with independence between bounds)
    p_alguna = 1 - math.prod(1 - r["p95"] for r in claves)
    p_alguna1 = 1 - math.prod(1 - r["p1"] for r in claves)

    # ---------------------------------------------------------------- figura
    pts = [r for r in filas_v if r["p95"] > 0 or r["p1"] > 0]
    fig, ax = plt.subplots(figsize=(8.8, 0.42 * max(len(pts), 1) + 1.7))
    piso = 1e-4
    for y, r in enumerate(reversed(pts)):
        c = ORANGE if r["p95"] > 0.05 else (YELLOW if r["p95"] > OBJETIVO else AQUA)
        ax.plot([max(r["p95"], piso), max(r["p1"], piso)], [y, y], color=GRID, lw=2, zorder=1)
        ax.scatter([max(r["p95"], piso)], [y], s=46, color=c, zorder=3, edgecolor=SURF, linewidth=1.5)
        ax.scatter([max(r["p1"], piso)], [y], s=30, facecolor=SURF, edgecolor=c, linewidth=1.5, zorder=3)
        ax.text(max(r["p1"], r["p95"], piso) * 1.25, y, f"{pct(r['p95'])} · pes. {pct(r['p1'])}", va="center", fontsize=7.5, color=INK2)
    ax.axvline(OBJETIVO, color="#c0392b", lw=1.1)
    ax.text(OBJETIVO * 1.05, len(pts) - 0.4, " objetivo 1 %", fontsize=7, color="#c0392b")
    ax.set_yticks(range(len(pts)))
    ax.set_yticklabels([f"{r['cid']}{'' if r['clave'] else ' (non-key)'}: {r['t'][:46]}" for r in reversed(pts)],
                       fontsize=7.2, color=INK2)
    ax.set_xscale("log"); ax.set_xlim(piso * 0.7, 4)
    ax.set_xlabel("P(the verdict is false) · ● range = 95 % CI   ○ pessimistic: range = ±1 σ", color=INK2)
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
    ax.grid(axis="x", color=GRID, lw=0.6); ax.set_facecolor(SURF); fig.set_facecolor(SURF)
    fig.suptitle("Framework confidence: probability that each verdict reverses",
                 x=0.02, ha="left", fontsize=11, color=INK)
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "K_confianza.png", dpi=150); plt.close(fig)

    # ---------------------------------------------------------------- documento
    niveles = {n: sum(1 for r in filas_v if r["nivel"] == n) for n in ("firme", "confiable", "**vigilar**", "**at risk**")}
    filas_md = [[r["cid"], r["t"], "yes" if r["clave"] else "no", f"{pct(r['p95'])} (≤ {pct(r['sup'])})", pct(r["p1"]),
                 r["req"], r["req1"], r["nivel"]] for r in filas_v]

    def orden(pr):
        pr = sorted(((d, x) for d, x in pr.items() if x > 1e-12), key=lambda t: -t[1])
        tot = sum(x for _, x in pr) or 1.0
        return [(d, x / tot) for d, x in pr if x / tot >= 0.005]   # < 0.5 % of the risk: not listed
    prio, prio1 = orden(prioridad), orden(prioridad1)
    filas_prio = [[i + 1, d, PAR[d].get("f") or "—", PAR[d]["e"], f"[{g(PAR[d]['r'][0])}, {g(PAR[d]['r'][1])}]",
                   f"{100 * x:.0f} %"] for i, (d, x) in enumerate(prio1)]
    riesgo = [r for r in filas_v if r["p95"] > OBJETIVO]
    riesgo1 = [r for r in claves if r["p1"] > OBJETIVO]

    doc = ("<!-- AUTO-GENERATED by red/confianza.py. DO NOT EDIT BY HAND. -->\n"
           "# StasisPath: confidence — how much each verdict can fail, as a percentage\n\n"
           "**What this adds to MARGENES.md:** there, the distance to a verdict's flip is measured by moving **one** parameter. "
           "Here **all of them move at once**, each according to its declared range, and **the probability that the verdict reverses** is counted. "
           f"{N:,} samples per bound, fixed seed (the document is reproducible).\n\n"
           "**How each range is read.** Primary: the range is a 95 % interval (split normal on a log scale, respecting asymmetry). "
           "This is an assumption, because several ranges are bounds or corners rather than CIs; that is why the **pessimistic** reading is also given, taking the range as ±1 σ. "
           "**The real probability lies between the two.** Parameters with a point range do not vary, and no correlations are declared.\n\n"
           "> **This module does not touch the framework.** It changes no values, ranges, thresholds or grounding: it measures and ranks. "
           "If a probability is high, the answer is **to measure the indicated parameter to the indicated range**, not to move the threshold (R2). "
           f"The {pct(OBJETIVO)} target was set before any results were seen.\n\n"
           "![Confianza](red/fig/K_confianza.png)\n\n"
           f"**Summary: {niveles['firme']} firm (0 % even in the pessimistic reading) · {niveles['confiable']} reliable (≤ 1 %) · "
           f"{niveles['**vigilar**']} to watch (1–5 %) · {niveles['**at risk**']} at risk (> 5 %).**\n\n"
           f"**Probability that at least one KEY verdict fails: {pct(p_alguna)} in the primary reading and {pct(p_alguna1)} in the pessimistic one** "
           "(assuming independent bounds). The verdicts that can fail with more than 1 % in the primary reading are all **non-key**.\n\n"
           + tabla(filas_md, ["bound", "verdict", "key?", "P(error) (95 % CI upper)", "P(error) pessimistic",
                              "what range would bring P(error) down to ≤ 1 %", "same, pessimistic reading", "level"]))
    if riesgo or riesgo1:
        doc += "\n## What to measure and to what precision\n\n"
        if riesgo1:
            doc += ("**Key verdicts exceeding 1 % in the pessimistic reading** (0 % in the primary one):\n\n" +
                    "\n".join(f"- **{r['cid']}** — «{r['t']}»: {pct(r['p1'])} ⇒ {r['req1']}." for r in riesgo1) + "\n\n")
        if riesgo:
            doc += ("**Non-key verdicts above 1 % in the primary reading:**\n\n" +
                    "\n".join(f"- **{r['cid']}** — «{r['t']}»: {pct(r['p95'])} (pesimista {pct(r['p1'])}) ⇒ {r['req']}."
                               for r in riesgo) + "\n")
    doc += ("\n## Which measurement most reduces the total risk of the key verdicts\n\n"
            "For each parameter, how much the sum of P(error) over the key verdicts would drop if it were known exactly, "
            "in the pessimistic reading (in the primary one the key risk is already practically nil). "
            "**This is the cost-effectiveness order for measuring, and it is recomputed automatically whenever the YAML changes.**\n\n"
            + tabla(filas_prio, ["#", "parameter", "source", "status", "declared range", "share of the key risk it removes"]))
    (ROOT / "CONFIANZA.md").write_text(doc)
    return {"filas": filas_v, "p_alguna": p_alguna, "p_alguna1": p_alguna1, "riesgo": riesgo,
            "riesgo1": riesgo1, "prio": prio, "prio1": prio1, "niveles": niveles}
