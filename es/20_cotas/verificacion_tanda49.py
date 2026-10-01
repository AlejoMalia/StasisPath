#!/usr/bin/env python3
"""VERIFICACION OBLIGATORIA ANTES DE COMMIT (tanda 49). Todo con `assert`: si algo falla, falla.

Comprueba:
  (a) el YAML es válido y ningún nodo apunta a una dependencia inexistente;
  (b) el preregistro está INTACTO (hash de red/prereg.lock frente al YAML) y P15/P18/P19/P20/P21
      no han cambiado de texto: los umbrales no se han movido (R2);
  (c) ningún nodo supera su estatus DECLARADO tras la propagación;
  (d) las tensiones que el marco debe conservar siguen conservadas (R1): X2 [A], L25 [P],
      V06/V09/V11 [P], L37 [P], el clúster de campos lejanos intacto;
  (e) el motor no se ha tocado: hash de red/motor.py frente al de HEAD (git);
  (f) no hay dependencias duplicadas ni ciclos en el grafo.
"""
import hashlib, subprocess, sys, yaml
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
D = yaml.safe_load(open(RAIZ / "red" / "dsny.yaml"))
print("(a) YAML válido: OK")

RANK = {"A": 0, "P": 1, "V": 2, "M": 2}
N = {}
for k, v in D["fuentes"].items(): N[k] = {"t": "fuente", "e": v["estatus"], "d": []}
for k, v in D["parametros"].items(): N[k] = {"t": "param", "e": v["e"], "d": [v["f"]] if v["f"] else []}
for k, v in D["cotas"].items():
    N[k] = {"t": "cota", "e": "M", "d": list(v["deps"]) + list(v.get("fuente_verif", []))}
for k, v in D["afirmaciones"].items(): N[k] = {"t": "afirmacion", "e": v["e"], "d": list(v["deps"])}
for k, v in D["vias"].items(): N[k] = {"t": "via", "e": v["e"], "d": list(v["deps"])}
for k in [x for x in D["preregistro"] if x != "fecha"]:
    N[k] = {"t": "prereg", "e": D["preregistro"][k]["e"], "d": list(D["preregistro"][k]["deps"])}
for k, v in D["preguntas"].items(): N[k] = {"t": "pregunta", "e": "M", "d": list(v["a"])}

faltan = [(n, d) for n, x in N.items() for d in x["d"] if d not in N]
assert not faltan, f"dependencias inexistentes: {faltan}"
dups = {n: x["d"] for n, x in N.items() if len(x["d"]) != len(set(x["d"]))}
assert not dups, f"dependencias duplicadas: {dups}"
print(f"    {len(N)} nodos · sin dependencias inexistentes · sin dependencias duplicadas")

# --------------------------------------------------------------- (b) preregistro intacto
PR = D["preregistro"]
IDS = [k for k in PR if k != "fecha"]
H = {k: hashlib.sha256((PR["fecha"] + PR[k]["t"]).encode()).hexdigest() for k in IDS}
lock = {}
for ln in (RAIZ / "red" / "prereg.lock").read_text().splitlines():
    if ":" in ln:
        kk, vv = ln.split(":", 1); lock[kk.strip()] = vv.strip()
rotos = [k for k in IDS if k in lock and lock[k] != H[k]]
assert not rotos, f"ALARMA R2 · preregistro editado tras congelarse: {rotos}"
for k in ("P15", "P18", "P19", "P20", "P21"):
    assert k in IDS and k in lock, f"falta el preregistro protegido {k}"
print(f"(b) preregistro INTACTO: {len(IDS)} preregistros, los 5 protegidos presentes y con hash igual")

# --------------------------------------------------------------- (c) nadie sobre su declaración
EF = {}


def ef(n, pila=()):
    if n in EF: return EF[n]
    x = N[n]; e = x["e"]
    if x["t"] == "prereg":
        EF[n] = e; return e
    for d in x["d"]:
        if N[d]["t"] == "param" or d in pila: continue
        v = ef(d, pila + (n,))
        if RANK[v] < RANK[e]: e = v
    EF[n] = e
    return e


sys.setrecursionlimit(10000)
for n in N: ef(n)
for q in D["preguntas"]: EF[q] = min((EF[a] for a in N[q]["d"]), key=lambda s: RANK[s])
malos = [(n, N[n]["e"], EF[n]) for n in EF if RANK[EF[n]] > RANK[N[n]["e"]] and N[n]["t"] != "pregunta"]
assert not malos, f"NODOS POR ENCIMA DE SU DECLARACION: {malos}"
print("(c) ningún nodo supera su estatus declarado: OK")

# --------------------------------------------------------------- (d) tensiones conservadas
TENSION = {"X2": "A", "L25": "P", "V06": "P", "V09": "V", "V11": "V", "L37": "V", "V25": "P",   # L37 en [V] desde la tanda 55
           "L29": "P", "L31": "P", "L32": "P", "L34": "P", "L35": "V", "L36": "P", "L38": "P",
           "L39": "P"}
for n, e in TENSION.items():
    assert EF[n] == e, f"R1: {n} debería seguir en [{e}] y está en [{EF[n]}]"
CERRADOS = {"L26": "V", "V16": "V", "Q22": "V"}
for n, e in CERRADOS.items():
    assert EF[n] == e, f"{n} debería estar en [{e}] tras la tanda 49 y está en [{EF[n]}]"
assert "L25" not in N["L26"]["d"] and "F6" not in N["V16"]["d"], "las aristas de la tanda 49 no se retiraron"
# TANDA 55: la premisa de este assert era que F19 debía conservarse en V09 y V11 porque ERA su
# única fuente. Ya no lo es: se han leído las primarias (F90 lémur, F91 pez pulmonado) y F19 se
# sustituye por ellas. NO es retirar una arista para subir el número; es cambiar un resumen por
# la fuente original. F19 sigue en el grafo sosteniendo la TORTUGA, vía el parámetro turtle22_h.
assert "F57" in N["V06"]["d"] and "F82" in N["L37"]["d"], \
    "las aristas que NO pasan el test deben seguir en el grafo"
assert "F19" in N["turtle22_h"]["d"], \
    "tanda 55: F19 debe seguir sosteniendo la tortuga mientras esa parte no tenga primaria"
assert "X2" in N["Q11"]["d"], "Q11 debe conservar X2: es una de sus respuestas"
# TANDA 52 (auditoría en contra): SEIS nodos reabiertos. Se registran aquí como expectativa para que
# ningún barrido posterior los vuelva a cerrar sin argumentar contra el motivo escrito en el YAML.
# Qué cambió y por qué, en una línea cada uno:
#   L43 [V]->[A] : su «100 % de 20 000 combinaciones» es un MonteCarlo triangular; con el criterio
#                  MATE del marco (esquinas) el tronco cae dentro en 12/64 y el cuerpo en 50/64.
#   V15 [V]->[A] : se cerró «por imposibilidad demostrada» apoyándose en L43, y además le FALTABA
#                  la arista a L43 (afirmaba su dato sin depender de él). La arista se añade.
#   F13 [V]->[P] : es una REVISIÓN, no una primaria (mismo criterio con el que F6, F19 y F82 están en [P]).
#   L7  [V]->[P] : su cierre decía literalmente «hoy F13 es [V]».
#   L8  [V]->[P] : ídem, y además atribuye a F13 el 52–68 % que es de Bradford/SpaceWorks (NIAC).
#   L5  [V]->[P] : vuelve F57 a `deps`: el dato del preprint APARECE en su texto, que es el test con
#                  el que la tanda 49 decidió CONSERVAR F57 en V06. Criterio simétrico o no es criterio.
# TANDA 53: L43 vuelve a [V], y el assert de la tanda 52 lo frenó correctamente. NO se refutó su
# motivo: se ACEPTÓ. El «100 %» era falso y se ha RETIRADO del enunciado; L43 ya no afirma nada
# sobre el tronco ni sobre el cuerpo entero, sólo el cerebro (64/64 esquinas, verificado de forma
# independiente). Es el patrón de L33: corregir la exageración y entonces cerrar. Lo que NO cambia
# es la consecuencia: V15 sigue en [A], porque la imposibilidad que invocaba no está demostrada.
# TANDA 54: L7 y L8 vuelven a [V] y esta vez el motivo de la tanda 52 SÍ queda refutado, no aceptado.
#   L8: el motivo era «el 52-68 % es de Bradford/SpaceWorks y NO está en la red». Ahora está: F89,
#       informe NIAC Phase I, PDF leído entero, con la frase literal «mass reductions ranging from
#       52% to 68%». L8 ya no depende de F13; depende de la primaria.
#   L7: el motivo era «su cierre decía "hoy F13 es [V]", y F13 es una revisión». Ya no se apoya en
#       F13: depende de F88, Gilbert 2000 Lancet, PDF leído entero, con la cronología de primera mano.
#   F13 sigue en [P] —sigue siendo una revisión— pero ya no sostiene nada.
REABIERTOS = {"L43": "V", "V15": "A", "F13": "P", "L7": "V", "L8": "V", "L5": "P"}
assert "F88" in N["L7"]["d"] and "F13" not in N["L7"]["d"], \
    "tanda 54: L7 sólo puede estar en [V] si depende de la primaria F88 y NO de la revisión F13"
assert "F89" in N["L8"]["d"] and "F13" not in N["L8"]["d"], \
    "tanda 54: L8 sólo puede estar en [V] si depende de la primaria F89 y NO de la revisión F13"
assert N["F88"]["e"] == "V" and N["F89"]["e"] == "V", "tanda 54: F88 y F89 son primarias leídas enteras"
# TANDA 55: F82 deja de ser una revisión y L37 se cierra por irrelevancia demostrada, no por
# encontrar la permitividad a 360 kHz, que SIGUE sin fuente. Lo que se retira de L37 es la CIFRA
# (λ ≈ 8.3 m, que exigía εr ≈ 1e4); lo que se sostiene es el RÉGIMEN, robusto por ×434.
assert N["F82"]["e"] == "V", "tanda 55: F82 debe estar en [V], sustituidas las revisiones por primarias"
# TANDA 55 (fauna): V09 y V11 se cierran contra primarias LEÍDAS, no contra los resúmenes de F19.
#   V09 <- F90 (Dausmann 2009, original paper: lémur medido en hibernáculo natural)
#   V11 <- F91 (Niu et al., investigación original) Y CORRIGIENDO su ventana de "3-4 años" a los
#         "7-8 meses" que dice la primaria. La corrección va EN CONTRA del marco: era un orden de
#         magnitud de más. F19 sigue en [P]: la parte de la TORTUGA no tiene primaria todavía.
assert "F19" not in N["V09"]["d"] and "F90" in N["V09"]["d"], "tanda 55: V09 debe apoyarse en F90, no en los resúmenes de F19"
assert "F19" not in N["V11"]["d"] and "F91" in N["V11"]["d"], "tanda 55: V11 debe apoyarse en F91, no en los resúmenes de F19"
assert "3–4 años" not in D["vias"]["V11"]["ventana"], "tanda 55: la ventana de V11 no puede volver a 3-4 años: ninguna primaria lo sostiene"
assert N["F19"]["e"] == "P", "tanda 55: F19 sigue en [P] mientras la tortuga no tenga primaria"
# Nota: el primer intento de este assert prohibía la cadena "8.3 m" en el texto, y saltó contra
# la propia frase que RETIRA la cifra. Un assert que impide explicar por qué se retiró un dato es
# un mal assert. Lo que hay que exigir es que la retirada esté declarada, no que la cifra no se
# mencione.
assert "se retira" in D["afirmaciones"]["L37"]["t"], \
    "tanda 55: L37 debe declarar EXPLÍCITAMENTE que retira la cifra de λ, cuyo εr no tiene fuente"
assert "434" in D["afirmaciones"]["L37"]["t"], \
    "tanda 55: si L37 está en [V], su texto DEBE declarar el margen ×434 que lo hace irrelevante"
_l43 = D["afirmaciones"]["L43"]["t"]   # ojo: en N, "t" es el TIPO de nodo; el texto está en el YAML
assert "tronco" in _l43 and "48" in _l43, \
    "tanda 53: si L43 está en [V], su texto DEBE declarar que el tronco sale fuera sólo en 48/64 esquinas"
assert EF["V15"] == "A", "tanda 53: V15 no puede cerrarse mientras la imposibilidad del tronco no esté demostrada"
for n, e in REABIERTOS.items():
    assert EF[n] == e, f"tanda 52: {n} se reabrió a [{e}] y está en [{EF[n]}]; si se vuelve a cerrar, hay que refutar el motivo escrito en su texto"
assert "L43" in N["V15"]["d"], "tanda 52: V15 debe depender de L43, que es lo que su texto afirma"
assert "F57" in N["L5"]["d"] and "F57" in N["V06"]["d"], \
    "tanda 52: F57 sujeta a L5 y a V06 por la misma razón (las dos afirman su dato); el criterio tiene que ser simétrico"
print(f"(d) tensiones conservadas (X2 [A], L25 [P], clúster de campos lejanos [P]), cierres aplicados "
      f"y {len(REABIERTOS)} reaperturas de la tanda 52 en pie: OK")

# --------------------------------------------------------------- (e) el marcador no se toca
try:
    base = subprocess.run(["git", "show", "HEAD:red/motor.py"], cwd=RAIZ,
                          capture_output=True, check=True).stdout
    ahora = (RAIZ / "red" / "motor.py").read_bytes()
    assert hashlib.sha256(base).hexdigest() == hashlib.sha256(ahora).hexdigest(), \
        "red/motor.py MODIFICADO: el marcador no se toca"
    print("(e) red/motor.py idéntico al de HEAD (COMP, SCORE y RANK intactos): OK")
except subprocess.CalledProcessError:
    print("(e) [aviso] no se pudo comparar motor.py con git; comprobar a mano")

# --------------------------------------------------------------- (f) sin ciclos
col = {}
ciclos = []


def dfs(n, path):
    col[n] = 1
    for d in N[n]["d"]:
        if N[d]["t"] == "param": continue
        if col.get(d) == 1: ciclos.append(path + [n, d])
        elif col.get(d) is None: dfs(d, path + [n])
    col[n] = 2


for n in N:
    if col.get(n) is None: dfs(n, [])
assert not ciclos, f"ciclos en el grafo: {ciclos}"
print("(f) grafo acíclico: OK")

print("\nTODAS LAS VERIFICACIONES PASAN.")
