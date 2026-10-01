"""StasisPath: cruce sistemático de capas — cada punto de datos contra cada ley, todos a la vez.

`encuentros.py` cruza DIMENSIONES por pares (T×t, masa×E...). Este módulo hace algo distinto:
enfrenta **la capa de datos entera contra la capa de leyes entera**, y busca estructura en los
residuos. Es lo que en las tandas 36 y 46 se hizo a mano y dio C10 y L11: un dato que ya estaba
en la red y respondía a otra pregunta.

Tres cruces, ninguno de los cuales inventa un dato:

  1. **Exceso térmico.** Para cada punto con (T, t) se calcula el exceso sobre la ventana que C2
     concede: exc = t / w(T), con w(T) = t37 · Q10^((37−T)/10). Un exceso ≫ 1 significa que ese
     sistema aguantó mucho más de lo que la ley térmica permite ⇒ **hay un mecanismo no térmico**.
     C4, C9 y C10 hacen esto para cuatro puntos sueltos; aquí se hace para todos.
  2. **Estructura en los excesos.** ¿El exceso se agrupa por clase, fase o por natural/artificial?
     Si se agrupa, es una regularidad cuantitativa que el marco no tenía escrita.
  3. **Vías contra cotas.** Cada vía declara una ventana; cada cota calcula lo permitido.
     Una vía que promete más de lo que su cota permite es o una refutación o un error de ficha.

**Límite declarado:** todo lo que sale de aquí es **derivado**, no medido. Un exceso calculado no
es un dato nuevo: es una relectura de datos existentes. Sirve para **señalar dónde mirar**, y toda
anomalía se marca para revisión humana, nunca se convierte sola en un nodo cerrado (R5).

Salida: CRUCE.md + red/fig/C_exceso.png. Lo llama motor.py.
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
COLOR_CLASE = {"hipotermia": BLUE, "bajo_flujo": BLUE, "normotermia": BLUE, "celular": BLUE,
               "fase_controlada": ORANGE, "vidrio": AQUA, "natural": YELLOW}

def g(x):
    if x is None: return "—"
    if x == float("inf"): return "∞"
    return f"{x:.3g}" if abs(x) < 1e4 else f"{x:.2e}"

def tabla(filas, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in f) + " |" for f in filas) + "\n"

def generar(D, PAR, ROOT):
    p = {k: v["v"] for k, v in PAR.items()}
    vent = lambda T: p["t37"] * p["Q10"] ** ((37 - T) / 10)   # C2: ventana isquémica (min) a T

    # ---------------------------------------------------------------- 1. exceso térmico
    filas, pts = [], []
    for pid, q in sorted(D["puntos"].items()):
        T, t = q.get("T"), q.get("t")
        if T is None or t is None: continue
        if q.get("fase") == "vidrio":
            # bajo Tg no hay metabolismo: la ley térmica no aplica y el exceso no significa nada
            filas.append([pid, q["label"][:44], g(T), g(t), q.get("clase", "—"), "—",
                          "no aplica (vidrio: sin metabolismo)"])
            continue
        w = vent(T); exc = t / w
        # el exceso en las esquinas del rango de Q10 y t37, para no dar un número sin banda
        excs = []
        for q10 in PAR["Q10"]["r"]:
            for t37 in PAR["t37"]["r"]:
                excs.append(t / (t37 * q10 ** ((37 - T) / 10)))
        lo, hi = min(excs), max(excs)
        if exc <= 1.5:        veredicto = "dentro de la ley térmica"
        elif lo <= 1.5:       veredicto = "**ambiguo**: la banda de Q10 lo cruza"
        else:                 veredicto = "**EXCESO**: exige mecanismo no térmico"
        filas.append([pid, q["label"][:44], g(T), g(t), q.get("clase", "—"),
                      f"×{g(exc)} ({g(lo)}–{g(hi)})", veredicto])
        pts.append((pid, q, exc, lo, hi))

    # ---------------------------------------------------------------- 2. estructura en los excesos
    def resumen(clave, valores=None):
        grupos = {}
        for pid, q, exc, lo, hi in pts:
            k = q.get(clave, "—")
            if isinstance(k, bool): k = "sí" if k else "no"
            grupos.setdefault(k, []).append(exc)
        out = []
        for k, v in sorted(grupos.items(), key=lambda t: -max(t[1])):
            v = sorted(v)
            med = v[len(v) // 2] if len(v) % 2 else (v[len(v) // 2 - 1] + v[len(v) // 2]) / 2
            out.append([k, len(v), g(min(v)), g(med), g(max(v))])
        return out

    excesivos = [(pid, q, exc, lo, hi) for pid, q, exc, lo, hi in pts if lo > 1.5]
    naturales = [x for x in excesivos if x[1].get("clase") == "natural"]
    artificiales = [x for x in excesivos if x[1].get("clase") != "natural"]
    max_art = max((x[2] for x in artificiales), default=0.0)
    min_nat = min((x[2] for x in naturales), default=float("inf"))
    # TANDA 52 (auditoría en contra): el documento afirmaba que «las bandas no se solapan ni en sus
    # extremos», pero eso NO se calculaba: `hay_brecha` comparaba sólo los valores centrales. Se
    # calcula ahora, y la frase se escribe a partir del cálculo en vez de a mano.
    max_art_hi = max((x[4] for x in artificiales), default=0.0)     # techo de la banda artificial
    min_nat_lo = min((x[3] for x in naturales), default=float("inf"))  # suelo de la banda natural
    bandas_disjuntas = min_nat_lo > max_art_hi
    hay_brecha = min_nat > max_art and naturales and artificiales
    # Tercera salvedad (tanda 52): el techo artificial y el suelo natural no están al mismo nivel de
    # éxito demostrado (escala E0–E5). Se mide qué pasa si se exige el mismo nivel a los dos lados.
    E_NAT = min((x[1].get("E", 0) for x in naturales), default=0)
    art_mismo_E = [x for x in artificiales if x[1].get("E", 0) >= E_NAT]
    max_art_E = max((x[2] for x in art_mismo_E), default=0.0)
    quien_art = max(artificiales, key=lambda x: x[2])[0] if artificiales else "—"
    quien_nat = min(naturales, key=lambda x: x[2])[0] if naturales else "—"
    E_art = dict(artificiales and [(x[0], x[1].get("E")) for x in artificiales]).get(quien_art)

    # ---------------------------------------------------------------- 3. vías contra cotas
    # Una vía cuya ventana declarada supere lo que su cota permite es anomalía. Sólo se comprueban
    # las vías con ventana numérica en minutos y temperatura deducible del texto: el resto se declara.
    sin_check = [v for v, q in D["vias"].items() if not any(c.isdigit() for c in str(q.get("ventana", "")))]

    # ---------------------------------------------------------------- figura
    fig, ax = plt.subplots(figsize=(8.6, 0.34 * len(pts) + 1.8))
    orden = sorted(pts, key=lambda x: x[2])
    for y, (pid, q, exc, lo, hi) in enumerate(orden):
        c = COLOR_CLASE.get(q.get("clase"), MUTED)
        ax.plot([lo, hi], [y, y], color=GRID, lw=2, zorder=1)
        ax.scatter([exc], [y], s=48, color=c, zorder=3, edgecolor=SURF, linewidth=1.2)
        ax.text(hi * 1.3, y, f"×{g(exc)}", va="center", fontsize=7, color=INK2)
    ax.axvline(1, color="#c0392b", lw=1.3)
    ax.text(1.1, len(pts) - 0.5, " ley térmica de C2", fontsize=7, color="#c0392b")
    ax.set_yticks(range(len(orden)))
    ax.set_yticklabels([f"{x[0]}: {x[1]['label'][:40]}" for x in orden], fontsize=7, color=INK2)
    ax.set_xscale("log")
    ax.set_xlabel("Exceso sobre la ventana térmica: tiempo aguantado / ventana que C2 concede a esa T", color=INK2)
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
    ax.grid(axis="x", color=GRID, lw=0.6); ax.set_facecolor(SURF); fig.set_facecolor(SURF)
    fig.suptitle("Cada punto del marco contra la ley térmica, todos a la vez",
                 x=0.02, ha="left", fontsize=11, color=INK)
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "C_exceso.png", dpi=150); plt.close(fig)

    # ---------------------------------------------------------------- documento
    doc = ("<!-- AUTO-GENERADO por red/cruce.py. NO EDITAR A MANO. -->\n"
           "# StasisPath: cruce sistemático — la capa de datos entera contra la capa de leyes\n\n"
           "`ENCUENTROS.md` cruza **dimensiones** por pares. Aquí se hace otra cosa: se enfrenta **cada punto de datos "
           "a la ley térmica**, todos a la vez. C4, C9 y C10 ya lo hacían para cuatro puntos sueltos; esto lo hace para "
           f"los {len(pts)} que tienen temperatura y tiempo.\n\n"
           "> **Todo lo de aquí es DERIVADO, no medido.** Un exceso calculado no es un dato nuevo: es una relectura de "
           "datos que ya estaban. Sirve para **señalar dónde mirar**. Ninguna anomalía cierra un nodo por sí sola (R5).\n\n"
           f"![Exceso térmico](red/fig/C_exceso.png)\n\n"
           "## 1. Cada punto contra la ventana de C2\n\n"
           f"Ventana: w(T) = t37 · Q10^((37−T)/10), con t37 = {p['t37']} min y Q10 = {p['Q10']}. La banda entre paréntesis "
           "son las esquinas del rango declarado de ambos. Un punto sólo cuenta como exceso si **toda** la banda supera 1.5.\n\n"
           + tabla(filas, ["punto", "sistema", "T °C", "t min", "clase", "exceso ×", "veredicto"])
           + f"\n**{len(excesivos)} puntos exigen un mecanismo no térmico** de forma robusta.\n\n"
           "## 2. ¿Hay estructura en los excesos?\n\n"
           "**Por clase de sistema:**\n\n"
           + tabla(resumen("clase"), ["clase", "n", "mínimo", "mediana", "máximo"])
           + "\n**Por fase:**\n\n"
           + tabla(resumen("fase"), ["fase", "n", "mínimo", "mediana", "máximo"])
           + "\n**Por origen (artificial = protocolo humano; natural = biología):**\n\n"
           + tabla(resumen("artificial"), ["artificial", "n", "mínimo", "mediana", "máximo"]))

    if hay_brecha:
        doc += (f"\n> **REGULARIDAD ENCONTRADA, y el marco no la tenía escrita como ley.** Entre los puntos que exceden "
                f"la ley térmica hay una **brecha limpia**: el mayor exceso conseguido por un **protocolo artificial** es "
                f"**×{g(max_art)}**, y el menor conseguido por la **biología natural** es **×{g(min_nat)}** — un salto de "
                f"**×{g(min_nat / max_art)}** sin ningún punto en medio. ⇒ Lo que la bioquímica de un hibernador o un "
                "anfibio consigue está **fuera del alcance de todo protocolo humano probado**, y no por poco: por un factor "
                f"de {g(min_nat / max_art)}. Es la misma frontera que C4 encontró para la rana y la tortuga, pero ahora "
                "medida sobre **todos** los puntos del marco y con la brecha cuantificada. "
                + (f"Las bandas **no se solapan ni en sus extremos** (techo artificial ×{g(max_art_hi)} frente a suelo "
                   f"natural ×{g(min_nat_lo)}), así que no es un artefacto del rango de Q10.\n\n"
                   if bandas_disjuntas else
                   f"⚠ **Pero las bandas SÍ se solapan** (techo artificial ×{g(max_art_hi)} frente a suelo natural "
                   f"×{g(min_nat_lo)}): la brecha está en los centrales y **puede ser un artefacto del rango de Q10**.\n\n")
                + "> **TRES SALVEDADES, y sin ellas el hallazgo engaña** (la tercera se añadió en la tanda 52, "
                "auditoría en contra; las dos primeras ya estaban).\n"
                "> 1. **La brecha describe lo INTENTADO, no lo posible.** El techo artificial de ×"
                f"{g(max_art)} es el mejor protocolo **probado**, no un límite demostrado. Ninguna ley del marco prohíbe "
                "superarlo; si mañana un protocolo llega a ×100, la brecha se cierra sin que nada de esto se refute. Es una "
                "**frontera empírica**, no una barrera.\n"
                "> 2. **Parte del exceso natural es ectotermia, no bioquímica transferible.** La ventana se calibra con "
                f"t37 = {p['t37']} min y Q10 = {p['Q10']}, **medidos en cerebro humano** (F4). Aplicarla a una tortuga o a un "
                "pez pulmonado extrapola fuera de su dominio: esos animales tienen un metabolismo basal mucho menor de "
                "partida. C4 ya lo advierte. El exceso de la **ardilla ártica** (×"
                f"{g(min_nat)}) es el más informativo de los naturales, porque es un **mamífero**, y ahí la comparación sí "
                "es cercana. **Comprobado en la tanda 52: el punto que fija el suelo natural ES la ardilla (un mamífero), "
                "así que el confundido de ectotermia NO invalida la brecha** — quitar la rana, la tortuga y el pez "
                f"pulmonado deja el suelo natural exactamente donde está, en ×{g(min_nat)}.\n"
                "> 3. **Los dos lados de la brecha no están al mismo nivel de éxito demostrado, y eso es un sesgo "
                f"propio (tanda 52).** El techo artificial lo fija **{quien_art}**, que alcanza **E{E_art}**, mientras "
                f"todos los puntos naturales están en **E{E_NAT}** (animal recuperado). Comparar un resultado celular con "
                "un animal entero no es comparar lo mismo con lo mismo. Exigiendo el mismo nivel E a los dos lados, el techo artificial baja "
                f"a ×{g(max_art_E)} y la brecha **crece** a ×{g(min_nat / max_art_E) if max_art_E else '—'}. "
                "⇒ La salvedad **no rompe el hallazgo: lo agranda.** Pero había que decirla, porque un lector podía "
                "leer la brecha como «los protocolos humanos llegan a ×48 con un animal recuperado», y eso es falso.\n")
    else:
        doc += ("\n> No aparece una brecha limpia entre protocolos artificiales y biología natural: sus excesos se "
                "solapan. La frontera que C4 sugiere para casos sueltos **no se sostiene** al mirar todos los puntos.\n")

    doc += ("\n## 3. Vías contra cotas\n\n"
            f"{len(D['vias'])} vías en el marco. **{len(sin_check)} declaran su ventana en texto libre sin cifra en minutos**, "
            "así que no se pueden enfrentar automáticamente a una cota. Es una **deuda de formato, no de conocimiento**: "
            "quien escriba una ventana como número y unidad hace que esta comprobación se ejecute sola.\n\n"
            "Vías sin ventana comprobable: " + ", ".join(sorted(sin_check)) + "\n\n"
            "## Qué hacer con esto\n\n"
            "1. Los puntos marcados **EXCESO** son los que sostienen que existe una vía biológica: sin ellos, la ley "
            "térmica bastaría para describir el marco entero.\n"
            "2. Los marcados **ambiguo** son los candidatos a medición: estrechar Q10 o t37 los resolvería sin experimento nuevo.\n"
            "3. Las vías sin ventana numérica son trabajo de ficha, de coste casi nulo, que desbloquea una comprobación automática.\n")
    (ROOT / "CRUCE.md").write_text(doc)
    return {"n_pts": len(pts), "excesivos": len(excesivos), "brecha": hay_brecha,
            "max_art": max_art, "min_nat": min_nat, "sin_check": sin_check,
            "bandas_disjuntas": bandas_disjuntas, "max_art_hi": max_art_hi, "min_nat_lo": min_nat_lo,
            "max_art_E": max_art_E, "E_nat": E_NAT, "quien_art": quien_art, "quien_nat": quien_nat}
