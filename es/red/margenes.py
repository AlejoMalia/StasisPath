"""StasisPath: análisis computacional de márgenes.

La pregunta: **¿cuánto tendría que equivocarse cada parámetro para que un veredicto se dé la vuelta?**
No es lo mismo una conclusión con margen ×1000 que una con margen ×1.2, aunque ambas figuren como
"M" en el marco. Aquí se mide, para cada veredicto de cada cota, el **factor de vuelco**: por cuánto
habría que multiplicar (o dividir) cada parámetro del que depende para que el veredicto deje de
cumplirse, manteniendo los demás en su valor central.

Salida: MARGENES.md + red/fig/M_margenes.png. Lo llama motor.py.
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"

def g(x):
    if x == float("inf"): return "∞"
    return f"{x:.3g}" if abs(x) < 1e4 else f"{x:,.0f}"

def tabla(filas, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in f) + " |" for f in filas) + "\n"

def generar(D, PAR, COTAS, ROOT):
    """COTAS: dict id -> función(p) que devuelve (salidas, {veredicto: (bool, clave)})."""
    base = {k: v["v"] for k, v in PAR.items()}
    filas, puntos = [], []

    for cid, cdef in D["cotas"].items():
        f = COTAS[cid]
        _, v0 = f(base)
        for texto, (ok0, clave) in v0.items():
            if not ok0:
                continue  # sólo se analizan veredictos que hoy se cumplen
            mejor_par, mejor_fac, direccion = None, float("inf"), ""
            for par in cdef["deps"]:
                # búsqueda binaria del factor multiplicativo que vuelca el veredicto
                for signo, etiq in ((+1, "×"), (-1, "÷")):
                    lo, hi = 1.0, 1.0
                    # expandir hasta encontrar vuelco o rendirse en ×10^6
                    for _ in range(60):
                        hi *= 1.15
                        q = dict(base); q[par] = base[par] * (hi if signo > 0 else 1 / hi)
                        try:
                            _, vt = f(q)
                        except Exception:
                            break
                        if not vt[texto][0]:
                            break
                        lo = hi
                    else:
                        continue
                    if hi > 1e6:
                        continue
                    q = dict(base); q[par] = base[par] * (hi if signo > 0 else 1 / hi)
                    try:
                        _, vt = f(q)
                    except Exception:
                        continue
                    if vt[texto][0]:
                        continue  # nunca volcó
                    # afinar
                    a, b = lo, hi
                    for _ in range(40):
                        mid = math.sqrt(a * b)
                        q = dict(base); q[par] = base[par] * (mid if signo > 0 else 1 / mid)
                        _, vm = f(q)
                        if vm[texto][0]: a = mid
                        else: b = mid
                    if b < mejor_fac:
                        mejor_fac, mejor_par, direccion = b, par, etiq
            # Normalizar contra la incertidumbre DECLARADA del parámetro: un vuelco a ×1.5 no es
            # frágil si el parámetro se conoce con ±10 %. Lo que importa es vuelco / error plausible.
            if mejor_par:
                lo_p, hi_p = PAR[mejor_par]["r"]; c_p = PAR[mejor_par]["v"]
                err_decl = max(hi_p / c_p, c_p / lo_p) if lo_p > 0 and c_p > 0 else 1.0
                holgura = mejor_fac / err_decl if err_decl > 0 else float("inf")
            else:
                err_decl, holgura = 1.0, float("inf")
            if mejor_fac == float("inf"):
                frag = "**estructural**"   # ningún parámetro lo vuelca: es cualitativo
            elif holgura < 1:   frag = "**DENTRO DEL ERROR**"
            elif holgura < 2:   frag = "**FRÁGIL**"
            elif holgura < 5:   frag = "ajustado"
            else:               frag = "holgado"
            filas.append([cid, texto, "sí" if clave else "no",
                          mejor_par or "—", f"{direccion}{g(mejor_fac)}" if mejor_par else "—",
                          f"±{g((err_decl - 1) * 100)} %" if mejor_par else "—",
                          g(holgura) if holgura != float("inf") else "∞", frag])
            if mejor_fac != float("inf"):
                puntos.append((f"{cid}: {texto[:44]}", holgura, clave))

    puntos.sort(key=lambda t: t[1])
    fig, ax = plt.subplots(figsize=(8.6, 0.38 * len(puntos) + 1.6))
    ys = range(len(puntos))
    for y, (lab, fac, clave) in zip(ys, puntos):
        c = ORANGE if fac < 2 else (YELLOW if fac < 5 else AQUA)
        ax.barh(y, fac, color=c, height=0.55, zorder=2)
        ax.text(fac * 1.12, y, f"×{g(fac)}", va="center", fontsize=7.5, color=INK2)
    ax.axvline(1, color="#c0392b", lw=1.2); ax.axvline(2, color=INK2, lw=1, ls="--")
    ax.text(1, len(puntos) - 0.3, " dentro del error declarado", fontsize=7, color="#c0392b")
    ax.set_yticks(list(ys)); ax.set_yticklabels([p[0] for p in puntos], fontsize=7.2, color=INK2)
    ax.set_xscale("log"); ax.set_xlabel("Holgura = factor de vuelco / error declarado del parámetro (< 1 = el error declarado ya lo tumba)")
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
    ax.grid(axis="y", visible=False); ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_facecolor(SURF); fig.set_facecolor(SURF)
    fig.suptitle("Márgenes del marco: qué conclusión se cae primero", x=0.02, ha="left", fontsize=11, color=INK)
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "M_margenes.png", dpi=150); plt.close(fig)

    fragiles = [f for f in filas if "FRÁGIL" in f[7] or "DENTRO" in f[7]]
    holgados = [f for f in filas if f[7] == "holgado"]
    estr = [f for f in filas if "estructural" in f[7]]
    doc = ("<!-- AUTO-GENERADO por red/margenes.py. NO EDITAR A MANO. -->\n"
           "# StasisPath: márgenes del marco\n\n"
           "**Qué mide:** para cada veredicto que hoy se cumple, por cuánto tendría que errar el parámetro **más sensible** "
           "para que el veredicto se diera la vuelta (los demás quedan en su valor central). Un veredicto con factor ×1.3 y otro "
           "con factor ×1000 figuran igual como «M» en el marco, pero **no valen lo mismo**: esto los separa.\n\n"
           "El factor de vuelco por sí solo engaña: ×1.5 no es poco si el parámetro se conoce al ±10 %. Por eso se normaliza contra "
           "la **incertidumbre declarada** del propio parámetro. **Holgura = factor de vuelco / error declarado.**\n\n"
           "- **DENTRO DEL ERROR** (holgura < 1): el rango que ya hemos declarado tumba el veredicto. Hay que medir mejor o rebajar la afirmación.\n"
           "- **FRÁGIL** (1–2): sobrevive por poco.\n"
           "- **ajustado** (2–5).\n"
           "- **holgado** (> 5): la conclusión no depende de la precisión del parámetro.\n"
           "- **estructural**: ningún parámetro lo vuelca ⇒ el veredicto es cualitativo, no numérico.\n\n"
           "![Márgenes](red/fig/M_margenes.png)\n\n"
           f"**Resumen: {len(fragiles)} frágiles · {len(filas) - len(fragiles) - len(holgados) - len(estr)} ajustados · "
           f"{len(holgados)} holgados · {len(estr)} estructurales.**\n\n"
           + tabla(filas, ["cota", "veredicto", "¿clave?", "parámetro más sensible", "factor de vuelco", "error declarado", "holgura", "margen"]))
    if fragiles:
        doc += ("\n## Lo frágil, en orden de prioridad de medición\n\n" +
                "\n".join(f"{i+1}. **{f[0]}** — «{f[1]}» se cae si **{f[3]}** erra {f[4]}; error ya declarado {f[5]} ⇒ holgura {f[6]}."
                          for i, f in enumerate(fragiles)) + "\n")
    (ROOT / "MARGENES.md").write_text(doc)
    return filas, fragiles
