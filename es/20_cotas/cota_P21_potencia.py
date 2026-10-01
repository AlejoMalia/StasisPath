"""TRIADA/MATEMATICA — P21 antes de cualquier dato: ¿el diseño DECIDE?
Simulación del experimento preregistrado (L45): añadir volúmenes al montaje de F2 y ajustar tasa ∝ LC^-n.

Decisiones (fijadas aquí y copiadas literalmente a P21):
  PASA   si la cota unilateral 95 % de n < 2.34 (certifica C3 y, a fortiori, C6 con umbral 2.52)
  FALLA  si la cota unilateral 95 % INFERIOR de n > 2.34 con ≥ 4 volúmenes (C3 refutada)
  (La primera versión decía «n ajustado > 2.34»: la simulación mostró hasta un 30 % de refutaciones FALSAS
   con n real = 2.2. Corregido aquí, ANTES de cualquier dato y antes de congelar P21.)
  si no, INCONCLUSO
Ruido: σ de la tasa medida (log). Con RÉPLICAS (≥ 3 bolsas por volumen nuevo) el ruido se estima por error puro
y deja de depender de 1 grado de libertad; sin réplicas, sólo de los residuos del ajuste.
"""
import math, random

random.seed(20260926)
T95U = {1: 6.314, 2: 2.920, 3: 2.353, 4: 2.132, 5: 2.015, 6: 1.943, 7: 1.895, 8: 1.860, 9: 1.833, 10: 1.812,
        11: 1.796, 12: 1.782, 14: 1.761, 16: 1.746, 20: 1.725}
t95u = lambda gl: T95U.get(gl) or T95U[max(k for k in T95U if k <= gl)]
F2 = [(1.2, 1.4), (1.402, 0.998), (2.2, 0.47)]           # (LC cm, °C/min)
LC_RINON, LC_7L = 0.80, 3.0

def ensayo(n_true, sig, nuevos, rep):
    """Devuelve PASA / FALLA / INCONCLUSO para un experimento simulado."""
    a_true = math.log(0.47) + n_true * math.log(2.2)       # la ley pasa por el ancla de 3 L
    pts = [(math.log(L), math.log(r)) for L, r in F2]      # los 3 de F2 se usan tal cual (no se re-sortean)
    reps = []
    for L in nuevos:
        ys = [a_true - n_true * math.log(L) + random.gauss(0, sig) for _ in range(rep)]
        reps.append(ys)
        pts += [(math.log(L), y) for y in ys]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    k = len(xs); mx, my = sum(xs) / k, sum(ys) / k
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    n_hat = -b
    if rep >= 2:   # error puro de las réplicas: grados de libertad = Σ(rep-1)
        ss = sum(sum((y - sum(g) / len(g)) ** 2 for y in g) for g in reps); gl = sum(len(g) - 1 for g in reps)
        # los 3 puntos de F2 no tienen réplicas: su ruido se supone igual (declarado)
    else:
        a = my - b * mx; ss = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys)); gl = k - 2
    s = math.sqrt(ss / gl)
    sup = n_hat + t95u(gl) * s / math.sqrt(sxx)
    nvol = 3 + len(nuevos)
    if sup < 2.34: return "PASA"
    inf = n_hat - t95u(gl) * s / math.sqrt(sxx)
    if nvol >= 4 and inf > 2.34: return "FALLA"
    return "INCONCLUSO"

disenos = {"A: 1 volumen 0.15 L, sin réplicas": ([LC_RINON], 1),
           "A': 0.15 L con 3 réplicas": ([LC_RINON], 3),
           "B: 0.15 L + 7 L, sin réplicas": ([LC_RINON, LC_7L], 1),
           "B': 0.15 L + 7 L con 3 réplicas": ([LC_RINON, LC_7L], 3)}
N = 4000
print(f"{'diseño':36s} {'ruido':>6s} " + " ".join(f"{'n=' + str(n):>20s}" for n in (1.8, 2.0, 2.2, 2.5, 2.8)))
print(f"{'':36s} {'':6s} " + " ".join(f"{'PASA/FALLA/INC %':>20s}" for _ in range(5)))
for nom, (nuevos, rep) in disenos.items():
    for sig in (0.05, 0.10, 0.15):
        celdas = []
        for n_true in (1.8, 2.0, 2.2, 2.5, 2.8):
            c = {"PASA": 0, "FALLA": 0, "INCONCLUSO": 0}
            for _ in range(N): c[ensayo(n_true, sig, nuevos, rep)] += 1
            celdas.append(f"{100*c['PASA']/N:5.0f}/{100*c['FALLA']/N:3.0f}/{100*c['INCONCLUSO']/N:3.0f}")
        print(f"{nom:36s} ±{100*sig:3.0f} % " + " ".join(f"{x:>20s}" for x in celdas))
print("\nLectura: con n real ≤ 2.2 (lo físico) se quiere PASA alto y FALLA ~0 (falsos negativos de C3);"
      " con n real ≥ 2.5 se quiere FALLA alto y PASA ~0 (falsos positivos).")
