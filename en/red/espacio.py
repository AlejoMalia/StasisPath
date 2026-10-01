"""StasisPath: the answer space of X2 — catalogue it instead of leaving it blank.

X2 asks whether a chemistry exists that **vitrifies at human scale AND preserves function**.
Leaving it as a blank gap wastes what the framework already knows: every known chemistry
occupies a point with MEASURED coordinates on two axes, and the gap has a shape and a size.

This module does not invent the missing datum. It does three things that can be done:

  1. **Catalogues** every chemistry in the framework with its two coordinates: measured CCR (does it
     vitrify at scale?) and demonstrated functional level on the E0-E5 ladder (does it preserve function?).
  2. **Measures the gap**: which region of the plane an answer to X2 must occupy, which chemistries
     come closest on each axis, and by how much they miss.
  3. **Tests whether the target region is EXCLUDED by any law in the framework.** If it were,
     X2 would close by demonstrated impossibility, as V15 was closed (pattern L43). If it is not,
     X2 stays open — but it is known exactly what a candidate must satisfy.

Declared limit, and it is the one that stops this becoming theatre: **a prediction of the
framework is NOT a datum**. The framework already predicts the outcome of arm C of P19 (DERIVACION.md
gives damage 0.142, and both paths of I1 predict PASS). That prediction is precisely **what the
experiment puts to the test**; counting it as a datum would close the loop on itself and the framework
would lose the ability to be wrong. That is why the prediction and measurement columns here are kept
separate and are NEVER added together.

Output: ESPACIO.md + red/fig/X_espacio.png. Called by motor.py.
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"

# Success scale of the framework (00_marco and Q3): what has been demonstrated, not what is hoped.
NIVEL = {0: "E0 estructura", 1: "E1 viable cells", 2: "E2 functional tissue",
         3: "E3 transplanted organ", 4: "E4 animal reanimado", 5: "E5 human"}

# Catalogue: each chemistry with its measured CCR and the MAXIMUM functional level DEMONSTRATED with it
# in neural tissue. CCR in °C/min. 'e_neural' is the level reached IN NEURAL TISSUE, which is
# what X2 asks; 'e_otro' is what was achieved in other tissue, which does not answer X2.
CPAS = [
    # nombre,          CCR,    M,     e_neural, e_otro, fuente,      nota
    ("M22",            0.10,   9.30,  0,        3,      "F2,F47,F5", "the only one whose CCR scales; in neural tissue ONLY ultrastructure (F47), no proof of function"),
    ("VM3",            3.00,   8.90,  None,     None,   "F37b",      "V3 + ice blockers; no published functional proof in neural tissue"),
    ("VS55 tej.",      1.00,   8.40,  None,     1,      "F3",        "toxic in rat kidney"),
    ("VS55 sol.",      2.50,   8.40,  None,     1,      "F3",        ""),
    ("V3",             5.40,   8.42,  2,        None,   "F46,F71",   "THE ONLY one with measured neural function: LTP 138.1 % vs control 157.7 % (n.s.)"),
    ("VMP",            5.40,   8.40,  None,     3,      "F1,F3",     "rat kidney transplanted; not tested in neural tissue"),
    ("EG 61 % alone",   5.40,   None,  1,        None,   "F52,F71",   "fEPSPs recovered but WITHOUT stable potentiation ⇒ does not reach E2"),
    ("MEDY",           None,   None,  2,        None,   "F35",       "does NOT vitrify: slow freezing with dilute CPA, millimetre scale"),
    ("NADES 50 %",     30.0,   None,  None,     1,      "F80",       "CCR > 30 MEASURED (they crystallize in DSC); cell lines only"),
    ("agua pura",      3.84e8, 0.0,   None,     None,   "F76",       "zero-concentration limit"),
]

def g(x):
    if x is None: return "—"
    return f"{x:.3g}" if abs(x) < 1e4 else f"{x:.2e}"

def tabla(filas, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in f) + " |" for f in filas) + "\n"

def generar(D, PAR, DERIV, ROOT):
    p = {k: v["v"] for k, v in PAR.items()}
    # BATCH 52 (audit against ourselves, R4 impostor box): the CPAS table had the CCR of M22, VS55 and
    # VMP WRITTEN BY HAND, duplicating parameters that already live in `parametros`. If the YAML value
    # changed —for instance on labelling `CCR_M22` as tissue, which is the open gap— this document
    # would not find out. No value is moved: it is CHECKED that they agree and, if not,
    # it is declared in the document instead of being kept quiet.
    _espejo = {"M22": "CCR_M22", "VS55 sol.": "CCR_VS55", "VMP": "CCR_VMP"}
    desfase = [(nom, ccr, PAR[k]["v"]) for nom, ccr, *_ in CPAS
               for k in [_espejo.get(nom)] if k and abs(ccr - PAR[k]["v"]) > 1e-9]
    # CCR threshold to vitrify a human brain by convection (L44, inverting C3)
    LCe = DERIV["LC_esfera"]
    lc_cerebro = LCe(D["humano"]["brain"])
    ccr_req = p["anc_rate"] * (p["anc_LC"] / lc_cerebro) ** p["exp_LC"]
    E_REQ = 2   # X2 requires at least tissue function (E2): LTP preserved

    # --- 1. catalogue
    filas = []
    for nom, ccr, M, en, eo, f, nota in CPAS:
        ok_ccr = (ccr is not None and ccr <= ccr_req)
        ok_fun = (en is not None and en >= E_REQ)
        veredicto = ("**RESUELVE X2**" if (ok_ccr and ok_fun) else
                     ("vitrifies, function missing" if ok_ccr else
                      ("function, does not vitrify" if ok_fun else "neither of the two")))
        filas.append([nom, g(ccr), g(M), (NIVEL[en].split()[0] if en is not None else "—"),
                      (NIVEL[eo].split()[0] if eo is not None else "—"), f, veredicto])

    # --- 2. the gap: who is closest on each axis and by how much it fails
    con_ccr = [(n, c) for n, c, *_ in CPAS if c is not None and c <= ccr_req]
    con_fun = [(n, e) for n, c, M, e, *_ in CPAS if e is not None and e >= E_REQ]
    # the one with the best CCR among those that DO have neural function
    mejor_fun = min([(c, n) for n, c, M, e, *_ in CPAS if e is not None and e >= E_REQ and c is not None],
                    default=(None, None))
    falta_ccr = (mejor_fun[0] / ccr_req) if mejor_fun[0] else None

    # --- 3. does any law of the framework EXCLUDE the target region?
    #     The target region is CCR ≤ ccr_req with E2 function in neural tissue. The question is whether the framework
    #     contains any law forbidding it. The candidate would be a CCR↔toxicity relation that
    #     forced low CCR ⇒ lethal toxicity. L20/L25/E7 say the opposite: toxicity
    #     depends on the quadruple (composition, temperature, time, protocol), NOT on molarity
    #     alone. That is why M22 at −22 °C and V3 at 10 °C are distinct points of the space, not the same.
    excluida = False
    razon_exclusion = (
        "**It is NOT excluded.** The only law that could forbid it would be one requiring that "
        "every low-CCR chemistry be lethal. The framework says the opposite: **L20, L25 and E7 "
        "establish that toxicity depends on the quadruple (composition, temperature, time, "
        "protocol) and NOT on molarity alone.** That is why M22 loaded at −22 °C and V3 loaded at "
        "10 °C are **different points** in the space even though their molarity is nearly equal (9.3 vs "
        "8.42 M, a 10 % difference). ⇒ X2 **does not close by impossibility**: it stays open, "
        "and that is a result, not a gap.")

    # --- figure: the plane with the gap marked
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    ax.axvspan(1e-3, ccr_req, color=AQUA, alpha=0.09, zorder=0)
    ax.axhspan(E_REQ - 0.5, 5.5, color=AQUA, alpha=0.09, zorder=0)
    ax.add_patch(plt.Rectangle((1e-3, E_REQ - 0.5), ccr_req - 1e-3, 6 - E_REQ,
                               facecolor=AQUA, alpha=0.16, edgecolor=AQUA, lw=1.4, zorder=1))
    ax.text(1.4e-3, 4.6, "REGION THAT RESOLVES X2\nempty: no measured chemistry lands here",
            fontsize=8, color="#0e7a55", va="top", zorder=4)
    # those without neural data go on a row of their own, with staggered labels
    # so they do not overlap (several share an almost identical CCR)
    sin_dato = [(n, c) for n, c, M, en, *_ in CPAS if c is not None and en is None]
    dy = {n: (12, -15, 25)[i % 3] for i, (n, _) in enumerate(sorted(sin_dato, key=lambda t: t[1]))}
    fuera = []
    for nom, ccr, M, en, eo, f, nota in CPAS:
        if ccr is None: continue
        if ccr > 1e3:                     # off scale: declared in the footer, not clipped
            fuera.append((nom, ccr)); continue
        e = en if en is not None else -0.42
        hueco = (en is None)
        ax.scatter([ccr], [e], s=74 if not hueco else 46,
                   color=(ORANGE if ccr > ccr_req else BLUE) if not hueco else SURF,
                   edgecolor=(ORANGE if ccr > ccr_req else BLUE), linewidth=1.8, zorder=3)
        ax.annotate(nom, (ccr, e), textcoords="offset points",
                    xytext=(7, 7) if not hueco else (6, dy[nom]),
                    fontsize=7.6 if not hueco else 7.0, color=INK2, zorder=4)
    ax.axvline(ccr_req, color="#c0392b", lw=1.3, zorder=2)
    ax.annotate(f"Max CCR for a\nhuman brain: {ccr_req:.3g} °C/min",
                (ccr_req, 3.5), textcoords="offset points", xytext=(9, 0),
                fontsize=7.4, color="#c0392b", zorder=4, va="center")
    if fuera:
        ax.text(0.99, -0.155, "off scale: " + " · ".join(f"{n} (CCR {c:.2e})" for n, c in fuera),
                transform=ax.transAxes, ha="right", fontsize=6.8, color=MUTED)
    ax.set_xscale("log"); ax.set_xlim(5e-2, 1e3); ax.set_ylim(-0.95, 5.6)
    ax.set_yticks([-0.42, 0, 1, 2, 3])
    ax.set_yticklabels(["no neural datum", "E0 estructura", "E1 cells", "E2 functional tissue",
                        "E3 organ"], fontsize=7.6, color=INK2)
    ax.set_xlabel("measured CCR (°C/min) — left of the line, it vitrifies a human brain", color=INK2)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.grid(color=GRID, lw=0.6); ax.set_facecolor(SURF); fig.set_facecolor(SURF)
    fig.suptitle("The answer space of X2: two measured axes and a gap with a shape",
                 x=0.02, ha="left", fontsize=11, color=INK)
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "X_espacio.png", dpi=150); plt.close(fig)

    doc = ("<!-- AUTO-GENERATED by red/espacio.py. DO NOT EDIT BY HAND. -->\n"
           "# StasisPath: the answer space of X2 — catalogued, not blank\n\n"
           "X2 asks whether a chemistry exists that **vitrifies at human scale AND preserves function**. "
           "Leaving it as a blank gap wastes what the framework already knows: every known chemistry occupies a point "
           "with **measured coordinates**, and the gap has a shape and a size.\n\n"
           "> **What this document does NOT do.** The framework already *predicts* the outcome of arm C of P19 "
           "(DERIVACION.md gives damage 0.142; both paths of I1 predict PASS). **That prediction is not counted as a datum.** "
           "It is precisely what the experiment puts to the test: counting it would close the loop on itself and the framework "
           "would lose the ability to be wrong. Only **measured** coordinates enter here.\n\n"
           f"![Space of X2](red/fig/X_espacio.png)\n\n"
           "## 1. Catalogue: every chemistry in the framework, with its two coordinates\n\n"
           f"**Vitrification requirement:** CCR ≤ **{ccr_req:.3g} °C/min** (inverting C3 for a human brain of "
           f"{D['humano']['brain']} g, LC = {lc_cerebro:.2f} cm). **Function requirement:** at least **E2**, "
           "functional, which is the level at which LTP is measured.\n\n"
           + tabla(filas, ["chemistry", "CCR °C/min", "M", "level in NEURAL", "level in other tissue", "source", "verdict"])
           + ("\n> ⚠ **MISMATCH BETWEEN THIS TABLE AND `red/stasispath.yaml`** (checked automatically): "
              + "; ".join(f"**{n}** here {g(a)} versus {g(b)} in `parametros`" for n, a, b in desfase)
              + ". The table **does not correct itself** (moving a value is forbidden, R2): a human must decide which one is right.\n"
              if desfase else
              "\n> **Checked:** the CCRs of M22, VS55 and VMP in this table **agree with `parametros` in "
              "`red/stasispath.yaml`**. They were written by hand and duplicated the datum; now a mismatch would be detected and "
              "declared right here. It matters because `CCR_M22` has an **open gap** (solution or tissue) and the day "
              "is tagged, this document has to find out about it.\n")
           + "\n## 2. The gap, measured\n\n"
           f"- **Chemistries that vitrify at human-brain scale:** {len(con_ccr)} — "
           + ", ".join(f"{n} ({g(c)})" for n, c in con_ccr) + ".\n"
           f"- **Chemistries with demonstrated function in neural tissue (≥ E2):** {len(con_fun)} — "
           + ", ".join(f"{n} (E{e})" for n, e in con_fun) + ".\n"
           f"- **Intersection: empty.** No measured chemistry satisfies both.\n\n"
           f"**By how much the best candidate on each side fails:**\n\n"
           f"- On the function axis, the best is **{mejor_fun[1]}**, with demonstrated E2 neural function, but its CCR "
           f"({g(mejor_fun[0])}) is **×{falta_ccr:.1f} the permitted value**. It must come down by a factor of {falta_ccr:.1f}.\n"
           f"- On the vitrification axis, the best is **M22** (CCR 0.1, ×{ccr_req / 0.10:.1f} of headroom over the "
           "requirement), but in neural tissue **it has only demonstrated ultrastructure (E0, F47), with no proof "
           "of function**.\n\n"
           "> **The gap is not diffuse: it is a jump between two known chemistries.** X2 reduces to one concrete "
           "question — **does M22 preserve the function of neural tissue?** — and that is exactly **arm C of P19**, "
           "which is already preregistered with frozen thresholds. Cataloguing the space does not close X2, but **it shows "
           "that a single experiment decides it**.\n\n"
           "## 3. Is the target region excluded by any law in the framework?\n\n"
           "This is the test that closed V15 (pattern L43): if the uncertainty cannot accommodate any answer, "
           "the verdict is closed even though nobody has measured.\n\n"
           + razon_exclusion + "\n\n"
           "**What a candidate would have to satisfy, in one line:** CCR ≤ "
           f"{ccr_req:.3g} °C/min with LTP ≥ 130 % of baseline in CA1 after HFS (the preregistered P19 threshold). "
           "M22 meets the first by a factor of "
           f"{ccr_req / 0.10:.1f}; nobody has measured the second.\n")
    (ROOT / "ESPACIO.md").write_text(doc)
    return {"ccr_req": ccr_req, "con_ccr": con_ccr, "con_fun": con_fun,
            "excluida": excluida, "falta_ccr": falta_ccr, "mejor_fun": mejor_fun}
