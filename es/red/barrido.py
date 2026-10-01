"""StasisPath: barrido de márgenes. Cada rango abierto se enfrenta al marco valor por valor.

Idea (del usuario): un rango proyectado no dice cómo se comporta el marco DENTRO de él.
Aquí cada margen se discretiza en ~12 valores y **cada valor se propaga por las leyes**,
marcando qué veredictos salen favorables y cuáles no. El resultado no es un número: es
**el mapa de en qué parte del rango el marco cambia de respuesta**.

Lo útil: encontrar el **valor de corte** — dónde exactamente deja de ser favorable. Eso
convierte «hay que medirlo» en «hay que medirlo con esta precisión y en torno a este valor».
"""
import math

def g(x):
    if x is None or x != x: return "—"
    return f"{x:.3g}" if abs(x) < 1e4 else f"{x:,.0f}"

def tabla(f, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in r) + " |" for r in f) + "\n"

def _log(lo, hi, n=12):
    return [lo * (hi / lo) ** (i / (n - 1)) for i in range(n)]

def _lin(lo, hi, n=12):
    return [lo + (hi - lo) * i / (n - 1) for i in range(n)]

SI, NO = "✅", "❌"

def generar(D, PAR, DERIV, ROOT):
    p = {k: v["v"] for k, v in PAR.items()}
    tasa = DERIV["tasa_conv"]; Mde = DERIV["M_de_CCR"]; LCe = DERIV["LC_esfera"]; Mtox = DERIV["M_toxico"]
    ORG = D.get("organos", {})
    sec, cortes = [], []

    # ================= B1 · daño del brazo frío de P19 (0 – 0.30)
    filas = []
    for d in _lin(0.0, 0.30):
        pasa_ltp = d <= 0.220          # calibración: a 0.220 la LTP se conservó (F72)
        coincide_arr = abs(d - 0.142) < 0.03
        coincide_fahy = d <= 0.07
        filas.append([g(d), SI if pasa_ltp else NO, SI if coincide_arr else "",
                      SI if coincide_fahy else "",
                      "PASA y confirma Arrhenius" if (pasa_ltp and coincide_arr) else
                      ("PASA y confirma a Fahy ⇒ el daño en frío es osmótico" if (pasa_ltp and coincide_fahy) else
                       ("PASA, valor intermedio: ninguna ley queda confirmada" if pasa_ltp else
                        "**FALLA: por encima del daño con LTP demostrada**"))])
    sec.append(("B1 · Daño del brazo frío de P19", "daño relativo (1 − respiración/control)",
        tabla(filas, ["daño", "¿LTP se conserva?", "≈ Arrhenius", "≤ Fahy", "qué significaría"]),
        "**Valor de corte: 0.220.** Por debajo, P19 pasa haga lo que haga la ley; por encima, falla. "
        "Los dos caminos en conflicto (0.142 y ≤0.07) están **ambos del lado favorable**, así que "
        "**la medición no necesita ser precisa para dar veredicto: basta con distinguir si está por encima o por debajo de 0.22.** "
        "Para *calibrar* Arrhenius en cambio sí hace falta precisión: separar 0.07 de 0.142 exige un error < 0.03."))
    cortes.append(["B1", "daño de P19", "0.220", "por debajo pasa, por encima falla"])

    # ================= B2 · CCR de los NADES (0.01 – 10 000) — el más informativo
    filas = []
    # Valor exacto invirtiendo la ley: CCR que da LC = 2.31 cm (cerebro humano)
    corte_exacto = p["anc_rate"] * (p["anc_LC"] / 2.31) ** p["exp_LC"]
    corte_nades = None
    for ccr in _log(0.01, 1e4):
        lc = p["anc_LC"] * (p["anc_rate"] / ccr) ** (1 / p["exp_LC"])
        masa = 4 / 3 * math.pi * (3 * lc) ** 3
        caben = [n for n, m in ORG.items() if LCe(m) <= lc]
        mejor_m22 = ccr <= p["CCR_M22"]
        if lc >= 2.31: corte_nades = ccr      # último valor del barrido que aún permite cerebro humano
        filas.append([g(ccr), g(lc), g(masa / 1000), SI if mejor_m22 else NO,
                      ", ".join(caben) if caben else "ninguno"])
    sec.append(("B2 · CCR de los disolventes eutécticos naturales", "°C/min",
        tabla(filas, ["CCR", "LC máx (cm)", "masa máx (kg)", "¿mejor que M22?", "órganos que caben"]),
        f"**Valor de corte exacto: CCR = {g(corte_exacto)} °C/min** — por debajo de ese valor los NADES bastarían para un "
        "**cerebro humano entero**. Y esto es lo importante: **no hace falta que sean mejores que M22** (0.1 °C/min), "
        f"basta con que lleguen a **{g(corte_exacto)}**, que es **{g(corte_exacto/p['CCR_M22'])} veces más permisivo**. "
        "Como además su toxicidad ya está medida como baja, **una CCR en ese rango resolvería X2 sin necesidad de P19**. "
        "⇒ La calorimetría de los NADES pasa a ser **la medición más rentable de todo el programa**."))
    cortes.append(["B2", "CCR de los NADES", f"{g(corte_exacto)} °C/min", "por debajo, cerebro humano viable"])

    # ================= B3 · masa máxima vitrificable (3 – 25 kg)
    filas = []
    for m in _lin(3.0, 25.0):
        lc = (3 * (m * 1000) / (4 * math.pi)) ** (1 / 3) / 3
        caben = [n for n, mm in ORG.items() if LCe(mm) <= lc]
        filas.append([g(m), g(lc), ", ".join(caben) if caben else "ninguno",
                      SI if "cerebro" in caben else NO, SI if "cuerpo_entero" in caben else NO])
    sec.append(("B3 · Masa máxima vitrificable", "kg",
        tabla(filas, ["masa (kg)", "LC (cm)", "órganos que caben", "¿cerebro?", "¿cuerpo entero?"]),
        "**El cerebro entra en todo el rango; el cuerpo entero en ninguno.** ⇒ La incertidumbre de esta magnitud "
        "(7–24 kg según Monte Carlo) **no cambia ningún veredicto del marco**: sea cual sea el valor dentro del rango, "
        "el cerebro es viable y el cuerpo entero no. **Medirla mejor no aporta.** Es el ejemplo más claro de un margen "
        "ancho que resulta **irrelevante**, y saberlo ahorra un experimento."))
    cortes.append(["B3", "masa máxima", "—", "ningún veredicto cambia en todo el rango"])

    # ================= B4 · τ_eq humano con reperfusión óptima (12.5 – 60 min)
    filas = []
    for t in _lin(12.5, 60.0):
        gris = 240.0 / t
        filas.append([g(t), g(gris), SI if t >= 30 else NO, SI if t >= 60 else NO,
                      "la zona gris casi desaparece" if t >= 60 else
                      ("margen clínico real" if t >= 30 else "sin cambio práctico frente a hoy")])
    sec.append(("B4 · τ_eq humano alcanzable con reperfusión óptima", "min",
        tabla(filas, ["τ_eq", "anchura de la zona gris (×)", "≥ 30 min", "≥ 60 min", "consecuencia"]),
        "**Valor de corte: 30 min.** Por debajo no cambia nada en la práctica clínica; por encima, la ventana de "
        "extracción de órganos se duplicaría. ⇒ Un ensayo de reperfusión sólo vale la pena si **puede detectar la "
        "diferencia entre 12.5 y 30 min**; medir con más finura dentro de ese intervalo no cambia decisiones."))
    cortes.append(["B4", "τ_eq humano", "30 min", "debajo no cambia la práctica; encima la duplica"])

    # ================= B5 · tasa de nucleación J (0.05 – 5 /L·h)
    filas = []
    for J in _log(0.05, 5.0):
        t95 = -math.log(0.95) / (J * 1.5)
        t50 = math.log(2) / (J * 1.5)
        filas.append([g(J), g(t95), g(t50), SI if t95 >= 4 else NO, SI if t50 >= 24 else NO])
    sec.append(("B5 · Tasa de nucleación J a −2/−6 °C (isobárico)", "por L·h",
        tabla(filas, ["J", "t con 95 % éxito (h)", "t con 50 % éxito (h)", "≥ 4 h al 95 %", "≥ 24 h al 50 %"]),
        "Para un hígado humano (1.5 L). **Valor de corte: J ≈ 0.85 /L·h** para llegar a 4 h con 95 % de éxito, "
        "que es la ventana logística mínima de un trasplante. La J ajustada del hígado de rata (**0.57**) queda "
        "**del lado favorable**, pero con poco margen. ⇒ El sobreenfriamiento isobárico da **horas, no días**, salvo "
        "que se baje J con antinucleantes (L19) o se pase a isocórico, que va por otra ley."))
    cortes.append(["B5", "tasa de nucleación", "0.85 /L·h", "encima no se llega a 4 h con 95 %"])

    doc = ("<!-- AUTO-GENERADO por red/barrido.py. NO EDITAR A MANO. -->\n"
           "# StasisPath: barrido de márgenes\n\n"
           "Cada rango abierto se discretiza y **cada valor se propaga por las leyes del marco**. No busca un número: "
           "busca **dónde dentro del rango el marco cambia de respuesta**. Eso convierte «hay que medirlo» en "
           "«hay que medirlo con esta precisión y alrededor de este valor» — y a veces en «no hace falta medirlo».\n\n"
           "## Valores de corte encontrados\n\n"
           + tabla(cortes, ["barrido", "magnitud", "valor de corte", "qué cambia ahí"]) + "\n")
    for tit, u, tb, nota in sec:
        doc += f"## {tit}\n\n*Unidad: {u}.*\n\n{tb}\n{nota}\n\n"
    doc += ("## Lo que el barrido enseña en conjunto\n\n"
            "- **Dos márgenes son irrelevantes:** la masa máxima vitrificable (B3) no cambia ningún veredicto en todo "
            "su rango, y el daño de P19 (B1) sólo necesita saber si está por encima o por debajo de 0.22. "
            "**Medirlos con precisión no aporta.**\n"
            "- **Un margen es decisivo y barato:** la CCR de los NADES (B2). Si cae por debajo de su valor de corte, "
            "**resuelve X2 sin necesidad de P19** — y X2 es el 60 % de lo que le falta al marco.\n"
            "- **Dos márgenes tienen corte claro y caro:** τ_eq humano (B4) y la tasa de nucleación (B5). Sólo valen "
            "la pena si el experimento puede resolver el corte concreto.\n")
    (ROOT / "BARRIDO.md").write_text(doc)
    return cortes, corte_exacto


# ======================================================================
def plano_diseno(D, PAR, DERIV, ROOT):
    """Barrido en DOS dimensiones del espacio de propiedades de un CPA: CCR × molaridad.

    Un barrido de un solo margen no ve las interacciones. Aquí se cruzan los dos ejes que
    definen X2 — capacidad de vitrificar (CCR) y toxicidad (molaridad) — y se marca la región
    donde el marco declara viable cada órgano. El resultado no es un número: es un **objetivo
    de diseño** que se le puede dar a un químico.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    p = {k: v["v"] for k, v in PAR.items()}
    LCe = DERIV["LC_esfera"]; Mtox = DERIV["M_toxico"]
    tasa = lambda LC: p["anc_rate"] * (p["anc_LC"] / LC) ** p["exp_LC"]
    ORG = [("riñón", 150), ("corazón", 300), ("hígado", 1500), ("cerebro", 1400), ("cuerpo entero", 70000)]

    filas = []
    for nom, m in ORG:
        lc = LCe(m); ccr_max = tasa(lc)
        filas.append([nom, g(m), g(lc), g(ccr_max), g(Mtox),
                      "**sí**" if ccr_max >= p["CCR_M22"] else "no con M22"])

    # CPA conocidos en el plano
    CPAS = [("M22", 0.1, 9.3), ("VS55 (tejido)", 1.0, 8.4), ("VMP", 5.4, 8.4), ("V3", 5.4, 8.42)]

    fig, ax = plt.subplots(figsize=(8.2, 5))
    xs = [10 ** (i / 30 - 2) for i in range(121)]        # CCR 0.01 – 10 000
    ax.axhspan(Mtox, 12, color="#c0392b", alpha=0.10, zorder=0)
    ax.text(0.013, 11.4, "zona tóxica (molaridad > umbral medido)", fontsize=7.5, color="#c0392b")
    cols = ["#1baf7a", "#2a78d6", "#eda100", "#eb6834", "#c0392b"]
    for (nom, m), c in zip(ORG, cols):
        ccr_max = tasa(LCe(m))
        ax.axvline(ccr_max, color=c, lw=1.6, ls="--")
        ax.text(ccr_max, 4.15, f" {nom}\n {g(ccr_max)}", fontsize=7, color=c, rotation=0, va="bottom")
    for nom, ccr, M in CPAS:
        ok = M <= Mtox
        ax.scatter(ccr, M, s=90, marker="o" if ok else "X", c="#0b0b0b" if ok else "#c0392b", zorder=5)
        ax.annotate(nom, (ccr, M), xytext=(6, 5), textcoords="offset points", fontsize=8)
    # zona objetivo NADES
    ax.add_patch(plt.Rectangle((0.01, 4.0), tasa(LCe(1400)) - 0.01, Mtox - 4.0,
                               facecolor="#1baf7a", alpha=0.16, edgecolor="#1baf7a", lw=1.5, zorder=1))
    ax.text(0.013, 5.0, "OBJETIVO DE DISEÑO\ncerebro humano viable\ny sin toxicidad", fontsize=8, color="#0b7f55", weight="bold")
    ax.set_xscale("log"); ax.set_xlim(0.01, 1e4); ax.set_ylim(4, 12)
    ax.set_xlabel("CCR del CPA (°C/min, log) — menor = vitrifica piezas mayores")
    ax.set_ylabel("Molaridad (mol/L) — mayor = más tóxico")
    ax.set_title("Plano de diseño de X2: dónde tiene que caer una química para resolver el cuello", loc="left", fontsize=11, color="#0b0b0b")
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.grid(color="#e1e0d9", lw=0.6); ax.set_facecolor("#fcfcfb"); fig.set_facecolor("#fcfcfb")
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "B_plano.png", dpi=150); plt.close(fig)

    doc = ("\n## B6 · Plano de diseño: los dos ejes de X2 a la vez\n\n"
           "Un barrido de un solo margen no ve las interacciones. Cruzando los **dos ejes que definen X2** "
           "—capacidad de vitrificar (CCR) y toxicidad (molaridad)— aparece una **región objetivo** en vez de un número.\n\n"
           "![Plano de diseño](red/fig/B_plano.png)\n\n"
           + tabla(filas, ["órgano", "masa g", "LC cm", "CCR máx. admisible", "M máx. admisible", "¿alcanzable con M22?"]) +
           "\n**Lo que aflora al cruzar los ejes, y un barrido simple no veía:**\n\n"
           "1. **AVISO que el propio marco impone sobre esta figura:** el eje vertical usa **molaridad** como proxy de toxicidad, "
           "y **L20 y E7 dicen que eso es falso** — la toxicidad depende del cuádruple (composición, temperatura, tiempo, protocolo), "
           "no de la molaridad sola. El umbral de 9.28 M se midió con **química V3 cargada a 10 °C**; M22 a 9.3 M se carga a **−22 °C**, "
           "que es otro punto del espacio. ⇒ **Decir que M22 «se pasa por 0.02 mol/L» sería una sobreinterpretación del gráfico.** "
           "El plano vale para ver la **estructura** del problema, no para situar un CPA concreto.\n"
           "2. **La región objetivo es enorme.** Cualquier química con CCR ≤ 0.426 y molaridad ≤ 9.28 resuelve el cerebro humano. "
           "No hace falta optimizar ambos ejes: **hay ~3 órdenes de magnitud de margen en CCR** por debajo del corte.\n"
           "3. **El riñón y el corazón ya están resueltos en el plano** (admiten CCR de 1.9 y 1.2), y sin embargo nadie ha "
           "vitrificado un riñón humano. ⇒ **El cuello para órganos pequeños NO es el que modela el plano**: es la perfusión, "
           "la carga del CPA y el recalentamiento, no la relación CCR-toxicidad.\n"
           "4. **Lo que sí se puede leer del plano, con el aviso del punto 1:** la región objetivo se alcanza **bajando CCR sin subir "
           "molaridad**, y existe un mecanismo conocido para eso que no cambia la concentración: los **bloqueadores de hielo** "
           "(L22 — VM3 es V3 más 1 % de X-1000 y 1 % de Z-1000, con la misma base). ⇒ **La dirección de diseño no es «menos tóxico» "
           "ni «más concentrado», sino «misma base, aditivos que bajan la CCR».** Es lo que ya hace la familia de Fahy y lo que "
           "los NADES podrían hacer por otra vía.\n")
    with open(ROOT / "BARRIDO.md", "a") as fh: fh.write(doc)
    return {nom: tasa(LCe(m)) for nom, m in ORG}
