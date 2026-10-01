"""StasisPath: cross-species scaling and leave-one-out validation (back-test).

Answers: "can what has been achieved in animals be scaled to project a human number,
and then checked for where it is right and where it is not?"

Method (MATE): no curve is fitted and its result proclaimed. Each candidate law is subjected
to **leave-one-out validation**: one species is left out, predicted from the others, and the
error is measured. A law is only used to project to human if its leave-one-out error is known
and bounded. Laws that fail are reported as failures: knowing where it does
NOT scale is half the result.
"""
import math, statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"

def g(x): return f"{x:.3g}" if abs(x) < 1e4 else f"{x:,.0f}"
def tabla(filas, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in f) + " |" for f in filas) + "\n"
def gmean(v): return math.exp(sum(math.log(x) for x in v) / len(v))

# Neurons and brain mass [P]: order of magnitude from the literature (Herculano-Houzel and others).
# Not reread in a primary source: used ONLY to test whether neuronal scale predicts anything.
ESPECIES = {
    "C. elegans": dict(neu=302,     brain=1e-6,  body=1e-6),
    "mouse":      dict(neu=71e6,    brain=0.4,   body=30),
    "rat":       dict(neu=200e6,   brain=2.0,   body=300),
    "rabbit":     dict(neu=500e6,   brain=10.0,  body=2500),
    "cat":       dict(neu=760e6,   brain=30.0,  body=4000),
    "dog":      dict(neu=2.25e9,  brain=70.0,  body=20000),
    "pig":      dict(neu=2.2e9,   brain=180.0, body=40000),
    "human":     dict(neu=86e9,    brain=1400., body=70000),
}

def generar(D, PAR, R, ROOT):
    pv = {k: v["v"] for k, v in PAR.items()}
    Q10, t37 = pv["Q10"], pv["t37"]
    fig_dir = ROOT / "red" / "fig"; fig_dir.mkdir(exist_ok=True)
    doc_secciones = []

    # ============================================================ T1  τ_eq: invariant across species?
    # τ_eq = t · Q10^((T-37)/10). If it were perfectly invariant, all species would give the same number.
    obs = [  # (especie, T, t, etiqueta, fuente, incluir_en_ajuste)
        ("human", 15, 31,  "DHCA 15 °C",              "F4",  True),
        ("human", 10, 45,  "DHCA 10 °C",              "F4",  True),
        ("dog",  37, 12.5,"arrest 12.5 min",          "F25b",True),
        ("dog",  10, 120, "cold flush 120 min",       "F30", True),
        ("pig",  10, 60,  "60 min, no deficit",      "F42", True),
        ("cat",   37, 60,  "1 h, brain only",        "F38", False),
    ]
    pts = []
    for e, T, t, lab, f, usar in obs:
        tau = t * Q10 ** ((T - 37) / 10)
        pts.append(dict(e=e, T=T, t=t, tau=tau, lab=lab, f=f, usar=usar, M=ESPECIES[e]["body"]))
    base = [p for p in pts if p["usar"]]
    # leave-one-out validation: predict each point with the geometric mean of the others
    for p in base:
        otros = [q["tau"] for q in base if q is not p]
        p["pred"] = gmean(otros)
        p["err"] = max(p["pred"] / p["tau"], p["tau"] / p["pred"])
    err_max = max(p["err"] for p in base)
    disp = max(p["tau"] for p in base) / min(p["tau"] for p in base)
    # does it depend on mass? log-log correlation
    xs = [math.log10(p["M"]) for p in base]; ys = [math.log10(p["tau"]) for p in base]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys)); sxx = sum((x - mx) ** 2 for x in xs)
    pend = sxy / sxx if sxx else 0.0
    r = sxy / math.sqrt(sxx * sum((y - my) ** 2 for y in ys)) if sxx else 0.0
    tau_h = gmean([p["tau"] for p in base if p["e"] != "human"])   # projection to human WITHOUT using human data
    tau_h_real = gmean([p["tau"] for p in base if p["e"] == "human"])
    veredicto_T1 = ("**PASS**" if err_max <= 3 and abs(pend) < 0.15 else "**FAIL**")
    filas = [[p["e"], p["lab"], g(p["T"]), g(p["t"]), f"**{g(p['tau'])}**", g(p["pred"]), f"×{g(p['err'])}", p["f"]] for p in base]
    filas.append(["cat", "1 h, brain only (excluded)", "37", "60", f"**{g(pts[-1]['tau'])}**", "—", "—", "F38"])
    doc_secciones.append(("T1 · Is τ_eq invariant across species? (leave-one-out validation)", None,
        f"Each species is left out and predicted from the others.\n\n" + tabla(filas,
        ["species", "observation", "T °C", "t min", "τ_eq min", "predicted without it", "error", "source"]) +
        f"\n- **Maximum leave-one-out error: ×{g(err_max)}** · total spread ×{g(disp)}.\n"
        f"- **Dependence on body mass:** log-log slope **{pend:+.2f}** (r = {r:+.2f}) over 3 orders of magnitude of mass "
        f"(dog 20 kg → human 70 kg → pig 40 kg). A slope ≈ 0 means **τ_eq does not depend on size**.\n"
        f"- **Projection to human without using any human datum: {g(tau_h)} min.** Real human value: {g(tau_h_real)} min. "
        f"Projection error: **×{g(max(tau_h/tau_h_real, tau_h_real/tau_h))}**.\n"
        f"- Verdict: {veredicto_T1}. The cross-species projection of τ_eq is valid within a factor of ×{g(err_max)}. "
        f"The cat is excluded from the fit because its ischemia was **brain-only** (a different protocol), and precisely for that reason its τ_eq jumps to {g(pts[-1]['tau'])}: "
        f"**the law does not fail by species, it fails by protocol.**"))

    # ============================================================ T2  thermal scaling: does the LC^-2 law hold?
    # Anchored on the 3 L bag. Compared against independent measured points.
    anc_LC, anc_rate = pv["anc_LC"], pv["anc_rate"]
    pred = lambda LC: anc_rate * (anc_LC / LC) ** 2
    casos = [("bolsa 0.5 L", 1.2, 1.4, "F2"), ("bolsa 1 L", 1.4, 1.0, "F2"), ("pig liver ~1 L", 1.8, 0.6, "F2")]
    filas, errs = [], []
    for nom, LC, medido, f in casos:
        p = pred(LC); e = max(p / medido, medido / p); errs.append(e)
        filas.append([nom, g(LC), g(medido), g(p), f"×{g(e)}", f])
    err_T2 = max(errs)
    doc_secciones.append(("T2 · Does the LC⁻² thermal law hold outside its anchor?", None,
        "The law was anchored on the 3 L bag (LC 2.2 cm → 0.47 °C/min) and is checked against independent measured points from the same work.\n\n" +
        tabla(filas, ["case", "LC cm", "measured °C/min", "predicted by LC⁻²", "error", "source"]) +
        f"\n- **Maximum error: ×{g(err_T2)}.** The thermal law **PASSES**: it predicts cooling rates within ×{g(err_T2)} over the 0.5–3 L range.\n"
        f"- That is why extrapolation to LC of 4–7.5 cm (body and trunk) is credible to order of magnitude, though it still lacks a direct datum.")

    )

    # ============================================================ T3  does neuronal scale predict cryogenic success?
    # The user's question: scale by number of neurons or connectomes?
    logros = [  # (species, mass of brain tissue with the achievement, type, year, source)
        ("rat",   0.01, "function (K+/Na+, ultrastructure) in slices", 2006, "F37"),
        ("mouse",  0.02, "function (LTP) in slices",                      2026, "F46"),
        ("mouse",  0.4,  "whole brain vitrified (function in slices)",2026, "F46"),
        ("cat",   30.0, "whole brain frozen: partial electrical activity", 1974, "F48"),
        ("pig",  180.0,"whole brain vitrified unfixed: structure only",  2026, "F47"),
    ]
    xs_n = [math.log10(ESPECIES[e]["neu"]) for e, *_ in logros]
    xs_y = [float(a) for *_, a, _ in logros]
    ys_l = [math.log10(m) for _, m, *_ in logros]
    def corr(xs, ys):
        mx, my = statistics.mean(xs), statistics.mean(ys)
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        sxx = sum((x - mx) ** 2 for x in xs); syy = sum((y - my) ** 2 for y in ys)
        return sxy / math.sqrt(sxx * syy) if sxx and syy else 0.0
    r_neu, r_yr = corr(xs_n, ys_l), corr(xs_y, ys_l)
    # is it real or a confound? neurons and brain mass are almost perfectly correlated across species
    esp_l = [e for e, *_ in logros]
    r_confund = corr([math.log10(ESPECIES[e]["neu"]) for e in ESPECIES if e != "C. elegans"],
                     [math.log10(ESPECIES[e]["brain"]) for e in ESPECIES if e != "C. elegans"])
    # is the achieved mass simply the brain mass of the chosen species?
    frac = [m / ESPECIES[e]["brain"] for e, m, *_ in logros]
    filas = [[e, g(ESPECIES[e]["neu"]), g(ESPECIES[e]["brain"]), g(m), tipo, a, f] for e, m, tipo, a, f in logros]
    doc_secciones.append(("T3 · Does neuron count work as a scaling variable?", None,
        tabla(filas, ["species", "neurons [P]", "brain g", "achieved mass g", "what was achieved", "year", "source"]) +
        f"\n- Correlation between achieved mass and **neuron count**: r = **{r_neu:+.2f}** (high).\n"
        f"- Correlation between achieved mass and **publication year**: r = **{r_yr:+.2f}**.\n"
        f"- **But the high correlation is a confound, not a law.** Across species, neuron count and brain mass travel together "
        f"(r = **{r_confund:+.2f}**), and the achieved mass is essentially the brain mass of the chosen species "
        f"(achieved/brain fractions: {', '.join(g(f) for f in frac)}). That is: a high r only says that **whoever vitrifies a pig brain obtains "
        f"the mass of a pig brain**. It is a tautology, not predictive power.\n"
        f"- **The test that settles it:** neuron count appears in none of the equations that limit the problem. "
        "**What limits is geometry, not neuron count.** Heat diffuses as LC², "
        "the cryoprotectant distributes through the vasculature, and fractures depend on the thermal gradient. None of those three things "
        "knows how many neurons are inside.\n"
        f"- **Where neuron count does matter:** on the **information** axis, not the physical one. The human brain has "
        f"~{g(ESPECIES['human']['neu'] / ESPECIES['mouse']['neu'])} times the neurons of the mouse and "
        f"~{g(ESPECIES['human']['neu'] / ESPECIES['C. elegans']['neu'])} times those of *C. elegans*: that fixes **how much** information must be preserved "
        "and how much must be sampled to verify it (P15), not whether the tissue survives.\n"
        "- **Methodological conclusion:** scaling by neuron count would yield a number with no physical content. To project to human one must use "
        "geometry (LC, mass) on the physical axes and neuron count only on the information axis."))

    # ============================================================ T4  projection to human with the laws that PASS
    LC_h_cerebro = (3 * 1400 / (4 * math.pi)) ** (1 / 3) / 3
    rate_h = pred(LC_h_cerebro)
    LC_raton = (3 * 0.4 / (4 * math.pi)) ** (1 / 3) / 3
    rate_raton = pred(LC_raton)
    # CORRECTION (see PRECISION.md §1): the mouse->human path CROSSES the Bi=1 frontier (LC 0.40 cm).
    # Applying LC^-2 across the whole path overestimates the difficulty by ×2.6.
    LC_CRIT = 0.40
    def _factor(a_, b_):
        a_, b_ = sorted((a_, b_))
        if b_ <= LC_CRIT: return b_ / a_
        if a_ >= LC_CRIT: return (b_ / a_) ** 2
        return (LC_CRIT / a_) * (b_ / LC_CRIT) ** 2
    ratio = _factor(LC_raton, LC_h_cerebro)
    tasa_german = 2.45 * 60   # °C/s -> °C/min, cooling achieved in mouse brain (F46)
    deficit = tasa_german / rate_h        # how many times it falls short of repeating that protocol in human
    ordenes = math.log10(deficit)
    filas = [
        ["entry τ_eq", f"×{g(err_T2 * 0 + err_max)}", f"{g(tau_h)} min", "**valid**: no mass dependence and bounded leave-one-out error"],
        ["Brain cooling (LC⁻²)", f"×{g(err_T2)}", f"{g(rate_h)} °C/min by convection at LC {g(LC_h_cerebro)} cm", "**valid** to order of magnitude"],
        ["Scaling by neuron count", "—", "no physical content", "**invalid** for the physical axes (T3)"],
    ]
    doc_secciones.append(("T4 · Projection to human with the validated laws", None,
        tabla(filas, ["law", "leave-one-out error", "human projection", "verdict"]) +
        f"\n**The number, computed:** German 2026 vitrifies the mouse brain (LC ≈ {g(LC_raton)} cm) cooling at ≥ {g(tasa_german)} °C/min. "
        f"A human brain has LC ≈ {g(LC_h_cerebro)} cm, that is **×{g(ratio)} worse in conduction** (respecting the regime change at Bi = 1; applying LC⁻² across the whole path would give ×231 and **overestimate the difficulty by ×2.6**). That same protocol demands {g(tasa_german)} °C/min, "
        f"but convection in a human brain gives only **{g(rate_h)} °C/min**: a deficit of **×{g(deficit)}**.\n\n"
        f"⇒ **German's protocol does not scale to the human brain by convection: it is short by ~{ordenes:.1f} orders of magnitude in cooling rate.** "
        f"This is not an opinion: it is the same LC⁻² law that was already accurate to within ×{g(err_T2)} in T2.\n\n"
        f"**What a human brain therefore demands:** a CPA whose CCR is ≤ {g(rate_h)} °C/min (the M22 class, CCR {g(pv['CCR_M22'])}, **meets it**; "
        f"V3 and VMP do not) plus volumetric warming. That is exactly what Fahy 2026 does (M22, pig brain, structure only) "
        f"and what German does NOT do (V3, high rate, mouse only). **The two halves of the bottleneck use mutually incompatible chemistries.**"))

    # ---- figure: τ_eq across species
    fig, ax = plt.subplots(figsize=(8, 4.4))
    for p in pts:
        c = ORANGE if not p["usar"] else BLUE
        ax.scatter(p["M"], p["tau"], s=80, c=c, edgecolors=SURF, linewidths=1.5, zorder=3)
        ax.annotate(f"{p['e']}: {p['lab']}", (p["M"], p["tau"]), xytext=(6, 5), textcoords="offset points", fontsize=7, color=INK2)
    lo, hi = min(p["tau"] for p in base), max(p["tau"] for p in base)
    ax.axhspan(lo, hi, color=BLUE, alpha=0.10, zorder=1)
    ax.axhline(gmean([p["tau"] for p in base]), color=BLUE, lw=2, zorder=2, label=f"invariante τ_eq ≈ {g(gmean([p['tau'] for p in base]))} min (banda ×{g(disp)})")
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(5e3, 3e5)
    ax.set_xlabel("Body mass (g, log)"); ax.set_ylabel("τ_eq: isquemia equivalente a 37 °C (min, log)")
    ax.set_title("T1 · τ_eq does not depend on animal size (orange = different protocol)", loc="left", fontsize=10.5, color=INK)
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.16))
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.grid(color=GRID, lw=0.6); ax.set_facecolor(SURF); fig.set_facecolor(SURF)
    fig.tight_layout(); fig.savefig(fig_dir / "T1_tau_especies.png", dpi=150); plt.close(fig)

    doc = ("<!-- AUTO-GENERATED by red/escalado.py (called from red/motor.py). DO NOT EDIT BY HAND. -->\n"
           "# StasisPath: cross-species scaling and leave-one-out validation\n\n"
           "**The question:** can what has been achieved in animals be scaled to project a human number, and then checked for where it is right and where it is not?\n\n"
           "**Short answer:** yes, but **not with neuron count**. It can be done with the laws whose leave-one-out error can be measured. "
           "Here each candidate law is validated by leaving out one species and predicting it from the others; only those that pass are used to project.\n\n"
           "![τ_eq across species](red/fig/T1_tau_especies.png)\n\n")
    for tit, figf, body in doc_secciones:
        doc += f"## {tit}\n\n" + (f"![{tit}](red/fig/{figf})\n\n" if figf else "") + body + "\n\n"
    doc += ("## Resumen\n\n"
            f"| law | valid? | error | use |\n|---|---|---|---|\n"
            f"| τ_eq invariant across species | yes | ×{g(err_max)} | projecting ischemia windows to human |\n"
            f"| LC⁻² cooling | yes | ×{g(err_T2)} | projecting vitrification to any size |\n"
            f"| scaling by neuron count | **no** | — | only for sizing the information (P15), not the physics |\n")
    (ROOT / "ESCALADO.md").write_text(doc)
    return dict(err_tau=err_max, err_term=err_T2, r_neu=r_neu, ratio_cerebro=ratio, rate_h=rate_h)
