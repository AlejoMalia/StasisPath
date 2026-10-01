"""TRIADA/MATEMATICA — cota Q10 para ventanas de isquemia (preguntas 8, 9, 12).
Supuesto: tiempo tolerable de isquemia escala con 1/tasa metabólica; tasa ~ Q10^((T-37)/10).
Anclas [P]: ~5 min tolerables a 37 C; Q10 cerebral ~2.3 (McCullough 1999, a verificar en #8)."""
import math
t37, Q10 = 5.0, 2.3
print("T(C)   factor_metab   ventana_estimada")
for T in (37, 30, 25, 20, 18, 15, 10, 0, -10):
    f = Q10 ** ((T - 37) / 10)
    w = t37 / f
    print(f"{T:4d}   {f:10.3f}     {w:8.1f} min ({w/60:.1f} h)")
for nombre, objetivo_min in (("1 dia", 1440), ("1 año", 525600), ("10 años", 5256000)):
    f_req = t37 / objetivo_min
    T_req = 37 + 10 * math.log(f_req) / math.log(Q10)
    print(f"Para {nombre}: factor {f_req:.1e} -> T ~ {T_req:.0f} C (bajo 0 C => requiere cambio de fase o vidrio)")
