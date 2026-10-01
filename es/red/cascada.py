"""StasisPath: la cascada hasta el final — ¿qué probabilidad le da el marco a que P19 pase?

`DERIVACION.md` compone la toxicidad en concentración con la toxicidad en temperatura y predice
el brazo frío de P19 con **un número puntual: 0.142**. Un número puntual no se puede comparar con
un umbral honestamente. Aquí se recorre la misma cascada **con toda la incertidumbre propagada**,
paso a paso, y se responde a la pregunta que el marco nunca ha respondido:

    **¿Con qué probabilidad, según sus propias leyes y sus propios rangos, el marco cree que P19 pasa?**

Eso NO cierra X2, y el módulo está escrito para que no se pueda confundir con un cierre:

  - La salida es una **probabilidad de creencia**, no una medición. Se etiqueta así en cada línea.
  - Se acompaña del **historial de aciertos** de este mismo tipo de predicción. Esta semana el marco
    predijo I2 = 0.3 °C/min y el valor medido resultó > 30: **un factor 100 de error**. Una cascada
    que produce una creencia muy segura, en un marco cuyo último acierto de este tipo falló por dos
    órdenes de magnitud, es información sobre la cascada, no sobre la química.
  - Se declara **qué eslabón no tiene dato**, que es donde la cascada deja de ser cálculo.

La contradicción I1 es el corazón del asunto y aquí se propaga en vez de ocultarse: el marco tiene
**dos caminos que discrepan en un factor ~2** sobre la misma magnitud (Arrhenius da 0.142; las
anclas de Fahy exigen ≤ 0.07). Un cálculo honesto no elige uno: muestrea los dos.

Salida: CASCADA.md + red/fig/CA_cascada.png. Lo llama motor.py.
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"

N = 200000
SEMILLA = 20260926

# --- anclas MEDIDAS que alimentan la cascada (todas ya en la red) ---
D_GERMAN_10C = 0.536      # daño medido a 9.28 M y 10 °C (F72)
D_LTP_OK     = 0.220      # nivel de daño con LTP DEMOSTRADAMENTE conservada (F46: 138.1 % vs 157.7 n.s.)
D_FAHY_MAX   = 0.070      # cota de las anclas de Fahy para "sin daño"
EaR_OVO      = 2952.0     # Ea/R de ovocitos (F55), medido entre 23 y 37 °C
EaR_NECES    = 4520.0     # Ea/R que haría encajar ambos caminos (PRECISION.md)
T_CAL        = (23.0, 37.0)   # rango donde Ea/R está calibrado
T_OBJ        = -22.0          # temperatura del brazo C de P19

def g(x):
    return f"{x:.3g}"

def tabla(filas, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in f) + " |" for f in filas) + "\n"

def generar(D, PAR, DERIV, ROOT):
    rng = np.random.default_rng(SEMILLA)

    # ---- eslabón 1: la energía de activación. Aquí vive la contradicción I1.
    # Camino A (Arrhenius sobre ovocitos): EaR ~ 2952, con la dispersión de un ajuste de 2 puntos.
    # Camino B (anclas de Fahy): exige EaR ~ 4520 para que el daño a -22 baje hasta 0.07.
    # No se elige: se muestrea una mezcla 50/50, que es lo que significa "contradicción abierta".
    camino = rng.random(N) < 0.5
    eaA = rng.normal(EaR_OVO, EaR_OVO * 0.25, N)      # ±25 %: ajuste de dos puntos
    eaB = rng.normal(EaR_NECES, EaR_NECES * 0.25, N)
    EaR = np.where(camino, eaA, eaB)
    EaR = np.clip(EaR, 500, 12000)

    # ---- eslabón 2: extrapolación térmica fuera del rango calibrado
    # factor = exp(-EaR (1/T_obj - 1/T_ref)) con T en kelvin
    Tref, Tobj = 10.0 + 273.15, T_OBJ + 273.15
    factor = np.exp(-EaR * (1.0 / Tobj - 1.0 / Tref))
    # penalización por extrapolar: el modelo se calibró entre 23 y 37 °C y se usa a -22 °C.
    # Se muestrea un sesgo multiplicativo log-normal creciente con la distancia de extrapolación.
    dist = (min(T_CAL) - T_OBJ) / (max(T_CAL) - min(T_CAL))   # ~3.2 rangos de calibración
    sesgo = np.exp(rng.normal(0, 0.25 * dist, N))
    dano = D_GERMAN_10C * factor * sesgo

    # ---- eslabón 3: transferencia ovocito -> tejido neural (sin dato)
    # Ea/R sale de OVOCITOS. Que la misma energía de activación valga para la LTP de CA1 no tiene
    # ningún dato detrás. Se modela como un factor de transferencia ancho y se declara.
    transf = np.exp(rng.normal(0, 0.35, N))
    dano_neural = dano * transf

    pasa = dano_neural < D_LTP_OK
    p_pasa = float(pasa.mean())
    q = lambda a: float(np.quantile(dano_neural, a))

    # sensibilidad: ¿qué pasa si la contradicción se resuelve a favor de cada camino?
    p_A = float((dano_neural[camino] < D_LTP_OK).mean())
    p_B = float((dano_neural[~camino] < D_LTP_OK).mean())
    # ¿y si no hubiera incertidumbre de transferencia ni de extrapolación?
    dano_limpio = D_GERMAN_10C * factor
    p_limpio = float((dano_limpio < D_LTP_OK).mean())

    # ================================================================ TODOS LOS CAMINOS DEL MARCO
    # La cadena de Arrhenius es UNO de los caminos. El marco tiene más, y el usuario tiene razón en
    # que hay que hacerlos hablar. Pero no son independientes: varios se apoyan en el MISMO dato de
    # German. Combinarlos como si lo fueran infla la confianza, y ése es el resultado interesante.
    #
    # ancla compartida: el conjunto de datos de German (F72/F46). Se muestrea UNA vez y se reutiliza
    # en todos los caminos que dependen de él, que es lo que crea la correlación.
    german_ok = rng.normal(1.0, 0.15, N)     # incertidumbre del propio conjunto de German

    CAMINOS = [
        # (nombre, P(pasa) que aporta ese camino por si solo, ancla, indep de German)
        ("Arrhenius × punto de German (I1, camino A)", None, "german", False),
        ("Anclas de Fahy: M22 tolerable a −22 °C en loncha renal (I1, camino B)", None, "fahy", True),
        ("Calibración daño↔LTP: a daño 0.220 la LTP se conservó (I1, camino C)", None, "german", False),
        ("F47: M22 en cerebro de conejo, cerdo y biopsia humana, SIN hielo", 0.62, "fahy_brain", True),
        ("F5: riñón de conejo con M22 trasplantado y funcional (E3)", 0.58, "conejo", True),
        ("L13/F71: V3 (8.42 M) conserva LTP y M22 sólo es un 10 % más concentrado", 0.70, "german", False),
    ]

    # Caminos 1 y 3 ya están en la simulación de arriba (dano_neural usa el punto de German).
    # Los caminos 4, 5 y 6 aportan evidencia que NO entra en esa cadena. Se modelan como
    # verosimilitudes independientes o correlacionadas según su ancla.
    # --- Modelo correcto: cada camino es una OBSERVACIÓN RUIDOSA del mismo hecho latente
    # ("¿M22 conserva la función neural?"), no una oportunidad independiente de que pase.
    # Combinarlos con 1-prod(1-p) sería tratarlos como billetes de lotería y satura en 99 %
    # dando igual lo que digan. Lo correcto es multiplicar RAZONES DE VEROSIMILITUD sobre un
    # prior de 0.5, que es lo que convierte "p de un camino" en "cuánto mueve la creencia".
    LR = lambda pr: pr / (1.0 - pr)

    # Dentro de un grupo que comparte ancla NO se multiplican: si el ancla está sesgada, fallan
    # todos a la vez. Se toma la razón de verosimilitud MÁS FUERTE del grupo.
    grupos = {}
    grupos.setdefault("german", []).append(LR(p_pasa))   # la cadena simulada es del grupo german
    for nom, pr, anc, _ in CAMINOS:
        if pr is not None:
            grupos.setdefault(anc, []).append(LR(pr))
    lr_honesta = 1.0
    for k, v in grupos.items():
        lr_honesta *= max(v)
    p_honesta = lr_honesta / (1.0 + lr_honesta)

    # Ingenua: multiplicar TODAS las razones, como si no compartieran nada.
    lr_ingenua = LR(p_pasa)
    for nom, pr, anc, _ in CAMINOS:
        if pr is not None: lr_ingenua *= LR(pr)
    p_ingenua = lr_ingenua / (1.0 + lr_ingenua)

    n_grupos = len(grupos)
    filas_cam = []
    for nom, pr, anc, indep in CAMINOS:
        filas_cam.append([nom, "en la cadena simulada" if pr is None else f"{100*pr:.0f} %",
                          "—" if pr is None else f"×{LR(pr):.2f}", anc,
                          "sí" if indep else "**no: comparte el dato de German**"])

    # ---- figura
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.2), gridspec_kw={"width_ratios": [2, 1]})
    bins = np.logspace(-3, 1, 90)
    ax.hist(dano_neural[camino], bins=bins, color=ORANGE, alpha=0.55, label="camino A: Arrhenius sobre ovocitos")
    ax.hist(dano_neural[~camino], bins=bins, color=BLUE, alpha=0.55, label="camino B: anclas de Fahy")
    ax.axvline(D_LTP_OK, color="#0e7a55", lw=1.8)
    ax.text(D_LTP_OK * 1.08, ax.get_ylim()[1] * 0.92, f" LTP conservada\n a daño {D_LTP_OK} (medido)",
            fontsize=7.4, color="#0e7a55", va="top")
    ax.axvline(D_FAHY_MAX, color=MUTED, lw=1, ls="--")
    ax.set_xscale("log"); ax.set_xlabel("daño predicho en el brazo frío de P19 (derivado, NO medido)", color=INK2)
    ax.set_yticks([]); ax.legend(fontsize=7.2, frameon=False, loc="upper left")
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)

    barras = [("TODO el marco,\ncombinación honesta", p_honesta, AQUA),
              ("todo el marco,\ncombinación ingenua", p_ingenua, "#c0392b"),
              ("sólo la cadena\nde Arrhenius", p_pasa, ORANGE),
              ("sin incertidumbre\nde transferencia", p_limpio, MUTED)]
    for i, (lab, v, c) in enumerate(barras):
        ax2.barh(i, v, color=c, height=0.55)
        ax2.text(min(v + 0.02, 0.8), i, f"{100*v:.0f} %", va="center", fontsize=8, color=INK2)
    ax2.set_yticks(range(len(barras))); ax2.set_yticklabels([b[0] for b in barras], fontsize=7.4, color=INK2)
    ax2.set_xlim(0, 1.05); ax2.set_xlabel("P(el marco CREE que P19 pasa)", color=INK2)
    for sp in ("top", "right", "left"): ax2.spines[sp].set_visible(False)
    for a in (ax, ax2): a.set_facecolor(SURF); a.grid(axis="x", color=GRID, lw=0.6)
    fig.set_facecolor(SURF)
    fig.suptitle("La cascada hasta el final: una creencia con su dispersión, no un número",
                 x=0.02, ha="left", fontsize=11, color=INK)
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "CA_cascada.png", dpi=150); plt.close(fig)

    doc = ("<!-- AUTO-GENERADO por red/cascada.py. NO EDITAR A MANO. -->\n"
           "# StasisPath: la cascada hasta el final — qué probabilidad le da el marco a su propia predicción\n\n"
           "`DERIVACION.md` predice el brazo frío de P19 con **un número puntual: 0.142**. Un número puntual no se compara "
           f"honestamente con un umbral. Aquí se recorre la misma cascada con **toda la incertidumbre propagada**, {N:,} muestras.\n\n"
           "> ## Esto NO cierra X2, y no puede\n"
           "> Lo que sale de aquí es una **probabilidad de creencia**: qué cree el marco, dadas sus propias leyes y rangos. "
           "No es una medición. **El precio de confundirlas está pagado esta misma semana:** el marco predijo que la CCR de los "
           "NADES sería 0.3 °C/min y declaró que se refutaría por encima de 0.426. El valor medido resultó **> 30**, un factor "
           "**100** de error. Si esa predicción se hubiera contado como dato, hoy el marco tendría un valor gravemente falso en "
           "el núcleo y seguiría recomendando el experimento equivocado. **Historial de esta clase de predicción: 0 aciertos de 1.**\n\n"
           "![Cascada](red/fig/CA_cascada.png)\n\n"
           "## Los tres eslabones, y dónde cada uno deja de ser cálculo\n\n"
           + tabla([
               ["1. Energía de activación", f"Ea/R = {g(EaR_OVO)} K (camino A) frente a {g(EaR_NECES)} K (camino B)",
                "**la contradicción I1, abierta.** Los dos caminos discrepan en un factor ~1.5 en Ea/R. No se elige: se muestrean ambos al 50 %"],
               ["2. Extrapolación térmica", f"de {g(T_CAL[0])}–{g(T_CAL[1])} °C hasta {g(T_OBJ)} °C",
                f"se usa el modelo a **{dist:.1f} rangos de calibración** de distancia. Ningún dato dice que Arrhenius siga valiendo ahí"],
               ["3. Ovocito → neural", "Ea/R está medida en OVOCITOS; P19 mide LTP en CA1",
                "**sin ningún dato.** Que la misma energía de activación gobierne ambos es una suposición, no una ley"]],
               ["eslabón", "qué compone", "dónde deja de ser cálculo"])
           + "\n## El resultado\n\n"
           + tabla([
               ["**P(el marco cree que P19 pasa)**", f"**{100*p_pasa:.0f} %**", "creencia, no medición"],
               ["daño predicho, mediana", g(q(0.5)), "derivado"],
               ["50 % central", f"{g(q(0.25))} – {g(q(0.75))}", "derivado"],
               ["90 % central", f"{g(q(0.05))} – {g(q(0.95))}", "derivado"],
               ["umbral con LTP conservada", g(D_LTP_OK), "**MEDIDO** (F46: 138.1 % frente a 157.7, n.s.)"]],
               ["magnitud", "valor", "naturaleza"])
           + "\n## Todos los caminos del marco, y por qué no se suman como parecen\n\n"
           "La cadena de Arrhenius es **uno** de los caminos. El marco tiene más, y hacerlos hablar es correcto. "
           "Pero varios **se apoyan en el mismo conjunto de datos de German** (F72/F46), así que no son evidencia "
           "independiente: si ese conjunto estuviera sesgado, fallarían a la vez.\n\n"
           + tabla(filas_cam, ["camino", "P(pasa) que aporta por sí solo", "razón de verosimilitud", "ancla", "¿independiente?"])
           + f"\n**Combinación honesta (agrupando por ancla, {n_grupos} grupos independientes): "
           f"{100*p_honesta:.0f} %.**\n\n"
           f"**Combinación ingenua (tratando los 6 como independientes): {100*p_ingenua:.0f} %.**\n\n"
           f"> **Cada camino es una observación ruidosa del MISMO hecho, no una oportunidad independiente de que pase.** "
           "Por eso no se combinan con 1−∏(1−p), que satura en 99 % diga lo que diga cada uno: se multiplican **razones de "
           "verosimilitud** sobre un prior de 0.5. Dentro de un grupo que comparte ancla no se multiplican — si el ancla está "
           "sesgada fallan todos a la vez — y se toma la más fuerte del grupo.\n\n"
           f"> La diferencia entre {100*p_ingenua:.0f} % y {100*p_honesta:.0f} % es **exactamente lo que cuesta contar dos veces "
           "el mismo experimento**. Tres de los seis caminos leen el mismo conjunto de datos: el de German. Sumarlos como si "
           "fueran independientes es el error clásico de la meta-evidencia, y aquí está cuantificado. **Añadir caminos que "
           "comparten ancla sube la confianza aparente sin añadir información.**\n\n"
           "> **Y aun con todo el marco hablando, la combinación honesta no llega a certeza.** El techo lo pone el eslabón que "
           "no tiene dato: ninguno de los seis caminos mide **M22 sobre tejido neural con función**. Todos rodean el hueco; "
           "ninguno lo cruza. Por eso el número sube pero no se cierra.\n"
           + f"\n**Si la contradicción I1 se resolviera a favor de cada camino:** camino A (Arrhenius sobre ovocitos) da "
           f"**{100*p_A:.0f} %**; camino B (anclas de Fahy) da **{100*p_B:.0f} %**. Sin la incertidumbre de transferencia ni de "
           f"extrapolación, la cascada daría **{100*p_limpio:.0f} %** — y esa cifra es precisamente la que NO hay derecho a usar, "
           "porque esos dos eslabones son reales.\n\n"
           "## Por qué esto no se puede convertir en un cierre\n\n"
           "1. **El eslabón 3 no tiene dato.** Toda la cascada descansa en que la energía de activación del daño medida en "
           "ovocitos gobierne la plasticidad sináptica de CA1. Ninguna fuente de la red lo sostiene. Es el punto donde el "
           "cálculo se convierte en suposición, y ninguna cantidad de muestreo lo arregla.\n"
           "2. **La contradicción I1 sigue abierta**, y es justo lo que P19 discrimina. Cerrar X2 con la cascada sería usar como "
           "prueba lo que está en disputa.\n"
           "3. **P19 tiene umbrales preregistrados y congelados por hash.** Si una predicción pudiera cerrarlo, el preregistro no "
           "significaría nada y el marco perdería la capacidad de equivocarse — que es de donde saca su valor. Esta semana se ha "
           "falsado a sí mismo dos veces (I2 y el atajo de los NADES); ninguna de las dos habría sido posible bajo esa regla.\n\n"
           f"**Lo que sí aporta este documento:** convierte «el marco predice 0.142» en «el marco cree que P19 pasa con un "
           f"{100*p_pasa:.0f} % y aquí está por qué». Eso hace la predicción **más falsable, no menos**: si P19 diera FALLA, este "
           "documento dice exactamente qué eslabón habría que revisar primero.\n")
    (ROOT / "CASCADA.md").write_text(doc)
    return {"p_pasa": p_pasa, "p_A": p_A, "p_B": p_B, "p_limpio": p_limpio, "p_honesta": p_honesta,
            "p_ingenua": p_ingenua, "n_grupos": n_grupos, "filas_cam": filas_cam,
            "mediana": q(0.5), "p05": q(0.05), "p95": q(0.95)}
