"""StasisPath: computational analysis of margins.

The question: **how wrong would each parameter have to be for a verdict to reverse?**
A conclusion with a margin of ×1000 is not the same as one with a margin of ×1.2, even though both
appear as "M" in the framework. Here, for each verdict of each bound, the **flip factor** is measured: by how
much each parameter it depends on would have to be multiplied (or divided) for the verdict to stop
holding, keeping the others at their central value.
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"

def g(x):
    if x == float("inf"): return "∞"
    return f"{x:.3g}" if abs(x) < 1e4 else f"{x:,.0f}"

def tabla(filas, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in f) + " |" for f in filas) + "\n"

def generar(D, PAR, COTAS, ROOT):
    """BOUNDS: dict id -> function(p) returning (outputs, {verdict: (bool, key)})."""
    base = {k: v["v"] for k, v in PAR.items()}
    filas, puntos = [], []

    for cid, cdef in D["cotas"].items():
        f = COTAS[cid]
        _, v0 = f(base)
        for texto, (ok0, clave) in v0.items():
            if not ok0:
                continue  # only verdicts that hold today are analysed
            mejor_par, mejor_fac, direccion = None, float("inf"), ""
            for par in cdef["deps"]:
                # binary search for the multiplicative factor that flips the verdict
                for signo, etiq in ((+1, "×"), (-1, "÷")):
                    lo, hi = 1.0, 1.0
                    # expand until a flip is found or give up at ×10^6
                    for _ in range(60):
                        hi *= 1.15
                        q = dict(base); q[par] = base[par] * (hi if signo > 0 else 1 / hi)
                        try:
                            _, vt = f(q)
                        except Exception:
                            break
                        if not vt[texto][0]:
                            break
                        lo = hi
                    else:
                        continue
                    if hi > 1e6:
                        continue
                    q = dict(base); q[par] = base[par] * (hi if signo > 0 else 1 / hi)
                    try:
                        _, vt = f(q)
                    except Exception:
                        continue
                    if vt[texto][0]:
                        continue  # never flipped
                    # afinar
                    a, b = lo, hi
                    for _ in range(40):
                        mid = math.sqrt(a * b)
                        q = dict(base); q[par] = base[par] * (mid if signo > 0 else 1 / mid)
                        _, vm = f(q)
                        if vm[texto][0]: a = mid
                        else: b = mid
                    if b < mejor_fac:
                        mejor_fac, mejor_par, direccion = b, par, etiq
            # Normalize against the DECLARED uncertainty of the parameter: a flip at ×1.5 is not
            # fragile if the parameter is known to ±10 %. What matters is flip / plausible error.
            if mejor_par:
                lo_p, hi_p = PAR[mejor_par]["r"]; c_p = PAR[mejor_par]["v"]
                err_decl = max(hi_p / c_p, c_p / lo_p) if lo_p > 0 and c_p > 0 else 1.0
                holgura = mejor_fac / err_decl if err_decl > 0 else float("inf")
            else:
                err_decl, holgura = 1.0, float("inf")
            if mejor_fac == float("inf"):
                frag = "**estructural**"   # no parameter flips it: it is qualitative
            elif holgura < 1:   frag = "**DENTRO DEL ERROR**"
            elif holgura < 2:   frag = "**FRAGILE**"
            elif holgura < 5:   frag = "ajustado"
            else:               frag = "holgado"
            filas.append([cid, texto, "yes" if clave else "no",
                          mejor_par or "—", f"{direccion}{g(mejor_fac)}" if mejor_par else "—",
                          f"±{g((err_decl - 1) * 100)} %" if mejor_par else "—",
                          g(holgura) if holgura != float("inf") else "∞", frag])
            if mejor_fac != float("inf"):
                puntos.append((f"{cid}: {texto[:44]}", holgura, clave))

    puntos.sort(key=lambda t: t[1])
    fig, ax = plt.subplots(figsize=(8.6, 0.38 * len(puntos) + 1.6))
    ys = range(len(puntos))
    for y, (lab, fac, clave) in zip(ys, puntos):
        c = ORANGE if fac < 2 else (YELLOW if fac < 5 else AQUA)
        ax.barh(y, fac, color=c, height=0.55, zorder=2)
        ax.text(fac * 1.12, y, f"×{g(fac)}", va="center", fontsize=7.5, color=INK2)
    ax.axvline(1, color="#c0392b", lw=1.2); ax.axvline(2, color=INK2, lw=1, ls="--")
    ax.text(1, len(puntos) - 0.3, " within the declared error", fontsize=7, color="#c0392b")
    ax.set_yticks(list(ys)); ax.set_yticklabels([p[0] for p in puntos], fontsize=7.2, color=INK2)
    ax.set_xscale("log"); ax.set_xlabel("Slack = flip factor / declared parameter error (< 1 = the declared error already overturns it)")
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
    ax.grid(axis="y", visible=False); ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_facecolor(SURF); fig.set_facecolor(SURF)
    fig.suptitle("Framework margins: which conclusion falls first", x=0.02, ha="left", fontsize=11, color=INK)
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "M_margenes.png", dpi=150); plt.close(fig)

    fragiles = [f for f in filas if "FRAGILE" in f[7] or "DENTRO" in f[7]]
    holgados = [f for f in filas if f[7] == "holgado"]
    estr = [f for f in filas if "estructural" in f[7]]
    doc = ("<!-- AUTO-GENERATED by red/margenes.py. DO NOT EDIT BY HAND. -->\n"
           "# StasisPath: margins of the framework\n\n"
           "**What this measures:** for every verdict that currently holds, by how much the **most sensitive** parameter would have to be wrong "
           "for the verdict to reverse (the rest stay at their central values). A verdict with factor ×1.3 and another "
           "with factor ×1000 both appear as 'M' in the framework, but **they are not worth the same**: this separates them.\n\n"
           "The flip factor alone is misleading: ×1.5 is not small if the parameter is known to ±10 %. That is why it is normalized against "
           "the parameter's own **declared uncertainty**. **Slack = flip factor / declared error.**\n\n"
           "- **WITHIN THE ERROR** (slack < 1): the range we have already declared overturns the verdict. Either measure better or weaken the claim.\n"
           "- **FRAGILE** (1–2): survives narrowly.\n"
           "- **ajustado** (2–5).\n"
           "- **comfortable** (> 5): the conclusion does not depend on the parameter's precision.\n"
           "- **structural**: no parameter overturns it ⇒ the verdict is qualitative, not numerical.\n\n"
           "![Margins](red/fig/M_margenes.png)\n\n"
           f"**Summary: {len(fragiles)} fragile · {len(filas) - len(fragiles) - len(holgados) - len(estr)} tight · "
           f"{len(holgados)} holgados · {len(estr)} estructurales.**\n\n"
           + tabla(filas, ["bound", "verdict", "key?", "most sensitive parameter", "flip factor", "declared error", "slack", "margin"]))
    if fragiles:
        doc += ("\n## The fragile parts, in measurement priority order\n\n" +
                "\n".join(f"{i+1}. **{f[0]}** — «{f[1]}» fails if **{f[3]}** is off by {f[4]}; declared error {f[5]} ⇒ slack {f[6]}."
                          for i, f in enumerate(fragiles)) + "\n")
    (ROOT / "MARGENES.md").write_text(doc)
    return filas, fragiles
