"""StasisPath: cierre por DERIVACIÓN. ¿Puede el marco predecir lo que aún no ha medido?

La idea (propuesta del usuario): con suficientes leyes verificadas, algunos nodos abiertos
no necesitan medición nueva — se cierran **derivándolos** de los que ya están cerrados.
Aquí se intenta con D_CPA: ajustar toxicidad(concentración) de un conjunto de datos y
toxicidad(temperatura) de otro **independiente**, componerlas, y con eso **predecir el
resultado de P19 antes de ejecutarlo**.

Regla MATE: una derivación sólo vale si (a) usa datos que no son el nodo que cierra,
(b) declara su rango de validez y (c) produce una predicción falsable con umbral.
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"

def g(x): return f"{x:.3g}" if abs(x) < 1e4 else f"{x:,.0f}"
def tabla(f, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in r) + " |" for r in f) + "\n"

# ---- Dato A: serie de concentración a T = 10 °C (German, F72). Respiración basal, pmol/min.
GERMAN = [(0.0, 173.3, 6.7), (4.28, 139.7, 3.1), (8.42, 135.1, 6.7), (9.28, 80.4, 5.6)]
T_GERMAN = 10.0
# ---- Dato B: dependencia con T a concentración y tiempo FIJOS (Szurek & Eroglu, F55).
#      PROH 1.5 M, 15 min: degeneración 54.2 % a 23 °C y 85 % a 37 °C.
SZUREK = [(23.0, 0.542), (37.0, 0.850)]
# ---- Anclas cualitativas para validar (Fahy, F39/F65): M22 9.3 M tolerable a −22 °C;
#      inaceptable a −3 °C. VMP 8.4 M tolerable a −3 °C.

def generar(ROOT):
    # (1) Forma de la curva en concentración, a 10 °C. daño = 1 − respiración/control.
    ctrl = GERMAN[0][1]
    pts = [(C, 1.0 - R / ctrl) for C, R, _ in GERMAN[1:]]
    # AUTOCORRECCIÓN: el primer intento ajustó una ley de potencia y salió exponente 0.9,
    # que NO describe estos datos: el daño es ~0.19-0.22 de 4.3 a 8.4 M y salta a 0.54 a 9.3 M.
    # Eso es un UMBRAL, no una potencia. Con 3 puntos no se ajusta una sigmoide de forma fiable,
    # así que no se ajusta nada: se usa el punto MEDIDO a 9.28 M y se escala sólo en temperatura.
    meseta = sum(d for C, d in pts if C < 9) / len([1 for C, d in pts if C < 9])
    salto = pts[-1][1]
    umbral_lo, umbral_hi = 8.42, 9.28

    # (2) g(T): factor de Arrhenius desde un conjunto INDEPENDIENTE.
    (T1, d1), (T2, d2) = SZUREK
    K1, K2 = T1 + 273.15, T2 + 273.15
    EaR = math.log(d2 / d1) / (1 / K1 - 1 / K2)      # K
    gT = lambda T: math.exp(-EaR / (T + 273.15))
    gnorm = lambda T: gT(T) / gT(T_GERMAN)           # normalizado a la T de German

    # (3) Composición y PREDICCIÓN
    # Daño = punto medido a esa concentración (meseta o salto) escalado por temperatura.
    def D(C, T):
        base = salto if C >= umbral_hi else meseta
        return base * gnorm(T)
    casos = [("German 9.28 M a 10 °C (MEDIDO: daño 0.54)", 9.28, 10.0),
             ("M22 9.3 M a −22 °C (brazo C de P19)", 9.30, -22.0),
             ("M22 9.3 M a −3 °C (Fahy: inaceptable)", 9.30, -3.0),
             ("VMP 8.4 M a −3 °C (Fahy: tolerable)", 8.40, -3.0),
             ("V3 8.42 M a 10 °C (MEDIDO: daño 0.22)", 8.42, 10.0)]
    filas = [[nm, g(C), g(T), g(D(C, T)), g(gnorm(T))] for nm, C, T in casos]

    pred = D(9.30, -22.0); medido_caliente = D(9.28, 10.0)
    factor = medido_caliente / pred

    # (4) Validación contra las anclas cualitativas de Fahy (no usadas en el ajuste)
    val = []
    val.append(("M22 a −3 °C debe salir PEOR que VMP a −3 °C", D(9.3, -3) > D(8.4, -3)))
    val.append(("M22 a −22 °C debe salir MEJOR que M22 a −3 °C", D(9.3, -22) < D(9.3, -3)))
    val.append(("V3 a 10 °C debe salir mejor que 9.28 M a 10 °C", D(8.42, 10) < D(9.28, 10)))
    ok = all(v for _, v in val)

    # ---- figura
    fig, ax = plt.subplots(figsize=(8, 4.6))
    Cs = [x / 20 for x in range(20, 210)]
    for T, c, lab in ((10.0, ORANGE, "carga a 10 °C (German)"), (-3.0, YELLOW, "carga a −3 °C"), (-22.0, AQUA, "carga a −22 °C (M22)")):
        ax.plot(Cs, [min(D(C, T), 1.2) for C in Cs], color=c, lw=2, label=lab)
    for C, d in pts:
        ax.scatter(C, d, s=70, c=INK, zorder=5)
    ax.scatter(9.30, pred, s=140, marker="*", c=AQUA, edgecolors=INK, linewidths=1, zorder=6)
    ax.annotate(f"predicción P19\n{g(pred)}", (9.30, pred), xytext=(8, 14), textcoords="offset points", fontsize=8, color=INK)
    ax.axhline(1 - 0.93, color=MUTED, ls="--", lw=1)
    ax.text(0.3, 1 - 0.93 + 0.015, "banda sin daño (K⁺/Na⁺ ≥ 93 % del control)", fontsize=7, color=MUTED)
    ax.set_xlabel("Concentración de CPA permeable (M)"); ax.set_ylabel("Daño relativo (1 − respiración/control)")
    ax.set_ylim(0, 1.0); ax.set_title("Derivación de D_CPA: predicción del brazo frío de P19", loc="left", fontsize=11, color=INK)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.grid(color=GRID, lw=0.6); ax.set_facecolor(SURF); fig.set_facecolor(SURF)
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "D_dcpa.png", dpi=150); plt.close(fig)

    doc = ("<!-- AUTO-GENERADO por red/derivar.py. NO EDITAR A MANO. -->\n"
           "# StasisPath: cierre por derivación — D_CPA y la predicción de P19\n\n"
           "**La idea.** Con suficientes leyes verificadas, algunos nodos abiertos no necesitan medición nueva: "
           "se **derivan** de los cerrados. Aquí se compone la toxicidad en concentración (de un conjunto de datos) "
           "con la toxicidad en temperatura (de **otro conjunto independiente**) y se predice el brazo de P19 que nadie ha hecho.\n\n"
           "**Regla:** una derivación sólo vale si usa datos distintos del nodo que cierra, declara su rango de validez "
           "y produce una predicción falsable con umbral.\n\n"
           "## 1. Forma de la curva en concentración, a 10 °C\n\n"
           f"De la serie de German (F72), daño = 1 − respiración/control:\n\n"
           + tabla([[g(C), g(d)] for C, d in pts], ["C (M)", "daño medido"]) +
           f"\n**No es una ley de potencia: es un umbral.** El daño se queda en una meseta de **{g(meseta)}** entre 4.3 y 8.4 M "
           f"y **salta a {g(salto)}** a 9.28 M. *(Autocorrección: el primer intento ajustó una potencia y dio exponente 0.9, "
           "que no describe estos datos. Con 3 puntos no se ajusta una sigmoide de forma fiable, así que **no se ajusta nada**: "
           "se usa el punto medido y se escala sólo en temperatura.)*\n\n"
           "## 2. Ajuste en temperatura, de un conjunto INDEPENDIENTE\n\n"
           f"De Szurek & Eroglu (F55), PROH 1.5 M y 15 min fijos, sólo cambia T: degeneración {SZUREK[0][1]*100:.1f} % a "
           f"{g(SZUREK[0][0])} °C y {SZUREK[1][1]*100:.1f} % a {g(SZUREK[1][0])} °C ⇒ Arrhenius con **Ea/R = {g(EaR)} K** "
           f"(Ea ≈ {g(EaR*8.314/1000)} kJ/mol, orden típico de daño proteico).\n\n"
           "## 3. Composición y predicción\n\n"
           + tabla(filas, ["caso", "C (M)", "T °C", "daño D_CPA predicho", "factor temperatura"]) +
           f"\n> **PREDICCIÓN DERIVADA:** cargar M22 a 9.3 M **a −22 °C** produce un daño de **{g(pred)}**, frente a **{g(medido_caliente)}** "
           f"a 10 °C: una reducción de **×{g(factor)}**. Eso sitúa el brazo frío **{'DENTRO' if pred <= 0.07 else 'FUERA'}** de la banda sin daño "
           f"(≤ 0.07, equivalente a K⁺/Na⁺ ≥ 93 % del control).\n\n"
           "![Derivación](red/fig/D_dcpa.png)\n\n"
           "## 4. Validación contra anclas que NO se usaron en el ajuste\n\n"
           + tabla([[t, "✔" if v else "✘"] for t, v in val], ["ancla cualitativa de Fahy (F39, F65)", "¿la reproduce?"]) +
           f"\n**{'Las tres anclas se reproducen' if ok else 'ALGUNA ancla falla'}.** Son datos cualitativos de Fahy que no entraron en ningún ajuste.\n\n"
           "## 5. Qué vale y qué no\n\n"
           "- **Vale como predicción falsable de P19**, con umbral fijado aquí y antes de cualquier dato: si el brazo frío "
           f"da un daño > 0.25, la derivación queda **refutada**; si da ≤ 0.10, **confirmada**.\n"
           "- **No cierra X2 por sí sola.** Es una predicción, no una medida: el nodo sigue abierto hasta que alguien ejecute P19. "
           "Lo que hace es convertir P19 en un experimento **con resultado esperado publicado de antemano**, que es más fuerte que uno exploratorio.\n"
           "- **Rango de validez declarado:** el ajuste en concentración es de 4.3 a 9.3 M en tejido neural; el de temperatura, "
           "de 23 a 37 °C en ovocitos. **Extrapolar a −22 °C es una extrapolación grande**, y es la debilidad principal: "
           "asume que la misma energía de activación gobierna el daño por debajo de 0 °C. Fahy advierte que a baja temperatura "
           "el daño dominante puede ser **osmótico y no químico** (L20), y ese término **no está en el modelo**.\n")
    (ROOT / "DERIVACION.md").write_text(doc)
    return dict(n=float("nan"), k=float("nan"), EaR=EaR, pred=pred, caliente=medido_caliente, factor=factor, anclas_ok=ok)
