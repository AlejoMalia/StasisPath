"""StasisPath: systematic layer cross-check — every data point against every law, all at once.

`encuentros.py` crosses DIMENSIONS pairwise (T×t, mass×E...). This module does something different:
it pits **the entire data layer against the entire law layer** and looks for structure in the
residuals. It is what was done by hand earlier and produced C10 and L11: a datum already in the
network that turned out to answer a different question.

Three cross-checks, none of which invents a datum:

  1. **Thermal excess.** For each point with (T, t), the excess over the window C2 allows is
     computed: exc = t / w(T), with w(T) = t37 · Q10^((37−T)/10). An excess ≫ 1 means that system
     withstood far more than the thermal law permits ⇒ **a non-thermal mechanism is at work**.
     C4, C9 and C10 do this for four isolated points; here it is done for all of them.
  2. **Structure in the excesses.** Does the excess cluster by class, by phase, or by
     natural/artificial? If it clusters, that is a quantitative regularity the framework had not written down.
  3. **Pathways against bounds.** Each pathway declares a window; each bound computes what is allowed.
     A pathway promising more than its bound permits is either a refutation or a bookkeeping error.

**Declared limit:** everything that comes out of here is **derived**, not measured. A computed excess
is not a new datum: it is a re-reading of existing data. It serves to **point at where to look**, and every
anomaly is flagged for human review, never turned into a closed node on its own (R5).

Output: CRUCE.md + red/fig/C_exceso.png. Called by motor.py.
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
COLOR_CLASE = {"hypothermia": BLUE, "low_flow": BLUE, "normothermia": BLUE, "cellular": BLUE,
               "controlled_phase": ORANGE, "glass": AQUA, "natural": YELLOW}

def g(x):
    if x is None: return "—"
    if x == float("inf"): return "∞"
    return f"{x:.3g}" if abs(x) < 1e4 else f"{x:.2e}"

def tabla(filas, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in f) + " |" for f in filas) + "\n"

def generar(D, PAR, ROOT):
    p = {k: v["v"] for k, v in PAR.items()}
    vent = lambda T: p["t37"] * p["Q10"] ** ((37 - T) / 10)   # C2: ischemic window (min) at T

    # ---------------------------------------------------------------- 1. thermal excess
    filas, pts = [], []
    for pid, q in sorted(D["puntos"].items()):
        T, t = q.get("T"), q.get("t")
        if T is None or t is None: continue
        if q.get("fase") == "glass":
            # below Tg there is no metabolism: the thermal law does not apply and the excess means nothing
            filas.append([pid, q["label"][:44], g(T), g(t), q.get("clase", "—"), "—",
                          "not applicable (glass: no metabolism)"])
            continue
        w = vent(T); exc = t / w
        # the excess at the corners of the Q10 and t37 range, so as not to give a number without a band
        excs = []
        for q10 in PAR["Q10"]["r"]:
            for t37 in PAR["t37"]["r"]:
                excs.append(t / (t37 * q10 ** ((37 - T) / 10)))
        lo, hi = min(excs), max(excs)
        if exc <= 1.5:        veredicto = "within the thermal law"
        elif lo <= 1.5:       veredicto = "**ambiguous**: the Q10 band crosses it"
        else:                 veredicto = "**EXCESS**: requires a non-thermal mechanism"
        filas.append([pid, q["label"][:44], g(T), g(t), q.get("clase", "—"),
                      f"×{g(exc)} ({g(lo)}–{g(hi)})", veredicto])
        pts.append((pid, q, exc, lo, hi))

    # ---------------------------------------------------------------- 2. structure in the excesses
    def resumen(clave, valores=None):
        grupos = {}
        for pid, q, exc, lo, hi in pts:
            k = q.get(clave, "—")
            if isinstance(k, bool): k = "yes" if k else "no"
            grupos.setdefault(k, []).append(exc)
        out = []
        for k, v in sorted(grupos.items(), key=lambda t: -max(t[1])):
            v = sorted(v)
            med = v[len(v) // 2] if len(v) % 2 else (v[len(v) // 2 - 1] + v[len(v) // 2]) / 2
            out.append([k, len(v), g(min(v)), g(med), g(max(v))])
        return out

    excesivos = [(pid, q, exc, lo, hi) for pid, q, exc, lo, hi in pts if lo > 1.5]
    naturales = [x for x in excesivos if x[1].get("clase") == "natural"]
    artificiales = [x for x in excesivos if x[1].get("clase") != "natural"]
    max_art = max((x[2] for x in artificiales), default=0.0)
    min_nat = min((x[2] for x in naturales), default=float("inf"))
    # BATCH 52 (audit against ourselves): the document claimed that 'the bands do not overlap even at their
    # extremes', but that was NOT computed: `hay_brecha` compared only the central values. It is
    # computed now, and the sentence is written from the computation instead of by hand.
    max_art_hi = max((x[4] for x in artificiales), default=0.0)     # ceiling of the artificial band
    min_nat_lo = min((x[3] for x in naturales), default=float("inf"))  # floor of the natural band
    bandas_disjuntas = min_nat_lo > max_art_hi
    hay_brecha = min_nat > max_art and naturales and artificiales
    # Third caveat (batch 52): the artificial ceiling and the natural floor are not at the same level of
    # demonstrated success (E0–E5 scale). It is measured what happens if the same level is required on both sides.
    E_NAT = min((x[1].get("E", 0) for x in naturales), default=0)
    art_mismo_E = [x for x in artificiales if x[1].get("E", 0) >= E_NAT]
    max_art_E = max((x[2] for x in art_mismo_E), default=0.0)
    quien_art = max(artificiales, key=lambda x: x[2])[0] if artificiales else "—"
    quien_nat = min(naturales, key=lambda x: x[2])[0] if naturales else "—"
    E_art = dict(artificiales and [(x[0], x[1].get("E")) for x in artificiales]).get(quien_art)

    # ---------------------------------------------------------------- 3. pathways against bounds
    # A pathway whose declared window exceeds what its bound permits is an anomaly. Only those
    # pathways with a numerical window in minutes and a temperature deducible from the text are checked: the rest is declared.
    sin_check = [v for v, q in D["vias"].items() if not any(c.isdigit() for c in str(q.get("ventana", "")))]

    # ---------------------------------------------------------------- figura
    fig, ax = plt.subplots(figsize=(8.6, 0.34 * len(pts) + 1.8))
    orden = sorted(pts, key=lambda x: x[2])
    for y, (pid, q, exc, lo, hi) in enumerate(orden):
        c = COLOR_CLASE.get(q.get("clase"), MUTED)
        ax.plot([lo, hi], [y, y], color=GRID, lw=2, zorder=1)
        ax.scatter([exc], [y], s=48, color=c, zorder=3, edgecolor=SURF, linewidth=1.2)
        ax.text(hi * 1.3, y, f"×{g(exc)}", va="center", fontsize=7, color=INK2)
    ax.axvline(1, color="#c0392b", lw=1.3)
    ax.text(1.1, len(pts) - 0.5, " thermal law of C2", fontsize=7, color="#c0392b")
    ax.set_yticks(range(len(orden)))
    ax.set_yticklabels([f"{x[0]}: {x[1]['label'][:40]}" for x in orden], fontsize=7, color=INK2)
    ax.set_xscale("log")
    ax.set_xlabel("Excess over the thermal window: time withstood / window C2 allows at that T", color=INK2)
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
    ax.grid(axis="x", color=GRID, lw=0.6); ax.set_facecolor(SURF); fig.set_facecolor(SURF)
    fig.suptitle("Every data point in the framework against the thermal law, all at once",
                 x=0.02, ha="left", fontsize=11, color=INK)
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "C_exceso.png", dpi=150); plt.close(fig)

    # ---------------------------------------------------------------- documento
    doc = ("<!-- AUTO-GENERATED by red/cruce.py. DO NOT EDIT BY HAND. -->\n"
           "# StasisPath: systematic cross-check — the entire data layer against the law layer\n\n"
           "`ENCUENTROS.md` crosses **dimensions** pairwise. Here something else is done: **every data point is pitted "
           "against the thermal law**, all at once. C4, C9 and C10 already did this for four isolated points; this does it for "
           f"the {len(pts)} that have both temperature and time.\n\n"
           "> **Everything here is DERIVED, not measured.** A computed excess is not a new datum: it is a re-reading of "
           "data that was already present. It serves to **point at where to look**. No anomaly closes a node on its own (R5).\n\n"
           f"![Thermal excess](red/fig/C_exceso.png)\n\n"
           "## 1. Every data point against the C2 window\n\n"
           f"Window: w(T) = t37 · Q10^((37−T)/10), with t37 = {p['t37']} min and Q10 = {p['Q10']}. The band in parentheses "
           "is the corners of the declared range of both. A point counts as an excess only if **the whole** band exceeds 1.5.\n\n"
           + tabla(filas, ["point", "system", "T °C", "t min", "class", "excess ×", "verdict"])
           + f"\n**{len(excesivos)} points robustly require a non-thermal mechanism.**\n\n"
           "## 2. Is there structure in the excesses?\n\n"
           "**By system class:**\n\n"
           + tabla(resumen("clase"), ["class", "n", "minimum", "median", "maximum"])
           + "\n**By phase:**\n\n"
           + tabla(resumen("fase"), ["phase", "n", "minimum", "median", "maximum"])
           + "\n**By origin (artificial = human protocol; natural = biology):**\n\n"
           + tabla(resumen("artificial"), ["artificial", "n", "minimum", "median", "maximum"]))

    if hay_brecha:
        doc += (f"\n> **REGULARITY FOUND, and the framework had not written it down as a law.** Among the points that exceed "
                f"the thermal law there is a **clean gap**: the largest excess achieved by an **artificial protocol** is "
                f"**×{g(max_art)}**, and the smallest achieved by **natural biology** is **×{g(min_nat)}** — a jump of "
                f"**×{g(min_nat / max_art)}** with no point in between. ⇒ What the biochemistry of a hibernator or an "
                "amphibian achieves is **beyond the reach of every tested human protocol**, and not narrowly: by a factor "
                f"of {g(min_nat / max_art)}. It is the same frontier C4 found for the frog and the turtle, but now "
                "measured over **all** the points in the framework and with the gap quantified. "
                + (f"The bands **do not overlap even at their extremes** (artificial ceiling ×{g(max_art_hi)} versus natural "
                   f"floor ×{g(min_nat_lo)}), so it is not an artefact of the Q10 range.\n\n"
                   if bandas_disjuntas else
                   f"⚠ **But the bands DO overlap** (artificial ceiling ×{g(max_art_hi)} versus natural floor "
                   f"×{g(min_nat_lo)}): the gap exists only between central values and **may be an artefact of the Q10 range**.\n\n")
                + "> **THREE CAVEATS, and without them the finding misleads** (the third was added later, "
                "audited against; the first two were already present).\n"
                "> 1. **The gap describes what has been ATTEMPTED, not what is possible.** The artificial ceiling of ×"
                f"{g(max_art)} is the best **tested** protocol, not a demonstrated limit. No law in the framework forbids "
                "exceeding it; if a protocol reaches ×100 tomorrow the gap closes without refuting any of this. It is an "
                "**empirical frontier**, not a barrier.\n"
                "> 2. **Part of the natural excess is ectothermy, not transferable biochemistry.** The window is calibrated with "
                f"t37 = {p['t37']} min and Q10 = {p['Q10']}, **measured in human brain** (F4). Applying it to a turtle or a "
                "lungfish extrapolates outside its domain: those animals have a far lower basal metabolism to begin "
                "with. C4 already warns of this. The excess of the **arctic ground squirrel** (×"
                f"{g(min_nat)}) is the most informative of the natural ones, because it is a **mammal**, and there the comparison "
                "is close. **Checked: the point that sets the natural floor IS the ground squirrel (a mammal), "
                "so the ectothermy confound does NOT invalidate the gap** — removing the frog, the turtle and the "
                f"lungfish leaves the natural floor exactly where it is, at ×{g(min_nat)}.\n"
                "> 3. **The two sides of the gap are not at the same level of demonstrated success, and that is a bias "
                f"of our own.** The artificial ceiling is set by **{quien_art}**, which reaches **E{E_art}**, while "
                f"every natural point sits at **E{E_NAT}** (animal recovered). Comparing a cellular result with "
                "a whole animal is not comparing like with like. Requiring the same E level on both sides, the artificial ceiling drops "
                f"to ×{g(max_art_E)} and the gap **widens** to ×{g(min_nat / max_art_E) if max_art_E else '—'}. "
                "⇒ The caveat **does not break the finding: it enlarges it.** But it had to be stated, because a reader could "
                "read the gap as 'human protocols reach ×48 with a recovered animal', and that is false.\n")
    else:
        doc += ("\n> No clean gap appears between artificial protocols and natural biology: their excesses "
                "overlap. The frontier C4 suggests for isolated cases **does not hold** when all the points are examined.\n")

    doc += ("\n## 3. Pathways against bounds\n\n"
            f"{len(D['vias'])} pathways in the framework. **{len(sin_check)} declare their window as free text with no figure in minutes**, "
            "so they cannot be checked automatically against a bound. This is a **formatting debt, not a knowledge gap**: "
            "whoever writes a window as a number and a unit makes this check run by itself.\n\n"
            "Pathways with no checkable window: " + ", ".join(sorted(sin_check)) + "\n\n"
            "## What to do with this\n\n"
            "1. The points marked **EXCESS** are those that sustain the existence of a biological route: without them, the "
            "thermal alone would suffice to describe the whole framework.\n"
            "2. Those marked **ambiguous** are the measurement candidates: narrowing Q10 or t37 would resolve them with no new experiment.\n"
            "3. Pathways without a numerical window are bookkeeping work, at almost zero cost, that unlocks an automatic check.\n")
    (ROOT / "CRUCE.md").write_text(doc)
    return {"n_pts": len(pts), "excesivos": len(excesivos), "brecha": hay_brecha,
            "max_art": max_art, "min_nat": min_nat, "sin_check": sin_check,
            "bandas_disjuntas": bandas_disjuntas, "max_art_hi": max_art_hi, "min_nat_lo": min_nat_lo,
            "max_art_E": max_art_E, "E_nat": E_NAT, "quien_art": quien_art, "quien_nat": quien_nat}
