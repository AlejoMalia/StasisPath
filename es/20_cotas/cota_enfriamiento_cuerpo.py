"""TRIADA/MATEMATICA — C3: ¿se puede VITRIFICAR (enfriar) un cuerpo por convección?
Ancla MEDIDA [V] (Etheridge/Bischof, preprint bioRxiv 2024.11.08.622572 = #2):
 3 L M22 en cryobag, LC ~2.2 cm -> ~0.45-0.5 C/min en el centro; 0.5 L LC 1.2 cm -> 1.4 C/min.
Escalado difusivo: tasa ~ 1/LC^2 (verificado entre los dos puntos medidos: (2.2/1.2)^2=3.4 vs 1.4/0.5=2.8).
LC = V/A (longitud característica). CCR medidos [V]: M22 ~0.1, VMP-riñón ~5.4, VS55 2.5, VS55-riñón <1 C/min."""
ancla_LC, ancla_rate = 2.2, 0.47
CCR = {"M22": 0.1, "VS55(tejido)": 1.0, "VMP": 5.4}
objetos = {  # LC = V/A, en cm
    "riñón humano (~0.15 L)": 1.0, "corazón/riñón en 1 L": 1.4, "hígado humano (~1.5 L)": 1.8,
    "cabeza (esfera r~9 cm, LC=r/3)": 3.0, "cuerpo entero (V=0.07 m3, A=1.8 m2)": 3.9,
    "tronco (cilindro r~15 cm, LC=r/2)": 7.5}
print(f"{'objeto':40s} {'LC cm':>6s} {'tasa C/min':>10s}  " + "  ".join(CCR))
for n, lc in objetos.items():
    r = ancla_rate * (ancla_LC / lc) ** 2
    print(f"{n:40s} {lc:6.1f} {r:10.3f}  " + "  ".join(("OK" if r >= c else "NO").center(len(k)) for k, c in CCR.items()))
