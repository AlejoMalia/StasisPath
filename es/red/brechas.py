"""StasisPath: brechas al humano. Triangulación entre especies + regla de tres generalizada.

Lo llama motor.py: generar(D, PAR, R, ROOT) escribe BRECHAS.md y red/fig/B_brechas.png.
Por cada apartado: proyecta cada observación animal al humano con su ley de escala,
triangula (n especies independientes, mediana o mejor valor, dispersión), mide cuántos
órdenes de magnitud faltan y los convierte en %. Cada vía hacia la meta se evalúa por su
cuello de botella (ley del mínimo): todos los apartados son necesarios a la vez.
"""
import math, statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID, BLUE, ORANGE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#2a78d6", "#eb6834"

def g(x): return f"{x:.3g}" if abs(x) < 1e4 else f"{x:,.0f}"
def tabla(filas, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in f) + " |" for f in filas) + "\n"

def generar(D, PAR, R, ROOT):
    Mh = D["humano"]["masa"]
    res = {}
    for bid, b in D["brechas"].items():
        meta = b["meta"]
        if isinstance(meta, str):                       # meta calculada por una cota de la red
            c, o = meta.split("."); meta = R[c]["out"][o]
        proy = []
        for o in b["obs"]:
            vh = o["v"] * (Mh / o["M"]) ** o["b"]
            proy.append({**o, "vh": vh})
        F = {"max": max, "min": min, "mediana": statistics.median}[b["agregado"]]
        firmes = [p for p in proy if not p.get("disputado")]
        vals = [p["vh"] for p in (firmes or proy)]
        agg = F(vals)
        agg_con = F([p["vh"] for p in proy])
        hay_disp = len(firmes) < len(proy)
        esp = {p["e"].split(" (")[0] for p in proy}
        if b["modo"] == "mayor":
            rest = max(0.0, math.log10(meta / agg)); logr = math.log10(agg / b["base"])
        else:
            rest = max(0.0, math.log10(agg / meta)); logr = math.log10(b["base"] / agg)
        logr = max(logr, 0.0)
        pct = 100.0 if rest == 0 else 100 * logr / (logr + rest)
        if b["modo"] == "mayor":
            rest_c = max(0.0, math.log10(meta / agg_con)); lg_c = max(math.log10(agg_con / b["base"]), 0.0)
        else:
            rest_c = max(0.0, math.log10(agg_con / meta)); lg_c = max(math.log10(b["base"] / agg_con), 0.0)
        pct_con = 100.0 if rest_c == 0 else 100 * lg_c / (lg_c + rest_c)
        res[bid] = dict(b=b, meta=meta, proy=proy, agg=agg, rest=rest, pct=pct, n=len(esp),
                        hay_disp=hay_disp, agg_con=agg_con, pct_con=pct_con, rest_con=rest_c,
                        disp=(max(vals) / min(vals)) if min(vals) > 0 else float("inf"))

    # rutas: ley del mínimo
    rutas = {}
    for via, nom in (("fisica", "Vía física (vitrificación → años)"), ("biologica", "Vía biológica (torpor → meses a 1 año)")):
        ids = [k for k, r in res.items() if via in r["b"]["via"]]
        cuello = min(ids, key=lambda k: res[k]["pct"])
        gm = math.exp(sum(math.log(max(res[k]["pct"], 1)) for k in ids) / len(ids))
        rutas[via] = dict(nom=nom, ids=ids, cuello=cuello, gm=gm)

    # potencia de nanowarming por regla de tres lineal (nota de B6)
    pot70 = 120 * (Mh / 1000 / 2) * (PAR["CWR_M22"]["v"] / PAR["nano_rate"]["v"])

    # ---- figura
    orden = sorted(res, key=lambda k: res[k]["pct"])
    fig, ax = plt.subplots(figsize=(8.5, 0.42 * len(orden) + 1.4))
    ys = range(len(orden))
    cuellos = {r["cuello"] for r in rutas.values()}
    for y, k in zip(ys, orden):
        r = res[k]
        ax.barh(y, 100, color=GRID, height=0.55, zorder=1)
        ax.barh(y, r["pct"], color=ORANGE if k in cuellos else BLUE, height=0.55, zorder=2)
        ax.text(min(r["pct"], 100) + 1.2, y, f"{r['pct']:.0f} %" + (f" · faltan {r['rest']:.1f} órdenes" if r["rest"] > 0 else " · alcanzado"),
                va="center", fontsize=7.5, color=INK2)
    ax.set_yticks(list(ys)); ax.set_yticklabels([f"{k} · " + (res[k]['b']['nombre'] if len(res[k]['b']['nombre']) <= 46 else res[k]['b']['nombre'][:45] + "…") for k in orden], fontsize=7.5, color=INK2)
    ax.set_xlim(0, 135); ax.set_xticks([0, 25, 50, 75, 100]); ax.set_xlabel("% del camino hasta el humano (escala logarítmica de órdenes de magnitud)")
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.grid(axis="y", visible=False); ax.set_facecolor(SURF); fig.set_facecolor(SURF)
    fig.suptitle("Brechas al humano por apartado\nnaranja = cuello de botella de una vía (física: B8 · biológica: B10m)", x=0.02, ha="left", fontsize=11, color=INK)
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "B_brechas.png", dpi=150); plt.close(fig)

    # ---- documento
    doc = ("<!-- AUTO-GENERADO por red/brechas.py (llamado desde red/motor.py). NO EDITAR A MANO. -->\n"
           "# StasisPath: brechas al humano (triangulación + regla de tres generalizada)\n\n"
           "**Qué mide esto y qué no:** el progreso del *marco* (conocimiento) está en MARCO.md. Aquí se mide **cuánto camino tecnológico falta hasta la meta humana** "
           "en cada apartado. El marco puede llegar al 100 % (saber exactamente qué falta y por qué) con la tecnología todavía lejos.\n\n"
           "**Método:** cada dato animal se proyecta al humano con la ley de escala del apartado, v_h = v·(M_h/M)^b: b = 0 invariante (τ_eq, tiempo bajo Tg), "
           "b = 1 lineal (energía, potencia), b = 0.25 Kleiber (autonomía de reservas). La regla de tres *lineal* sólo se usa donde la física es lineal: "
           "escalar el enfriamiento de un riñón de rata (1.5 g) a 70 kg con regla de tres lineal daría una tasa ~36 veces menor que la correcta (M^−2/3). "
           "% = órdenes logrados / (logrados + restantes), con base declarada en cada fila. **Triangulación:** n = especies o sistemas independientes (n < 3 ⇒ débil).\n\n")
    doc += "![Brechas](red/fig/B_brechas.png)\n\n## Rutas hacia la meta (ley del mínimo: todos los apartados a la vez)\n\n"
    for via, rt in rutas.items():
        c = res[rt["cuello"]]
        doc += (f"- **{rt['nom']}:** cuello de botella **{rt['cuello']} · {c['b']['nombre']}** con **{c['pct']:.0f} %** "
                f"(faltan {c['rest']:.1f} órdenes de magnitud). Media geométrica de sus apartados: {rt['gm']:.0f} %.\n")
    doc += "\n## Apartados\n\n"
    filas = []
    for k in sorted(res, key=lambda k: res[k]["pct"]):
        r = res[k]; b = r["b"]
        marca = f" · con disputado: {g(r['agg_con'])} → {r['pct_con']:.0f} %" if r["hay_disp"] else ""
        filas.append([k, b["nombre"], f"{g(r['meta'])} {b['u']}", f"{g(r['agg'])} ({b['agregado']}){marca}", f"{r['rest']:.2f}",
                      f"**{r['pct']:.0f} %**", f"{r['n']}" + (" ⚠ débil" if r["n"] < 3 else ""), g(b["base"])])
    doc += tabla(filas, ["id", "apartado", "meta humana", "proyección triangulada", "órdenes restantes", "% camino", "n", "base"])
    doc += "\n## Detalle de la proyección (animal → humano)\n\n"
    for k in sorted(res):
        r = res[k]; b = r["b"]
        doc += f"### {k} · {b['nombre']}\n"
        if b.get("nota"): doc += b["nota"].replace("{pot70}", f"{pot70:.0f}") + "\n\n"
        doc += tabla([[p["e"], g(p["v"]), g(p["M"]), p["b"], g(p["vh"]), p["f"]] for p in r["proy"]],
                     ["observación", f"valor ({b['u']})", "masa g", "exponente b", "proyectado al humano", "fuente"])
        doc += f"Dispersión de la triangulación: ×{g(r['disp'])} entre la mayor y la menor proyección.\n\n"
    doc += ("## Cómo atacar los agujeros\n\nOrdenados por **órdenes de magnitud restantes** (el mayor es el que más limita):\n\n" +
            "\n".join(f"{i+1}. **{k}** ({res[k]['rest']:.1f} órdenes): {res[k]['b']['nombre']}" for i, k in
                      enumerate(sorted([k for k in res if res[k]["rest"] > 0], key=lambda k: -res[k]["rest"]))) + "\n")
    (ROOT / "BRECHAS.md").write_text(doc)
    return res, rutas
