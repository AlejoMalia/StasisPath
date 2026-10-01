#!/usr/bin/env python3
"""StasisPath: motor de la red. Fuente única: red/stasispath.yaml.

  python3 red/motor.py             recalcula todo y regenera los documentos
  python3 red/motor.py impacto X   lista los nodos aguas abajo de X (parámetro, fuente, cota, afirmación...)

MATE: cada cota se evalúa en las esquinas del rango de sus parámetros. Las funciones son monótonas
en cada parámetro, así que las esquinas acotan el rango completo sin Monte Carlo (R5: no hay teatro).
Un veredicto que se sostiene en todas las esquinas es mate (M); si falla en alguna, hay una fuga
y la tensión se conserva (A, R1).
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

def _rate(p, LC):  # enfriamiento convectivo en el centro (°C/min), anclado en 3 L
    return p["anc_rate"] * (p["anc_LC"] / LC) ** p["exp_LC"]

def C1(p):
    rs = lambda cwr: math.sqrt(p["alpha"] * p["dT_rew"] / (cwr / 60)) * 100
    o = {"rstar_M22": rs(p["CWR_M22"]), "rstar_VMP": rs(p["CWR_VMP"])}
    v = {"VMP exige calentamiento volumétrico por encima de 1 cm": (o["rstar_VMP"] < 1, True),
         "M22 no se recalienta por superficie en el tronco (r ~15 cm)": (o["rstar_M22"] < 15, True)}
    return o, v

def C2(p):
    T10 = 37 + 10 * math.log(p["t37"] / (10 * 525600)) / math.log(p["Q10"])
    o = {"w15": _w(p, 15), "w10": _w(p, 10), "w0": _w(p, 0), "T10y": T10}
    T10f = 37 + 10 * math.log(p["t37"] / (10 * 525600)) / math.log(p["Q10_frio"])
    o["T10y_frio"] = T10f
    v = {"10 años exigen T < 0 °C con CUALQUIER Q10 medido (templado y frío)": (T10 < 0 and T10f < 0, True),
         "el Q10 del tramo frío exige MENOS frío que el templado (no-linealidad, NO significativa en la fuente)": (T10f > T10, False)}
    return o, v

def C3(p):
    n = p["exp_LC"]
    o = {"LCstar_M22": p["anc_LC"] * (p["anc_rate"] / p["CCR_M22"]) ** (1 / n),
         "LCstar_VMP": p["anc_LC"] * (p["anc_rate"] / p["CCR_VMP"]) ** (1 / n),
         "rate_kidneyH": _rate(p, p["LC_kidneyH"]), "rate_body": _rate(p, p["LC_body"]),
         "rate_trunk": _rate(p, p["LC_trunk"])}
    v = {"VMP no vitrifica un riñón humano por convección": (o["rate_kidneyH"] < p["CCR_VMP"], True),
         "M22 vitrifica el cuerpo medio (LC ~3.9 cm)": (o["rate_body"] >= p["CCR_M22"], False),
         "M22 falla en el centro del tronco": (o["rate_trunk"] < p["CCR_M22"], False)}
    return o, v

def C4(p):
    o = {"frog": p["frog_days"] * 1440 / _w(p, -6.3), "turtle": p["turtle_days"] * 1440 / _w(p, 3),
         "turtle22": p["turtle22_h"] * 60 / _w(p, 22)}
    v = {"rana > ×100": (o["frog"] > 100, True), "tortuga > ×100": (o["turtle"] > 100, True),
         "tortuga a 22 °C > ×10 (no térmico)": (o["turtle22"] > 10, True)}
    return o, v

def C5(p):
    kg = lambda f: p["BMR"] * f * 365 / 7700
    o = {"kg25": kg(0.25), "kg3": kg(0.03)}
    return o, {"1 año al 25 % < 30 kg de grasa": (o["kg25"] < 30, True)}

def C6(p):
    r4 = _rate(p, 4.0)
    Q = 0.5 * 0.8 * 334e3            # J: congelar el 50 % del agua de 1 kg
    P = 100 * (1e-3 / 0.04) * 10     # W: h = 100, A = V/LC, ΔT = 10 K
    o = {"rate4": r4, "latent4": Q / P / 60}
    v = {"LC 4 cm dentro de la ventana lenta 0.1–1 °C/min": (0.1 <= r4 <= 1.0, True),
         "calor latente < 3 h": (o["latent4"] < 180, True)}
    return o, v

def C7(p):
    o = {"tau_org_good": p["tau_org_good"], "tau_org_surv": p["tau_org_surv"], "tau_cel": p["tau_cel"],
         "f_org": p["tau_org_good"] / p["t37"], "f_cel": p["tau_cel"] / p["t37"],
         "legal_x": p["tau_org_good"] / p["legal_obs"]}
    o["f_exist"] = p["tau_org_exist"] / p["t37"]
    v = {"zona gris: τ_cel > τ_org (sobrevive con déficit)": (p["tau_cel"] > p["tau_org_surv"], True),
         "existencia fuera de lo reproducible: τ_org,bueno < τ_exist ≤ τ_cel": (p["tau_org_good"] < p["tau_org_exist"] <= p["tau_cel"], True),
         "la muerte legal se declara antes del umbral del organismo": (p["legal_obs"] <= p["tau_org_good"], True)}
    return o, v

def C8(p):
    req = _rate(p, 4.0)
    o = {"CCR_req4": req}
    v = {"VMP insuficiente a LC 4 cm": (p["CCR_VMP"] > req, True),
         "M22 suficiente a LC 4 cm": (p["CCR_M22"] <= req, False)}
    return o, v

def C9(p):
    w = _w(p, p["hypo_case_T"])
    o = {"w137": w, "extra": p["hypo_case_min"] / w}
    return o, {"no lo explica el flujo cero de C2 (×>3) ⇒ hubo bajo flujo": (o["extra"] > 3, True)}

def C11(p):
    # Banda de lesión por frío: 0-20 C (F53). Atravesarla rápido reduce daño; el hielo extracelular exige lento.
    banda = 20.0
    lento = 1.0                      # C/min, techo de la ventana "lenta" para hielo extracelular
    t_banda = banda / lento          # min que se tarda en cruzar la banda enfriando lento
    r4 = _rate(p, 4.0)               # lo que da la convección a LC 4 cm
    o = {"t_banda_lento": t_banda, "t_banda_conv": banda / r4, "rate4": r4}
    return o, {"cruzar la banda 0-20 C enfriando lento tarda > 15 min (exposicion real)": (t_banda > 15, True),
               "a LC 4 cm la conveccion es aun mas lenta que el techo lento": (r4 < lento, True)}

def C10(p):
    w = _w(p, p["flush_T"])            # perro: temperatura lograda con el flush
    wp = _w(p, p["pig_T"])             # cerdo: su propia temperatura (F42), no la del perro
    o = {"w": w, "w_pig": wp, "extra": p["flush_min"] / w, "extra_pig": p["pig_min"] / wp}
    return o, {
        # El CERDO es el veredicto clave: mismo protocolo de hipotermia, sin flush aórtico.
        "C2 calibra dentro de ×5 contra el CERDO a 10 °C": (o["extra_pig"] < 5, True),
        "C2 es conservadora frente al cerdo (no robusto: en la esquina generosa se vuelve OPTIMISTA)": (o["extra_pig"] >= 1, False),
        # El PERRO con flush queda como no clave: su protocolo añade lavado aórtico, no es comparación limpia.
        "C2 dentro de ×5 del perro con flush (protocolo distinto, no clave)": (o["extra"] < 5, False)}

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
# texto derivado de C3: veredicto del tronco
tv = next(x for x in R["C3"]["ver"] if x["t"].startswith("M22 falla"))
R["C3"]["txt"] = {"trunk_verdict": "imposible (robusto)" if tv["robusto"] else
                  ("indeterminado: LC del tronco dentro de la banda de LC*" if tv["central"] else "posible")}

# ---------------------------------------------------------------- derivadas
# Magnitudes calculadas desde parámetros y entre sí. Se resuelven por dependencia
# y quedan disponibles en el texto de cualquier nodo como {nombre}.
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
# son TODAS fuertes es sospechoso: puede que su declaración se escribiera antes de que las fuentes
# se verificaran. No se sube solo (eso sería inflar el número): se AVISA para revisarlo a mano.
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
        # Un preregistro no vale menos porque lo que prueba esté abierto: ESE es su propósito.
        # Se juzga por su especificación (umbrales, n, cegado, falsación), que es su estatus declarado.
        EF[n] = e; MOTIVO[n] = None
        return e
    for d in x["deps"]:
        if d not in NODOS or NODOS[d]["tipo"] == "param" or d in pila: continue  # los parámetros entran vía las cotas
        ed = efectivo(d, pila + (n,))
        if RANK[ed] < RANK[e]: e, motivo = ed, d
    EF[n] = e; MOTIVO[n] = motivo
    return e
for n in NODOS: efectivo(n)
for q in D["preguntas"]:   # una pregunta vale lo que su respuesta más débil
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
# Cada preregistro se congela por separado: añadir uno nuevo es legítimo, editar uno ya congelado es ALARMA R2.
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
if rotos: PRE_ESTADO = f"**ALARMA R2: editado tras congelarse: {', '.join(rotos)}**"
elif nuevos: PRE_ESTADO = f"intacto; congelados hoy: {', '.join(nuevos)} ({len(IDS_PR)} en total)"
else: PRE_ESTADO = f"intacto ({len(IDS_PR)} preregistros)"
h = HASHES[IDS_PR[0]]

# ---------------------------------------------------------------- progreso
# Cada componente se define por TIPO de nodo (no por prefijo del id: un prefijo nuevo se quedaba fuera del cómputo).
COMP = [("Ontología", 15, {"afirmacion"}, {"ontologia"}), ("Magnitudes y umbrales", 35, {"afirmacion"}, {"magnitud", "frontera"}),
        ("Leyes y cotas", 15, {"afirmacion", "cota"}, {"ley", None}), ("Vías", 10, {"via"}, None),
        ("Preregistro falsable", 15, {"prereg"}, None), ("Preguntas respondidas", 10, {"pregunta"}, None)]
def comp_score(tipos, capas):
    ns = [n for n in EF if NODOS[n]["tipo"] in tipos and
          (capas is None or D["afirmaciones"].get(n, {}).get("capa") in capas)]
    return (sum(SCORE[EF[n]] for n in ns) / len(ns), len(ns)) if ns else (0.0, 0)
PROG = [(nom, w, *comp_score(tp, cp)) for nom, w, tp, cp in COMP]
TOTAL = sum(w * s for _, w, s, _ in PROG)

# ---------------------------------------------------------------- salidas
AUTO = "<!-- AUTO-GENERADO por red/motor.py desde red/stasispath.yaml. NO EDITAR A MANO. -->\n"
def badge(n): return f"**{EF[n]}**" + ("" if EF[n] == NODOS[n]["e"] or NODOS[n]["tipo"] == "pregunta" else f" (declarado {NODOS[n]['e']}, rebajado por {MOTIVO[n]})")
def tabla(filas, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join("| " + " | ".join(str(c) for c in f) + " |" for f in filas) + "\n"

def sec_cotas():
    out = []
    for cid, c in D["cotas"].items():
        r = R[cid]
        outs = ", ".join(f"{k} = {fmt(r['out'][k], *r['rng'][k])}" for k in r["out"])
        vers = "; ".join(f"{'✔' if v['central'] else '✘'} {v['t']} → {v['e']}{'' if v['clave'] else ' (no clave)'}" for v in r["ver"])
        out.append([cid, c["titulo"], outs, vers, f"**{r['e']}**"])
    return tabla(out, ["cota", "ley", "salidas: central (rango en esquinas)", "veredictos", "estatus"])

def cap(capa): return [n for n, v in D["afirmaciones"].items() if v["capa"] == capa]
def bloque(ids): return "\n".join(f"- **{n}** [{badge(n)}] {rellenar(D['afirmaciones'][n]['t'])}" for n in ids) + "\n"

vias = [[k, v["via"], rellenar(v["mec"]), rellenar(v["escala"]), rellenar(v["ventana"]), rellenar(v["fallo"]), badge(k)] for k, v in D["vias"].items()]
TV = tabla(vias, ["id", "vía", "mecanismo", "escala demostrada", "ventana", "fallo típico", "estatus"])
preg = [[k, v["t"], ", ".join(v["a"]), f"**{EF[k]}**"] for k, v in D["preguntas"].items()]
TQ = tabla(preg, ["#", "pregunta", "responde", "estatus efectivo"])
TP = tabla([[n, f"{w} %", f"{s*100:.0f} %", k, f"{w*s:.1f}"] for n, w, s, k in PROG] + [["**Total**", "", "", "", f"**{TOTAL:.1f} %**"]],
           ["componente", "peso", "cumplido", "nodos", "aporta"])
FU = "\n".join(f"- **{k}** [{v['estatus']}] {v['cita']}: {v['url']}" for k, v in D["fuentes"].items())
avisos = [f"- dependencia inexistente: {n} → {d}" for n, d in faltan]
avisos += [f"- {n}: declarado {NODOS[n]['e']}, efectivo {EF[n]} (por {MOTIVO[n]})" for n in NODOS if MOTIVO.get(n) and NODOS[n]["tipo"] != "pregunta"]
abiertos = [n for n in NODOS if EF[n] == "A" and NODOS[n]["tipo"] in ("afirmacion", "cota", "via")]

marco = AUTO + f"""# {D['meta']['titulo']}

> **Pregunta canónica:** {D['meta']['pregunta']}
> Versión generada automáticamente · preregistro {PRE_ESTADO} · progreso **{TOTAL:.0f} %**
> Estatus: M = mate (cota robusta en todo el rango) · V = verificado con fuente primaria · P = prior o fuente secundaria · A = abierto (tensión conservada)

Encuentros entre capas: **[ENCUENTROS.md](ENCUENTROS.md)** · Brechas al humano: **[BRECHAS.md](BRECHAS.md)** · Escalado y validación: **[ESCALADO.md](ESCALADO.md)** · Márgenes: **[MARGENES.md](MARGENES.md)** · Derivación y predicción de P19: **[DERIVACION.md](DERIVACION.md)** · Formulación interna: **[FORMULACION.md](FORMULACION.md)** · Triangulación: **[TRIANGULACION.md](TRIANGULACION.md)** · Precisión: **[PRECISION.md](PRECISION.md)** · Barrido: **[BARRIDO.md](BARRIDO.md)** · Proyección condicional: **[PROYECCION.md](PROYECCION.md)**

## 1. Ontología
{bloque(cap('ontologia'))}
## 2. Espacio de estados: magnitudes y umbrales
Un sistema está en **pausa reversible** si y sólo si todas las magnitudes quedan por debajo de su umbral durante la entrada, el almacenamiento y la salida.
{bloque(cap('magnitud'))}
## 3. Leyes de escala (el estatus de cada una lo fija la red)
{bloque(cap('ley'))}
### 3.1 Cotas: cálculo en las esquinas del rango de parámetros
{sec_cotas()}
## 4. Frontera empírica
{bloque(cap('frontera'))}
## 5. Vías
{TV}
## 6. Preregistro (congelado el {PR['fecha']}; hash {h[:12]})
{chr(10).join(rellenar(PR[k]['t']) + (chr(10) + "> " + rellenar(PR[k]['enmiendas']).replace(chr(10), chr(10) + "> ") if PR[k].get('enmiendas') else "") for k in IDS_PR)}
## 7. Preguntas canónicas
{TQ}
## 8. Tensiones abiertas (R1)
{chr(10).join('- ' + n + ': ' + (rellenar(D['afirmaciones'][n]['t']) if n in D['afirmaciones'] else D['cotas'][n]['titulo'] if n in D['cotas'] else D['vias'][n]['via']) for n in abiertos) or '- ninguna'}

## 9. Progreso (calculado desde los estatus de los nodos)
{TP}
Puntuación por nodo: M/V = 1 · P = 0.6 · A = 0.2 · ROTO = 0.

## 10. Fuentes
{FU}
"""
(ROOT / "MARCO.md").write_text(marco)
(ROOT / "00_marco" / "preguntas.md").write_text(AUTO + "# Preguntas canónicas\n\n" + TQ)
(ROOT / "40_vias" / "tabla_vias.md").write_text(AUTO + "# Tabla de vías\n\n" + TV)
(ROOT / "00_marco" / "progreso.md").write_text(AUTO + "# Progreso\n\n" + TP)

# grafo mermaid
col = {"M": "fill:#1b7f3b,color:#fff", "V": "fill:#2e9e57,color:#fff", "P": "fill:#e0a800", "A": "fill:#c0392b,color:#fff", "ROTO": "fill:#000,color:#fff"}
g = ["flowchart LR"]
capas = {"param": "Parámetros", "cota": "Cotas", "afirmacion": "Afirmaciones", "prereg": "Preregistro", "via": "Vías", "pregunta": "Preguntas"}
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
(RED / "grafo.md").write_text(AUTO + "# Red StasisPath\n\nVerde = M/V · ámbar = P · rojo = A · negro = ROTO. Las flechas van de la dependencia al nodo dependiente.\n\n```mermaid\n" + "\n".join(g) + "\n```\n")
DER_TXT = "\n## Derivadas (calculadas, no escritas a mano)\n" + tabla(
    [[k, D["derivadas"][k].get("u", ""), fmt(DERIV[k], DERIV[k], DERIV[k]) if not callable(DERIV[k]) else "función",
      D["derivadas"][k].get("d", "")] for k in DERIV], ["magnitud", "unidad", "valor", "qué es"])
if DERIV_FALLAN: DER_TXT += f"\n**No se pudieron evaluar:** {', '.join(DERIV_FALLAN)}\n"
ORG_TXT = "\n## Órganos (una línea cada uno; lo demás se calcula)\n" + tabla(
    [[n, f"{m:,}", fmt(DERIV["LC_esfera"](m), 0, 0), fmt(DERIV["tasa_conv"](DERIV["LC_esfera"](m)), 0, 0),
      fmt(DERIV["M_de_CCR"](DERIV["tasa_conv"](DERIV["LC_esfera"](m))), 0, 0),
      "viable" if DERIV["M_de_CCR"](DERIV["tasa_conv"](DERIV["LC_esfera"](m))) <= DERIV["M_toxico"] else "**no viable**"]
     for n, m in D.get("organos", {}).items()],
    ["órgano", "masa g", "LC cm", "tasa °C/min", "M exigida", "veredicto"])
import cruce
CRU = cruce.generar(D, PAR, ROOT)
print(f"Cruce de capas: {CRU['n_pts']} puntos contra la ley termica · {CRU['excesivos']} exigen mecanismo no termico · "
      + (f"BRECHA artificial x{CRU['max_art']:.3g} | natural x{CRU['min_nat']:.3g}" if CRU['brecha'] else "sin brecha limpia")
      + f" · {len(CRU['sin_check'])} vias sin ventana numerica")
import cascada
CAS = cascada.generar(D, PAR, DERIV, ROOT)
print(f"Cascada: TODO el marco combinado honestamente = {100*CAS['p_honesta']:.0f} % (ingenuo {100*CAS['p_ingenua']:.0f} %, "
      f"{CAS['n_grupos']} anclas independientes) · solo la cadena de Arrhenius {100*CAS['p_pasa']:.0f} % · "
      f"dano mediana {CAS['mediana']:.3g} (90 % {CAS['p05']:.3g}-{CAS['p95']:.3g}) · NO cierra X2")
import espacio
ESP = espacio.generar(D, PAR, DERIV, ROOT)
print(f"Espacio de X2: CCR requerida {ESP['ccr_req']:.3g} C/min · {len(ESP['con_ccr'])} vitrifican, {len(ESP['con_fun'])} con funcion neural, interseccion VACIA · region objetivo {'excluida' if ESP['excluida'] else 'NO excluida por ninguna ley'}")
import rumbo
RUMBO = rumbo.generar(D, NODOS, RANK, SCORE, COMP, ROOT)
print(f"Rumbo: {RUMBO['base']:.1f} % -> meta {RUMBO['meta']:.1f} % · {len(RUMBO['camino'])} cierres llegan a {RUMBO['final']:.1f} % · techo con todo abierto cerrado {RUMBO['techo']:.1f} %")
import proyeccion
PROY = proyeccion.generar(D, PAR, DERIV, ROOT, TOTAL, RUMBO)
print(f"Proyeccion: tenemos +-{PROY['med_t']*100:.0f} % vs necesitamos +-{PROY['med_n']*100:.0f} % · techo del escenario {PROY['proy']:.1f} % · irreducible {PROY['irreducible']:.1f} %")

(RED / "informe.md").write_text(AUTO + DER_TXT + ORG_TXT + f"\n# Informe de la red\n\nNodos: {len(NODOS)} · preregistro: {PRE_ESTADO} · progreso: {TOTAL:.1f} %\n\n## Avisos\n" + ("\n".join(avisos) or "- ninguno") + "\n\n## Cotas\n" + sec_cotas())

sys.path.insert(0, str(RED))
import encuentros
ENC_AVISOS, ENC_HUECOS, ENC_CHEB = encuentros.generar(D, PAR, R, ROOT)
import barrido
CORTES, CORTE_NADES = barrido.generar(D, PAR, DERIV, ROOT)
PLANO = barrido.plano_diseno(D, PAR, DERIV, ROOT)
print(f"Barrido: {len(CORTES)} margenes barridos · corte NADES CCR={CORTE_NADES:.3g} C/min")
import precision
PREC = precision.generar(D, PAR, DERIV, ROOT)
print(f"Precision: Bi=1 en LC={PREC['LC_crit']:.2f} cm · MonteCarlo masa viable mediana {PREC['mediana']:.1f} kg (p5 {PREC['p5']:.1f}, p95 {PREC['p95']:.1f})")
import triangular
TRI = triangular.generar(D, PAR, DERIV, ROOT)
_con = [r for r in TRI if "contradicción" in str(r[2])]
print(f"Triangulacion: {len(TRI)} incognitas proyectadas · {len(_con)} con CONTRADICCION" + (": " + ", ".join(r[0] for r in _con) if _con else ""))
import formular
FOR = formular.generar(D, PAR, ROOT)
print(f"Formulacion: {FOR['n_formulas']} formulas · limite de viabilidad LC={FOR['lc_critico']:.2f} cm ~ {FOR['m_critico']/1000:.1f} kg")
import derivar
DER = derivar.generar(ROOT)
print(f"Derivacion: Arrhenius Ea/R={DER['EaR']:.0f}K -> P19 frio predicho {DER['pred']:.3f} (vs {DER['caliente']:.2f} caliente, x{DER['factor']:.0f}) · anclas {'OK' if DER['anclas_ok'] else 'FALLAN'}")
import margenes
MG_FILAS, MG_FRAGILES = margenes.generar(D, PAR, COTAS, ROOT)
print(f"Margenes: {len(MG_FRAGILES)} veredictos con holgura < 2 de {len(MG_FILAS)}")
import p21
P21R = p21.generar(D, ROOT)
print(f"P21: {P21R['estado']} · {P21R['motivo']}")
import confianza
CF = confianza.generar(D, PAR, COTAS, ROOT)
print(f"Confianza: P(falla algún veredicto clave) = {confianza.pct(CF['p_alguna'])} (pesimista {confianza.pct(CF['p_alguna1'])}) · "
      f"{len(CF['riesgo'])} no clave > 1 % · medir primero: {', '.join(d for d, _ in CF['prio1'][:3])}")
import escalado
ESC = escalado.generar(D, PAR, R, ROOT)
print(f"Escalado: tau_eq valida (error x{ESC['err_tau']:.1f}) - termica valida (x{ESC['err_term']:.1f}) - neuronas r={ESC['r_neu']:+.2f} (no valida)")
import brechas
BR, RUTAS = brechas.generar(D, PAR, R, ROOT)
print("Brechas al humano: " + " · ".join(f"{v['nom'].split(' (')[0]}: cuello {v['cuello']} {BR[v['cuello']]['pct']:.0f} %" for v in RUTAS.values()))
with open(RED / "informe.md", "a") as fh:
    fh.write(f"\n## Encuentros\n- distancia de la meta a la frontera: {ENC_CHEB:.1f} órdenes de magnitud\n- huecos: {', '.join(ENC_HUECOS)}\n"
             + "".join(f"- {a}\n" for a in ENC_AVISOS))

if len(sys.argv) > 2 and sys.argv[1] == "impacto":
    x = sys.argv[2]; imp = impacto(x)
    print(f"Si cambias {x}, se recalculan o reevalúan {len(imp)} nodos:")
    for t in ("cota", "afirmacion", "via", "prereg", "pregunta"):
        s = [m for m in imp if NODOS[m]["tipo"] == t]
        if s: print(f"  {t:11s}: {', '.join(s)}")
else:
    print(f"OK · {len(NODOS)} nodos · progreso {TOTAL:.1f} % · preregistro {PRE_ESTADO}")
    for cid in R: print(f"  {cid}: {R[cid]['e']:4s} " + " | ".join(f"{'✔' if v['central'] else '✘'}{'R' if v['robusto'] else '~'} {v['t']}" for v in R[cid]["ver"]))
    print("Avisos:\n" + ("\n".join(avisos) or "  ninguno"))
    _aud = auditoria_declaraciones()
    print(f"Auditoría de declaraciones: {len(_aud)} nodo(s) declarados débiles con TODAS sus dependencias fuertes"
          + (" — revisar si la declaración está obsoleta:" if _aud else " (ninguno)"))
    for _n, _ds in _aud:
        print(f"  {_n} [{NODOS[_n]['e']}] <- " + ", ".join(f"{d}[{e}]" for d, e in _ds))
