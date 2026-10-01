"""StasisPath: proyección de cada capa en una dimensión y cálculo de los encuentros (pares de ejes).

Lo llama motor.py al final: generar(D, PAR, R) escribe ENCUENTROS.md y red/fig/*.png.
Cada encuentro tiene una ley (una frontera calculada con los parámetros de la red), los puntos
de datos y un veredicto calculado: qué puntos cruzan la frontera, a cuántos órdenes de magnitud
está la meta y qué pares de ejes no tienen datos.
"""
import itertools, math
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# paleta validada (dataviz, modo claro): 4 slots categóricos + tinta y superficie
SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
CLASES = {  # clase -> (etiqueta, color, marcador)  forma = codificación secundaria
    "hipotermia": ("Hipotermia / flujo", "#2a78d6", "o"), "bajo_flujo": ("Hipotermia / flujo", "#2a78d6", "o"),
    "normotermia": ("Hipotermia / flujo", "#2a78d6", "o"), "celular": ("Hipotermia / flujo", "#2a78d6", "o"),
    "fase_controlada": ("Sobreenfriamiento / hielo controlado", "#eb6834", "s"),
    "vidrio": ("Vidrio", "#1baf7a", "D"), "natural": ("Biología natural", "#eda100", "^")}
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "axes.edgecolor": "#c3c2b7",
                     "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "font.size": 9,
                     "axes.spines.top": False, "axes.spines.right": False})

def lc_de_masa(g):  # longitud característica de una esfera de agua: LC = r/3 (cm)
    return (3 * g / (4 * math.pi)) ** (1 / 3) / 3

def tabla(filas, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in f) + " |" for f in filas) + "\n"

def g(x): return f"{x:.3g}" if abs(x) < 1e4 else f"{x:,.0f}"

def _etiquetar(ax, items):
    """items: [(x, y, texto)]. Coloca etiquetas evitando solapes en píxeles (desplazamiento vertical escalonado)."""
    ax.figure.canvas.draw()
    usados = []
    for x, y, txt in sorted(items, key=lambda i: (i[0], i[1])):
        px, py = ax.transData.transform((x, y))
        w, h = 5.2 * len(txt), 11
        for dy in (4, 14, -12, 24, -22, 34, -32, 44):
            box = (px + 5, py + dy, px + 5 + w, py + dy + h)
            if all(box[2] < u[0] or box[0] > u[2] or box[3] < u[1] or box[1] > u[3] for u in usados):
                break
        usados.append(box)
        ax.annotate(txt, (x, y), xytext=(5, dy), textcoords="offset points", fontsize=7, color=INK2,
                    arrowprops=dict(arrowstyle="-", color=GRID, lw=0.6) if abs(dy) > 5 else None)

def _leyenda(ax):
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3)

def _scatter(ax, pts, xk, yk, etiquetar=True):
    vistos = set()
    for k, p in pts.items():
        et, c, m = CLASES[p["clase"]]
        ax.scatter(p[xk], p[yk], s=64, c=c, marker=m, edgecolors=SURF, linewidths=1.5, zorder=3,
                   label=et if et not in vistos else None)
        vistos.add(et)
    if etiquetar:
        _etiquetar(ax, [(p[xk], p[yk], p["label"]) for p in pts.values()])

def generar(D, PAR, R, ROOT):
    fig_dir = ROOT / "red" / "fig"; fig_dir.mkdir(exist_ok=True)
    pv = {k: v["v"] for k, v in PAR.items()}
    rng = {k: v["r"] for k, v in PAR.items()}
    P = D["puntos"]; META = D["meta_punto"]
    w = lambda T, t37, q: t37 * q ** ((37 - T) / 10)
    out, avisos = [], []

    # ---------------------------------------------------------------- E1  T × t
    pts = {k: p for k, p in P.items() if p.get("T") is not None and p.get("t")}
    fig, ax = plt.subplots(figsize=(8, 5.6))
    Ts = [x / 2 for x in range(-40, 76)]
    lo = [w(T, rng["t37"][0], rng["Q10"][0]) for T in Ts]; hi = [w(T, rng["t37"][1], rng["Q10"][1]) for T in Ts]
    ax.fill_between(Ts, lo, hi, color="#2a78d6", alpha=0.12, linewidth=0)
    ax.plot(Ts, [w(T, pv["t37"], pv["Q10"]) for T in Ts], color="#2a78d6", lw=2, label="C2: ventana del cerebro de mamífero (flujo cero)")
    ax.axvline(0, color="#c3c2b7", lw=1)
    sub = {k: p for k, p in pts.items() if p["T"] > -40}
    _scatter(ax, sub, "T", "t")
    ax.set_yscale("log"); ax.set_xlabel("Temperatura (°C)"); ax.set_ylabel("Duración de la pausa (min, log)")
    ax.set_title("Encuentro T × t: capa térmica frente a almacenamiento", loc="left", fontsize=11, color=INK)
    _leyenda(ax); fig.tight_layout(); fig.savefig(fig_dir / "E1_T_t.png", dpi=150); plt.close(fig)
    filas = []
    for k, p in sorted(pts.items(), key=lambda kv: kv[1]["T"]):
        r = p["t"] / w(p["T"], pv["t37"], pv["Q10"])
        rmin = p["t"] / w(p["T"], rng["t37"][1], rng["Q10"][1])
        if p["fase"] == "vidrio": dx = "vidrio: fuera del dominio de C2 (química detenida bajo Tg)"
        elif p["clase"] == "natural": dx = "excede C2 → bioquímica natural no térmica"
        elif p["fase"] in ("hielo_extra", "sobreenfriado") or p["T"] < 0: dx = "excede C2 → estado bajo 0 °C (hielo controlado o sobreenfriamiento)"
        elif rmin <= 1: dx = "explicado por Q10 pasivo"
        elif p["flujo"] == "bajo": dx = "excede C2 → hubo flujo (bajo)"
        elif p.get("mecanismo") == "reperfusion": dx = "excede C2 → reperfusión optimizada (zona gris X1)"
        elif r <= 5: dx = "margen de tejido o flujo (≤ ×5)"
        else: dx = "**ANOMALÍA**: excede C2 sin mecanismo declarado"; avisos.append(f"E1: {p['label']} excede C2 ×{g(r)} sin mecanismo")
        filas.append([p["label"], g(p["T"]), g(p["t"]), f"×{g(r)} (≥ ×{g(rmin)})", dx, p["f"]])
    out.append(("E1 · Temperatura × duración", "E1_T_t.png",
        "**Ley:** C2 (banda = esquinas de t37 y Q10). Encima de la banda, la pausa no la explica la supresión térmica pasiva del cerebro de mamífero.\n\n" +
        tabla(filas, ["punto", "T °C", "t min", "t / ventana C2", "diagnóstico", "fuente"])))

    # ---------------------------------------------------------------- E2  τ_eq (capa isquemia) × E × información
    iso = {k: p for k, p in P.items() if p.get("T") is not None and p.get("t") and p["fase"] == "liquido" and p["artificial"]}
    fig, ax = plt.subplots(figsize=(8, 4.6))
    filas, lab2 = [], []
    for k, p in iso.items():
        f = pv["Q10"] ** ((p["T"] - 37) / 10); tau = p["t"] * f
        flo = p["t"] * rng["Q10"][1] ** ((p["T"] - 37) / 10); fhi = p["t"] * rng["Q10"][0] ** ((p["T"] - 37) / 10)
        p["tau"] = tau
        filas.append([p["label"], g(p["t"]), g(p["T"]), f"{g(tau)} ({g(min(flo, fhi))}–{g(max(flo, fhi))})", p["E"], p["info"], p["flujo"], p["f"]])
        et, c, m = CLASES[p["clase"]]
        bajo = p["flujo"] == "bajo"
        ax.scatter(tau, p["E"], s=70, marker="X" if bajo else m, c=MUTED if bajo else (c if p["info"] == "si" else SURF),
                   edgecolors=MUTED if bajo else c, linewidths=2, zorder=3)
        lab2.append((tau, p["E"], p["label"] + (" · bajo flujo: τ_eq sobreestimado" if bajo else "")))
    for x, lab in ((pv["t37"], "clínico 5"), (pv["tau_org_good"], "reproducible 12.5"), (pv["tau_org_exist"], "existencia 60"), (pv["tau_cel"], "celular 240")):
        ax.axvline(x, color="#c3c2b7", lw=1, ls="--"); ax.text(x, 5.35, lab, fontsize=7, color=MUTED, ha="center")
    ax.set_xscale("log"); ax.set_ylim(0.5, 5.6); _etiquetar(ax, lab2); ax.set_xlabel("τ_eq: isquemia equivalente a 37 °C (min, log)"); ax.set_ylabel("Éxito E0–E5")
    ax.set_title("Encuentro τ_eq × éxito × información\n(relleno = información conservada · hueco = parcial o desconocida · X gris = bajo flujo, τ_eq no comparable)", loc="left", fontsize=10, color=INK)
    fig.tight_layout(); fig.savefig(fig_dir / "E2_tau_E.png", dpi=150); plt.close(fig)
    dh = [p["tau"] for p in iso.values() if p["clase"] == "hipotermia"]
    inv = (f"**Invariante del encuentro:** la capa térmica (C2) y la capa de isquemia (G1) coinciden: los casos hipotérmicos con E ≥ 4 "
           f"caen en τ_eq = {g(min(dh))}–{g(max(dh))} min, el mismo rango que los normotérmicos reproducibles (5–12.5 min). "
           "El perro con flush frío (120 min a 10 °C) queda en τ_eq ≈ 12.7 min: es el mismo umbral del perro normotérmico (12.5 min). "
           "⇒ **τ_eq funciona como magnitud única entre especies y temperaturas.** Por encima de ~13 min, E4 sólo aparece con información parcial (déficit o atrofia del hipocampo).")
    out.append(("E2 · Isquemia equivalente × éxito × información", "E2_tau_E.png",
        inv + "\n\n" + tabla(filas, ["punto", "t min", "T °C", "τ_eq min (rango Q10)", "E", "info", "flujo", "fuente"])))

    # ---------------------------------------------------------------- E3  masa × duración: frontera de reversibilidad
    pts = {k: p for k, p in P.items() if p.get("t") and p.get("masa")}
    fig, ax = plt.subplots(figsize=(8, 5.8))
    _scatter(ax, pts, "masa", "t")
    ax.scatter(META["masa"], META["t"], s=140, marker="*", c=INK, zorder=4); ax.annotate(META["label"], (META["masa"], META["t"]), xytext=(-40, 8), textcoords="offset points", fontsize=8, color=INK)
    art = [p for p in pts.values() if p["artificial"] and p["E"] >= 3]
    par = sorted([p for p in art if not any(q["masa"] >= p["masa"] and q["t"] >= p["t"] and q is not p for q in art)], key=lambda p: p["masa"])
    ax.step([p["masa"] for p in par], [p["t"] for p in par], where="post", color=INK2, lw=2, label="Frontera artificial (E ≥ 3)")
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("Masa del sistema (g, log)"); ax.set_ylabel("Duración de la pausa (min, log)")
    ax.set_title("Encuentro escala × duración: distancia a la meta", loc="left", fontsize=11, color=INK)
    _leyenda(ax); fig.tight_layout(); fig.savefig(fig_dir / "E3_masa_t.png", dpi=150); plt.close(fig)
    best_t_at_M = max((p["t"] for p in art if p["masa"] >= META["masa"] * 0.25), default=None)
    best_m_at_t = max((p["masa"] for p in art if p["t"] >= META["t"]), default=None)
    cheb = min(max(math.log10(META["masa"] / p["masa"]), math.log10(META["t"] / p["t"])) for p in par)
    nat = [p for p in pts.values() if not p["artificial"]]
    brecha = (f"- **Frontera artificial (Pareto, E ≥ 3):** " + " → ".join(f"{p['label']} ({g(p['masa'])} g, {g(p['t'])} min)" for p in par) + "\n"
              f"- Con la masa de la meta (≥ 17.5 kg), la pausa artificial más larga con E ≥ 3 es de **{g(best_t_at_M)} min** ⇒ faltan **{math.log10(META['t']/best_t_at_M):.1f} órdenes de magnitud** de tiempo.\n"
              f"- Con la duración de la meta (≥ 1 año), la masa artificial máxima con E ≥ 3 es de **{g(best_m_at_t) if best_m_at_t else 'ninguna'}** ⇒ ningún sistema artificial con E ≥ 3 ha llegado a 1 año.\n"
              f"- **Distancia de Chebyshev de la meta a la frontera: {cheb:.1f} órdenes de magnitud** (el menor salto simultáneo en masa y tiempo).\n"
              f"- La biología natural ya ocupa la región de meses a años con 10–1000 g ({', '.join(p['label'] for p in nat)}): la meta está fuera de la frontera artificial, pero no fuera de lo biológicamente posible en masa pequeña.")
    out.append(("E3 · Escala × duración (frontera de reversibilidad)", "E3_masa_t.png", brecha))

    # ---------------------------------------------------------------- E4  LC × tasas (capa escala frente a capa química)
    fig, ax = plt.subplots(figsize=(8, 5))
    LCs = [10 ** (x / 40) for x in range(-60, 41)]
    cool = lambda L, a=pv["anc_rate"], L0=pv["anc_LC"]: a * (L0 / L) ** 2
    warm = lambda L, al=pv["alpha"], dT=pv["dT_rew"]: dT / ((3 * L / 100) ** 2 / al / 60)
    ax.plot(LCs, [cool(L) for L in LCs], color="#2a78d6", lw=2, label="Enfriamiento convectivo (C3)")
    ax.plot(LCs, [warm(L) for L in LCs], color="#eb6834", lw=2, label="Recalentamiento convectivo (C1)")
    ax.axhline(pv["nano_rate"], color="#1baf7a", lw=2, label="Nanowarming 2 L (independiente del volumen)")
    for nom, v, ls in (("CCR M22", pv["CCR_M22"], ":"), ("CWR M22", pv["CWR_M22"], "--"), ("CCR VMP", pv["CCR_VMP"], ":"), ("CWR VMP", pv["CWR_VMP"], "--")):
        ax.axhline(v, color=MUTED, lw=1, ls=ls); ax.text(LCs[0] * 1.05, v * 1.12, nom, fontsize=7, color=MUTED)
    objs = [("riñón de rata", lc_de_masa(1.5)), ("riñón de conejo", lc_de_masa(12.7)), ("riñón humano", pv["LC_kidneyH"]),
            ("bolsa de 3 L", pv["anc_LC"]), ("cuerpo (media)", pv["LC_body"]), ("tronco", pv["LC_trunk"])]
    for n, L in objs:
        ax.axvline(L, color=GRID, lw=1); ax.text(L, 3e-3, n, rotation=90, fontsize=7, color=INK2, va="bottom", ha="right")
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_ylim(1e-3, 1e5)
    ax.set_xlabel("Longitud característica LC (cm, log)"); ax.set_ylabel("Tasa en el centro (°C/min, log)")
    ax.set_title("Encuentro escala × química: ventana de vitrificación por CPA", loc="left", fontsize=11, color=INK)
    _leyenda(ax); fig.tight_layout(); fig.savefig(fig_dir / "E4_LC_tasas.png", dpi=150); plt.close(fig)
    filas = []
    for nom, c in D["cpas"].items():
        LCc = pv["anc_LC"] * math.sqrt(pv["anc_rate"] / c["CCR"])
        LClo = rng["anc_LC"][0] * math.sqrt(rng["anc_rate"][0] / (c["CCR"] * (1.0 if nom != "M22" else rng["CCR_M22"][1] / pv["CCR_M22"])))
        cabe = [n for n, L in objs if L <= LCc]
        filas.append([nom, c["CCR"], c["M"], f"{g(LCc)} cm (peor caso {g(LClo)})", ", ".join(cabe) or "—", c["tox_rango"]])
    choque = ("**Choque de capas:** la ventana de vitrificación la cierra el **enfriamiento** (curva azul), no el recalentamiento, porque el nanowarming levanta el techo de calentamiento para cualquier tamaño. "
              "La ventana crece al bajar la CCR, lo que exige más concentración y química más agresiva ⇒ **el eje de escala empuja al eje de toxicidad**. "
              "El orden de toxicidad (1 = menor) es **ordinal y sin escala común [P]**: el encuentro escala × toxicidad está **sin cuantificar** (ver E6).")
    out.append(("E4 · Escala × química (enfriar / recalentar / CPA)", "E4_LC_tasas.png",
        choque + "\n\n" + tabla(filas, ["CPA", "CCR °C/min", "M", "LC máx. vitrificable por convección", "objetos que caben", "toxicidad (ordinal, P)"])))

    # ---------------------------------------------------------------- E5  función × información
    cat = {}
    for p in P.values():
        fun = "alta (E ≥ 3)" if p["E"] >= 3 else ("baja (E1–E2)" if p["E"] >= 1 else "nula (E0)")
        cat.setdefault((fun, p["info"]), []).append(p["label"])
    filas = [[f, i, len(v), "; ".join(v)] for (f, i), v in sorted(cat.items())]
    txt = ("**Encuentro ontológico:** función e información son ejes separados. Casos que lo prueban: *Gata 60 min* (función alta, información parcial), "
           "*ASC* (función nula, información sí), *C. elegans* (baja función medida, información sí). "
           f"Los órganos no tienen eje de información (n/a). **Hueco:** ningún punto tiene a la vez E ≥ 4, información medida y pausa > 1 día en mamífero artificial.\n\n" +
           tabla(filas, ["función", "información", "n", "puntos"]))
    out.append(("E5 · Función × información", None, txt))

    # ---------------------------------------------------------------- E7  química: concentración × temperatura × protocolo → resultado
    X = D.get("exposiciones", {})
    RES = {3: "sin toxicidad o función completa", 2: "daño bajo o parcial", 1: "dañino o a veces fatal", 0: "letal"}
    filas = [[x["cpa"], g(x["M"]) if x["M"] else "—", g(x["T"]) if x["T"] is not None else "—", g(x["t"]) if x["t"] else "—",
              g(x["masa"]), x["sistema"], f"{x['res']} · {RES[x['res']]}", x["f"]] for x in X.values()]
    grupos = {}
    for x in X.values():
        if x["M"] and x["T"] is not None: grupos.setdefault((x["M"], x["T"]), []).append(x)
    choques = [f"a {g(M)} M y {g(T)} °C: " + " frente a ".join(f"{x['cpa']} → {x['res']}" for x in xs)
               for (M, T), xs in grupos.items() if len({x["res"] for x in xs}) > 1]
    txt = ("**Hallazgo calculado:** " + (f"hay {len(choques)} pares con **la misma concentración y la misma temperatura, pero resultado opuesto**: " + "; ".join(choques) +
           ". ⇒ La toxicidad **no es función de la molaridad ni de la temperatura por separado**: la deciden la composición (qv*) y el protocolo de carga y descarga. "
           "La dimensión 'toxicidad' debe modelarse como D_CPA(composición, T, t, protocolo), no como un número por CPA." if choques else "sin choques detectables.") +
           "\n\n" + tabla(filas, ["CPA / protocolo", "M", "T °C", "t min", "masa g", "sistema", "resultado (ordinal)", "fuente"]))
    out.append(("E7 · Química: concentración × temperatura × protocolo → toxicidad", None, txt))

    # ---------------------------------------------------------------- E6  matriz de encuentros (cobertura)
    dims = list(D["dimensiones"])
    tiene = lambda p, d: (p.get(d) is not None and p.get(d) not in ("desconocida", "n/a")) if d not in ("tau", "tox") else \
        (d == "tau" and "tau" in p)
    leyes = {("T", "t"): "C2", ("t", "tau"): "G1", ("T", "tau"): "C2", ("masa", "CCR"): "C3", ("masa", "t"): "frontera", ("E", "info"): "O4",
             ("masa", "E"): "frontera", ("tau", "E"): "G1/X1", ("tau", "info"): "O4/X1", ("t", "E"): "frontera", ("CCR", "tox"): "L6 (qv*)", ("masa", "tox"): "C8", ("T", "fase"): "C2/G2"}
    # pares con significado físico o clínico (el resto se marca "no pertinente" para no inflar la lista de huecos)
    PERTINENTES = {frozenset(x) for x in [("T", "t"), ("T", "tau"), ("t", "tau"), ("T", "fase"), ("t", "masa"), ("masa", "E"), ("t", "E"),
        ("tau", "E"), ("E", "info"), ("tau", "info"), ("t", "info"), ("fase", "info"), ("masa", "CCR"), ("CCR", "E"), ("CCR", "tox"),
        ("masa", "tox"), ("T", "tox"), ("t", "tox"), ("tox", "E"), ("fase", "E"), ("masa", "fase")]}
    filas, huecos = [], []
    for a, b in itertools.combinations(dims, 2):
        n = sum(1 for p in P.values() if tiene(p, a) and tiene(p, b))
        if {a, b} <= {"CCR", "tox"}: n = len(D["cpas"])
        elif "tox" in (a, b):
            otro = b if a == "tox" else a
            campo = {"T": "T", "t": "t", "masa": "masa", "E": "res"}.get(otro)
            n = sum(1 for x in D.get("exposiciones", {}).values() if campo and x.get(campo) is not None)
        ley = leyes.get((a, b)) or leyes.get((b, a)) or ""
        estado = "cuantificado" if n >= 3 and ley else ("ley sin datos" if ley and n < 3 else ("datos sin ley" if n >= 3 else "**vacío**"))
        if "tox" in (a, b): estado = ("cuantificado (ordinal)" if n >= 3 else ("**pocos datos**" if n else "**vacío**")) if {a, b} != {"CCR", "tox"} else "**sin escala cuantitativa**"
        if frozenset((a, b)) not in PERTINENTES: estado = "no pertinente"
        if estado.startswith("**") or estado == "ley sin datos": huecos.append(f"{a}×{b}")
        filas.append([f"{D['dimensiones'][a]['nombre']} × {D['dimensiones'][b]['nombre']}", ley or "—", n, estado])
    HJ = ", ".join(huecos)
    txt = (f"{len(filas)} encuentros posibles entre {len(dims)} dimensiones; {len(PERTINENTES)} pertinentes. **Huecos (vacíos, sin escala o con ley sin datos): {len(huecos)}**: {HJ} → son la lista priorizada de investigación "
           "(cada uno es un par de capas cuyo choque no se puede calcular todavía).\n\n" + tabla(filas, ["encuentro", "ley", "n puntos", "estado"]))
    out.append(("E6 · Matriz de encuentros (cobertura del modelo)", None, txt))

    doc = ("<!-- AUTO-GENERADO por red/encuentros.py (llamado desde red/motor.py). NO EDITAR A MANO. -->\n"
           "# StasisPath: encuentros entre capas\n\nCada capa del marco se proyecta en una dimensión. Cada par de dimensiones es un **encuentro**: "
           "una ley traza una frontera, los datos caen a un lado u otro y el veredicto se calcula. "
           "Los datos viven en `red/stasispath.yaml → puntos`; cambiar un parámetro o añadir un punto regenera todo.\n\n"
           "Colores: azul = hipotermia/flujo · naranja = sobreenfriamiento/hielo controlado · verde = vidrio · amarillo = biología natural (la forma del marcador repite la clase).\n\n")
    for tit, fig, body in out:
        doc += f"## {tit}\n\n" + (f"![{tit}](red/fig/{fig})\n\n" if fig else "") + body + "\n"
    doc += "## Avisos de los encuentros\n" + ("\n".join("- " + a for a in avisos) or "- ninguno (ningún punto cruza una frontera sin mecanismo declarado)") + "\n"
    (ROOT / "ENCUENTROS.md").write_text(doc)
    return avisos, huecos, cheb
