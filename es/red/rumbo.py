"""StasisPath: rumbo — el marco calcula hacia dónde crecer.

Para cada nodo abierto (fuente secundaria [P], o afirmación/cota/vía en [A] o [P]) se simula EN MEMORIA
qué pasaría si se cerrara (pasara a [V]), se repropagan los estatus con la misma regla del motor
(un nodo nunca vale más que su dependencia más débil) y se mide cuánto sube el progreso.

Con eso:
  1. ranking de cierres por puntos ganados;
  2. camino voraz: la secuencia mínima de cierres que llega a la meta fijada en `rumbo.meta` del YAML;
  3. para cada cierre, la acción que lo cumple (campo `cierra` del nodo si existe; si no, la genérica).

Límite declarado: esto NO cierra nada. Dice qué cerrar y cuánto vale. Un nodo sólo sube cuando entra
el dato o la fuente en el YAML (R2, R5). Salida: RUMBO.md. Lo llama motor.py.
"""
from collections import defaultdict

ACCION = {"fuente": "leer la fuente primaria y extraer el dato",
          "afirmacion": "dato o fuente primaria para sus dependencias propias",
          "cota": "estrechar los parámetros o verificar con fuente primaria",
          "via": "datos publicados de la vía (escala, ventana, fallo)"}

def _propagar(NODOS, D, RANK, cambios):
    EF = {}
    def ef(n, pila=()):
        if n in EF: return EF[n]
        x = NODOS[n]; e = cambios.get(n, x["e"])
        if x["tipo"] == "prereg":
            EF[n] = e; return e
        for d in x["deps"]:
            if d not in NODOS or NODOS[d]["tipo"] == "param" or d in pila: continue
            ed = ef(d, pila + (n,))
            if RANK[ed] < RANK[e]: e = ed
        EF[n] = e; return e
    for n in NODOS: ef(n)
    for q in D["preguntas"]:
        EF[q] = min((EF[a] for a in D["preguntas"][q]["a"]), key=lambda s: RANK[s])
    return EF

def _total(EF, NODOS, D, COMP, SCORE):
    t = 0.0
    for _, w, tipos, capas in COMP:
        ns = [n for n in EF if NODOS[n]["tipo"] in tipos and
              (capas is None or D["afirmaciones"].get(n, {}).get("capa") in capas)]
        if ns: t += w * sum(SCORE[EF[n]] for n in ns) / len(ns)
    return t

def _accion(n, NODOS, D):
    for sec in ("fuentes", "afirmaciones", "vias", "cotas"):
        if n in D.get(sec, {}) and isinstance(D[sec][n], dict) and D[sec][n].get("cierra"):
            return D[sec][n]["cierra"]
    return ACCION.get(NODOS[n]["tipo"], "—")

def simular(D, NODOS, RANK, SCORE, COMP, nodos):
    """Progreso si los nodos dados pasaran a [V]. Sólo en memoria."""
    return _total(_propagar(NODOS, D, RANK, {n: "V" for n in nodos}), NODOS, D, COMP, SCORE)

def generar(D, NODOS, RANK, SCORE, COMP, ROOT):
    base = _total(_propagar(NODOS, D, RANK, {}), NODOS, D, COMP, SCORE)
    abiertos = [n for n, x in NODOS.items()
                if x["tipo"] in ("fuente", "afirmacion", "cota", "via") and x["e"] in ("A", "P")]
    gan = {n: _total(_propagar(NODOS, D, RANK, {n: "V"}), NODOS, D, COMP, SCORE) - base for n in abiertos}

    # camino voraz hacia la meta
    meta = float(D.get("rumbo", {}).get("meta", 98.0))
    cambios, actual, camino = {}, base, []
    while actual < meta - 1e-9:
        mejor, mg = None, 0.0
        for n in abiertos:
            if n in cambios: continue
            c = dict(cambios); c[n] = "V"
            g = _total(_propagar(NODOS, D, RANK, c), NODOS, D, COMP, SCORE) - actual
            if g > mg + 1e-12: mejor, mg = n, g
        if mejor is None:
            # ningún cierre suelto sube: buscar el PAR que más sube (uno sujeta al otro)
            resto = [n for n in abiertos if n not in cambios]
            par, pg = None, 0.0
            for i, n1 in enumerate(resto):
                for n2 in resto[i + 1:]:
                    c = dict(cambios); c[n1] = "V"; c[n2] = "V"
                    g = _total(_propagar(NODOS, D, RANK, c), NODOS, D, COMP, SCORE) - actual
                    if g > pg + 1e-12: par, pg = (n1, n2), g
            if par is None: break
            for n in par: cambios[n] = "V"
            actual += pg
            camino.append((" + ".join(par), pg, actual))
            continue
        cambios[mejor] = "V"; actual += mg
        camino.append((mejor, mg, actual))
    techo = _total(_propagar(NODOS, D, RANK, {n: "V" for n in abiertos}), NODOS, D, COMP, SCORE)

    def fila(n, g):
        x = NODOS[n]
        return [n, x["tipo"], x["e"], f"+{g:.2f}", _accion(n, NODOS, D)]
    tab = lambda filas, cab: ("| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" +
                              "\n".join("| " + " | ".join(str(c) for c in f) + " |" for f in filas) + "\n")
    rank = sorted(((n, g) for n, g in gan.items() if g > 0.005), key=lambda t: -t[1])
    solos = sum(1 for g in gan.values() if g <= 0.005)
    doc = ("<!-- AUTO-GENERADO por red/rumbo.py. NO EDITAR A MANO. -->\n"
           "# StasisPath: rumbo — qué cerrar, en qué orden y cuánto vale\n\n"
           f"**Progreso actual: {base:.1f} %. Meta fijada en el YAML (`rumbo.meta`): {meta:.1f} %.**\n\n"
           "El marco simula en memoria el cierre de cada nodo abierto y repropaga los estatus con la regla del motor. "
           "**No cierra nada**: un nodo sólo sube cuando entra su dato o su fuente en `red/stasispath.yaml`.\n\n"
           f"- **Techo si se cerrara TODO lo abierto:** {techo:.1f} %. Lo que queda por encima no depende de nodos abiertos, "
           "sino de preguntas o ramas que nadie ha medido.\n"
           f"- **Camino mínimo hacia la meta:** {len(camino)} cierres llevan de {base:.1f} % a {actual:.1f} %"
           + (" (meta alcanzada)." if actual >= meta - 1e-9 else f" y ahí se agota: la meta de {meta:.1f} % **no es alcanzable** cerrando nodos abiertos.") + "\n"
           f"- {solos} nodos abiertos **no suben el total por sí solos** (otro nodo más débil los sujeta). "
           "Por eso el orden importa.\n\n"
           "## Camino voraz (cada paso, el cierre que más sube con lo anterior ya hecho)\n\n"
           + tab([[i + 1, n, " + ".join(NODOS[k]["tipo"] for k in n.split(" + ")),
                   " + ".join(NODOS[k]["e"] for k in n.split(" + ")), f"+{g:.2f}", f"{t:.1f} %",
                   " · ".join(_accion(k, NODOS, D) for k in n.split(" + "))]
                  for i, (n, g, t) in enumerate(camino)],
                 ["#", "nodo", "tipo", "estatus", "gana", "acumulado", "qué lo cierra"])
           + "\n## Ranking individual (cada nodo cerrado solo)\n\n"
           + tab([fila(n, g) for n, g in rank], ["nodo", "tipo", "estatus", "gana solo", "qué lo cierra"]))
    (ROOT / "RUMBO.md").write_text(doc)
    sim = lambda nodos: simular(D, NODOS, RANK, SCORE, COMP, nodos)
    return {"base": base, "techo": techo, "camino": camino, "meta": meta, "final": actual, "gan": gan, "simular": sim}
