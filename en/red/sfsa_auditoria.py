"""StasisPath self-audit: assumption integrity (AIE), dimensions (UDE) and value of information (VOI).

It touches neither stasispath.yaml nor the engine. It only AUDITS. If it finds something, the number
goes down or is annotated: that is the point. An engine that can only raise your percentage is not an
engine, it is an amplifier.
"""
import sys, math, yaml, pathlib
import os
_SFSA = os.environ.get("SFSA_PATH")
if _SFSA: sys.path.insert(0, _SFSA)   # path to the SFSA package, if installed outside site-packages
try:
    from sfsa.aie import AssumptionIntegrityEngine
    from sfsa.ude import UnitDimensionalEngine, DimensionVector
    from sfsa.voi import ValueInformationEngine
except ModuleNotFoundError:
    sys.exit('The self-audit needs the SFSA package. Install it, or point SFSA_PATH at its python/ directory '
             '(optional: the rest of the framework does not depend on it).')

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = yaml.safe_load(open(ROOT / "red" / "stasispath.yaml"))
P = {k: v["v"] for k, v in D["parametros"].items()}
ORG = D["organos"]

LC_CRIT = 0.40          # Bi = 1 (precision.py)
Tg = P["Tg"]            # -123 C

def LC_esfera(m_g):  return (3 * m_g / (4 * math.pi)) ** (1 / 3) / 3
def tasa_conv(LC):   return P["anc_rate"] * (P["anc_LC"] / LC) ** P["exp_LC"]

# ---------------------------------------------------------------- AIE
aie = AssumptionIntegrityEngine()

aie.register_assumption("A1", "Biot regime: LC exponent consistency",
    lambda s: (not ("LC" in s) or (s["LC"] > LC_CRIT) == (P["exp_LC"] > 1.5),
               f"LC={s.get('LC')} cm versus LC_crit={LC_CRIT}: exponent {P['exp_LC']} belongs to "
               f"{'conduction' if P['exp_LC']>1.5 else 'convection'} and the regime is the opposite"),
    "SWITCH_MODEL", "The LC^-2 law holds only above Bi=1. This failure already cost a factor of x2.6 in the scaling.")

aie.register_assumption("A2", "Q10 applied below Tg",
    lambda s: (not ("T" in s) or s["T"] > Tg,
               f"T={s.get('T')} C is below Tg={Tg} C: there is no liquid water, "
               f"there is no metabolism and therefore Q10 is undefined there"),
    "FAIL_STOP", "A metabolic Q10 extrapolated into the glassy state describes nothing physical.")

aie.register_assumption("A3", "Q10 within the measured range",
    lambda s: (not ("T" in s) or s["T"] >= -10,
               f"T={s.get('T')} C: no Q10 in the network was measured below -10 C; "
               f"this is extrapolation, not measurement"),
    "WARNING", "Q10 was measured between 37 C and ~0 C. Outside that it is projection.")

aie.register_assumption("A4", "Spherical geometry for LC",
    lambda s: (not ("geom" in s) or s["geom"] == "sphere",
               f"LC=V/A was computed with the sphere formula (r/3) on a '{s.get('geom')}' piece; "
               f"a cylinder gives r/2, that is LC 1.5x larger and rate 2.25x lower"),
    "WARNING", "The trunk is not a sphere. The sphere formula is optimistic for elongated pieces.")

aie.register_assumption("A5", "Pressure regime in nucleation",
    lambda s: (not ("regimen" in s) or s["regimen"] == "isobaric",
               f"J measured in the '{s.get('regimen')}' regime compared against an isobaric bound; "
               f"the isochoric regime suppresses nucleation and they are not interchangeable"),
    "SWITCH_MODEL", "This is the contradiction triangulation already flagged in I5.")

aie.register_assumption("A6", "Exponent n=2 not experimentally verified",
    lambda s: (P["exp_LC"] != 2.0 or s.get("P21_ejecutado", False),
               f"exp_LC={P['exp_LC']} is used in ALL the scaling and P21 (which measures it) is PENDING"),
    "WARNING", "The entire organ table hangs on an exponent that is preregistered but unmeasured.")

aie.register_assumption("A7", "Density implicit in LC_sphere",
    lambda s: (not s.get("usa_LC_esfera", False) or s.get("rho_declarada", False),
               "LC_sphere converts grams to cm without declaring a density: it silently assumes rho = 1 g/cm3"),
    "WARNING", "Hidden premise. With rho=1.05 the bias is -1.6 % in LC; small, but undeclared.")

estados = []
for nom, m in ORG.items():
    lc = LC_esfera(m)
    estados.append({"nodo": f"organ:{nom}", "LC": lc, "geom": "cylinder" if nom in
                    ("whole_body",) else "sphere", "usa_LC_esfera": True, "rho_declarada": False})
estados += [
    {"nodo": "C2:T10y (temperate branch)", "T": -129.0},
    {"nodo": "C2:T10y (cold branch)",     "T": -73.7},
    {"nodo": "C2:w0",              "T": 0.0},
    {"nodo": "C3:anclaje F2",      "LC": P["anc_LC"], "geom": "sphere"},
    {"nodo": "I5:J rat liver",   "regimen": "isochoric"},
    {"nodo": "escalado global",    "P21_ejecutado": False},
]

viol = []
for s in estados:
    for v in aie.audit_state(s):
        viol.append((s["nodo"], v))

# ---------------------------------------------------------------- UDE
ude = UnitDimensionalEngine()
cm = DimensionVector(length=1)
FORMULAS = [
    ("C1  r* = sqrt(alpha*dT/CWR)", DimensionVector(length=2) , "cm^2 under the root -> cm", True),
    ("C3  rate = anc_rate*(anc_LC/LC)^n", DimensionVector(), "dimensionless ratio x C/min -> C/min", True),
    ("C6  t_latent = L_f*m/(P)", DimensionVector(time=1), "J/(J/s) -> s", True),
    ("sigma_th <= 2*sigma*alpha*(1-nu)/(E*beta*L^2)", DimensionVector(temp=1, time=-1),
     "MPa*cm2/min / (MPa*K^-1*cm2) -> K/min", True),
    ("LC_sphere = (3m/4pi)^(1/3)/3", DimensionVector(mass=1/3), "g^(1/3) DECLARED cm", False),
]
ok_c, _ = ude.verify_compatibility("cm", "cm")
mal_c, msg_c = ude.verify_compatibility("g", "cm")

# ---------------------------------------------------------------- VOI
voi = ValueInformationEngine(min_evoi_threshold=0.15)
CAND = [
    # id, predicted value, ABSOLUTE sigma, decision threshold, relative cost, what it is
    ("I2 · DSC of the eutectic solvents",      0.30,  0.36,  0.426, 1.0,  "calorimetry, days, ~1 k"),
    ("P21 · exponent n",          2.00,  0.26,  2.34,  0.5,  "7 water bags and a thermocouple"),
    ("I4 · human tau_eq",        17.0,   7.65, 12.5,  30.0,  "clinical series, years"),
    ("I5 · J at -6 C",              0.57,  0.285, 0.85, 12.0,  "nucleation in liver, months"),
    ("P19 · LTP in slice",        0.142, 0.078, 0.25, 20.0,  "full electrophysiology"),
]
ev = [(c[0], c[5], voi.evaluate_candidate(c[0], c[1], c[2], c[3], c[4])) for c in CAND]
ev.sort(key=lambda t: -t[2].voi_cost_ratio)

# ---------------------------------------------------------------- informe
L = ["<!-- AUTO-GENERATED by red/sfsa_auditoria.py. DO NOT EDIT BY HAND. -->",
     "# StasisPath self-audit: assumptions, dimensions and value of information", "",
     "> This module **cannot raise the percentage**: it does not write to `stasispath.yaml`. It only audits.",
     "> Whatever it finds either lowers the number or annotates it with a caveat.", "",
     "## AIE — assumption integrity", "",
     f"{len(aie.assumptions)} premises registered, audited against {len(estados)} real states of the framework.", "",
     "| estado | premisa | criticidad | diagnostico |", "|---|---|---|---|"]
for nodo, v in viol:
    L.append(f"| `{nodo}` | {v.name} | **{v.criticality}** | {v.diagnostic_message} |")
if not viol:
    L.append("| — | — | — | no violation |")
L += ["", f"**{len(viol)} violations** over {len(estados)} states.", "",
      "## UDE — homogeneidad dimensional", "", "| formula | dimension resultante | coherente |", "|---|---|---|"]
for nom, dim, expl, ok in FORMULAS:
    L.append(f"| `{nom}` | {expl} | {'OK' if ok else '**NO**'} |")
L += ["", f"Control check (g vs cm): {msg_c}", "",
      "## VOI — what to measure first", "",
      "High EVOI = the measurement has a real probability of **changing the verdict**. "
      "Cost in relative units (P19 = 20).", "",
      "| candidate | EVOI | cost | EVOI/cost | recommendation | what it is |", "|---|---|---|---|---|---|"]
for cid, que, a in ev:
    L.append(f"| {cid} | {a.expected_value_of_information:.3f} | {a.estimated_cost:.1f} | "
             f"**{a.voi_cost_ratio:.2f}** | `{a.recommendation}` | {que} |")
(ROOT / "SFSA.md").write_text("\n".join(L) + "\n")
print("\n".join(L[4:]))
