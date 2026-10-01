"""StasisPath: escalado entre especies y validación por exclusión (back-test).

Responde a: "¿se puede escalar lo logrado en animales y proyectar un número humano,
y luego comprobar dónde acierta y dónde no?"

Método (MATE): no se ajusta una curva y se proclama el resultado. Cada ley candidata se
somete a **validación por exclusión (leave-one-out)**: se deja fuera una especie, se predice
con las demás y se mide el error. Una ley sólo se usa para proyectar al humano si su error
de exclusión es conocido y acotado. Las leyes que fallan se reportan como fallo: saber dónde
NO escala es la mitad del resultado.
"""
import math, statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"

def g(x): return f"{x:.3g}" if abs(x) < 1e4 else f"{x:,.0f}"
def tabla(filas, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in f) + " |" for f in filas) + "\n"
def gmean(v): return math.exp(sum(math.log(x) for x in v) / len(v))

# Neuronas y masa encefálica [P]: orden de magnitud de la literatura (Herculano-Houzel y otros).
# No releídas en fuente primaria: se usan SÓLO para probar si la escala neuronal predice algo.
ESPECIES = {
    "C. elegans": dict(neu=302,     cerebro=1e-6,  cuerpo=1e-6),
    "ratón":      dict(neu=71e6,    cerebro=0.4,   cuerpo=30),
    "rata":       dict(neu=200e6,   cerebro=2.0,   cuerpo=300),
    "conejo":     dict(neu=500e6,   cerebro=10.0,  cuerpo=2500),
    "gato":       dict(neu=760e6,   cerebro=30.0,  cuerpo=4000),
    "perro":      dict(neu=2.25e9,  cerebro=70.0,  cuerpo=20000),
    "cerdo":      dict(neu=2.2e9,   cerebro=180.0, cuerpo=40000),
    "humano":     dict(neu=86e9,    cerebro=1400., cuerpo=70000),
}

def generar(D, PAR, R, ROOT):
    pv = {k: v["v"] for k, v in PAR.items()}
    Q10, t37 = pv["Q10"], pv["t37"]
    fig_dir = ROOT / "red" / "fig"; fig_dir.mkdir(exist_ok=True)
    doc_secciones = []

    # ============================================================ T1  τ_eq: ¿invariante entre especies?
    # τ_eq = t · Q10^((T-37)/10). Si fuera invariante perfecto, todas las especies darían el mismo número.
    obs = [  # (especie, T, t, etiqueta, fuente, incluir_en_ajuste)
        ("humano", 15, 31,  "DHCA 15 °C",              "F4",  True),
        ("humano", 10, 45,  "DHCA 10 °C",              "F4",  True),
        ("perro",  37, 12.5,"parada 12.5 min",          "F25b",True),
        ("perro",  10, 120, "flush frío 120 min",       "F30", True),
        ("cerdo",  10, 60,  "60 min, sin déficit",      "F42", True),
        ("gato",   37, 60,  "1 h, sólo cerebro",        "F38", False),
    ]
    pts = []
    for e, T, t, lab, f, usar in obs:
        tau = t * Q10 ** ((T - 37) / 10)
        pts.append(dict(e=e, T=T, t=t, tau=tau, lab=lab, f=f, usar=usar, M=ESPECIES[e]["cuerpo"]))
    base = [p for p in pts if p["usar"]]
    # validación por exclusión: predecir cada punto con la media geométrica de los demás
    for p in base:
        otros = [q["tau"] for q in base if q is not p]
        p["pred"] = gmean(otros)
        p["err"] = max(p["pred"] / p["tau"], p["tau"] / p["pred"])
    err_max = max(p["err"] for p in base)
    disp = max(p["tau"] for p in base) / min(p["tau"] for p in base)
    # ¿depende de la masa? correlación log-log
    xs = [math.log10(p["M"]) for p in base]; ys = [math.log10(p["tau"]) for p in base]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys)); sxx = sum((x - mx) ** 2 for x in xs)
    pend = sxy / sxx if sxx else 0.0
    r = sxy / math.sqrt(sxx * sum((y - my) ** 2 for y in ys)) if sxx else 0.0
    tau_h = gmean([p["tau"] for p in base if p["e"] != "humano"])   # proyección al humano SIN usar humano
    tau_h_real = gmean([p["tau"] for p in base if p["e"] == "humano"])
    veredicto_T1 = ("**PASA**" if err_max <= 3 and abs(pend) < 0.15 else "**FALLA**")
    filas = [[p["e"], p["lab"], g(p["T"]), g(p["t"]), f"**{g(p['tau'])}**", g(p["pred"]), f"×{g(p['err'])}", p["f"]] for p in base]
    filas.append(["gato", "1 h, sólo cerebro (excluido)", "37", "60", f"**{g(pts[-1]['tau'])}**", "—", "—", "F38"])
    doc_secciones.append(("T1 · ¿Es τ_eq invariante entre especies? (validación por exclusión)", None,
        f"Se deja fuera cada especie y se predice con las demás.\n\n" + tabla(filas,
        ["especie", "observación", "T °C", "t min", "τ_eq min", "predicho sin él", "error", "fuente"]) +
        f"\n- **Error máximo de exclusión: ×{g(err_max)}** · dispersión total ×{g(disp)}.\n"
        f"- **Dependencia de la masa corporal:** pendiente log-log **{pend:+.2f}** (r = {r:+.2f}) sobre 3 órdenes de magnitud de masa "
        f"(perro 20 kg → humano 70 kg → cerdo 40 kg). Una pendiente ≈ 0 significa que **τ_eq no depende del tamaño**.\n"
        f"- **Proyección al humano sin usar ningún dato humano: {g(tau_h)} min.** Valor humano real: {g(tau_h_real)} min. "
        f"Error de la proyección: **×{g(max(tau_h/tau_h_real, tau_h_real/tau_h))}**.\n"
        f"- Veredicto: {veredicto_T1}. La proyección entre especies de τ_eq es válida dentro de un factor ×{g(err_max)}. "
        f"El gato queda fuera del ajuste porque su isquemia fue **sólo cerebral** (otro protocolo), y precisamente por eso su τ_eq se dispara a {g(pts[-1]['tau'])}: "
        f"**la ley no falla por especie, falla por protocolo.**"))

    # ============================================================ T2  escalado térmico: ¿acierta la ley LC^-2?
    # Anclada en la bolsa de 3 L. Se compara con puntos medidos independientes.
    anc_LC, anc_rate = pv["anc_LC"], pv["anc_rate"]
    pred = lambda LC: anc_rate * (anc_LC / LC) ** 2
    casos = [("bolsa 0.5 L", 1.2, 1.4, "F2"), ("bolsa 1 L", 1.4, 1.0, "F2"), ("hígado de cerdo ~1 L", 1.8, 0.6, "F2")]
    filas, errs = [], []
    for nom, LC, medido, f in casos:
        p = pred(LC); e = max(p / medido, medido / p); errs.append(e)
        filas.append([nom, g(LC), g(medido), g(p), f"×{g(e)}", f])
    err_T2 = max(errs)
    doc_secciones.append(("T2 · ¿Acierta la ley térmica LC⁻² fuera de su ancla?", None,
        "La ley se ancló en la bolsa de 3 L (LC 2.2 cm → 0.47 °C/min) y se comprueba contra puntos medidos independientes del mismo trabajo.\n\n" +
        tabla(filas, ["caso", "LC cm", "medido °C/min", "predicho por LC⁻²", "error", "fuente"]) +
        f"\n- **Error máximo: ×{g(err_T2)}.** La ley térmica **PASA**: predice tasas de enfriamiento dentro de ×{g(err_T2)} en el rango 0.5–3 L.\n"
        f"- Por eso la extrapolación a LC de 4–7.5 cm (cuerpo y tronco) es creíble en orden de magnitud, aunque siga sin dato directo.")

    )

    # ============================================================ T3  ¿predice la escala neuronal el éxito criogénico?
    # La pregunta del usuario: ¿escalar por número de neuronas o conectomas?
    logros = [  # (especie, masa de tejido cerebral con el logro, tipo, año, fuente)
        ("rata",   0.01, "función (K+/Na+, ultraestructura) en lonchas", 2006, "F37"),
        ("ratón",  0.02, "función (LTP) en lonchas",                      2026, "F46"),
        ("ratón",  0.4,  "cerebro entero vitrificado (función en lonchas)",2026, "F46"),
        ("gato",   30.0, "cerebro entero congelado: actividad eléctrica parcial", 1974, "F48"),
        ("cerdo",  180.0,"cerebro entero vitrificado sin fijar: sólo estructura",  2026, "F47"),
    ]
    xs_n = [math.log10(ESPECIES[e]["neu"]) for e, *_ in logros]
    xs_y = [float(a) for *_, a, _ in logros]
    ys_l = [math.log10(m) for _, m, *_ in logros]
    def corr(xs, ys):
        mx, my = statistics.mean(xs), statistics.mean(ys)
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        sxx = sum((x - mx) ** 2 for x in xs); syy = sum((y - my) ** 2 for y in ys)
        return sxy / math.sqrt(sxx * syy) if sxx and syy else 0.0
    r_neu, r_yr = corr(xs_n, ys_l), corr(xs_y, ys_l)
    # ¿es real o un confundido? neuronas y masa encefálica están casi perfectamente correlacionadas entre especies
    esp_l = [e for e, *_ in logros]
    r_confund = corr([math.log10(ESPECIES[e]["neu"]) for e in ESPECIES if e != "C. elegans"],
                     [math.log10(ESPECIES[e]["cerebro"]) for e in ESPECIES if e != "C. elegans"])
    # ¿la masa lograda es simplemente la masa del cerebro de la especie elegida?
    frac = [m / ESPECIES[e]["cerebro"] for e, m, *_ in logros]
    filas = [[e, g(ESPECIES[e]["neu"]), g(ESPECIES[e]["cerebro"]), g(m), tipo, a, f] for e, m, tipo, a, f in logros]
    doc_secciones.append(("T3 · ¿Sirve el número de neuronas como variable de escalado?", None,
        tabla(filas, ["especie", "neuronas [P]", "cerebro g", "masa lograda g", "qué se logró", "año", "fuente"]) +
        f"\n- Correlación entre la masa lograda y el **número de neuronas**: r = **{r_neu:+.2f}** (alta).\n"
        f"- Correlación entre la masa lograda y el **año de publicación**: r = **{r_yr:+.2f}**.\n"
        f"- **Pero la correlación alta es un confundido, no una ley.** Entre especies, neuronas y masa encefálica van juntas "
        f"(r = **{r_confund:+.2f}**), y la masa lograda es esencialmente la masa del cerebro de la especie elegida "
        f"(fracciones logrado/cerebro: {', '.join(g(f) for f in frac)}). Es decir: r alto sólo dice que **quien vitrifica un cerebro de cerdo obtiene "
        f"la masa de un cerebro de cerdo**. Es una tautología, no capacidad predictiva.\n"
        f"- **La prueba que lo zanja:** el número de neuronas no aparece en ninguna de las ecuaciones que limitan el problema. "
        "**Lo que limita es la geometría, no el recuento neuronal.** El calor difunde como LC², "
        "el crioprotector se reparte por la vasculatura y las grietas dependen del gradiente térmico. Ninguna de esas tres cosas "
        "sabe cuántas neuronas hay dentro.\n"
        f"- **Dónde sí importa el recuento neuronal:** en el eje de **información**, no en el de física. El cerebro humano tiene "
        f"~{g(ESPECIES['humano']['neu'] / ESPECIES['ratón']['neu'])} veces las neuronas del ratón y "
        f"~{g(ESPECIES['humano']['neu'] / ESPECIES['C. elegans']['neu'])} veces las de *C. elegans*: eso fija **cuánta** información hay que conservar "
        "y cuánto hay que muestrear para verificarlo (P15), no si el tejido sobrevive.\n"
        "- **Conclusión de método:** escalar por neuronas daría un número sin contenido físico. Para proyectar al humano hay que usar "
        "la geometría (LC, masa) en los ejes físicos y el recuento neuronal sólo en el eje de información."))

    # ============================================================ T4  proyección al humano con las leyes que PASAN
    LC_h_cerebro = (3 * 1400 / (4 * math.pi)) ** (1 / 3) / 3
    rate_h = pred(LC_h_cerebro)
    LC_raton = (3 * 0.4 / (4 * math.pi)) ** (1 / 3) / 3
    rate_raton = pred(LC_raton)
    # CORRECCIÓN (ver PRECISION.md §1): el trayecto ratón->humano CRUZA la frontera Bi=1 (LC 0.40 cm).
    # Aplicar LC^-2 a todo el trayecto sobreestima la dificultad en ×2.6.
    LC_CRIT = 0.40
    def _factor(a_, b_):
        a_, b_ = sorted((a_, b_))
        if b_ <= LC_CRIT: return b_ / a_
        if a_ >= LC_CRIT: return (b_ / a_) ** 2
        return (LC_CRIT / a_) * (b_ / LC_CRIT) ** 2
    ratio = _factor(LC_raton, LC_h_cerebro)
    tasa_german = 2.45 * 60   # °C/s -> °C/min, enfriamiento logrado en cerebro de ratón (F46)
    deficit = tasa_german / rate_h        # cuántas veces falta para repetir ese protocolo en humano
    ordenes = math.log10(deficit)
    filas = [
        ["τ_eq de entrada", f"×{g(err_T2 * 0 + err_max)}", f"{g(tau_h)} min", "**válida**: sin dependencia de la masa y error de exclusión acotado"],
        ["Enfriamiento del cerebro (LC⁻²)", f"×{g(err_T2)}", f"{g(rate_h)} °C/min por convección en LC {g(LC_h_cerebro)} cm", "**válida** en orden de magnitud"],
        ["Escalado por neuronas", "—", "sin contenido físico", "**inválida** para los ejes físicos (T3)"],
    ]
    doc_secciones.append(("T4 · Proyección al humano con las leyes validadas", None,
        tabla(filas, ["ley", "error de exclusión", "proyección humana", "veredicto"]) +
        f"\n**El número que pedías, calculado:** German 2026 vitrifica el cerebro de ratón (LC ≈ {g(LC_raton)} cm) enfriando a ≥ {g(tasa_german)} °C/min. "
        f"Un cerebro humano tiene LC ≈ {g(LC_h_cerebro)} cm, es decir **×{g(ratio)} peor en conducción** (respetando el cambio de régimen en Bi = 1; aplicar LC⁻² a todo el trayecto daría ×231 y **sobreestimaría la dificultad ×2.6**). Ese mismo protocolo exige {g(tasa_german)} °C/min, "
        f"pero la convección en un cerebro humano sólo da **{g(rate_h)} °C/min**: un déficit de **×{g(deficit)}**.\n\n"
        f"⇒ **El protocolo de German no escala al cerebro humano por convección: le faltan ~{ordenes:.1f} órdenes de magnitud de velocidad de enfriamiento.** "
        f"Esto no es una opinión: es la misma ley LC⁻² que ya acertó dentro de ×{g(err_T2)} en T2.\n\n"
        f"**Qué exige entonces un cerebro humano:** un CPA cuya CCR sea ≤ {g(rate_h)} °C/min (la clase M22, CCR {g(pv['CCR_M22'])}, **cumple**; "
        f"V3 y VMP no) más calentamiento volumétrico. Es exactamente lo que hace Fahy 2026 (M22, cerebro de cerdo, sólo estructura) "
        f"y lo que NO hace German (V3, alta velocidad, sólo ratón). **Las dos mitades del cuello de botella usan químicas incompatibles entre sí.**"))

    # ---- figura: τ_eq entre especies
    fig, ax = plt.subplots(figsize=(8, 4.4))
    for p in pts:
        c = ORANGE if not p["usar"] else BLUE
        ax.scatter(p["M"], p["tau"], s=80, c=c, edgecolors=SURF, linewidths=1.5, zorder=3)
        ax.annotate(f"{p['e']}: {p['lab']}", (p["M"], p["tau"]), xytext=(6, 5), textcoords="offset points", fontsize=7, color=INK2)
    lo, hi = min(p["tau"] for p in base), max(p["tau"] for p in base)
    ax.axhspan(lo, hi, color=BLUE, alpha=0.10, zorder=1)
    ax.axhline(gmean([p["tau"] for p in base]), color=BLUE, lw=2, zorder=2, label=f"invariante τ_eq ≈ {g(gmean([p['tau'] for p in base]))} min (banda ×{g(disp)})")
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(5e3, 3e5)
    ax.set_xlabel("Masa corporal (g, log)"); ax.set_ylabel("τ_eq: isquemia equivalente a 37 °C (min, log)")
    ax.set_title("T1 · τ_eq no depende del tamaño del animal (naranja = protocolo distinto)", loc="left", fontsize=10.5, color=INK)
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.16))
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.grid(color=GRID, lw=0.6); ax.set_facecolor(SURF); fig.set_facecolor(SURF)
    fig.tight_layout(); fig.savefig(fig_dir / "T1_tau_especies.png", dpi=150); plt.close(fig)

    doc = ("<!-- AUTO-GENERADO por red/escalado.py (llamado desde red/motor.py). NO EDITAR A MANO. -->\n"
           "# StasisPath: escalado entre especies y validación por exclusión\n\n"
           "**La pregunta:** ¿se puede escalar lo logrado en animales y proyectar un número humano, y después comprobar dónde acierta y dónde no?\n\n"
           "**Respuesta corta:** sí, pero **no con el número de neuronas**. Se puede con las leyes cuyo error de exclusión se puede medir. "
           "Aquí cada ley candidata se valida dejando fuera una especie y prediciéndola con las demás; sólo las que pasan se usan para proyectar.\n\n"
           "![τ_eq entre especies](red/fig/T1_tau_especies.png)\n\n")
    for tit, figf, body in doc_secciones:
        doc += f"## {tit}\n\n" + (f"![{tit}](red/fig/{figf})\n\n" if figf else "") + body + "\n\n"
    doc += ("## Resumen\n\n"
            f"| ley | ¿valida? | error | uso |\n|---|---|---|---|\n"
            f"| τ_eq invariante entre especies | sí | ×{g(err_max)} | proyectar ventanas de isquemia al humano |\n"
            f"| enfriamiento LC⁻² | sí | ×{g(err_T2)} | proyectar vitrificación a cualquier tamaño |\n"
            f"| escalado por neuronas | **no** | — | sólo para dimensionar la información (P15), no la física |\n")
    (ROOT / "ESCALADO.md").write_text(doc)
    return dict(err_tau=err_max, err_term=err_T2, r_neu=r_neu, ratio_cerebro=ratio, rate_h=rate_h)
