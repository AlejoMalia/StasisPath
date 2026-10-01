"""StasisPath: confianza de cada veredicto — de «margen» a PORCENTAJE.

MARGENES.md dice a qué distancia está el vuelco de cada veredicto, pero no con qué probabilidad
ocurre. Aquí cada rango declarado se lee como un intervalo del 95 % (así se declaró Q10, IC 95 %
de n = 37) y se convierte en una distribución normal partida en escala logarítmica: respeta la
asimetría del rango y no inventa dispersión donde el rango es un punto. Con eso:

  1. P(error) de cada veredicto que hoy se cumple, con todos sus parámetros variando a la vez.
  2. Qué parámetro concentra ese riesgo (P(error) si ese parámetro se conociera exactamente).
  3. Qué precisión haría falta medir para bajar P(error) del objetivo (1 en 100).

Límites declarados, no ocultos:
  - Leer el rango como ±1.96 σ es una SUPOSICIÓN: muchos rangos son cotas o esquinas, no IC. Por eso
    se da también la columna pesimista (rango = ±1 σ). La verdad está, como mucho, entre las dos.
  - Parámetros independientes; no hay correlaciones declaradas en el YAML.
  - Este módulo NO cambia valores, rangos, umbrales ni el progreso. Sólo mide y prioriza (R2, R5).
  - La semilla es fija para que el documento sea reproducible.

Salida: CONFIANZA.md + red/fig/K_confianza.png. Lo llama motor.py.
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
ORANGE, YELLOW, AQUA = "#eb6834", "#eda100", "#1baf7a"

N = 20000            # muestras por cota
SEMILLA = 20260926
OBJETIVO = 0.01      # P(error) aceptable: 1 en 100. Fijado antes de ver resultados; no se ajusta.
K95, K1 = 1.96, 1.0  # rango leído como ±1.96 σ (principal) o ±1 σ (pesimista)

def g(x):
    return f"{x:.3g}"

def pct(p):
    if p == 0: return "0 %"
    return f"{100 * p:.2g} %" if p < 1e-3 else f"{100 * p:.3g} %"

def tabla(filas, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in f) + " |" for f in filas) + "\n"

def _sigmas(pv, K):
    """σ hacia arriba y hacia abajo (log si el parámetro es positivo, lineal si no)."""
    v, (lo, hi) = pv["v"], pv["r"]
    if lo > 0 and v > 0:
        return "log", math.log(hi / v) / K, math.log(v / lo) / K
    return "lin", (hi - v) / K, (v - lo) / K

def _muestra(pv, z, K, escala=1.0):
    modo, su, sd = _sigmas(pv, K)
    s = np.where(z > 0, su, sd) * escala
    return pv["v"] * np.exp(z * s) if modo == "log" else pv["v"] + z * s

def _media_err(pv, K, escala=1.0):
    """Semiancho al 95 % equivalente, en % del central (el lado más ancho)."""
    modo, su, sd = _sigmas(pv, K)
    s = max(su, sd) * escala * K95
    return (math.exp(s) - 1) * 100 if modo == "log" else (s / abs(pv["v"]) * 100 if pv["v"] else float("inf"))

def _rango(pv, a):
    """Rango declarado estrechado por el factor a alrededor del central (en la misma escala que el muestreo)."""
    v, (lo, hi) = pv["v"], pv["r"]
    if lo > 0 and v > 0:
        return v * (lo / v) ** a, v * (hi / v) ** a
    return v - a * (v - lo), v + a * (hi - v)

def _wilson_sup(k, n, z=1.96):
    p = k / n
    c = (p + z * z / (2 * n) + z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / (1 + z * z / n)
    return min(1.0, c)

def generar(D, PAR, COTAS, ROOT):
    rng = np.random.default_rng(SEMILLA)
    base = {k: v["v"] for k, v in PAR.items()}
    filas_v, prioridad, prioridad1 = [], {}, {}

    for cid, cdef in D["cotas"].items():
        f = COTAS[cid]
        _, v0 = f(base)
        vivos = [t for t, (ok, _) in v0.items() if ok]
        if not vivos:
            continue
        deps = [d for d in cdef["deps"] if PAR[d]["r"][0] != PAR[d]["r"][1]]
        Z = rng.standard_normal((N, len(deps)))

        def fallos(K, fijo=None, escala=None):
            cols = {}
            for j, d in enumerate(deps):
                e = escala if (escala is not None and d == fijo) else 1.0
                zz = np.zeros(N) if (d == fijo and escala is None) else Z[:, j]
                cols[d] = _muestra(PAR[d], zz, K, e)
            cuenta = {t: 0 for t in vivos}
            for i in range(N):
                q = dict(base)
                for d in deps: q[d] = float(cols[d][i])
                _, vt = f(q)
                for t in vivos:
                    if not vt[t][0]: cuenta[t] += 1
            return cuenta

        c95, c1 = fallos(K95), fallos(K1)
        sin = {d: fallos(K95, fijo=d) for d in deps}   # P(error) si d se conociera exactamente
        sin1 = {d: fallos(K1, fijo=d) for d in deps}   # lo mismo en la lectura pesimista

        def precision(t, K, p, sinK):
            """Parámetro dominante y precisión que baja P(error) del objetivo en la lectura K."""
            dom, p_dom = None, p
            for d in deps:
                pd = sinK[d][t] / N
                if pd < p_dom: dom, p_dom = d, pd
            if p <= OBJETIVO: return dom, p_dom, "ya cumple"
            if dom is None: return dom, p_dom, "ningún parámetro lo explica solo"
            if p_dom > OBJETIVO: return dom, p_dom, f"no basta con {dom}: aun exacto queda {pct(p_dom)}"
            a, b = 0.0, 1.0          # escala de σ de dom: a cumple, b no
            for _ in range(10):
                m = (a + b) / 2
                if fallos(K, fijo=dom, escala=m)[t] / N <= OBJETIVO: a = m
                else: b = m
            # expresado como el RANGO nuevo que habría que medir: vale igual en las dos lecturas
            lo, hi = _rango(PAR[dom], a)
            return dom, p_dom, f"{dom}: de [{g(PAR[dom]['r'][0])}, {g(PAR[dom]['r'][1])}] a [{g(lo)}, {g(hi)}] ({100 * a:.0f} % del ancho)"

        for t in vivos:
            clave = v0[t][1]
            p95, p1 = c95[t] / N, c1[t] / N
            dom, p_dom, req = precision(t, K95, p95, sin)
            dom1, p_dom1, req1 = precision(t, K1, p1, sin1)
            if clave:
                for d in deps:
                    prioridad[d] = prioridad.get(d, 0.0) + (p95 - sin[d][t] / N)
                    prioridad1[d] = prioridad1.get(d, 0.0) + (p1 - sin1[d][t] / N)
            if p95 == 0 and p1 == 0: nivel = "firme"
            elif p95 <= OBJETIVO:     nivel = "confiable"
            elif p95 <= 0.05:         nivel = "**vigilar**"
            else:                     nivel = "**en riesgo**"
            filas_v.append({"cid": cid, "t": t, "clave": clave, "p95": p95, "p1": p1,
                            "sup": _wilson_sup(c95[t], N), "dom": dom, "p_dom": p_dom,
                            "req": req, "dom1": dom1, "req1": req1, "nivel": nivel})

    filas_v.sort(key=lambda r: (-r["p95"], -r["p1"], not r["clave"]))
    claves = [r for r in filas_v if r["clave"]]
    # probabilidad de que falle al menos un veredicto clave (con independencia entre cotas)
    p_alguna = 1 - math.prod(1 - r["p95"] for r in claves)
    p_alguna1 = 1 - math.prod(1 - r["p1"] for r in claves)

    # ---------------------------------------------------------------- figura
    pts = [r for r in filas_v if r["p95"] > 0 or r["p1"] > 0]
    fig, ax = plt.subplots(figsize=(8.8, 0.42 * max(len(pts), 1) + 1.7))
    piso = 1e-4
    for y, r in enumerate(reversed(pts)):
        c = ORANGE if r["p95"] > 0.05 else (YELLOW if r["p95"] > OBJETIVO else AQUA)
        ax.plot([max(r["p95"], piso), max(r["p1"], piso)], [y, y], color=GRID, lw=2, zorder=1)
        ax.scatter([max(r["p95"], piso)], [y], s=46, color=c, zorder=3, edgecolor=SURF, linewidth=1.5)
        ax.scatter([max(r["p1"], piso)], [y], s=30, facecolor=SURF, edgecolor=c, linewidth=1.5, zorder=3)
        ax.text(max(r["p1"], r["p95"], piso) * 1.25, y, f"{pct(r['p95'])} · pes. {pct(r['p1'])}", va="center", fontsize=7.5, color=INK2)
    ax.axvline(OBJETIVO, color="#c0392b", lw=1.1)
    ax.text(OBJETIVO * 1.05, len(pts) - 0.4, " objetivo 1 %", fontsize=7, color="#c0392b")
    ax.set_yticks(range(len(pts)))
    ax.set_yticklabels([f"{r['cid']}{'' if r['clave'] else ' (no clave)'}: {r['t'][:46]}" for r in reversed(pts)],
                       fontsize=7.2, color=INK2)
    ax.set_xscale("log"); ax.set_xlim(piso * 0.7, 4)
    ax.set_xlabel("P(el veredicto es falso) · ● rango = IC 95 %   ○ pesimista: rango = ±1 σ", color=INK2)
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
    ax.grid(axis="x", color=GRID, lw=0.6); ax.set_facecolor(SURF); fig.set_facecolor(SURF)
    fig.suptitle("Confianza del marco: probabilidad de que cada veredicto se dé la vuelta",
                 x=0.02, ha="left", fontsize=11, color=INK)
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "K_confianza.png", dpi=150); plt.close(fig)

    # ---------------------------------------------------------------- documento
    niveles = {n: sum(1 for r in filas_v if r["nivel"] == n) for n in ("firme", "confiable", "**vigilar**", "**en riesgo**")}
    filas_md = [[r["cid"], r["t"], "sí" if r["clave"] else "no", f"{pct(r['p95'])} (≤ {pct(r['sup'])})", pct(r["p1"]),
                 r["req"], r["req1"], r["nivel"]] for r in filas_v]

    def orden(pr):
        pr = sorted(((d, x) for d, x in pr.items() if x > 1e-12), key=lambda t: -t[1])
        tot = sum(x for _, x in pr) or 1.0
        return [(d, x / tot) for d, x in pr if x / tot >= 0.005]   # < 0.5 % del riesgo: no se lista
    prio, prio1 = orden(prioridad), orden(prioridad1)
    filas_prio = [[i + 1, d, PAR[d].get("f") or "—", PAR[d]["e"], f"[{g(PAR[d]['r'][0])}, {g(PAR[d]['r'][1])}]",
                   f"{100 * x:.0f} %"] for i, (d, x) in enumerate(prio1)]
    riesgo = [r for r in filas_v if r["p95"] > OBJETIVO]
    riesgo1 = [r for r in claves if r["p1"] > OBJETIVO]

    doc = ("<!-- AUTO-GENERADO por red/confianza.py. NO EDITAR A MANO. -->\n"
           "# StasisPath: confianza — cuánto puede fallar cada veredicto, en porcentaje\n\n"
           "**Qué añade a MARGENES.md:** allí se mide a qué distancia está el vuelco de un veredicto moviendo **un** parámetro. "
           "Aquí se mueven **todos a la vez**, cada uno según su rango declarado, y se cuenta **con qué probabilidad el veredicto se da la vuelta**. "
           f"{N:,} muestras por cota, semilla fija (el documento es reproducible).\n\n"
           "**Cómo se lee cada rango.** Principal: el rango es un intervalo del 95 % (normal partida en escala log, respeta la asimetría). "
           "Es una suposición, porque varios rangos son cotas o esquinas y no IC; por eso se da también la lectura **pesimista**, que toma el rango como ±1 σ. "
           "**La probabilidad real queda entre las dos.** Los parámetros con rango puntual no varían, y no hay correlaciones declaradas.\n\n"
           "> **Este módulo no toca el marco.** No cambia valores, rangos, umbrales ni el progreso: mide y prioriza. "
           "Si una probabilidad es alta, la respuesta es **medir el parámetro indicado con el rango indicado**, no mover el umbral (R2). "
           f"El objetivo del {pct(OBJETIVO)} se fijó antes de ver resultados.\n\n"
           "![Confianza](red/fig/K_confianza.png)\n\n"
           f"**Resumen: {niveles['firme']} firmes (0 % incluso en la lectura pesimista) · {niveles['confiable']} confiables (≤ 1 %) · "
           f"{niveles['**vigilar**']} a vigilar (1–5 %) · {niveles['**en riesgo**']} en riesgo (> 5 %).**\n\n"
           f"**Probabilidad de que falle al menos un veredicto CLAVE: {pct(p_alguna)} en la lectura principal y {pct(p_alguna1)} en la pesimista** "
           "(suponiendo cotas independientes). Los veredictos que pueden fallar con más de un 1 % en la lectura principal son todos **no clave**.\n\n"
           + tabla(filas_md, ["cota", "veredicto", "¿clave?", "P(error) (IC 95 % sup.)", "P(error) pesimista",
                              "qué rango bajaría P(error) a ≤ 1 %", "ídem, lectura pesimista", "nivel"]))
    if riesgo or riesgo1:
        doc += "\n## Qué medir y con qué precisión\n\n"
        if riesgo1:
            doc += ("**Veredictos clave que superan el 1 % en la lectura pesimista** (en la principal están en 0 %):\n\n" +
                    "\n".join(f"- **{r['cid']}** — «{r['t']}»: {pct(r['p1'])} ⇒ {r['req1']}." for r in riesgo1) + "\n\n")
        if riesgo:
            doc += ("**Veredictos no clave por encima del 1 % en la lectura principal:**\n\n" +
                    "\n".join(f"- **{r['cid']}** — «{r['t']}»: {pct(r['p95'])} (pesimista {pct(r['p1'])}) ⇒ {r['req']}."
                               for r in riesgo) + "\n")
    doc += ("\n## Qué medición reduce más el riesgo total de los veredictos clave\n\n"
            "Para cada parámetro, cuánto bajaría la suma de P(error) de los veredictos clave si se conociera exactamente, "
            "en la lectura pesimista (en la principal el riesgo clave ya es prácticamente nulo). "
            "**Es el orden de rentabilidad de medir, y se recalcula solo cada vez que cambia el YAML.**\n\n"
            + tabla(filas_prio, ["#", "parámetro", "fuente", "estatus", "rango declarado", "parte del riesgo clave que elimina"]))
    (ROOT / "CONFIANZA.md").write_text(doc)
    return {"filas": filas_v, "p_alguna": p_alguna, "p_alguna1": p_alguna1, "riesgo": riesgo,
            "riesgo1": riesgo1, "prio": prio, "prio1": prio1, "niveles": niveles}
