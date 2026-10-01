"""StasisPath: precision of the ranges. Methods to narrow what triangulation leaves open.

Four tools, chosen because **they can be applied with the data already in hand**:

1. **Biot number** — checks whether C3's hypothesis (conduction-limited regime, rate ∝ LC⁻²)
   is valid at each scale. Where it is not, the law changes exponent.
2. **Monte Carlo** — propagates parameter uncertainty and returns a distribution instead of a
   corner-derived range, with percentiles.
3. **Sensitivity analysis on a contradiction** — how wrong each assumption would have to be for
   the intersection to stop being empty.
4. **Poisson nucleation** — converts a single survival observation into a bound on the rate J(T)
   and a probability, instead of a point.

What is NOT implemented and why: Kissinger/Ozawa/Avrami require calorimetry data we do not have;
Kaplan-Meier and Cox require times-to-failure nobody has published. They are left declared as
'applicable once the data arrives'.
"""
import math, random, statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA, RED = "#2a78d6", "#eb6834", "#1baf7a", "#c0392b"

H_CONV = 100.0    # W/m²K — coefficient declared in Bischof's model (F2)
K_CPA = 0.40      # W/mK — conductivity of aqueous CPA solution (order of magnitude)

def g(x):
    if x is None or x != x: return "—"
    return f"{x:.3g}" if abs(x) < 1e4 else f"{x:,.0f}"

def tabla(f, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in r) + " |" for r in f) + "\n"

def biot(LC_cm, h=H_CONV, k=K_CPA): return h * (LC_cm / 100) / k
LC_CRIT = K_CPA / H_CONV * 100    # cm donde Bi = 1

def factor_regimen(LC1, LC2):
    """Conduction penalty from LC1 to LC2, respecting the regime change at Bi=1."""
    a, b = sorted((LC1, LC2))
    if b <= LC_CRIT: return b / a                      # convection: LC⁻¹
    if a >= LC_CRIT: return (b / a) ** 2               # conduction: LC⁻²
    return (LC_CRIT / a) * (b / LC_CRIT) ** 2          # mixto

def generar(D, PAR, DERIV, ROOT):
    p = {k: v["v"] for k, v in PAR.items()}
    rng = {k: v["r"] for k, v in PAR.items()}
    sec = []

    # ---------------------------------------------------- 1. Biot
    casos = [("hippocampal slices (350 µm)", 0.035 / 3), ("mouse brain (German)", 0.152),
             ("rat kidney", 0.36), ("human kidney", 0.88), ("3 L bag (C3 anchor)", p["anc_LC"]),
             ("human brain", 2.31), ("whole body", p["LC_body"]), ("trunk", p["LC_trunk"])]
    filas = []
    for nom, lc in casos:
        Bi = biot(lc)
        reg = "conduction — **LC⁻² holds**" if Bi >= 1 else ("transition" if Bi > 0.3 else "convection — **LC⁻² does NOT hold**")
        filas.append([nom, g(lc), g(Bi), reg])
    f_mal = (2.31 / 0.152) ** 2
    f_bien = factor_regimen(0.152, 2.31)
    sec.append(("1. Biot number: where does our law hold?",
        "C3's exponent is not universal. The law **rate ∝ LC⁻²** assumes a **conduction-limited** regime (Bi ≫ 1). "
        "If Bi ≪ 1 the body is nearly isothermal and the rate is set by surface convection: it scales as **LC⁻¹**.\n\n"
        f"With h = {g(H_CONV)} W/m²K (declared in F2) and k ≈ {g(K_CPA)} W/mK, the Bi = 1 boundary lies at "
        f"**LC = {g(LC_CRIT)} cm**.\n\n" + tabla(filas, ["system", "LC cm", "Bi", "regime"]) +
        f"\n> **Good news:** all the framework's extrapolations to human organs (LC {g(p['LC_kidneyH'])}–{g(p['LC_trunk'])} cm) "
        "fall in the **conduction** regime, where LC⁻² is correct. F1, F2, C3 and C6 are validated over their range of use.\n\n"
        f"> ⚠ **CORRECTION of an error of our own:** in the scaling module the conduction penalty from mouse brain "
        f"(LC 0.152 cm) to human (2.31 cm) was computed by applying LC⁻² across the whole path, giving **×{g(f_mal)}**. But that path "
        f"**crosses the regime boundary**: respecting it gives **×{g(f_bien)}**. **The difficulty was overestimated by ×{g(f_mal/f_bien)}.** "
        "The deficit for repeating German's protocol in a human brain does not change (it is computed from the human rate, not by "
        "scaling from the mouse), but the statement 'the human brain is ×231 worse in conduction' was incorrect."))

    # ---------------------------------------------------- 2. Monte Carlo
    random.seed(7)
    N = 20000
    def muestra(k):
        lo, hi = rng[k]; c = p[k]
        # triangular with mode at the central value: respects the declared range without inventing normality
        return random.triangular(lo, hi, c)
    Mtox = DERIV["M_toxico"]
    vals = []
    for _ in range(N):
        q = {k: muestra(k) for k in ("anc_LC", "anc_rate", "exp_LC", "CCR_M22", "CCR_VS55", "CCR_VMP")}
        b = (math.log10(q["CCR_M22"]) - (math.log10(q["CCR_VS55"]) + math.log10(q["CCR_VMP"])) / 2) / 0.9
        a = (math.log10(q["CCR_VS55"]) + math.log10(q["CCR_VMP"])) / 2 - b * 8.4
        tasa = lambda LC: q["anc_rate"] * (q["anc_LC"] / LC) ** q["exp_LC"]
        lc = next((i / 100 for i in range(25, 3000) if (math.log10(tasa(i / 100)) - a) / b > Mtox), None)
        if lc: vals.append(4 / 3 * math.pi * (3 * lc) ** 3 / 1000)
    vals.sort()
    pc = lambda q_: vals[int(q_ * (len(vals) - 1))]
    sec.append(("2. Monte Carlo: a distribution instead of corners",
        f"Corners give a range; Monte Carlo gives **where it concentrates**. {N:,} samples with a triangular distribution "
        "within each parameter's declared range (mode at the central value: it respects what is declared without assuming normality).\n\n"
        "**Maximum vitrifiable mass (the F2 frontier):**\n\n"
        + tabla([["percentil 5", f"{g(pc(0.05))} kg"], ["percentil 25", f"{g(pc(0.25))} kg"],
                 ["**mediana**", f"**{g(pc(0.5))} kg**"], ["percentil 75", f"{g(pc(0.75))} kg"],
                 ["percentil 95", f"{g(pc(0.95))} kg"]], ["percentile", "mass"]) +
        f"\n> The corner range was wide; the median is at **{g(pc(0.5))} kg** and the central 50 % lies between "
        f"**{g(pc(0.25))} and {g(pc(0.75))} kg**. The distribution is **right-skewed**: the typical value is lower "
        "than the mean, so reporting the mean would be optimistic."))

    # ---------------------------------------------------- 3. Sensitivity on contradiction I1
    # Arrhenius gives 0.142; Fahy's anchors require <= 0.07. What would have to change?
    dano_medido, T_ger, T_frio = 0.536, 10.0, -22.0
    obj = 0.07
    EaR_nec = math.log(dano_medido / obj) / (1 / (T_frio + 273.15) - 1 / (T_ger + 273.15))
    EaR_act = 2952.0
    filas = [["Ea/R used (from oocytes, F55)", f"{g(EaR_act)} K", "gives damage 0.142"],
             ["Ea/R needed to reach 0.07", f"{g(EaR_nec)} K", f"×{g(EaR_nec/EaR_act)} the current value"],
             ["Damage measured at 9.28 M and 10 °C", g(dano_medido), "F72, not disputed"]]
    sec.append(("3. Sensitivity: what would resolve the I1 contradiction",
        "Triangulation found that Arrhenius predicts 0.142 while Fahy's anchors require ≤ 0.07. "
        "Instead of choosing by eye, **what would have to be true** for there to be no clash is computed.\n\n"
        + tabla(filas, ["quantity", "value", "note"]) +
        f"\n> **For both paths to fit, the activation energy of damage would have to be ×{g(EaR_nec/EaR_act)} "
        f"the value measured in oocytes** (from {g(EaR_act)} to {g(EaR_nec)} K, that is from ~24.5 to ~{g(EaR_nec*8.314/1000)} kJ/mol). "
        "That is **not implausible**: 24.5 kJ/mol is low for protein damage, and the value comes from a system (oocyte) and a "
        "temperature range (23–37 °C) that are very different. ⇒ **The likeliest hypothesis is that the Arrhenius extrapolation "
        "underestimates the activation energy, not that Fahy is wrong.** A concrete prediction P19 can check."))

    # ---------------------------------------------------- 4. Poisson nucleation
    V1, t1 = 0.2, 5.0     # L, h — pig kidney at −2 °C without nucleating (F20)
    J_max = 3.0 / (V1 * t1)          # si P(no nuclear) ≥ 5 %, entonces J·V·t ≤ 3
    filas = []
    for V, nom in ((0.2, "pig kidney"), (1.5, "human liver"), (70.0, "whole body")):
        t_50 = math.log(2) / (J_max * V)
        t_95 = -math.log(0.95) / (J_max * V)
        filas.append([nom, g(V), g(t_95), g(t_50)])
    sec.append(("4. Nucleation as a Poisson process: from one observation to a probability",
        "A single 'did not nucleate' observation does not give a number, but **it does give a bound** if modelled as Poisson: "
        "P(no nucleation) = exp(−J·V·t). From the pig kidney (0.2 L, 5 h at −2 °C without nucleating) one obtains, with 95 % "
        f"confidence, **J ≤ {g(J_max)} per L·h**.\n\n"
        + tabla(filas, ["system", "V (L)", "t at 95 % success (h)", "t at 50 % success (h)"]) +
        "\n> I5 thus stops being '≤ 0.67 h' and becomes **a probability curve against time**, which is what a "
        "clinical protocol needs. **Important caveat:** this holds only in the **isobaric** regime; the isochoric system "
        "suppresses nucleation and follows a different law (see I5)."))

    # ---- figura Monte Carlo
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.hist(vals, bins=60, color=BLUE, edgecolor=SURF, linewidth=0.4)
    for q_, c, lab in ((0.05, MUTED, "p5"), (0.5, RED, "mediana"), (0.95, MUTED, "p95")):
        ax.axvline(pc(q_), color=c, lw=1.6 if q_ == 0.5 else 1, ls="-" if q_ == 0.5 else "--")
        ax.text(pc(q_), ax.get_ylim()[1] * 0.92, f" {lab} {g(pc(q_))}", fontsize=7.5, color=c)
    ax.set_xlabel("Maximum vitrifiable mass (kg)"); ax.set_ylabel("frecuencia")
    ax.set_title("Monte Carlo: where the viability frontier concentrates", loc="left", fontsize=11, color=INK)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.grid(axis="y", color=GRID, lw=0.6); ax.set_facecolor(SURF); fig.set_facecolor(SURF)
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "P_montecarlo.png", dpi=150); plt.close(fig)

    doc = ("<!-- AUTO-GENERATED by red/precision.py. DO NOT EDIT BY HAND. -->\n"
           "# StasisPath: precision — narrowing what triangulation leaves open\n\n"
           "Four methods, chosen because **they can be applied with the data already in hand**. "
           "Those requiring data nobody has published are declared at the end rather than applied halfway.\n\n")
    for tit, cuerpo in sec:
        doc += f"## {tit}\n\n{cuerpo}\n\n"
        if tit.startswith("2."): doc += "![Monte Carlo](red/fig/P_montecarlo.png)\n\n"
    doc += ("## Methods that cannot be applied yet, and which datum they lack\n\n"
            + tabla([["Kissinger / Ozawa / Avrami", "crystallization kinetics from calorimetry", "**DSC data for the eutectic solvents** (I2)"],
                     ["Kaplan-Meier / Cox regression", "survival versus ischemia time", "times to failure in a cohort (I4)"],
                     ["Finite elements with real geometry", "thermal field in an organ, not in a sphere", "mesh of a human organ + CPA properties"],
                     ["Inferencia bayesiana completa", "posterior for each parameter instead of a range", "independent replicates; today most are n = 1"]],
                    ["method", "what for", "which datum is missing"]))
    (ROOT / "PRECISION.md").write_text(doc)
    return dict(LC_crit=LC_CRIT, f_mal=f_mal, f_bien=f_bien, mediana=pc(0.5), p5=pc(0.05), p95=pc(0.95), EaR_nec=EaR_nec)
