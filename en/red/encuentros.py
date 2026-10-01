"""StasisPath: projection of each layer onto a dimension and computation of the collisions (axis pairs).

Called by motor.py at the end: generar(D, PAR, R) writes ENCUENTROS.md and red/fig/*.png.
Each collision has a law (a frontier computed from the network's parameters), the data points,
and a computed verdict: which points cross the frontier, how many orders of magnitude away the
goal is, and which axis pairs have no data.
"""
import itertools, math
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# validated palette (dataviz, light mode): 4 categorical slots + ink and surface
SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
CLASES = {  # class -> (label, colour, marker)  shape = secondary encoding
    "hypothermia": ("Hypothermia / flow", "#2a78d6", "o"), "low_flow": ("Hypothermia / flow", "#2a78d6", "o"),
    "normothermia": ("Hypothermia / flow", "#2a78d6", "o"), "cellular": ("Hypothermia / flow", "#2a78d6", "o"),
    "controlled_phase": ("Supercooling / controlled ice", "#eb6834", "s"),
    "glass": ("Glass", "#1baf7a", "D"), "natural": ("Natural biology", "#eda100", "^")}
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "axes.edgecolor": "#c3c2b7",
                     "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "font.size": 9,
                     "axes.spines.top": False, "axes.spines.right": False})

def lc_de_masa(g):  # characteristic length of an aqueous sphere: LC = r/3 (cm)
    return (3 * g / (4 * math.pi)) ** (1 / 3) / 3

def tabla(filas, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in f) + " |" for f in filas) + "\n"

def g(x): return f"{x:.3g}" if abs(x) < 1e4 else f"{x:,.0f}"

def _etiquetar(ax, items):
    """items: [(x, y, text)]. Places labels avoiding pixel overlaps (staggered vertical offset)."""
    ax.figure.canvas.draw()
    usados = []
    for x, y, txt in sorted(items, key=lambda i: (i[0], i[1])):
        px, py = ax.transData.transform((x, y))
        w, h = 5.2 * len(txt), 11
        for dy in (4, 14, -12, 24, -22, 34, -32, 44):
            box = (px + 5, py + dy, px + 5 + w, py + dy + h)
            if all(box[2] < u[0] or box[0] > u[2] or box[3] < u[1] or box[1] > u[3] for u in usados):
                break
        usados.append(box)
        ax.annotate(txt, (x, y), xytext=(5, dy), textcoords="offset points", fontsize=7, color=INK2,
                    arrowprops=dict(arrowstyle="-", color=GRID, lw=0.6) if abs(dy) > 5 else None)

def _leyenda(ax):
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3)

def _scatter(ax, pts, xk, yk, etiquetar=True):
    vistos = set()
    for k, p in pts.items():
        et, c, m = CLASES[p["clase"]]
        ax.scatter(p[xk], p[yk], s=64, c=c, marker=m, edgecolors=SURF, linewidths=1.5, zorder=3,
                   label=et if et not in vistos else None)
        vistos.add(et)
    if etiquetar:
        _etiquetar(ax, [(p[xk], p[yk], p["label"]) for p in pts.values()])

def generar(D, PAR, R, ROOT):
    fig_dir = ROOT / "red" / "fig"; fig_dir.mkdir(exist_ok=True)
    pv = {k: v["v"] for k, v in PAR.items()}
    rng = {k: v["r"] for k, v in PAR.items()}
    P = D["puntos"]; META = D["meta_punto"]
    w = lambda T, t37, q: t37 * q ** ((37 - T) / 10)
    out, avisos = [], []

    # ---------------------------------------------------------------- E1  T × t
    pts = {k: p for k, p in P.items() if p.get("T") is not None and p.get("t")}
    fig, ax = plt.subplots(figsize=(8, 5.6))
    Ts = [x / 2 for x in range(-40, 76)]
    lo = [w(T, rng["t37"][0], rng["Q10"][0]) for T in Ts]; hi = [w(T, rng["t37"][1], rng["Q10"][1]) for T in Ts]
    ax.fill_between(Ts, lo, hi, color="#2a78d6", alpha=0.12, linewidth=0)
    ax.plot(Ts, [w(T, pv["t37"], pv["Q10"]) for T in Ts], color="#2a78d6", lw=2, label="C2: mammalian brain window (zero flow)")
    ax.axvline(0, color="#c3c2b7", lw=1)
    sub = {k: p for k, p in pts.items() if p["T"] > -40}
    _scatter(ax, sub, "T", "t")
    ax.set_yscale("log"); ax.set_xlabel("Temperatura (°C)"); ax.set_ylabel("Pause duration (min, log)")
    ax.set_title("T × t collision: thermal layer versus storage", loc="left", fontsize=11, color=INK)
    _leyenda(ax); fig.tight_layout(); fig.savefig(fig_dir / "E1_T_t.png", dpi=150); plt.close(fig)
    filas = []
    for k, p in sorted(pts.items(), key=lambda kv: kv[1]["T"]):
        r = p["t"] / w(p["T"], pv["t37"], pv["Q10"])
        rmin = p["t"] / w(p["T"], rng["t37"][1], rng["Q10"][1])
        if p["fase"] == "glass": dx = "glass: outside the domain of C2 (chemistry halted below Tg)"
        elif p["clase"] == "natural": dx = "exceeds C2 → natural non-thermal biochemistry"
        elif p["fase"] in ("extra_ice", "supercooled") or p["T"] < 0: dx = "exceeds C2 → state below 0 °C (controlled ice or supercooling)"
        elif rmin <= 1: dx = "explained by passive Q10"
        elif p["flujo"] == "low": dx = "exceeds C2 → there was (low) flow"
        elif p.get("mecanismo") == "reperfusion": dx = "exceeds C2 → optimized reperfusion (grey zone X1)"
        elif r <= 5: dx = "tissue or flow margin (≤ ×5)"
        else: dx = "**ANOMALY**: exceeds C2 with no declared mechanism"; avisos.append(f"E1: {p['label']} exceeds C2 by ×{g(r)} with no mechanism")
        filas.append([p["label"], g(p["T"]), g(p["t"]), f"×{g(r)} (≥ ×{g(rmin)})", dx, p["f"]])
    out.append(("E1 · Temperature × duration", "E1_T_t.png",
        "**Law:** C2 (band = corners of t37 and Q10). Above the band, the pause is not explained by passive thermal suppression of the mammalian brain.\n\n" +
        tabla(filas, ["point", "T °C", "t min", "t / C2 window", "diagnostic", "source"])))

    # ---------------------------------------------------------------- E2  τ_eq (ischemia layer) × E × information
    iso = {k: p for k, p in P.items() if p.get("T") is not None and p.get("t") and p["fase"] == "liquid" and p["artificial"]}
    fig, ax = plt.subplots(figsize=(8, 4.6))
    filas, lab2 = [], []
    for k, p in iso.items():
        f = pv["Q10"] ** ((p["T"] - 37) / 10); tau = p["t"] * f
        flo = p["t"] * rng["Q10"][1] ** ((p["T"] - 37) / 10); fhi = p["t"] * rng["Q10"][0] ** ((p["T"] - 37) / 10)
        p["tau"] = tau
        filas.append([p["label"], g(p["t"]), g(p["T"]), f"{g(tau)} ({g(min(flo, fhi))}–{g(max(flo, fhi))})", p["E"], p["info"], p["flujo"], p["f"]])
        et, c, m = CLASES[p["clase"]]
        bajo = p["flujo"] == "low"
        ax.scatter(tau, p["E"], s=70, marker="X" if bajo else m, c=MUTED if bajo else (c if p["info"] == "yes" else SURF),
                   edgecolors=MUTED if bajo else c, linewidths=2, zorder=3)
        lab2.append((tau, p["E"], p["label"] + (" · low flow: τ_eq overestimated" if bajo else "")))
    for x, lab in ((pv["t37"], "clinical 5"), (pv["tau_org_good"], "reproducible 12.5"), (pv["tau_org_exist"], "existencia 60"), (pv["tau_cel"], "celular 240")):
        ax.axvline(x, color="#c3c2b7", lw=1, ls="--"); ax.text(x, 5.35, lab, fontsize=7, color=MUTED, ha="center")
    ax.set_xscale("log"); ax.set_ylim(0.5, 5.6); _etiquetar(ax, lab2); ax.set_xlabel("τ_eq: isquemia equivalente a 37 °C (min, log)"); ax.set_ylabel("Success E0–E5")
    ax.set_title("Collision τ_eq × success × information\n(filled = information preserved · hollow = partial or unknown · grey X = low flow, τ_eq not comparable)", loc="left", fontsize=10, color=INK)
    fig.tight_layout(); fig.savefig(fig_dir / "E2_tau_E.png", dpi=150); plt.close(fig)
    dh = [p["tau"] for p in iso.values() if p["clase"] == "hypothermia"]
    inv = (f"**Invariant of the collision:** the thermal layer (C2) and the ischemia layer (G1) agree: the hypothermic cases with E ≥ 4 "
           f"fall at τ_eq = {g(min(dh))}–{g(max(dh))} min, the same range as the reproducible normothermic ones (5–12.5 min). "
           "The dog with cold flush (120 min at 10 °C) lands at τ_eq ≈ 12.7 min: the same threshold as the normothermic dog (12.5 min). "
           "⇒ **τ_eq works as a single quantity across species and temperatures.** Above ~13 min, E4 appears only with partial information (deficit or hippocampal atrophy).")
    out.append(("E2 · Equivalent ischemia × success × information", "E2_tau_E.png",
        inv + "\n\n" + tabla(filas, ["point", "t min", "T °C", "τ_eq min (Q10 range)", "E", "info", "flow", "source"])))

    # ---------------------------------------------------------------- E3  mass × duration: reversibility frontier
    pts = {k: p for k, p in P.items() if p.get("t") and p.get("masa")}
    fig, ax = plt.subplots(figsize=(8, 5.8))
    _scatter(ax, pts, "masa", "t")
    ax.scatter(META["masa"], META["t"], s=140, marker="*", c=INK, zorder=4); ax.annotate(META["label"], (META["masa"], META["t"]), xytext=(-40, 8), textcoords="offset points", fontsize=8, color=INK)
    art = [p for p in pts.values() if p["artificial"] and p["E"] >= 3]
    par = sorted([p for p in art if not any(q["masa"] >= p["masa"] and q["t"] >= p["t"] and q is not p for q in art)], key=lambda p: p["masa"])
    ax.step([p["masa"] for p in par], [p["t"] for p in par], where="post", color=INK2, lw=2, label="Artificial frontier (E ≥ 3)")
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("System mass (g, log)"); ax.set_ylabel("Pause duration (min, log)")
    ax.set_title("Scale × duration collision: distance to the goal", loc="left", fontsize=11, color=INK)
    _leyenda(ax); fig.tight_layout(); fig.savefig(fig_dir / "E3_masa_t.png", dpi=150); plt.close(fig)
    best_t_at_M = max((p["t"] for p in art if p["masa"] >= META["masa"] * 0.25), default=None)
    best_m_at_t = max((p["masa"] for p in art if p["t"] >= META["t"]), default=None)
    cheb = min(max(math.log10(META["masa"] / p["masa"]), math.log10(META["t"] / p["t"])) for p in par)
    nat = [p for p in pts.values() if not p["artificial"]]
    brecha = (f"- **Artificial frontier (Pareto, E ≥ 3):** " + " → ".join(f"{p['label']} ({g(p['masa'])} g, {g(p['t'])} min)" for p in par) + "\n"
              f"- At the goal's mass (≥ 17.5 kg), the longest artificial pause with E ≥ 3 is **{g(best_t_at_M)} min** ⇒ **{math.log10(META['t']/best_t_at_M):.1f} orders of magnitude** of time are missing.\n"
              f"- At the goal's duration (≥ 1 year), the maximum artificial mass with E ≥ 3 is **{g(best_m_at_t) if best_m_at_t else 'none'}** ⇒ no artificial system with E ≥ 3 has reached 1 year.\n"
              f"- **Chebyshev distance from the goal to the frontier: {cheb:.1f} orders of magnitude** (the smallest simultaneous jump in mass and time).\n"
              f"- Natural biology already occupies the months-to-years region at 10–1000 g ({', '.join(p['label'] for p in nat)}): the goal lies outside the artificial frontier, but not outside what is biologically possible at small mass.")
    out.append(("E3 · Scale × duration (reversibility frontier)", "E3_masa_t.png", brecha))

    # ---------------------------------------------------------------- E4  LC × rates (scale layer against chemistry layer)
    fig, ax = plt.subplots(figsize=(8, 5))
    LCs = [10 ** (x / 40) for x in range(-60, 41)]
    cool = lambda L, a=pv["anc_rate"], L0=pv["anc_LC"]: a * (L0 / L) ** 2
    warm = lambda L, al=pv["alpha"], dT=pv["dT_rew"]: dT / ((3 * L / 100) ** 2 / al / 60)
    ax.plot(LCs, [cool(L) for L in LCs], color="#2a78d6", lw=2, label="Convective cooling (C3)")
    ax.plot(LCs, [warm(L) for L in LCs], color="#eb6834", lw=2, label="Recalentamiento convectivo (C1)")
    ax.axhline(pv["nano_rate"], color="#1baf7a", lw=2, label="Nanowarming 2 L (volume-independent)")
    for nom, v, ls in (("CCR M22", pv["CCR_M22"], ":"), ("CWR M22", pv["CWR_M22"], "--"), ("CCR VMP", pv["CCR_VMP"], ":"), ("CWR VMP", pv["CWR_VMP"], "--")):
        ax.axhline(v, color=MUTED, lw=1, ls=ls); ax.text(LCs[0] * 1.05, v * 1.12, nom, fontsize=7, color=MUTED)
    objs = [("rat kidney", lc_de_masa(1.5)), ("rabbit kidney", lc_de_masa(12.7)), ("human kidney", pv["LC_kidneyH"]),
            ("3 L bag", pv["anc_LC"]), ("body (mean)", pv["LC_body"]), ("trunk", pv["LC_trunk"])]
    for n, L in objs:
        ax.axvline(L, color=GRID, lw=1); ax.text(L, 3e-3, n, rotation=90, fontsize=7, color=INK2, va="bottom", ha="right")
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_ylim(1e-3, 1e5)
    ax.set_xlabel("Characteristic length LC (cm, log)"); ax.set_ylabel("Centre cooling rate (°C/min, log)")
    ax.set_title("Scale × chemistry collision: vitrification window by CPA", loc="left", fontsize=11, color=INK)
    _leyenda(ax); fig.tight_layout(); fig.savefig(fig_dir / "E4_LC_tasas.png", dpi=150); plt.close(fig)
    filas = []
    for nom, c in D["cpas"].items():
        LCc = pv["anc_LC"] * math.sqrt(pv["anc_rate"] / c["CCR"])
        LClo = rng["anc_LC"][0] * math.sqrt(rng["anc_rate"][0] / (c["CCR"] * (1.0 if nom != "M22" else rng["CCR_M22"][1] / pv["CCR_M22"])))
        cabe = [n for n, L in objs if L <= LCc]
        filas.append([nom, c["CCR"], c["M"], f"{g(LCc)} cm (worst case {g(LClo)})", ", ".join(cabe) or "—", c["tox_rango"]])
    choque = ("**Layer clash:** the vitrification window is closed by **cooling** (blue curve), not rewarming, because nanowarming raises the warming ceiling at any size. "
              "The window grows as CCR falls, which demands higher concentration and more aggressive chemistry ⇒ **the scale axis pushes on the toxicity axis**. "
              "The toxicity ordering (1 = lowest) is **ordinal with no common scale [P]**: the scale × toxicity collision is **unquantified** (see E6).")
    out.append(("E4 · Scale × chemistry (cool / rewarm / CPA)", "E4_LC_tasas.png",
        choque + "\n\n" + tabla(filas, ["CPA", "CCR °C/min", "M", "Max LC vitrifiable by convection", "objects that fit", "toxicity (ordinal, P)"])))

    # ---------------------------------------------------------------- E5  function × information
    cat = {}
    for p in P.values():
        fun = "high (E ≥ 3)" if p["E"] >= 3 else ("low (E1–E2)" if p["E"] >= 1 else "nula (E0)")
        cat.setdefault((fun, p["info"]), []).append(p["label"])
    filas = [[f, i, len(v), "; ".join(v)] for (f, i), v in sorted(cat.items())]
    txt = ("**Ontological collision:** function and information are separate axes. Cases that prove it: *Cat 60 min* (high function, partial information), "
           "*ASC* (no function, information yes), *C. elegans* (low measured function, information yes). "
           f"Organs have no information axis (n/a). **Gap:** no point simultaneously has E ≥ 4, measured information and a pause > 1 day in an artificial mammal.\n\n" +
           tabla(filas, ["function", "information", "n", "points"]))
    out.append(("E5 · Function × information", None, txt))

    # ---------------------------------------------------------------- E7  chemistry: concentration × temperature × protocol → outcome
    X = D.get("exposiciones", {})
    RES = {3: "no toxicity or full function", 2: "low or partial damage", 1: "damaging or sometimes fatal", 0: "letal"}
    filas = [[x["cpa"], g(x["M"]) if x["M"] else "—", g(x["T"]) if x["T"] is not None else "—", g(x["t"]) if x["t"] else "—",
              g(x["masa"]), x["sistema"], f"{x['res']} · {RES[x['res']]}", x["f"]] for x in X.values()]
    grupos = {}
    for x in X.values():
        if x["M"] and x["T"] is not None: grupos.setdefault((x["M"], x["T"]), []).append(x)
    choques = [f"a {g(M)} M y {g(T)} °C: " + " frente a ".join(f"{x['cpa']} → {x['res']}" for x in xs)
               for (M, T), xs in grupos.items() if len({x["res"] for x in xs}) > 1]
    txt = ("**Hallazgo calculado:** " + (f"there are {len(choques)} pairs with **the same concentration and the same temperature but the opposite outcome**: " + "; ".join(choques) +
           ". ⇒ Toxicity **is not a function of molarity or of temperature separately**: it is decided by composition (qv*) and by the loading and unloading protocol. "
           "The 'toxicity' dimension must be modelled as D_CPA(composition, T, t, protocol), not as one number per CPA." if choques else "no detectable collisions.") +
           "\n\n" + tabla(filas, ["CPA / protocol", "M", "T °C", "t min", "mass g", "system", "result (ordinal)", "source"]))
    out.append(("E7 · Chemistry: concentration × temperature × protocol → toxicity", None, txt))

    # ---------------------------------------------------------------- E6  matriz de encuentros (cobertura)
    dims = list(D["dimensiones"])
    tiene = lambda p, d: (p.get(d) is not None and p.get(d) not in ("unknown", "n/a")) if d not in ("tau", "tox") else \
        (d == "tau" and "tau" in p)
    leyes = {("T", "t"): "C2", ("t", "tau"): "G1", ("T", "tau"): "C2", ("masa", "CCR"): "C3", ("masa", "t"): "frontera", ("E", "info"): "O4",
             ("masa", "E"): "frontera", ("tau", "E"): "G1/X1", ("tau", "info"): "O4/X1", ("t", "E"): "frontera", ("CCR", "tox"): "L6 (qv*)", ("masa", "tox"): "C8", ("T", "fase"): "C2/G2"}
    # pairs with physical or clinical meaning (the rest is marked 'not applicable' so as not to inflate the gap list)
    PERTINENTES = {frozenset(x) for x in [("T", "t"), ("T", "tau"), ("t", "tau"), ("T", "fase"), ("t", "masa"), ("masa", "E"), ("t", "E"),
        ("tau", "E"), ("E", "info"), ("tau", "info"), ("t", "info"), ("fase", "info"), ("masa", "CCR"), ("CCR", "E"), ("CCR", "tox"),
        ("masa", "tox"), ("T", "tox"), ("t", "tox"), ("tox", "E"), ("fase", "E"), ("masa", "fase")]}
    filas, huecos = [], []
    for a, b in itertools.combinations(dims, 2):
        n = sum(1 for p in P.values() if tiene(p, a) and tiene(p, b))
        if {a, b} <= {"CCR", "tox"}: n = len(D["cpas"])
        elif "tox" in (a, b):
            otro = b if a == "tox" else a
            campo = {"T": "T", "t": "t", "masa": "masa", "E": "res"}.get(otro)
            n = sum(1 for x in D.get("exposiciones", {}).values() if campo and x.get(campo) is not None)
        ley = leyes.get((a, b)) or leyes.get((b, a)) or ""
        estado = "cuantificado" if n >= 3 and ley else ("law without data" if ley and n < 3 else ("data without a law" if n >= 3 else "**empty**"))
        if "tox" in (a, b): estado = ("cuantificado (ordinal)" if n >= 3 else ("**few data**" if n else "**empty**")) if {a, b} != {"CCR", "tox"} else "**no quantitative scale**"
        if frozenset((a, b)) not in PERTINENTES: estado = "not applicable"
        if estado.startswith("**") or estado == "law without data": huecos.append(f"{a}×{b}")
        filas.append([f"{D['dimensiones'][a]['nombre']} × {D['dimensiones'][b]['nombre']}", ley or "—", n, estado])
    HJ = ", ".join(huecos).replace("masa", "mass")
    txt = (f"{len(filas)} possible collisions among {len(dims)} dimensions; {len(PERTINENTES)} relevant. **Gaps (empty, unscaled, or law without data): {len(huecos)}**: {HJ} → these are the prioritized research list "
           "(each is a pair of layers whose clash cannot yet be computed).\n\n" + tabla(filas, ["collision", "law", "n points", "state"]))
    out.append(("E6 · Collision matrix (model coverage)", None, txt))

    doc = ("<!-- AUTO-GENERATED by red/encuentros.py (called from red/motor.py). DO NOT EDIT BY HAND. -->\n"
           "# StasisPath: collisions between layers\n\nEach layer of the framework is projected onto a dimension. Each pair of dimensions is a **collision**: "
           "a law draws a frontier, the data fall on one side or the other, and the verdict is computed. "
           "The data live in `red/stasispath.yaml → puntos`; changing a parameter or adding a point regenerates everything.\n\n"
           "Colours: blue = hypothermia/flow · orange = supercooling/controlled ice · green = glass · yellow = natural biology (the marker shape repeats the class).\n\n")
    for tit, fig, body in out:
        doc += f"## {tit}\n\n" + (f"![{tit}](red/fig/{fig})\n\n" if fig else "") + body + "\n"
    doc += "## Warnings from the layer collisions\n" + ("\n".join("- " + a for a in avisos) or "- none (no point crosses a frontier without a declared mechanism)") + "\n"
    (ROOT / "ENCUENTROS.md").write_text(doc)
    return avisos, huecos, cheb
