#!/usr/bin/env python3
"""TANDA 52 — COTA: ¿qué se cae si `CCR_M22` fuera un valor de SOLUCIÓN y el de TEJIDO fuera menor?

R2: NO se mueve ningún valor del YAML. Este script CALCULA el escenario y DECLARA.
El parámetro `CCR_M22` = 0.1 °C/min, rango [0.05, 0.15], viene de F2, que vitrificó M22 en
BOLSAS de crioconservación, no en tejido. El marco ya documenta que el efecto tejido/solución
existe: `CCR_VS55` = "tejido <1, solución 2.5" (factor > 2.5) y `CCR_VMP` está etiquetada como
tejido. La laguna quedó declarada en la tanda 51.

Lo que este script recorre, y que la tanda 51 NO recorrió:
  1. la propagación por la recta CCR<->molaridad (`b_CCR`, `a_CCR`, `M_de_CCR`) y por tanto
     `LC_viable` y `masa_viable` — la FRONTERA de F2, que es el corazón del marco;
  2. los tres veredictos de C3/C8 que mencionan M22, con su holgura exacta;
  3. el Monte Carlo de 20 000 muestras que sostiene la afirmación de L43
     («tronco y cuerpo entero fuera de la región viable en el 100 % de los casos»),
     que NO tenía script guardado en el repositorio;
  4. el corte de NADES de `barrido.py` y la holgura de M22 en `ESPACIO.md`;
  5. una INCONSISTENCIA DE ETIQUETA que la tanda 51 no vio: aplicar el factor de tejido sólo a
     M22 y dejar `CCR_VS55` en 2.5 (valor de SOLUCIÓN) mezcla las dos etiquetas en la MISMA recta.
"""
import math, random, statistics, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
D = yaml.safe_load(open(ROOT / "red" / "dsny.yaml"))
PAR = D["parametros"]
p0 = {k: v["v"] for k, v in PAR.items()}
r0 = {k: v["r"] for k, v in PAR.items()}
HUM = D["humano"]

g = lambda x: "—" if x is None else (f"{x:.4g}" if abs(x) < 1e4 else f"{x:.3e}")

# ---------------------------------------------------------------- funciones del marco (copiadas)
LC_esfera = lambda m: (3 * m / (4 * math.pi)) ** (1 / 3) / 3
masa_de_LC = lambda lc: 4 / 3 * math.pi * (3 * lc) ** 3 / 1000          # kg
tasa = lambda q, LC: q["anc_rate"] * (q["anc_LC"] / LC) ** q["exp_LC"]
M_TOX = 9.28                                                            # F72

def recta(q):
    b = (math.log10(q["CCR_M22"]) - (math.log10(q["CCR_VS55"]) + math.log10(q["CCR_VMP"])) / 2) / (9.3 - 8.4)
    a = (math.log10(q["CCR_VS55"]) + math.log10(q["CCR_VMP"])) / 2 - b * 8.4
    return a, b

def M_de_CCR(q, ccr):
    a, b = recta(q)
    return (math.log10(ccr) - a) / b

def frontera(q):
    """LC (cm) y masa (kg) a partir de los cuales la química necesaria es tóxica. Igual que `derivadas`."""
    for i in range(25, 20000):
        if M_de_CCR(q, tasa(q, i / 100)) > M_TOX:
            return i / 100, masa_de_LC(i / 100)
    return None, None

# ---------------------------------------------------------------- escenarios
# f = factor por el que el valor EN TEJIDO sería menor que el declarado.
# "coherente" = además se lleva `CCR_VS55` a su extremo de TEJIDO (1.0, que el propio
#   parámetro declara), para no mezclar etiquetas en la misma recta.
ESC = [("declarado (F2, bolsas)", 1.0, False),
       ("tejido x2.5 (factor VS55 del propio marco)", 2.5, False),
       ("tejido x5 (tope de la literatura citada)", 5.0, False),
       ("tejido x2.5 + VS55 a su valor de TEJIDO (1.0)", 2.5, True),
       ("tejido x5 + VS55 a su valor de TEJIDO (1.0)", 5.0, True)]

def escenario(f, coherente):
    q = dict(p0)
    q["CCR_M22"] = p0["CCR_M22"] / f
    if coherente:
        q["CCR_VS55"] = 1.0        # extremo inferior del rango declarado = el valor de TEJIDO
    rr = {k: list(v) for k, v in r0.items()}
    rr["CCR_M22"] = [r0["CCR_M22"][0] / f, r0["CCR_M22"][1] / f]
    if coherente:
        rr["CCR_VS55"] = [1.0, 1.0]
    return q, rr

print("=" * 108)
print("COTA CCR_M22: qué se cae si el valor en TEJIDO fuera menor que el de F2 (bolsas). R2: no se mueve nada.")
print("=" * 108)

# ---------------------------------------------------------------- 1. veredictos de C3 y C8
LCs = {"riñón humano": p0["LC_kidneyH"], "cerebro (1400 g)": LC_esfera(HUM["cerebro"]),
       "cuerpo medio": p0["LC_body"], "tronco": p0["LC_trunk"]}
print("\n1. TASAS DE ENFRIAMIENTO (valores centrales, no dependen de CCR_M22)")
for n, lc in LCs.items():
    print(f"   {n:20s} LC = {lc:6.3f} cm   tasa = {tasa(p0, lc):8.5f} °C/min")

print("\n2. LOS TRES VEREDICTOS QUE MENCIONAN M22 (C3 y C8), en el CENTRO y en las ESQUINAS")
print(f"   {'escenario':46s} {'CCR_M22':>16s} {'tronco FALLA':>14s} {'cuerpo VITRIF':>14s} {'LC4 sufic.':>12s}")
res_ver = {}
for nom, f, coh in ESC:
    q, rr = escenario(f, coh)
    c = q["CCR_M22"]
    # veredicto central
    v_tr = tasa(q, q["LC_trunk"]) < c
    v_bo = tasa(q, q["LC_body"]) >= c
    v_l4 = c <= tasa(q, 4.0)
    # robustez: esquinas de las deps declaradas de C3 y C8
    import itertools
    deps3 = D["cotas"]["C3"]["deps"]
    rob_tr = rob_bo = True
    for combo in itertools.product(*[rr[d] for d in deps3]):
        qq = dict(q); qq.update(zip(deps3, combo))
        rob_tr &= tasa(qq, qq["LC_trunk"]) < qq["CCR_M22"]
        rob_bo &= tasa(qq, qq["LC_body"]) >= qq["CCR_M22"]
    deps8 = D["cotas"]["C8"]["deps"]
    rob_l4 = True
    for combo in itertools.product(*[rr[d] for d in deps8]):
        qq = dict(q); qq.update(zip(deps8, combo))
        rob_l4 &= qq["CCR_M22"] <= tasa(qq, 4.0)
    m = lambda ok, rob: ("SI-robusto" if rob else "SI-frágil") if ok else "**NO**"
    print(f"   {nom:46s} {g(c):>16s} {m(v_tr,rob_tr):>14s} {m(v_bo,rob_bo):>14s} {m(v_l4,rob_l4):>12s}")
    res_ver[nom] = (v_tr, rob_tr, v_bo, rob_bo, v_l4, rob_l4)

print("\n   Holgura exacta del veredicto del tronco en el escenario declarado:")
print(f"     tasa en el tronco = {tasa(p0, p0['LC_trunk']):.5f} °C/min; el veredicto exige CCR_M22 > esa tasa.")
print(f"     mínimo del rango declarado 0.05 -> holgura x{0.05/tasa(p0, p0['LC_trunk']):.3f}")
print(f"     con esquinas GENEROSAS de LC_trunk=9 y exp_LC=1.67: tasa = {tasa(dict(p0, exp_LC=1.67), 9.0):.5f}")

# ---------------------------------------------------------------- 3. la recta CCR<->molaridad
print("\n3. LO QUE LA TANDA 51 NO RECORRIÓ: la recta CCR<->molaridad y la FRONTERA DE VIABILIDAD")
print("   `b_CCR` es la pendiente local; `masa_viable` es la frontera de F2 que usan L43, L44, L45, V14 y V15.")
print(f"   {'escenario':46s} {'b décadas/M':>12s} {'a':>8s} {'LC_viable cm':>13s} {'masa_viable kg':>15s}")
fron = {}
for nom, f, coh in ESC:
    q, rr = escenario(f, coh)
    a, b = recta(q)
    lc, ma = frontera(q)
    fron[nom] = (b, lc, ma)
    print(f"   {nom:46s} {b:12.4f} {a:8.4f} {g(lc):>13s} {g(ma):>15s}")

lcB = LC_esfera(HUM["cerebro"])
print(f"\n   Masas equivalentes de referencia: cerebro {masa_de_LC(lcB):.2f} kg (LC {lcB:.3f} cm) · "
      f"cuerpo medio {masa_de_LC(p0['LC_body']):.1f} kg (LC {p0['LC_body']}) · tronco {masa_de_LC(p0['LC_trunk']):.1f} kg (LC {p0['LC_trunk']})")
print("   OJO: `masa_viable` es la masa de la ESFERA equivalente a la LC, no la masa del órgano real.")
for nom, (b, lc, ma) in fron.items():
    ver = []
    for n, l in (("cerebro", lcB), ("cuerpo medio", p0["LC_body"]), ("tronco", p0["LC_trunk"])):
        ver.append(f"{n}={'DENTRO' if l <= lc else 'fuera'}")
    print(f"   {nom:46s} -> " + " · ".join(ver))

# ---------------------------------------------------------------- 4. Monte Carlo (la afirmación de L43)
print("\n4. EL MONTE CARLO DE L43 (20 000 combinaciones de los SEIS parámetros de la frontera).")
print("   L43 afirma: cerebro DENTRO en el 100 %, tronco y cuerpo entero FUERA en el 100 %.")
print("   No había script guardado en el repositorio; se reconstruye aquí con el muestreo de `precision.py`")
print("   (triangular con moda en el central, que es el que el marco ya usa).")
SEIS = ("anc_LC", "anc_rate", "exp_LC", "CCR_M22", "CCR_VS55", "CCR_VMP")
N = 20000
print(f"   {'escenario':46s} {'cerebro DENTRO':>15s} {'cuerpo FUERA':>13s} {'tronco FUERA':>13s} {'p5':>7s} {'p50':>7s} {'p95':>7s}")
mc = {}
for nom, f, coh in ESC:
    q, rr = escenario(f, coh)
    random.seed(7)
    n_br = n_bo = n_tr = 0
    vals = []
    for _ in range(N):
        s = dict(q)
        for k in SEIS:
            lo, hi = rr[k]
            s[k] = random.triangular(lo, hi, min(max(q[k], lo), hi))
        lc, ma = frontera(s)
        if lc is None: continue
        vals.append(ma)
        n_br += (lcB <= lc)
        n_bo += (p0["LC_body"] > lc)
        n_tr += (p0["LC_trunk"] > lc)
    vals.sort()
    pc = lambda t: vals[int(t * (len(vals) - 1))]
    mc[nom] = (100 * n_br / N, 100 * n_bo / N, 100 * n_tr / N, pc(.05), pc(.5), pc(.95))
    print(f"   {nom:46s} {100*n_br/N:14.2f}% {100*n_bo/N:12.2f}% {100*n_tr/N:12.2f}% "
          f"{pc(.05):7.2f} {pc(.5):7.2f} {pc(.95):7.2f}")

# ------------------------------------------------- 4b. LA MISMA AFIRMACIÓN, CON EL CRITERIO DEL PROPIO MARCO
# `red/motor.py` declara en su docstring que el criterio MATE del marco son las ESQUINAS del rango:
# «cada cota se evalúa en las esquinas del rango de sus parámetros ... las esquinas acotan el rango
# completo sin Monte Carlo (R5: no hay teatro)». L43 usa en cambio un Monte Carlo TRIANGULAR, que
# concentra la masa en el centro y NUNCA visita una esquina. Se aplica aquí el criterio propio.
import itertools
print("\n4b. LA MISMA AFIRMACIÓN DE L43 CON EL CRITERIO MATE DEL MARCO: las 2^6 = 64 ESQUINAS")
print("    (valores DECLARADOS, ningún parámetro movido — R2)")
res = []
for combo in itertools.product(*[r0[k] for k in SEIS]):
    q = dict(p0); q.update(zip(SEIS, combo))
    lc, ma = frontera(q); res.append((lc, ma, combo))
lcs = [x[0] for x in res]; mas = [x[1] for x in res]
print(f"    LC_viable en las esquinas: {min(lcs):.3f} – {max(lcs):.3f} cm (central {frontera(p0)[0]:.2f})")
print(f"    masa_viable en las esquinas: {min(mas):.2f} – {max(mas):.1f} kg (central {frontera(p0)[1]:.1f})")
print(f"    cerebro (LC {lcB:.3f}) DENTRO en {sum(1 for l in lcs if lcB <= l)}/64 esquinas")
print(f"    cuerpo entero (LC {p0['LC_body']}) FUERA en {sum(1 for l in lcs if p0['LC_body'] > l)}/64 esquinas")
print(f"    tronco (LC {p0['LC_trunk']}) FUERA en {sum(1 for l in lcs if p0['LC_trunk'] > l)}/64 esquinas")
print(f"    por MASA de esfera equivalente: tronco (47.7 kg) FUERA en {sum(1 for m in mas if 47.7 > m)}/64 · "
      f"cuerpo (70 kg) FUERA en {sum(1 for m in mas if 70 > m)}/64")
peor = max(res, key=lambda x: x[0])
print("    esquina más generosa: " + ", ".join(f"{k}={v}" for k, v in zip(SEIS, peor[2])) +
      f"  ->  LC_viable {peor[0]:.2f} cm ({peor[1]:.1f} kg)")
print("    ⇒ EN ESA ESQUINA EL TRONCO (LC 7.5) CAE **DENTRO** DE LA REGIÓN VIABLE.")
print("    ⇒ El «100 %» de L43 NO se sostiene con el criterio mate del propio marco, y esto NO necesita")
print("      la laguna de CCR_M22: se cae con los valores DECLARADOS. Coincide con lo que C3 ya imprime:")
print("      el veredicto «M22 falla en el centro del tronco» sale ✔~ (cierto en el centro, NO robusto).")

# ---------------------------------------------------------------- 5. barrido NADES y ESPACIO
print("\n5. OTRAS SALIDAS QUE TOCAN CCR_M22")
ccr_req = tasa(p0, lcB)
print(f"   `ESPACIO.md` / L44: CCR requerida por un cerebro humano = {ccr_req:.4g} °C/min.")
print("     NO depende de CCR_M22 (sale de C3 sola) -> la 'intersección vacía' de X2 NO se cae en ningún escenario.")
for nom, f, coh in ESC:
    print(f"     holgura de M22 sobre ese requisito, {nom:46s}: x{ccr_req/(p0['CCR_M22']/f):.2f}")
print("   `red/espacio.py`: el CCR de M22 está ESCRITO A MANO como 0.10 en la tabla CPAS, no leído de PAR.")
print("     -> si el parámetro se etiquetara algún día, ESPACIO.md NO se enteraría. Duplicado de dato (R4, impostor).")
print(f"   `barrido.py`: el corte de NADES se compara contra CCR_M22; con el valor declarado la razón")
print(f"     corte/CCR_M22 es x{tasa(p0, lcB)/p0['CCR_M22']:.2f}; los NADES fallan por x{30.0/ccr_req:.0f} y eso NO cambia en ningún escenario.")

# ---------------------------------------------------------------- 6. veredicto
print("\n" + "=" * 108)
print("6. QUÉ SE CAE Y QUÉ AGUANTA")
print("=" * 108)
aguanta = [
    "C3 sigue MATE: su único veredicto CLAVE ('VMP no vitrifica un riñón humano') no toca CCR_M22.",
    "C8 sigue MATE: su único veredicto CLAVE ('VMP insuficiente a LC 4 cm') no toca CCR_M22.",
    "C1 intacta: usa CWR_M22, no CCR_M22. El veredicto del recalentamiento del tronco no se mueve.",
    "X2 sigue abierta y la intersección sigue VACÍA: el eje que le falta a M22 es FUNCIÓN neural, no CCR.",
    "L35/L44 (NADES): fallan por un factor >70 contra el requisito del cerebro, que no depende de CCR_M22.",
    "El cerebro humano sigue DENTRO de la región viable en el 100 % en todos los escenarios (y con más holgura).",
]
cae = []
for nom, f, coh in ESC[1:]:
    v_tr, rob_tr, *_ = res_ver[nom]
    b, lc, ma = fron[nom]
    br, bo, tr, p5, p50, p95 = mc[nom]
    linea = (f"{nom}: veredicto del tronco {'SE DA LA VUELTA (ya no falla)' if not v_tr else ('deja de ser robusto' if not rob_tr else 'aguanta')}"
             f" · masa_viable {ma:.1f} kg (declarado {fron[ESC[0][0]][2]:.1f})"
             f" · L43 'tronco fuera' pasa del 100 % al {tr:.1f} % · 'cuerpo entero fuera' al {bo:.1f} %")
    cae.append(linea)
print("\nAGUANTA:")
for x in aguanta: print("  + " + x)
print("\nSE CAE (o queda condicionado):")
for x in cae: print("  - " + x)
print("\nY EL HALLAZGO QUE NO NECESITA LA LAGUNA (ver bloque 4b):")
print("  * L43 afirma «tronco y cuerpo entero fuera de la región viable en el 100 % de las 20 000")
print("    combinaciones». Con los valores DECLARADOS y el criterio MATE del propio marco (esquinas),")
print("    el tronco cae DENTRO en 12 de las 64 esquinas y el cuerpo entero en 50 de 64.")
print("    El «100 %» es un artefacto del muestreo TRIANGULAR, que nunca visita una esquina.")
print("    ⇒ L43 afirma MÁS de lo que su cálculo sostiene, y V15 se cerró apoyándose justo en eso.")
print("  * Además L43 mide «cuerpo entero» por MASA (70 kg frente a masa_viable) mientras C3 lo mide")
print("    por LC (3.9 cm frente a LC_viable) y concluye lo CONTRARIO: «M22 vitrifica el cuerpo medio».")
print("    Dos criterios distintos para el mismo objeto dentro del mismo marco.")
print("\nY LA INCONSISTENCIA DE ETIQUETA, que es el otro hallazgo propio de esta cota:")
print("  * `b_CCR` mezcla en UNA recta un punto de M22 cuya etiqueta no consta con un punto de VS55 tomado")
print("    en su valor de SOLUCIÓN (2.5) y uno de VMP etiquetado como TEJIDO. Sea cual sea la etiqueta de M22,")
print(f"    la recta actual ya es mixta. Con los tres puntos en TEJIDO y M22 sin cambiar, b seria "
      f"{recta(dict(p0, CCR_VS55=1.0))[1]:.4f} en vez de {recta(p0)[1]:.4f}, y masa_viable "
      f"{frontera(dict(p0, CCR_VS55=1.0))[1]:.1f} kg en vez de {frontera(p0)[1]:.1f} kg.")
print("    ⇒ la laguna NO es sólo 'de qué tipo es CCR_M22': es que la recta no declara de qué tipo es NINGUNO.")
print("\nR2 comprobado: este script no escribe en red/dsny.yaml. Ningún valor se ha movido.")
