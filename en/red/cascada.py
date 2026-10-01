"""StasisPath: the cascade to the end — what probability does the framework assign to P19 passing?

`DERIVACION.md` composes toxicity-in-concentration with toxicity-in-temperature and predicts
the cold arm of P19 with **a point value: 0.142**. A point value cannot honestly be compared with
a threshold. Here the same cascade is walked **with all the uncertainty propagated**, step by step,
and it answers the question the framework has never answered:

    **With what probability, by its own laws and its own ranges, does the framework believe P19 passes?**

That does NOT close X2, and the module is written so it cannot be mistaken for a closure:

  - The output is a **probability of belief**, not a measurement. It is labelled as such on every line.
  - It is accompanied by the **track record** of this same kind of prediction. The framework predicted
    I2 = 0.3 °C/min and the measured value turned out to be > 30: **a factor of 100 in error**. A cascade
    producing a very confident belief, inside a framework whose last prediction of this kind was wrong by
    two orders of magnitude, is information about the cascade, not about the chemistry.
  - It declares **which link has no datum**, which is where the cascade stops being calculation.

Contradiction I1 is the heart of the matter and here it is propagated rather than hidden: the framework has
**two paths that disagree by a factor of ~2** about the same quantity (Arrhenius gives 0.142; Fahy's
anchors require ≤ 0.07). An honest calculation does not pick one: it samples both.

Output: CASCADA.md + red/fig/CA_cascada.png. Called by motor.py.
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"

N = 200000
SEMILLA = 20260926

# --- MEASURED anchors feeding the cascade (all already in the network) ---
D_GERMAN_10C = 0.536      # damage measured at 9.28 M and 10 °C (F72)
D_LTP_OK     = 0.220      # damage level with DEMONSTRABLY preserved LTP (F46: 138.1 % vs 157.7 n.s.)
D_FAHY_MAX   = 0.070      # bound from Fahy's anchors for 'no damage'
EaR_OVO      = 2952.0     # Ea/R from oocytes (F55), measured between 23 and 37 °C
EaR_NECES    = 4520.0     # Ea/R that would make both paths fit (PRECISION.md)
T_CAL        = (23.0, 37.0)   # range over which Ea/R is calibrated
T_OBJ        = -22.0          # temperature of arm C of P19

def g(x):
    return f"{x:.3g}"

def tabla(filas, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in f) + " |" for f in filas) + "\n"

def generar(D, PAR, DERIV, ROOT):
    rng = np.random.default_rng(SEMILLA)

    # ---- link 1: the activation energy. Contradiction I1 lives here.
    # Path A (Arrhenius on oocytes): EaR ~ 2952, with the dispersion of a 2-point fit.
    # Path B (Fahy's anchors): requires EaR ~ 4520 for the damage at -22 to fall to 0.07.
    # Neither is chosen: a 50/50 mixture is sampled, which is what 'open contradiction' means.
    camino = rng.random(N) < 0.5
    eaA = rng.normal(EaR_OVO, EaR_OVO * 0.25, N)      # ±25 %: ajuste de dos puntos
    eaB = rng.normal(EaR_NECES, EaR_NECES * 0.25, N)
    EaR = np.where(camino, eaA, eaB)
    EaR = np.clip(EaR, 500, 12000)

    # ---- link 2: thermal extrapolation outside the calibrated range
    # factor = exp(-EaR (1/T_obj - 1/T_ref)) with T in kelvin
    Tref, Tobj = 10.0 + 273.15, T_OBJ + 273.15
    factor = np.exp(-EaR * (1.0 / Tobj - 1.0 / Tref))
    # penalty for extrapolating: the model was calibrated between 23 and 37 °C and is used at -22 °C.
    # A log-normal multiplicative bias is sampled, growing with the extrapolation distance.
    dist = (min(T_CAL) - T_OBJ) / (max(T_CAL) - min(T_CAL))   # ~3.2 calibration ranges
    sesgo = np.exp(rng.normal(0, 0.25 * dist, N))
    dano = D_GERMAN_10C * factor * sesgo

    # ---- link 3: oocyte -> neural tissue transfer (no datum)
    # Ea/R comes from OOCYTES. That the same activation energy holds for CA1 LTP has
    # no datum behind it. It is modelled as a wide transfer factor and declared.
    transf = np.exp(rng.normal(0, 0.35, N))
    dano_neural = dano * transf

    pasa = dano_neural < D_LTP_OK
    p_pasa = float(pasa.mean())
    q = lambda a: float(np.quantile(dano_neural, a))

    # sensitivity: what happens if the contradiction resolves in favour of each path?
    p_A = float((dano_neural[camino] < D_LTP_OK).mean())
    p_B = float((dano_neural[~camino] < D_LTP_OK).mean())
    # and what if there were no transfer or extrapolation uncertainty?
    dano_limpio = D_GERMAN_10C * factor
    p_limpio = float((dano_limpio < D_LTP_OK).mean())

    # ================================================================ TODOS LOS CAMINOS DEL MARCO
    # The Arrhenius chain is ONE of the paths. The framework has more, and the user is right that
    # they should be made to speak. But they are not independent: several rest on the SAME German
    # datum. Combining them as if they were inflates confidence, and that is the interesting result.
    #
    # shared anchor: the German dataset (F72/F46). It is sampled ONCE and reused
    # in all the paths that depend on it, which is what creates the correlation.
    german_ok = rng.normal(1.0, 0.15, N)     # uncertainty of the German dataset itself

    CAMINOS = [
        # (name, P(passes) contributed by that path on its own, anchor, independent of German)
        ("Arrhenius × German's point (I1, path A)", None, "german", False),
        ("Fahy's anchors: M22 tolerable at −22 °C in kidney slice (I1, path B)", None, "fahy", True),
        ("Damage↔LTP calibration: at damage 0.220 LTP was preserved (I1, path C)", None, "german", False),
        ("F47: M22 in rabbit brain, pig brain and human biopsy, NO ice", 0.62, "fahy_brain", True),
        ("F5: rabbit kidney with M22, transplanted and functional (E3)", 0.58, "rabbit", True),
        ("L13/F71: V3 (8.42 M) preserves LTP and M22 is only 10 % more concentrated", 0.70, "german", False),
    ]

    # Paths 1 and 3 are already in the simulation above (dano_neural uses German's point).
    # Paths 4, 5 and 6 contribute evidence that does NOT enter that chain. They are modelled as
    # independent or correlated likelihoods depending on their anchor.
    # --- Correct model: each path is a NOISY OBSERVATION of the same latent fact
    # ('Does M22 preserve neural function?'), not an independent chance of it happening.
    # Combining them with 1-prod(1-p) would treat them as lottery tickets and saturates at 99 %
    # whatever they say. The correct thing is to multiply LIKELIHOOD RATIOS over a
    # prior of 0.5, which is what turns 'p of a path' into 'how much it moves the belief'.
    LR = lambda pr: pr / (1.0 - pr)

    # Within a group sharing an anchor they are NOT multiplied: if the anchor is biased, they all
    # fail together. The STRONGEST likelihood ratio of the group is taken.
    grupos = {}
    grupos.setdefault("german", []).append(LR(p_pasa))   # the simulated chain belongs to the German group
    for nom, pr, anc, _ in CAMINOS:
        if pr is not None:
            grupos.setdefault(anc, []).append(LR(pr))
    lr_honesta = 1.0
    for k, v in grupos.items():
        lr_honesta *= max(v)
    p_honesta = lr_honesta / (1.0 + lr_honesta)

    # Naive: multiply ALL the ratios, as if they shared nothing.
    lr_ingenua = LR(p_pasa)
    for nom, pr, anc, _ in CAMINOS:
        if pr is not None: lr_ingenua *= LR(pr)
    p_ingenua = lr_ingenua / (1.0 + lr_ingenua)

    n_grupos = len(grupos)
    filas_cam = []
    for nom, pr, anc, indep in CAMINOS:
        filas_cam.append([nom, "in the simulated chain" if pr is None else f"{100*pr:.0f} %",
                          "—" if pr is None else f"×{LR(pr):.2f}", anc,
                          "yes" if indep else "**no: shares the German datum**"])

    # ---- figura
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.2), gridspec_kw={"width_ratios": [2, 1]})
    bins = np.logspace(-3, 1, 90)
    ax.hist(dano_neural[camino], bins=bins, color=ORANGE, alpha=0.55, label="path A: Arrhenius on oocytes")
    ax.hist(dano_neural[~camino], bins=bins, color=BLUE, alpha=0.55, label="path B: Fahy's anchors")
    ax.axvline(D_LTP_OK, color="#0e7a55", lw=1.8)
    ax.text(D_LTP_OK * 1.08, ax.get_ylim()[1] * 0.92, f" LTP preserved\n at damage {D_LTP_OK} (measured)",
            fontsize=7.4, color="#0e7a55", va="top")
    ax.axvline(D_FAHY_MAX, color=MUTED, lw=1, ls="--")
    ax.set_xscale("log"); ax.set_xlabel("damage predicted in the cold arm of P19 (derived, NOT measured)", color=INK2)
    ax.set_yticks([]); ax.legend(fontsize=7.2, frameon=False, loc="upper left")
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)

    barras = [("The WHOLE framework,\nhonest combination", p_honesta, AQUA),
              ("the whole framework,\nnaive combination", p_ingenua, "#c0392b"),
              ("the Arrhenius\nchain alone", p_pasa, ORANGE),
              ("no transfer\nuncertainty", p_limpio, MUTED)]
    for i, (lab, v, c) in enumerate(barras):
        ax2.barh(i, v, color=c, height=0.55)
        ax2.text(min(v + 0.02, 0.8), i, f"{100*v:.0f} %", va="center", fontsize=8, color=INK2)
    ax2.set_yticks(range(len(barras))); ax2.set_yticklabels([b[0] for b in barras], fontsize=7.4, color=INK2)
    ax2.set_xlim(0, 1.05); ax2.set_xlabel("P(the framework BELIEVES P19 passes)", color=INK2)
    for sp in ("top", "right", "left"): ax2.spines[sp].set_visible(False)
    for a in (ax, ax2): a.set_facecolor(SURF); a.grid(axis="x", color=GRID, lw=0.6)
    fig.set_facecolor(SURF)
    fig.suptitle("The cascade to the end: a belief with its dispersion, not a number",
                 x=0.02, ha="left", fontsize=11, color=INK)
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "CA_cascada.png", dpi=150); plt.close(fig)

    doc = ("<!-- AUTO-GENERATED by red/cascada.py. DO NOT EDIT BY HAND. -->\n"
           "# StasisPath: the cascade to the end — what probability the framework assigns to its own prediction\n\n"
           "`DERIVACION.md` predicts the cold arm of P19 with **a point value: 0.142**. A point value cannot be compared "
           f"honestly with a threshold. Here the same cascade is walked with **all the uncertainty propagated**, {N:,} samples.\n\n"
           "> ## This does NOT close X2, and cannot\n"
           "> What comes out of here is a **probability of belief**: what the framework believes, given its own laws and ranges. "
           "It is not a measurement. **The price of confusing the two has already been paid:** the framework predicted that the CCR of the "
           "eutectic solvents would be 0.3 °C/min and declared it refuted above 0.426. The measured value turned out to be **> 30**, a factor of "
           "**100** in error. Had that prediction been counted as a datum, the framework would today hold a gravely false value at "
           "its core and would still be recommending the wrong experiment. **Track record of this class of prediction: 0 correct out of 1.**\n\n"
           "![Cascada](red/fig/CA_cascada.png)\n\n"
           "## The three links, and where each one stops being calculation\n\n"
           + tabla([
               ["1. Activation energy", f"Ea/R = {g(EaR_OVO)} K (path A) versus {g(EaR_NECES)} K (path B)",
                "**contradiction I1, open.** The two paths disagree by a factor of ~1.5 in Ea/R. Neither is chosen: both are sampled at 50 %"],
               ["2. Thermal extrapolation", f"from {g(T_CAL[0])}–{g(T_CAL[1])} °C to {g(T_OBJ)} °C",
                f"the model is used **{dist:.1f} calibration ranges** away. No datum says Arrhenius still holds there"],
               ["3. Ovocito → neural", "Ea/R is measured in OOCYTES; P19 measures LTP in CA1",
                "**with no datum at all.** That the same activation energy governs both is an assumption, not a law"]],
               ["link", "what it is composed of", "where it stops being calculation"])
           + "\n## El resultado\n\n"
           + tabla([
               ["**P(the framework believes P19 passes)**", f"**{100*p_pasa:.0f} %**", "belief, not measurement"],
               ["predicted damage, median", g(q(0.5)), "derivado"],
               ["50 % central", f"{g(q(0.25))} – {g(q(0.75))}", "derivado"],
               ["90 % central", f"{g(q(0.05))} – {g(q(0.95))}", "derivado"],
               ["threshold with LTP preserved", g(D_LTP_OK), "**MEASURED** (F46: 138.1 % vs 157.7, n.s.)"]],
               ["quantity", "value", "nature"])
           + "\n## All the framework's paths, and why they do not add up the way they appear to\n\n"
           "The Arrhenius chain is **one** of the paths. The framework has more, and letting them speak is right. "
           "But several **rest on the same German dataset** (F72/F46), so they are not independent "
           "evidence: if that dataset were biased, they would all fail together.\n\n"
           + tabla(filas_cam, ["path", "P(passes) contributed on its own", "likelihood ratio", "anchor", "independent?"])
           + f"\n**Honest combination (grouped by anchor, {n_grupos} independent groups): "
           f"{100*p_honesta:.0f} %.**\n\n"
           f"**Naive combination (treating all 6 as independent): {100*p_ingenua:.0f} %.**\n\n"
           f"> **Each path is a noisy observation of the SAME fact, not an independent chance of it happening.** "
           "That is why they are not combined with 1−∏(1−p), which saturates at 99 % whatever each one says: **likelihood "
           "ratios** are multiplied over a prior of 0.5. Within a group sharing an anchor they are not multiplied — if the anchor is "
           "biased they all fail together — and the strongest in the group is taken.\n\n"
           f"> The difference between {100*p_ingenua:.0f} % and {100*p_honesta:.0f} % is **exactly what it costs to count the same "
           "experiment twice**. Three of the six paths read the same dataset: German's. Adding them as if they "
           "were independent is the classic meta-evidence error, and here it is quantified. **Adding paths that "
           "share an anchor raises apparent confidence without adding information.**\n\n"
           "> **And even with the whole framework speaking, the honest combination does not reach certainty.** The ceiling is set by the link that "
           "has no datum: none of the six paths measures **M22 on neural tissue with function**. They all circle the gap; "
           "none crosses it. That is why the number rises but does not close.\n"
           + f"\n**If contradiction I1 resolved in favour of each path:** path A (Arrhenius on oocytes) gives "
           f"**{100*p_A:.0f} %**; path B (Fahy's anchors) gives **{100*p_B:.0f} %**. Without the transfer or extrapolation "
           f"uncertainty, the cascade would give **{100*p_limpio:.0f} %** — and that is precisely the figure one has NO right to use, "
           "because those two links are real.\n\n"
           "## Why this cannot be turned into a closure\n\n"
           "1. **Link 3 has no datum.** The whole cascade rests on the activation energy of damage measured in "
           "oocytes governing synaptic plasticity in CA1. No source in the network supports this. It is the point where "
           "calculation turns into assumption, and no amount of sampling fixes it.\n"
           "2. **Contradiction I1 remains open**, and it is exactly what P19 discriminates. Closing X2 with the cascade would mean using as "
           "tests exactly what is in dispute.\n"
           "3. **P19 has preregistered, hash-frozen thresholds.** If a prediction could close it, the preregistration would "
           "mean nothing and the framework would lose the ability to be wrong — which is where its value comes from. It has "
           "falsified itself twice (I2 and the eutectic-solvent shortcut); neither would have been possible under that rule.\n\n"
           f"**What this document does contribute:** it turns 'the framework predicts 0.142' into 'the framework believes P19 passes with "
           f"{100*p_pasa:.0f} % probability, and here is why'. That makes the prediction **more falsifiable, not less**: if P19 came out FAIL, this "
           "document says exactly which link should be revisited first.\n")
    (ROOT / "CASCADA.md").write_text(doc)
    return {"p_pasa": p_pasa, "p_A": p_A, "p_B": p_B, "p_limpio": p_limpio, "p_honesta": p_honesta,
            "p_ingenua": p_ingenua, "n_grupos": n_grupos, "filas_cam": filas_cam,
            "mediana": q(0.5), "p05": q(0.05), "p95": q(0.95)}
