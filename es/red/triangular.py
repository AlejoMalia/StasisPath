"""StasisPath: triangulación de incógnitas. El marco proyecta rangos para lo que no ha medido.

Idea (del usuario): en vez de decir «no lo sabemos», recorrer **todos los caminos
independientes** de la red que acotan una incógnita, calcular el rango de cada uno y
quedarse con la **intersección**. El resultado no es un número exacto: es un rango
proyectado que después se afina midiendo.

Lo más útil no es la intersección: es la **contradicción**. Si dos caminos independientes
dan rangos incompatibles, una de las leyes que los alimenta está mal, y el marco lo dice.

Cada camino declara: de qué leyes/fuentes sale, qué tipo de cota impone (mínimo, máximo o
rango) y su valor. Un camino que dependa de otro NO es independiente y se marca.
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA, YELLOW, RED = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#c0392b"

def g(x):
    if x is None or x != x: return "—"
    if x == float("inf"): return "∞"
    if x == float("-inf"): return "−∞"
    return f"{x:.3g}" if abs(x) < 1e4 else f"{x:,.0f}"

def tabla(f, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in r) + " |" for r in f) + "\n"


def _rango(c):
    """Convierte un camino en (lo, hi)."""
    t = c["tipo"]
    if t == "rango": return (c["lo"], c["hi"])
    if t == "min":   return (c["v"], float("inf"))
    if t == "max":   return (float("-inf"), c["v"])
    return (c["v"], c["v"])


def generar(D, PAR, DERIV, ROOT):
    p = {k: v["v"] for k, v in PAR.items()}
    INC = incognitas(p, DERIV)
    out, resumen = [], []

    for iid, inc in INC.items():
        cams = inc["caminos"]
        indep = [c for c in cams if c.get("indep", True) and not c.get("regimen")]
        otros_reg = [c for c in cams if c.get("regimen")]
        # intersección sólo de los caminos independientes
        lo = max((_rango(c)[0] for c in indep), default=float("-inf"))
        hi = min((_rango(c)[1] for c in indep), default=float("inf"))
        vacio = lo > hi
        # ¿qué par se contradice?
        choque = None
        if vacio:
            for i, a in enumerate(indep):
                for b in indep[i + 1:]:
                    la, ha = _rango(a); lb, hb = _rango(b)
                    if la > hb or lb > ha: choque = (a["via"], b["via"]); break
                if choque: break
        filas = [[c["via"], "sí" if c.get("indep", True) else "**no**",
                  {"min": "≥", "max": "≤", "rango": "∈", "punto": "="}[c["tipo"]],
                  g(_rango(c)[0]) if c["tipo"] != "max" else "",
                  g(_rango(c)[1]) if c["tipo"] != "min" else "",
                  c["de"]] for c in cams]
        cuerpo = (f"**{inc['desc']}**\n\n" + tabla(filas, ["camino", "¿independiente?", "", "mín", "máx", "de qué sale"]))
        for c in otros_reg:
            cuerpo += (f"\n> **Régimen aparte — «{c['via']}» ({c['regimen']}).** No entra en la intersección: "
                       f"no contradice a los demás, describe **otro sistema físico**. Acota {'≥' if c['tipo']=='min' else '≤'} "
                       f"{g(_rango(c)[0] if c['tipo']=='min' else _rango(c)[1])} {inc['u']}.\n")
        if vacio:
            cuerpo += (f"\n> ⚠ **CONTRADICCIÓN: la intersección es vacía.** Los caminos «{choque[0]}» y «{choque[1]}» "
                       "son incompatibles. **Eso no es un fallo del método: es el resultado.** Una de las leyes que los "
                       "alimenta está mal, y la incógnita no puede proyectarse hasta resolverlo.\n")
            if inc.get("nota_choque"): cuerpo += "\n" + inc["nota_choque"] + "\n"
            resumen.append([iid, inc["desc"][:52], "**contradicción**", "—", f"{choque[0]} vs {choque[1]}"])
        else:
            ancho = (hi / lo) if (lo > 0 and hi < float("inf")) else float("inf")
            cuerpo += (f"\n> **RANGO PROYECTADO: {g(lo)} – {g(hi)} {inc['u']}** "
                       f"({len(indep)} caminos independientes"
                       + (f", factor ×{g(ancho)} de anchura" if ancho != float("inf") else ", sin acotar por un lado") + ").\n")
            if inc.get("afinar"): cuerpo += f"\n**Cómo afinarlo a un número:** {inc['afinar']}\n"
            resumen.append([iid, inc["desc"][:52], f"{g(lo)} – {g(hi)} {inc['u']}",
                            f"×{g(ancho)}" if ancho != float("inf") else "abierto", f"{len(indep)} caminos"])
        out.append((iid, inc["titulo"], cuerpo))

    # ---- figura
    proy = [(iid, inc, max((_rango(c)[0] for c in inc["caminos"] if c.get("indep", True)), default=float("-inf")),
             min((_rango(c)[1] for c in inc["caminos"] if c.get("indep", True)), default=float("inf")))
            for iid, inc in INC.items()]
    proy = [x for x in proy if x[2] <= x[3] and x[2] > 0 and x[3] < float("inf")]
    fig, ax = plt.subplots(figsize=(8.4, 0.62 * len(proy) + 1.6))
    for y, (iid, inc, lo, hi) in enumerate(proy):
        for c in inc["caminos"]:
            cl, ch = _rango(c)
            cl = max(cl, lo / 8 if lo > 0 else cl); ch = min(ch, hi * 8 if hi < float("inf") else ch)
            ax.plot([cl, ch], [y + 0.22, y + 0.22], color=GRID, lw=5, solid_capstyle="butt", zorder=1)
        ax.plot([lo, hi], [y, y], color=BLUE, lw=9, solid_capstyle="butt", zorder=3)
        ax.text(hi, y, f"  {g(lo)}–{g(hi)}", va="center", fontsize=8, color=INK2)
    ax.set_yticks(range(len(proy))); ax.set_yticklabels([f"{i} · {inc['desc'][:44]}" for i, inc, _, _ in proy], fontsize=7.5, color=INK2)
    ax.set_xscale("log"); ax.set_xlabel("rango proyectado (escala log) — gris: cada camino · azul: intersección")
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
    ax.grid(axis="x", color=GRID, lw=0.6); ax.grid(axis="y", visible=False)
    ax.set_facecolor(SURF); fig.set_facecolor(SURF)
    fig.suptitle("Triangulación: lo que el marco puede proyectar sin medirlo", x=0.02, ha="left", fontsize=11, color=INK)
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "T_triangulacion.png", dpi=150); plt.close(fig)

    doc = ("<!-- AUTO-GENERADO por red/triangular.py. NO EDITAR A MANO. -->\n"
           "# StasisPath: triangulación de incógnitas\n\n"
           "Para cada dato que **no tenemos**, se recorren todos los caminos independientes de la red que lo acotan "
           "y se toma la **intersección**. No da el número exacto: da el **rango proyectado**, que después se afina midiendo.\n\n"
           "**Lo más útil no es la intersección, es la contradicción.** Si dos caminos independientes dan rangos "
           "incompatibles, una de las leyes que los alimenta está mal — y eso es un resultado, no un fallo.\n\n"
           "![Triangulación](red/fig/T_triangulacion.png)\n\n"
           + tabla(resumen, ["id", "incógnita", "rango proyectado", "anchura", "nota"]) + "\n")
    for iid, tit, cuerpo in out:
        doc += f"## {iid} · {tit}\n\n{cuerpo}\n"
    (ROOT / "TRIANGULACION.md").write_text(doc)
    return resumen


def incognitas(p, DERIV):
    """Cada incógnita con sus caminos. `indep: False` marca un camino que reusa otro."""
    Mtox = DERIV["M_toxico"]; Mde = DERIV["M_de_CCR"]; tasa = DERIV["tasa_conv"]; LCe = DERIV["LC_esfera"]
    I = {}

    # ---- I1: daño de P19 (brazo frío) -------------------------------------
    I["I1"] = dict(titulo="Daño del brazo frío de P19 (M22 9.3 M a −22 °C)",
        desc="Daño relativo (1 − respiración/control) al cargar 9.3 M a −22 °C", u="",
        afirmar=None, u2="",
        nota_choque=("**PERO la contradicción NO afecta al veredicto de P19, y eso se puede demostrar.** "
            "German midió en el **mismo brazo** daño respiratorio **0.220** (a 8.42 M) y LTP **138.1 %**, que **pasa** nuestro "
            "umbral preregistrado de 130 %. ⇒ Hay un nivel de daño con **LTP demostradamente conservada: 0.220**. "
            "Los dos caminos que chocan predicen **0.142 y ≤0.07**, y **ambos quedan por debajo de 0.220**. "
            "**La contradicción es sobre CUÁNTO daño habrá, no sobre si P19 pasa: los dos caminos predicen PASA.**\n\n"
            "**Y sigue siendo el mejor argumento para ejecutarlo.** Los dos caminos no son opinables: "
            "el de Arrhenius extrapola desde 23–37 °C hasta −22 °C, una extrapolación grande y **sin el término osmótico de L20**; "
            "el de Fahy es una medida real de M22 a −22 °C, pero **en loncha renal, no neural**. ⇒ El experimento no sólo mide "
            "un número: **discrimina entre dos leyes del propio marco**. Si sale ≈0.14, la extrapolación de Arrhenius vale y el "
            "resultado de Fahy no transfiere del riñón al cerebro. Si sale ≤0.07, la toxicidad a baja temperatura cae más rápido "
            "de lo que predice Arrhenius, y **L20 tenía razón: el daño dominante en frío es osmótico, no químico**."),
        afinar="es exactamente lo que mide P19.",
        caminos=[
            dict(via="Arrhenius desde ovocitos × punto medido de German", tipo="punto", v=0.142,
                 de="F72 (9.28 M a 10 °C → 0.536) escalado por Ea/R = 2952 K de F55", indep=True),
            dict(via="Anclas de Fahy: M22 es tolerable a −22 °C en loncha renal", tipo="max", v=0.07,
                 de="F65/F39 + banda sin daño K⁺/Na⁺ ≥ 93 % (G4b)", indep=True),
            dict(via="Calibración daño↔LTP: a daño 0.220 la LTP SÍ se conservó", tipo="max", v=0.220,
                 de="F72: German midió en el MISMO brazo daño respiratorio 0.220 (8.42 M) y LTP 138.1 % (control 157.7, n.s.)", indep=True),
            dict(via="Cota inferior: no puede ser mejor que el control sin CPA", tipo="min", v=0.0,
                 de="definición", indep=True),
        ])
    I["I1"]["u"] = ""

    # ---- I2: CCR de los NADES ---------------------------------------------
    I["I2"] = dict(titulo="CCR de los disolventes eutécticos naturales (NADES)",
        desc="Velocidad crítica de enfriamiento de los NADES", u="°C/min",
        afinar="YA NO HACE FALTA: la calorimetría estaba publicada en F80 y se leyó en la tanda 46. **CCR > 30 °C/min ⇒ la predicción I2 (0.3 °C/min) queda REFUTADA por su propio criterio (refutada si > 0.426).**",
        caminos=[
            dict(via="Vitrifican por inmersión directa en N₂ líquido", tipo="max", v=1e4,
                 de="F80: si vitrifican al sumergir una muestra pequeña, su CCR no supera la tasa de inmersión (~10⁴ °C/min)", indep=True),
            dict(via="No son agua pura: su CCR está por debajo de la del agua", tipo="max", v=3.84e8,
                 de="F76 (agua pura: 3.84 × 10⁸ °C/min)", indep=True),
            dict(via="**MEDIDO (F80, tanda 46): cristalizan en DSC enfriando a 30 °C/min**", tipo="min", v=30.0,
                 de="F80 Tabla 2: Tc onset −26.6 a −32.3 °C al 50 % p/v ⇒ CCR > 30 °C/min", indep=True),
        ])

    # ---- I3: masa máxima de órgano humano vitrificable ---------------------
    lc_f2 = DERIV["LC_viable"]; m_f2 = DERIV["masa_viable"] * 1000
    I["I3"] = dict(titulo="Masa máxima de tejido humano vitrificable con la química actual",
        desc="Masa máxima vitrificable sin cruzar el umbral tóxico", u="g",
        afinar="midiendo la CCR de un CPA a concentración baja. Si existe, el límite sube; si no, se confirma.",
        caminos=[
            dict(via="F2: donde la molaridad exigida cruza el umbral tóxico", tipo="max", v=m_f2,
                 de="C3 + recta CCR↔M + umbral 9.28 M de F72", indep=True),
            dict(via="Demostrado físicamente: 3 L de M22 vitrificados", tipo="min", v=3000.0,
                 de="F2 (vidrio físico a escala de litros, sin biología)", indep=True),
            dict(via="Demostrado con función: riñón de conejo de 13.9 g trasplantado", tipo="min", v=13.9,
                 de="F50 (dieléctrico, función clínica normal)", indep=False),
        ])

    # ---- I4: τ_eq humano con reperfusión óptima ----------------------------
    I["I4"] = dict(titulo="τ_eq humano alcanzable con reperfusión óptima",
        desc="Isquemia equivalente a 37 °C que un humano podría tolerar con la mejor reperfusión", u="min",
        afinar="un ensayo de reperfusión optimizada en cerdo, que es el modelo más cercano y ya se usa (F42).",
        caminos=[
            dict(via="Invariancia entre especies: el perro aguanta 17 min", tipo="min", v=12.5,
                 de="F25/F25b + T1 del módulo de escalado (τ_eq invariante, error ×1.9)", indep=True),
            dict(via="Existencia en otro mamífero: gata, 1 h sólo cerebro", tipo="max", v=60.0,
                 de="F38 — cota superior: nadie ha superado esto en organismo", indep=True),
            dict(via="Límite celular: BrainEx recupera células a 4 h", tipo="max", v=240.0,
                 de="F23 — techo absoluto; por encima ni la célula vuelve", indep=False),
        ])

    # ---- I5: duración de sobreenfriamiento a escala de hígado --------------
    I["I5"] = dict(titulo="Duración de sobreenfriamiento de un hígado humano a −2 °C",
        desc="Horas de sobreenfriamiento a −2 °C para 1.5 L antes de nuclear", u="h",
        afinar="sobreenfriar dos volúmenes distintos a la misma temperatura y ver si el tiempo escala como 1/V. **Experimento barato y decisivo para L16.** El contraste isobárico/isocórico da además una medida directa de cuánto suprime la nucleación el confinamiento a volumen constante.",
        caminos=[
            dict(via="Tasa de Poisson AJUSTADA con el hígado de rata (2 puntos, −6 °C)", tipo="max", v=-math.log(0.5)/(0.567*1.5),
                 de="F85: 100 % a 72 h y 58 % a 96 h ⇒ J(−6 °C) ≈ 0.57 /L·h; aquí se da el tiempo con 50 % de éxito", indep=True),
            dict(via="Invariante V·t desde el riñón de cerdo (isobárico)", tipo="max", v=0.2 * 5.0 / 1.5,
                 de="F20 (0.2 L × 5 h a −2 °C) suponiendo nucleación tipo Poisson (F4 de FORMULACION)", indep=True),
            dict(via="Medido a −2 °C en hígado de cerdo isocórico", tipo="min", v=24.0,
                 de="F22 (1.5 L, 24–48 h sin congelarse, en sistema isocórico)", indep=True,
                 regimen="isocórico: el volumen constante genera presión al nuclear y **suprime la nucleación**"),
        ])
    return I
