"""StasisPath: proyección condicional al cierre. Las dos campanas.

Idea (del usuario): proyectar dos distribuciones —lo que TENEMOS y lo que NECESITAMOS— y ver
cómo quedaría el marco al cerrarse.

**Límite declarado y no negociable:** esto NO sube el porcentaje real. El marco sigue donde
está hasta que alguien mida. Lo que se calcula aquí es un **escenario condicional**: «si cada
predicción se confirma, el marco quedaría así». Un escenario no es un logro, y se etiqueta como
tal en cada línea. Dejar que el código se redondee solo sería fabricar avance.

Lo que sí aporta, y es mucho: hace el marco **enteramente falsable**. Cada predicción lleva su
valor, su dispersión y **qué resultado la refutaría**. Cuando llegue el dato, el módulo compara
y avisa si cae fuera — ahí está la autocorrección real.
"""
import math

def g(x):
    if x is None or x != x: return "—"
    return f"{x:.3g}" if abs(x) < 1e4 else f"{x:,.0f}"

def tabla(f, cab):
    return "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in r) + " |" for r in f) + "\n"

# Lo que NECESITAMOS: predicción del marco para cada nodo abierto, con dispersión y refutación.
# sigma_rel = dispersión relativa (1σ) que el marco le asigna a su propia predicción.
PREDICHO = [
    # id, qué es, valor predicho, unidad, sigma_rel, de dónde sale, qué lo REFUTA
    ("I1", "daño del brazo frío de P19", 0.142, "", 0.55, "Arrhenius × punto de German (DERIVACION)",
     "un daño > 0.25 refuta la derivación; > 0.22 además haría fallar a P19"),
    ("I2", "CCR de los NADES", 0.3, "°C/min", 1.20, "cota superior por inmersión + orden de los CPA conocidos",
     "una CCR > 0.426 deja el cerebro humano fuera y obliga a ejecutar P19"),
    ("I4", "τ_eq humano con reperfusión óptima", 17.0, "min", 0.45, "invariancia entre especies (T1 del escalado)",
     "un valor < 12.5 min refutaría la invariancia; > 60 min contradiría a la gata de Hossmann"),
    ("I5", "J de nucleación a −6 °C", 0.57, "/L·h", 0.50, "ajuste con los dos puntos del hígado de rata",
     "una J > 0.85 impide llegar a 4 h con 95 % en hígado humano"),
    ("X2", "¿resuelve la química el cuello?", 1.0, "veredicto", 0.0, "B1: ambos caminos predicen PASA",
     "que P19 dé LTP ≤ 110 % con el control positivo válido"),
]

def generar(D, PAR, DERIV, ROOT, total_actual, rumbo=None):
    # ---- Campana 1: lo que TENEMOS. Dispersión relativa de cada parámetro verificado.
    tengo = []
    for k, v in PAR.items():
        lo, hi = v["r"]; c = v["v"]
        if c and lo > 0 and hi > lo:
            tengo.append((k, (hi - lo) / (2 * c)))     # semiancho relativo ≈ 1σ
    tengo.sort(key=lambda t: t[1])
    rel_t = [x[1] for x in tengo]
    med_t = rel_t[len(rel_t) // 2]

    # ---- Campana 2: lo que NECESITAMOS.
    rel_n = sorted(p[4] for p in PREDICHO if p[4] > 0)
    med_n = rel_n[len(rel_n) // 2]

    filas_n = [[i, q, f"{g(v)} {u}", f"±{g(s*100)} %", src, ref] for i, q, v, u, s, src, ref in PREDICHO]

    # ---- Escenario condicional: el marco SI todas las predicciones se confirman
    #      No se toca el motor: se calcula aparte y se etiqueta como escenario.
    # Los puntos NO se escriben a mano: se simulan con red/rumbo.py (misma regla de propagación del motor).
    # Antes aquí había constantes (X2 = +5.95) que resultaron optimistas en ~3 puntos (tanda 44).
    CADENA_I2 = ["X2", "V26", "F80"]                 # NADES: CCR medida cierra X2 y su vía
    CADENA_I5 = ["L41", "V27", "F85", "F22"]         # nucleación ajustada: sobreenfriamiento
    sim = rumbo["simular"]
    pts_x2 = sim(CADENA_I2) - total_actual
    pts_resto = sim(CADENA_I2 + CADENA_I5) - total_actual - pts_x2
    proy = total_actual + pts_x2 + pts_resto
    irreducible = 100 - proy
    techo_todo = rumbo["techo"]

    doc = ("<!-- AUTO-GENERADO por red/proyeccion.py. NO EDITAR A MANO. -->\n"
           "# StasisPath: proyección condicional al cierre\n\n"
           "> **Esto NO es progreso.** El marco está en "
           f"**{total_actual:.1f} %** y sigue ahí hasta que alguien mida. Lo que hay debajo es un "
           "**escenario condicional**: cómo quedaría *si* cada predicción se confirma. Un escenario no es un logro. "
           "Dejar que el código se redondee solo al 100 % sería fabricar avance, y por eso no se hace.\n\n"
           "Lo que sí aporta: **hace el marco enteramente falsable**. Cada predicción lleva valor, dispersión y "
           "**qué resultado la refutaría**.\n\n"
           "## Las dos campanas\n\n"
           + tabla([["**lo que tenemos**", f"{len(tengo)} parámetros verificados", f"±{g(med_t*100)} %",
                     f"del ±{g(min(rel_t)*100)} % al ±{g(max(rel_t)*100)} %"],
                    ["**lo que necesitamos**", f"{len(rel_n)} predicciones abiertas", f"±{g(med_n*100)} %",
                     f"del ±{g(min(rel_n)*100)} % al ±{g(max(rel_n)*100)} %"]],
                   ["campana", "n", "dispersión mediana", "rango"]) +
           f"\n**Lo que dice la comparación:** lo que ya tenemos está medido con una dispersión mediana del "
           f"**±{g(med_t*100)} %**; lo que falta lo predecimos con **±{g(med_n*100)} %**, es decir "
           f"**{g(med_n/med_t)} veces más ancho**. ⇒ **No hace falta medir mejor de lo que ya medimos**: basta con "
           "medir lo que falta **con la misma calidad** que lo que ya está, y el marco se cierra.\n\n"
           "## Lo que el marco predice, y qué lo refuta\n\n"
           + tabla(filas_n, ["id", "magnitud", "predicción", "±1σ", "de dónde sale", "qué la REFUTA"]) +
           "\n## Escenario de cierre (condicional, no logrado)\n\n"
           + tabla([["Estado real hoy", f"{total_actual:.1f} %", "medido"],
                    ["Si se confirma la CCR de los NADES (cierra X2, V26, F80)", f"+{pts_x2:.1f}", "**escenario simulado**"],
                    ["Si además se confirma I5 (L41, V27, F85, F22)", f"+{pts_resto:.1f}", "**escenario simulado**"],
                    ["**Techo del escenario de predicciones**", f"**{proy:.1f} %**", "**escenario simulado**"],
                    ["No cubierto por ninguna predicción", f"{irreducible:.1f} %", "fuentes secundarias y vías sin dato (ver RUMBO.md)"],
                    ["Techo si se cerrara TODO lo abierto", f"{techo_todo:.1f} %", "RUMBO.md"]],
                   ["concepto", "valor", "naturaleza"]) +
           f"\n> **Las predicciones solas no cierran el marco.** Confirmarlas todas da {proy:.1f} %; los "
           f"**{irreducible:.1f} puntos** restantes no dependen de ninguna predicción sino de **leer fuentes primarias y "
           "conseguir datos de vías** que nadie ha publicado todavía. RUMBO.md los ordena por puntos. "
           "**Los puntos se simulan con la regla del motor; ya no se escriben a mano.**\n\n"
           "## La autocorrección, que sí es real\n\n"
           "Cuando llegue un dato para cualquiera de estas predicciones, el procedimiento es automático:\n\n"
           "1. Se añade como parámetro o fuente en `red/stasispath.yaml` (una línea).\n"
           "2. El motor recalcula cotas, derivadas, márgenes, triangulación y barrido.\n"
           "3. **Si el valor cae fuera del rango predicho, la triangulación lo marca como contradicción** y señala "
           "qué ley del marco falla — que es exactamente lo que pasó con I1 y con el régimen isocórico de I5.\n\n"
           "Eso es autocorrección: **el marco no se ajusta para encajar el dato, señala qué tendría que cambiar.**\n")
    (ROOT / "PROYECCION.md").write_text(doc)
    return dict(med_t=med_t, med_n=med_n, proy=proy, irreducible=irreducible)
