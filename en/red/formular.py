"""StasisPath: internal formulation. The framework solving itself.

It composes ALREADY verified laws to produce quantitative statements nobody measured
directly. Each formula declares which laws it derives from, its range of validity, and a
falsifiable prediction. Those that do not reach falsifiability are marked as such.

Rule: compose only closed laws (M/V). A formula resting on an open node is reported as
CONDITIONAL, not as derived.
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"

def g(x):
    if x != x: return "—"
    if x == float("inf"): return "∞"
    return f"{x:.3g}" if abs(x) < 1e4 else f"{x:,.0f}"

def tabla(f, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in r) + " |" for r in f) + "\n"

def generar(D, PAR, ROOT):
    p = {k: v["v"] for k, v in PAR.items()}
    rng = {k: v["r"] for k, v in PAR.items()}
    F = []   # (id, title, markdown body, status)

    # ============================ F1. Maximum vitrifiable mass by convection, per CPA
    # Composes C3 (rate ∝ LC^−n anchored) with the CCR of the CPA. LC of an aqueous sphere = r/3.
    rate = lambda LC, q=p: q["anc_rate"] * (q["anc_LC"] / LC) ** q["exp_LC"]
    LCstar = lambda CCR, q=p: q["anc_LC"] * (q["anc_rate"] / CCR) ** (1 / q["exp_LC"])
    masa_de_LC = lambda LC: 4 / 3 * math.pi * (3 * LC) ** 3        # g, esfera de agua
    CPAS = {"M22": (p["CCR_M22"], 9.3), "VS55 (tissue)": (p["CCR_VS55"], 8.4), "VMP": (p["CCR_VMP"], 8.4)}
    filas = []
    for nom, (ccr, M) in CPAS.items():
        lc = LCstar(ccr); m = masa_de_LC(lc)
        # esquinas
        lo = min(LCstar(ccr, {**p, "anc_LC": a, "anc_rate": r, "exp_LC": e})
                 for a in rng["anc_LC"] for r in rng["anc_rate"] for e in rng["exp_LC"])
        hi = max(LCstar(ccr, {**p, "anc_LC": a, "anc_rate": r, "exp_LC": e})
                 for a in rng["anc_LC"] for r in rng["anc_rate"] for e in rng["exp_LC"])
        filas.append([nom, g(ccr), g(M), f"{g(lc)} ({g(lo)}–{g(hi)})", f"{g(m)} ({g(masa_de_LC(lo))}–{g(masa_de_LC(hi))})"])
    F.append(("F1", "Maximum vitrifiable mass by convection, per cryoprotectant",
        "**Derives from:** C3 (cooling ∝ LC⁻ⁿ, anchored on the 3 L bag) + the measured CCRs.\n\n"
        "**Formula:** LC\\* = LC₀ · (rate₀ / CCR)^(1/n) and M\\* = (4/3)π(3·LC\\*)³ for an aqueous sphere.\n\n"
        + tabla(filas, ["CPA", "CCR °C/min", "M (mol/L)", "max LC (cm)", "max mass (g)"]) +
        "\n**Reading:** with convection alone, M22 reaches tens of kg and VMP does not exceed a few grams. "
        "This is the number that was missing to say 'which organ fits which chemistry' without simulating each case.", "derivada"))

    # ============================ F2. Viability theorem: does a chemistry exist for a given organ?
    # Composes F1 with the CCR↔concentration relation (3 points) and with the toxicity threshold (German).
    import statistics
    pts = [(9.3, p["CCR_M22"]), (8.4, p["CCR_VS55"]), (8.4, p["CCR_VMP"])]
    CCR_AGUA = 6.4e6 * 60      # °C/min — pure water, measured by electron cryomicroscopy (F76, L31)
    # log10(CCR) ~ a + b·M  (with 8.4 repeated at two CCRs: averaged in log)
    agg = {}
    for M, c in pts: agg.setdefault(M, []).append(math.log10(c))
    xs = sorted(agg); ys = [statistics.mean(agg[x]) for x in xs]
    b = (ys[1] - ys[0]) / (xs[1] - xs[0]); a = ys[0] - b * xs[0]
    M_de_CCR = lambda CCR: (math.log10(CCR) - a) / b
    UMBRAL_TOX = 9.28          # M — above it, damage jumps (German, F72)
    objetos = [("human kidney", 0.88), ("human heart (~300 g)", 1.2), ("human liver (~1.5 kg)", 1.8),
               ("human brain (1.4 kg)", 2.31), ("whole body (mean)", 3.9), ("trunk", 7.5)]
    filas = []
    for nom, lc in objetos:
        ccr_req = rate(lc); M_req = M_de_CCR(ccr_req)
        veredicto = "**viable**" if M_req <= UMBRAL_TOX else "**requires C > toxic threshold**"
        filas.append([nom, g(lc), g(ccr_req), g(M_req), veredicto])
    # Same calculation as the `derivadas` layer of the YAML (LC_viable / masa_viable): a single definition.
    lc_critico = next((i / 100 for i in range(25, 2000) if M_de_CCR(rate(i / 100)) > UMBRAL_TOX), None)
    m_critico = masa_de_LC(lc_critico) if lc_critico else float("nan")
    F.append(("F2", "Viability theorem: is any chemistry possible for a given organ?",
        "**Derives from:** F1 + the measured CCR↔concentration relation (3 CPAs) + German's toxicity threshold "
        f"({UMBRAL_TOX} M, where basal respiration halves).\n\n"
        f"**Formula:** log₁₀(CCR) = {g(a)} + {g(b)}·M ⇒ to vitrify a given LC requires "
        "M ≥ (log₁₀(CCR_required) − a)/b. If that M exceeds the toxic threshold, **no known chemistry works**.\n\n"
        + tabla(filas, ["object", "LC cm", "required CCR °C/min", "required M (mol/L)", "verdict"]) +
        f"\n> **DERIVED RESULT:** the limit lies at **LC ≈ {g(lc_critico)} cm**, that is a mass of "
        f"**≈ {g(m_critico/1000)} kg**. Above that, the required concentration crosses the threshold where "
        "toxicity escalates. \n\n**What the table says when read carefully:** the human brain requires **8.94 M**, below the threshold, with a margin of only **0.34 M**. The whole body (mean LC) requires **9.20 M**: a margin of **0.08 M**, practically nil. **The trunk is the only one that crosses it** (9.53 M) — and it is precisely the piece C3 already flagged as failing along the pure thermal route. **The derivation reproduces that result from another direction**, which is a cross-check, not a coincidence sought after the fact.\n\n"
        f"**Validation with a third point, from a distant field (L31):** the CCR of **pure water** is {g(CCR_AGUA)} °C/min "
        f"(cryo-electron microscopy). With it, the relation is seen to be **curved**: −0.95 decades/mol between 0 and 8.4 M, but "
        f"**−1.74 between 8.4 and 9.3 M**. ⇒ **Extrapolating with the local slope near 9 M, as F2 does, is the correct choice**, "
        "and it is now justified by evidence rather than by assumption.\n\n"
        + "**Honesty warning:** the CCR↔M line is fitted with **three points and only two distinct concentrations** "
        "(8.4 and 9.3 M). It is the weakest piece of the whole derivation. The result must be read as an **order of magnitude**, "
        "not as a precise frontier, and it is refuted as soon as a CPA with a low CCR at low concentration is measured.\n\n"
        "**And a neighbouring field says that is possible (L29):** tardigrade CAHS proteins form a glass or gel "
        "at **~0.6 mM**, four orders of magnitude below the 8.4–9.3 M of M22 or V3. The CCR↔molarity relation that "
        "underpins F2 **is not a law of nature: it is a property of the chemical class the field chose** (small "
        "molecules). F2 remains valid **within that class**, and that is its real range of validity.", "weak derivation, with chemical-class range"))

    # ============================ F3. τ_eq with regimes and domains
    def tau_eq(T, t, dominio="mamifero"):
        if dominio == "hibernador" and T <= 12: return float("nan")   # L27: ceases to be a function of T
        q = p["Q10"] if T >= 15 else p["Q10_frio"]
        return t * q ** ((T - 37) / 10)
    casos = [("Human DHCA 15 °C, 31 min", 15, 31, "mamifero"), ("Dog flush 10 °C, 120 min", 10, 120, "mamifero"),
             ("Pig 10 °C, 60 min", 10, 60, "mamifero"), ("Euthermic ground squirrel 37 °C, 8 min", 37, 8, "hibernador"),
             ("Ground squirrel in torpor, 5 °C", 5, 1440, "hibernador")]
    filas = [[nm, g(T), g(t), g(tau_eq(T, t, d)) if tau_eq(T, t, d) == tau_eq(T, t, d) else "**not applicable** (L27)"] for nm, T, t, d in casos]
    F.append(("F3", "piecewise τ_eq, with declared domain",
        "**Derives from:** C2 + L2 (Q10 not constant) + L24 (mechanism) + L27 (the hibernator is a different regime).\n\n"
        f"**Formula:** τ_eq = t · Q10(T)^((T−37)/10), with **Q10 = {g(p['Q10'])} above 15 °C** and "
        f"**{g(p['Q10_frio'])} below it**; and **undefined** for hibernators below 12 °C, where metabolism "
        "ceases to be a function of temperature.\n\n" + tabla(filas, ["case", "T °C", "t min", "τ_eq (min at 37 °C)"]) +
        "\n**What it contributes:** it unifies in a single expression what was spread across four laws, **and declares where it does not hold**. "
        "The 'not applicable' cell matters as much as the numbers: it is the error we would make by applying C2 to a cold hibernator.", "derivada"))

    # ============================ F4. Volume × time limit of supercooling
    # L16: nucleation is stochastic; its probability grows with volume and time.
    # Anchors: 3 L at −2 °C would fail at 24-48 h (that is why they went up to −0.5); pig kidney ~0.2 L held 5 h at −2 °C.
    V1, t1, T1 = 0.2, 5.0, -2.0      # L, h, °C  (pig kidney, F20)
    V2, t2, T2 = 0.2, 48.0, -0.5     # they had to raise T for 48 h
    prod1 = V1 * t1
    F.append(("F4", "Volume × time invariant of supercooling",
        "**Derives from:** L16 (cumulative nucleation limits the time, not the minimum temperature) + G7 (cold-injury band).\n\n"
        "**Proposed form:** if nucleation is a Poisson process with rate per unit volume J(T), "
        "the probability of NO nucleation is exp(−J(T)·V·t) ⇒ **the invariant is V·t at fixed T**.\n\n"
        f"**Only anchor available:** pig kidney, {g(V1)} L at {g(T1)} °C for {g(t1)} h ⇒ V·t = {g(prod1)} L·h without nucleating. "
        f"For {g(t2)} h the same group had to raise it to {g(T2)} °C.\n\n"
        "> **PREDICTION (not fully derived):** at −2 °C, a 1.5 L organ (liver) would last only "
        f"≈ {g(prod1/1.5)} h before matching the nucleation dose the kidney accumulated in 5 h.\n\n"
        "**Honest status: this is NOT yet a valid derivation.** There is **a single point**: one datum does not determine J(T) "
        "nor does it verify that the invariant is V·t. It is left written **as a falsifiable hypothesis** because the experiment that would "
        "test it is cheap: supercool two different volumes at the same temperature and see whether the time to nucleation "
        "scales as 1/V.", "hypothesis, not derived"))

    # ============================ F5. Non-monotonic cooling protocol
    Tg = p["Tg"]
    F.append(("F5", "Optimal cooling protocol (non-monotonic)",
        "**Derives from:** L14 (rate conflict) + G7 (0–20 °C cold-injury band) + G3 (Tg and rewarming "
        "profile) + F68 (lowering the rate between storage and Tg reduces stress).\n\n"
        "**Derived rule, in three regimes:**\n"
        "1. **From 37 to 20 °C:** rate unconstrained. There is neither cold injury nor ice risk.\n"
        "2. **From 20 to 0 °C: as fast as possible.** This is the phase-transition band of membrane lipids, "
        "where damage grows with *exposure time* (G7). Exception: if the route is controlled extracellular ice, "
        "cellular dehydration governs here and one must go slowly (0.1–1 °C/min) — **the two objectives are incompatible "
        "in this band and the route must be chosen before entering it.**\n"
        f"3. **From 0 °C to Tg ({g(Tg)} °C):** above the CPA's CCR, but **no faster than necessary**: excess "
        "of rate only adds a thermal gradient.\n"
        f"4. **Below Tg:** slow (< 1 °C/min) and far from Tg in storage, because storing just below Tg "
        "**doubles the CWR** needed afterwards (F2).\n\n"
        "**What it contributes:** it is the only one of these formulas that is directly **actionable in a protocol**, and it comes from composing "
        "four laws that came from four different fields (human reproduction, organ cryobiology, materials and "
        "neurociencia).", "derivada cualitativa"))

    # ---- figura de F2
    fig, ax = plt.subplots(figsize=(8, 4.6))
    LCs = [x / 50 for x in range(25, 500)]
    ax.plot(LCs, [M_de_CCR(rate(lc)) for lc in LCs], color=BLUE, lw=2, label="concentration needed to vitrify")
    ax.axhline(UMBRAL_TOX, color=ORANGE, lw=2, ls="--", label=f"measured toxicity threshold ({UMBRAL_TOX} M)")
    if lc_critico: ax.axvline(lc_critico, color=MUTED, lw=1)
    for nom, lc in objetos:
        ax.scatter(lc, M_de_CCR(rate(lc)), s=55, c=INK, zorder=4)
        ax.annotate(nom, (lc, M_de_CCR(rate(lc))), xytext=(5, -10), textcoords="offset points", fontsize=7, color=INK2)
    ax.set_xlabel("Characteristic length LC (cm)"); ax.set_ylabel("Required CPA concentration (mol/L)")
    ax.set_ylim(7, 12); ax.set_title("F2 · Where the required chemistry crosses the toxic threshold", loc="left", fontsize=11, color=INK)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.grid(color=GRID, lw=0.6); ax.set_facecolor(SURF); fig.set_facecolor(SURF)
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "F_viabilidad.png", dpi=150); plt.close(fig)

    doc = ("<!-- AUTO-GENERATED by red/formular.py. DO NOT EDIT BY HAND. -->\n"
           "# StasisPath: internal formulation — the framework solving itself\n\n"
           "Each formula composes **already closed** laws to produce a quantitative statement nobody measured directly. "
           "What it derives from, its range of validity, and whether it reaches a falsifiable prediction are all declared. "
           "**A formula resting on an open node is marked conditional, not derived.**\n\n"
           "| formula | status |\n|---|---|\n" + "\n".join(f"| **{i} · {t}** | {st} |" for i, t, _, st in F) + "\n\n")
    for i, t, body, st in F:
        doc += f"## {i} · {t}\n\n*Status: {st}.*\n\n{body}\n\n"
        if i == "F2": doc += "![F2](red/fig/F_viabilidad.png)\n\n"
    doc += ("## What this formulation achieved\n\n"
            "- **Two new falsifiable formulas** (F1, F2) answering questions that previously required case-by-case simulation.\n"
            "- **One unification** (F3): four laws in one expression, with its domain of validity declared.\n"
            "- **One actionable protocol rule** (F5), composed from four different fields.\n"
            "- **One hypothesis honestly marked as not derived** (F4): with a single point there is no law, and that is stated.\n\n"
            "**What it does NOT achieve:** none of these formulas closes X2. Deriving produces **predictions**, not measurements. "
            "The framework can now say what it expects to find and where it would break if it is wrong — which is exactly "
            "what it would take for the experiment to be worth more.\n")
    (ROOT / "FORMULACION.md").write_text(doc)
    return dict(lc_critico=lc_critico, m_critico=m_critico, a=a, b=b, n_formulas=len(F))
