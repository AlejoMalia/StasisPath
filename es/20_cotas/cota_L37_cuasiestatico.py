"""TRIADA/MATEMATICA — L37: ¿depende el veredicto cuasiestático del εr que NO tiene fuente?

La auditoría de la tanda 52 dejó L37 abierta con esta laguna: los 360 kHz del nanowarming y la
permitividad del tejido a esa frecuencia no tienen fuente en la red. L37 afirma λ ≈ 8.3 m, que
exige εr ≈ 1.0e4.

La pregunta MATE no es «cuánto vale εr» sino «¿para qué εr se rompe el veredicto?».
Régimen cuasiestático ⇔ el cuerpo mide ≪ 1 longitud de onda ⇔ no puede formar nulos por
interferencia. Se toma como frontera L = λ.
"""
import math
c, f_nano, L = 3e8, 360e3, 0.40          # m/s, Hz, cuerpo de 40 cm
lam = lambda fr, er: c / (fr * math.sqrt(er))

print("1. Lado RMN, AHORA CON FUENTE (F82b in vivo; εr = 64 del modelo a 7T de F82c)")
for nom, fr in (("7 T (300 MHz)", 300e6), ("3 T (128 MHz)", 128e6)):
    l = lam(fr, 64)
    print(f"   {nom:16s} λ = {l*100:5.1f} cm · cuerpo de 40 cm = {L/l:5.2f} λ  (L37 afirma 13 cm/3.1 y 30 cm/1.3)")

print("\n2. Lado nanowarming: ¿para qué εr deja de ser cuasiestático?")
er_rotura = (c / (f_nano * L)) ** 2
print(f"   El veredicto se rompe cuando el cuerpo alcanza 1 λ, es decir εr ≥ {er_rotura:.2e}")
for nom, er in (("εr = 64 (valor de F82c, demasiado bajo aquí)", 64),
                ("εr = 1.0e4 (el que L37 usa, sin fuente)", 1.0e4),
                ("εr = 1.0e5 (extremo alto de la dispersión α)", 1.0e5)):
    l = lam(f_nano, er)
    print(f"   {nom:46s} λ = {l:8.2f} m · cuerpo = {L/l:.4f} λ")
print(f"\n   Margen: haría falta un εr **×{er_rotura/1.0e4:,.0f}** el que L37 supone para romperlo.")
print("   ⇒ El veredicto «el nanowarming está en régimen cuasiestático» es CIERTO en todo el")
print("     rango físicamente posible de εr de tejido. La laguna de la fuente es IRRELEVANTE")
print("     para el veredicto (patrón L43/cerebro). Lo que NO queda sostenido es la CIFRA 8.3 m.")
