#!/usr/bin/env python3
"""AUDITORIA DE ENLACES A X2 (tanda 48) — patrón 4: dependencia innecesaria.

PROBLEMA. En `red/dsny.yaml` el comentario de la capa de afirmaciones dice:
«deps = nodos de los que dependen», y el motor propaga con la regla «un nodo nunca vale
más que su dependencia más débil». Es decir: `deps` es APOYO PROBATORIO, y cada arista
es también una PENALIZACION.

Las tandas 27-30 añadieron ocho nodos de «campos vecinos y lejanos» escritos EXPLICITAMENTE
para atacar X2 desde fuera, y a todos se les puso `X2` en `deps` como marca temática.
X2 está [A] (es la frontera empírica abierta del programa), así que esa marca temática
arrastra a [A] ocho nodos cuya evidencia está entera en otras fuentes ya verificadas.
Es el mismo tipo de fallo que la tanda 41 llamó «error de cableado».

TEST (contrafáctico, uno por nodo). X2 pregunta: ¿existe una química con función Y escala
a la vez? Es un SI/NO empírico todavía sin medir. Para cada nodo:

    ¿cambiaría el contenido del nodo si X2 saliera SI?  ¿y si saliera NO?

    - Si el nodo dice lo mismo con las dos respuestas  =>  X2 no es apoyo: la arista sale.
    - Si el nodo necesita una de las dos respuestas    =>  la arista se queda.

Y la dirección importa: un nodo que APORTA EVIDENCIA SOBRE X2 no puede a la vez DERIVAR
de X2. La relación se conserva donde debe estar, en el texto del nodo, que nombra X2.

LIMITE AUTOIMPUESTO, y es lo que hace la auditoría comprobable: **ningún nodo sube por
encima de su estatus DECLARADO**. Quitar la arista no cierra nada nuevo; sólo deja de
rebajar declaraciones que ya existían. Este script lo verifica al final y falla si no.
"""
import copy, yaml
from pathlib import Path

YAML = Path(__file__).resolve().parent.parent / "red" / "dsny.yaml"
D0 = yaml.safe_load(open(YAML))

# nodo -> (¿sale la arista?, evidencia real del nodo, por qué X2 no es apoyo)
TEST = {
 "L22": (True,  "F37b + F46 + F71",
   "V3 = VM3 sin bloqueadores de hielo es una IDENTIDAD DE COMPOSICION, confirmada al decimal "
   "y por el suplementario de los propios autores (F71). Sigue siendo cierta con X2 = SI y con "
   "X2 = NO. Lo que el texto dice de X2 ('no enfrenta dos linajes, sino uno a dos "
   "concentraciones') se DEDUCE de esta identidad: la evidencia va de L22 a X2, no al revés."),
 "L23": (True,  "F72 + F37b + G4b",
   "«el daño lo causa la exposición química, no el cambio de fase» son dos pares de números "
   "medidos en el mismo tejido (respiración 135.1 vs 131.4; reserva 48.6 vs 50.6, F72) más el "
   "clásico de 50 vs 53 % de F37b. No depende de si existe o no una química con función y escala."),
 "L25": (True,  "F72 + L22 + L20",
   "«a 9.28 M cargada a 10 °C la respiración cae a la mitad» es una medida de F72; que la "
   "temperatura de carga sea la variable decisiva lo da L20 [V]. Ninguna de las dos cosas cambia "
   "con la respuesta a X2."),
 "L29": (True,  "F74",
   "Las CAHS del tardígrado forman vidrio o gel a ~0.6 mM: dato de F74. El nodo ATACA el supuesto "
   "CCR<->molaridad que hay DEBAJO de X2; no se apoya en X2."),
 "L30": (True,  "F75 + F59 + G3",
   "«existe un marco computacional de diseño de excipientes» es un hecho sobre la literatura de "
   "liofilización (F75) más el papel de Tg en el agrietamiento (F59). Verdadero con X2 = SI y con "
   "X2 = NO; de hecho es una PROPUESTA DE VIA para resolver X2."),
 "L31": (True,  "F76",
   "La CCR del agua pura, 6.4e6 K/s, es una medición ajena al marco (F76). El tercer punto de la "
   "curva CCR<->concentración existe con independencia de la respuesta a X2."),
 "L32": (True,  "F77 + G3 + F75",
   "Que la metalurgia de vidrios masivos defina Trg y gamma y derive de ellos el espesor crítico "
   "es un hecho de F77. No necesita saber si hay una química con función y escala."),
 "L35": (True,  "F80 + L29 + G4",
   "«los NADES protegen pero cristalizan a 30 °C/min» es la calorimetría de F80 leída en la tanda "
   "46. Es un resultado NEGATIVO sobre un candidato a X2: aporta a X2, no deriva de X2."),
}
# Nodos con X2 en deps que NO se tocan:
NO_TOCAR = {"Q11": "es una PREGUNTA; X2 figura entre sus respuestas, que es su papel correcto."}

RANK = {"A": 0, "P": 1, "V": 2, "M": 2, "ROTO": -1}
SCORE = {"M": 1.0, "V": 1.0, "P": 0.6, "A": 0.2, "ROTO": 0.0}
COMP = [("Ontología", 15, {"afirmacion"}, {"ontologia"}), ("Magnitudes y umbrales", 35, {"afirmacion"}, {"magnitud", "frontera"}),
        ("Leyes y cotas", 15, {"afirmacion", "cota"}, {"ley", None}), ("Vías", 10, {"via"}, None),
        ("Preregistro falsable", 15, {"prereg"}, None), ("Preguntas respondidas", 10, {"pregunta"}, None)]

def evaluar(D):
    """Réplica de la propagación del motor. Las cotas son todas M en el estado actual del marco
    (el motor lo imprime en cada ejecución); aquí se leen como M para no reimplementar la física."""
    N = {}
    for k, v in D["fuentes"].items(): N[k] = {"t": "fuente", "e": v["estatus"], "d": []}
    for k, v in D["parametros"].items(): N[k] = {"t": "param", "e": v["e"], "d": [v["f"]] if v["f"] else []}
    for k, v in D["cotas"].items(): N[k] = {"t": "cota", "e": "M", "d": v["deps"] + v["fuente_verif"]}
    for k, v in D["afirmaciones"].items(): N[k] = {"t": "afirmacion", "e": v["e"], "d": v["deps"], "capa": v["capa"]}
    for k, v in D["vias"].items(): N[k] = {"t": "via", "e": v["e"], "d": v["deps"]}
    PR = D["preregistro"]
    for k in [x for x in PR if x != "fecha"]: N[k] = {"t": "prereg", "e": PR[k]["e"], "d": PR[k]["deps"]}
    for k, v in D["preguntas"].items(): N[k] = {"t": "pregunta", "e": "M", "d": v["a"]}
    EF = {}
    def ef(n, pila=()):
        if n in EF: return EF[n]
        x = N[n]; e = x["e"]
        if x["t"] == "prereg": EF[n] = e; return e
        for d in x["d"]:
            if d not in N or N[d]["t"] == "param" or d in pila: continue
            ed = ef(d, pila + (n,))
            if RANK[ed] < RANK[e]: e = ed
        EF[n] = e; return e
    for n in N: ef(n)
    for q in D["preguntas"]:
        EF[q] = min((EF[a] for a in D["preguntas"][q]["a"]), key=lambda s: RANK[s])
    tot = 0.0
    for _, w, tp, cp in COMP:
        ns = [n for n in EF if N[n]["t"] in tp and (cp is None or N[n].get("capa") in cp)]
        if ns: tot += w * sum(SCORE[EF[n]] for n in ns) / len(ns)
    return tot, EF, N

def con_aristas(D, poner):
    """Devuelve una copia del YAML con X2 presente (poner=True) o ausente en los 8 nodos."""
    D = copy.deepcopy(D)
    for n in TEST:
        deps = D["afirmaciones"][n]["deps"]
        if poner and "X2" not in deps: deps.append("X2")
        if not poner and "X2" in deps: deps.remove("X2")
    return D

print(__doc__)
print("=" * 96)
for n, (sale, evid, por) in TEST.items():
    print(f"\n{n}  arista X2 -> {'SALE' if sale else 'SE QUEDA'}   evidencia real: {evid}")
    for ln in por.split(". "):
        if ln.strip(): print("      " + ln.strip().rstrip(".") + ".")
for n, por in NO_TOCAR.items():
    print(f"\n{n}  arista X2 -> SE QUEDA   {por}")

t_con, EF_con, N_ = evaluar(con_aristas(D0, True))
t_sin, EF_sin, N = evaluar(con_aristas(D0, False))
print("\n" + "=" * 96)
print(f"{'nodo':6} {'declarado':10} {'efectivo CON X2':16} {'efectivo SIN X2':16} ¿supera lo declarado?")
mal = []
for n in list(TEST) + ["L26", "X2"]:
    decl = N[n]["e"]
    sube = RANK[EF_sin[n]] > RANK[decl]
    if sube: mal.append(n)
    print(f"{n:6} {decl:10} {EF_con[n]:16} {EF_sin[n]:16} {'SI (PROHIBIDO)' if sube else 'no'}")
print()
print(f"Progreso CON las aristas temáticas: {t_con:.2f} %")
print(f"Progreso SIN las aristas temáticas: {t_sin:.2f} %   (+{t_sin - t_con:.2f})")
print(f"X2 sigue en [{EF_sin['X2']}]: la tensión del programa (R1) se conserva intacta.")
assert not mal, f"ningún nodo debía superar su declaración, y lo hacen: {mal}"
print("\nCOMPROBADO: ningún nodo supera su estatus declarado. La auditoría no cierra nada nuevo;")
print("sólo deja de rebajar declaraciones que el marco ya tenía escritas.")
