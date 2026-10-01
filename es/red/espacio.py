"""StasisPath: el espacio de respuestas de X2 — catalogar en vez de dejar en blanco.

X2 pregunta si existe una química que **vitrifique a escala humana Y conserve la función**.
Dejarlo como hueco en blanco desaprovecha lo que el marco ya sabe: cada química conocida
ocupa un punto con coordenadas MEDIDAS en dos ejes, y el hueco tiene forma y tamaño.

Este módulo no inventa el dato que falta. Hace tres cosas que sí se pueden hacer:

  1. **Cataloga** cada química del marco con sus dos coordenadas: CCR medida (¿vitrifica a
     escala?) y nivel funcional demostrado en la escala E0–E5 (¿conserva la función?).
  2. **Mide el hueco**: qué región del plano debe ocupar una respuesta a X2, qué químicas
     están más cerca por cada eje, y por cuánto fallan.
  3. **Prueba si la región objetivo está EXCLUIDA por alguna ley del marco.** Si lo estuviera,
     X2 quedaría cerrada por imposibilidad demostrada, como se cerró V15 (patrón L43). Si no
     lo está, X2 sigue abierta — pero se sabe exactamente qué tiene que cumplir un candidato.

Límite declarado, y es el que impide que esto se convierta en teatro: **una predicción del
marco NO es un dato**. El marco ya predice el resultado del brazo C de P19 (DERIVACION.md da
daño 0.142, y los dos caminos de I1 predicen PASA). Esa predicción es justamente **lo que el
experimento pone a prueba**; contarla como dato cerraría el bucle sobre sí mismo y el marco
dejaría de poder equivocarse. Por eso aquí las columnas de predicción y de medición van
separadas y NUNCA se suman.

Salida: ESPACIO.md + red/fig/X_espacio.png. Lo llama motor.py.
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"

# Escala de éxito del marco (00_marco y Q3): qué se ha demostrado, no qué se espera.
NIVEL = {0: "E0 estructura", 1: "E1 células viables", 2: "E2 tejido funcional",
         3: "E3 órgano trasplantado", 4: "E4 animal reanimado", 5: "E5 humano"}

# Catálogo: cada química con su CCR medida y el MÁXIMO nivel funcional DEMOSTRADO con ella
# en tejido neural. CCR en °C/min. "e_neural" es el nivel alcanzado EN TEJIDO NEURAL, que es
# lo que X2 pregunta; "e_otro" es lo logrado en otro tejido, que no responde a X2.
CPAS = [
    # nombre,          CCR,    M,     e_neural, e_otro, fuente,      nota
    ("M22",            0.10,   9.30,  0,        3,      "F2,F47,F5", "único con CCR que escala; en neural SÓLO ultraestructura (F47), sin prueba de función"),
    ("VM3",            3.00,   8.90,  None,     None,   "F37b",      "V3 + bloqueadores de hielo; sin prueba funcional en neural publicada"),
    ("VS55 tej.",      1.00,   8.40,  None,     1,      "F3",        "tóxico en riñón de rata"),
    ("VS55 sol.",      2.50,   8.40,  None,     1,      "F3",        ""),
    ("V3",             5.40,   8.42,  2,        None,   "F46,F71",   "ÚNICO con función neural medida: LTP 138.1 % vs control 157.7 % (n.s.)"),
    ("VMP",            5.40,   8.40,  None,     3,      "F1,F3",     "riñón de rata trasplantado; no probado en neural"),
    ("EG 61 % solo",   5.40,   None,  1,        None,   "F52,F71",   "fEPSP recuperados pero SIN potenciación estable ⇒ no llega a E2"),
    ("MEDY",           None,   None,  2,        None,   "F35",       "NO vitrifica: congelación lenta con CPA diluido, escala de milímetros"),
    ("NADES 50 %",     30.0,   None,  None,     1,      "F80",       "CCR > 30 MEDIDA (cristalizan en DSC); sólo líneas celulares"),
    ("agua pura",      3.84e8, 0.0,   None,     None,   "F76",       "extremo de concentración cero"),
]

def g(x):
    if x is None: return "—"
    return f"{x:.3g}" if abs(x) < 1e4 else f"{x:.2e}"

def tabla(filas, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in f) + " |" for f in filas) + "\n"

def generar(D, PAR, DERIV, ROOT):
    p = {k: v["v"] for k, v in PAR.items()}
    # TANDA 52 (auditoría en contra, R4 casilla del impostor): la tabla CPAS tenía la CCR de M22, de
    # VS55 y de VMP ESCRITAS A MANO, duplicando parámetros que ya viven en `parametros`. Si el valor
    # del YAML cambiara —por ejemplo al etiquetar `CCR_M22` como de tejido, que es la laguna abierta—
    # este documento no se enteraría. No se mueve ningún valor: se COMPRUEBA que coinciden y, si no,
    # se declara en el documento en vez de callarlo.
    _espejo = {"M22": "CCR_M22", "VS55 sol.": "CCR_VS55", "VMP": "CCR_VMP"}
    desfase = [(nom, ccr, PAR[k]["v"]) for nom, ccr, *_ in CPAS
               for k in [_espejo.get(nom)] if k and abs(ccr - PAR[k]["v"]) > 1e-9]
    # Umbral de CCR para vitrificar un cerebro humano por convección (L44, invirtiendo C3)
    LCe = DERIV["LC_esfera"]
    lc_cerebro = LCe(D["humano"]["cerebro"])
    ccr_req = p["anc_rate"] * (p["anc_LC"] / lc_cerebro) ** p["exp_LC"]
    E_REQ = 2   # X2 exige al menos función de tejido (E2): LTP conservada

    # --- 1. catálogo
    filas = []
    for nom, ccr, M, en, eo, f, nota in CPAS:
        ok_ccr = (ccr is not None and ccr <= ccr_req)
        ok_fun = (en is not None and en >= E_REQ)
        veredicto = ("**RESUELVE X2**" if (ok_ccr and ok_fun) else
                     ("vitrifica, falta función" if ok_ccr else
                      ("función, no vitrifica" if ok_fun else "ninguna de las dos")))
        filas.append([nom, g(ccr), g(M), (NIVEL[en].split()[0] if en is not None else "—"),
                      (NIVEL[eo].split()[0] if eo is not None else "—"), f, veredicto])

    # --- 2. el hueco: quién está más cerca por cada eje y por cuánto falla
    con_ccr = [(n, c) for n, c, *_ in CPAS if c is not None and c <= ccr_req]
    con_fun = [(n, e) for n, c, M, e, *_ in CPAS if e is not None and e >= E_REQ]
    # la que mejor CCR tiene entre las que SÍ tienen función neural
    mejor_fun = min([(c, n) for n, c, M, e, *_ in CPAS if e is not None and e >= E_REQ and c is not None],
                    default=(None, None))
    falta_ccr = (mejor_fun[0] / ccr_req) if mejor_fun[0] else None

    # --- 3. ¿alguna ley del marco EXCLUYE la región objetivo?
    #     La región objetivo es CCR ≤ ccr_req con función E2 en neural. Se pregunta si el marco
    #     contiene alguna ley que la prohíba. La candidata sería una relación CCR↔toxicidad que
    #     obligara a que CCR baja ⇒ toxicidad letal. L20/L25/E7 dicen lo contrario: la toxicidad
    #     depende del cuádruple (composición, temperatura, tiempo, protocolo), NO de la molaridad
    #     sola. Por eso M22 a −22 °C y V3 a 10 °C son puntos distintos del espacio, no el mismo.
    excluida = False
    razon_exclusion = (
        "**NO está excluida.** La única ley que podría prohibirla sería una que obligara a que "
        "toda química con CCR baja fuera letal. El marco dice lo contrario: **L20, L25 y E7 "
        "establecen que la toxicidad depende del cuádruple (composición, temperatura, tiempo, "
        "protocolo) y NO de la molaridad sola.** Por eso M22 cargado a −22 °C y V3 cargado a "
        "10 °C son **puntos distintos** del espacio aunque su molaridad sea casi igual (9.3 vs "
        "8.42 M, un 10 % de diferencia). ⇒ X2 **no se cierra por imposibilidad**: sigue abierta, "
        "y eso es un resultado, no una laguna.")

    # --- figura: el plano con el hueco marcado
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    ax.axvspan(1e-3, ccr_req, color=AQUA, alpha=0.09, zorder=0)
    ax.axhspan(E_REQ - 0.5, 5.5, color=AQUA, alpha=0.09, zorder=0)
    ax.add_patch(plt.Rectangle((1e-3, E_REQ - 0.5), ccr_req - 1e-3, 6 - E_REQ,
                               facecolor=AQUA, alpha=0.16, edgecolor=AQUA, lw=1.4, zorder=1))
    ax.text(1.4e-3, 4.6, "REGIÓN QUE RESUELVE X2\nvacía: ninguna química medida cae aquí",
            fontsize=8, color="#0e7a55", va="top", zorder=4)
    # las que no tienen dato neural van en una fila propia, con las etiquetas escalonadas
    # para que no se pisen (varias comparten CCR casi idéntica)
    sin_dato = [(n, c) for n, c, M, en, *_ in CPAS if c is not None and en is None]
    dy = {n: (12, -15, 25)[i % 3] for i, (n, _) in enumerate(sorted(sin_dato, key=lambda t: t[1]))}
    fuera = []
    for nom, ccr, M, en, eo, f, nota in CPAS:
        if ccr is None: continue
        if ccr > 1e3:                     # fuera de escala: se declara en el pie, no se recorta
            fuera.append((nom, ccr)); continue
        e = en if en is not None else -0.42
        hueco = (en is None)
        ax.scatter([ccr], [e], s=74 if not hueco else 46,
                   color=(ORANGE if ccr > ccr_req else BLUE) if not hueco else SURF,
                   edgecolor=(ORANGE if ccr > ccr_req else BLUE), linewidth=1.8, zorder=3)
        ax.annotate(nom, (ccr, e), textcoords="offset points",
                    xytext=(7, 7) if not hueco else (6, dy[nom]),
                    fontsize=7.6 if not hueco else 7.0, color=INK2, zorder=4)
    ax.axvline(ccr_req, color="#c0392b", lw=1.3, zorder=2)
    ax.annotate(f"CCR máxima para un\ncerebro humano: {ccr_req:.3g} °C/min",
                (ccr_req, 3.5), textcoords="offset points", xytext=(9, 0),
                fontsize=7.4, color="#c0392b", zorder=4, va="center")
    if fuera:
        ax.text(0.99, -0.155, "fuera de escala: " + " · ".join(f"{n} (CCR {c:.2e})" for n, c in fuera),
                transform=ax.transAxes, ha="right", fontsize=6.8, color=MUTED)
    ax.set_xscale("log"); ax.set_xlim(5e-2, 1e3); ax.set_ylim(-0.95, 5.6)
    ax.set_yticks([-0.42, 0, 1, 2, 3])
    ax.set_yticklabels(["sin dato neural", "E0 estructura", "E1 células", "E2 tejido funcional",
                        "E3 órgano"], fontsize=7.6, color=INK2)
    ax.set_xlabel("CCR medida (°C/min) — a la izquierda de la línea, vitrifica un cerebro humano", color=INK2)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.grid(color=GRID, lw=0.6); ax.set_facecolor(SURF); fig.set_facecolor(SURF)
    fig.suptitle("El espacio de respuestas de X2: dos ejes medidos y un hueco con forma",
                 x=0.02, ha="left", fontsize=11, color=INK)
    fig.tight_layout(); fig.savefig(ROOT / "red" / "fig" / "X_espacio.png", dpi=150); plt.close(fig)

    doc = ("<!-- AUTO-GENERADO por red/espacio.py. NO EDITAR A MANO. -->\n"
           "# StasisPath: el espacio de respuestas de X2 — catalogado, no en blanco\n\n"
           "X2 pregunta si existe una química que **vitrifique a escala humana Y conserve la función**. "
           "Dejarlo como hueco en blanco desaprovecha lo que el marco ya sabe: cada química conocida ocupa un punto "
           "con **coordenadas medidas**, y el hueco tiene forma y tamaño.\n\n"
           "> **Lo que este documento NO hace.** El marco ya *predice* el resultado del brazo C de P19 "
           "(DERIVACION.md da daño 0.142; los dos caminos de I1 predicen PASA). **Esa predicción no se cuenta como dato.** "
           "Es justamente lo que el experimento pone a prueba: contarla cerraría el bucle sobre sí mismo y el marco "
           "dejaría de poder equivocarse. Aquí sólo entran coordenadas **medidas**.\n\n"
           f"![Espacio de X2](red/fig/X_espacio.png)\n\n"
           "## 1. Catálogo: toda química del marco, con sus dos coordenadas\n\n"
           f"**Requisito de vitrificación:** CCR ≤ **{ccr_req:.3g} °C/min** (invirtiendo C3 para un cerebro humano de "
           f"{D['humano']['cerebro']} g, LC = {lc_cerebro:.2f} cm). **Requisito de función:** al menos **E2**, tejido "
           "funcional, que es el nivel donde se mide la LTP.\n\n"
           + tabla(filas, ["química", "CCR °C/min", "M", "nivel en NEURAL", "nivel en otro tejido", "fuente", "veredicto"])
           + ("\n> ⚠ **DESFASE ENTRE ESTA TABLA Y `red/stasispath.yaml`** (comprobado automáticamente desde la tanda 52): "
              + "; ".join(f"**{n}** aquí {g(a)} frente a {g(b)} en `parametros`" for n, a, b in desfase)
              + ". La tabla **no se corrige sola** (mover un valor está prohibido, R2): hay que decidir cuál es el bueno.\n"
              if desfase else
              "\n> **Comprobado (tanda 52):** las CCR de M22, VS55 y VMP de esta tabla **coinciden con `parametros` en "
              "`red/stasispath.yaml`**. Estaban escritas a mano y duplicaban el dato; ahora el desfase se detectaría y se "
              "declararía aquí mismo. Importa porque `CCR_M22` tiene una **laguna abierta** (solución o tejido) y el día "
              "que se etiquete, este documento tiene que enterarse.\n")
           + "\n## 2. El hueco, medido\n\n"
           f"- **Químicas que vitrifican a escala de cerebro humano:** {len(con_ccr)} — "
           + ", ".join(f"{n} ({g(c)})" for n, c in con_ccr) + ".\n"
           f"- **Químicas con función demostrada en tejido neural (≥ E2):** {len(con_fun)} — "
           + ", ".join(f"{n} (E{e})" for n, e in con_fun) + ".\n"
           f"- **Intersección: vacía.** Ninguna química medida cumple las dos.\n\n"
           f"**Por cuánto falla la mejor candidata de cada lado:**\n\n"
           f"- Por el eje de la función, la mejor es **{mejor_fun[1]}**, con función neural E2 demostrada, pero su CCR "
           f"({g(mejor_fun[0])}) es **×{falta_ccr:.1f} la permitida**. Le falta bajar un factor {falta_ccr:.1f}.\n"
           f"- Por el eje de la vitrificación, la mejor es **M22** (CCR 0.1, holgura ×{ccr_req / 0.10:.1f} sobre el "
           "requisito), pero en tejido neural **sólo tiene ultraestructura demostrada (E0, F47), sin ninguna prueba "
           "de función**.\n\n"
           "> **El hueco no es difuso: es un salto entre dos químicas conocidas.** X2 se reduce a una pregunta "
           "concreta — **¿conserva M22 la función del tejido neural?** — y eso es exactamente el **brazo C de P19**, "
           "que ya está preregistrado y con umbrales congelados. Catalogar el espacio no cierra X2, pero **demuestra "
           "que un solo experimento lo decide**.\n\n"
           "## 3. ¿Está la región objetivo excluida por alguna ley del marco?\n\n"
           "Esta es la prueba que cerró V15 (patrón L43): si la incertidumbre no puede alojar ninguna respuesta, "
           "el veredicto está cerrado aunque nadie haya medido.\n\n"
           + razon_exclusion + "\n\n"
           "**Qué tendría que cumplir un candidato, en una línea:** CCR ≤ "
           f"{ccr_req:.3g} °C/min con LTP ≥ 130 % del basal en CA1 tras HFS (el umbral preregistrado de P19). "
           "M22 cumple el primero por un factor "
           f"{ccr_req / 0.10:.1f}; nadie ha medido el segundo.\n")
    (ROOT / "ESPACIO.md").write_text(doc)
    return {"ccr_req": ccr_req, "con_ccr": con_ccr, "con_fun": con_fun,
            "excluida": excluida, "falta_ccr": falta_ccr, "mejor_fun": mejor_fun}
