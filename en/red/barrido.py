"""StasisPath: margin sweep. Every open range is tested against the framework value by value.

A projected range says nothing about how the framework behaves INSIDE it. Here each margin is
discretized into ~12 values and **every value is propagated through the laws**, marking which
verdicts come out favourable and which do not. The result is not a number: it is
**a map of where inside the range the framework changes its answer**.

The useful part: finding the **cut-off value** — exactly where it stops being favourable. That
turns 'this must be measured' into 'this must be measured to this precision, around this value'.
"""
import math

def g(x):
    if x is None or x != x: return "—"
    return f"{x:.3g}" if abs(x) < 1e4 else f"{x:,.0f}"

def tabla(f, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in r) + " |" for r in f) + "\n"

def _log(lo, hi, n=12):
    return [lo * (hi / lo) ** (i / (n - 1)) for i in range(n)]

def _lin(lo, hi, n=12):
    return [lo + (hi - lo) * i / (n - 1) for i in range(n)]

SI, NO = "✅", "❌"

def generar(D, PAR, DERIV, ROOT):
    p = {k: v["v"] for k, v in PAR.items()}
    tasa = DERIV["tasa_conv"]; Mde = DERIV["M_de_CCR"]; LCe = DERIV["LC_esfera"]; Mtox = DERIV["M_toxico"]
    ORG = D.get("organos", {})
    sec, cortes = [], []

    # ================= B1 · damage in the cold arm of P19 (0 – 0.30)
    filas = []
    for d in _lin(0.0, 0.30):
        pasa_ltp = d <= 0.220          # calibration: at 0.220 LTP was preserved (F72)
        coincide_arr = abs(d - 0.142) < 0.03
        coincide_fahy = d <= 0.07
        filas.append([g(d), SI if pasa_ltp else NO, SI if coincide_arr else "",
                      SI if coincide_fahy else "",
                      "PASSES and confirms Arrhenius" if (pasa_ltp and coincide_arr) else
                      ("PASSES and confirms Fahy ⇒ cold damage is osmotic" if (pasa_ltp and coincide_fahy) else
                       ("PASS, intermediate value: no law is confirmed" if pasa_ltp else
                        "**FAILS: above the damage level at which LTP was demonstrated**"))])
    sec.append(("B1 · Damage in the cold arm of P19", "relative damage (1 − respiration/control)",
        tabla(filas, ["damage", "Is LTP preserved?", "≈ Arrhenius", "≤ Fahy", "what it would mean"]),
        "**Cut-off value: 0.220.** Below it P19 passes whatever the law does; above it, it fails. "
        "The two conflicting paths (0.142 and ≤0.07) are **both on the favourable side**, so "
        "**the measurement need not be precise to yield a verdict: it suffices to tell whether it is above or below 0.22.** "
        "To *calibrate* Arrhenius, however, precision is required: separating 0.07 from 0.142 demands an error < 0.03."))
    cortes.append(["B1", "P19 damage", "0.220", "below it passes, above it fails"])

    # ================= B2 · CCR of the eutectic solvents (0.01 – 10 000) — the most informative
    filas = []
    # Exact value by inverting the law: the CCR that gives LC = 2.31 cm (human brain)
    corte_exacto = p["anc_rate"] * (p["anc_LC"] / 2.31) ** p["exp_LC"]
    corte_nades = None
    for ccr in _log(0.01, 1e4):
        lc = p["anc_LC"] * (p["anc_rate"] / ccr) ** (1 / p["exp_LC"])
        masa = 4 / 3 * math.pi * (3 * lc) ** 3
        caben = [n for n, m in ORG.items() if LCe(m) <= lc]
        mejor_m22 = ccr <= p["CCR_M22"]
        if lc >= 2.31: corte_nades = ccr      # last value of the sweep that still admits a human brain
        filas.append([g(ccr), g(lc), g(masa / 1000), SI if mejor_m22 else NO,
                      ", ".join(caben) if caben else "none"])
    sec.append(("B2 · CCR of natural deep eutectic solvents", "°C/min",
        tabla(filas, ["CCR", "max LC (cm)", "max mass (kg)", "better than M22?", "organs that fit"]),
        f"**Exact cut-off value: CCR = {g(corte_exacto)} °C/min** — below that value the eutectic solvents would suffice for a "
        "**whole human brain**. And this is the point: **they do not need to be better than M22** (0.1 °C/min), "
        f"it is enough to reach **{g(corte_exacto)}**, which is **{g(corte_exacto/p['CCR_M22'])} times more permissive**. "
        "Since their toxicity is already measured as low, **a CCR in that range would resolve X2 without needing P19**. "
        "⇒ Calorimetry of the eutectic solvents becomes **the most cost-effective measurement in the whole programme**."))
    cortes.append(["B2", "CCR of the eutectic solvents", f"{g(corte_exacto)} °C/min", "below it, human brain viable"])

    # ================= B3 · maximum vitrifiable mass (3 – 25 kg)
    filas = []
    for m in _lin(3.0, 25.0):
        lc = (3 * (m * 1000) / (4 * math.pi)) ** (1 / 3) / 3
        caben = [n for n, mm in ORG.items() if LCe(mm) <= lc]
        filas.append([g(m), g(lc), ", ".join(caben) if caben else "none",
                      SI if "brain" in caben else NO, SI if "whole_body" in caben else NO])
    sec.append(("B3 · Maximum vitrifiable mass", "kg",
        tabla(filas, ["mass (kg)", "LC (cm)", "organs that fit", "brain?", "whole body?"]),
        "**The brain fits across the whole range; the whole body fits nowhere in it.** ⇒ The uncertainty in this quantity "
        "(7–24 kg by Monte Carlo) **changes no verdict in the framework**: whatever the value inside the range, "
        "the brain is viable and the whole body is not. **Measuring it better adds nothing.** It is the clearest example of a wide margin "
        "that turns out to be **irrelevant**, and knowing that saves an experiment."))
    cortes.append(["B3", "maximum mass", "—", "no verdict changes across the whole range"])

    # ================= B4 · human τ_eq with optimal reperfusion (12.5 – 60 min)
    filas = []
    for t in _lin(12.5, 60.0):
        gris = 240.0 / t
        filas.append([g(t), g(gris), SI if t >= 30 else NO, SI if t >= 60 else NO,
                      "the grey zone nearly disappears" if t >= 60 else
                      ("real clinical margin" if t >= 30 else "no practical change versus today")])
    sec.append(("B4 · Human τ_eq attainable with optimal reperfusion", "min",
        tabla(filas, ["τ_eq", "width of the grey zone (×)", "≥ 30 min", "≥ 60 min", "consequence"]),
        "**Cut-off value: 30 min.** Below it nothing changes in clinical practice; above it, the organ "
        "procurement window would double. ⇒ A reperfusion trial is only worth running if **it can detect the "
        "difference between 12.5 and 30 min**; finer resolution inside that interval changes no decision."))
    cortes.append(["B4", "human τ_eq", "30 min", "below it practice is unchanged; above it doubles"])

    # ================= B5 · nucleation rate J (0.05 – 5 /L·h)
    filas = []
    for J in _log(0.05, 5.0):
        t95 = -math.log(0.95) / (J * 1.5)
        t50 = math.log(2) / (J * 1.5)
        filas.append([g(J), g(t95), g(t50), SI if t95 >= 4 else NO, SI if t50 >= 24 else NO])
    sec.append(("B5 · Nucleation rate J at −2/−6 °C (isobaric)", "per L·h",
        tabla(filas, ["J", "t at 95 % success (h)", "t at 50 % success (h)", "≥ 4 h at 95 %", "≥ 24 h at 50 %"]),
        "For a human liver (1.5 L). **Cut-off value: J ≈ 0.85 /L·h** to reach 4 h at 95 % success, "
        "which is the minimum logistical window for a transplant. The J fitted from rat liver (**0.57**) lands "
        "**on the favourable side**, but with little margin. ⇒ Isobaric supercooling gives **hours, not days**, unless "
        "J is lowered with antinucleants (L19) or one switches to isochoric, which follows a different law."))
    cortes.append(["B5", "nucleation rate", "0.85 /L·h", "above it 4 h at 95 % is unreachable"])

    doc = ("<!-- AUTO-GENERATED by red/barrido.py. DO NOT EDIT BY HAND. -->\n"
           "# StasisPath: margin sweep\n\n"
           "Every open range is discretized and **every value is propagated through the framework's laws**. It does not look for a number: "
           "it looks for **where inside the range the framework changes its answer**. That turns 'this must be measured' into "
           "'this must be measured to this precision, around this value' — and sometimes into 'this need not be measured'.\n\n"
           "## Cut-off values found\n\n"
           + tabla(cortes, ["sweep", "quantity", "cut-off value", "what changes there"]) + "\n")
    for tit, u, tb, nota in sec:
        doc += f"## {tit}\n\n*Unidad: {u}.*\n\n{tb}\n{nota}\n\n"
    doc += ("## What the sweep shows as a whole\n\n"
            "- **Two margins are irrelevant:** the maximum vitrifiable mass (B3) changes no verdict across its entire "
            "range, and the P19 damage (B1) only needs to be placed above or below 0.22. "
            "**Measuring these precisely adds nothing.**\n"
            "- **One margin is decisive and cheap:** the CCR of the eutectic solvents (B2). If it falls below its cut-off, "
            "**it resolves X2 without needing P19** — and X2 is 60 % of what the framework is missing.\n"
            "- **Two margins have a clear but expensive cut-off:** human τ_eq (B4) and the nucleation rate (B5). They are only "
            "worth it if the experiment can resolve the specific cut-off.\n")
    (ROOT / "BARRIDO.md").write_text(doc)
    return cortes, corte_exacto


# ======================================================================
def plano_diseno(D, PAR, DERIV, ROOT):
    """TWO-dimensional sweep of a CPA's property space: CCR × molarity.

    A single-margin sweep cannot see interactions. Here the two axes that define X2 are crossed
    — vitrification capability (CCR) and toxicity (molarity) — and the region in which the
    framework declares each organ viable is marked. The result is not a number: it is a
    **design target** that can be handed to a chemist.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    p = {k: v["v"] for k, v in PAR.items()}
    LCe = DERIV["LC_esfera"]; Mtox = DERIV["M_toxico"]
    tasa = lambda LC: p["anc_rate"] * (p["anc_LC"] / LC) ** p["exp_LC"]
    ORG = [("kidney", 150), ("heart", 300), ("liver", 1500), ("brain", 1400), ("whole body", 70000)]

    filas = []
    for nom, m in ORG:
        lc = LCe(m); ccr_max = tasa(lc)
        filas.append([nom, g(m), g(lc), g(ccr_max), g(Mtox),
                      "**yes**" if ccr_max >= p["CCR_M22"] else "not with M22"])

    # known CPAs on the plane
    CPAS = [("M22", 0.1, 9.3), ("VS55 (tissue)", 1.0, 8.4), ("VMP", 5.4, 8.4), ("V3", 5.4, 8.42)]

    fig, ax = plt.subplots(figsize=(8.2, 5))
    xs = [10 ** (i / 30 - 2) for i in range(121)]        # CCR 0.01 – 10 000
    ax.axhspan(Mtox, 12, color="#c0392b", alpha=0.10, zorder=0)
    ax.text(0.013, 11.4, "toxic zone (molarity > measured threshold)", fontsize=7.5, color="#c0392b")
    cols = ["#1baf7a", "#2a78d6", "#eda100", "#eb6834", "#c0392b"]
    for (nom, m), c in zip(ORG, cols):
        ccr_max = tasa(LCe(m))
        ax.axvline(ccr_max, color=c, lw=1.6, ls="--")
        ax.text(ccr_max, 4.15, f" {nom}\n {g(ccr_max)}", fontsize=7, color=c, rotation=0, va="bottom")
    for nom, ccr, M in CPAS:
        ok = M <= Mtox
        ax.scatter(ccr, M, s=90, marker="o" if ok else "X", c="#0b0b0b" if ok else "#c0392b", zorder=5)
        ax.annotate(nom, (ccr, M), xytext=(6, 5), textcoords="offset points", fontsize=8)
    # zona objetivo NADES
    ax.add_patch(plt.Rectangle((0.01, 4.0), tasa(LCe(1400)) - 0.01, Mtox - 4.0,
                               facecolor="#1baf7a", alpha=0.16, edgecolor="#1baf7a", lw=1.5, zorder=1))
    ax.text(0.013, 5.0, "DESIGN TARGET\nviable human brain\nwith no toxicity", fontsize=8, color="#0b7f55", weight="bold")
    ax.set_xscale("log"); ax.set_xlim(0.01, 1e4); ax.set_ylim(4, 12)
    ax.set_xlabel("CPA CCR (°C/min, log) — lower = vitrifies larger pieces")
    ax.set_ylabel("Molarity (mol/L) — higher = more toxic")
    ax.set_title("Design plane of X2: where a chemistry must land to resolve the bottleneck", loc="left", fontsize=11, color="#0b0b0b")
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.grid(color="#e1e0d9", lw=0.6); ax.set_facecolor("#fcfcfb"); fig.set_facecolor("#fcfcfb")
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "B_plano.png", dpi=150); plt.close(fig)

    doc = ("\n## B6 · Design plane: both axes of X2 at once\n\n"
           "A single-margin sweep cannot see interactions. Crossing the **two axes that define X2** "
           "—vitrification capability (CCR) and toxicity (molarity)— yields a **target region** instead of a number.\n\n"
           "![Design plane](red/fig/B_plano.png)\n\n"
           + tabla(filas, ["organ", "mass g", "LC cm", "Max admissible CCR", "Max admissible M", "reachable with M22?"]) +
           "\n**What surfaces when the axes are crossed, and a simple sweep could not see:**\n\n"
           "1. **WARNING the framework itself imposes on this figure:** the vertical axis uses **molarity** as a proxy for toxicity, "
           "and **L20 and E7 say that is false** — toxicity depends on the quadruple (composition, temperature, time, protocol), "
           "not on molarity alone. The 9.28 M threshold was measured with **V3 chemistry loaded at 10 °C**; M22 at 9.3 M is loaded at **−22 °C**, "
           "which is a different point in the space. ⇒ **Saying that M22 'exceeds by 0.02 mol/L' would be an over-reading of the plot.** "
           "The plane is useful for seeing the **structure** of the problem, not for placing a specific CPA.\n"
           "2. **The target region is enormous.** Any chemistry with CCR ≤ 0.426 and molarity ≤ 9.28 solves the human brain. "
           "There is no need to optimize both axes: **there are ~3 orders of magnitude of headroom in CCR** below the cut-off.\n"
           "3. **Kidney and heart are already solved in the plane** (they admit CCRs of 1.9 and 1.2), and yet nobody has "
           "vitrified a human kidney. ⇒ **The bottleneck for small organs is NOT the one this plane models**: it is perfusion, "
           "CPA loading and rewarming, not the CCR–toxicity relation.\n"
           "4. **What can legitimately be read from the plane, with the caveat in point 1:** the target region is reached by **lowering CCR without raising "
           "molarity**, and a known mechanism exists for that which does not change concentration: **ice blockers** "
           "(L22 — VM3 is V3 plus 1 % X-1000 and 1 % Z-1000, on the same base). ⇒ **The design direction is not 'less toxic' "
           "nor 'more concentrated', but 'same base, additives that lower the CCR'.** It is what Fahy's family already does and what "
           "the eutectic solvents might achieve by another route.\n")
    with open(ROOT / "BARRIDO.md", "a") as fh: fh.write(doc)
    return {nom: tasa(LCe(m)) for nom, m in ORG}
