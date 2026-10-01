# Semana 2: hibernación natural y definiciones de muerte

Fuentes nuevas: F11 = Larson et al. 2014, *J Exp Biol* 217:2193 (rana de bosque de Alaska) · F12 = Wu, Sunagawa, Chen 2025, revisión de torpor sintético (PMC12659898) · F13 = Nordeen & Martin 2019, *Physiology* 34:101 (sólo el resumen; el texto completo dio 403) · F14 = McKenzie et al. 2024, *Brain Sci* 14:942, hoja de ruta de biostasis (PMC11430499) · F15 = McKenzie, "Defining Death" (brainpreservation.github.io) · F16 = Wowk 2022, "Matters of Life and Death", *Cryonics* 43(3) · F17 = Shemie et al. 2023, *Can J Anaesth* 70:483 (sólo el resumen) · F18 = Tessier et al. 2022, *Nat Commun* 13:4008 (congelación parcial) · F19 = datos de la tortuga pintada, del lémur *Cheirogaleus* y del pez pulmonado (resúmenes y fichas; calidad media).

---

## H1: ¿La hibernación y la tolerancia a la congelación de los anfibios son una salida de C2? · [M]
**Cota C4, escrita antes de leer** (`20_cotas/cota_anfibios.py`): ¿cuánta supresión extra, no térmica, hace falta frente a la ventana que C2 concede a un mamífero?

| organismo | condición | duración medida | supresión extra vs C2 |
|---|---|---|---|
| Rana de bosque (Alaska) | congelada, media −6.3 °C, mínima −18 °C, 100 % de supervivencia (n = 18) | 193 ± 11 días [V F11] | ×1 500 |
| Rana, tras ciclos de congelación | hasta −18 °C | 218 días [V F11] | ×1 700 |
| Tortuga pintada adulta | **anoxia total** a 3 °C | 177 días [V F19] | ×3 000 |
| Tortuga pintada | anoxia a **22 °C** | > 30 h [V F19] | ×100 |

**Línea forzada:** un factor ×100 a 22 °C demuestra que la tolerancia **no depende de la temperatura**. Es bioquímica: tolerancia a la anoxia, metabolismo basal de ectotermo y crioprotector endógeno (la glucosa sube ×13 en el músculo de la rana, F11). ⇒ **C2 no cae, pero se acota su dominio:** vale para *tejido de mamífero sin reprogramación bioquímica*. La salida existe como **biología**, no como física.

**Qué aporta la rana a StasisPath:**
1. **Una tercera vía física además del vidrio: hielo extracelular controlado.** La rana tolera ~65 % del agua corporal como hielo [P, cifra clásica de Storey; no releída] porque controla dónde se forma. Esto contradice el supuesto de la semana 1 de que "bajo 0 °C, o vidrio o nada". La formulación correcta es: **o vidrio, o hielo extracelular controlado con crioprotector endógeno.**
2. **Ya tiene un residual clínico:** la congelación parcial de hígado de rata a −10/−15 °C, inspirada explícitamente en animales tolerantes a la congelación, alarga 5 veces la conservación, con función algo peor que los controles (F18). Es el puente rana → clínica.
3. **Límite de escala:** la rana pesa decenas de gramos y se congela en horas. C3 (enfriamiento ∝ 1/LC²) no la limita porque congelar no exige una CCR. **Pregunta abierta [A]:** ¿escala la congelación parcial controlada a LC de ~4 cm sin daño mecánico por el hielo? No hay datos más allá del hígado de rata.

## H2: Torpor e hibernación en mamíferos, incluidos primates · [V]
| sistema | metabolismo | T corporal | duración continua | fuente |
|---|---|---|---|---|
| Ardilla ártica | 2–4 % | −3 °C | ≤ ~3 semanas por episodio; temporada de 9 meses con despertares | F10 |
| **Lémur *Cheirogaleus medius*** (**primate**) | hasta ~2 % | sigue al ambiente (oscila hasta 25 °C al día) | hasta 7 meses por temporada | F19 |
| Ratón, activación de neuronas Q | −75 % | −34 % | ~1 semana | F12 |
| Ratón, H₂S | −90 % VO₂ | −22 °C (a 13 °C ambiente) | horas | F12 |
| Cerdo/oveja, H₂S | sin reducción significativa | — | — | F12 |
| Macaco, activación quimiogenética del área preóptica | sin torpor real: tiritona, FC +40–60 lpm | −1.3/−1.7 °C | — | F12 |
| Humano | **ningún dato**; ensayos con H₂S terminados antes de tiempo por complicaciones cardiorrespiratorias | — | — | F12 |

**Líneas forzadas:**
- **Un primate hiberna meses con el metabolismo cerca del 2 % y el cuerpo templado** ⇒ la hibernación no exige frío y no es ajena al linaje primate. Es la mejor prueba de que el programa existe en el genoma de un pariente (lo sostiene F13).
- **La inducción farmacológica o neural no escala:** funciona en ratón y falla en cerdo, oveja y macaco (F12). La razón superficie/volumen del roedor hace que no sea buen modelo del humano (F12).
- **Toda hibernación de mamífero tiene despertares periódicos** ⇒ no es una pausa continua. La máxima duración continua medida es ~3 semanas.

## H3: Corrección a la Q12 de la semana 1 (R2: se corrige el texto, no el umbral)
En la semana 1 afirmé que ningún sistema biológico pasa años en pausa continua sin vidrio. **Es incorrecto tal como estaba escrito:** el pez pulmonado africano estiva desde algunos meses **hasta 3–4 años** a temperatura templada (F19). Matiz: es **hipometabolismo** con respiración aérea y consumo de reservas, no una pausa.
**Reformulación que sí es forzada:** *ningún **mamífero** conocido reduce su metabolismo de forma continua durante más de ~3 semanas sin despertar, y ninguno lo mantiene más de ~9 meses por temporada.* Para un humano durante años, el veredicto sigue siendo vitrificación (C2 en su dominio) **o bien** hipometabolismo de tipo pulmonado o lémur, que es una vía **biológica** sin demostrar en mamíferos grandes.

## H4: Presupuesto de combustible del torpor humano (Q13) · [P] cota C5
Con un metabolismo basal de ~1 700 kcal/día y 7 700 kcal/kg de tejido adiposo: 1 año al 25 % del basal ≈ 20 kg de grasa; al 3 % (nivel lémur o ardilla) ≈ 2.4 kg.
⇒ **Si se lograra un torpor profundo, la energía deja de ser el problema: con ~20 kg de reservas basta.** Los problemas pasan a ser la atrofia, el hueso, la radiación, los despertares y el control. Es la razón de F13 para preferir imitar la hibernación en vez de la hipotermia terapéutica.

---

## D1: Definiciones de muerte: capas y umbrales (refina Q1 y Q2) · [V]/[P]
| capa | criterio | ¿reversible hoy? | fuente |
|---|---|---|---|
| Muerte clínica | parada circulatoria, ausencia de consciencia | sí: DHCA y EPR demuestran que la pausa es reversible | F4, F9, F15 |
| **Muerte legal por criterio circulatorio** | cese **permanente**, no necesariamente irreversible: no volverá espontáneamente y no se intentará restaurar; ~5 min de observación en Canadá [P, práctica estándar; el resumen de F17 no lo cita] | depende de la decisión de no reanimar | F17 |
| **Muerte legal por criterio neurológico** (Canadá 2023) | cese permanente de la función cerebral: sin consciencia, sin reflejos de tronco, sin respiración autónoma | no | F17 |
| Muerte celular | pérdida de la capacidad de recuperar función de forma aguda | **tras 20 min de muerte clínica aún no ha muerto ninguna neurona** en ese sentido; en rata, 15 % de necrosis a las 6 h y 65 % a las 12 h | F16, F5 |
| **Muerte teórico-informacional** ("muerte total") | la información que codifica memoria e identidad ya no puede inferirse, ni siquiera en principio | criterio físico, independiente de la tecnología | F15, Merkle (sin releer) |

**Líneas forzadas nuevas:**
1. **"Permanente" (decisión) ≠ "irreversible" (física).** La definición legal canadiense se apoya en la permanencia. StasisPath mide la irreversibilidad. Q2 queda cerrada con más fuerza: la muerte legal es un umbral **normativo**, y la información es un umbral **físico**.
2. **Hay una brecha de horas entre el umbral del organismo (~5 min de τ_eq) y el de la célula (≥ 20 min hasta horas).** Lo que es irreversible a los 5 minutos no es que las neuronas mueran, sino **que la reperfusión se maneje mal** (no reflujo, hiperemia reactiva a los 10 min, F16). ⇒ **El umbral de τ_eq no es una constante física: depende de la medicina de reperfusión.** Hay que reportarlo como τ_eq,org (≈ 5–12 min, con la medicina actual) separado de τ_eq,cel (≥ 20 min y hasta horas).
3. **Criónica, según su propia literatura:** la vitrificación cerebral completa verificada por TC sólo se ha visto en casos con **< 10 min** entre la parada y la declaración de muerte y un equipo presente. Las demostraciones premiadas **no tuvieron parada circulatoria** (F16). Wowk distingue Tipo I (ideal, τ_eq bajo) de Tipo II (condiciones peores), y reconoce que el caso científico sólo cubre el Tipo I. Esto confirma y endurece la Q14.

## D2: Preservación frente a estasis: taxonomía adoptada · [V]
La hoja de ruta de biostasis (F14) separa: **(a) preservación demostrablemente reversible = estasis o animación suspendida**, y **(b) preservación de rasgos informacionales, no reversible con la tecnología conocida.** F15 lo resume en que la preservación cerebral no es animación suspendida. **StasisPath adopta esta frontera como eje principal:** sólo (a) cuenta como residual clínico o espacial; (b) es un programa de información (escala E0).
Métricas propuestas por F14 para (b): trazabilidad por EM, anotación biomolecular, densidad y concentración de crioprotector por TC, viabilidad y LTP tras recalentar. **F14 no da umbrales numéricos** ⇒ StasisPath puede aportarlos (ver Q15).

## D3: Memoria tras vitrificación (Q15.4 ya tiene un dato) · [V con fuente secundaria]
*C. elegans* entrenado con un olor (benzaldehído), vitrificado 30 min a −196 °C y recalentado **conserva la preferencia aprendida** (Vita-More & Barranco 2015, citado en F15). Es el primer punto E2 con información: la pausa en vidrio puede conservar memoria de largo plazo en un sistema nervioso real, aunque de 302 neuronas. [A] Falta leer el paper primario y verificar n y controles.

---

## Impacto en el marco
- **Q1:** τ_eq se desdobla en τ_eq,org y τ_eq,cel (D1.2). Se añade una sexta magnitud candidata, **f_hielo,intra**: la fracción de hielo **intracelular**, porque la rana muestra que el hielo extracelular controlado es tolerable (H1).
- **Q12:** hay dos vías para años: la física (vidrio) y la biológica (hipometabolismo de tipo pulmonado o lémur, sin demostrar en mamíferos grandes).
- **Q18:** a la afirmación se le añade una cláusula: *la condición (a) puede sustituirse por hielo sólo extracelular con crioprotector si la fracción de hielo intracelular es 0; esa vía está demostrada en ectotermos de < 100 g y en hígado de rata (5× de conservación), no por encima.*
