# -*- coding: utf-8 -*-
"""TANDA 49 - AUDITORIA DEL CLUSTER DE CAMPOS LEJANOS. Falla si algo se infla.

Igual que `20_cotas/auditoria_enlaces_X2.py` hizo en la tanda 48, este script es la
verificacion obligatoria antes del commit. Comprueba, con assert:

  1. El YAML es valido y el preregistro esta intacto (hashes de red/prereg.lock).
  2. NINGUN nodo de la red supera su estatus DECLARADO (limite autoimpuesto).
  3. El clúster de campos lejanos NO se ha inflado: las 7 fuentes lejanas siguen [P] y
     las 7 leyes que no se cerraron siguen [P]. Solo L35 sube, y solo a [V].
  4. Las aristas retiradas en la tanda 49 estan efectivamente fuera de `deps` y las que
     siguen siendo apoyo siguen dentro.
  5. Ninguna de las fuentes lejanas es un impostor: identificador unico y URL unica (R4).

Uso: python3 20_cotas/auditoria_campos_lejanos.py
"""
import hashlib
import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
D = yaml.safe_load(open(ROOT / "red" / "dsny.yaml"))
print("1) YAML valido: %d fuentes, %d afirmaciones, %d vias, %d preguntas"
      % (len(D["fuentes"]), len(D["afirmaciones"]), len(D["vias"]), len(D["preguntas"])))

# ------------------------------------------------------------------ 1) preregistro
LOCK = ROOT / "red" / "prereg.lock"
guardado = {}
for ln in LOCK.read_text().splitlines():
    if ":" in ln:
        kk, vv = ln.split(":", 1)
        guardado[kk.strip()] = vv.strip()
PR = D["preregistro"]
# Mismo calculo que red/motor.py (linea 239): sha256(fecha + texto del preregistro).
HASHES = {k: hashlib.sha256((PR["fecha"] + PR[k]["t"]).encode()).hexdigest()
          for k in PR if k != "fecha"}
rotos = [k for k in HASHES if k in guardado and guardado[k] != HASHES[k]]
perdidos = [k for k in guardado if k not in HASHES]
assert not rotos, "ALARMA R2: preregistro editado tras congelarse: %s" % rotos
assert not perdidos, "ALARMA R2: preregistro PERDIDO del YAML: %s" % perdidos
print("   preregistro intacto: %s (hash identico al de prereg.lock)"
      % ", ".join(sorted(HASHES)))

# ------------------------------------------------------------------ 2) propagacion
RANK = {"A": 0, "P": 1, "V": 2, "M": 2, "ROTO": -1}
N = {}
for k, v in D["fuentes"].items():
    N[k] = {"tipo": "fuente", "e": v["estatus"], "deps": []}
for k, v in D["parametros"].items():
    N[k] = {"tipo": "param", "e": v["e"], "deps": [v["f"]] if v.get("f") else []}
for k, v in D["cotas"].items():
    N[k] = {"tipo": "cota", "e": "M", "deps": v["deps"] + v["fuente_verif"]}
for k, v in D["afirmaciones"].items():
    N[k] = {"tipo": "afirmacion", "e": v["e"], "deps": list(v["deps"])}
for k, v in D["vias"].items():
    N[k] = {"tipo": "via", "e": v["e"], "deps": list(v["deps"])}
for k in [x for x in PR if x != "fecha"]:
    N[k] = {"tipo": "prereg", "e": PR[k]["e"], "deps": PR[k]["deps"]}
for k, v in D["preguntas"].items():
    N[k] = {"tipo": "pregunta", "e": "M", "deps": list(v["a"])}

faltan = [(n, d) for n, x in N.items() for d in x["deps"] if d not in N]
assert not faltan, "DEPENDENCIAS INEXISTENTES: %s" % faltan
print("   todas las dependencias existen (%d nodos)" % len(N))

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

sube = [(n, N[n]["e"], EF[n]) for n in N
        if N[n]["tipo"] != "pregunta" and RANK[EF[n]] > RANK[N[n]["e"]]]
assert not sube, "NODOS POR ENCIMA DE SU DECLARACION: %s" % sube
print("2) ningun nodo supera su estatus declarado  [%d nodos comprobados]" % len(N))

# ------------------------------------------------------------------ 3) el cluster
LEJANAS = ["F74", "F76", "F77", "F79", "F81", "F83", "F84"]
ABIERTAS = ["L29", "L31", "L32", "L34", "L36", "L38", "L39"]
for f in LEJANAS:
    assert D["fuentes"][f]["estatus"] == "P", \
        "%s no puede subir de [P]: su primaria no se ha podido leer en esta sesion" % f
for l in ABIERTAS:
    assert D["afirmaciones"][l]["e"] == "P", \
        "%s no puede subir: su fuente lejana [P] SI es su apoyo, no es color" % l
assert D["afirmaciones"]["L35"]["e"] == "V", "L35 se cerro en la tanda 49"
assert EF["L35"] == "V", "L35 declarada V pero efectiva %s" % EF["L35"]
assert D["fuentes"]["F80"]["estatus"] == "V", "el cierre de L35 depende de que F80 sea [V]"
print("3) clúster no inflado: 7 fuentes lejanas en [P], 7 leyes en [P], solo L35 en [V]")

# ------------------------------------------------------------------ 4) aristas
assert "L29" not in D["afirmaciones"]["L35"]["deps"], "la arista L35<-L29 debia retirarse"
assert "X1" not in D["afirmaciones"]["L36"]["deps"], "la arista L36<-X1 debia retirarse"
assert "L34" not in D["afirmaciones"]["L38"]["deps"], "la arista L38<-L34 debia retirarse"
# lo que NO se retira, porque si es apoyo:
assert "F80" in D["afirmaciones"]["L35"]["deps"]
assert "G4" in D["afirmaciones"]["L35"]["deps"]
assert "F81" in D["afirmaciones"]["L36"]["deps"] and "G1" in D["afirmaciones"]["L36"]["deps"]
assert "F84" in D["afirmaciones"]["L38"]["deps"] and "C3" in D["afirmaciones"]["L38"]["deps"]
assert "F79" in D["afirmaciones"]["L34"]["deps"]
assert "F76" in D["afirmaciones"]["L31"]["deps"]
assert "F74" in D["afirmaciones"]["L29"]["deps"]
assert "F77" in D["afirmaciones"]["L32"]["deps"]
assert "F83" in D["afirmaciones"]["L39"]["deps"] and "L36" in D["afirmaciones"]["L39"]["deps"]
print("4) 3 aristas retiradas y verificadas fuera; las 9 que si son apoyo siguen dentro")

# --------------------------------------------- 5) casilla del impostor (R4)
urls = {}
for k, v in D["fuentes"].items():
    u = (v.get("url") or "").strip().rstrip("/")
    if u:
        urls.setdefault(u, []).append(k)
dobles = {u: ks for u, ks in urls.items() if len(ks) > 1}
assert not dobles, "DOS IDENTIFICADORES CON LA MISMA URL (posible impostor): %s" % dobles
for f in LEJANAS:
    assert f in D["fuentes"], f
print("5) ninguna URL de fuente esta duplicada: no hay impostor del tipo F72 = F46")

print("\nTODAS LAS ASERCIONES PASAN. El marcador (COMP/SCORE/RANK de red/motor.py) "
      "no se ha tocado; este script solo lee.")
