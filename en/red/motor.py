#!/usr/bin/env python3
"""StasisPath: the network engine. Single source of truth: red/stasispath.yaml.

  python3 red/motor.py             recompute everything and regenerate the documents
  python3 red/motor.py impacto X   list the nodes downstream of X (parameter, source, bound, claim...)

METHOD: every bound is evaluated at the corners of its parameters' ranges. The functions are monotonic
in each parameter, so the corners bound the full range without Monte Carlo (R5: no theatre).
A verdict that holds at every corner is mate (M); if it fails at any corner there is an escape
and the tension is preserved (A, R1).
"""
import hashlib, itertools, math, re, sys
from collections import defaultdict
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
RED = ROOT / "red"
D = yaml.safe_load(open(RED / "stasispath.yaml"))
PAR = D["parametros"]
RANK = {"A": 0, "P": 1, "V": 2, "M": 2, "ROTO": -1}
SCORE = {"M": 1.0, "V": 1.0, "P": 0.6, "A": 0.2, "ROTO": 0.0}

# ---------------------------------------------------------------- cotas
def _w(p, T):  # ventana C2 (min) a temperatura T
    return p["t37"] * p["Q10"] ** ((37 - T) / 10)

def _rate(p, LC):  # convective cooling at the centre (°C/min), anchored on 3 L
    return p["anc_rate"] * (p["anc_LC"] / LC) ** p["exp_LC"]

def C1(p):
    rs = lambda cwr: math.sqrt(p["alpha"] * p["dT_rew"] / (cwr / 60)) * 100
    o = {"rstar_M22": rs(p["CWR_M22"]), "rstar_VMP": rs(p["CWR_VMP"])}
    v = {"VMP requires volumetric warming above 1 cm": (o["rstar_VMP"] < 1, True),
         "M22 cannot be surface-rewarmed in the trunk (r ~15 cm)": (o["rstar_M22"] < 15, True)}
    return o, v

def C2(p):
    T10 = 37 + 10 * math.log(p["t37"] / (10 * 525600)) / math.log(p["Q10"])
    o = {"w15": _w(p, 15), "w10": _w(p, 10), "w0": _w(p, 0), "T10y": T10}
    T10f = 37 + 10 * math.log(p["t37"] / (10 * 525600)) / math.log(p["Q10_frio"])
    o["T10y_cold"] = T10f
    v = {"10 years require T < 0 °C under ANY measured Q10 (temperate and cold)": (T10 < 0 and T10f < 0, True),
         "the cold-branch Q10 requires LESS cold than the temperate one (non-linearity, NOT significant in the source)": (T10f > T10, False)}
    return o, v

def C3(p):
    n = p["exp_LC"]
    o = {"LCstar_M22": p["anc_LC"] * (p["anc_rate"] / p["CCR_M22"]) ** (1 / n),
         "LCstar_VMP": p["anc_LC"] * (p["anc_rate"] / p["CCR_VMP"]) ** (1 / n),
         "rate_kidneyH": _rate(p, p["LC_kidneyH"]), "rate_body": _rate(p, p["LC_body"]),
         "rate_trunk": _rate(p, p["LC_trunk"])}
    v = {"VMP does not vitrify a human kidney by convection": (o["rate_kidneyH"] < p["CCR_VMP"], True),
         "M22 vitrifies the average body (LC ~3.9 cm)": (o["rate_body"] >= p["CCR_M22"], False),
         "M22 fails at the centre of the trunk": (o["rate_trunk"] < p["CCR_M22"], False)}
    return o, v

def C4(p):
    o = {"frog": p["frog_days"] * 1440 / _w(p, -6.3), "turtle": p["turtle_days"] * 1440 / _w(p, 3),
         "turtle22": p["turtle22_h"] * 60 / _w(p, 22)}
    v = {"frog > ×100": (o["frog"] > 100, True), "turtle > ×100": (o["turtle"] > 100, True),
         "turtle at 22 °C > ×10 (non-thermal)": (o["turtle22"] > 10, True)}
    return o, v

def C5(p):
    kg = lambda f: p["BMR"] * f * 365 / 7700
    o = {"kg25": kg(0.25), "kg3": kg(0.03)}
    return o, {"1 year at 25 % < 30 kg of fat": (o["kg25"] < 30, True)}

def C6(p):
    r4 = _rate(p, 4.0)
    Q = 0.5 * 0.8 * 334e3            # J: freezing 50 % of the water of 1 kg
    P = 100 * (1e-3 / 0.04) * 10     # W: h = 100, A = V/LC, ΔT = 10 K
    o = {"rate4": r4, "latent4": Q / P / 60}
    v = {"LC 4 cm within the slow window 0.1–1 °C/min": (0.1 <= r4 <= 1.0, True),
         "latent heat < 3 h": (o["latent4"] < 180, True)}
    return o, v

def C7(p):
    o = {"tau_org_good": p["tau_org_good"], "tau_org_surv": p["tau_org_surv"], "tau_cel": p["tau_cel"],
         "f_org": p["tau_org_good"] / p["t37"], "f_cel": p["tau_cel"] / p["t37"],
         "legal_x": p["tau_org_good"] / p["legal_obs"]}
    o["f_exist"] = p["tau_org_exist"] / p["t37"]
    v = {"grey zone: τ_cel > τ_org (survives with deficit)": (p["tau_cel"] > p["tau_org_surv"], True),
         "existence outside the reproducible range: τ_org,good < τ_exist ≤ τ_cel": (p["tau_org_good"] < p["tau_org_exist"] <= p["tau_cel"], True),
         "legal death is declared before the organism threshold": (p["legal_obs"] <= p["tau_org_good"], True)}
    return o, v

def C8(p):
    req = _rate(p, 4.0)
    o = {"CCR_req4": req}
    v = {"VMP insufficient at LC 4 cm": (p["CCR_VMP"] > req, True),
         "M22 sufficient at LC 4 cm": (p["CCR_M22"] <= req, False)}
    return o, v

def C9(p):
    w = _w(p, p["hypo_case_T"])
    o = {"w137": w, "extra": p["hypo_case_min"] / w}
    return o, {"zero flow in C2 does not explain it (×>3) ⇒ there was low flow": (o["extra"] > 3, True)}

def C11(p):
    # Cold-injury band: 0-20 C (F53). Crossing it fast reduces damage; extracellular ice requires slow.
    banda = 20.0
    lento = 1.0                      # C/min, ceiling of the 'slow' window for extracellular ice
    t_banda = banda / lento          # min taken to cross the band when cooling slowly
    r4 = _rate(p, 4.0)               # what convection gives at LC 4 cm
    o = {"t_banda_lento": t_banda, "t_banda_conv": banda / r4, "rate4": r4}
    return o, {"crossing the 0-20 C band while cooling slowly takes > 15 min (real exposure)": (t_banda > 15, True),
               "at LC 4 cm convection is even slower than the slow ceiling": (r4 < lento, True)}

def C10(p):
    w = _w(p, p["flush_T"])            # dog: temperature achieved with the flush
    wp = _w(p, p["pig_T"])             # pig: its own temperature (F42), not the dog's
    o = {"w": w, "w_pig": wp, "extra": p["flush_min"] / w, "extra_pig": p["pig_min"] / wp}
    return o, {
        # The PIG is the key verdict: same hypothermia protocol, without aortic flush.
        "C2 calibrates within ×5 against the PIG at 10 °C": (o["extra_pig"] < 5, True),
        "C2 is conservative versus the pig (not robust: at the generous corner it becomes OPTIMISTIC)": (o["extra_pig"] >= 1, False),
        # The DOG with flush stays non-key: its protocol adds aortic washout, so it is not a clean comparison.
        "C2 within ×5 of the dog with flush (different protocol, not key)": (o["extra"] < 5, False)}

COTAS = {k: globals()[k] for k in D["cotas"]}

def evaluar(cid):
    deps = D["cotas"][cid]["deps"]
    base = {k: v["v"] for k, v in PAR.items()}
    oc, vc = COTAS[cid](base)
    rng = {k: [x, x] for k, x in oc.items()}
    robust = {k: ok for k, (ok, _) in vc.items()}
    for combo in itertools.product(*[PAR[d]["r"] for d in deps]):
        q = dict(base); q.update(zip(deps, combo))
        o, v = COTAS[cid](q)
        for k, x in o.items():
            rng[k][0] = min(rng[k][0], x); rng[k][1] = max(rng[k][1], x)
        for k, (ok, _) in v.items():
            robust[k] = robust[k] and ok
    ver = []
    for k, (ok, clave) in vc.items():
        est = "ROTO" if not ok else ("M" if robust[k] else "A")
        ver.append({"t": k, "central": ok, "robusto": robust[k], "clave": clave, "e": est})
    claves = [x["e"] for x in ver if x["clave"]] or ["M"]
    estado = min(claves, key=lambda s: RANK[s])
    return {"out": oc, "rng": rng, "ver": ver, "e": estado}

def fmt(c, lo, hi):
    f = lambda x: f"{x:.3g}" if abs(x) < 1e4 else f"{x:,.0f}"
    return f(c) if abs(hi - lo) <= 1e-9 * max(1, abs(c)) else f"{f(c)} ({f(lo)}–{f(hi)})"

R = {cid: evaluar(cid) for cid in D["cotas"]}
# text derived from C3: trunk verdict
tv = next(x for x in R["C3"]["ver"] if x["t"].startswith("M22 fails at the centre"))
R["C3"]["txt"] = {"trunk_verdict": "impossible (robust)" if tv["robusto"] else
                  ("indeterminate: trunk LC inside the LC* band" if tv["central"] else "possible")}

# ---------------------------------------------------------------- derivadas
# Quantities computed from parameters and from one another. They are resolved by dependency
# and become available in the text of any node as {name}.
DERIV, _ns = {}, {"math": math, **{k: v["v"] for k, v in PAR.items()}}
_pend = dict(D.get("derivadas", {}))
for _ in range(len(_pend) + 2):
    for k, v in list(_pend.items()):
        try:
            _ns[k] = eval(v["expr"], _ns)
        except Exception:
            continue
        DERIV[k] = _ns[k]; _pend.pop(k)
    if not _pend: break
DERIV_FALLAN = list(_pend)

def rellenar(s):
    def sub(m):
        k = m.group(1)
        if k in DERIV and not callable(DERIV[k]):
            return fmt(DERIV[k], DERIV[k], DERIV[k])
        if "." in k:
            c, o = k.split(".")
            if o in R[c].get("txt", {}): return R[c]["txt"][o]
            lo, hi = R[c]["rng"][o]; return fmt(R[c]["out"][o], lo, hi)
        pv = PAR[k]; return fmt(pv["v"], *pv["r"])
    return re.sub(r"\{([A-Za-z0-9_\.]+)\}", sub, s)

# ---------------------------------------------------------------- grafo y estatus
NODOS = {}   # id -> {"tipo","e_decl","deps"}
for k, v in D["fuentes"].items(): NODOS[k] = {"tipo": "fuente", "e": v["estatus"], "deps": []}
for k, v in PAR.items(): NODOS[k] = {"tipo": "param", "e": v["e"], "deps": [v["f"]] if v["f"] else []}
for k, v in D["cotas"].items(): NODOS[k] = {"tipo": "cota", "e": R[k]["e"], "deps": v["deps"] + v["fuente_verif"]}
for k, v in D["afirmaciones"].items(): NODOS[k] = {"tipo": "afirmacion", "e": v["e"], "deps": v["deps"]}
for k, v in D["vias"].items(): NODOS[k] = {"tipo": "via", "e": v["e"], "deps": v["deps"]}
PR = D["preregistro"]
for k in [x for x in PR if x != "fecha"]: NODOS[k] = {"tipo": "prereg", "e": PR[k]["e"], "deps": PR[k]["deps"]}
for k, v in D["preguntas"].items(): NODOS[k] = {"tipo": "pregunta", "e": "M", "deps": v["a"]}

faltan = [(n, d) for n, x in NODOS.items() for d in x["deps"] if d not in NODOS]

# AUDITORÍA DE DECLARACIONES OBSOLETAS (tanda 47): un nodo declarado [A] o [P] cuyas dependencias
# that they are ALL strong is suspicious: their declaration may have been written before the sources
# were verified. It is not raised on its own (that would inflate the number): it is FLAGGED for manual review.
def auditoria_declaraciones():
    fuera = []
    for n, x in NODOS.items():
        if x["tipo"] in ("param", "prereg", "pregunta") or x["e"] not in ("A", "P"): continue
        deps = [d for d in x["deps"] if d in NODOS and NODOS[d]["tipo"] != "param"]
        if deps and all(EF.get(d) in ("V", "M") for d in deps):
            fuera.append((n, [(d, EF[d]) for d in deps]))
    return fuera
EF, MOTIVO = {}, {}
def efectivo(n, pila=()):
    if n in EF: return EF[n]
    x = NODOS[n]; e = x["e"]; motivo = None
    if x["tipo"] == "prereg":
        # A preregistration is not worth less because what it tests is open: THAT is its purpose.
        # It is judged by its specification (thresholds, n, blinding, falsification), which is its declared status.
        EF[n] = e; MOTIVO[n] = None
        return e
    for d in x["deps"]:
        if d not in NODOS or NODOS[d]["tipo"] == "param" or d in pila: continue  # the parameters enter via the bounds
        ed = efectivo(d, pila + (n,))
        if RANK[ed] < RANK[e]: e, motivo = ed, d
    EF[n] = e; MOTIVO[n] = motivo
    return e
for n in NODOS: efectivo(n)
for q in D["preguntas"]:   # a question is worth as much as its weakest answer
    EF[q] = min((EF[a] for a in D["preguntas"][q]["a"]), key=lambda s: RANK[s])

INV = defaultdict(set)
for n, x in NODOS.items():
    for d in x["deps"]: INV[d].add(n)

def impacto(x):
    vis, cola = [], [x]
    while cola:
        for m in sorted(INV[cola.pop(0)]):
            if m not in vis: vis.append(m); cola.append(m)
    return vis

# ---------------------------------------------------------------- preregistro (R2)
# Each preregistration is frozen separately: adding a new one is legitimate, editing one already frozen is ALARM R2.
IDS_PR = [k for k in PR if k != "fecha"]
HASHES = {k: hashlib.sha256((PR["fecha"] + PR[k]["t"]).encode()).hexdigest() for k in IDS_PR}
lock = RED / "prereg.lock"
guardado = {}
if lock.exists():
    for ln in lock.read_text().splitlines():
        if ":" in ln: kk, vv = ln.split(":", 1); guardado[kk.strip()] = vv.strip()
        elif ln.strip(): guardado["P15_P18_legacy"] = ln.strip()
nuevos = [k for k in IDS_PR if k not in guardado]
rotos = [k for k in IDS_PR if k in guardado and guardado[k] != HASHES[k]]
if "P15_P18_legacy" in guardado and not rotos:
    legacy = hashlib.sha256((PR["fecha"] + PR["P15"]["t"] + PR["P18"]["t"]).encode()).hexdigest()
    if legacy != guardado["P15_P18_legacy"]: rotos = ["P15/P18 (formato antiguo)"]
lock.write_text("\n".join(f"{k}: {HASHES[k]}" for k in IDS_PR) + "\n")
if rotos: PRE_ESTADO = f"**ALARM R2: edited after freezing: {', '.join(rotos)}**"
elif nuevos: PRE_ESTADO = f"intact; frozen today: {', '.join(nuevos)} ({len(IDS_PR)} in total)"
else: PRE_ESTADO = f"intact ({len(IDS_PR)} preregistrations)"
h = HASHES[IDS_PR[0]]

# ---------------------------------------------------------------- progreso
# Each component is defined by node TYPE (not by id prefix: a new prefix used to fall outside the computation).
COMP = [("Ontology", 15, {"afirmacion"}, {"ontologia"}), ("Magnitudes and thresholds", 35, {"afirmacion"}, {"magnitud", "frontera"}),
        ("Laws and bounds", 15, {"afirmacion", "cota"}, {"ley", None}), ("Pathways", 10, {"via"}, None),
        ("Falsifiable preregistration", 15, {"prereg"}, None), ("Preguntas respondidas", 10, {"pregunta"}, None)]
def comp_score(tipos, capas):
    ns = [n for n in EF if NODOS[n]["tipo"] in tipos and
          (capas is None or D["afirmaciones"].get(n, {}).get("capa") in capas)]
    return (sum(SCORE[EF[n]] for n in ns) / len(ns), len(ns)) if ns else (0.0, 0)
PROG = [(nom, w, *comp_score(tp, cp)) for nom, w, tp, cp in COMP]
TOTAL = sum(w * s for _, w, s, _ in PROG)

# ---------------------------------------------------------------- salidas
AUTO = "<!-- AUTO-GENERATED by red/motor.py from red/stasispath.yaml. DO NOT EDIT BY HAND. -->\n"
def badge(n): return f"**{EF[n]}**" + ("" if EF[n] == NODOS[n]["e"] or NODOS[n]["tipo"] == "pregunta" else f" (declared {NODOS[n]['e']}, downgraded by {MOTIVO[n]})")
def tabla(filas, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join("| " + " | ".join(str(c) for c in f) + " |" for f in filas) + "\n"

def sec_cotas():
    out = []
    for cid, c in D["cotas"].items():
        r = R[cid]
        outs = ", ".join(f"{k} = {fmt(r['out'][k], *r['rng'][k])}" for k in r["out"])
        vers = "; ".join(f"{'✔' if v['central'] else '✘'} {v['t']} → {v['e']}{'' if v['clave'] else ' (non-key)'}" for v in r["ver"])
        out.append([cid, c["titulo"], outs, vers, f"**{r['e']}**"])
    return tabla(out, ["bound", "law", "outputs: central (range at corners)", "verdicts", "status"])

def cap(capa): return [n for n, v in D["afirmaciones"].items() if v["capa"] == capa]
def bloque(ids): return "\n".join(f"- **{n}** [{badge(n)}] {rellenar(D['afirmaciones'][n]['t'])}" for n in ids) + "\n"

vias = [[k, v["via"], rellenar(v["mec"]), rellenar(v["escala"]), rellenar(v["ventana"]), rellenar(v["fallo"]), badge(k)] for k, v in D["vias"].items()]
TV = tabla(vias, ["id", "pathway", "mechanism", "demonstrated scale", "window", "typical failure", "status"])
preg = [[k, v["t"], ", ".join(v["a"]), f"**{EF[k]}**"] for k, v in D["preguntas"].items()]
TQ = tabla(preg, ["#", "question", "answers", "effective status"])
TP = tabla([[n, f"{w} %", f"{s*100:.0f} %", k, f"{w*s:.1f}"] for n, w, s, k in PROG] + [["**Total**", "", "", "", f"**{TOTAL:.1f} %**"]],
           ["component", "weight", "achieved", "nodes", "contributes"])
FU = "\n".join(f"- **{k}** [{v['estatus']}] {v['cita']}: {v['url']}" for k, v in D["fuentes"].items())
avisos = [f"- dependencia inexistente: {n} → {d}" for n, d in faltan]
avisos += [f"- {n}: declared {NODOS[n]['e']}, effective {EF[n]} (due to {MOTIVO[n]})" for n in NODOS if MOTIVO.get(n) and NODOS[n]["tipo"] != "pregunta"]
abiertos = [n for n in NODOS if EF[n] == "A" and NODOS[n]["tipo"] in ("afirmacion", "cota", "via")]

marco = AUTO + f"""# {D['meta']['titulo']}

> **Canonical question:** {D['meta']['pregunta']}
> Automatically generated version · preregistration {PRE_ESTADO} · grounding **{TOTAL:.0f} %**
> Status: M = mate (bound robust across the whole range) · V = verified against a primary source · P = prior or secondary source · A = open (tension preserved)

Layer collisions: **[ENCUENTROS.md](ENCUENTROS.md)** · Gaps to human: **[BRECHAS.md](BRECHAS.md)** · Scaling and validation: **[ESCALADO.md](ESCALADO.md)** · Margins: **[MARGENES.md](MARGENES.md)** · Derivation and P19 prediction: **[DERIVACION.md](DERIVACION.md)** · Internal formulation: **[FORMULACION.md](FORMULACION.md)** · Triangulation: **[TRIANGULACION.md](TRIANGULACION.md)** · Precision: **[PRECISION.md](PRECISION.md)** · Sweep: **[BARRIDO.md](BARRIDO.md)** · Conditional projection: **[PROYECCION.md](PROYECCION.md)**

## 1. Ontology
{bloque(cap('ontologia'))}
## 2. State space: magnitudes and thresholds
A system is in **reversible pause** if and only if every magnitude stays below its threshold during entry, storage and exit.
{bloque(cap('magnitud'))}
## 3. Scaling laws (the status of each is set by the network)
{bloque(cap('ley'))}
### 3.1 Bounds: computation at the corners of the parameter ranges
{sec_cotas()}
## 4. Empirical frontier
{bloque(cap('frontera'))}
## 5. Pathways
{TV}
## 6. Preregistration (frozen on {PR['fecha']}; hash {h[:12]})
{chr(10).join(rellenar(PR[k].get('t_en') or PR[k]['t']) + (chr(10) + "> " + rellenar(PR[k]['enmiendas']).replace(chr(10), chr(10) + "> ") if PR[k].get('enmiendas') else "") for k in IDS_PR)}
## 7. Canonical questions
{TQ}
## 8. Open tensions (R1)
{chr(10).join('- ' + n + ': ' + (rellenar(D['afirmaciones'][n]['t']) if n in D['afirmaciones'] else D['cotas'][n]['titulo'] if n in D['cotas'] else D['vias'][n]['via']) for n in abiertos) or '- none'}

## 9. Grounding (computed from the node statuses)
{TP}
Score per node: M/V = 1 · P = 0.6 · A = 0.2 · BROKEN = 0.

## 10. Sources
{FU}
"""
(ROOT / "MARCO.md").write_text(marco)
(ROOT / "00_marco" / "preguntas.md").write_text(AUTO + "# Canonical questions\n\n" + TQ)
(ROOT / "40_vias" / "tabla_vias.md").write_text(AUTO + "# Pathway table\n\n" + TV)
(ROOT / "00_marco" / "progreso.md").write_text(AUTO + "# Grounding\n\n" + TP)

# grafo mermaid
col = {"M": "fill:#1b7f3b,color:#fff", "V": "fill:#2e9e57,color:#fff", "P": "fill:#e0a800", "A": "fill:#c0392b,color:#fff", "ROTO": "fill:#000,color:#fff"}
g = ["flowchart LR"]
capas = {"param": "Parameters", "cota": "Bounds", "afirmacion": "Claims", "prereg": "Preregistration", "via": "Pathways", "pregunta": "Questions"}
for t, nom in capas.items():
    g.append(f"  subgraph {t}[{nom}]")
    g += [f"    {n}[{n}]" for n, x in NODOS.items() if x["tipo"] == t]
    g.append("  end")
for n, x in NODOS.items():
    if x["tipo"] == "fuente": continue
    g += [f"  {d} --> {n}" for d in x["deps"] if d in NODOS and NODOS[d]["tipo"] != "fuente"]
for s, c in col.items(): g.append(f"  classDef {s.lower()} {c}")
for n, x in NODOS.items():
    if x["tipo"] != "fuente": g.append(f"  class {n} {EF[n].lower()}")
(RED / "grafo.md").write_text(AUTO + "# StasisPath network\n\nGreen = M/V · amber = P · red = A · black = BROKEN. Arrows run from dependency to dependent node.\n\n```mermaid\n" + "\n".join(g) + "\n```\n")
DER_TXT = "\n## Derived quantities (computed, never written by hand)\n" + tabla(
    [[k, D["derivadas"][k].get("u", ""), fmt(DERIV[k], DERIV[k], DERIV[k]) if not callable(DERIV[k]) else "function",
      D["derivadas"][k].get("d", "")] for k in DERIV], ["quantity", "unit", "value", "what it is"])
if DERIV_FALLAN: DER_TXT += f"\n**Could not be evaluated:** {', '.join(DERIV_FALLAN)}\n"
ORG_TXT = "\n## Organs (one line each; everything else is computed)\n" + tabla(
    [[n, f"{m:,}", fmt(DERIV["LC_esfera"](m), 0, 0), fmt(DERIV["tasa_conv"](DERIV["LC_esfera"](m)), 0, 0),
      fmt(DERIV["M_de_CCR"](DERIV["tasa_conv"](DERIV["LC_esfera"](m))), 0, 0),
      "viable" if DERIV["M_de_CCR"](DERIV["tasa_conv"](DERIV["LC_esfera"](m))) <= DERIV["M_toxico"] else "**not viable**"]
     for n, m in D.get("organos", {}).items()],
    ["organ", "mass g", "LC cm", "rate °C/min", "required M", "verdict"])
import cruce
CRU = cruce.generar(D, PAR, ROOT)
print(f"Layer cross-check: {CRU['n_pts']} points against the thermal law · {CRU['excesivos']} require a non-thermal mechanism · "
      + (f"BRECHA artificial x{CRU['max_art']:.3g} | natural x{CRU['min_nat']:.3g}" if CRU['brecha'] else "no clean gap")
      + f" · {len(CRU['sin_check'])} pathways with no numerical window")
import cascada
CAS = cascada.generar(D, PAR, DERIV, ROOT)
print(f"Cascade: the WHOLE framework combined honestly = {100*CAS['p_honesta']:.0f} % (naive {100*CAS['p_ingenua']:.0f} %, "
      f"{CAS['n_grupos']} independent anchors) · the Arrhenius chain alone {100*CAS['p_pasa']:.0f} % · "
      f"median damage {CAS['mediana']:.3g} (90 % {CAS['p05']:.3g}-{CAS['p95']:.3g}) · does NOT close X2")
import espacio
ESP = espacio.generar(D, PAR, DERIV, ROOT)
print(f"Space of X2: required CCR {ESP['ccr_req']:.3g} C/min · {len(ESP['con_ccr'])} vitrify, {len(ESP['con_fun'])} with neural function, intersection EMPTY · target region {'excluded' if ESP['excluida'] else 'NOT excluded by any law'}")
import rumbo
RUMBO = rumbo.generar(D, NODOS, RANK, SCORE, COMP, ROOT)
print(f"Course: {RUMBO['base']:.1f} % -> goal {RUMBO['meta']:.1f} % · {len(RUMBO['camino'])} closures reach {RUMBO['final']:.1f} % · ceiling with everything open closed {RUMBO['techo']:.1f} %")
import proyeccion
PROY = proyeccion.generar(D, PAR, DERIV, ROOT, TOTAL, RUMBO)
print(f"Projection: we have +-{PROY['med_t']*100:.0f} % vs we need +-{PROY['med_n']*100:.0f} % · scenario ceiling {PROY['proy']:.1f} % · irreducible {PROY['irreducible']:.1f} %")

(RED / "informe.md").write_text(AUTO + DER_TXT + ORG_TXT + f"\n# Network report\n\nNodes: {len(NODOS)} · preregistration: {PRE_ESTADO} · grounding: {TOTAL:.1f} %\n\n## Warnings\n" + ("\n".join(avisos) or "- none") + "\n\n## Bounds\n" + sec_cotas())

sys.path.insert(0, str(RED))
import encuentros
ENC_AVISOS, ENC_HUECOS, ENC_CHEB = encuentros.generar(D, PAR, R, ROOT)
import barrido
CORTES, CORTE_NADES = barrido.generar(D, PAR, DERIV, ROOT)
PLANO = barrido.plano_diseno(D, PAR, DERIV, ROOT)
print(f"Sweep: {len(CORTES)} margins swept · eutectic-solvent cut-off CCR={CORTE_NADES:.3g} C/min")
import precision
PREC = precision.generar(D, PAR, DERIV, ROOT)
print(f"Precision: Bi=1 at LC={PREC['LC_crit']:.2f} cm · Monte Carlo median viable mass {PREC['mediana']:.1f} kg (p5 {PREC['p5']:.1f}, p95 {PREC['p95']:.1f})")
import triangular
TRI = triangular.generar(D, PAR, DERIV, ROOT)
_con = [r for r in TRI if "contradiction" in str(r[2])]
print(f"Triangulation: {len(TRI)} unknowns projected · {len(_con)} with CONTRADICTION" + (": " + ", ".join(r[0] for r in _con) if _con else ""))
import formular
FOR = formular.generar(D, PAR, ROOT)
print(f"Formulation: {FOR['n_formulas']} formulas · viability limit LC={FOR['lc_critico']:.2f} cm ~ {FOR['m_critico']/1000:.1f} kg")
import derivar
DER = derivar.generar(ROOT)
print(f"Derivation: Arrhenius Ea/R={DER['EaR']:.0f}K -> predicted P19 cold arm {DER['pred']:.3f} (vs {DER['caliente']:.2f} warm, x{DER['factor']:.0f}) · anchors {'OK' if DER['anclas_ok'] else 'FAIL'}")
import margenes
MG_FILAS, MG_FRAGILES = margenes.generar(D, PAR, COTAS, ROOT)
print(f"Margins: {len(MG_FRAGILES)} verdicts with slack < 2 out of {len(MG_FILAS)}")
import p21
P21R = p21.generar(D, ROOT)
print(f"P21: {P21R['estado']} · {P21R['motivo']}")
import confianza
CF = confianza.generar(D, PAR, COTAS, ROOT)
print(f"Confidence: P(any key verdict fails) = {confianza.pct(CF['p_alguna'])} (pessimistic {confianza.pct(CF['p_alguna1'])}) · "
      f"{len(CF['riesgo'])} non-key > 1 % · measure first: {', '.join(d for d, _ in CF['prio1'][:3])}")
import escalado
ESC = escalado.generar(D, PAR, R, ROOT)
print(f"Scaling: tau_eq valid (error x{ESC['err_tau']:.1f}) - thermal valid (x{ESC['err_term']:.1f}) - neurons r={ESC['r_neu']:+.2f} (not valid)")
import brechas
BR, RUTAS = brechas.generar(D, PAR, R, ROOT)
print("Gaps to human: " + " · ".join(f"{v['nom'].split(' (')[0]}: bottleneck {v['cuello']} {BR[v['cuello']]['pct']:.0f} %" for v in RUTAS.values()))
with open(RED / "informe.md", "a") as fh:
    fh.write(f"\n## Layer collisions\n- distance from the goal to the frontier: {ENC_CHEB:.1f} orders of magnitude\n- gaps: {', '.join(ENC_HUECOS)}\n"
             + "".join(f"- {a}\n" for a in ENC_AVISOS))

if len(sys.argv) > 2 and sys.argv[1] == "impacto":
    x = sys.argv[2]; imp = impacto(x)
    print(f"If you change {x}, {len(imp)} nodes are recomputed or re-evaluated:")
    for t in ("cota", "afirmacion", "via", "prereg", "pregunta"):
        s = [m for m in imp if NODOS[m]["tipo"] == t]
        if s: print(f"  {t:11s}: {', '.join(s)}")
else:
    print(f"OK · {len(NODOS)} nodes · grounding {TOTAL:.1f} % · preregistration {PRE_ESTADO}")
    for cid in R: print(f"  {cid}: {R[cid]['e']:4s} " + " | ".join(f"{'✔' if v['central'] else '✘'}{'R' if v['robusto'] else '~'} {v['t']}" for v in R[cid]["ver"]))
    print("Warnings:\n" + ("\n".join(avisos) or "  none"))
    _aud = auditoria_declaraciones()
    print(f"Declaration audit: {len(_aud)} node(s) declared weak with ALL their dependencies strong"
          + (" — check whether the declaration is stale:" if _aud else " (none)"))
    for _n, _ds in _aud:
        print(f"  {_n} [{NODOS[_n]['e']}] <- " + ", ".join(f"{d}[{e}]" for d, e in _ds))
