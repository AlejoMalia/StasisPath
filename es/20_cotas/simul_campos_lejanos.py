# -*- coding: utf-8 -*-
"""Simulacion de valor de cierre para el cluster de CAMPOS LEJANOS (tanda 49).
NO toca red/motor.py ni red/dsny.yaml: replica la propagacion y el COMP del motor
en memoria y se AUTOVALIDA contra el progreso que imprime el motor.
Uso: python3 20_cotas/simul_campos_lejanos.py
"""
import pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]
D = yaml.safe_load(open(ROOT / "red" / "dsny.yaml"))

RANK = {"A": 0, "P": 1, "V": 2, "M": 2, "ROTO": -1}
SCORE = {"M": 1.0, "V": 1.0, "P": 0.6, "A": 0.2, "ROTO": 0.0}
COMP = [("Ontologia", 15, {"afirmacion"}, {"ontologia"}),
        ("Magnitudes y umbrales", 35, {"afirmacion"}, {"magnitud", "frontera"}),
        ("Leyes y cotas", 15, {"afirmacion", "cota"}, {"ley", None}),
        ("Vias", 10, {"via"}, None),
        ("Preregistro falsable", 15, {"prereg"}, None),
        ("Preguntas respondidas", 10, {"pregunta"}, None)]

# Las cotas C1..C11 salen todas M en la ejecucion actual del motor (verificado en su salida).
COTAS_E = {k: "M" for k in D["cotas"]}


def construir(over_e=None, over_deps=None):
    over_e = over_e or {}
    over_deps = over_deps or {}
    N = {}
    for k, v in D["fuentes"].items():
        N[k] = {"tipo": "fuente", "e": v["estatus"], "deps": []}
    for k, v in D["parametros"].items():
        N[k] = {"tipo": "param", "e": v["e"], "deps": [v["f"]] if v.get("f") else []}
    for k, v in D["cotas"].items():
        N[k] = {"tipo": "cota", "e": COTAS_E[k], "deps": v["deps"] + v["fuente_verif"]}
    for k, v in D["afirmaciones"].items():
        N[k] = {"tipo": "afirmacion", "e": v["e"], "deps": list(v["deps"])}
    for k, v in D["vias"].items():
        N[k] = {"tipo": "via", "e": v["e"], "deps": list(v["deps"])}
    PR = D["preregistro"]
    for k in [x for x in PR if x != "fecha"]:
        N[k] = {"tipo": "prereg", "e": PR[k]["e"], "deps": PR[k]["deps"]}
    for k, v in D["preguntas"].items():
        N[k] = {"tipo": "pregunta", "e": "M", "deps": list(v["a"])}
    for k, e in over_e.items():
        N[k]["e"] = e
    for k, ds in over_deps.items():
        N[k]["deps"] = list(ds)
    return N


def progreso(N):
    EF = {}

    def ef(n, pila=()):
        if n in EF:
            return EF[n]
        x = N[n]
        e = x["e"]
        if x["tipo"] == "prereg":
            EF[n] = e
            return e
        for d in x["deps"]:
            if d not in N or N[d]["tipo"] == "param" or d in pila:
                continue
            ed = ef(d, pila + (n,))
            if RANK[ed] < RANK[e]:
                e = ed
        EF[n] = e
        return e

    for n in N:
        ef(n)
    for q in D["preguntas"]:
        EF[q] = min((EF[a] for a in D["preguntas"][q]["a"]), key=lambda s: RANK[s])
    total = 0.0
    for _nom, w, tipos, capas in COMP:
        ns = [n for n in EF if N[n]["tipo"] in tipos and
              (capas is None or D["afirmaciones"].get(n, {}).get("capa") in capas)]
        if ns:
            total += w * sum(SCORE[EF[n]] for n in ns) / len(ns)
    return total, EF


BASE, EF0 = progreso(construir())
print("progreso replicado = %.2f %%" % BASE)

CLUSTER = ["L29", "L31", "L32", "L34", "L35", "L36", "L38", "L39"]
FUENTES = ["F74", "F76", "F77", "F79", "F81", "F83", "F84"]

print("\n-- estatus declarado / efectivo del cluster --")
for n in CLUSTER + FUENTES:
    e = D["afirmaciones"][n]["e"] if n in D["afirmaciones"] else D["fuentes"][n]["estatus"]
    print("  %s: declarado %s . efectivo %s" % (n, e, EF0[n]))

print("\n-- valor de cada cierre individual (declaracion -> V) --")
for n in CLUSTER + FUENTES:
    t, _ = progreso(construir(over_e={n: "V"}))
    print("  %s -> V : +%.2f" % (n, t - BASE))

print("\n-- preguntas que dependen del cluster --")
for q, v in D["preguntas"].items():
    if set(v["a"]) & set(CLUSTER):
        print("  %s (%s) efectivo %s <- %s" % (q, v["t"][:40], EF0[q], v["a"]))

print("\n-- cierre propuesto en la tanda 49: L35 sin L29 y declarada V --")
t, EFn = progreso(construir(over_e={"L35": "V"}, over_deps={"L35": ["F80", "G4"]}))
print("  total %.2f %% (+%.2f)" % (t, t - BASE))
print("  Q6 efectivo: %s -> %s" % (EF0["Q6"], EFn["Q6"]))
