#!/usr/bin/env python3
"""COTA L41 — ¿la suposición declarada en L41 puede romper su veredicto?  (tanda 48)

L41 afirma dos cosas distintas y hay que separarlas (R4: definición → unidad → suelo → impostor → afirmación):

  (a) VALOR: J(-6 C) ~ 0.57 nucleaciones por L·h, "ajustado" con los dos puntos de F85.
  (b) VEREDICTO: ese valor es COMPATIBLE con la cota independiente del riñón de cerdo
      a -2 C (J <= 3 por L·h, F20).

La salvedad que L41 declara: atribuir el 42 % de fallos a las 96 h a la NUCLEACION es una
suposición; podría ser daño isquémico, del CPA o de la propia cirugía de trasplante.
Sea phi in [0, 1] la fracción de esos fallos realmente causada por nucleación.

MODELO (el de L16: nucleación estocástica, probabilidad que crece con volumen Y tiempo)
  P(sin nucleación) = exp(-J · V · t)      (Poisson homogéneo en volumen-tiempo)
  => J(phi) = -ln(1 - 0.42·phi) / (V · t)

MONOTONIA: J(phi) es creciente en phi.  El máximo del rango está en phi = 1, que es
justo el caso que L41 supone.  => cualquier desviación de la suposición BAJA J.
Por tanto lo que los dos puntos de F85 dan no es un valor ajustado: es una COTA SUPERIOR.

UNIDADES: J en 1/(L·h). V en L. t en h.  Suelo: J >= 0 (no puede haber nucleación negativa).

SUPUESTO DECLARADO (no está en ninguna fuente de la red, así que entra como RANGO y el
veredicto se evalúa en las esquinas, como hace el motor con los parámetros):
  V hígado de rata   = 10 mL   (rango 8-14 mL; rata de 250-350 g, hígado ~4 % del peso)
  V riñón de cerdo   = 60 mL   (rango 40-90 mL; cerdo Yorkshire de 30 kg, F20)
Si el veredicto aguanta en TODAS las esquinas, el supuesto no lo sostiene.
"""
import math

ln = math.log

# ---------------------------------------------------------------- datos de la red
# F85 (V, PDF leído tanda 46): hígado de rata a -6 C, trasplante ortotópico REAL.
S72, T72 = 1.00, 72.0      # 100 % de supervivencia a 72 h
S96, T96 = 0.58, 96.0      # ~58 % de supervivencia a 96 h  => 42 % de fallos
# F20 (V, texto completo leído): 22 cerdos; -2 C durante 5 h con n = 5 + 5, SIN nucleación.
N_CERDO, T_CERDO = 5, 5.0  # brazo bajo cero del tramo de 5 h
# Regla de tres para cero eventos en n ensayos: p <= 3/n al 95 % => lambda <= -ln(1 - 3/n)
LAMBDA_CERDO = -ln(1 - 3.0 / N_CERDO)

V_RATA = (0.010, 0.008, 0.014)     # L: central, lo, hi
V_CERDO = (0.060, 0.040, 0.090)

def J_rata(phi, V):
    """Tasa de nucleación implicada por F85 si una fracción phi de los fallos es nucleación."""
    if phi <= 0: return 0.0
    return -ln(1 - (1 - S96) * phi) / (V * T96)

def J_cerdo(V):
    """Cota superior de F20 por la regla de tres (cero nucleaciones en n = 5 a 5 h)."""
    return LAMBDA_CERDO / (V * T_CERDO)

print(__doc__)
print("=" * 78)
print(f"Cota del cerdo (F20): lambda_max = -ln(1-3/{N_CERDO}) = {LAMBDA_CERDO:.4f} eventos en {T_CERDO:g} h")
for lab, V in zip(("central", "lo", "hi"), V_CERDO):
    print(f"   V = {V*1000:5.0f} mL ({lab:7s}) -> J <= {J_cerdo(V):6.3f} por L·h")
print(f"   ** reproduce el 'J <= 3 por L·h' que L41 tenía escrito a mano: "
      f"{J_cerdo(V_CERDO[0]):.2f} con V = 60 mL **")
print()
print(f"Punto de F85 a 72 h: supervivencia {S72:.0%} => lambda ~ 0 => no acota por arriba "
      f"(es consistente con cualquier J pequeña); el punto informativo es el de 96 h.")
print()
print("J implicada por F85 a -6 C, barriendo la SUPOSICION phi y el volumen:")
print(f"{'phi':>6} | " + " | ".join(f"V={v*1000:.0f} mL" for v in V_RATA))
for phi in (1.0, 0.75, 0.50, 0.25, 0.10, 0.01):
    print(f"{phi:6.2f} | " + " | ".join(f"{J_rata(phi, v):8.3f}" for v in V_RATA))
print()

# ---------------------------------------------------------------- veredictos
J_MAX = max(J_rata(1.0, v) for v in V_RATA)          # esquina peor: phi = 1 y V mínimo
J_CERDO_MIN = min(J_cerdo(v) for v in V_CERDO)       # esquina peor: la cota más estricta
print(f"Esquina PEOR para la compatibilidad: J_rata maxima = {J_MAX:.3f} (phi=1, V={V_RATA[1]*1000:.0f} mL)")
print(f"                                     J_cerdo minima = {J_CERDO_MIN:.3f} (V={V_CERDO[2]*1000:.0f} mL)")

ok_todas = all(J_rata(phi, vr) <= J_cerdo(vc)
               for phi in [i / 100 for i in range(0, 101)]
               for vr in V_RATA for vc in V_CERDO)
print()
print(f"V1 (clave) 'compatible con la cota del cerdo' en TODO el rango de la suposición "
      f"phi in [0,1] y en todas las esquinas de volumen: {'MATE' if ok_todas else 'FUGA'}")
print(f"V2 (clave) 'lo que F85 da es una COTA SUPERIOR, no un valor ajustado': "
      f"MATE por monotonia (dJ/dphi > 0, maximo en phi=1)")
print(f"V3 (NO clave) 'el valor central 0.57 es el valor verdadero de J': "
      f"ABIERTO — depende de phi, que nadie ha medido")
print()
print(f"Holgura de V1 en la esquina peor: factor x{J_CERDO_MIN / J_MAX:.2f} "
      f"(haría falta phi > 1, imposible, para romperla)")
# ¿qué haría falta para romper V1? J_rata > J_cerdo exige mas fallos que el 42 % observado.
frac_rotura = 1 - math.exp(-J_CERDO_MIN * V_RATA[1] * T96)
print(f"Para romper V1 harían falta {frac_rotura:.1%} de fallos por nucleación a las 96 h; "
      f"F85 observa {1-S96:.0%} en TOTAL.")
print()
print("FUGAS DECLARADAS de la cota superior J <= 0.57 por L·h:")
print(" 1. Supone 'nucleación => fallo del injerto'. Si nuclear fuera sobrevivible, J sería MAYOR.")
print("    Apoyo en la red: F22 (dep de L41) congeló higados de cerdo a -2 C 24 h como control")
print("    y midió 98 % de picnosis nuclear, destrucción severa => a escala de órgano,")
print("    nuclear NO es sobrevivible. La misma convención la usa la cota del cerdo (F20),")
print("    así que la comparación es consistente en convención.")
print(" 2. Supone Poisson homogéneo (J·V·t). Es el modelo de L16 [V], no un añadido.")
print(" 3. El 42 % incluye la mortalidad de la propia cirugía de trasplante: eso BAJA J,")
print("    no la sube => refuerza la cota, no la rompe.")
print(" 4. Extrapolar J de -6 C (rata) a -2 C (cerdo) no se hace aquí: son dos cotas")
print("    independientes a dos temperaturas, y sólo se comprueba que NO se contradigan.")
