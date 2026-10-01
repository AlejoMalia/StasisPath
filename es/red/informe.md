<!-- AUTO-GENERADO por red/motor.py desde red/stasispath.yaml. NO EDITAR A MANO. -->

## Derivadas (calculadas, no escritas a mano)
| magnitud | unidad | valor | qué es |
|---|---|---|---|
| LC_esfera | cm | función | LC de una esfera de agua de masa m (g) |
| tasa_conv | °C/min | función | enfriamiento convectivo en el centro (C3) |
| b_CCR | décadas/M | -1.74 | pendiente local de log10(CCR) frente a molaridad |
| a_CCR |  | 15.2 | ordenada de la recta CCR-molaridad |
| M_de_CCR | mol/L | función | molaridad necesaria para una CCR dada |
| M_toxico | mol/L | 9.28 | molaridad a la que la respiración basal cae a la mitad |
| LC_viable | cm | 4.59 | LC crítica de F2 |
| masa_viable | kg | 10.9 | masa crítica de F2 |
| tasa_canal | °C/min | 0.0387 | media canal de vacuno, 40->4 °C en 15.5 h (F79) |
| razon_canal |  | 0.957 | medido/predicho a escala de 150 kg |
| limite_LNG | °C/min | 0.15 | límite industrial de enfriamiento sin daño estructural (F84) |

## Órganos (una línea cada uno; lo demás se calcula)
| órgano | masa g | LC cm | tasa °C/min | M exigida | veredicto |
|---|---|---|---|---|---|
| riñón | 150 | 1.1 | 1.88 | 8.57 | viable |
| corazón | 300 | 1.38 | 1.19 | 8.68 | viable |
| hígado | 1,500 | 2.37 | 0.406 | 8.95 | viable |
| cerebro | 1,400 | 2.31 | 0.425 | 8.94 | viable |
| cuerpo_entero | 70,000 | 8.52 | 0.0313 | 9.59 | **no viable** |
| páncreas | 90 | 0.927 | 2.65 | 8.48 | viable |

# Informe de la red

Nodos: 251 · preregistro: intacto (5 preregistros) · progreso: 97.3 %

## Avisos
- ninguno

## Cotas
| cota | ley | salidas: central (rango en esquinas) | veredictos | estatus |
|---|---|---|---|---|
| C1 | Recalentamiento convectivo: radio crítico r* = √(α·ΔT/CWR) | rstar_M22 = 4.42 (2.83–6.2), rstar_VMP = 0.355 (0.262–0.458) | ✔ VMP exige calentamiento volumétrico por encima de 1 cm → M; ✔ M22 no se recalienta por superficie en el tronco (r ~15 cm) → M | **M** |
| C2 | Hipotermia sin cambio de fase: ventana = t37·Q10^((37−T)/10) | w15 = 31.2 (20–46.2), w10 = 47.4 (28.9–73.5), w0 = 109 (60.1–186), T10y = -129 (-155–-110), T10y_frio = -73.7 (-115–-57.9) | ✔ 10 años exigen T < 0 °C con CUALQUIER Q10 medido (templado y frío) → M; ✔ el Q10 del tramo frío exige MENOS frío que el templado (no-linealidad, NO significativa en la fuente) → A (no clave) | **M** |
| C3 | Enfriamiento convectivo: tasa ∝ 1/LC² anclada en 3 L; LC* = LC₀·√(tasa₀/CCR) | LCstar_M22 = 4.77 (3.48–9.33), LCstar_VMP = 0.649 (0.464–0.796), rate_kidneyH = 2.94 (1.82–4.59), rate_body = 0.15 (0.0943–0.257), rate_trunk = 0.0404 (0.0189–0.105) | ✔ VMP no vitrifica un riñón humano por convección → M; ✔ M22 vitrifica el cuerpo medio (LC ~3.9 cm) → A (no clave); ✔ M22 falla en el centro del tronco → A (no clave) | **M** |
| C4 | Supresión extra (no térmica) de los ectotermos frente a C2 | frog = 1.51e+03 (785–3.08e+03), turtle = 3e+03 (1.53e+03–5.28e+03), turtle22 = 103 (59.6–180) | ✔ rana > ×100 → M; ✔ tortuga > ×100 → M; ✔ tortuga a 22 °C > ×10 (no térmico) → M | **M** |
| C5 | Combustible para 1 año de torpor humano | kg25 = 20.1 (17.8–23.7), kg3 = 2.42 (2.13–2.84) | ✔ 1 año al 25 % < 30 kg de grasa → M | **M** |
| C6 | Congelación parcial: ¿el calor limita a LC 4 cm? | rate4 = 0.142 (0.11–0.206), latent4 = 89.1 | ✔ LC 4 cm dentro de la ventana lenta 0.1–1 °C/min → M; ✔ calor latente < 3 h → M | **M** |
| C7 | Techo de la reperfusión: τ_org frente a τ_cel | tau_org_good = 12.5 (10–12.5), tau_org_surv = 17, tau_cel = 240, f_org = 2.5 (1.67–3.12), f_cel = 48 (40–60), legal_x = 2.5 (2–2.5), f_exist = 12 (10–15) | ✔ zona gris: τ_cel > τ_org (sobrevive con déficit) → M; ✔ existencia fuera de lo reproducible: τ_org,bueno < τ_exist ≤ τ_cel → M; ✔ la muerte legal se declara antes del umbral del organismo → M | **M** |
| C8 | Tensión CCR ↔ toxicidad: CCR requerida a LC 4 cm | CCR_req4 = 0.142 (0.11–0.206) | ✔ VMP insuficiente a LC 4 cm → M; ✔ M22 suficiente a LC 4 cm → A (no clave) | **M** |
| C9 | Hipotermia accidental a 13.7 °C: ¿fuga de C2? | w137 = 34.8 (22–52.2), extra = 11.8 (7.9–18.7) | ✔ no lo explica el flujo cero de C2 (×>3) ⇒ hubo bajo flujo → M | **M** |
| C11 | Conflicto de velocidad: banda de lesión por frío frente a hielo extracelular | t_banda_lento = 20, t_banda_conv = 141 (97.2–181), rate4 = 0.142 (0.11–0.206) | ✔ cruzar la banda 0-20 C enfriando lento tarda > 15 min (exposicion real) → M; ✔ a LC 4 cm la conveccion es aun mas lenta que el techo lento → M | **M** |
| C10 | Calibración de C2 en DOS mamíferos: perro con flush (120 min) y cerdo (60 min), ambos a ~10 °C | w = 47.4 (20–73.5), w_pig = 47.4 (28.9–73.5), extra = 2.53 (1.63–5.99), extra_pig = 1.27 (0.816–2.08) | ✔ C2 calibra dentro de ×5 contra el CERDO a 10 °C → M; ✔ C2 es conservadora frente al cerdo (no robusto: en la esquina generosa se vuelve OPTIMISTA) → A (no clave); ✔ C2 dentro de ×5 del perro con flush (protocolo distinto, no clave) → A (no clave) | **M** |

## Encuentros
- distancia de la meta a la frontera: 2.5 órdenes de magnitud
- huecos: t×tox, masa×CCR, E×CCR, CCR×tox
