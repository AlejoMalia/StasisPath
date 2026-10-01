"""StasisPath: triangulation of unknowns. The framework projects ranges for what it has not measured.

Instead of saying 'we do not know', it walks **every independent path** in the network that
bounds an unknown, computes each one's range, and keeps the **intersection**. The result is not
an exact number: it is a projected range that is later sharpened by measurement.

The most useful output is not the intersection: it is the **contradiction**. If two independent
paths give incompatible ranges, one of the laws feeding them is wrong, and the framework says so.

Each path declares which laws/sources it derives from, what kind of bound it imposes (minimum,
maximum or range) and its value. A path that depends on another is NOT independent and is flagged.
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA, YELLOW, RED = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#c0392b"

def g(x):
    if x is None or x != x: return "—"
    if x == float("inf"): return "∞"
    if x == float("-inf"): return "−∞"
    return f"{x:.3g}" if abs(x) < 1e4 else f"{x:,.0f}"

def tabla(f, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in r) + " |" for r in f) + "\n"


def _rango(c):
    """Converts a path into (lo, hi)."""
    t = c["tipo"]
    if t == "rango": return (c["lo"], c["hi"])
    if t == "min":   return (c["v"], float("inf"))
    if t == "max":   return (float("-inf"), c["v"])
    return (c["v"], c["v"])


def generar(D, PAR, DERIV, ROOT):
    p = {k: v["v"] for k, v in PAR.items()}
    INC = incognitas(p, DERIV)
    out, resumen = [], []

    for iid, inc in INC.items():
        cams = inc["caminos"]
        indep = [c for c in cams if c.get("indep", True) and not c.get("regimen")]
        otros_reg = [c for c in cams if c.get("regimen")]
        # intersection of the independent paths only
        lo = max((_rango(c)[0] for c in indep), default=float("-inf"))
        hi = min((_rango(c)[1] for c in indep), default=float("inf"))
        vacio = lo > hi
        # which pair contradicts?
        choque = None
        if vacio:
            for i, a in enumerate(indep):
                for b in indep[i + 1:]:
                    la, ha = _rango(a); lb, hb = _rango(b)
                    if la > hb or lb > ha: choque = (a["via"], b["via"]); break
                if choque: break
        filas = [[c["via"], "yes" if c.get("indep", True) else "**no**",
                  {"min": "≥", "max": "≤", "rango": "∈", "punto": "="}[c["tipo"]],
                  g(_rango(c)[0]) if c["tipo"] != "max" else "",
                  g(_rango(c)[1]) if c["tipo"] != "min" else "",
                  c["de"]] for c in cams]
        cuerpo = (f"**{inc['desc']}**\n\n" + tabla(filas, ["path", "independent?", "", "min", "max", "what it derives from"]))
        for c in otros_reg:
            cuerpo += (f"\n> **Separate regime — '{c['via']}' ({c['regimen']}).** It does not enter the intersection: "
                       f"it does not contradict the others, it describes **a different physical system**. It bounds {'≥' if c['tipo']=='min' else '≤'} "
                       f"{g(_rango(c)[0] if c['tipo']=='min' else _rango(c)[1])} {inc['u']}.\n")
        if vacio:
            cuerpo += (f"\n> ⚠ **CONTRADICTION: the intersection is empty.** The paths '{choque[0]}' and '{choque[1]}' "
                       "are incompatible. **That is not a failure of the method: it is the result.** One of the laws feeding "
                       "them is wrong, and the unknown cannot be projected until that is resolved.\n")
            if inc.get("nota_choque"): cuerpo += "\n" + inc["nota_choque"] + "\n"
            resumen.append([iid, inc["desc"][:52], "**contradiction**", "—", f"{choque[0]} vs {choque[1]}"])
        else:
            ancho = (hi / lo) if (lo > 0 and hi < float("inf")) else float("inf")
            cuerpo += (f"\n> **PROJECTED RANGE: {g(lo)} – {g(hi)} {inc['u']}** "
                       f"({len(indep)} independent paths"
                       + (f", width factor ×{g(ancho)}" if ancho != float("inf") else ", unbounded on one side") + ").\n")
            if inc.get("afinar"): cuerpo += f"\n**How to sharpen this to a number:** {inc['afinar']}\n"
            resumen.append([iid, inc["desc"][:52], f"{g(lo)} – {g(hi)} {inc['u']}",
                            f"×{g(ancho)}" if ancho != float("inf") else "open", f"{len(indep)} paths"])
        out.append((iid, inc["titulo"], cuerpo))

    # ---- figura
    proy = [(iid, inc, max((_rango(c)[0] for c in inc["caminos"] if c.get("indep", True)), default=float("-inf")),
             min((_rango(c)[1] for c in inc["caminos"] if c.get("indep", True)), default=float("inf")))
            for iid, inc in INC.items()]
    proy = [x for x in proy if x[2] <= x[3] and x[2] > 0 and x[3] < float("inf")]
    fig, ax = plt.subplots(figsize=(8.4, 0.62 * len(proy) + 1.6))
    for y, (iid, inc, lo, hi) in enumerate(proy):
        for c in inc["caminos"]:
            cl, ch = _rango(c)
            cl = max(cl, lo / 8 if lo > 0 else cl); ch = min(ch, hi * 8 if hi < float("inf") else ch)
            ax.plot([cl, ch], [y + 0.22, y + 0.22], color=GRID, lw=5, solid_capstyle="butt", zorder=1)
        ax.plot([lo, hi], [y, y], color=BLUE, lw=9, solid_capstyle="butt", zorder=3)
        ax.text(hi, y, f"  {g(lo)}–{g(hi)}", va="center", fontsize=8, color=INK2)
    ax.set_yticks(range(len(proy))); ax.set_yticklabels([f"{i} · {inc['desc'][:44]}" for i, inc, _, _ in proy], fontsize=7.5, color=INK2)
    ax.set_xscale("log"); ax.set_xlabel("projected range (log scale) — grey: each path · blue: intersection")
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
    ax.grid(axis="x", color=GRID, lw=0.6); ax.grid(axis="y", visible=False)
    ax.set_facecolor(SURF); fig.set_facecolor(SURF)
    fig.suptitle("Triangulation: what the framework can project without measuring", x=0.02, ha="left", fontsize=11, color=INK)
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "T_triangulacion.png", dpi=150); plt.close(fig)

    doc = ("<!-- AUTO-GENERATED by red/triangular.py. DO NOT EDIT BY HAND. -->\n"
           "# StasisPath: triangulation of unknowns\n\n"
           "For every datum we **do not have**, all independent paths in the network that bound it are walked "
           "and the **intersection** is taken. It does not give the exact number: it gives the **projected range**, which is later sharpened by measurement.\n\n"
           "**The most useful output is not the intersection, it is the contradiction.** If two independent paths give "
           "incompatible ranges, one of the laws feeding them is wrong — and that is a result, not a failure.\n\n"
           "![Triangulation](red/fig/T_triangulacion.png)\n\n"
           + tabla(resumen, ["id", "unknown", "projected range", "width", "note"]) + "\n")
    for iid, tit, cuerpo in out:
        doc += f"## {iid} · {tit}\n\n{cuerpo}\n"
    (ROOT / "TRIANGULACION.md").write_text(doc)
    return resumen


def incognitas(p, DERIV):
    """Each unknown with its paths. `indep: False` marks a path that reuses another."""
    Mtox = DERIV["M_toxico"]; Mde = DERIV["M_de_CCR"]; tasa = DERIV["tasa_conv"]; LCe = DERIV["LC_esfera"]
    I = {}

    # ---- I1: damage in the cold arm of P19 -------------------------------------
    I["I1"] = dict(titulo="Damage in the cold arm of P19 (M22 9.3 M at −22 °C)",
        desc="Relative damage (1 − respiration/control) when loading 9.3 M at −22 °C", u="",
        afirmar=None, u2="",
        nota_choque=("**BUT the contradiction does NOT affect the P19 verdict, and that can be demonstrated.** "
            "German measured, in the **same arm**, respiratory damage of **0.220** (at 8.42 M) and LTP of **138.1 %**, which **passes** our "
            "preregistered threshold of 130 %. ⇒ There exists a damage level with **demonstrably preserved LTP: 0.220**. "
            "The two colliding paths predict **0.142 and ≤0.07**, and **both fall below 0.220**. "
            "**The contradiction is about HOW MUCH damage there will be, not about whether P19 passes: both paths predict PASS.**\n\n"
            "**And it remains the best argument for running it.** The two paths are not matters of opinion: "
            "the Arrhenius one extrapolates from 23–37 °C down to −22 °C, a large extrapolation and **without L20's osmotic term**; "
            "Fahy's is a real measurement of M22 at −22 °C, but **in kidney slice, not neural tissue**. ⇒ The experiment does not merely measure "
            "a number: **it discriminates between two of the framework's own laws**. If it comes out ≈0.14, the Arrhenius extrapolation holds and "
            "Fahy's result does not transfer from kidney to brain. If it comes out ≤0.07, low-temperature toxicity falls faster "
            "than Arrhenius predicts, and **L20 was right: the dominant damage in the cold is osmotic, not chemical**."),
        afinar="is exactly what P19 measures.",
        caminos=[
            dict(via="Arrhenius from oocytes × German's measured point", tipo="punto", v=0.142,
                 de="F72 (9.28 M at 10 °C → 0.536) scaled by Ea/R = 2952 K from F55", indep=True),
            dict(via="Fahy anchors: M22 is tolerable at −22 °C in kidney slice", tipo="max", v=0.07,
                 de="F65/F39 + no-damage band K⁺/Na⁺ ≥ 93 % (G4b)", indep=True),
            dict(via="Damage↔LTP calibration: at damage 0.220 LTP WAS preserved", tipo="max", v=0.220,
                 de="F72: German measured in the SAME arm respiratory damage 0.220 (8.42 M) and LTP 138.1 % (control 157.7, n.s.)", indep=True),
            dict(via="Lower bound: cannot be better than the CPA-free control", tipo="min", v=0.0,
                 de="definition", indep=True),
        ])
    I["I1"]["u"] = ""

    # ---- I2: CCR of the eutectic solvents ---------------------------------------------
    I["I2"] = dict(titulo="CCR of natural deep eutectic solvents (NADES)",
        desc="Critical cooling rate of the eutectic solvents", u="°C/min",
        afinar="NO LONGER NEEDED: the calorimetry was already published in F80 and has been read. **CCR > 30 °C/min ⇒ prediction I2 (0.3 °C/min) is REFUTED by its own criterion (refuted if > 0.426).**",
        caminos=[
            dict(via="They vitrify by direct immersion in liquid N₂", tipo="max", v=1e4,
                 de="F80: if they vitrify when a small sample is immersed, their CCR does not exceed the immersion rate (~10⁴ °C/min)", indep=True),
            dict(via="They are not pure water: their CCR is below that of water", tipo="max", v=3.84e8,
                 de="F76 (agua pura: 3.84 × 10⁸ °C/min)", indep=True),
            dict(via="**MEASURED (F80): they crystallize in DSC when cooled at 30 °C/min**", tipo="min", v=30.0,
                 de="F80 Table 2: Tc onset −26.6 to −32.3 °C at 50 % w/v ⇒ CCR > 30 °C/min", indep=True),
        ])

    # ---- I3: maximum mass of vitrifiable human organ ---------------------
    lc_f2 = DERIV["LC_viable"]; m_f2 = DERIV["masa_viable"] * 1000
    I["I3"] = dict(titulo="Maximum mass of human tissue vitrifiable with current chemistry",
        desc="Maximum vitrifiable mass without crossing the toxic threshold", u="g",
        afinar="by measuring the CCR of a CPA at low concentration. If one exists, the limit rises; if not, it is confirmed.",
        caminos=[
            dict(via="F2: where the required molarity crosses the toxic threshold", tipo="max", v=m_f2,
                 de="C3 + CCR↔M line + 9.28 M threshold from F72", indep=True),
            dict(via="Physically demonstrated: 3 L of M22 vitrified", tipo="min", v=3000.0,
                 de="F2 (physical glass at litre scale, no biology)", indep=True),
            dict(via="Demonstrated with function: 13.9 g rabbit kidney transplanted", tipo="min", v=13.9,
                 de="F50 (dielectric, normal clinical function)", indep=False),
        ])

    # ---- I4: human τ_eq with optimal reperfusion ----------------------------
    I["I4"] = dict(titulo="human τ_eq attainable with optimal reperfusion",
        desc="Equivalent ischemia at 37 °C a human could tolerate with the best reperfusion", u="min",
        afinar="an optimized reperfusion trial in pig, the closest model and already in use (F42).",
        caminos=[
            dict(via="Cross-species invariance: the dog withstands 17 min", tipo="min", v=12.5,
                 de="F25/F25b + T1 from the scaling module (τ_eq invariant, error ×1.9)", indep=True),
            dict(via="Existence in another mammal: cat, 1 h brain only", tipo="max", v=60.0,
                 de="F38 — upper bound: nobody has exceeded this in a whole organism", indep=True),
            dict(via="Cellular limit: BrainEx recovers cells at 4 h", tipo="max", v=240.0,
                 de="F23 — absolute ceiling; above it not even the cell returns", indep=False),
        ])

    # ---- I5: supercooling duration at liver scale --------------
    I["I5"] = dict(titulo="Supercooling duration of a human liver at −2 °C",
        desc="Hours of supercooling at −2 °C for 1.5 L before nucleation", u="h",
        afinar="supercool two different volumes at the same temperature and see whether the time scales as 1/V. **A cheap and decisive experiment for L16.** The isobaric/isochoric contrast additionally gives a direct measure of how much constant-volume confinement suppresses nucleation.",
        caminos=[
            dict(via="Poisson rate FITTED with rat liver (2 points, −6 °C)", tipo="max", v=-math.log(0.5)/(0.567*1.5),
                 de="F85: 100 % at 72 h and 58 % at 96 h ⇒ J(−6 °C) ≈ 0.57 /L·h; the time at 50 % success is given here", indep=True),
            dict(via="V·t invariant from the pig kidney (isobaric)", tipo="max", v=0.2 * 5.0 / 1.5,
                 de="F20 (0.2 L × 5 h at −2 °C) assuming Poisson-type nucleation (F4 of FORMULACION)", indep=True),
            dict(via="Measured at −2 °C in isochoric pig liver", tipo="min", v=24.0,
                 de="F22 (1.5 L, 24–48 h without freezing, isochoric system)", indep=True,
                 regimen="isochoric: constant volume generates pressure upon nucleation and **suppresses nucleation**"),
        ])
    return I
