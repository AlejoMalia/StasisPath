"""TRIADA/MATEMATICA — C4: ¿la tolerancia a congelación de anfibios es una fuga de C2?
C2 (verificada en humano): ventana ~ 5 min x Q10^((37-T)/10), Q10=2.3, ancla = cerebro de MAMÍFERO.
Prior [P] a verificar: rana de bosque (Rana sylvatica, Alaska) sobrevive ~meses congelada a ~-6 C
(corazón parado, ~65 % del agua corporal como hielo extracelular, glucosa como crioprotector).
Pregunta: ¿cuánta supresión EXTRA (no térmica) haría falta respecto a C2 para explicar eso?"""
t37, Q10 = 5.0, 2.3
for T, dias in ((-2.5, 14), (-6, 60), (-6, 218), (-16, 60)):
    ventana_C2 = t37 * Q10 ** ((37 - T) / 10)          # min que C2 concede a un mamífero
    extra = dias * 1440 / ventana_C2
    print(f"T={T:6.1f} C  dias={dias:4d}  C2 concede {ventana_C2:7.0f} min  -> supresión extra requerida x{extra:,.0f}")
print("\nSi extra >> 1: la fuga NO es térmica; es bioquímica (tolerancia a isquemia/anoxia,"
      "\nmetabolismo basal de ectotermo, crioprotector endógeno). C2 no cae: se acota su dominio a"
      "\n'tejido de mamífero sin reprogramación bioquímica'.")

# --- Verificación con datos [V] (2026-09-26) ---
print("\n[V] casos medidos vs C2 (ancla mamífero):")
casos = [("rana de bosque Alaska, congelada", -6.3, 193), ("rana, tras ciclos congelación-descongelación", -6.3, 218),
         ("tortuga pintada adulta, ANOXIA", 3.0, 177), ("tortuga pintada, anoxia", 22.0, 30/24)]
for n, T, dias in casos:
    v = t37 * Q10 ** ((37 - T) / 10)
    print(f"  {n:46s} T={T:5.1f}  {dias:7.1f} d  -> extra x{dias*1440/v:,.0f}")

# --- C5: combustible para torpor humano (Q13) ---
print("\nC5 — reserva de grasa para 1 año de torpor humano (BMR ~1700 kcal/d, grasa 9 kcal/g, ~7700 kcal/kg tejido adiposo):")
for nombre, frac in (("oso (~25 % BMR)", 0.25), ("Q-neurons ratón (~25 %)", 0.25), ("lémur/ardilla (2-4 %)", 0.03)):
    kcal = 1700 * frac * 365
    print(f"  {nombre:28s} {kcal:9,.0f} kcal/año  = {kcal/7700:5.1f} kg de tejido adiposo")
