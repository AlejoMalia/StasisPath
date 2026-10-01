"""StasisPath: formulación interna. El marco resolviéndose a sí mismo.

Compone leyes YA verificadas para producir enunciados cuantitativos que nadie midió
directamente. Cada fórmula declara: de qué leyes sale, su rango de validez, y una
predicción falsable. Las que no llegan a falsable se marcan como tales.

Regla (MATE): componer sólo leyes cerradas (M/V). Una fórmula que se apoya en un nodo
abierto se reporta como CONDICIONAL, no como derivada.
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"

def g(x):
    if x != x: return "—"
    if x == float("inf"): return "∞"
    return f"{x:.3g}" if abs(x) < 1e4 else f"{x:,.0f}"

def tabla(f, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in r) + " |" for r in f) + "\n"

def generar(D, PAR, ROOT):
    p = {k: v["v"] for k, v in PAR.items()}
    rng = {k: v["r"] for k, v in PAR.items()}
    F = []   # (id, título, cuerpo markdown, estatus)

    # ============================ F1. Masa máxima vitrificable por convección, por CPA
    # Compone C3 (tasa ∝ LC^−n anclada) con la CCR del CPA. LC de esfera de agua = r/3.
    rate = lambda LC, q=p: q["anc_rate"] * (q["anc_LC"] / LC) ** q["exp_LC"]
    LCstar = lambda CCR, q=p: q["anc_LC"] * (q["anc_rate"] / CCR) ** (1 / q["exp_LC"])
    masa_de_LC = lambda LC: 4 / 3 * math.pi * (3 * LC) ** 3        # g, esfera de agua
    CPAS = {"M22": (p["CCR_M22"], 9.3), "VS55 (tejido)": (p["CCR_VS55"], 8.4), "VMP": (p["CCR_VMP"], 8.4)}
    filas = []
    for nom, (ccr, M) in CPAS.items():
        lc = LCstar(ccr); m = masa_de_LC(lc)
        # esquinas
        lo = min(LCstar(ccr, {**p, "anc_LC": a, "anc_rate": r, "exp_LC": e})
                 for a in rng["anc_LC"] for r in rng["anc_rate"] for e in rng["exp_LC"])
        hi = max(LCstar(ccr, {**p, "anc_LC": a, "anc_rate": r, "exp_LC": e})
                 for a in rng["anc_LC"] for r in rng["anc_rate"] for e in rng["exp_LC"])
        filas.append([nom, g(ccr), g(M), f"{g(lc)} ({g(lo)}–{g(hi)})", f"{g(m)} ({g(masa_de_LC(lo))}–{g(masa_de_LC(hi))})"])
    F.append(("F1", "Masa máxima vitrificable por convección, por crioprotector",
        "**Deriva de:** C3 (enfriamiento ∝ LC⁻ⁿ, anclado en la bolsa de 3 L) + las CCR medidas.\n\n"
        "**Fórmula:** LC\\* = LC₀ · (tasa₀ / CCR)^(1/n) · y M\\* = (4/3)π(3·LC\\*)³ para una esfera acuosa.\n\n"
        + tabla(filas, ["CPA", "CCR °C/min", "M (mol/L)", "LC máx. (cm)", "masa máx. (g)"]) +
        "\n**Lectura:** con la convección sola, M22 llega a decenas de kg y VMP no pasa de unos gramos. "
        "Es el número que faltaba para decir «qué órgano cabe en qué química» sin tener que simular cada caso.", "derivada"))

    # ============================ F2. Teorema de viabilidad: ¿existe química para un órgano dado?
    # Compone F1 con la relación CCR↔concentración (3 puntos) y con el umbral de toxicidad (German).
    import statistics
    pts = [(9.3, p["CCR_M22"]), (8.4, p["CCR_VS55"]), (8.4, p["CCR_VMP"])]
    CCR_AGUA = 6.4e6 * 60      # °C/min — agua pura, medida en criomicroscopía electrónica (F76, L31)
    # log10(CCR) ~ a + b·M  (con 8.4 repetido a dos CCR: se promedia en log)
    agg = {}
    for M, c in pts: agg.setdefault(M, []).append(math.log10(c))
    xs = sorted(agg); ys = [statistics.mean(agg[x]) for x in xs]
    b = (ys[1] - ys[0]) / (xs[1] - xs[0]); a = ys[0] - b * xs[0]
    M_de_CCR = lambda CCR: (math.log10(CCR) - a) / b
    UMBRAL_TOX = 9.28          # M — por encima, el daño salta (German, F72)
    objetos = [("riñón humano", 0.88), ("corazón humano (~300 g)", 1.2), ("hígado humano (~1.5 kg)", 1.8),
               ("cerebro humano (1.4 kg)", 2.31), ("cuerpo entero (media)", 3.9), ("tronco", 7.5)]
    filas = []
    for nom, lc in objetos:
        ccr_req = rate(lc); M_req = M_de_CCR(ccr_req)
        veredicto = "**viable**" if M_req <= UMBRAL_TOX else "**exige C > umbral tóxico**"
        filas.append([nom, g(lc), g(ccr_req), g(M_req), veredicto])
    # Mismo cálculo que la capa `derivadas` del YAML (LC_viable / masa_viable): una sola definición.
    lc_critico = next((i / 100 for i in range(25, 2000) if M_de_CCR(rate(i / 100)) > UMBRAL_TOX), None)
    m_critico = masa_de_LC(lc_critico) if lc_critico else float("nan")
    F.append(("F2", "Teorema de viabilidad: ¿hay química posible para un órgano dado?",
        "**Deriva de:** F1 + la relación medida CCR↔concentración (3 CPA) + el umbral de toxicidad de German "
        f"({UMBRAL_TOX} M, donde la respiración basal cae a la mitad).\n\n"
        f"**Fórmula:** log₁₀(CCR) = {g(a)} + {g(b)}·M ⇒ para vitrificar una LC dada hace falta "
        "M ≥ (log₁₀(CCR_requerida) − a)/b. Si esa M supera el umbral tóxico, **ninguna química conocida sirve**.\n\n"
        + tabla(filas, ["objeto", "LC cm", "CCR requerida °C/min", "M requerida (mol/L)", "veredicto"]) +
        f"\n> **RESULTADO DERIVADO:** el límite está en **LC ≈ {g(lc_critico)} cm**, es decir una masa de "
        f"**≈ {g(m_critico/1000)} kg**. Por encima, la concentración que haría falta cruza el umbral donde la "
        "toxicidad se dispara. \n\n**Lo que dice la tabla leída con cuidado:** el cerebro humano exige **8.94 M**, por debajo del umbral, con un margen de sólo **0.34 M**. El cuerpo entero (LC media) exige **9.20 M**: margen de **0.08 M**, prácticamente nulo. **El tronco es el único que lo cruza** (9.53 M) — y es justamente la pieza que C3 ya señalaba como la que falla por la vía térmica pura. **La derivación reproduce ese resultado desde otra dirección**, lo que es una comprobación cruzada, no una coincidencia buscada.\n\n"
        f"**Validación con un tercer punto, de un campo lejano (L31):** la CCR del **agua pura** es {g(CCR_AGUA)} °C/min "
        f"(criomicroscopía electrónica). Con él, la relación se ve **curva**: −0.95 décadas/mol entre 0 y 8.4 M, pero "
        f"**−1.74 entre 8.4 y 9.3 M**. ⇒ **Extrapolar con la pendiente local cerca de 9 M, como hace F2, es lo correcto**, "
        "y ahora está justificado con evidencia en vez de por suposición.\n\n"
        + "**Aviso de honestidad:** la recta CCR↔M se ajusta con **tres puntos y sólo dos concentraciones distintas** "
        "(8.4 y 9.3 M). Es la pieza más débil de toda la derivación. El resultado debe leerse como **orden de magnitud**, "
        "no como una frontera precisa, y se refuta en cuanto se mida un CPA con CCR baja a concentración baja.\n\n"
        "**Y hay un campo vecino que dice que eso es posible (L29):** las proteínas CAHS del tardígrado forman vidrio o gel "
        "a **~0.6 mM**, cuatro órdenes de magnitud por debajo de los 8.4–9.3 M de M22 o V3. La relación CCR↔molaridad que "
        "sostiene F2 **no es una ley de la naturaleza: es una propiedad de la clase química que el campo eligió** (moléculas "
        "pequeñas). F2 sigue siendo válida **dentro de esa clase**, y ese es su rango de validez real.", "derivada débil, con rango de clase química"))

    # ============================ F3. τ_eq con tramos y dominios
    def tau_eq(T, t, dominio="mamifero"):
        if dominio == "hibernador" and T <= 12: return float("nan")   # L27: deja de ser función de T
        q = p["Q10"] if T >= 15 else p["Q10_frio"]
        return t * q ** ((T - 37) / 10)
    casos = [("DHCA humano 15 °C, 31 min", 15, 31, "mamifero"), ("Perro flush 10 °C, 120 min", 10, 120, "mamifero"),
             ("Cerdo 10 °C, 60 min", 10, 60, "mamifero"), ("Ardilla eutérmica 37 °C, 8 min", 37, 8, "hibernador"),
             ("Ardilla en torpor 5 °C", 5, 1440, "hibernador")]
    filas = [[nm, g(T), g(t), g(tau_eq(T, t, d)) if tau_eq(T, t, d) == tau_eq(T, t, d) else "**no aplica** (L27)"] for nm, T, t, d in casos]
    F.append(("F3", "τ_eq por tramos, con dominio declarado",
        "**Deriva de:** C2 + L2 (Q10 no constante) + L24 (mecanismo) + L27 (el hibernador es otro régimen).\n\n"
        f"**Fórmula:** τ_eq = t · Q10(T)^((T−37)/10), con **Q10 = {g(p['Q10'])} por encima de 15 °C** y "
        f"**{g(p['Q10_frio'])} por debajo**; y **no definida** para hibernadores por debajo de 12 °C, donde el metabolismo "
        "deja de ser función de la temperatura.\n\n" + tabla(filas, ["caso", "T °C", "t min", "τ_eq (min a 37 °C)"]) +
        "\n**Lo que aporta:** unifica en una sola expresión lo que estaba repartido en cuatro leyes, **y declara dónde no vale**. "
        "La casilla «no aplica» es tan importante como los números: es el error que cometeríamos si aplicáramos C2 a un hibernador frío.", "derivada"))

    # ============================ F4. Límite volumen × tiempo del sobreenfriamiento
    # L16: la nucleación es estocástica; su probabilidad crece con volumen y tiempo.
    # Anclas: 3 L a −2 °C fallaría a 24-48 h (por eso subieron a −0.5); riñón de cerdo ~0.2 L aguantó 5 h a −2 °C.
    V1, t1, T1 = 0.2, 5.0, -2.0      # L, h, °C  (riñón de cerdo, F20)
    V2, t2, T2 = 0.2, 48.0, -0.5     # tuvieron que subir T para 48 h
    prod1 = V1 * t1
    F.append(("F4", "Invariante volumen × tiempo del sobreenfriamiento",
        "**Deriva de:** L16 (la nucleación acumulada limita el tiempo, no la temperatura mínima) + G7 (banda de lesión por frío).\n\n"
        "**Forma propuesta:** si la nucleación es un proceso de Poisson con tasa por unidad de volumen J(T), "
        "la probabilidad de que NO nuclee es exp(−J(T)·V·t) ⇒ **el invariante es V·t a T fija**.\n\n"
        f"**Ancla única disponible:** riñón de cerdo, {g(V1)} L a {g(T1)} °C durante {g(t1)} h ⇒ V·t = {g(prod1)} L·h sin nuclear. "
        f"Para {g(t2)} h el mismo grupo tuvo que subir a {g(T2)} °C.\n\n"
        "> **PREDICCIÓN (no derivada del todo):** a −2 °C, un órgano de 1.5 L (hígado) sólo aguantaría "
        f"≈ {g(prod1/1.5)} h antes de igualar la dosis de nucleación que el riñón acumuló en 5 h.\n\n"
        "**Estatus honesto: NO es una derivación válida todavía.** Hay **un solo punto**: con un dato no se determina J(T) "
        "ni se comprueba que el invariante sea V·t. Se deja escrita **como hipótesis falsable** porque el experimento que la "
        "probaría es barato: sobreenfriar dos volúmenes distintos a la misma temperatura y ver si el tiempo hasta nuclear "
        "escala como 1/V.", "hipótesis, no derivada"))

    # ============================ F5. Protocolo de enfriamiento no monótono
    Tg = p["Tg"]
    F.append(("F5", "Protocolo de enfriamiento óptimo (no monótono)",
        "**Deriva de:** L14 (conflicto de velocidad) + G7 (banda 0–20 °C de lesión por frío) + G3 (Tg y perfil de "
        "recalentamiento) + F68 (bajar la velocidad entre almacenamiento y Tg reduce el estrés).\n\n"
        "**Regla derivada, en tres tramos:**\n"
        "1. **De 37 a 20 °C:** velocidad libre. No hay lesión por frío ni riesgo de hielo.\n"
        "2. **De 20 a 0 °C: lo más rápido posible.** Es la banda de transición de fase de los lípidos de membrana, "
        "donde el daño crece con el *tiempo de exposición* (G7). Excepción: si la vía es hielo extracelular controlado, "
        "aquí manda la deshidratación celular y hay que ir lento (0.1–1 °C/min) — **los dos objetivos son incompatibles "
        "en esta banda y hay que elegir vía antes de entrar en ella.**\n"
        f"3. **De 0 °C a Tg ({g(Tg)} °C):** por encima de la CCR del CPA, pero **no más rápido de lo necesario**: el exceso "
        "de velocidad sólo añade gradiente térmico.\n"
        f"4. **Por debajo de Tg:** lento (< 1 °C/min) y lejos de Tg en el almacenamiento, porque almacenar justo bajo Tg "
        "**duplica la CWR** que hará falta después (F2).\n\n"
        "**Lo que aporta:** es la única de estas fórmulas que es directamente **accionable en protocolo**, y sale de componer "
        "cuatro leyes que venían de cuatro campos distintos (reproducción humana, criobiología de órganos, materiales y "
        "neurociencia).", "derivada cualitativa"))

    # ---- figura de F2
    fig, ax = plt.subplots(figsize=(8, 4.6))
    LCs = [x / 50 for x in range(25, 500)]
    ax.plot(LCs, [M_de_CCR(rate(lc)) for lc in LCs], color=BLUE, lw=2, label="concentración necesaria para vitrificar")
    ax.axhline(UMBRAL_TOX, color=ORANGE, lw=2, ls="--", label=f"umbral de toxicidad medido ({UMBRAL_TOX} M)")
    if lc_critico: ax.axvline(lc_critico, color=MUTED, lw=1)
    for nom, lc in objetos:
        ax.scatter(lc, M_de_CCR(rate(lc)), s=55, c=INK, zorder=4)
        ax.annotate(nom, (lc, M_de_CCR(rate(lc))), xytext=(5, -10), textcoords="offset points", fontsize=7, color=INK2)
    ax.set_xlabel("Longitud característica LC (cm)"); ax.set_ylabel("Concentración de CPA necesaria (mol/L)")
    ax.set_ylim(7, 12); ax.set_title("F2 · Dónde la química necesaria cruza el umbral tóxico", loc="left", fontsize=11, color=INK)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.grid(color=GRID, lw=0.6); ax.set_facecolor(SURF); fig.set_facecolor(SURF)
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "F_viabilidad.png", dpi=150); plt.close(fig)

    doc = ("<!-- AUTO-GENERADO por red/formular.py. NO EDITAR A MANO. -->\n"
           "# StasisPath: formulación interna — el marco resolviéndose a sí mismo\n\n"
           "Cada fórmula compone leyes **ya cerradas** para producir un enunciado cuantitativo que nadie midió directamente. "
           "Se declara de qué sale, su rango de validez y si llega o no a predicción falsable. "
           "**Una fórmula apoyada en un nodo abierto se marca como condicional, no como derivada.**\n\n"
           "| fórmula | estatus |\n|---|---|\n" + "\n".join(f"| **{i} · {t}** | {st} |" for i, t, _, st in F) + "\n\n")
    for i, t, body, st in F:
        doc += f"## {i} · {t}\n\n*Estatus: {st}.*\n\n{body}\n\n"
        if i == "F2": doc += "![F2](red/fig/F_viabilidad.png)\n\n"
    doc += ("## Qué ha conseguido esta formulación\n\n"
            "- **Dos fórmulas nuevas y falsables** (F1, F2) que responden preguntas que antes exigían simular caso por caso.\n"
            "- **Una unificación** (F3): cuatro leyes en una expresión, con su dominio de validez declarado.\n"
            "- **Una regla de protocolo accionable** (F5), compuesta de cuatro campos distintos.\n"
            "- **Una hipótesis honestamente marcada como no derivada** (F4): con un solo punto no hay ley, y se dice.\n\n"
            "**Lo que NO consigue:** ninguna de estas fórmulas cierra X2. Derivar produce **predicciones**, no medidas. "
            "El marco puede ahora decir qué espera encontrar y dónde se rompería si se equivoca — que es exactamente "
            "lo que hace falta para que el experimento valga más.\n")
    (ROOT / "FORMULACION.md").write_text(doc)
    return dict(lc_critico=lc_critico, m_critico=m_critico, a=a, b=b, n_formulas=len(F))
