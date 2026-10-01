"""TRIADA/MATEMATICA — exp_LC y anc_LC: ¿qué medición haría falta y con qué precisión?
Escrito ANTES de leer nada nuevo (R3/TRIADA). Se reutiliza sólo lo que la red ya tiene:

  Inventario (F2, Etheridge/Bischof):
    0.5 L  LC 1.2 cm  -> 1.4  °C/min        (20_cotas/cota_enfriamiento_cuerpo.py)
    1 L    LC ~1.40   -> ~1.0 °C/min        (reconstruido de las pendientes por pares de BITACORA:194)
    3 L    LC 2.2     -> 0.47 [0.45, 0.50]  (anc_rate)
  LC por V/A desde el espesor: x1.06, x1.13, x1.06 sobre la LC citada (BITACORA:194).

Preguntas, en orden:
  A. ¿El punto de 1 L reconstruido reproduce las tres pendientes registradas? (control de implementación)
  B. Ajuste log-log de los 3 puntos con las DOS definiciones de LC: exponente y su error.
  C. Predicción directa a LC 4 cm (C6/C8/C11) con el ajuste, frente a lo que usa hoy el motor.
  D. ¿Cuántos volúmenes y con qué ruido hacen falta para que exp_LC quede en ±0.1 al 95 %?
"""
import math

pts_cit = [(1.2, 1.4), (None, None), (2.2, 0.47)]
# A. reconstruir 1 L desde las pendientes registradas: s12 = 2.18, s23 = 1.67, s13 = 1.80
s12, s23 = 2.18, 1.67
L1, r1, L3, r3 = 1.2, 1.4, 2.2, 0.47
s13 = math.log(r1 / r3) / math.log(L3 / L1)
# ln L2 tal que  s12*ln(L2/L1) + s23*ln(L3/L2) = s13*ln(L3/L1)
lnL2 = (s13 * math.log(L3 / L1) - s23 * math.log(L3) + s12 * math.log(L1)) / (s12 - s23)
L2 = math.exp(lnL2); r2 = r1 * (L1 / L2) ** s12
print("A. control de implementación")
print(f"   s13 calculada = {s13:.3f} (registrada 1.80)  ->  1 L: LC = {L2:.3f} cm, tasa = {r2:.3f} °C/min")
print(f"   comprobación s23 = {math.log(r2 / r3) / math.log(L3 / L2):.3f} (registrada 1.67)")

def ajuste(pts):
    x = [math.log(L) for L, _ in pts]; y = [math.log(r) for _, r in pts]
    n = len(x); mx, my = sum(x) / n, sum(y) / n
    sxx = sum((a - mx) ** 2 for a in x); sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    b = sxy / sxx; a = my - b * mx
    res = [yy - (a + b * xx) for xx, yy in zip(x, y)]
    s2 = sum(e * e for e in res) / (n - 2)
    return -b, math.sqrt(s2 / sxx), a, mx, sxx, math.sqrt(s2), res

T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 8: 2.306, 10: 2.228}
print("\nB. ajuste de los 3 volúmenes (tasa ∝ LC^-n)")
defs = {"LC citada": [(L1, r1), (L2, r2), (L3, r3)],
        "LC = V/A reconstruida": [(L1 * 1.06, r1), (L2 * 1.13, r2), (L3 * 1.06, r3)]}
fits = {}
for nom, pts in defs.items():
    n, se, a, mx, sxx, s, res = ajuste(pts)
    fits[nom] = (n, se, a, mx, sxx, s, pts)
    print(f"   {nom:22s} n = {n:.3f} ± {se:.3f} (1σ) · IC95 (1 gl) = [{n - T975[1] * se:.2f}, {n + T975[1] * se:.2f}]"
          f" · residuo típico {100 * (math.exp(s) - 1):.1f} %")
print("   rango del motor: exp_LC = 2.0 [1.67, 2.18]")

print("\nC. predicción a LC 4 cm (ventana lenta de C6: 0.1–1 °C/min)")
motor = lambda n: 0.47 * (2.2 / 4.0) ** n
print(f"   motor, central n=2: {motor(2):.3f} · esquinas n=1.67/2.18: {motor(2.18):.3f}–{motor(1.67):.3f} °C/min")
for nom, (n, se, a, mx, sxx, s, pts) in fits.items():
    x0 = math.log(4.0); yhat = a - n * x0
    sp = s * math.sqrt(1 + 1 / 3 + (x0 - mx) ** 2 / sxx)
    lo, hi = math.exp(yhat - T975[1] * sp), math.exp(yhat + T975[1] * sp)
    print(f"   {nom:22s} {math.exp(yhat):.3f} °C/min · IC95 predicción (1 gl) {lo:.3g}–{hi:.3g}")

print("\nD. diseño de la medición que cerraría exp_LC a ±0.1 (IC 95 %)")
# volúmenes repartidos uniformemente en ln LC entre 0.5 L (1.2 cm) y V_max; ruido de tasa σ_r
for vmax_lc, etiqueta in ((2.2, "hasta 3 L (lo que F2 ya hace)"), (3.5, "hasta ~12 L"), (4.5, "hasta ~25 L")):
    for sig in (0.05, 0.10, 0.17):
        for k in (3, 4, 5, 6, 8, 10):
            xs = [math.log(1.2) + i * (math.log(vmax_lc) - math.log(1.2)) / (k - 1) for i in range(k)]
            m = sum(xs) / k; sxx = sum((x - m) ** 2 for x in xs)
            half = T975.get(k - 2, 2.2) * sig / math.sqrt(sxx)
            if half <= 0.10:
                print(f"   {etiqueta:30s} ruido ±{100 * sig:.0f} % -> {k} volúmenes (semiancho {half:.3f})")
                break
        else:
            print(f"   {etiqueta:30s} ruido ±{100 * sig:.0f} % -> ni con 10 volúmenes")

print("\nE. MATE: ¿se sostienen los veredictos clave con el ajuste honesto (1 gl)?")
# Los veredictos clave sólo se vuelcan por UN lado; la pregunta correcta es unilateral.
T95u, T99u = 6.314, 31.821   # t unilateral con 1 gl
casos = [  # (veredicto, LC objetivo [cm], lado que debe cumplirse, umbral [°C/min] en su esquina peor)
    ("C6: LC 4 cm dentro de la ventana lenta (tasa ≥ 0.1)", 4.0, "≥", 0.1),
    ("C3: VMP no vitrifica riñón humano (tasa < CCR_VMP=5.3)", 0.85, "<", 5.3),
    ("C8: VMP insuficiente a LC 4 cm (tasa < 5.3)", 4.0, "<", 5.3),
    ("C11: a LC 4 cm más lento que 1 °C/min", 4.0, "<", 1.0)]
for ver, x0L, lado, umbral in casos:
    peor = None
    for nom, (n, se, a, mx, sxx, s, pts) in fits.items():
        x0 = math.log(x0L); yhat = a - n * x0
        for tipo, extra in (("línea", 0.0), ("predicción", 1.0)):
            sp = s * math.sqrt(extra + 1 / 3 + (x0 - mx) ** 2 / sxx)
            for t, conf in ((T95u, 95), (T99u, 99)):
                cota = math.exp(yhat - t * sp) if lado == "≥" else math.exp(yhat + t * sp)
                ok = cota >= umbral if lado == "≥" else cota < umbral
                if tipo == "predicción":
                    peor = (peor or []) + [(nom, conf, cota, ok)]
    print(f"   {ver}")
    for nom, conf, cota, ok in peor:
        print(f"      {nom:22s} {conf} % unilateral (predicción): tasa {'≥' if lado == '≥' else '<'} {cota:.3g} -> {'SE SOSTIENE' if ok else 'FUGA'}")

print("\nF. ¿qué exponente vuelca cada veredicto? (anc 2.2/2.33, tasa ancla 0.45–0.5, riñón 0.85–0.91)")
for ver, x0L, lado, umbral in casos:
    ns = []
    for ancL in (2.2, 2.332):
        for ar in (0.45, 0.50):
            for LC in ((0.85, 0.91) if x0L < 1 else (x0L,)):
                # tasa = ar*(ancL/LC)^n ; vuelco cuando tasa cruza el umbral
                ns.append(math.log(umbral / ar) / math.log(ancL / LC))
    print(f"   {ver:58s} vuelca con n {'>' if lado == '≥' else ('>' if x0L < 2.2 else '<')} {min(ns) if (lado == '≥' or x0L < 2.2) else max(ns):.2f}")

print("\nG. diseño MÍNIMO: certificar n < 2.34 (umbral de C3, el más exigente) al 95 % unilateral")
# criterio: n_ajustado + t_{k-2} · σ / sqrt(Sxx) < 2.34, con n_ajustado ≈ 1.82 (peor de las dos definiciones)
T95u_gl = {1: 6.314, 2: 2.920, 3: 2.353, 4: 2.132, 5: 2.015, 6: 1.943}
n_hat, techo = 1.82, 2.34
base_x = [math.log(1.2), math.log(1.402), math.log(2.2)]
for sig in (0.047, 0.10, 0.15):
    print(f"   ruido de tasa ±{100 * sig:.1f} %:")
    for nuevos, etiqueta in (([], "sólo los 3 de F2"),
                             ([math.log(0.5)], "+ 1 volumen de ~40 mL (LC 0.5 cm)"),
                             ([math.log(0.8)], "+ 1 volumen de ~0.15 L (LC 0.8 cm, tamaño riñón)"),
                             ([math.log(3.0)], "+ 1 volumen de ~7 L (LC 3.0 cm)"),
                             ([math.log(0.8), math.log(3.0)], "+ 0.15 L y 7 L"),
                             ([math.log(0.8), math.log(3.0), math.log(4.0)], "+ 0.15 L, 7 L y ~17 L (LC 4 cm)")):
        xs = base_x + nuevos; k = len(xs)
        m = sum(xs) / k; sxx = sum((x - m) ** 2 for x in xs)
        sup = n_hat + T95u_gl[k - 2] * sig / math.sqrt(sxx)
        print(f"      {etiqueta:62s} n ≤ {sup:.2f} -> {'CERTIFICA' if sup < techo else 'no basta'}")

print("\nH. Camino FÍSICO independiente (PRECISION.md, número de Biot)")
# Con h, material y protocolo iguales: tasa ∝ LC^-1 si Bi << 1 y ∝ LC^-2 si Bi >> 1  =>  1 ≤ n ≤ 2.
# Lo único que puede empujar el exponente APARENTE por encima de 2 es la forma (objetos no autosemejantes)
# y el ruido. Su tamaño está medido: el par 0.5→1 L de F2 dio 2.18, es decir un exceso de 0.18 sobre el techo.
exceso_obs = s12 - 2.0
for ver, x0L, lado, umbral in casos[:2]:
    ns = []
    for ancL in (2.2, 2.332):
        for ar in (0.45, 0.50):
            for LC in ((0.85, 0.91) if x0L < 1 else (x0L,)):
                ns.append(math.log(umbral / ar) / math.log(ancL / LC))
    n_vuelco = min(ns)
    print(f"   {ver}")
    print(f"      vuelca con n > {n_vuelco:.2f} · techo físico 2 + exceso observado {exceso_obs:.2f} = {2 + exceso_obs:.2f}"
          f" · haría falta un exceso de forma/ruido de {n_vuelco - 2:.2f} = x{(n_vuelco - 2) / exceso_obs:.1f} el observado")
print("   Fuga declarada: órganos reales no son bolsas (forma no autosemejante). Se acota con el exceso observado;"
      " un exceso > x1.9 el observado la abriría.")
