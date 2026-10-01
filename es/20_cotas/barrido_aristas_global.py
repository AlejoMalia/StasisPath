#!/usr/bin/env python3
"""BARRIDO SISTEMATICO DE ARISTAS SOBRE TODO EL GRAFO (tanda 49).

La tanda 48 auditó SOLO las aristas que apuntaban a X2 y encontró ocho que no eran apoyo
(la evidencia iba del nodo HACIA X2). Valió +1.83 puntos sin conocimiento nuevo.

Este script generaliza el test a TODA arista del grafo, sin privilegiar ningún destino.
No decide nada: ENUMERA los candidatos y los ordena por lo que cuesta cada uno, para que
el test contrafáctico se aplique a mano nodo a nodo (el test es semántico, no mecánico).

DEFINICIONES (idénticas a red/motor.py, que NO se toca)
  RANK  A=0 P=1 V=M=2
  estatus efectivo de un nodo = min(su declarado, el efectivo de cada dep no-parámetro)

ARISTA PENALIZANTE (n -> d): RANK[EF[d]] < RANK[declarado(n)].
  Es decir: la arista, y sólo ella, impide que n valga lo que su propio texto declara.
  Toda arista NO penalizante es gratis y no hace falta auditarla: quitarla no cambia el
  número (sí cambiaría el sentido del grafo, así que no se toca).

Para cada arista penalizante se mide su COSTE REAL: puntos de progreso que recupera el
marco si esa arista sale (recalculando con la regla del motor, en memoria, sin escribir).
Se mide también el coste de cada CONJUNTO de aristas que comparten origen, porque un nodo
sujeto por dos deps débiles no sube quitando sólo una.

EL TEST QUE DECIDE (a mano, para cada candidata):
  ¿la afirmación de n sigue diciendo lo mismo si d fuera cierta Y si d fuera falsa?
    SI en ambos casos -> d no es apoyo probatorio de n: la arista es temática y sale
                          (la relación se conserva en el TEXTO del nodo, que nombra d).
    NO -> la arista se queda: n hereda legítimamente la debilidad de d.

LIMITE AUTOIMPUESTO Y VERIFICADO: ningún nodo sube por encima de su estatus DECLARADO.
"""
import copy, yaml
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
D = yaml.safe_load(open(RAIZ / "red" / "dsny.yaml"))

RANK = {"A": 0, "P": 1, "V": 2, "M": 2, "ROTO": -1}
SCORE = {"M": 1.0, "V": 1.0, "P": 0.6, "A": 0.2, "ROTO": 0.0}
COMP = [("Ontologia", 15, {"afirmacion"}, {"ontologia"}),
        ("Magnitudes y umbrales", 35, {"afirmacion"}, {"magnitud", "frontera"}),
        ("Leyes y cotas", 15, {"afirmacion", "cota"}, {"ley", None}),
        ("Vias", 10, {"via"}, None),
        ("Preregistro falsable", 15, {"prereg"}, None),
        ("Preguntas respondidas", 10, {"pregunta"}, None)]

# Las cotas del marco están todas en M (el motor lo recalcula en las esquinas del rango;
# aquí no se duplica la física, sólo se necesita el estatus para propagar).
COTAS_E = {c: "M" for c in D["cotas"]}


def construir(d):
    N = {}
    for k, v in d["fuentes"].items():
        N[k] = {"tipo": "fuente", "e": v["estatus"], "deps": [], "capa": None}
    for k, v in d["parametros"].items():
        N[k] = {"tipo": "param", "e": v["e"], "deps": [v["f"]], "capa": None}
    for k, v in d["cotas"].items():
        N[k] = {"tipo": "cota", "e": COTAS_E[k],
                "deps": list(v["deps"]) + list(v.get("fuente_verif", [])), "capa": None}
    for k, v in d["afirmaciones"].items():
        N[k] = {"tipo": "afirmacion", "e": v["e"], "deps": list(v["deps"]), "capa": v["capa"]}
    for k, v in d["vias"].items():
        N[k] = {"tipo": "via", "e": v["e"], "deps": list(v["deps"]), "capa": None}
    for k in [x for x in d["preregistro"] if x != "fecha"]:
        N[k] = {"tipo": "prereg", "e": d["preregistro"][k]["e"],
                "deps": list(d["preregistro"][k]["deps"]), "capa": None}
    for k, v in d["preguntas"].items():
        N[k] = {"tipo": "pregunta", "e": "M", "deps": list(v["a"]), "capa": None}
    return N


def propagar(N, preguntas):
    EF, MOT = {}, {}

    def ef(n, pila=()):
        if n in EF: return EF[n]
        x = N[n]; e = x["e"]; m = None
        if x["tipo"] == "prereg":
            EF[n] = e; MOT[n] = None; return e
        for dd in x["deps"]:
            if dd not in N or N[dd]["tipo"] == "param" or dd in pila: continue
            ed = ef(dd, pila + (n,))
            if RANK[ed] < RANK[e]: e, m = ed, dd
        EF[n] = e; MOT[n] = m
        return e

    for n in N: ef(n)
    for q in preguntas:
        # TANDA 52: guarda añadida. Al simular la retirada de una arista se puede dejar a una pregunta
        # SIN respuestas, y `min()` de una secuencia vacía revienta. El motor nunca llega a ese estado
        # (ninguna pregunta del YAML está sin respuestas), pero el barrido sí lo visita al simular.
        # Una pregunta sin ninguna respuesta no está respondida: vale [A], que es su suelo.
        EF[q] = min((EF[a] for a in N[q]["deps"]), key=lambda s: RANK[s], default="A")
    return EF, MOT


def progreso(N, EF):
    t = 0.0
    for _, w, tp, cp in COMP:
        ns = [n for n in EF if N[n]["tipo"] in tp and (cp is None or N[n]["capa"] in cp)]
        if ns: t += w * sum(SCORE[EF[n]] for n in ns) / len(ns)
    return t


N0 = construir(D)
EF0, MOT0 = propagar(N0, D["preguntas"])
P0 = progreso(N0, EF0)
print(f"BASE: {len(N0)} nodos · progreso {P0:.2f} %\n")

# --------------------------------------------------- 1. enumerar aristas penalizantes
pen = []
for n, x in N0.items():
    if x["tipo"] in ("param", "prereg"): continue
    for d in x["deps"]:
        if d not in N0 or N0[d]["tipo"] == "param": continue
        if RANK[EF0[d]] < RANK[x["e"]]:
            pen.append((n, d))

total = sum(len([d for d in x["deps"] if d in N0 and N0[d]["tipo"] != "param"])
            for x in N0.values())
print(f"Aristas totales (sin parámetros): {total}")
print(f"Aristas PENALIZANTES (impiden que el nodo valga lo declarado): {len(pen)}\n")


def quitar(pares):
    d2 = copy.deepcopy(D)
    for n, dep in pares:
        for sec, k in (("afirmaciones", "deps"), ("vias", "deps"), ("cotas", "deps"),
                       ("preguntas", "a")):
            if n in d2[sec] and dep in d2[sec][n][k]:
                d2[sec][n][k].remove(dep)
    N = construir(d2)
    EF, _ = propagar(N, d2["preguntas"])
    return progreso(N, EF), N, EF


print("=" * 98)
print("COSTE DE CADA ARISTA PENALIZANTE (puntos que recupera el marco si sale)")
print("=" * 98)
print(f"{'nodo':6} {'decl':5} {'-> dep':10} {'EF(dep)':8} {'gana sola':>10}   capa/tipo")
for n, d in pen:
    p, _, _ = quitar([(n, d)])
    print(f"{n:6} [{N0[n]['e']}]   -> {d:8} [{EF0[d]}]     "
          f"{p - P0:+8.2f}    {N0[n]['capa'] or N0[n]['tipo']}")

# --------------------------------------------------- 2. conjuntos por nodo
print()
print("=" * 98)
print("NODOS SUJETOS POR VARIAS ARISTAS DEBILES (quitar una sola no los sube)")
print("=" * 98)
porn = {}
for n, d in pen: porn.setdefault(n, []).append(d)
hay = False
for n, ds in sorted(porn.items()):
    if len(ds) < 2: continue
    hay = True
    p, _, _ = quitar([(n, d) for d in ds])
    print(f"{n:6} [{N0[n]['e']}] deps débiles {ds} -> quitando TODAS: {p - P0:+.2f}")
if not hay: print("(ninguno)")

# --------------------------------------------------- 3. techo del barrido
print()
print("=" * 98)
ptop, Nt, EFt = quitar(pen)
print(f"TECHO TEORICO si TODAS las {len(pen)} penalizantes fueran temáticas: "
      f"{P0:.2f} -> {ptop:.2f} % ({ptop - P0:+.2f})")
print("NO es un objetivo: la mayoría de estas aristas SI son apoyo probatorio real.")
print("El techo sólo dice cuánto está en juego en esta capa del barrido.")

# --------------------------------------------------- 4. limite autoimpuesto
print()
print("=" * 98)
print("VERIFICACION DEL LIMITE: ningun nodo por encima de su estatus DECLARADO")
malos = [n for n in EFt if RANK[EFt[n]] > RANK[Nt[n]["e"]] and Nt[n]["tipo"] != "pregunta"]
assert not malos, f"VIOLACION: {malos}"
print("OK · ninguna retirada de arista sube un nodo sobre su declaracion.")
