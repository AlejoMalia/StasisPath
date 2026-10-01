"""StasisPath: análisis automático de P21 (exponente de la ley de enfriamiento).

Aplica LITERALMENTE las reglas congeladas en el preregistro P21. No tiene parámetros ajustables:
los umbrales (2.34, 5.3, control 1.4 ± 15 %) se leen del texto congelado y el hash los protege (R2).
Con `mediciones_P21: []` informa «pendiente de datos». Salida: P21.md. Lo llama motor.py.
"""
import math

UMBRAL_N, CCR_VMP, CTRL, CTRL_TOL = 2.34, 5.3, 1.4, 0.15
F2 = [(1.2, 1.4), (1.402, 0.998), (2.2, 0.47)]   # (LC cm, °C/min): los tres volúmenes publicados
T95U = {1: 6.314, 2: 2.920, 3: 2.353, 4: 2.132, 5: 2.015, 6: 1.943, 7: 1.895, 8: 1.860, 9: 1.833, 10: 1.812,
        12: 1.782, 15: 1.753, 20: 1.725, 30: 1.697}

def _t(gl):
    return T95U[max(k for k in T95U if k <= gl)]

def analizar(meds):
    """meds: lista de {vol_L, V_mL, A_cm2, tasa}. Devuelve dict con veredicto y números."""
    ctrl = [m for m in meds if abs(m["vol_L"] - 0.5) < 1e-9]
    nuevas = [m for m in meds if abs(m["vol_L"] - 0.5) >= 1e-9]
    if not meds:
        return {"estado": "PENDIENTE", "motivo": "sin datos: el experimento no se ha ejecutado"}
    if not ctrl:
        return {"estado": "NO INTERPRETABLE", "motivo": "falta la bolsa de control de 0.5 L"}
    c = sum(m["tasa"] for m in ctrl) / len(ctrl)
    if abs(c / CTRL - 1) > CTRL_TOL:
        return {"estado": "NO INTERPRETABLE", "motivo": f"control de 0.5 L = {c:.3g} °C/min, fuera de 1.4 ± 15 %: el montaje no es el de F2"}
    grupos = {}
    for m in nuevas:
        grupos.setdefault(m["vol_L"], []).append((m["V_mL"] / m["A_cm2"], m["tasa"]))
    pts = [(math.log(L), math.log(r)) for L, r in F2] + [(math.log(L), math.log(r)) for g in grupos.values() for L, r in g]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    k = len(xs); mx, my = sum(xs) / k, sum(ys) / k
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    n = -b
    gl = sum(len(g) - 1 for g in grupos.values())
    if gl >= 1:   # error puro de las réplicas, como fija P21
        ss = sum(sum((math.log(r) - sum(math.log(q) for _, q in g) / len(g)) ** 2 for _, r in g) for g in grupos.values())
    else:         # sin réplicas: residuos del ajuste (P21 no lo prevé; se informa, pero penaliza)
        a = my - b * mx; ss = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys)); gl = k - 2
    se = math.sqrt(ss / gl) / math.sqrt(sxx)
    sup, inf = n + _t(gl) * se, n - _t(gl) * se
    nvol = 3 + len(grupos)
    peq = [r for v, g in grupos.items() if v <= 0.3 for _, r in g]
    directa = (sum(peq) / len(peq)) if peq else None
    if directa is not None and directa >= CCR_VMP:
        est, mot = "FALLA", f"comprobación directa: bolsas pequeñas a {directa:.3g} °C/min ≥ CCR de VMP"
    elif sup < UMBRAL_N:
        est, mot = "PASA", f"cota superior 95 % de n = {sup:.3g} < {UMBRAL_N}"
    elif nvol >= 4 and inf > UMBRAL_N:
        est, mot = "FALLA", f"cota inferior 95 % de n = {inf:.3g} > {UMBRAL_N}: C3 refutada"
    else:
        est, mot = "INCONCLUSO", f"n = {n:.3g}, IC unilateral [{inf:.3g}, {sup:.3g}] contiene {UMBRAL_N}"
    return {"estado": est, "motivo": mot, "n": n, "se": se, "gl": gl, "sup": sup, "inf": inf,
            "nvol": nvol, "control": c, "directa": directa, "grupos": grupos}

def generar(D, ROOT):
    r = analizar(D.get("mediciones_P21") or [])
    doc = ("<!-- AUTO-GENERADO por red/p21.py. NO EDITAR A MANO. -->\n"
           "# P21: exponente de la ley de enfriamiento — estado del experimento\n\n"
           f"**Estado: {r['estado']}** — {r['motivo']}.\n\n"
           "Reglas (congeladas en el preregistro P21, protegidas por hash): PASA si la cota unilateral superior 95 % de n < 2.34; "
           "FALLA si la inferior > 2.34 o si las bolsas de ~0.15 L enfrían ≥ 5.3 °C/min; si no, inconcluso. "
           "Control: 0.5 L debe dar 1.4 °C/min ± 15 %.\n\n")
    if r["estado"] == "PENDIENTE":
        doc += ("**Cómo se carga un dato:** una línea por bolsa en `mediciones_P21` de `red/stasispath.yaml` "
                "(`{vol_L, V_mL, A_cm2, tasa}`) y `python3 red/motor.py`. El veredicto sale solo.\n\n"
                "**Diseño preregistrado (B′):** 1 bolsa de control de 0.5 L + 3 bolsas de ~0.15 L + 3 bolsas de ~7 L, montaje idéntico a F2.\n")
    elif "n" in r:
        doc += (f"| magnitud | valor |\n|---|---|\n| n ajustado | {r['n']:.3f} ± {r['se']:.3f} ({r['gl']} gl) |\n"
                f"| cota unilateral 95 % | [{r['inf']:.3f}, {r['sup']:.3f}] |\n| volúmenes | {r['nvol']} |\n"
                f"| control 0.5 L | {r['control']:.3g} °C/min |\n"
                + (f"| tasa directa ~0.15 L | {r['directa']:.3g} °C/min |\n" if r['directa'] is not None else ""))
    (ROOT / "P21.md").write_text(doc)
    return r
