"""TRIADA/MATEMATICA — cota de conducción térmica antes de leer papers.
Pregunta: ¿puede calentarse desde la superficie (convectivo) un volumen vitrificado
lo bastante rápido para superar la CWR (velocidad crítica de calentamiento)?
Cota: tiempo característico de difusión t ~ r^2 / alpha (centro de un cilindro/esfera).
Tasa máxima alcanzable en el centro ~ dT / t, con dT = rango a recorrer (Tg -> ~ -20 C).
Valores de entrada = priors a verificar con fuentes #4, #5, #6."""
alpha = 1.3e-7          # m^2/s, difusividad térmica de solución CPA/tejido vítreo (orden, [P])
dT = 100.0              # K, de ~ -120 C (Tg) a ~ -20 C: zona peligrosa de desvitrificación
CWR = {"VS55": 50.0, "VM3": 3.0, "M22": 0.4}   # C/min, priors [P] a verificar
casos = {"ovocito/embrión 0.1 mm": 1e-4, "tejido 1 mm": 1e-3, "riñón rata ~1 cm": 1e-2,
         "riñón/corazón humano ~5 cm": 5e-2, "cabeza/torso ~12 cm": 0.12}
print(f"{'caso':30s} {'t_dif':>10s} {'tasa_max C/min':>15s}  " + "  ".join(f"{k}?" for k in CWR))
for nombre, r in casos.items():
    t = r**2 / alpha
    tasa = dT / (t / 60)
    ok = "  ".join(("SI  " if tasa >= c else "NO  ").rjust(len(k)+1) for k, c in CWR.items())
    print(f"{nombre:30s} {t/60:8.1f}min {tasa:15.3g}  {ok}")
