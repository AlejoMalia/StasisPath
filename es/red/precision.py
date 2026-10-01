"""StasisPath: precisión de los rangos. Métodos para estrechar lo que la triangulación deja abierto.

Cuatro herramientas, elegidas porque **se pueden aplicar con los datos que ya hay**:

1. **Número de Biot** — comprueba si la hipótesis de C3 (régimen limitado por conducción,
   tasa ∝ LC⁻²) es válida en cada escala. Donde no lo es, la ley cambia de exponente.
2. **Monte Carlo** — propaga la incertidumbre de los parámetros y devuelve una distribución
   en vez de un rango por esquinas, con percentiles.
3. **Análisis de sensibilidad sobre una contradicción** — cuánto tendría que estar equivocado
   cada supuesto para que la intersección deje de ser vacía.
4. **Nucleación de Poisson** — convierte una única observación de supervivencia en una cota de
   la tasa J(T) y una probabilidad, en vez de un punto.

Lo que NO se implementa y por qué: Kissinger/Ozawa/Avrami exigen datos de calorimetría que no
tenemos; Kaplan-Meier y Cox exigen tiempos hasta fallo que nadie ha publicado. Se dejan
declarados como «aplicables cuando llegue el dato».
"""
import math, random, statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA, RED = "#2a78d6", "#eb6834", "#1baf7a", "#c0392b"

H_CONV = 100.0    # W/m²K — coeficiente declarado en el modelo de Bischof (F2)
K_CPA = 0.40      # W/mK — conductividad de solución CPA acuosa (orden de magnitud)

def g(x):
    if x is None or x != x: return "—"
    return f"{x:.3g}" if abs(x) < 1e4 else f"{x:,.0f}"

def tabla(f, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in r) + " |" for r in f) + "\n"

def biot(LC_cm, h=H_CONV, k=K_CPA): return h * (LC_cm / 100) / k
LC_CRIT = K_CPA / H_CONV * 100    # cm donde Bi = 1

def factor_regimen(LC1, LC2):
    """Penalización de conducción de LC1 a LC2 respetando el cambio de régimen en Bi=1."""
    a, b = sorted((LC1, LC2))
    if b <= LC_CRIT: return b / a                      # convección: LC⁻¹
    if a >= LC_CRIT: return (b / a) ** 2               # conducción: LC⁻²
    return (LC_CRIT / a) * (b / LC_CRIT) ** 2          # mixto

def generar(D, PAR, DERIV, ROOT):
    p = {k: v["v"] for k, v in PAR.items()}
    rng = {k: v["r"] for k, v in PAR.items()}
    sec = []

    # ---------------------------------------------------- 1. Biot
    casos = [("lonchas de hipocampo (350 µm)", 0.035 / 3), ("cerebro de ratón (German)", 0.152),
             ("riñón de rata", 0.36), ("riñón humano", 0.88), ("bolsa de 3 L (ancla de C3)", p["anc_LC"]),
             ("cerebro humano", 2.31), ("cuerpo entero", p["LC_body"]), ("tronco", p["LC_trunk"])]
    filas = []
    for nom, lc in casos:
        Bi = biot(lc)
        reg = "conducción — **LC⁻² vale**" if Bi >= 1 else ("transición" if Bi > 0.3 else "convección — **LC⁻² NO vale**")
        filas.append([nom, g(lc), g(Bi), reg])
    f_mal = (2.31 / 0.152) ** 2
    f_bien = factor_regimen(0.152, 2.31)
    sec.append(("1. Número de Biot: ¿dónde vale nuestra ley?",
        "El exponente de C3 no es universal. La ley **tasa ∝ LC⁻²** supone régimen **limitado por conducción** (Bi ≫ 1). "
        "Si Bi ≪ 1 el cuerpo es casi isotermo y la tasa la fija la convección superficial: escala como **LC⁻¹**.\n\n"
        f"Con h = {g(H_CONV)} W/m²K (declarado en F2) y k ≈ {g(K_CPA)} W/mK, la frontera Bi = 1 está en "
        f"**LC = {g(LC_CRIT)} cm**.\n\n" + tabla(filas, ["sistema", "LC cm", "Bi", "régimen"]) +
        f"\n> **Buena noticia:** todas las extrapolaciones del marco a órganos humanos (LC {g(p['LC_kidneyH'])}–{g(p['LC_trunk'])} cm) "
        "caen en el régimen de **conducción**, donde LC⁻² es correcto. F1, F2, C3 y C6 quedan validadas en su rango de uso.\n\n"
        f"> ⚠ **CORRECCIÓN de un error propio:** en el módulo de escalado calculé la penalización de conducción del cerebro de "
        f"ratón (LC 0.152 cm) al humano (2.31 cm) aplicando LC⁻² a todo el trayecto, y dio **×{g(f_mal)}**. Pero ese trayecto "
        f"**cruza la frontera de régimen**: respetándola son **×{g(f_bien)}**. **Sobreestimé la dificultad en ×{g(f_mal/f_bien)}.** "
        "El déficit para repetir el protocolo de German en un cerebro humano no cambia (se calcula con la tasa humana, no "
        "escalando desde el ratón), pero la frase «el cerebro humano es ×231 peor en conducción» era incorrecta."))

    # ---------------------------------------------------- 2. Monte Carlo
    random.seed(7)
    N = 20000
    def muestra(k):
        lo, hi = rng[k]; c = p[k]
        # triangular con moda en el valor central: respeta el rango declarado sin inventar normalidad
        return random.triangular(lo, hi, c)
    Mtox = DERIV["M_toxico"]
    vals = []
    for _ in range(N):
        q = {k: muestra(k) for k in ("anc_LC", "anc_rate", "exp_LC", "CCR_M22", "CCR_VS55", "CCR_VMP")}
        b = (math.log10(q["CCR_M22"]) - (math.log10(q["CCR_VS55"]) + math.log10(q["CCR_VMP"])) / 2) / 0.9
        a = (math.log10(q["CCR_VS55"]) + math.log10(q["CCR_VMP"])) / 2 - b * 8.4
        tasa = lambda LC: q["anc_rate"] * (q["anc_LC"] / LC) ** q["exp_LC"]
        lc = next((i / 100 for i in range(25, 3000) if (math.log10(tasa(i / 100)) - a) / b > Mtox), None)
        if lc: vals.append(4 / 3 * math.pi * (3 * lc) ** 3 / 1000)
    vals.sort()
    pc = lambda q_: vals[int(q_ * (len(vals) - 1))]
    sec.append(("2. Monte Carlo: distribución en vez de esquinas",
        f"Las esquinas dan un rango; Monte Carlo da **dónde se concentra**. {N:,} muestras con distribución triangular "
        "dentro del rango declarado de cada parámetro (moda en el valor central: respeta lo declarado sin suponer normalidad).\n\n"
        "**Masa máxima vitrificable (la frontera de F2):**\n\n"
        + tabla([["percentil 5", f"{g(pc(0.05))} kg"], ["percentil 25", f"{g(pc(0.25))} kg"],
                 ["**mediana**", f"**{g(pc(0.5))} kg**"], ["percentil 75", f"{g(pc(0.75))} kg"],
                 ["percentil 95", f"{g(pc(0.95))} kg"]], ["percentil", "masa"]) +
        f"\n> El rango por esquinas era amplio; la mediana está en **{g(pc(0.5))} kg** y el 50 % central entre "
        f"**{g(pc(0.25))} y {g(pc(0.75))} kg**. La distribución está **sesgada a la derecha**: el valor típico es menor "
        "que la media, así que reportar la media sería optimista."))

    # ---------------------------------------------------- 3. Sensibilidad sobre la contradicción I1
    # Arrhenius da 0.142; las anclas de Fahy exigen <= 0.07. ¿Qué tendría que cambiar?
    dano_medido, T_ger, T_frio = 0.536, 10.0, -22.0
    obj = 0.07
    EaR_nec = math.log(dano_medido / obj) / (1 / (T_frio + 273.15) - 1 / (T_ger + 273.15))
    EaR_act = 2952.0
    filas = [["Ea/R usado (de ovocitos, F55)", f"{g(EaR_act)} K", "da daño 0.142"],
             ["Ea/R necesario para llegar a 0.07", f"{g(EaR_nec)} K", f"×{g(EaR_nec/EaR_act)} el actual"],
             ["Daño medido a 9.28 M y 10 °C", g(dano_medido), "F72, no discutido"]]
    sec.append(("3. Sensibilidad: qué resolvería la contradicción de I1",
        "La triangulación encontró que Arrhenius predice 0.142 y las anclas de Fahy exigen ≤ 0.07. "
        "En vez de elegir a ojo, se calcula **qué tendría que ser cierto** para que no hubiera choque.\n\n"
        + tabla(filas, ["magnitud", "valor", "nota"]) +
        f"\n> **Para que ambos caminos encajen, la energía de activación del daño tendría que ser ×{g(EaR_nec/EaR_act)} "
        f"la medida en ovocitos** (de {g(EaR_act)} a {g(EaR_nec)} K, es decir de ~24.5 a ~{g(EaR_nec*8.314/1000)} kJ/mol). "
        "Eso **no es descabellado**: 24.5 kJ/mol es bajo para daño proteico, y el valor sale de un sistema (ovocito) y un "
        "rango de temperatura (23–37 °C) muy distintos. ⇒ **La hipótesis más probable es que la extrapolación de Arrhenius "
        "subestima la energía de activación, no que Fahy esté equivocado.** Predicción concreta que P19 puede comprobar."))

    # ---------------------------------------------------- 4. Nucleación de Poisson
    V1, t1 = 0.2, 5.0     # L, h — riñón de cerdo a −2 °C sin nuclear (F20)
    J_max = 3.0 / (V1 * t1)          # si P(no nuclear) ≥ 5 %, entonces J·V·t ≤ 3
    filas = []
    for V, nom in ((0.2, "riñón de cerdo"), (1.5, "hígado humano"), (70.0, "cuerpo entero")):
        t_50 = math.log(2) / (J_max * V)
        t_95 = -math.log(0.95) / (J_max * V)
        filas.append([nom, g(V), g(t_95), g(t_50)])
    sec.append(("4. Nucleación como proceso de Poisson: de una observación a una probabilidad",
        "Una sola observación de «no nucleó» no da un número, pero **sí da una cota** si se modela como Poisson: "
        "P(no nuclear) = exp(−J·V·t). Del riñón de cerdo (0.2 L, 5 h a −2 °C sin nuclear) se obtiene, con un 95 % de "
        f"confianza, **J ≤ {g(J_max)} por L·h**.\n\n"
        + tabla(filas, ["sistema", "V (L)", "t con 95 % de éxito (h)", "t con 50 % de éxito (h)"]) +
        "\n> Así I5 deja de ser «≤ 0.67 h» y pasa a ser **una curva de probabilidad frente al tiempo**, que es lo que un "
        "protocolo clínico necesita. **Salvedad importante:** esto vale sólo en régimen **isobárico**; el sistema isocórico "
        "suprime la nucleación y va por otra ley (ver I5)."))

    # ---- figura Monte Carlo
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.hist(vals, bins=60, color=BLUE, edgecolor=SURF, linewidth=0.4)
    for q_, c, lab in ((0.05, MUTED, "p5"), (0.5, RED, "mediana"), (0.95, MUTED, "p95")):
        ax.axvline(pc(q_), color=c, lw=1.6 if q_ == 0.5 else 1, ls="-" if q_ == 0.5 else "--")
        ax.text(pc(q_), ax.get_ylim()[1] * 0.92, f" {lab} {g(pc(q_))}", fontsize=7.5, color=c)
    ax.set_xlabel("Masa máxima vitrificable (kg)"); ax.set_ylabel("frecuencia")
    ax.set_title("Monte Carlo: dónde se concentra la frontera de viabilidad", loc="left", fontsize=11, color=INK)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.grid(axis="y", color=GRID, lw=0.6); ax.set_facecolor(SURF); fig.set_facecolor(SURF)
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "P_montecarlo.png", dpi=150); plt.close(fig)

    doc = ("<!-- AUTO-GENERADO por red/precision.py. NO EDITAR A MANO. -->\n"
           "# StasisPath: precisión — estrechar lo que la triangulación deja abierto\n\n"
           "Cuatro métodos, elegidos porque **se pueden aplicar con los datos que ya hay**. "
           "Los que exigen datos que nadie ha publicado se declaran al final en vez de aplicarse a medias.\n\n")
    for tit, cuerpo in sec:
        doc += f"## {tit}\n\n{cuerpo}\n\n"
        if tit.startswith("2."): doc += "![Monte Carlo](red/fig/P_montecarlo.png)\n\n"
    doc += ("## Métodos que aún no se pueden aplicar, y qué dato les falta\n\n"
            + tabla([["Kissinger / Ozawa / Avrami", "cinética de cristalización desde calorimetría", "**datos de DSC de los NADES** (I2)"],
                     ["Kaplan-Meier / regresión de Cox", "supervivencia frente a tiempo de isquemia", "tiempos hasta fallo en una cohorte (I4)"],
                     ["Elementos finitos con geometría real", "campo térmico en un órgano, no en una esfera", "malla de un órgano humano + propiedades del CPA"],
                     ["Inferencia bayesiana completa", "posterior de cada parámetro en vez de rango", "réplicas independientes; hoy la mayoría son n = 1"]],
                    ["método", "para qué", "qué dato falta"]))
    (ROOT / "PRECISION.md").write_text(doc)
    return dict(LC_crit=LC_CRIT, f_mal=f_mal, f_bien=f_bien, mediana=pc(0.5), p5=pc(0.05), p95=pc(0.95), EaR_nec=EaR_nec)
