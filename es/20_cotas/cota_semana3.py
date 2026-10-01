"""TRIADA/MATEMATICA — semana 3. Tres cotas escritas ANTES de leer.
C6: ¿la congelación parcial está limitada térmicamente a LC ~4 cm?
C7: techo de lo que la reperfusión óptima puede mover τ_eq,org.
C8: forma de la tensión CCR-bajo <-> toxicidad del CPA."""
import math
print("C6 — congelación parcial (hielo extracelular) a escala de órgano")
# (a) velocidad: el hielo extracelular EXIGE enfriar LENTO (deshidratación celular, Mazur): óptimo ~0.1–1 C/min [P]
# C3 dio a LC 4 cm ~0.15 C/min por convección -> la lentitud juega A FAVOR.
for LC in (1.0, 1.4, 2.2, 4.0):
    rate = 0.47 * (2.2 / LC) ** 2
    print(f"  LC={LC:.1f} cm  enfriamiento convectivo ~{rate:.2f} C/min  (ventana 'lenta' 0.1-1 C/min: {'SI' if 0.1 <= rate <= 1.5 else 'NO'})")
# (b) calor latente: congelar 50 % del agua de un órgano de 1 kg (80 % agua)
Q = 0.5 * 0.8 * 334e3          # J
for LC in (1.4, 4.0):
    A = 1e-3 / (LC / 100) * (1.0)   # m2 para 1 L... escala A = V/LC
    P = 100 * A * 10               # h=100 W/m2K, dT=10 K
    print(f"  calor latente 1 kg, LC={LC} cm: {Q/1e3:.0f} kJ / {P:.0f} W = {Q/P/60:.0f} min")
print("  => térmicamente NO limitado: el límite de C6 es biológico o mecánico (nucleación uniforme, 9 % de expansión en espacio vascular, soluto a -15 C).")

print("\nC7 — techo de la reperfusión óptima")
t_org, t_cel_min = 5, 20      # min: umbral del organismo (F4) vs 'ninguna neurona muerta a 20 min' (F16)
necrosis = {6*60: 0.15, 12*60: 0.65}   # rata, F5
print(f"  suelo actual τ_org ≈ {t_org} min; techo teórico = tolerancia celular ≥ {t_cel_min} min, necrosis del 15 % a 6 h")
print(f"  => la medicina de reperfusión podría mover el umbral x{t_cel_min/t_org:.0f} (seguro) hasta x{360/t_org:.0f} (si 15 % de necrosis es recuperable).")
print("  Predicción a verificar: los mejores datos animales o ex vivo caen entre 15 min y unas pocas horas, no más allá.")

print("\nC8 — tensión CCR ↔ toxicidad")
# CCR medidos [V]: VMP 5.4 (8.4 M), VS55 2.5 (8.4 M), M22 0.1 (~9.3 M)
pts = [("VS55", 8.4, 2.5), ("VMP", 8.4, 5.4), ("M22", 9.3, 0.1)]
# pendiente log10(CCR)/M entre la clase 8.4 M y M22
s = (math.log10(0.1) - math.log10(2.5)) / (9.3 - 8.4)
print(f"  pendiente ~{s:.1f} décadas de CCR por mol/L  => +1 M de CPA baja la CCR ~{10**-s:.0f}x")
print("  Requisito C3 para LC 4 cm (~0.15 C/min): CCR ≤ 0.1 => hace falta CPA de la clase M22 o superior.")
print("  => toxicidad: necesito la ley. Hipótesis a verificar: toxicidad ~ f(qv*) de Fahy, no ~ concentración total;")
print("     y cargar a baja temperatura (−22 °C) reduce la toxicidad (Arrhenius). Si se cumplen, la tensión no es dura: es diseño de mezcla.")
