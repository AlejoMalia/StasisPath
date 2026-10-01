# Semana 3: congelación parcial a escala, techo de la reperfusión y toxicidad del crioprotector

Cotas escritas antes de leer: `20_cotas/cota_semana3.py` (C6, C7, C8).
Fuentes nuevas: F20 = Calderon Novoa et al. 2025, *Am J Transplant* 26:91 (riñón de cerdo, conservación bajo cero con autotrasplante; resumen) · F21 = Ozgur et al. 2024, *Sci Rep* 14:25260 (congelación parcial optimizada, 10 días, hígado de rata; resumen) · F22 = conservación isocórica sobreenfriada de hígado de cerdo (PMC10203736; resumen del buscador) · F23 = Vrselja et al. 2019, *Nature* (BrainEx, PMC6844189) · F24 = OrganEx 2022, *Nature* (resumen) · F25 = Safar et al., estudios en perros (resúmenes de PubMed 2237954 y 8446790) · F26 = Fahy, Wowk, Wu, Paynter 2004, *Cryobiology* 48:22 (qv*; resumen) · F27 = formulario nacional de Saskatchewan (2023), que reproduce las recomendaciones de la guía canadiense.

---

## T1 (C6): ¿Escala la congelación parcial controlada a órganos de ~4 cm? · [M] en física / [A] en biología
**La cota prerregistrada dice que el calor no limita.** El hielo extracelular exige enfriar **lento** (0.1–1 °C/min, para que la célula se deshidrate y no forme hielo interno). La convección a LC de 1.4–4 cm da 1.2–0.14 °C/min, justo en esa ventana. **A diferencia del vidrio (C3), el tamaño juega a favor.** El calor latente (congelar la mitad del agua de 1 kg) se evacua en ~30–90 min.

**Datos:**
| sistema | escala | T y método | duración | resultado | fuente |
|---|---|---|---|---|---|
| Hígado de rata | LC < 1 cm | −15 °C, congelación parcial con nucleador y crioprotector | 5 días → **10 días** (protocolo optimizado) | supera al frío estático | F18, F21 |
| **Riñón de cerdo** (tamaño humano) | LC ~1–1.5 cm [P] | "bajo cero" (T exacta no dada en el resumen) | 24–48 h | autotrasplante, 0 % de mortalidad, 7 días de seguimiento, **sin cristales de hielo en la histología**, función comparable al frío estático | F20 |
| Hígado de cerdo | ~1–1.5 L | −2 °C, sobreenfriamiento **isocórico** (volumen constante) | 24–48 h, sin congelarse (medido por presión) | factible | F22 |

**Línea forzada:**
1. El **sobreenfriamiento** sin hielo ya funciona a escala de órgano humano durante 1–2 días (F20, F22).
2. La **congelación parcial** con hielo sólo está demostrada en hígado de rata (10 días). **No hay datos a escala de órgano grande.**
3. Por C6, lo que falta **no es térmico**. Faltan tres cosas: (a) nucleación **uniforme** en todo el volumen, porque si no hay sobreenfriamiento seguido de congelación súbita; (b) daño **mecánico** por la expansión del 9 % del hielo en el espacio vascular, que el sistema isocórico ataca de raíz; (c) carga y descarga del crioprotector (edema y resistencia vascular, F21).
⇒ **Veredicto MATE:** la escala de 4 cm **no está prohibida por la física**. El límite es de ingeniería biológica y no hay dato. Es la vía con **mejor relación entre riesgo físico y ganancia** de todo el programa: días a semanas, no años.

## T2 (C7): ¿Cuánto puede mover una reperfusión óptima el límite de 5 min? · [V]
**Cota prerregistrada:** entre ×4 (techo seguro, porque a los 20 min no ha muerto ninguna neurona) y ×72 (necrosis del 15 % a las 6 h). Predicción: los mejores datos caerían entre 15 min y unas pocas horas.

| nivel | condición | dato | factor frente a 5 min | fuente |
|---|---|---|---|---|
| Umbral legal | observación mínima para declarar la muerte (donación controlada) | **5 min** sin circulación, presión de pulso ≤ 5 mmHg; **10 min** en donación no controlada; la cuenta se reinicia si vuelve la circulación | ×1 | F27 [V] |
| Clínico | RCP y cuidados estándar | ~5 min | ×1 | F4 |
| Organismo, reperfusión estándar | perros, fibrilación normotérmica | 7.5, 10 y 12.5 min **sin diferencias** en déficit neurológico | ×2.5 | F25 |
| **Organismo, reperfusión óptima** | perros: circulación extracorpórea con hipotermia **durante la reperfusión** | **17 min** normotérmicos, 18/18 supervivientes (el grado neurológico exacto sigue [P]) | **×3.4** | F25 |
| Celular y sináptico | BrainEx, cerebro de cerdo | **4 h** post mortem: viabilidad celular, sinapsis espontáneas y metabolismo activo; **sin actividad global (EEG plano)**, con bloqueantes neuronales en el perfundido | ×48 | F23 |
| Celular multiorgánico | OrganEx, cerdo entero | 1 h de isquemia caliente seguida de 6 h de perfusión: menos muerte celular en cerebro, corazón, hígado y riñón | ×12 | F24 |

**Línea forzada (predicción cumplida):**
- **La reperfusión óptima mueve el umbral del organismo ~×3.4 con recuperación demostrada (5 → 17 min),** dentro del rango "seguro" ×4 de C7.
- **El umbral celular está al menos en 4 h (×48).** Ahí la célula vuelve, pero la función global no se ha demostrado.
- ⇒ **La zona gris de StasisPath es exactamente 17 min – 4 h de isquemia normotérmica.** Dentro de ella, las células son recuperables y el organismo no se ha demostrado recuperable. **Es la frontera empírica de la pregunta canónica**, con números en ambos extremos.
- **Consecuencia legal (cierra Q2):** la muerte se declara a los **5 min**, entre 3.4 y ~50 veces **antes** del límite de irreversibilidad demostrado. "Permanente" es una decisión (no se reanimará); no es irreversibilidad física.

## T3 (C8): Toxicidad del crioprotector (Q6) · [V] como ley / [A] como umbral numérico
**Cota prerregistrada:** a LC ~4 cm hace falta una CCR ≤ 0.1 °C/min, es decir, la clase M22. Hipótesis: la toxicidad sigue a qv* y no a la concentración total, y la tensión con la CCR es blanda.

**Verificado (F26, Fahy et al. 2004):**
- La teoría de qv* (**moléculas de agua por grupo polar del crioprotector** en la concentración mínima que vitrifica) **explicó la toxicidad de 20 soluciones** de vitrificación en loncha de corteza renal de conejo. La toxicidad es **proporcional a la fuerza media del puente de hidrógeno con el agua**: cuanto menos perturba el agua intracelular, menos tóxica es la solución.
- **Diseñando por qv*:** riñones enteros de conejo perfundidos a −3 °C con **8.4 M** (antes **100 % letal** a esa temperatura) **no mostraron daño** tras trasplantarlos con nefrectomía contralateral inmediata. Óvulos de ratón: 80 % del control llegó a blastocisto, frente a 30 % con la mejor solución previa.
- La familia M22 sale de ese principio de diseño (usada en el riñón de conejo, F5).

**Línea forzada:**
- **La tensión entre CCR baja y toxicidad no es una ley física dura: es un problema de diseño de mezcla con una variable conocida (qv*)**, más la temperatura de carga (perfundir a −3 °C y no a 0–4 °C) y la neutralización cruzada entre componentes.
- **Pendiente numérica (C8):** entre la clase de 8.4 M (CCR 2.5–5.4) y M22 (CCR 0.1), añadir ~1 M baja la CCR ~36 veces. La composición pesa tanto como la molaridad (VS55 y VMP tienen la misma molaridad y CCR que difieren ×2).
- **D_CPA queda definida operativamente:** D_CPA = ∫ f(qv*) · g(T) · C(t) dt, con el marcador **K⁺/Na⁺ en loncha** como ensayo estándar [P: fuente clásica, no releída]. **Sin umbral numérico universal** ⇒ se mantiene la tensión (R1).

---

## Correcciones y consolidaciones
- **Q2 queda cerrada con números:** 5 min legales frente a 17 min del organismo con reperfusión óptima frente a ≥ 4 h de la célula.
- **Q1:** τ_eq,org ∈ [5, 17] min (con la medicina actual y la mejor reperfusión) · τ_eq,cel ≥ 240 min.
- **Tabla de vías:** el sobreenfriamiento pasa a escala de órgano humano (riñón de cerdo e hígado de cerdo, 1–2 días). La congelación parcial se queda en rata (10 días).
- **Q18, nueva predicción falsable:** *un órgano del tamaño humano conservado por congelación parcial con nucleación controlada, o de forma isocórica, superará 5 días con función de trasplante antes de que ningún órgano humano vitrificado funcione tras trasplante.* Motivo: C6 no tiene barrera física y C3 sí.
