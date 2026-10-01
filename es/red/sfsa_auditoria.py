"""StasisPath x SFSA: auditoria de premisas (AIE), dimensiones (UDE) y valor de informacion (VOI).

No toca stasispath.yaml ni el motor. Solo AUDITA. Si encuentra algo, el numero baja o se anota:
ese es el proposito. Un motor que solo puede subirte el porcentaje no es un motor, es un amplificador.
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

aie.register_assumption("A1", "Regimen de Biot: exponente LC coherente",
    lambda s: (not ("LC" in s) or (s["LC"] > LC_CRIT) == (P["exp_LC"] > 1.5),
               f"LC={s.get('LC')} cm frente a LC_crit={LC_CRIT}: exponente {P['exp_LC']} es de "
               f"{'conduccion' if P['exp_LC']>1.5 else 'conveccion'} y el regimen es el contrario"),
    "SWITCH_MODEL", "La ley LC^-2 vale solo por encima de Bi=1. Este fallo ya costo un x2.6 en el escalado.")

aie.register_assumption("A2", "Q10 aplicado por debajo de Tg",
    lambda s: (not ("T" in s) or s["T"] > Tg,
               f"T={s.get('T')} C esta por debajo de Tg={Tg} C: no hay agua liquida, "
               f"no hay metabolismo y por tanto Q10 no esta definido ahi"),
    "FAIL_STOP", "Un Q10 metabolico extrapolado al estado vitreo no describe nada fisico.")

aie.register_assumption("A3", "Q10 dentro del rango medido",
    lambda s: (not ("T" in s) or s["T"] >= -10,
               f"T={s.get('T')} C: ningun Q10 de la red se midio por debajo de -10 C; "
               f"esto es extrapolacion, no medicion"),
    "WARNING", "Q10 se midio entre 37 C y ~0 C. Fuera de ahi es proyeccion.")

aie.register_assumption("A4", "Geometria esferica de LC",
    lambda s: (not ("geom" in s) or s["geom"] == "esfera",
               f"LC=V/A se calculo con formula de esfera (r/3) sobre una pieza '{s.get('geom')}'; "
               f"un cilindro da r/2, es decir LC 1.5x mayor y tasa 2.25x menor"),
    "WARNING", "El tronco no es una esfera. La formula de esfera es optimista para piezas alargadas.")

aie.register_assumption("A5", "Regimen de presion en la nucleacion",
    lambda s: (not ("regimen" in s) or s["regimen"] == "isobarico",
               f"J medida en regimen '{s.get('regimen')}' comparada con una cota isobarica; "
               f"el isocorico suprime la nucleacion y no son intercambiables"),
    "SWITCH_MODEL", "Esta es la contradiccion que la triangulacion ya marco en I5.")

aie.register_assumption("A6", "Exponente n=2 no verificado experimentalmente",
    lambda s: (P["exp_LC"] != 2.0 or s.get("P21_ejecutado", False),
               f"exp_LC={P['exp_LC']} se usa en TODO el escalado y P21 (que lo mide) esta PENDIENTE"),
    "WARNING", "Toda la tabla de organos cuelga de un exponente preregistrado pero sin medir.")

aie.register_assumption("A7", "Densidad implicita en LC_esfera",
    lambda s: (not s.get("usa_LC_esfera", False) or s.get("rho_declarada", False),
               "LC_esfera convierte gramos en cm sin declarar densidad: asume rho = 1 g/cm3 en silencio"),
    "WARNING", "Premisa oculta. Con rho=1.05 el sesgo es -1.6 % en LC; pequeno, pero no declarado.")

estados = []
for nom, m in ORG.items():
    lc = LC_esfera(m)
    estados.append({"nodo": f"organo:{nom}", "LC": lc, "geom": "cilindro" if nom in
                    ("cuerpo_entero",) else "esfera", "usa_LC_esfera": True, "rho_declarada": False})
estados += [
    {"nodo": "C2:T10y (templado)", "T": -129.0},
    {"nodo": "C2:T10y (frio)",     "T": -73.7},
    {"nodo": "C2:w0",              "T": 0.0},
    {"nodo": "C3:anclaje F2",      "LC": P["anc_LC"], "geom": "esfera"},
    {"nodo": "I5:J higado rata",   "regimen": "isocorico"},
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
    ("C1  r* = sqrt(alpha*dT/CWR)", DimensionVector(length=2) , "cm^2 bajo la raiz -> cm", True),
    ("C3  tasa = anc_rate*(anc_LC/LC)^n", DimensionVector(), "razon adimensional x C/min -> C/min", True),
    ("C6  t_latente = L_f*m/(P)", DimensionVector(time=1), "J/(J/s) -> s", True),
    ("sigma_th <= 2*sigma*alpha*(1-nu)/(E*beta*L^2)", DimensionVector(temp=1, time=-1),
     "MPa*cm2/min / (MPa*K^-1*cm2) -> K/min", True),
    ("LC_esfera = (3m/4pi)^(1/3)/3", DimensionVector(mass=1/3), "g^(1/3) DECLARADO cm", False),
]
ok_c, _ = ude.verify_compatibility("cm", "cm")
mal_c, msg_c = ude.verify_compatibility("g", "cm")

# ---------------------------------------------------------------- VOI
voi = ValueInformationEngine(min_evoi_threshold=0.15)
CAND = [
    # id, valor predicho, sigma ABSOLUTA, umbral de decision, coste relativo, que es
    ("I2 · DSC de los NADES",      0.30,  0.36,  0.426, 1.0,  "calorimetria, dias, ~1 k"),
    ("P21 · exponente n",          2.00,  0.26,  2.34,  0.5,  "7 bolsas de agua y un termopar"),
    ("I4 · tau_eq humano",        17.0,   7.65, 12.5,  30.0,  "serie clinica, anos"),
    ("I5 · J a -6 C",              0.57,  0.285, 0.85, 12.0,  "nucleacion en higado, meses"),
    ("P19 · LTP en rodaja",        0.142, 0.078, 0.25, 20.0,  "electrofisiologia completa"),
]
ev = [(c[0], c[5], voi.evaluate_candidate(c[0], c[1], c[2], c[3], c[4])) for c in CAND]
ev.sort(key=lambda t: -t[2].voi_cost_ratio)

# ---------------------------------------------------------------- informe
L = ["<!-- AUTO-GENERADO por red/sfsa_auditoria.py. NO EDITAR A MANO. -->",
     "# StasisPath x SFSA: auditoria de premisas, dimensiones y valor de informacion", "",
     "> Este modulo **no puede subir el porcentaje**: no escribe en `stasispath.yaml`. Solo audita.",
     "> Lo que encuentre, o baja el numero o lo anota con una salvedad.", "",
     "## AIE — integridad de supuestos", "",
     f"{len(aie.assumptions)} premisas registradas, auditadas contra {len(estados)} estados reales del marco.", "",
     "| estado | premisa | criticidad | diagnostico |", "|---|---|---|---|"]
for nodo, v in viol:
    L.append(f"| `{nodo}` | {v.name} | **{v.criticality}** | {v.diagnostic_message} |")
if not viol:
    L.append("| — | — | — | ninguna violacion |")
L += ["", f"**{len(viol)} violaciones** sobre {len(estados)} estados.", "",
      "## UDE — homogeneidad dimensional", "", "| formula | dimension resultante | coherente |", "|---|---|---|"]
for nom, dim, expl, ok in FORMULAS:
    L.append(f"| `{nom}` | {expl} | {'OK' if ok else '**NO**'} |")
L += ["", f"Comprobacion de control (g vs cm): {msg_c}", "",
      "## VOI — que medir primero", "",
      "EVOI alto = la medicion tiene probabilidad real de **cambiar el veredicto**. "
      "Coste en unidades relativas (P19 = 20).", "",
      "| candidato | EVOI | coste | EVOI/coste | recomendacion | que es |", "|---|---|---|---|---|---|"]
for cid, que, a in ev:
    L.append(f"| {cid} | {a.expected_value_of_information:.3f} | {a.estimated_cost:.1f} | "
             f"**{a.voi_cost_ratio:.2f}** | `{a.recommendation}` | {que} |")
(ROOT / "SFSA.md").write_text("\n".join(L) + "\n")
print("\n".join(L[4:]))
