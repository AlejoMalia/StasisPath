#!/usr/bin/env python3
"""AUDITORIA DE ARISTAS, TANDA 49 — las dos candidatas que pasan el test, y las que NO.

Sale de `20_cotas/barrido_aristas_global.py`, que enumera las 17 aristas penalizantes del
grafo entero. Este script aplica a cada candidata de ámbito propio el test contrafáctico y
deja escrito el veredicto, para que sea auditable sin volver a pensarlo.

TEST (patrón 4, dependencia innecesaria; el mismo que cerró L5 y L13 en la tanda 48):
    ¿la afirmación de n sigue diciendo LO MISMO si d fuera cierta y si d fuera falsa?
    SI en ambos casos -> d no es apoyo probatorio: la arista sale y la relación se queda
                         en el TEXTO del nodo.
    NO -> la arista se queda: el nodo hereda legítimamente la debilidad de d.

Verificación de ausencia para V16 -> F6: en lugar de razonar sobre un fragmento de
buscador (que fue lo que hizo abortar esta misma auditoría en la tanda 48), se busca cada
afirmación de V16 en el TEXTO COMPLETO del PDF de F6, que está en `10_fuentes/pdf/`.

LIMITE AUTOIMPUESTO Y VERIFICADO AL FINAL: ningún nodo sube por encima de su estatus
DECLARADO, y el preregistro no se toca.
"""
import copy, re, yaml
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
D = yaml.safe_load(open(RAIZ / "red" / "dsny.yaml"))

# --------------------------------------------------------------------------- 1. V16 -> F6
print("=" * 98)
print("CANDIDATA 1 · V16 (Criónica) -> F6   [+0.15]")
print("=" * 98)
print("""HISTORIA DE LA ARISTA (es lo que la delata). La ficha F6 era originalmente un
ARTICULO DE DIVULGACION (Asterisk Mag, «brain freeze»), cuya columna «extraer» en
10_fuentes/fuentes.md pedía «límites reconocidos por el propio campo»: por eso se colgó de
V16. En la TANDA 46 esa ficha se SUSTITUYO por McKenzie et al. 2024, Free Neuropathology
5:35, «Cryopreservation of brain cell structure: a review». Cambió la fuente y nadie volvió
a comprobar si la arista seguía teniendo sentido. Es el análogo en ARISTAS de la auditoría
de declaraciones obsoletas de la tanda 47: una arista obsoleta por sustitución de fuente.""")

V16 = D["vias"]["V16"]
print("\nV16 hoy, campo a campo, y quién sostiene cada campo:")
ATRIB = {
 "mec":     ("F16 + F69", "CPA tras la muerte legal + −196 °C: el protocolo está en Wowk (F16) "
                          "y documentado caso a caso en el informe P-19 (F69)."),
 "escala":  ("F16", "«vitrificación cerebral completa verificada por TC sólo en casos con "
                    "< 10 min entre parada y declaración» — el propio texto cita (F16)."),
 "ventana": ("—", "«almacenamiento»: no es un dato, es la categoría de la fila."),
 "fallo":   ("F69 + F16", "τ_eq real ≫ umbral con el caso primario P-19 (declaración ~1 h, "
                          "perfusión 4 h 40) y «fallo de N₂ líquido en el enfriamiento», que es "
                          "la incidencia de la hora ~85 registrada en la ficha de F69."),
}
for k, (quien, por) in ATRIB.items():
    print(f"  · {k:8} <- {quien:10} {por}")
print("  => NINGUN campo de V16 procede de F6.")

# Verificación de ausencia en el texto completo del PDF de F6.
PDF = RAIZ / "10_fuentes" / "pdf" / "freeneuropathol-05-35-5883.pdf"
try:
    import pymupdf
    doc = pymupdf.open(PDF)
    T = re.sub(r"\s+", " ", "".join(p.get_text() for p in doc))
except Exception as e:                                    # pragma: no cover
    T, doc = "", None
    print(f"\n[aviso] no se pudo abrir el PDF de F6 ({e}); la atribución de arriba no depende de él")

if T:
    print(f"\nTexto completo de F6 leído: {len(T)} caracteres, {doc.page_count} páginas.")
    CLAVES = {
        "cryonic":                 "la práctica de la criónica",
        "legal death":             "la muerte legal (cuello de V16)",
        "computed tomograph":      "verificación por TC de la concentración de CPA",
        "10 min":                  "el umbral de <10 min parada->declaración",
        "shrink":                  "encogimiento cerebral",
        "standby":                 "guardia del equipo",
        "nitrogen depletion":      "agotamiento de N2 líquido",
    }
    for k, q in CLAVES.items():
        n = len(re.findall(k, T, re.I))
        ctx = ""
        if n:
            m = re.search(k, T, re.I)
            ctx = " | 1er contexto: ..." + T[max(0, m.start() - 90):m.start() + 110] + "..."
        print(f"  '{k}': {n} aparicion(es) — {q}{ctx}")
    print("""  => Las dos únicas apariciones de 'cryonic' son BIBLIOGRAFICAS: F6 menciona que
     existe una revisión ajena sobre la práctica de la criónica (Best 2008, que en esta red
     es F5, y que está huérfana). F6 no aporta ninguno de los datos de V16: es una revisión
     de HISTOLOGIA de estructura cerebral, no del procedimiento de la criónica.""")

print("""
TEST CONTRAFACTUAL. ¿Dice V16 lo mismo si la revisión de McKenzie fuera cierta? Sí.
¿Y si fuera enteramente falsa? También: los 4 h 40 hasta la perfusión, el 83 % del área por
encima de la diana, el 36 % de encogimiento y la incidencia de N₂ están medidos en F69 [V],
y el umbral de <10 min está en F16 [V]. => F6 NO es apoyo probatorio de V16.
VEREDICTO: la arista SALE. F6 se conserva en la tabla de fuentes como referencia de
contexto (revisión leída entera en la tanda 46) y su campo `cierra` se corrige, porque decía
que sostenía V16 y no lo sostiene.
NOTA ESTRUCTURAL, y es una fragilidad del marco: F6 no se puede RECOLOCAR donde sí sería
buen apoyo (G5, V17, la capa E0), porque en esta red añadir una fuente [P] a un nodo [V] lo
REBAJA. El marco penaliza citar una revisión aunque la revisión sea correcta.""")

# --------------------------------------------------------------------------- 2. L26 -> L25
print()
print("=" * 98)
print("CANDIDATA 2 · L26 (dosis y daño osmótico en un cerebro criopreservado real) -> L25   [+0.29]")
print("=" * 98)
print("""L26 afirma cuatro cosas, y cada una tiene su fuente:
  1) el caso P-19 fija como objetivo 65 % p/v de CPA ................. F69 [V]
  2) esa misma concentración reduce la respiración basal a la mitad
     (80.4 ± 5.6 frente a 173.3 ± 6.7, capacidad de reserva 38.9 vs 73.4)  F72 [V]
  3) la perfusión fue técnicamente buena (TC: 83.17 % del área por
     encima del 100 % de la diana, 97.42 % por encima del 92 %) ...... F69 [V]
  4) el encogimiento cerebral medido es del 36 %, que es lesión
     OSMOTICA y no toxicidad química ................................. F69 [V] + L20 [V]
  ⇒ veredicto: buena perfusión y baja toxicidad son objetivos enfrentados.

QUE APORTA L25, Y QUE NO. L25 contiene los MISMOS números de F72 (los cita) más una
afirmación propia que sigue ABIERTA: «la temperatura de carga es la variable decisiva»,
que L25 no puede cerrar porque su ancla (la carga en frío rescata la alta molaridad) está
medida en RIÑON (F65/L20) y no en tejido neural — la contradicción I1 del marco.

TEST CONTRAFACTUAL sobre esa afirmación abierta, que es lo único que L25 añade:
  · Si la carga en frío SI rescata la alta molaridad (L25 cierto): el caso P-19 cargó a
    temperatura de perfusión de criónica, no a −22 °C, así que siguió recibiendo la dosis
    tóxica completa. L26 dice lo mismo.
  · Si NO rescata (L25 falso): con más razón la dosis de 65 % p/v es tóxica en cualquier
    protocolo. L26 dice lo mismo, y más fuerte.
  ⇒ el veredicto de L26 es CIERTO en las dos ramas de la incógnita de L25. La arista no es
    apoyo: es una referencia cruzada (L26 cita «F72, L25» por comodidad de lectura, y F72
    es la fuente real de esos números).
VEREDICTO: la arista SALE. La referencia a L25 se conserva en el TEXTO de L26.
EFECTO EN CADENA: Q22 («¿qué dosis y qué daño osmótico recibe un cerebro criopreservado
real?») tiene como respuestas L26, L21 y G4; con L26 en [V] la pregunta pasa a respondida.
LA TENSION NO SE PIERDE (R1): L25 SIGUE EN [P] y la contradicción I1 sigue abierta. Lo que
deja de ocurrir es que una incógnita sobre el MECANISMO rebaje una MEDIDA ya hecha.""")

# ------------------------------------------------------- 3. las que NO pasan el test
print()
print("=" * 98)
print("CANDIDATAS QUE NO PASAN EL TEST (se quedan, y por qué)")
print("=" * 98)
print("""· V06 -> F57 [+0.15]. La columna «escala» de V06 AFIRMA literalmente el dato del
  preprint (riñón de cerdo y humano, 10 días, trasplante simulado) y ése es el mayor
  tamaño alcanzado por la vía: es su veredicto, no un adorno. Si F57 fuera falso, la fila
  cambiaría. Se queda (misma decisión que la tanda 48).
· V09 -> F19 [+0.15]. F19 es la ÚNICA fuente del lémur Cheirogaleus, que es el único
  primate de la fila. Quitar la arista dejaría el dato sin fuente, que es peor. Buscado un
  sustituto en los once PDF de 10_fuentes/pdf/: no hay ninguno sobre lémures (la única
  coincidencia de 'lemur' es un falso positivo dentro del apellido «Lebranth»). Se queda.
· V11 -> F19 [+0.15]. Es la única fuente de la fila entera (estivación del pez pulmonado):
  sin ella la vía no tiene nada. Se queda. Ver la nota de V11 sobre por qué tampoco se
  cierra por irrelevancia demostrada.
· L37 -> F82 [+0.11]. Sin F82 la ley se quedaría sin ninguna fuente. Además la laguna real
  (ni los 360 kHz ni la permitividad del tejido tienen fuente en la red) se buscó otra vez
  en los once PDF: ninguno menciona kHz, MHz, permitividad ni dieléctrico salvo una cita
  bibliográfica en F6 a Wowk 2024 (27 MHz), que es OTRO trabajo y no está en la red. Se
  queda (misma decisión que la tanda 48).
· Q5, Q6, Q7, Q11, Q20 -> leyes de campo lejano y X2. Una PREGUNTA vale lo que su
  respuesta más débil, y eso es correcto: una pregunta con una respuesta floja no está
  respondida. Quitar la respuesta para subir la pregunta sería esconder la respuesta, no
  auditar una arista. Se quedan TODAS. (Además el clúster de campos lejanos lo trabaja
  otro agente en paralelo en esta misma tanda.)""")

# ------------------------------------------------------- 4. efecto medido
print()
print("=" * 98)
print("EFECTO MEDIDO DE LAS DOS RETIRADAS (regla del motor, en memoria)")
print("=" * 98)
import importlib.util
spec = importlib.util.spec_from_file_location("bar", RAIZ / "20_cotas" / "barrido_aristas_global.py")

RANK = {"A": 0, "P": 1, "V": 2, "M": 2, "ROTO": -1}
SCORE = {"M": 1.0, "V": 1.0, "P": 0.6, "A": 0.2, "ROTO": 0.0}
COMP = [("Ontologia", 15, {"afirmacion"}, {"ontologia"}),
        ("Magnitudes y umbrales", 35, {"afirmacion"}, {"magnitud", "frontera"}),
        ("Leyes y cotas", 15, {"afirmacion", "cota"}, {"ley", None}),
        ("Vias", 10, {"via"}, None),
        ("Preregistro falsable", 15, {"prereg"}, None),
        ("Preguntas respondidas", 10, {"pregunta"}, None)]


def construir(d):
    N = {}
    for k, v in d["fuentes"].items(): N[k] = {"tipo": "fuente", "e": v["estatus"], "deps": [], "capa": None}
    for k, v in d["parametros"].items(): N[k] = {"tipo": "param", "e": v["e"], "deps": [v["f"]], "capa": None}
    for k, v in d["cotas"].items():
        N[k] = {"tipo": "cota", "e": "M", "deps": list(v["deps"]) + list(v.get("fuente_verif", [])), "capa": None}
    for k, v in d["afirmaciones"].items():
        N[k] = {"tipo": "afirmacion", "e": v["e"], "deps": list(v["deps"]), "capa": v["capa"]}
    for k, v in d["vias"].items(): N[k] = {"tipo": "via", "e": v["e"], "deps": list(v["deps"]), "capa": None}
    for k in [x for x in d["preregistro"] if x != "fecha"]:
        N[k] = {"tipo": "prereg", "e": d["preregistro"][k]["e"], "deps": list(d["preregistro"][k]["deps"]), "capa": None}
    for k, v in d["preguntas"].items(): N[k] = {"tipo": "pregunta", "e": "M", "deps": list(v["a"]), "capa": None}
    return N


def propagar(N, pregs):
    EF = {}

    def ef(n, pila=()):
        if n in EF: return EF[n]
        x = N[n]; e = x["e"]
        if x["tipo"] == "prereg":
            EF[n] = e; return e
        for dd in x["deps"]:
            if dd not in N or N[dd]["tipo"] == "param" or dd in pila: continue
            ed = ef(dd, pila + (n,))
            if RANK[ed] < RANK[e]: e = ed
        EF[n] = e
        return e
    for n in N: ef(n)
    for q in pregs: EF[q] = min((EF[a] for a in N[q]["deps"]), key=lambda s: RANK[s])
    return EF


def prog(N, EF):
    t = 0.0
    for _, w, tp, cp in COMP:
        ns = [n for n in EF if N[n]["tipo"] in tp and (cp is None or N[n]["capa"] in cp)]
        if ns: t += w * sum(SCORE[EF[n]] for n in ns) / len(ns)
    return t


N0 = construir(D); EF0 = propagar(N0, D["preguntas"]); P0 = prog(N0, EF0)
d2 = copy.deepcopy(D)
quitadas = []
for sec, n, dep in (("vias", "V16", "F6"), ("afirmaciones", "L26", "L25")):
    if dep in d2[sec][n]["deps"]:
        d2[sec][n]["deps"].remove(dep); quitadas.append(f"{n}->{dep}")
N1 = construir(d2); EF1 = propagar(N1, d2["preguntas"]); P1 = prog(N1, EF1)
print(f"aristas retiradas en la simulación: {quitadas or '(ya retiradas en el YAML)'}")
print(f"progreso: {P0:.2f} % -> {P1:.2f} %  ({P1 - P0:+.2f})")
print("nodos que cambian de estatus efectivo:")
for n in sorted(EF1):
    if EF0.get(n) != EF1[n]: print(f"  {n}: {EF0[n]} -> {EF1[n]}  (declarado {N1[n]['e']})")

print()
print("VERIFICACION DEL LIMITE: ningun nodo por encima de su estatus DECLARADO")
malos = [n for n in EF1 if RANK[EF1[n]] > RANK[N1[n]["e"]] and N1[n]["tipo"] != "pregunta"]
assert not malos, f"VIOLACION: {malos}"
assert EF1["L25"] == "P", "L25 debe seguir en [P]: la tensión de I1 se conserva"
assert EF1["X2"] == "A", "X2 debe seguir en [A]: la frontera empírica no se toca"
assert EF1["V06"] == "P" and EF1["V09"] == "P" and EF1["V11"] == "P" and EF1["L37"] == "P", \
    "las aristas que NO pasan el test deben seguir penalizando"
print("OK · L25 sigue [P] · X2 sigue [A] · V06/V09/V11/L37 siguen [P] · nadie supera su declaración")
