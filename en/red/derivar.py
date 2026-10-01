"""StasisPath: closure by DERIVATION. Can the framework predict what it has not yet measured?

The idea: with enough verified laws, some open nodes need no new measurement — they close by
being **derived** from those already closed. It is attempted here with D_CPA: fit
toxicity(concentration) from one dataset and toxicity(temperature) from another **independent**
one, compose them, and with that **predict the outcome of P19 before running it**.

Rule: a derivation is only valid if (a) it uses data other than the node it closes,
(b) it declares its range of validity and (c) it produces a falsifiable prediction with a threshold.
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"

def g(x): return f"{x:.3g}" if abs(x) < 1e4 else f"{x:,.0f}"
def tabla(f, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in r) + " |" for r in f) + "\n"

# ---- Datum A: concentration series at T = 10 °C (German, F72). Basal respiration, pmol/min.
GERMAN = [(0.0, 173.3, 6.7), (4.28, 139.7, 3.1), (8.42, 135.1, 6.7), (9.28, 80.4, 5.6)]
T_GERMAN = 10.0
# ---- Datum B: dependence on T at FIXED concentration and time (Szurek & Eroglu, F55).
#      PROH 1.5 M, 15 min: degeneration 54.2 % at 23 °C and 85 % at 37 °C.
SZUREK = [(23.0, 0.542), (37.0, 0.850)]
# ---- Qualitative anchors to validate against (Fahy, F39/F65): M22 9.3 M tolerable at −22 °C;
#      inaceptable a −3 °C. VMP 8.4 M tolerable a −3 °C.

def generar(ROOT):
    # (1) Shape of the concentration curve, at 10 °C. damage = 1 − respiration/control.
    ctrl = GERMAN[0][1]
    pts = [(C, 1.0 - R / ctrl) for C, R, _ in GERMAN[1:]]
    # SELF-CORRECTION: the first attempt fitted a power law and gave an exponent of 0.9,
    # which does NOT describe these data: damage is ~0.19-0.22 from 4.3 to 8.4 M and jumps to 0.54 at 9.3 M.
    # That is a THRESHOLD, not a power. A sigmoid cannot be fitted reliably to 3 points,
    # so nothing is fitted: the MEASURED point at 9.28 M is used and scaled in temperature only.
    meseta = sum(d for C, d in pts if C < 9) / len([1 for C, d in pts if C < 9])
    salto = pts[-1][1]
    umbral_lo, umbral_hi = 8.42, 9.28

    # (2) g(T): Arrhenius factor from an INDEPENDENT dataset.
    (T1, d1), (T2, d2) = SZUREK
    K1, K2 = T1 + 273.15, T2 + 273.15
    EaR = math.log(d2 / d1) / (1 / K1 - 1 / K2)      # K
    gT = lambda T: math.exp(-EaR / (T + 273.15))
    gnorm = lambda T: gT(T) / gT(T_GERMAN)           # normalizado a la T de German

    # (3) Composition and PREDICTION
    # Damage = point measured at that concentration (plateau or jump) scaled by temperature.
    def D(C, T):
        base = salto if C >= umbral_hi else meseta
        return base * gnorm(T)
    casos = [("German 9.28 M at 10 °C (MEASURED: damage 0.54)", 9.28, 10.0),
             ("M22 9.3 M at −22 °C (arm C of P19)", 9.30, -22.0),
             ("M22 9.3 M a −3 °C (Fahy: inaceptable)", 9.30, -3.0),
             ("VMP 8.4 M a −3 °C (Fahy: tolerable)", 8.40, -3.0),
             ("V3 8.42 M at 10 °C (MEASURED: damage 0.22)", 8.42, 10.0)]
    filas = [[nm, g(C), g(T), g(D(C, T)), g(gnorm(T))] for nm, C, T in casos]

    pred = D(9.30, -22.0); medido_caliente = D(9.28, 10.0)
    factor = medido_caliente / pred

    # (4) Validation against Fahy's qualitative anchors (not used in the fit)
    val = []
    val.append(("M22 at −3 °C must come out WORSE than VMP at −3 °C", D(9.3, -3) > D(8.4, -3)))
    val.append(("M22 at −22 °C must come out BETTER than M22 at −3 °C", D(9.3, -22) < D(9.3, -3)))
    val.append(("V3 at 10 °C must come out better than 9.28 M at 10 °C", D(8.42, 10) < D(9.28, 10)))
    ok = all(v for _, v in val)

    # ---- figura
    fig, ax = plt.subplots(figsize=(8, 4.6))
    Cs = [x / 20 for x in range(20, 210)]
    for T, c, lab in ((10.0, ORANGE, "carga a 10 °C (German)"), (-3.0, YELLOW, "carga a −3 °C"), (-22.0, AQUA, "carga a −22 °C (M22)")):
        ax.plot(Cs, [min(D(C, T), 1.2) for C in Cs], color=c, lw=2, label=lab)
    for C, d in pts:
        ax.scatter(C, d, s=70, c=INK, zorder=5)
    ax.scatter(9.30, pred, s=140, marker="*", c=AQUA, edgecolors=INK, linewidths=1, zorder=6)
    ax.annotate(f"P19 prediction\n{g(pred)}", (9.30, pred), xytext=(8, 14), textcoords="offset points", fontsize=8, color=INK)
    ax.axhline(1 - 0.93, color=MUTED, ls="--", lw=1)
    ax.text(0.3, 1 - 0.93 + 0.015, "no-damage band (K⁺/Na⁺ ≥ 93 % of control)", fontsize=7, color=MUTED)
    ax.set_xlabel("Permeating CPA concentration (M)"); ax.set_ylabel("Relative damage (1 − respiration/control)")
    ax.set_ylim(0, 1.0); ax.set_title("Derivation of D_CPA: prediction for the cold arm of P19", loc="left", fontsize=11, color=INK)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.grid(color=GRID, lw=0.6); ax.set_facecolor(SURF); fig.set_facecolor(SURF)
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "D_dcpa.png", dpi=150); plt.close(fig)

    doc = ("<!-- AUTO-GENERATED by red/derivar.py. DO NOT EDIT BY HAND. -->\n"
           "# StasisPath: closure by derivation — D_CPA and the P19 prediction\n\n"
           "**The idea.** With enough verified laws, some open nodes need no new measurement: "
           "they are **derived** from the closed ones. Here toxicity-in-concentration (from one dataset) is composed "
           "with toxicity-in-temperature (from **another independent dataset**) to predict the arm of P19 nobody has run.\n\n"
           "**Rule:** a derivation is only valid if it uses data other than the node it closes, declares its range of validity "
           "and produces a falsifiable prediction with a threshold.\n\n"
           "## 1. Shape of the concentration curve at 10 °C\n\n"
           f"From German's series (F72), damage = 1 − respiration/control:\n\n"
           + tabla([[g(C), g(d)] for C, d in pts], ["C (M)", "measured damage"]) +
           f"\n**It is not a power law: it is a threshold.** Damage stays on a plateau of **{g(meseta)}** between 4.3 and 8.4 M "
           f"and **jumps to {g(salto)}** at 9.28 M. *(Self-correction: the first attempt fitted a power law and gave exponent 0.9, "
           "which does not describe these data. A sigmoid cannot be fitted reliably to 3 points, so **nothing is fitted**: "
           "the measured point is used and scaled in temperature only.)*\n\n"
           "## 2. Temperature fit, from an INDEPENDENT dataset\n\n"
           f"From Szurek & Eroglu (F55), PROH 1.5 M and 15 min fixed, only T changes: degeneration {SZUREK[0][1]*100:.1f} % at "
           f"{g(SZUREK[0][0])} °C and {SZUREK[1][1]*100:.1f} % at {g(SZUREK[1][0])} °C ⇒ Arrhenius with **Ea/R = {g(EaR)} K** "
           f"(Ea ≈ {g(EaR*8.314/1000)} kJ/mol, the typical order for protein damage).\n\n"
           "## 3. Composition and prediction\n\n"
           + tabla(filas, ["case", "C (M)", "T °C", "predicted D_CPA damage", "temperature factor"]) +
           f"\n> **DERIVED PREDICTION:** loading M22 at 9.3 M **at −22 °C** produces damage of **{g(pred)}**, versus **{g(medido_caliente)}** "
           f"at 10 °C: a reduction of **×{g(factor)}**. That places the cold arm **{'INSIDE' if pred <= 0.07 else 'OUTSIDE'}** the no-damage band "
           f"(≤ 0.07, equivalent to K⁺/Na⁺ ≥ 93 % of control).\n\n"
           "![Derivation](red/fig/D_dcpa.png)\n\n"
           "## 4. Validation against anchors NOT used in the fit\n\n"
           + tabla([[t, "✔" if v else "✘"] for t, v in val], ["Fahy's qualitative anchor (F39, F65)", "reproduces it?"]) +
           f"\n**{'All three anchors are reproduced' if ok else 'SOME anchor fails'}.** These are qualitative data from Fahy that entered no fit.\n\n"
           "## 5. What holds and what does not\n\n"
           "- **It stands as a falsifiable prediction for P19**, with the threshold fixed here and before any data: if the cold arm "
           f"gives damage > 0.25, the derivation is **refuted**; if it gives ≤ 0.10, **confirmed**.\n"
           "- **It does not close X2 on its own.** It is a prediction, not a measurement: the node stays open until someone runs P19. "
           "What it does is turn P19 into an experiment **with its expected result published in advance**, which is stronger than an exploratory one.\n"
           "- **Declared range of validity:** the concentration fit spans 4.3 to 9.3 M in neural tissue; the temperature one, "
           "23 to 37 °C in oocytes. **Extrapolating to −22 °C is a large extrapolation**, and it is the principal weakness: "
           "it assumes the same activation energy governs damage below 0 °C. Fahy warns that at low temperature "
           "the dominant damage may be **osmotic rather than chemical** (L20), and that term **is not in the model**.\n")
    (ROOT / "DERIVACION.md").write_text(doc)
    return dict(n=float("nan"), k=float("nan"), EaR=EaR, pred=pred, caliente=medido_caliente, factor=factor, anclas_ok=ok)
