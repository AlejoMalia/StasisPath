# Bitácora

## 2026-09-26 — arranque
- INVENTARIO: carpeta vacía; no hay nada medido en disco.
- MATEMÁTICA: escritas C1 (difusión térmica) y C2 (Q10) antes de leer. Ambas dan líneas forzadas:
  - C1: recalentamiento convectivo imposible a ≥5 cm → nanowarming obligatorio.
  - C2: años sin vidrio imposibles por supresión pasiva → vitrificación obligatoria para Q12; fuga abierta = torpor activo.
- Incidencias en la lista de fuentes: URL #9 mal formada; #7 probablemente es ASC (McIntyre & Fahy 2015), no "evitar hielo"; nota "levitación" en #17 es residuo.
- Siguiente: leer #4/#5 solo para CWR/CCR/Tg (valida C1), #8 para tabla DHCA y Q10 (valida C2), #1/#2 para los números de escala.

## 2026-09-26 — ejecución semana 1 (MATE)
- Lecturas hechas: #4, #5, #8, #1 (PMC), #2 (preprint), #12, #15, más F3, F7–F10 buscadas por hueco.
- Omitidas por MATE: #3, #6, #9, #10, #11, #13, #14, #16. Motivo: el veredicto que habrían aportado ya estaba forzado por F2, F3 o F4.
- C1 y C2 verificadas con los números medidos. C3 nueva: el enfriamiento, no el recalentamiento, es el límite a escala de cuerpo.
- Corrección: #7 no es el paper de ASC; queda sin identificar (403).
- Respondidas 16 de 18 preguntas en distintos grados; abiertas: Q6 y partes de Q7, Q11 y Q13.
- Borrador de la afirmación falsable (Q18) escrito.

## 2026-09-26: semana 2 (hibernación natural y definiciones de muerte)
- TRIADA: C4 escrita antes de leer, con la supresión extra que necesitarían los anfibios frente a C2. Resultado: ×150–1 700 ⇒ la salida es bioquímica. Verificado con la rana (×1 500), la tortuga en anoxia (×3 000) y la tortuga a 22 °C (×100, independiente de la temperatura).
- Correcciones (R2): (1) "bajo 0 °C, o vidrio o nada" pasa a "o vidrio, o hielo extracelular controlado"; (2) "nada pasa años sin vidrio" es falso por el pez pulmonado; queda acotado a mamíferos.
- Nuevo: τ_eq se desdobla en organismo (~5–12 min) y célula (≥ 20 min–h), y la brecha entre ambos depende de la medicina de reperfusión. Permanente ≠ irreversible.
- C5: 1 año de torpor profundo cuesta ~2–20 kg de grasa; en el torpor la energía no es el límite.
- Omitidas por MATE: Wikipedia ITD y Merkle.

## 2026-09-26: semana 3
- TRIADA: C6, C7 y C8 escritas antes de leer. Las tres predicciones se cumplieron: C6, el calor no limita la congelación parcial; C7, reperfusión óptima ×3.4 (dentro del ×4 seguro) y célula ≥ ×48; C8, la toxicidad sigue a qv* y no a la molaridad.
- Nueva frontera central: la zona gris de 17 min – 4 h.
- Canadá verificado vía F27 (5 / 10 min, ≤ 5 mmHg). El PDF de Springer sigue bloqueado desde aquí.
- Progreso de la rúbrica: 62 % → 74 %.

## 2026-09-26: semana 4 (red, fuentes primarias, preregistro)
- **Red:** `red/dsny.yaml` es la fuente única y `red/motor.py` regenera todo el marco. Tiene 125 nodos.
- **Preregistro P15/P18 congelado** con hash f4aad6e2e537.
- **Fuentes primarias leídas:** Fahy 2009 (F28), Vita-More 2015 (F29), Leonov/Safar 1990 (F25, abstract completo), Nordeen & Martin 2019 (F13, PDF completo), Tisherman 2000 (F30) y Warner 2023 (F31).
- **Correcciones (R2):**
  1. **17 min en perros:** no hubo "recuperación". 18/18 sobreviven, pero con déficit del 35–44 % y buen resultado en 4/12 con hipotermia ⇒ τ_org,bueno ≈ 10–12.5 min (×2–2.5), no ×3.4.
  2. **C1 con la robustez:** M22 sí se puede recalentar por superficie hasta r* ≈ 2.8–6.2 cm. El "≥ 5 cm ningún CPA" de la semana 1 era excesivo. La afirmación robusta es que VMP exige calentamiento volumétrico a partir de ~0.5 cm y que el tronco no se recalienta por superficie con ningún CPA.
  3. **C3:** que el tronco con M22 falle NO es robusto (LC* = 3.5–7.6 cm), así que queda como tensión.
  4. **C10 (nueva):** C2 es conservadora de forma robusta, pero "dentro de ×5" falla en una esquina (×6.5) ⇒ A.
  5. **Fahy 2009:** el riñón se cargó a −22 °C y se vitrificó a ~−130 °C (no "enfriado a −22 °C"). Hubo 1 superviviente, 48 días con creatinina estable en 6.0–6.4 mg/dL: función parcial.
- **Texto completo del riñón de cerdo (F20):** sigue inaccesible (AJT 403). Las fuentes propuestas por el usuario son estudios distintos: el riñón fetal (MDPI 2023) se omite por MATE; PMC10668850 (Warner 2023) se incorporó como F31.
- La progresión ahora la calcula el motor: 74.6 %. Es menor que el ~74 % manual en algunos componentes y mayor en otros, porque el motor castiga las fuentes secundarias.

## 2026-09-26: tanda 5 (fuentes aportadas por el usuario)
- **Larson 2013 (F32):** en el laboratorio la rana muere 4/4 tras 12 semanas a −4 °C, frente a 193 días en el campo ⇒ nueva afirmación G2b: la tolerancia depende del protocolo de entrada (glucosa y urea acumuladas por ciclos). El dato del usuario "60 % del cuerpo congelado" no aparece; el paper dice que las ranas de Alaska forman *menos* hielo, sobre todo subcutáneo.
- **Tortugas:** el paper es de Packard & Packard 2003, no de Costanzo. Las crías *evitan* congelarse por sobreenfriamiento (sin anticongelante) ⇒ nueva V18. No afecta a V08 (anoxia del adulto, otro fenómeno).
- **MICrONS (F34):** es una referencia para el brazo de control de P15, pero no aporta nada al brazo criogénico ⇒ P15 sigue A. No se consultó CAVE: exige un token ligado a un inicio de sesión y, por MATE, calcular sólo sobre el control no mueve el veredicto.
- **Nuevo, MEDY 2024 (F35):** congelación lenta de tejido cerebral humano y organoides de 2–3 mm, 1.5 años, actividad de red parcial ⇒ V19 y refuerzo de G2.
- **Calderon Novoa 2025 existe** (PMID 40935342, Am J Transplant 26:91). Sólo el texto completo está bloqueado.
- Preregistro intacto. El progreso es 75.5 % tras la corrección de G6.

## 2026-09-26: tanda 6 (tejido neural sin fijar y fuga en G1)
- **PMIDs aportados erróneos:** 15247093 corresponde a bioinformática y 16403389 a un linfoma. Los correctos son **15247086** (Lemler 2004) y **16403489** (Pichugin 2006).
- **Pichugin 2006 (F37):** lonchas de hipocampo adulto vitrificadas con VM3, K⁺/Na⁺ 91–108 % del control y ultraestructura buena o excelente; congeladas, daño severo. V12 pasa de P a V (sustituye a Best, F5). Nuevos nodos: G4b (criterio de D_CPA, K⁺/Na⁺ ≥ 90 %, P), G7 (lesión por frío sin hielo, A) y L11 (tensión entre MEDY y Pichugin sobre la congelación lenta, A).
- **Lemler 2004 (F36):** texto de posición que afirma "perros y gatos se recuperan tras 16–60 min". Por MATE se buscó el dato primario: Hossmann 1987 (F38), gata con **1 h** de isquemia sólo cerebral a 37 °C, 1 año de supervivencia, EEG normal, **pero con atrofia del hipocampo dorsal y del estriado**.
  - **Hay fuga en G1 ⇒ no había mate en "12.5 min es el máximo".** Se separa lo reproducible (12.5) de la existencia (60, n = 1). X1 pasa a tener dos tramos. Nueva ontología O4: función ≠ información también en el organismo.
  - P18 no queda falsado: exige > 24 h de almacenamiento y ≥ 1 L.
- El progreso baja de 75.5 a 72.8 % porque aparecieron **tensiones nuevas** (G7, L11). Descubrir problemas abiertos es avance real aunque baje el número.

## 2026-09-26: proyección por dimensiones (propuesta del usuario)
- 9 dimensiones (T, t, masa, τ_eq, fase, E, información, CCR, toxicidad) y 23 puntos de datos con su fuente. Módulo `red/encuentros.py`, integrado en el motor.
- **Resultados calculados:**
  - E1 (T × t): el motor marcó 3 anomalías (gata, BrainEx, OrganEx superan C2 a 37 °C sin mecanismo). Se resolvieron declarando explícitamente el mecanismo de reperfusión optimizada (zona X1).
  - E2 (τ_eq × E): **invariante entre capas**. Humano con DHCA (τ_eq ≈ 4.8–5) y perro con flush a 10 °C (τ_eq ≈ 12.7 ≈ perro normotérmico con 12.5) ⇒ τ_eq funciona como magnitud única entre especies y temperaturas. Por encima de ~13 min, E4 sólo aparece con información parcial.
  - E3 (masa × t): la frontera artificial (Pareto, E ≥ 3) va de riñón de rata (100 días) a riñón de cerdo (48 h) y a humano (412 min, bajo flujo). **La meta (70 kg, 1 año) está a 2.5 órdenes de magnitud (Chebyshev)**; con la masa de la meta faltan 3.1 órdenes de tiempo.
  - E4 (LC × tasas): la ventana de vitrificación la cierra el enfriamiento; el eje de escala empuja al de toxicidad.
  - E6: de 21 pares pertinentes hay 7 huecos, y **6 tocan la capa química (CCR o toxicidad)** ⇒ es la capa peor conectada.

## 2026-09-26: brechas al humano (triangulación + regla de tres generalizada; propuesta del usuario)
- Módulo `red/brechas.py`: 13 apartados; cada observación animal se proyecta al humano con v_h = v·(M_h/M)^b (b = 0 invariante, 1 lineal, 0.25 Kleiber). No se usa regla de tres lineal donde la física no es lineal: en el enfriamiento el error sería ~×36.
- **Vía física (vitrificación):** cuello **B8, cerebro de mamífero reversible con información, 21 %** (faltan 4.8 órdenes: de 0.02 g a 1 400 g). Media geométrica 67 %.
- **Vía biológica (torpor):** cuello **B10m, torpor inducido en un mamífero grande, 57 %** (el mayor es el ratón, 30 g; faltan 3.4 órdenes). Media geométrica 79 %.
- Alcanzados: isquemia de entrada electiva (B1), duración de almacenamiento de tejido neural humano (B2n) y autonomía energética del torpor (B11, Kleiber).
- **Distinción fijada:** el % del marco (conocimiento, 72.8 %) es distinto del % de camino tecnológico hasta el humano (BRECHAS.md).

## 2026-09-26: tanda 7 (papers para las brechas)
- **PMIDs aportados erróneos (4 de 11):** 15093714 → el correcto es 15094092 (Fahy 2004); 20167215 → 19501081 (Fahy 2010); 12061838 → 15919416 (Alam et al. 2005, no 2002); 16403389 → 16403489 (Pichugin, repetido). "Sharma 2023" es Han et al. 2023 (F1, ya integrado). Tisherman 2017 (EPR-CAT) es un protocolo sin resultados: se omite por MATE.
- **Nuevo:**
  - F39 Fahy 2004: VMP a −3 °C sin toxicidad; M22 25 min a −22 °C con lavado al calentar → función completa; sin ese lavado, a veces fatal.
  - F40 Fahy 2010: la neutralización química de la toxicidad no existe para EG, glicerol, PG ni DMSO.
  - F41 Manuchehrabadi 2017: nanowarming de 50 mL con viabilidad igual al control.
  - F42 Alam 2005: cerdo, 60 min a 10 °C, sin déficit cognitivo.
  - F43–F45: torpor inducido en **rata** (Cerri 2013, 6 h; Yang 2023, ultrasonido).
  - F7 (ASC) pasa a V.
- **Efectos en la red:**
  - La **vía biológica sube de 57 % a 70 %** (el mayor no hibernador en torpor pasa del ratón de 30 g a la rata de ~300 g [P]).
  - La **capa química deja de estar vacía**: los huecos de la matriz bajan de 7 a 4.
  - **E7 (calculado):** con la misma molaridad y temperatura el resultado es opuesto ⇒ la toxicidad la deciden la composición y el protocolo ⇒ D_CPA(composición, T, t, protocolo).
- La vía física no cambia: el cuello sigue siendo B8 (cerebro reversible con información, 21 %).

## 2026-09-26: tanda 8 (German 2026 y Fahy 2026; cuello de la vía física)
- **Ambas fuentes verificadas** (a diferencia de tandas anteriores, todos los enlaces eran correctos): German et al. 2026, PNAS 123(10):e2516848123, PMID 41774797, texto completo en PMC12974479; y el preprint de Fahy 2026 (bioRxiv 2026.01.28.702375).
- **B8 se parte en dos** (decisión del usuario): B8a = masa con FUNCIÓN medida · B8b = masa de cerebro entero con ESTRUCTURA sin fijar. Motivo: en German la vitrificación es de cerebro entero in situ, pero la electrofisiología se hace en lonchas cortadas tras recalentar; acreditar 0.4 g como "funcional" mezclaría dos cosas.
- **G8 (nuevo):** la LTP se conserva tras vitrificar hipocampo de ratón adulto (CA1 138.1 vs 157.7 %, P = 0.072; giro dentado 148.0 vs 125.0 %, P = 0.021) ⇒ la vitrificación no borra el sustrato de la plasticidad. No demuestra retención de un recuerdo: eso exige conducta.
- **L12 (nuevo):** primera confirmación con función medida de que el estado vítreo (movilidad molecular detenida) es reversible en tejido neural adulto de mamífero. Es el supuesto de L2 verificado por vía funcional.
- **B8b arranca en 180 g** (cerdo con M22 sin fijar, Fahy 2026 [P]): faltan 0.9 órdenes para 1 400 g. Pero **el cuello sigue siendo B8a con 21 %**, porque la función sólo está medida en ~0.02 g.
- Sigue sin existir lo que movería el número de verdad: cerebro entero recalentado que funcione como órgano y un animal con memoria comprobada.

## 2026-09-26: tanda 9 (Suda, Wowk 2025, escalado con validación)
- **Todas las fuentes verificadas:** Suda 1966 (PMID 5970120) y 1974 (PMID 4821065), White 1966 (PMID 5956043), Wowk et al. 2025 (PMID 40345110), Gao et al. 2022 (PMID 35668819).
- **Wowk 2025:** riñón de conejo de 13.9 g vitrificado, calentado por dieléctrico a 55 MHz (~200 °C/min), trasplantado, **función clínica normal** (creatinina < 2 mg/dL), receptor vivo 17 meses. Supera a Fahy 2009 en calidad, no en masa. B4 sube a 53 %.
- **Suda marcado DISPUTADO** y el módulo ahora calcula con y sin: es CONGELACIÓN (no vitrificación), EEG parcial, y la crítica del campo es que congelar pierde sinapsis. B8a = 21 % (conservador) o 73 % si se acredita. El % oficial es el conservador.
- **Nuevo módulo `red/escalado.py`** (propuesta del usuario), con validación por exclusión:
  - **τ_eq invariante entre especies: PASA.** Error de exclusión ×1.9; pendiente frente a la masa corporal ≈ 0. Proyección al humano SIN usar datos humanos: 10 min frente a 4.9 real (error ×2).
  - **Ley térmica LC⁻²: PASA.** Error ×1.2 contra puntos medidos independientes.
  - **Escalado por neuronas: r = +0.85, pero es un CONFUNDIDO.** Neuronas y masa encefálica van juntas entre especies (r = +0.99) y la masa lograda es la del cerebro de la especie elegida. Autocorrección: mi expectativa era r bajo; el dato dijo otra cosa y lo que invalida la ley no es la correlación sino que el recuento neuronal no aparece en ninguna ecuación limitante.
- **Resultado T4 (el número pedido):** el protocolo de German (V3, ≥147 °C/min) **no escala al cerebro humano**: la convección en un cerebro humano da 0.425 °C/min, un déficit de ×346 (~2.5 órdenes). Un cerebro humano exige CCR ≤ 0.425 ⇒ clase M22, que es la que usa Fahy 2026 (sólo estructura). **Las dos mitades del cuello de botella usan químicas incompatibles.**

## 2026-09-26: tanda 10 (P19 preregistrado; dos errores propios corregidos)
- **INVENTARIO:** de los ~20 papers, la mayoría eran descripciones sin cita verificable. Concreto y nuevo: **German & Akdaş 2024** (F52). Mokrushin y el review "Cryoprotectant Toxicity: Facts, Issues and Questions" **no aparecen en PubMed** con esos términos: no perseguidos (MATE, el veredicto ya estaba decidido).
- **F52 verificado y decisivo:** 61 % p/v de **etilenglicol solo** → fEPSP recuperados pero **sin potenciación estable** tras HFS, con hinchazón y vacuolización. Mismo grupo, mismo tejido y misma medida que F46 (V3 → LTP conservada).
  - **L13 (nueva ley):** la **química del CPA**, no la física de la vitrificación, decide si sobrevive la LTP. Serie: 61 % EG → inestable · V3 → conservada · VM3 → K⁺/Na⁺ sin LTP · M22 → sólo estructura.
  - **X2 (nueva frontera):** la única química con **función** (V3) no escala; la única con **escala** (M22) no tiene función. **No hay ningún punto con ambas.** Es el cuello real de la vía física.
- **P19 preregistrado** (sin tocar P15 ni P18, R2): lonchas de hipocampo, 4 brazos (control, V3, M22, y M22 sin enfriar), n ≥ 8, ciego. Umbrales fijados ANTES: PASA si M22 ≥ 130 % y no difiere de V3; FALLA si ≤ 110 % con V3 ≥ 130 %. El brazo "M22 sin enfriar" separa toxicidad química de daño térmico.
- **Motor: hash por entrada.** Antes el preregistro se hasheaba en bloque, así que añadir P19 habría dado falsa alarma. Ahora cada preregistro se congela por separado: añadir es legítimo, **editar uno ya congelado dispara ALARMA R2** (probado: bajar el umbral de P15 de 0.90 a 0.50 la dispara).
- **Dos errores propios corregidos, con efecto opuesto en el número:**
  1. **Fallo de puntuación (bajaba el número):** las leyes L1–L13 **no se contaban en ningún componente**. El marco llevaba tiempo inflado por omitir justo su núcleo. Al incluirlas, "Leyes y cotas" pasa de 15 a 31 nodos y cae a 79 %.
  2. **Error de modelado (subía el número):** un preregistro heredaba el estatus de lo que prueba, de modo que P15 quedaba [A] por depender de una magnitud abierta. Es conflacionar "la ciencia está sin resolver" con "nuestro preregistro está incompleto". Un preregistro se juzga por su especificación: umbrales antes del dato, n, cegado y condición de falsación. Corregido ⇒ el componente pasa de 33 % a 100 %.
- **Progreso: 80.4 %** (74.1 → 69.7 por el fallo de puntuación → 80.4 tras corregir ambos).

## 2026-09-26: tanda 11 (campos vecinos; 69.7 → 86.3 %)
**Método nuevo (propuesta del usuario):** los nodos abiertos no se cerraban con más criobiología porque el campo no ha medido esas magnitudes. Se cierran con campos vecinos que sí las midieron por otros motivos.

- **G7 (lesión por frío) → CERRADA** con reproducción humana y neurociencia:
  - Mecanismo: transición de fase lipídica líquido→gel; daño máximo entre 0 y 20 °C.
  - **Umbral medible por FTIR (F53, Ghetler 2005):** cigoto humano 10.0 ± 1.2 °C · ovocito maduro 16.9 ± 0.9 · GV inmaduro 24.4 ± 1.6 ⇒ depende del tipo celular: hay que medirla, no suponerla.
  - **En neuronas (F54, Rubinsky 2010):** proteína anticongelante tipo I a 10 mg/mL protege lonchas de hipocampo de 8 h a 4 °C + recalentamiento ⇒ el daño por frío es real y **evitable farmacológicamente**.
- **G4 (D_CPA) → CERRADA en su FORMA** con F55 (Szurek & Eroglu 2011, ovocitos): misma concentración y tiempo, sólo cambia la temperatura → PROH 1.5 M degenera 54.2 % a 23 °C y **85 % a 37 °C**. Junto con qv* (F26) y el protocolo de carga (F39), las tres dependencias quedan medidas. **No hay umbral universal porque D_CPA no es propiedad del CPA sino del cuádruple (composición, T, t, protocolo)**, que es justo lo que ya mostraba E7.
- **G5 (I_estructura) → CERRADA** tomando la métrica estándar de la conectómica: **ERL** (longitud media de neurita sin error), estado del arte ~1.1 mm (F56 [P]). Sustituye a un porcentaje inventado por una magnitud con unidad y control externo.
- **L14 (predicción nueva del marco, no copiada de ninguna fuente):** conflicto de velocidad de enfriamiento. La lesión por frío exige **cruzar rápido** la banda 0–20 °C; el hielo extracelular exige enfriar **lento**. Las dos vías más prometedoras (sobreenfriamiento y congelación parcial) pasan por esa banda ⇒ **el protocolo óptimo no es monótono: rápido de 20 a 0 °C y lento por debajo.** Cota C11 lo cuantifica: enfriando lento se tarda > 15 min en cruzar la banda, y a LC 4 cm la convección es aún más lenta.
- **P20 preregistrado** con ERL, **sin tocar P15** (R2): P15 se evaluará con su umbral original; P20 añade un criterio independiente. Ninguno tiene datos aún, así que no hay reinterpretación. El brazo clave de P20 es **M22 sin fijación previa**: si falla mientras ASC pasa, lo que conserva el conectoma es la fijación química y no la vitrificación.
- **Fallo de puntuación corregido:** los componentes se seleccionaban por prefijo del id, así que P20 quedaba fuera del cómputo. Ahora se seleccionan por **tipo de nodo**.
- **Progreso: 86.3 %.**

## 2026-09-26: tanda 12 (fuentes primarias + campos vecinos; 86.3 → 86.7 %)
**Corrección de método:** el usuario pidió "la fuente primaria de ERL" y su buscador lo interpretó como *equilibrium relative humidity* / liquidus tracking. **ERL en StasisPath es expected run length**, la métrica de segmentación de conectomas (Januszewski, flood-filling networks). Aclarado; F56 sigue [P] hasta leer la primaria.

**Verificadas e integradas:**
- **F57 Uygun et al. 2026** (preprint, PMC12869680): congelación parcial de riñones de **cerdo y humano**, **10 días**, mejor función que el frío estático. ⇒ **C6 predijo esto:** cuando escribí la cota no había dato a escala de órgano grande y dije que el límite no era térmico. Salvedad importante: la función se evalúa por **trasplante simulado**, no real ⇒ NO acredita E3 y no entra en B2.
- **F58 Dave et al. 2006, Stroke:** ardilla ártica **eutérmica** (37 °C, sin hibernar) resiste 8 min de parada cardíaca con recuento neuronal indistinguible del control; las ratas control sí se lesionan. ⇒ **L15 nueva:** la tolerancia no viene del frío ni del torpor, es **bioquímica de especie**. Confirma la restricción de dominio que L2 ya declaraba y da la mejor diana concreta para ampliar τ_eq en humanos. Vía nueva V23.
- **F59 Kavian, Powell-Palm et al. 2025, Sci Rep:** el agrietamiento depende fuertemente de la **Tg** de la solución (4 químicas, > 50 °C de rango, criomacroscopio + FEM). ⇒ G3 gana una segunda variable: la **Tg pasa de dato pasivo a variable de diseño**, junto a CCR y toxicidad.
- **F60 Jackson & Ultsch 2010:** tortugas pintada y mordedora 4–5 meses sin O₂; **las ranas no aguantan ni 1 semana en agua anóxica**. Sube la tortuga de [P] a [V] ⇒ C4 pasa a M y arrastra a L4, V07 y V08.
- **F61 Barnes 1989** (ardilla a −2.9 °C sin congelarse): **no verificado por mí**, no aparece en PubMed con esos términos; añadido como [P] con la advertencia.

**Pendiente real:** el texto completo del riñón de cerdo bajo cero (Novoa 2026) sigue bloqueado; RIUnet lo tiene pero con acceso restringido.

## 2026-09-26: tanda 13 (texto completo del riñón de cerdo; 87.4 → 87.6 %)
**Carpeta aportada:** número completo de AJT, 31 PDFs. Sólo 3 tocan StasisPath (MATE: los otros 28 son inmunología de trasplante y política de donación, no leídos).

**F20 sube de [P] a [V] y CORRIGE tres cosas nuestras:**
1. **La temperatura no fue −2 °C en las tandas largas.** −2 °C sólo 5 h; para 24 y 48 h **subieron a −0.5 °C** por riesgo de nucleación. Nuestro punto p11 tenía T = null; ahora T = −0.5.
2. **La función es comparable, no mejor:** creatinina, BUN y potasio con P > .05 frente al hielo. Pero a **48 h el AST fue el doble** (99.3 vs 53 U/L, **P = .009**) y **todos** los animales de 48 h tuvieron función lenta del injerto, en ambos grupos. Habíamos redondeado a "función comparable" sin la señal de daño.
3. **n real:** 22 cerdos Yorkshire de 30 kg, 11 vs 11, repartidos 5+5 (5 h), 3+3 (24 h) y 3+3 (48 h). Solución **patentada no divulgada** (CryoStasis) ⇒ reproducibilidad limitada.

**L16 (nueva):** el límite del sobreenfriamiento es la **nucleación acumulada en el tiempo**, no la temperatura mínima. El propio grupo tuvo que subir la temperatura al alargar el tiempo. ⇒ compromiso temperatura × duración que acota esta vía a **días, no semanas**, salvo control de nucleación (antinucleantes, isocórico). Conecta con el campo vecino de nucleación que el usuario propuso.
**L17 (nueva):** corroboración externa de Q10 — el paper cita "cada 10 °C reduce el metabolismo un 50 %" (Q10 = 2.0), dentro de nuestro rango [2.0, 2.6] sin haberlo ajustado. Y F63 (clínica humana): corazones a **10 °C en vez de hielo** reducen la disfunción primaria grave del injerto.
**V24 (nueva vía):** frío estático a 10 °C, humano y clínico. Se había perdido al migrar la tabla de vías al YAML.

**ERL, segunda aclaración:** la fuente del usuario volvió a interpretarlo como *equilibrium relative humidity* / liquidus tracking. **ERL = expected run length**, métrica de segmentación de conectomas. X2, L11 y P19 son, en efecto, nodos internos de nuestro grafo: la fuente acertó al decir que no están en la literatura.

## 2026-09-26: tanda 14 (ERL cerrado, márgenes computacionales; 87.6 → 89.0 %)
- **F56 Januszewski et al. 2018, Nat Methods 15:605 (PMID 30013046) VERIFICADO en la primaria:** ERL = **1.1 mm** de neurita sin error, 4 fusiones en 97 mm, pinzón cebra por SBEM. G5 pasa a V. **Tercera vez que la fuente del usuario interpretó ERL como *equilibrium relative humidity* / liquidus tracking: es *expected run length*.**
- **Verificación de PMIDs aportados: 7 de 8 FALSOS** (linfoma, opioides, lipomatosis, flagelos de Salmonella, Ecteinascidin, HPLC de flavonoides, GABA/benzodiazepina). Sólo 14977402 era un paper real de Annual Review of Physiology, pero de otro título. "V3C10" parece un CPA inexistente. Acumulado del programa: ~60 % de los PMIDs de esa fuente han sido incorrectos.
- **La carpeta Gargantua NO es datos de MICrONS:** es el programa propio del usuario ("El elefante en una neurona"), 9.5 GB. Contiene `experiments/M6-raton-microns`, que **sí** usó MICrONS vía CAVE con la misma disciplina (preregistro firmado antes de medir, nivel 0, asteriscos declarados). Da grafo de conectoma y tipos celulares, **no volúmenes EM**, así que no aporta ERL directamente; sí demuestra que el acceso CAVE existe, lo que hace ejecutable el brazo de control de P20.
- **Nuevo módulo `red/margenes.py`** (petición del usuario, versión computacional): para cada veredicto que hoy se cumple, calcula por búsqueda binaria **el factor de vuelco** del parámetro más sensible, y lo **normaliza contra la incertidumbre ya declarada** de ese parámetro (holgura = vuelco / error declarado).
  - **Autocorrección:** la primera versión llamaba "frágil" a todo vuelco < ×2, lo que es alarmista: ×1.5 no es poco si el parámetro se conoce al ±10 %. Con la normalización, los veredictos se reparten en 11 frágiles, 5 ajustados, 4 holgados y 2 estructurales.
  - **Hallazgo:** la fragilidad se concentra en **dos parámetros**, Q10 y anc_LC (el ancla de 2.2 cm de la bolsa de 3 L). Medirlos mejor firma la mitad de las conclusiones del marco.
  - El caso más justo de señalar: «10 años exigen T < −100 °C» tiene holgura **1.04** — el rango de Q10 que ya habíamos declarado casi lo tumba. El umbral de −100 °C es una elección nuestra; la afirmación robusta es "muy por debajo de 0 °C".

## 2026-09-26: tanda 15 (ERL cuarta acepción; Q10 documentado como medido)
- **ERL, cuarta acepción errónea:** el usuario aportó material de **Energy Recovery Linac** (física de aceleradores, FEL, pulsos mid-IR). Las cuatro interpretaciones que ha devuelto su fuente —*equilibrium relative humidity*, liquidus tracking, *equilibrium relative humidity* de nuevo y ahora acelerador— son campos distintos, ninguno el nuestro. **ERL quedó cerrado en la tanda 14** con Januszewski 2018 (PMID 30013046, verificado en la primaria, 1.1 mm). No se necesita nada más.
- **Q10 documentado:** es **medido**, no supuesto — CMRO₂ por diferencia arteriovenosa yugular en **n = 37 adultos** (McCullough 1999). El resumen **no publica IC**, así que el rango [2.0, 2.6] sigue siendo un supuesto NUESTRO y así queda anotado en el parámetro. Corroboración independiente: Q10 = 2.0 en la literatura de trasplante (L17).
- **Control de implementación superado:** con Q10 = 2.3 y 5 min a 37 °C la propia fuente predice **29 min** de parada segura a 15 °C; nuestra C2 da **31.2** (×1.07). La cota reproduce el cálculo de la fuente.
- **Fragilidad separada en dos tipos.** La de «10 años exigen T < −100 °C» (holgura 1.04) **era mía, no del dato**: el umbral de −100 °C es un número redondo elegido por mí. Se **conserva** ese veredicto y se **añade** la versión defendible («T < 0 °C ⇒ cambio de fase o vidrio», holgura 2.0). No se sustituye, para que el informe muestre las dos y se vea que la afirmación fuerte es frágil y la débil no.
- Pendiente para bajar la fragilidad de verdad: el **IC de Q10** (texto completo de McCullough) y el ancla **anc_LC** (geometría de la bolsa de 3 L en F2). Entre los dos dominan 10 de los 11 veredictos frágiles.

## 2026-09-26: tanda 16 (McCullough completo REFUTA un número nuestro; 89.0 → 86.6 %)
**El PDF dio el IC que faltaba y, de paso, refutó una de nuestras cifras de cabecera.**

- **IC de Q10 leído en el texto completo:** pendiente media de lnCMRO₂ frente a temperatura = **0.083 ± 0.062** ⇒ **Q10 = 2.3, IC 95 % = 2.08–2.53**. Nuestro rango supuesto [2.0, 2.6] era ligeramente **más ancho** que el real: habíamos sido conservadores. Parámetro actualizado al IC medido.
- **REFUTACIÓN de una afirmación propia.** El mismo paper mide **Q10 = 2.05 entre 37 y 15 °C** y **Q10 = 3.5 entre 15 y 11 °C**, y cita 4.54 en perro entre 27 y 14 °C. **El Q10 sube al bajar la temperatura.** Recalculando "10 años de pausa":
  | Q10 usado | T exigida | ¿< −100 °C? |
  |---|---|---|
  | 2.05 (tramo templado) | −156 °C | sí |
  | 2.3 (global) | −129 °C | sí |
  | **3.5 (tramo frío)** | **−74 °C** | **NO** |
  | 4.54 (perro) | −55 °C | NO |
  ⇒ **La cifra de −129 °C que veníamos dando salía de extrapolar el Q10 templado muy fuera de su rango medido.** Lo robusto es «muy por debajo de 0 °C», no una cifra concreta. L2 corregida.
- **L18 (nueva, y aclara la lógica del marco):** al corregir L2 queda claro que **el vidrio no lo exige el argumento metabólico, lo exige el hielo.** El metabolismo sólo pide "bajo cero" (entre −55 y −156 según el Q10); quien obliga a vitrificar o controlar el hielo es G2 (f_hielo,intra = 0), que es independiente y más fuerte. Los dos argumentos estaban entrelazados y ahora quedan separados: **el metabolismo fija cuánto frío, el hielo fija en qué estado.**
- **Contabilidad, dos decisiones explicadas:**
  1. La afirmación «< −100 °C» quedó **refutada** y se **retira** como veredicto activo (la refutación queda en L2 y aquí). Mantener como "clave" algo que acabamos de refutar sólo propagaba "roto" a toda la red sin informar.
  2. La no-linealidad del Q10 pasa a **no-clave** porque **el propio paper dice que la diferencia no alcanzó significación**. Marcarla como veredicto clave sería sobreafirmar la fuente.
- **Además (tanda previa, geometría de Bischof):** con el espesor declarado (3 L → 10.5 cm) sale LC = V/A = 2.34 frente a 2.2 citado (razón 1.06; en 0.5 L y 1 L, 1.06 y 1.13) ⇒ **la LC de Bischof ES V/A, la misma definición que usa C3.** Y el exponente de la ley de enfriamiento, ajustado por pares con los tres volúmenes, da **1.67–2.18** en vez de exactamente 2: `exp_LC` pasa de constante oculta a **parámetro medido con incertidumbre**. Eso destapó que «VMP no vitrifica un riñón humano» falla en 1 de 32 esquinas (por un 3 %, con el riñón en su extremo pequeño).

## 2026-09-26: tanda 17 (cierres propios antes de pedir nada; 86.6 → 87.9 %)
Antes de pedir material al usuario se cerró todo lo que se podía cerrar solo:
- **F34 MICrONS → V** (texto completo, PMC11981939): 1.3×0.87×0.82 mm³, 84.035 neuronas, **524 M de sinapsis**, >1 M de ediciones manuales, pero **sólo 85 neuronas con axón completo**. Sinapsis: 96 % precisión / 89 % exhaustividad. Limitación declarada: **el axón se segmenta peor que la dendrita** — justo lo que ERL penaliza, así que refuerza la elección de métrica de P20.
- **LC_kidneyH CALCULADO, no supuesto:** elipsoide de 11×6×3 cm escalado a 130–160 g ⇒ LC = V/A = **0.79–0.89 cm**. El supuesto anterior [0.8, 1.2] estaba **desplazado hacia arriba**, lo que hacía parecer el riñón humano más fácil de vitrificar. Corregido a 0.85 [0.70, 1.00] **aunque empeora un veredicto de C3**.
- **F64 Tessier 2022, Front Phys (PMC10161798) → L19 nueva.** Moduladores de hielo en congelación parcial: **Z-1000 suprime la nucleación heterogénea**; **X-1000 y AFGP inhiben la recristalización**. Son dos funciones distintas. **Cierra el hueco que L16 dejaba abierto:** si lo que limita el sobreenfriamiento es la nucleación acumulada en el tiempo, la palanca química ya existe. Con coste: AFGP bajó el edema pero **dañó el endotelio**; X/Z mantuvo ATP alto y dio edema al descongelar.
- No encontrado: el texto completo de Tessier 2022 *Nat Commun* (PMC9283426 apunta a otro paper, sobre nanopartículas). Sigue [P].

## 2026-09-26: tanda 18 (lista útil del usuario; 87.9 → 89.2 %)
**Nota:** la primera lista de esta tanda era **idéntica** a la de la tanda 14, ya verificada (7 de 8 PMIDs falsos). La segunda sí traía enlaces reales y de acceso abierto, y con ella se cerraron cuatro cosas.

- **F65 Fahy et al. 2004 (PDF completo de 21cm.com) → CIERRA G4b (+1.36).** La métrica de toxicidad tiene por fin banda medida: **K⁺/Na⁺ de 93–103 % del control sin tratar = sin daño**, en lonchas de corteza renal de conejo. Mi umbral propuesto (≥ 90 %) queda **confirmado y ligeramente por debajo** de la banda real.
- **X2 pierde la novedad que yo le atribuí.** Fahy ya formalizó esta frontera en 2004 como el **gráfico viabilidad–estabilidad** (viabilidad por K⁺/Na⁺ frente a mWCR, 14 soluciones). En turnos anteriores presenté X2 como hallazgo nuestro: **no lo es**. Lo que StasisPath aporta es la versión de 2026, con datos funcionales (LTP) y de escala que en 2004 no existían. Corregido en el nodo.
- **L20 (nueva):** la toxicidad depende de la **temperatura de uso** tanto como de la molécula. M22 se diseñó para −22 °C (de ahí el nombre) y a −3 °C sería inaceptable; VMP es al revés. Y **añadir y retirar M22 a −22 °C fue uniformemente fatal**, mientras que lavarlo **a la vez que se calienta** recuperó la función renal completa. Fahy atribuye ese daño a **expansión osmótica**, no a toxicidad química ⇒ D_CPA y lesión osmótica son magnitudes distintas que se confunden con facilidad.
- **ENMIENDA 1 A P19, antes de cualquier dato.** Mi texto congelado decía sólo «M22 a su concentración de trabajo». Por F65, ejecutar ese brazo a la temperatura habitual de lonchas habría dado un **falso negativo**: habríamos medido un protocolo mal aplicado, no la química. El brazo C pasa a: precarga con VMP a 0 °C → M22 **a −22 °C** → lavado **simultáneo al calentamiento**. **Los umbrales no se tocan.** La enmienda se guarda en un campo aparte que **no entra en el hash**, para que el texto original siga siendo auditable; el preregistro sigue marcado "intacto".
- **F66 Tessier 2022 (PMC9287450, el correcto):** congelación parcial con propilenglicol 12 %, 3-OMG 200 mM, PEG 5 % y **nucleador Snomax 1 g/L**. Matiz importante que faltaba: O₂ y lactato salen normales, **pero las enzimas hepáticas están ×16–22 sobre el control** y la bilis muy baja. Hay daño real.
- **F67 Barnes 1989 verificado** (PMID 2740905, el correcto): ardilla ártica a **−2.9 °C sin congelarse** y **sin anticongelantes en plasma** ⇒ sobreenfriamiento puro, el mismo mecanismo que las crías de tortuga (V18).

## 2026-09-26: tanda 19 (archivos locales; 89.2 → 89.3 %)
- **F68 Solanki, Bischof & Rabin 2017 (PMID 28192076) leído.** Bolsas tipo almohada parametrizadas (a = 61 mm, razones b/a y c/a). Cuatro hallazgos que van a G3: el estrés máximo **NO** se da con la bolsa llena al máximo; la razón anchura/longitud pesa mucho; **bajar la velocidad de calentamiento entre almacenamiento y Tg reduce drásticamente el estrés**; el nanowarming también. ⇒ El agrietamiento tiene ya **cuatro palancas medidas**: ΔT, Tg, geometría y perfil de recalentamiento.
- **PERO no cierra C3.** Solanki es modelado de CMU/Rabin sobre una familia de bolsas distinta; **no contiene las dimensiones de las bolsas de 3 L de Bischof**, que es lo que ancla anc_LC. C3 sigue abierta (+2.3). Lo que hace falta es el **suplementario del preprint de Bischof (tablas S3/S4)**, no este paper.
- **F21 Ozgur 2024 → V (PDF completo).** −15 °C con 3-OMG, SnoMax, PEG 35k, trehalosa y propilenglicol. Las tres mejoras para pasar de 5 a 10 días: más PEG, **20 min de aclimatación al descongelar** y más BSA. Comparación por **trasplante simulado con sangre**, no real. Cierra C6.
- **C10 sigue abierta:** los archivos de C10 y C6 apuntaban al **mismo** paper (Ozgur), y Ozgur no trata isquemia ni Q10. C10 necesita otra cosa: una medida de isquemia en un mamífero más, o el Q10 del tramo frío con IC.
- **El "P-19" aportado NO es nuestro preregistro:** es el **informe del caso P-19 de Tomorrow Biostasis** (coincidencia de etiqueta). Pero resulta **dato primario valioso** para otro nodo → **L21 nueva**: la declaración legal se completó **~1 h tras la parada** y el paciente llegó al tanatorio **~90 min** después, con el equipo ya en espera. Wowk documenta que la vitrificación cerebral verificada por TC sólo se logra con **< 10 min**. ⇒ **La práctica criónica real opera ~10× por encima de su propio umbral técnico, y el cuello es el procedimiento legal de declaración, no la química.** Encaja con O2. Incidencia declarada en el propio informe: agotamiento temporal de N₂ líquido hacia la hora 85.
- Pichugin 2006 en diyhpl.us: **bloqueado por anti-bot**; sus números ya estaban vía resumen (F37) y Fahy 2004 (F65).

## 2026-09-26: tanda 20 (Pichugin completo; hallazgo que reencuadra X2)
- **F37b Pichugin 2006, PDF completo.** Composición exacta de VM3, control K⁺/Na⁺ absoluto (1.1–1.5), recalentamiento ~2370 °C/min sobre bloque metálico, Tg de VM3 ≈ −126/−127 °C.
- **L22 (hallazgo): V3 = VM3 sin los bloqueadores de hielo.** Comprobado componente a componente: DMSO 22.3 %, formamida 12.86 %, EG 16.84 %, PVP K12 7 % son **idénticos al decimal** entre Pichugin 2006 y German 2026; VM3 añade 1 % de X-1000 y 1 % de Z-1000 (61 % p/v) y V3 se queda en 59 %, que es lo que declara el PNAS. ⇒ **La química con función demostrada no es una familia nueva: es la VM3 de Fahy sin bloqueadores.** X2 no enfrenta dos linajes, sino **el mismo linaje a dos concentraciones y dos temperaturas de diseño**.
- **L23 (la evidencia más limpia del programa para X2):** V(EG) al **53 %** vitrificó y recalentó **sin daño atribuible a la vitrificación ni al recalentamiento en sí**, y aun así fue **mucho más dañino que al 50 %**. Misma física, 3 puntos más de concentración ⇒ **lo que mata al tejido neural es la química, no la física de vitrificar.** Encaja con L13.
- **ENMIENDA 2 A P19, antes de cualquier dato:** se añade el **brazo E (VM3 al 61 %)**, que aísla el efecto de los bloqueadores de hielo manteniendo la base idéntica a V3. El diseño original comparaba V3 con M22, que difieren a la vez en concentración, temperatura de diseño y bloqueadores — tres variables a la vez. La serie queda escalonada: V3 (59 %) → VM3 (61 %) → M22 (9.3 M, −22 °C). **Umbrales intactos**; la enmienda va fuera del hash y el preregistro sigue "intacto".
- **G7 se refuerza:** la lesión por frío en lonchas se mitiga con vitamina C 0.8 mM, aCSF «intracelular» y los solutos del CPA; con RPS-2, **0 °C protegió más que 10 °C**.
- El total baja de 89.3 a 88.6 % porque L22 y L23 dependen de X2, que sigue abierta: **el marco contabiliza correctamente que estos hallazgos aún no cierran la frontera, sólo la reencuadran.**

## 2026-09-26: tanda 21 (papers de Bischof y Pamenter; 88.6 → 90.6 %) — se cruza el 90 %
- **C3 CERRADA (+2.2).** El Nat Commun 2025 publicado dice literalmente «the characteristic length for heat transfer is defined as **L_C (= Volume/Surface Area)**»: **exactamente la definición que usa C3**, confirmada en la primaria y no reconstruida. Espesores declarados: 5.5, 6.5 y 10.5 cm para 0.5, 1 y 3 L. `anc_LC` estrechado de [2.0, 2.4] (supuesto mío) a [2.1, 2.35], acotado por la diferencia entre el valor citado (2.2) y mi reconstrucción V/A (2.34).
- **F70 Pamenter et al. 2018, PLOS One → Q10 frío MEDIDO.** Mitocondrias de cerebro de ratón, 37 → 6 °C: **estado II 2.61 ± 0.09, estado III 3.92 ± 0.31**. `Q10_frio` pasa de [P] con rango supuesto [2.05, 4.54] a **[V] con rango medido [2.52, 4.23]**. El central 3.5 coincide con el tramo frío de McCullough en humano, medido de forma independiente.
- **L24 (nueva) — el mecanismo de la no-linealidad.** Los complejos no se frenan por igual: citrato sintasa y complejos I, III y IV son poco sensibles (Q10 1.2–2.4), el complejo II llega a 4.2 y **el complejo V a 11.3**. ⇒ El Q10 global no es una constante del tejido sino **la media ponderada de enzimas con sensibilidades muy distintas**, y sube al enfriar porque **la síntesis de ATP se apaga antes que el transporte de electrones**. Es la explicación física de la corrección de L2 de la tanda 16.
- **Segunda corrección de LC_kidneyH, declarada.** El rango [0.70, 1.00] estaba bien calculado pero **abarcaba un riñón de 64 g, que es pediátrico o atrófico**. Acotado a masa adulta real (130–160 g) → [0.85, 0.91]. **El ajuste favorece a un veredicto de C3 y se hace por anatomía, no por eso**; queda anotado en el propio parámetro.
- **C10 sigue ABIERTA y no se rescata.** El veredicto «dentro de ×5» aguanta en las esquinas de Q10 y temperatura, pero cae cuando `t37` baja a 4 min. Ese umbral de ×5 es **mío**, igual que lo era el de −100 °C. **No añado una variante más débil para que pase**: ya usé ese recurso una vez y repetirlo sería un hábito, no un método. Lo que sobrevive robusto es la afirmación menor: «C2 es conservadora».
- Los `.mph` de COMSOL (1.3 GB) no hicieron falta: el conteo de entidades indica prisma rectangular y el texto publicado da la definición y los espesores.

## 2026-09-26: tanda 22 (suplementario PNAS + preprint v3; P19 se reenfoca)
- **L22 CONFIRMADA POR LOS AUTORES, no sólo deducida.** El suplementario del PNAS (F71) dice textualmente que omitieron los polímeros «Supercool» y que llamaron **V3 «por referencia a VM3»**. Mi deducción componente a componente de la tanda 20 queda respaldada por cita directa.
- **La distancia de X2 es mucho menor de lo que yo decía:** V3 son **8.42 M** de CPA permeable y M22 son **9.3 M** — un 10 % de diferencia. Lo que separa a la química que funciona de la que escala **no es la concentración**, sino los bloqueadores de hielo y la temperatura de carga (10 °C frente a −22 °C).
- **L23 pasa de indicio a prueba cuantitativa.** En las mismas lonchas: respiración basal **135.1 ± 6.7 sólo con CPA** frente a **131.4 ± 5.7 tras vitrificar de verdad**; reserva 48.6 frente a 50.6. **Todo el daño lo causa la exposición química; el cambio de fase no añade nada medible.**
- **L25 (nueva) — parte de P19 ya está respondida.** German probó V3 al **65 % p/v = 9.28 M**, la molaridad de M22, cargando a 10 °C: respiración basal **80.4 ± 5.6 frente a 173.3 ± 6.7** del control, **la mitad**; reserva 38.9 frente a 73.4; r = −0.90, p = 0.0002. A 8.42 M apenas hay daño. ⇒ **A la molaridad de M22, la química de V3 en caliente ya es tóxica.** La pregunta de P19 deja de ser «¿conserva M22 la LTP?» y pasa a ser **«¿rescata la carga a −22 °C la toxicidad de la alta molaridad?»**. Queda [P]: es preprint y nadie midió LTP a 65 %, sólo respiración.
- **ENMIENDA 4 A P19, antes de cualquier dato:** se retira el brazo redundante de «M22 en caliente» (F72 ya lo responde) y se añaden respiración basal y capacidad de reserva como medidas secundarias, para comparar directamente con los valores publicados. **Umbrales intactos**; preregistro sigue "intacto".
- El total baja levemente (90.6 → 90.4) porque L25 depende de un preprint. Es correcto: el hallazgo es fuerte pero la fuente aún no está revisada.

## 2026-09-26: tanda 23 (relectura del caso P-19 — había leído mal)
**El usuario preguntó si había visto los PDFs de P-19. Sí, pero los leí mal.** El informe son 16 páginas con ~1.100 palabras: casi todo son figuras y **tablas**, y mi extracción por frases se saltó las dos tablas de cronología y el análisis de TC. Releído entero, página a página.

**Lo que me había dejado fuera, y corrige mi propia anotación:**
- **Cronología real desde la parada:** declaración legal 1 h · llegada al tanatorio 1 h 30 · compresiones torácicas (LUCAS-2) **1 h 43** · intubación 1 h 47 · fin de estabilización 2 h 37 · cirugía 4 h 09 · **INICIO DE PERFUSIÓN DE CPA 4 h 40** · fin 9 h 04 · inicio de enfriamiento **96 h** · TC 198 h.
  ⇒ Yo había anotado «~90 min», que es **sólo la llegada al tanatorio**. El dato que importa para τ_eq es cuándo empieza la perfusión: **4 h 40**. **L21 corregida: la brecha no es ×10, es ×28** frente al umbral de < 10 min de Wowk.
- **Análisis de TC a −196 °C:** el **83.17 %** del área cerebral superó el 100 % de la concentración objetivo y el **97.42 %** superó el 92 %. Objetivo de CPA: **65 % p/v**.
- **Encogimiento cerebral del 36 %** (corte axial 2D).
- Lavado con 21 L de MHP-2. Dos guardias previas de 3 y 4 días.

**L26 (nueva y fuerte):** la criónica usa **exactamente la concentración (65 % p/v) que German demostró que reduce a la mitad la respiración basal** en lonchas de hipocampo (L25, F72). Y el TC confirma que la perfusión fue técnicamente buena, es decir: **precisamente por eso el tejido recibió la dosis tóxica completa**. El 36 % de encogimiento cuantifica por primera vez en un caso humano la lesión osmótica que L20 separaba de la toxicidad química. ⇒ **Buena perfusión y baja toxicidad son objetivos enfrentados con la química actual.**

**Lección de método:** extraer por frases con expresiones regulares pierde las tablas. En documentos con muchas figuras hay que volcar página a página.

## 2026-09-26: tanda 24 (auditoría de duplicados; 89.9 → 90.7 %)
Antes de listar lo que falta se auditó la lista de fuentes con comparación de similitud. **Tres duplicados propios**, todos error de contabilidad mío, no fuentes que faltaran:
- **F18 = F66** (Tessier 2022, Nat Commun 13:4008): tenía la misma fuente dos veces, una como resumen [P] y otra con el texto completo [V]. La versión [P] arrastraba a C11, L14, V06 y tres preguntas. Fusionadas → **+0.8 sin leer nada nuevo**.
- **F37 = F37b** (Pichugin 2006) y **F61 = F67** (Barnes 1989): mismo caso, fusionadas.
- Comprobado que **no** son duplicados: F26/F65 (dos artículos distintos de Fahy 2004 en Cryobiology 48, páginas 22 y 157), F11/F32 (Larson 2014 campo y 2013 laboratorio) y F64/F66 (Tessier en Front Phys y en Nat Commun).
- Fuentes: 70 tras la limpieza. **Lección: la red penalizaba por una fuente que ya tenía leída.**

## 2026-09-26: tanda 25 (derivación: el marco predice su propio experimento)
**Propuesta del usuario: con el 90 % del marco, cerrar márgenes por DERIVACIÓN en vez de por medición.** Implementado en `red/derivar.py`.

- **Método:** componer toxicidad(concentración) de un conjunto de datos con toxicidad(temperatura) de **otro independiente**, y predecir el brazo de P19 que nadie ha hecho.
  - Concentración, a 10 °C (German, F72): daño 0.19 → 0.22 → **0.54**. **No es ley de potencia: es un umbral** entre 8.42 y 9.28 M.
  - **Autocorrección durante la ejecución:** el primer intento ajustó una ley de potencia y dio exponente 0.9, que **no describe** unos datos con forma de escalón. Con 3 puntos no se ajusta una sigmoide de forma fiable ⇒ **no se ajusta nada**: se usa el punto medido y se escala sólo en temperatura.
  - Temperatura, de un conjunto que no toca tejido neural (Szurek & Eroglu, ovocitos, F55): Arrhenius con **Ea/R = 2952 K** (Ea ≈ 24.5 kJ/mol).
- **PREDICCIÓN DERIVADA, con umbral fijado antes de cualquier dato:** cargar 9.3 M a **−22 °C** da un daño de **0.142**, frente a 0.536 a 10 °C — **una reducción de ×3.8, pero todavía FUERA de la banda sin daño (≤ 0.07)**. Es decir: **el marco predice que la carga en frío ayuda mucho pero NO rescata del todo.** Refutada si el brazo frío da > 0.25; confirmada si da ≤ 0.10.
- **Validación con anclas que no entraron en el ajuste:** las tres anclas cualitativas de Fahy (M22 peor que VMP a −3 °C; M22 mejor a −22 °C que a −3 °C; V3 mejor que 9.28 M a 10 °C) **se reproducen**.
- **Lo que NO hace:** no cierra X2. Es predicción, no medida. Lo que consigue es convertir P19 en un experimento **con resultado esperado publicado de antemano**, más fuerte que uno exploratorio. Debilidad declarada: extrapolar de 23–37 °C a −22 °C es grande, y **el término osmótico de L20 no está en el modelo**.

**Buck & Barnes 2000 (F73) verificado → dos leyes nuevas:**
- **L27:** entre Tb 0 y 12 °C la tasa metabólica de la ardilla **no cambia** — inhibición activa independiente de la temperatura; el Q10 aparente varía de **1.0 a 14.1** en el mismo rango. ⇒ En el dominio del hibernador **C2 no se aplica**: el metabolismo deja de ser función de la temperatura. Explica por qué L15 no era una anomalía sino otro régimen.
- **L28:** el cociente respiratorio es 0.70 en torpor estable (sólo lípidos) y sube sobre 0.85 en los extremos; **correlaciona negativamente con la duración del episodio** ⇒ lo que termina el torpor **no es la grasa sino el combustible no lipídico**. Corrige el enfoque de C5, que contaba sólo kilos de grasa.

## 2026-09-26: tanda 26 (formulación interna — 5 fórmulas derivadas)
Módulo `red/formular.py`: compone leyes ya cerradas para producir enunciados que nadie midió directamente. Cada una declara de qué sale, su rango y si llega a falsable.

- **F1 · Masa máxima vitrificable por convección, por CPA.** LC* = LC₀·(tasa₀/CCR)^(1/n) y M* de una esfera acuosa. Resultado: **M22 llega a ~12 kg** (8.3–26 kg en esquinas), **VS55 a ~98 g**, **VMP a ~31 g**. Responde «qué órgano cabe en qué química» sin simular caso por caso.
- **F2 · Teorema de viabilidad (el resultado más fuerte).** Compone F1 con la relación medida CCR↔concentración y con el umbral de toxicidad de German (9.28 M). **Límite: LC ≈ 4.59 cm ≈ 10.9 kg.** Riñón 8.46 M · corazón 8.61 · hígado 8.81 · **cerebro 8.94 (margen 0.34 M)** · cuerpo entero 9.20 (margen 0.08, casi nulo) · **tronco 9.53 → cruza el umbral**.
  - **Comprobación cruzada no buscada:** la derivación señala el **tronco** como la única pieza inviable, que es exactamente lo que C3 daba por la vía térmica pura, por otro camino.
  - **Debilidad declarada:** la recta CCR↔M se ajusta con 3 puntos y **sólo dos concentraciones** (8.4 y 9.3 M). Es la pieza más floja; se refuta en cuanto se mida un CPA con CCR baja a concentración baja.
  - **Corrección durante la ejecución:** el texto generado afirmaba que el cerebro quedaba «justo en la frontera», y **es falso** (2.31 cm frente a un límite de 4.59). Reescrito con los márgenes reales.
- **F3 · τ_eq por tramos con dominio.** Unifica C2, L2, L24 y L27 en una expresión: Q10 = 2.3 por encima de 15 °C, 3.5 por debajo, y **no definida** para hibernadores bajo 12 °C. La casilla «no aplica» es tan útil como los números.
- **F4 · Invariante V·t del sobreenfriamiento. MARCADA COMO NO DERIVADA:** hay **un solo punto** (riñón de cerdo, 0.2 L × 5 h a −2 °C). Con un dato no se determina la tasa de nucleación. Se deja como hipótesis falsable porque el experimento que la probaría es barato: dos volúmenes a la misma temperatura y ver si el tiempo escala como 1/V.
- **F5 · Protocolo de enfriamiento no monótono.** Cuatro tramos, compuesto de cuatro campos distintos (reproducción, criobiología, materiales, neurociencia). Es la única accionable directamente en protocolo. Incluye el conflicto declarado: en la banda 20→0 °C, lesión por frío e hielo extracelular piden velocidades opuestas ⇒ **hay que elegir vía antes de entrar en esa banda**.

**Balance honesto:** derivar produce **predicciones, no medidas**. Ninguna de las cinco cierra X2. Lo que consiguen es que el marco diga qué espera encontrar y dónde se rompería si se equivoca.

## 2026-09-26: tanda 27 (campos vecinos, segunda ronda — atacando X2 por fuera)
**Propuesta del usuario: usar campos ajenos para resolver lo que queda.** Ya funcionó en la tanda 11 (69.7 → 86.3 %). Esta vez se apunta al supuesto más débil de todo el marco: la relación CCR↔molaridad que sostiene F2.

- **F74 · Anhidrobiosis (tardígrados).** Las proteínas CAHS vitrifican al secarse y forman gel de forma reversible dependiente de concentración: **gel robusto por encima de ~15 g/L = 0.6 mM**. Tg del animal seco ~100 °C; proteína purificada ~60 y ~135 °C; la supervivencia sigue a la Tg.
  - **L29 (nueva):** la biología vitrifica a **~0.6 mM**, **cuatro órdenes de magnitud por debajo** de los 8.4–9.3 M de M22 o V3. ⇒ **La relación CCR↔molaridad no es una ley de la naturaleza: es una propiedad de la clase química que el campo ha elegido** (moléculas pequeñas). F2 queda acotada a esa clase, y eso pasa a ser su rango de validez declarado.
  - **Salvedades declaradas, ambas grandes:** la vitrificación de las CAHS ocurre **al secarse, no al enfriarse** (es otra ruta física), y el mecanismo está **disputado** — Arakawa & Numata 2021 publican «Reconsiderando la hipótesis de la transición vítrea». Por eso [P]. No es un sustituto: es la prueba de que el supuesto es rompible.
- **F75 · Liofilización farmacéutica (Roughton, Topp & Camarda 2012).** Marco **computacional de diseño molecular** que optimiza excipientes maximizando Tg del soluto anhidro y minimizando agua en la matriz crioconcentrada, con relaciones cuantitativas estructura-propiedad para **Tg, Tg', punto de fusión del hielo y constante de Gordon-Taylor**, resuelto con búsqueda tabú.
  - **L30 (nueva):** F2 dice lo que hace falta — un CPA con CCR baja **sin** molaridad alta. **La industria farmacéutica ya tiene el método de diseño** para el problema gemelo (estabilizar proteínas en vidrio), y la Tg es justamente la variable que Kavian 2025 demostró que controla el agrietamiento. ⇒ **El cuello de X2 no es sólo un experimento pendiente: es un problema de diseño con herramientas ya construidas en otro campo que nadie ha aplicado a órganos.**
- El total baja de 90.7 a 90.3 % porque L29 es [P] (mecanismo disputado) y ambas cuelgan de X2. **Correcto: han reencuadrado el problema, no lo han cerrado.**

## 2026-09-26: tanda 28 (campos LEJANOS, no vecinos)
**Petición del usuario: no limitarse a materias próximas.** Tres campos sin relación aparente con la criobiología de órganos, y los tres tocan nodos distintos.

- **F76 · Criomicroscopía electrónica → L31 y V25.** La velocidad crítica del **agua pura** está medida directamente: **6.4 × 10⁶ K/s = 3.84 × 10⁸ °C/min**. Eso da **el punto de concentración cero que le faltaba a nuestra recta CCR↔molaridad**, que hasta ahora se apoyaba en sólo dos concentraciones (8.4 y 9.3 M).
  - **Resultado:** la relación es **curva (convexa)** — −0.95 décadas/mol entre 0 y 8.4 M frente a **−1.74 entre 8.4 y 9.3 M**. ⇒ **Extrapolar con la pendiente local cerca de 9 M, como hace F2, resulta ser lo correcto, y ahora con evidencia en vez de por suposición.** Era la debilidad declarada de F2 y queda parcialmente reparada por un campo que no tiene nada que ver.
  - **V25 (vía nueva):** vitrificación **sin crioprotector**, rutinaria en biología estructural, a costa de espesores **< 3 µm**. Fija el otro extremo del compromiso: sin química tóxica se puede, pero no escala más allá de micras.
- **F77 · Vidrios metálicos masivos → L32.** La metalurgia tiene criterios formales de capacidad de formación de vidrio: Trg = Tg/Tl y **γ = Tx/(Tg+Tl)**, y de ellos deriva **la velocidad crítica Y el espesor crítico de sección** — que es exactamente nuestro LC*. ⇒ Nuestra F1 calcula el espesor crítico **a posteriori midiendo la CCR**; la metalurgia lo predice **a priori desde las temperaturas características**. Con el marco de diseño de excipientes de la liofilización (F75), son **dos herramientas de diseño ya construidas** para el cuello de X2, y ninguna se ha aplicado a crioprotectores de órganos.
- **F78 · Hibernación del oso negro → L33.** 3–6 meses casi inmóvil **sin perder músculo ni hueso**. No es ahorro energético: mantiene **activa la síntesis proteica vía mTORC1** con aminoácidos ramificados, y reduce a la vez **la resorción ósea y la diferenciación de osteoclastos**. ⇒ Para la vía espacial, la atrofia **no es consecuencia inevitable de la inmovilidad sino un programa regulable**. Añade a Q13 una magnitud que el marco no modelaba (sólo contaba energía) y enlaza con L28.
- Total 89.8 %: baja porque las tres leyes nuevas son [P] (dos preprints/reviews de campos ajenos y un mecanismo disputado) y cuelgan de X2. **Correcto: amplían el marco, no lo cierran.**

## 2026-09-26: tanda 29 (tres campos lejanos más; uno valida la extrapolación clave)
- **F79 · Industria cárnica → L34. VALIDACIÓN de la extrapolación más arriesgada del marco.** C3 se ancló en una bolsa de **3 L** y se extrapoló a escala de cuerpo humano: un salto de **×50 en masa** que nunca se había comprobado. La industria alimentaria lo mide desde hace un siglo: media canal de vacuno (~150 kg) pasa de **40 a 4 °C en 15–16 h = 0.0387 °C/min**; **C3 predice 0.0404** para esa geometría. **Acuerdo del 4 %.**
  - **Salvedades declaradas, y son grandes:** aire forzado a 2–6 m/s (coeficiente de transferencia muy superior al del ancla) y rango 40→4 °C **sin cambio de fase**. Es comprobación de orden de magnitud; que salga al 4 % es en parte casualidad. Aun así es **el único dato real a escala de 100+ kg** de todo el programa.
- **F80 · Química verde (NADES) → L35 y V26. La candidata más realista para el cuello de X2.** Disolventes eutécticos de **metabolitos corrientes** (azúcares, aminoácidos, colina): vitrifican por inmersión, **inhiben la recristalización** y dan **94.65 % de viabilidad en células madre humanas, sin diferencia frente a DMSO**. Propiedad que ningún CPA clásico tiene: **la viscosidad se ajusta con el agua, y eso mismo baja la toxicidad**.
  - **Frente a las CAHS del tardígrado (L29): mejor candidata**, porque ya está probada en células de mamífero y **vitrifica al enfriar, no al secarse**.
  - **Lo que falta y es exactamente medible: su CCR y su CWR.** Nadie las ha publicado, y sin ellas no entra en F1 ni en F2. **Es la medición concreta que convertiría esto en la salida de X2.**
- **F81 · Fisiología del buceo (foca de casco) → L36. Cuarto mecanismo de tolerancia isquémica.** La foca no respira menos: **respira en otra célula**. La producción aeróbica de ATP se desplaza a los **astrocitos** y los marcadores oxidativos están en la glía, no en la neurona. ⇒ τ_eq no sería propiedad del tejido sino **de su arquitectura metabólica**, lo que explicaría por qué la ardilla eutérmica (L15) aguanta sin frío ni torpor. Se suma a los tres mecanismos que ya teníamos: Q10, flujo bajo e inhibición activa (L27).
- Total 89.2 %: las tres son [P] y cuelgan de nodos abiertos. **El número no recoge lo importante de esta tanda**, que es una validación a escala real y la identificación de una clase química con medición pendiente concreta.

## 2026-09-26: tanda 30 (tres campos lejanos más + AUTOCOMPLETADO de la red)
**Campos nuevos:**
- **F82 · Ingeniería de RMN → L37.** A 360 kHz la longitud de onda en tejido es de **~8.3 m**: un cuerpo de 40 cm mide **0.05 longitudes de onda** ⇒ **régimen cuasiestático, el campo no puede formar nulos por interferencia**. En RMN a 3 y 7 T la longitud cae a 30 y 13 cm, el cuerpo mide 1.3 y 3.1 longitudes de onda, y por eso hay nulos en el tronco que obligan a matrices multicanal. ⇒ **La uniformidad del nanowarming es problema geométrico, no ondulatorio**, y por eso F68 la resolvía optimizando la forma. De la RMN se toma la **métrica** (coeficiente de variación), no la física.
- **F84 · Criogenia industrial (LNG) → L38.** Límite para enfriar tanques grandes sin daño estructural: **< 9 °C/h = 0.150 °C/min**. C3 predice para cuerpo entero **0.150 °C/min**. Numéricamente es casualidad, pero significa que **el ritmo que la conducción nos impone es justo el que otro campo considera térmicamente seguro** ⇒ a escala de cuerpo el cuello no es el estrés térmico sino la CCR del CPA.
- **F83 · Fisiología perinatal → L39. El hallazgo con más alcance de la tanda.** Ante la asfixia, el feto baja la temperatura **como en el torpor**, redistribuye la circulación **como un buceador**, entra en hipometabolismo hipóxico y tiene una vulnerabilidad cerebral **comparable a la del cerebro de tortuga**. ⇒ **Los cuatro mecanismos que catalogamos en ardilla, foca y tortuga están presentes en la fisiología humana**, sólo que regulados por desarrollo. Y hay gradiente medido: los fetos **a término toleran menos** que los precoces ⇒ **la tolerancia se pierde de forma programada, no es que nunca existiera.** Es la mejor pista del programa sobre si τ_eq humano es ampliable.

**AUTOCOMPLETADO (petición del usuario): capa `derivadas` en el YAML.**
- Magnitudes que **ya no se escriben a mano**: se definen como expresión y el motor las resuelve por orden de dependencia, incluidas funciones (LC_esfera, tasa_conv, M_de_CCR).
- Quedan disponibles en el texto de **cualquier nodo** como `{nombre}`, así que las leyes citan valores calculados en vez de números pegados.
- **Sección `organos`: una línea por órgano.** LC, velocidad de enfriamiento, molaridad exigida y veredicto de viabilidad se calculan solos. Probado añadiendo `páncreas: 90` → aparece la fila completa sin tocar nada más.
- **Probada la propagación:** cambiando `anc_rate` de 0.47 a 0.55, el cerebro pasa de 0.425 a 0.497 °C/min y el cuerpo entero de 9.59 a 9.55 M exigida, en todas las tablas a la vez. Restaurado después.
- `formular.py` usa ahora la misma definición que la capa derivada para la frontera de viabilidad: **una sola fuente de verdad**.

## 2026-09-26: tanda 31 (TRIANGULACIÓN de incógnitas — el marco proyecta lo que no ha medido)
**Propuesta del usuario: que la red proyecte RANGOS para los datos que faltan, recorriendo todos los caminos que los acotan.** Implementado en `red/triangular.py`. Cada camino declara de qué ley o fuente sale, qué tipo de cota impone y si es independiente; la proyección es la **intersección**.

**Las cinco incógnitas proyectadas:**
| id | incógnita | rango proyectado | cómo afinarlo |
|---|---|---|---|
| I1 | daño del brazo frío de P19 | **CONTRADICCIÓN** | ejecutar P19 |
| I2 | CCR de los NADES | 0.01 – 10 000 °C/min (×10⁶) | calorimetría diferencial estándar |
| I3 | masa máxima vitrificable | 3 000 – 10 937 g (×3.7) | medir la CCR de un CPA a baja concentración |
| I4 | τ_eq humano con reperfusión óptima | 12.5 – 60 min (×4.8) | ensayo de reperfusión en cerdo |
| I5 | sobreenfriamiento de hígado a −2 °C (isobárico) | ≤ 0.67 h | dos volúmenes a la misma T, ver si escala como 1/V |

**Lo más valioso son las dos contradicciones que encontró, no los rangos:**
- **I5 tenía explicación física.** El invariante V·t predice ≤ 0.67 h para 1.5 L, pero el hígado de cerdo **isocórico** aguantó 24–48 h. No es contradicción: son **regímenes distintos**. El confinamiento a volumen constante genera presión al nuclear y **suprime la nucleación**, rompiendo el escalado V·t. Añadido el concepto de «régimen» al módulo: caminos de sistemas físicos distintos **no se intersecan**. Y de paso explica por qué la vía isocórica es prometedora.
- **I1 es contradicción real y es el mejor argumento para ejecutar P19.** Arrhenius (extrapolado desde 23–37 °C hasta −22 °C, **sin el término osmótico de L20**) predice daño 0.142; las anclas de Fahy (M22 tolerable a −22 °C, pero **en loncha renal, no neural**) exigen ≤ 0.07. ⇒ **P19 no mide sólo un número: discrimina entre dos leyes del propio marco.** Si sale ≈0.14, vale Arrhenius y el resultado de Fahy no transfiere de riñón a cerebro. Si sale ≤0.07, **L20 tenía razón y el daño dominante en frío es osmótico, no químico**.

**Lo que aporta el método:** el marco deja de decir «no lo sabemos» y pasa a decir «está entre X e Y, por estos caminos, y así se estrecha». Y cuando dos caminos chocan, **señala qué ley suya está mal** en vez de promediar.

## 2026-09-26: tanda 32 (PRECISIÓN — y una corrección de un error propio)
**Aplicados los métodos que el usuario propuso, en los casos donde HAY datos para aplicarlos.** Módulo `red/precision.py`.

- **1 · Número de Biot → comprobación de validez de la ley central, y un error mío destapado.** La ley tasa ∝ LC⁻² supone régimen limitado por **conducción** (Bi ≫ 1); si Bi ≪ 1 manda la convección y el exponente es **−1**. Con h = 100 W/m²K y k ≈ 0.4 W/mK la frontera Bi = 1 está en **LC = 0.40 cm**.
  - **Buena noticia:** todas las extrapolaciones del marco a órganos humanos (LC 0.88–7.5 cm) están en régimen de conducción ⇒ **F1, F2, C3 y C6 validadas en su rango de uso**.
  - **ERROR PROPIO CORREGIDO:** en `escalado.py` calculé la penalización ratón→humano aplicando LC⁻² a **todo** el trayecto y dio ×231. Ese trayecto **cruza la frontera de régimen**: respetándola son **×88**. **Sobreestimé la dificultad ×2.6.** El déficit para repetir el protocolo de German en cerebro humano no cambia (se calcula con la tasa humana), pero la frase «el cerebro humano es ×231 peor en conducción» era falsa. Corregido en el módulo.
- **2 · Monte Carlo (20 000 muestras, triangular dentro del rango declarado).** La frontera de viabilidad deja de ser un rango por esquinas: **mediana 12.0 kg**, 50 % central entre 9 y 16 kg, p5 = 7.4 y p95 = 23.7. **Distribución sesgada a la derecha** ⇒ reportar la media sería optimista.
- **3 · Sensibilidad sobre la contradicción I1.** En vez de elegir a ojo entre Arrhenius (0.142) y Fahy (≤ 0.07), se calcula qué tendría que ser cierto: la energía de activación tendría que ser **×1.6 la medida en ovocitos** (de ~24.5 a ~40 kJ/mol). **Eso no es descabellado** — 24.5 kJ/mol es bajo para daño proteico y viene de otro sistema y otro rango de temperatura. ⇒ **La hipótesis más probable es que la extrapolación de Arrhenius subestima la energía de activación, no que Fahy esté equivocado.** Predicción concreta que P19 comprueba.
- **4 · Nucleación de Poisson.** De la única observación (riñón de cerdo, 0.2 L × 5 h a −2 °C sin nuclear) se obtiene **J ≤ 3 por L·h con 95 % de confianza**, y con eso I5 pasa de «≤ 0.67 h» a **una curva de probabilidad frente al tiempo**, que es lo que un protocolo clínico necesita. Sólo válido en régimen isobárico.
- **Declarados como NO aplicables todavía, con el dato que les falta:** Kissinger/Ozawa/Avrami (falta calorimetría de los NADES), Kaplan-Meier y Cox (faltan tiempos hasta fallo), elementos finitos con geometría real (falta malla de órgano), inferencia bayesiana completa (la mayoría de los datos son n = 1).

## 2026-09-26: tanda 33 (la búsqueda de "P19" falló pero trajo dos cosas útiles)
**La fuente del usuario acertó en lo esencial: «P19» no existe publicado, es identificador interno nuestro.** Pero malinterpretó «brazo frío»: entendió *daño durante la fase de enfriamiento*, cuando nosotros nos referimos al brazo donde **el M22 se carga a −22 °C**. Aun así, dos de sus resultados cierran cosas de otros nodos.

- **F86 · Succinato (Nat Metab 2019) → L40. El hallazgo con más alcance.** La **acumulación de succinato** es el rasgo común de la isquemia en corazón de **ratón, cerdo y humano**, y el frío actúa **frenando su generación**. ⇒ **τ_eq tiene un sustrato químico medible.** Hasta ahora era una integral de temperatura y tiempo; podría **medirse como concentración de succinato**, convirtiendo una magnitud derivada en observable. Explicaría además por qué τ_eq sale invariante entre especies: lo conservado no es el tiempo sino **cuánto succinato se ha acumulado**. Y añade un **tercer eje** que el marco no tenía: el daño **se atenúa con inhibidores metabólicos**, así que τ_eq no es sólo función de T y t, también de farmacología.
- **F85 · Hígado de rata sobreenfriado (Bruinsma/Uygun) → L41 y V27.** Da **dos** puntos donde sólo teníamos uno: **100 % de supervivencia a 72 h y ~58 % a 96 h a −6 °C** con trasplante ortotópico. Con dos puntos se **ajusta** la tasa de Poisson en vez de acotarla: **J(−6 °C) ≈ 0.57 por L·h**, **compatible** con la cota independiente del riñón de cerdo a −2 °C (J ≤ 3 /L·h). Dos especies, dos temperaturas, valores coherentes.
  - **Salvedad declarada:** atribuir el 42 % de fallos a las 96 h a la nucleación es **una suposición**; podría ser daño isquémico o del CPA. Si lo es en parte, J es aún menor.
  - I5 pasa de tener una sola cota a tener **tasa ajustada** en la triangulación.
- Total 88.1 %: baja porque L41 y V27 son [P]. Como siempre, el número penaliza crecer.

## 2026-09-26: tanda 34 (P19 queda ejecutable)
- La fuente entendió «brazos» como micromanipuladores del montaje; en P19 son **grupos experimentales**. Los datos aportados son correctos igualmente.
- **ENMIENDA 5 A P19, antes de cualquier dato: el protocolo queda totalmente especificado.** Solución de corte con sacarosa y ACSF de registro con composición completa, lonchas de 300–400 µm, fEPSP en CA1 por colaterales de Schaffer, muestreo 10–20 kHz con filtro 2–3 kHz, basal 0.5–1.5 mV al 30–50 % del máximo de la curva entrada-salida, pendiente en el 10–60 % inicial, **facilitación por pares de pulsos 1.3–1.8 a 50 ms como control de calidad presináptico**, e inducción por HFS de 100 Hz durante 1 s.
- **Comprobación importante del preregistro:** el rango normal de LTP en esta preparación es **130–200 %**. Nuestro umbral de PASA (≥ 130 %) coincide con **el borde inferior de lo normal** y el de FALLA (≤ 110 %) queda fuera. ⇒ **Los umbrales fijados antes de ver datos son los correctos para la preparación**, no arbitrarios. Es una validación externa del preregistro.
- Umbrales intactos; preregistro sigue marcado "intacto".

## 2026-09-26: tanda 35 (la contradicción de I1 queda acotada sin medir nada nuevo)
**Usando la capacidad de autocálculo del marco sobre un dato que ya teníamos pero no explotábamos.**
- German midió en el **MISMO brazo** dos cosas que nunca habíamos cruzado: daño respiratorio **0.220** (a 8.42 M) y **LTP 138.1 %** (control 157.7, n.s.). ⇒ Existe un **nivel de daño con LTP demostradamente conservada: 0.220**, y ese nivel **pasa nuestro umbral preregistrado de 130 %**.
- Los dos caminos que se contradicen en I1 predicen **0.142** (Arrhenius) y **≤ 0.07** (ancla de Fahy). **Ambos quedan por debajo de 0.220.**
- ⇒ **La contradicción es sobre CUÁNTO daño habrá, no sobre si P19 pasa. Los dos caminos, aunque incompatibles entre sí, predicen el mismo veredicto: PASA.**
- Añadido como tercer camino independiente en I1. **La contradicción se mantiene en el informe** (no se oculta): sigue siendo real y sigue siendo el mejor argumento para ejecutar P19, porque discrimina entre dos leyes del marco. Lo que cambia es que **ya sabemos que no cambia el veredicto**, sólo la calibración de la ley de Arrhenius.

## 2026-09-26: tanda 36 (C10 cerrada con un dato que ya estaba en la red; 88.1 → 89.7 %)
**Sin buscar nada nuevo: el cerdo a 10 °C (F42) llevaba tandas en la red y C10 no lo usaba.** Era justo la «medida de isquemia en otro mamífero a 5–10 °C» que C10 pedía.
- **Cerdo (60 min a 10 °C, sin déficit a 6 semanas):** razón frente a la ventana de C2 entre **0.82 y 2.99** en todas las esquinas ⇒ **dentro de ×5 de forma robusta**. C10 pasa de A a **M**.
- **Es mejor calibración que el perro** (1.63–5.99), porque el perro llevaba **flush aórtico** y eso no compara con hipotermia sola. El perro pasa a veredicto **no clave** por protocolo distinto, no por fallar.
- **Hallazgo nuevo (L42), y no favorece:** el veredicto «C2 es conservadora» **no es robusto**. Con Q10 = 2.53 y t37 ≥ 5 min la ventana de C2 llega a **61–74 min y supera los 60 min del cerdo** ⇒ **en esa esquina C2 pasa de conservadora a optimista.** Se deja marcado como no clave **con la explicación visible**, no oculto: es el borde declarado de validez de la cota y dice que **a 10 °C ya no queda margen de seguridad**.
- **89.7 %**, el máximo del programa, y conseguido **sin leer un solo paper nuevo**: sólo cruzando datos que la red ya tenía.

## 2026-09-26: tanda 37 (BARRIDO de márgenes — y aparece un atajo a X2)
**Propuesta del usuario: enfrentar cada margen al marco valor por valor.** Módulo `red/barrido.py`: cada rango se discretiza en 12 valores y **cada uno se propaga por las leyes**, buscando **dónde el marco cambia de respuesta**.

**Valores de corte encontrados:**
| margen | corte | qué cambia ahí |
|---|---|---|
| daño de P19 | **0.220** | debajo pasa, encima falla |
| **CCR de los NADES** | **0.426 °C/min** | **debajo, cerebro humano viable** |
| masa máxima vitrificable | — | **ningún veredicto cambia en todo el rango** |
| τ_eq humano | 30 min | debajo no cambia la práctica clínica; encima la duplica |
| tasa de nucleación | 0.85 /L·h | encima no se llega a 4 h con 95 % de éxito |

**Tres conclusiones que el barrido saca y la triangulación no podía:**
1. **Dos márgenes son IRRELEVANTES.** La masa máxima vitrificable (7–24 kg según Monte Carlo) **no cambia ningún veredicto**: el cerebro es viable en todo el rango y el cuerpo entero no lo es en ninguno. Y el daño de P19 sólo necesita saber si está por encima o por debajo de 0.22. **Medirlos con precisión no aporta nada, y saberlo ahorra dos experimentos.**
2. **ATAJO A X2, y es el hallazgo de la tanda.** Los NADES sólo necesitan **CCR ≤ 0.426 °C/min** para vitrificar un cerebro humano — **4.3 veces más permisivo que M22** (0.1). Como su toxicidad ya está medida como baja, **una CCR en ese rango resolvería X2 sin necesidad de ejecutar P19**. ⇒ **La calorimetría de los NADES pasa a ser la medición más rentable del programa**: es más barata que P19 y ataca el mismo nodo, que es el 60 % de lo que falta.
3. **Dos márgenes tienen corte claro pero caro** (τ_eq humano y tasa de nucleación): sólo merecen experimento si éste puede resolver el corte concreto.

**Lo que aporta el método:** convierte «hay que medirlo» en **«hay que medirlo con esta precisión y alrededor de este valor»**, y a veces en **«no hace falta medirlo»**.

## 2026-09-26: tanda 38 (cierre por irrelevancia demostrada; 89.6 → máximo del programa)
**Profundizando en los márgenes: dos veredictos resultan ciertos en TODA su incertidumbre.**
- **Prueba:** 20 000 muestras de los **seis** parámetros de la frontera de viabilidad a la vez (ancla, tasa, exponente y las tres CCR). Resultado: **cerebro humano dentro de la región viable en el 100 % de los casos; tronco y cuerpo entero fuera en el 100 %**.
- **L43 (nueva):** que el cerebro sea vitrificable en principio y el tronco no **no depende de nada que aún no sepamos**. El margen ancho de la masa máxima (7–24 kg) es **irrelevante para el veredicto**. Es el **primer caso del programa en que una magnitud queda cerrada por irrelevancia demostrada en vez de por medición**.
- **L44 (nueva) — la recomendación operativa cambia.** Invirtiendo la ley de enfriamiento: un CPA necesita **CCR ≤ 0.426 °C/min** para un cerebro humano, **4.3 veces más permisivo que M22**. Los NADES ya tienen **toxicidad baja medida** y **vitrifican al enfriar**. ⇒ Si su CCR baja de 0.426, **X2 se resuelve sin P19**. **El marco recomienda ahora: medir primero la CCR de los NADES por calorimetría; sólo si supera 0.426, ejecutar P19.**
- **Corrección de dependencia:** L44 heredaba «abierto» de X2, pero **no se apoya en X2**, lo referencia: calcula un umbral desde C3 (verificada) y lo compara con la toxicidad medida de F80. Quitada esa dependencia, igual que se hizo con G6. Queda [P] por depender de F80, que es fuente secundaria — **correcto, no se fuerza a V**.

## 2026-09-26: tanda 39 (barrido en DOS dimensiones — y una autocorrección sobre el propio gráfico)
**Profundizando: barrer los márgenes en PARES, no uno a uno.** Módulo ampliado con `plano_diseno`: cruza los dos ejes que definen X2 — CCR (capacidad de vitrificar) y molaridad (toxicidad) — y dibuja la **región objetivo** en vez de un número.

**Lo que aflora al cruzar ejes y un barrido simple no veía:**
1. **La región objetivo es enorme:** cualquier química con CCR ≤ 0.426 y molaridad ≤ 9.28 resuelve el cerebro humano, con **~3 órdenes de magnitud de margen en CCR** por debajo del corte. No hay que optimizar los dos ejes.
2. **Riñón y corazón ya están resueltos en el plano** (admiten CCR de 1.9 y 1.2 °C/min) **y sin embargo nadie ha vitrificado un riñón humano**. ⇒ **Para órganos pequeños el cuello NO es el que modela el plano**: es la perfusión, la carga del CPA y el recalentamiento. El plano identifica dónde NO está el problema, que es tan útil como dónde está.
3. **Dirección de diseño:** la región objetivo se alcanza **bajando CCR sin subir molaridad**, y existe un mecanismo conocido que hace justo eso sin cambiar la concentración: los **bloqueadores de hielo** (L22 — VM3 es V3 más 1 % de X-1000 y 1 % de Z-1000, misma base). ⇒ No es «menos tóxico» ni «más concentrado», es **«misma base, aditivos que bajan la CCR»**.

**AUTOCORRECCIÓN sobre el propio gráfico.** La primera versión concluía que «M22 se pasa del umbral por sólo 0.02 mol/L» y proponía bajar su molaridad un 0.2 %. **Eso contradice L20 y E7**, leyes del propio marco: la toxicidad depende del cuádruple (composición, temperatura, tiempo, protocolo), **no de la molaridad sola**. El umbral de 9.28 M se midió con **V3 a 10 °C**; M22 se carga a **−22 °C**, otro punto del espacio. Corregido: el plano sirve para ver la **estructura** del problema, **no para situar un CPA concreto**, y el aviso queda escrito en la propia figura.

## 2026-09-26: tanda 40 (las dos campanas y la proyección condicional)
**Petición del usuario: proyectar dos gaussianas (lo que tenemos y lo que necesitamos) y cerrar a un 100 % falsable, con el código autocorrigiéndose.**
**Límite declarado antes de empezar, y no negociable:** NO se deja que el código se redondee solo al 100 %. Eso sería **fabricar avance**. Lo que se calcula es un **escenario condicional**, etiquetado como tal en cada línea. Módulo `red/proyeccion.py`.

- **Las dos campanas, y el resultado es alentador:**
  - lo que **tenemos**: 21 parámetros verificados, dispersión mediana **±12.8 %** (de ±2.8 % a ±50 %).
  - lo que **necesitamos**: 4 predicciones abiertas, dispersión mediana **±55 %** (de ±45 % a ±120 %).
  - ⇒ Lo que falta lo predecimos **4.3 veces más ancho** de lo que ya medimos. **No hace falta medir mejor de lo que medimos: basta con medir lo que falta con la misma calidad**, y el marco se cierra.
- **Cada predicción lleva valor, ±1σ y QUÉ LA REFUTA.** Eso es lo que hace el marco enteramente falsable: I1 (0.142, refutada si > 0.25), I2 (0.3 °C/min, refutada si > 0.426), I4 (17 min, refutada si < 12.5 o > 60), I5 (J = 0.57, refutada si > 0.85), X2 (PASA, refutado si la LTP ≤ 110 % con control positivo válido).
- **Techo del escenario: 98.0 %. Irreducible: 2.0 %.** ⇒ **Ni el escenario perfecto llega al 100 %**, porque quedan cosas que nadie ha hecho y que el marco **no puede proyectar**: vitrificación de cuerpo entero con recuperación, estivación de mamífero y reversibilidad de ASC. **Un marco honesto no llega al 100 %: llega hasta donde llega el conocimiento y deja el resto marcado.**
- **La autocorrección que sí es real:** al añadir un dato (una línea en el YAML), el motor recalcula todo y **si el valor cae fuera del rango predicho, la triangulación lo marca como contradicción y señala qué ley falla**. Ya ocurrió dos veces: con I1 y con el régimen isocórico de I5. ⇒ **El marco no se ajusta para encajar el dato: señala qué tendría que cambiar.**

## 2026-09-26: tanda 41 (de márgenes a PORCENTAJES, y un error de cableado en C10)
**Petición del usuario: medir, calcular y reducir los márgenes con precisión, con el código autorregulándose.** Límite declarado de nuevo: **no se mueve ningún valor, rango ni umbral para mejorar un número** (R2). Lo que se reduce es la incertidumbre que no existía y la que se puede medir.

- **Módulo nuevo `red/confianza.py` → `CONFIANZA.md`.** MARGENES.md decía a qué distancia está el vuelco moviendo un parámetro; ahora cada rango se lee como IC 95 % (normal partida en log) y se mueven **todos a la vez** (20 000 muestras por cota, semilla fija). Se da también la lectura **pesimista** (rango = ±1 σ): la verdad está entre las dos.
  - **Veredictos clave: P(falla alguno) = 0 % en la lectura principal y 2.7 % en la pesimista.** 13 veredictos son firmes (0 % incluso pesimista).
  - Los que superan el 1 % son **todos no clave**: «C2 es conservadora frente al cerdo» (7.0 %), y los tres de M22 cerca de LC ~4 cm (3–4.7 %), que dependen de **CCR_M22**, cuyo rango declarado es ×2 hacia abajo.
  - Para cada uno se da **el rango nuevo que habría que medir** (p. ej. CCR_M22 de [0.05, 0.15] a ~[0.064, 0.13]; Q10 de [2.08, 2.53] a [2.23, 2.37]).
  - **Orden de rentabilidad de medir** para los veredictos clave: exp_LC (40 %), anc_LC (33 %), BMR (14 %). Se recalcula solo al cambiar el YAML.
- **ERROR PROPIO CORREGIDO en C10:** el veredicto clave del **cerdo** se evaluaba con `flush_T`, la temperatura 10–15 °C del **perro** con flush. F42 da 10 °C para el cerdo. Nuevo parámetro `pig_T` (10, F42). Efecto: razón cerdo/C2 de 0.82–2.99 a **0.82–2.08**; P(error) pesimista del veredicto clave de 1.1 % a **0.01 %**; P(falla algún clave) pesimista de 3.8 % a **2.7 %**.
  - **Y no todo favorece:** sin la dispersión prestada del perro, el veredicto no clave «C2 es conservadora frente al cerdo» sube de 4.3 % a **7.0 %** de error. Confirma L42: a 10 °C, C2 ya no tiene margen de seguridad.
- **Comprobado y NO aplicado:** estrechar exp_LC. Un ajuste de los tres volúmenes de F2 da ≈ 1.77 ± 0.10 (1 σ), pero con 1 grado de libertad el IC 95 % es mucho más ancho que [1.67, 2.18]. El rango actual no es holgado; estrecharlo sería inventar precisión. Hacen falta más volúmenes medidos.
- Progreso **89.7 %, sin cambios**. Preregistro intacto.

## 2026-09-26: tanda 42 (TRIADA + MATE sobre exp_LC: la física cierra lo que 3 puntos no pueden)
**Paso siguiente de la tanda 41:** exp_LC y anc_LC concentran el 73 % del riesgo de los veredictos clave. Aplicado el método completo.

- **TRIADA 1 · INVENTARIO.** En la red ya estaban 0.5 L (LC 1.2 → 1.4 °C/min) y 3 L (LC 2.2 → 0.47). El de 1 L no estaba escrito, pero las tres pendientes registradas lo fijan: **LC 1.402 cm, 0.998 °C/min** (control de implementación: reproduce 2.18 / 1.80 / 1.67 exactos).
- **TRIADA 2 · MATEMÁTICA ANTES DE LEER** (`20_cotas/cota_exp_LC.py`):
  - Ajuste de los 3 volúmenes: **n = 1.77 (LC citada) – 1.82 (LC = V/A) ± 0.10**. El central teórico 2 queda a ~2 σ por encima.
  - Con 1 grado de libertad el IC 95 % bilateral es **[0.45, 3.1]**: dejar exp_LC en ±0.1 exigiría 8 volúmenes hasta ~25 L. **Inasumible, y además no es la pregunta.**
  - **La pregunta MATE es unilateral:** C3-riñón se vuelca con n > **2.34**; C6 con n > **2.52**; C8 y C11 sólo con n negativo (estructurales).
  - Camino estadístico unilateral 95 %: **C3 aguanta por poco (5.2 < 5.3); C6 NO (0.079–0.092 < 0.1) ⇒ fuga.**
  - Camino físico (Biot, PRECISION.md): 1 ≤ n ≤ 2 con h y material iguales; por encima de 2 sólo empuja la forma o el ruido, y eso está medido (+0.18). Volcar C3 exige **×1.9** ese exceso y C6 **×2.9**.
- **TRIADA 3 · MATE (reutilizar, leer sólo lo necesario).** Buscado un cuarto volumen en F2: **no existe** (0.5, 1 y 3 L). El punto de 1 L queda **confirmado en la primaria** («~1 °C/min for a 1 L (LC~1.4 cm)»). Se deja de leer.
- **Resultado — L45 (nueva):** C3 cierra por los dos caminos, C6 por el físico. **Fuga declarada:** un órgano real no es una bolsa; una forma que añada > ×1.9 el exceso observado abriría C3. Sale **[P] efectivo** (hereda de C6 ← F22): correcto, no se fuerza.
- **exp_LC documentado:** su rango [1.67, 2.18] **no es un IC**, es techo físico + exceso medido. Central en 2 y **no** en 1.8: a LC grande el exponente local tiende a 2 y 1.8 sería optimista justo donde C6 extrapola.
- **Medición mínima que cerraría también el camino estadístico:** UN volumen más en el montaje de F2 con ruido ≤ 10 %, mejor **~0.15 L** (tamaño riñón: además prueba C3 en su escala). Con ruido 15 %, dos (0.15 L y ~7 L). **Refuta:** exponente > 2.34 con ≥ 4 volúmenes.
- Progreso **89.7 %, sin cambios**. Preregistro intacto.

## 2026-09-26: tanda 43 (P21 lanzado como preregistro; dos errores propios corregidos antes de los datos)
**Petición del usuario: lanzar la prueba del volumen extra.** No hay laboratorio en esta sesión: lanzar = **preregistrar** (R2) con análisis automático. Inventar el resultado sería teatro (R5).

- **TRIADA 1 · INVENTARIO:** ningún cuarto volumen publicado en el montaje de F2. La guía mL→L del mismo grupo usa otros recipientes y protocolos ⇒ impostor (R4), no sirve.
- **TRIADA 2 · MATEMÁTICA ANTES DE LOS DATOS** (`20_cotas/cota_P21_potencia.py`, simulación de 4 000 experimentos por celda). **Dos errores propios de la tanda 42, corregidos antes de congelar:**
  1. «Basta un volumen de 0.15 L» sólo es cierto si n real ≈ 1.8; con n = 2.0 decide el 44 % de las veces, y **sin réplicas nunca puede refutar**.
  2. La regla «n ajustado > 2.34 refuta C3» daba hasta un **30 % de refutaciones falsas** con n real = 2.2. Cambiada a regla simétrica: refuta sólo si la cota **inferior** 95 % > 2.34.
  - Con la regla simétrica: **0 % de falsos positivos y 0 % de falsas refutaciones** en toda la simulación.
- **Diseño elegido (B′):** 0.15 L + ~7 L, **3 bolsas de cada uno** + 1 de control de 0.5 L (7 bolsas). Con ruido ±10 %: n ≤ 2.0 ⇒ PASA 100 %; n = 2.5 ⇒ nunca PASA; n = 2.8 ⇒ FALLA 100 %.
- **P21 congelado** (hash en prereg.lock; P15–P20 intactos). `red/p21.py` aplica las reglas literalmente; los datos se cargan en `mediciones_P21` y el motor da el veredicto. **Estado: PENDIENTE.**
- **Contrafactuales del progreso (copia desechable, no aplicados):**
  - P21 PASA: **+0 puntos**. C6 está en [P] por F22 (fuente secundaria), no por exp_LC. P21 reduce incertidumbre, no sube el número. Se dice claro.
  - F22 a fuente primaria: 89.9 %.
  - **X2 cerrada: 92.5 %**, no los +6 que da PROYECCION.md: varias leyes que dependen de X2 tienen además su propio [P]. **El escenario de PROYECCION era optimista en ~3 puntos.**
- Progreso **89.7 %**, sin cambios.

## 2026-09-26: tanda 44 (el marco calcula su propio rumbo; la proyección estaba inflada)
**Petición del usuario: darle al marco la dirección para que trabaje sobre sí mismo hacia las cuotas.**
- **Módulo nuevo `red/rumbo.py` → `RUMBO.md`.** Simula EN MEMORIA el cierre de cada nodo abierto con la misma regla de propagación del motor y calcula el camino voraz hacia `rumbo.meta` (98 %). Si ningún cierre suelto sube el total, prueba pares. **No cierra nada**: dice qué cerrar y cuánto vale.
  - **21 cierres concretos llevan de 89.7 % a 98.1 %.** Techo si se cerrara todo lo abierto: 100 %.
  - **Hallazgo:** **F47 + F52 juntas valen +1.78 puntos** y cada una sola vale 0 (se sujetan mutuamente). Es el segundo bloque después de X2 (+2.86). El ranking individual no lo veía.
- **ERROR PROPIO CORREGIDO en PROYECCION:** los puntos del escenario estaban **escritos a mano** (X2 = +5.95). Simulados con la regla del motor dan **+2.86 por la cadena NADES (X2, V26, F80)**. Techo del escenario de predicciones: **93.4 %, no 98 %**. El «2 % irreducible» era un residuo, no un cálculo: pasa a «no cubierto por ninguna predicción» (6.6 %), que depende de fuentes primarias y datos de vías, no de predicciones.
- **Punto 1 de la petición (análisis de la CCR de los NADES por calorimetría): no completado en esta tanda.**
- Progreso **89.7 %, sin cambios**.

## 2026-09-26: tanda 45 (F72 era F46 duplicada; y el rumbo pasa a decir QUÉ TIPO de trabajo pide cada cierre)
**Petición: buscar las versiones publicadas de F47 y F52 (+1.78) y recorrer el camino de 21 cierres.**

- **TRIADA 1 · INVENTARIO + casilla del IMPOSTOR (R4), y ahí estaba el hallazgo.** Buscando la versión publicada de F52 aparecieron los números 157.68 ± 7.14 y 138.06 ± 6.90 — **que el marco ya tenía en F46**. Comprobado: **F72 (preprint bioRxiv 2025.01.22.634384v3) y F46 (PNAS 123(10):e2516848123) son EL MISMO TRABAJO**, mismo título y mismos autores (German, Akdaş, Flügel-Koch, Erterek, Frischknecht, Fejtova, Winkler, Alzheimer, Zheng). Estaban duplicados: uno [V] y otro [P].
  - **F72 pasa a [V]** citando la versión publicada. **89.7 → 89.8 %.** Es el único cierre real de la tanda, y sale de detectar un duplicado, no de leer nada nuevo.
  - Aviso para futuras tandas: **antes de dar por nueva una fuente, comprobar que no sea otra ya presente con otro identificador.**
- **F47 sigue sin publicar** (bioRxiv 2026.01.28.702375, ya en v3, sin revista). **F52 sin versión publicada confirmada**: existe un segundo artículo en PNAS (123(24):e2605838123, PMID 42258742) pero **no se ha podido verificar que sea su versión publicada** ⇒ no se toca. Los +1.78 **no se pueden cobrar hoy**: es espera, no lectura.
- **LÍMITE DEL ENTORNO, declarado:** la política de red de esta sesión bloquea **todos** los dominios de revistas (nature, PNAS, PMC, PubMed, bioRxiv, ScienceDirect, Springer, arXiv...). Sólo llegan fragmentos de buscador. **El trabajo de lectura no se puede hacer desde aquí**, y decirlo es parte del método: una fuente no sube a [V] por un fragmento de buscador.
- **Enriquecimiento del rumbo:** 25 nodos anotados en el YAML con el campo `cierra`, que dice **qué acción concreta** los cierra y de qué tipo es: **[lectura]** (13 nodos), **[laboratorio]** (2), **[espera]** (3), **[no existe]** (1). RUMBO.md ya no dice sólo cuánto vale cada cierre, sino si es trabajo de biblioteca, de laboratorio o de esperar a que alguien publique.
- **Reparto real de los 10.2 puntos que faltan:** ~4.4 por lectura, ~3.0 por laboratorio (X2 y V26), ~2.0 por espera de publicación, ~0.3 sin fuente posible (V15).
- Progreso **89.8 %**.

## 2026-09-26: tanda 46 (once PDF leídos; 89.8 → 90.8 % y el atajo de los NADES se cae)
**El usuario descargó las primarias que la red de esta sesión no alcanza.** TRIADA aplicada a cada una: extraer sólo el dato que la cota pide y parar.

### El hallazgo de la tanda, y va CONTRA el marco: **el atajo a X2 por los NADES queda REFUTADO**
Las tandas 37–38 declararon que la calorimetría de los NADES era «la medición más rentable del programa». **Ya estaba publicada en F80 desde 2022 y nadie la había leído.** Al abrir el PDF:
- **Enfriando a 30 °C/min en DSC, los NADES al 50 % p/v CRISTALIZAN** (Tc onset: −26.6, −32.3, −31.0 °C; agua pura −23.7) ⇒ **CCR > 30 °C/min**, frente al umbral de **0.426** que exige un cerebro humano. Falla por un factor **> 70**.
- En el mismo ensayo el **DMSO al 50 % NO cristaliza** ⇒ a esa concentración los NADES vitrifican **peor** que el DMSO.
- Su «vitrificación» es **inmersión de un criovial en N₂** (15 000–30 000 °C/min), lo contrario de lo que pide un volumen grande.
- **La predicción I2 queda REFUTADA por su propio criterio preregistrado** (predecía 0.3 °C/min, refutada si > 0.426). El marco se falsó a sí mismo, que es para lo que se escribió.
- **ERROR PROPIO, corregido:** la ficha de F80 decía «94.65 % de viabilidad en células madre mesenquimales humanas, sin diferencia frente a DMSO». **Ese número no aparece en el artículo y no se estudian células madre** (son líneas L929 y HacaT, y la viabilidad se informa como densidad óptica). Corregido en F80, L35 y L44.
- **La recomendación operativa se INVIERTE:** medir los NADES ya no es prioritario. **X2 se queda sin atajo conocido y P19 vuelve a ser el camino.**

### Fuentes cerradas leyendo la primaria (todas de [P] a [V])
- **F22** — hígado de **cerdo entero**, 48 h a −2 °C **sin congelar** en cámara isocórica (verificado por presión), histología normal. n = 2, sin trasplante.
- **F8** — hígados **humanos** a −4 °C: **+27 h** de vida ex vivo frente a <12 h del frío clínico; viabilidad sin cambios; trasplante **simulado**.
- **F85** — hígado de rata a −6 °C hasta **96 h** con **trasplante ortotópico real**: 100 % a 72 h, ~58 % a 96 h.
- **F9** — **corrobora de forma independiente los dos anclajes de C10**: 120 min en perro a 10 °C y **60 min como límite sin deterioro de memoria**. Añade óptimos medidos: objetivo **10 °C**, enfriar a **2 °C/min**, recalentar a **0.5 °C/min**.
- **F35** — MEDY (metilcelulosa + EG + DMSO + Y-27632) en tejido cerebral humano y organoides; los de pacientes con epilepsia **conservan su patología**. Es congelación lenta con CPA diluido, **no vitrificación**, a escala de milímetros.
- **F78** — oso negro: **ninguna pérdida de hueso en 4–6 meses**, por **apagado de la resorción** (no por más formación); músculo conservado vía **mTORC1**.
- **F10** — Geiser y Kenagy 1988: **dato nuevo que acota la vía biológica.** El torpor se alarga al bajar de 8 a 2 °C, pero **por debajo de 2 °C se ACORTA**. ⇒ **Para un hibernador hay un óptimo cerca de 2 °C: más frío no es mejor**, justo al revés que en la vía física (C2).

### Otros
- **L11 RESUELTA (A → V):** las dos primarias no se contradicen. F37b falló con **glicerol o DMSO solos**; MEDY añade **inhibidor de ROCK y metilcelulosa**. **El fracaso era del CPA, no de congelar despacio.** Fuga declarada: MEDY sólo llega a milímetros.
- **F6:** el artículo de divulgación se sustituye por la revisión con revisión por pares de McKenzie 2024. **Sigue en [P]**: una revisión es mejor apoyo, pero no es primaria y no sube el número.
- **F57 sigue en [P]:** el PDF es el preprint de Res Sq, sin revisión por pares.
- Progreso **89.8 → 90.8 %**.

## 2026-09-26: tanda 47 (auditoría de declaraciones obsoletas: 90.8 → 92.1 % sin un solo dato nuevo)
**Petición del usuario: no esperar a datos, cerrar con lo que el marco ya tiene.** Tiene razón en una parte concreta, y se hace; en otra no, y se dice.

**El patrón auditado:** un nodo declarado [A] o [P] **cuyas dependencias son hoy TODAS fuertes**. Suele significar que la declaración se escribió **antes** de que sus fuentes se verificaran y nadie volvió a mirarla. No es inflar el número: es corregir una etiqueta caducada. El marco ya había hecho esto dos veces a mano (G6 y L44, tanda 38); ahora se busca en los 243 nodos de golpe.

**Seis candidatos encontrados; cinco cerrados, uno NO:**
- **L7 → [V]:** declarada [P] antes de que F13 se leyera entera. C9 es mate, F13 es [V], y la ley no afirma nada más.
- **L8 → [V]:** ídem. El veredicto que importa («la energía no limita») lo da C5, que es **mate**; la cifra de SpaceWorks es color y viene de F13 [V].
- **V27 → [V]:** F85 se leyó entera en la tanda 46 y la vía dice exactamente lo que dice la primaria (72 h al 100 %, 96 h al 58 %, trasplante real).
- **V17 → [V]:** F7 es [V] y **la irreversibilidad de la ASC es definicional, no una incógnita**. Estaba abierta por inercia.
- **V15 → [V] por IMPOSIBILIDAD DEMOSTRADA** (patrón L43): la vía no existe, pero **el veredicto sobre ella está cerrado**: tronco y cuerpo entero caen fuera de la región viable en el **100 % de las 20 000 combinaciones**. Saber que la respuesta es NO es conocimiento cerrado, no un hueco.
- **L41 se queda en [P], y es la prueba de que la auditoría no es un truco:** sigue **suponiendo** que el 42 % de fallos a las 96 h es nucleación y no daño isquémico. Esa suposición no la cierra ninguna auditoría.
- **L33 → [V]** tras corregir una imprecisión propia: decía «sin perder músculo ni hueso»; el artículo dice **pérdida «limitada»** de músculo (el hueso sí es cero). Corregido y cerrado, con la fuga declarada: nadie ha inducido ese programa en un humano.

**La auditoría queda AUTOMÁTICA en el motor:** cada ejecución lista los nodos con declaración sospechosa. **Avisa, no sube nada sola** — subirlo automáticamente sería fabricar avance (R5).

**Lo que NO se puede cerrar calculando, y por qué:**
- **X2 (+2.86)** pregunta si existe una química que sirva a escala **y** conserve la función. Es una pregunta empírica sobre una química que **nadie ha probado**. Proyectarla cerrada sería inventar el resultado. Y tras la tanda 46 **ya no tiene atajo**: los NADES quedaron descartados por su propia calorimetría.
- **F47 y F52 (+1.78)** son preprints. Sólo los cierra el calendario de una revista.
- **F6, F19, F82 (+0.41)** son divulgación, resúmenes y revisiones: por definición no son primarias. Sustituirlas exige leer las primarias que citan.

Progreso **92.1 %**. Quedan **7.9 puntos**: 2.9 de dato empírico, 2.0 de espera editorial, 3.0 de lectura de primarias.

## 2026-09-26: tanda 48 (auditoría de ARISTAS, no de nodos: 92.1 → 94.5 % sin un dato nuevo)
**Petición: cerrar todo lo honestamente cerrable, iterando hasta agotarlo.** La tanda 47 auditó *declaraciones* (etiquetas caducadas). Esta audita **aristas**: en este YAML `deps` significa apoyo probatorio y **además penaliza** (un nodo nunca vale más que su dependencia más débil). Una arista puesta como marca temática no es un adorno: es una multa.

### El hallazgo de la tanda: **ocho aristas a X2 que nunca fueron apoyo** (+1.83)
Las tandas 27–30 añadieron nodos de campos vecinos y lejanos **escritos explícitamente para atacar X2 desde fuera** (L22, L23, L25, L29, L30, L31, L32, L35) y a todos se les puso `X2` en `deps`. X2 está [A] — es la frontera empírica del programa — así que esa marca arrastraba a [A] contenido cuya evidencia está entera en fuentes ya verificadas. Es el mismo tipo de fallo que la tanda 41 llamó «error de cableado».
- **Test contrafáctico, uno por nodo.** X2 es un SÍ/NO empírico sin medir: *¿dice el nodo lo mismo con X2 = SÍ y con X2 = NO?* Los ocho lo pasan. La identidad de composición V3 = VM3 (L22) la firman los propios autores en el suplementario; los pares de números de respiración (L23) están medidos; la CCR del agua pura (L31) es una medición ajena; la calorimetría de los NADES (L35) es un resultado **negativo** sobre un candidato a X2. En los ocho **la evidencia va del nodo a X2, no al revés**.
- **Q11 conserva X2**: es una *pregunta* y X2 es una de sus respuestas. Ése es el papel correcto de la arista.
- **Límite autoimpuesto y verificado por el script: ningún nodo sube por encima de su estatus DECLARADO.** La auditoría no cierra nada nuevo; sólo deja de rebajar declaraciones que el marco ya tenía escritas. `20_cotas/auditoria_enlaces_X2.py` lo comprueba y **falla si alguno las supera**. X2 sigue [A]: la tensión (R1) se conserva intacta.

### L41 cerrada separando dos afirmaciones que estaban pegadas (+0.29)
La tanda 47 dejó L41 abierta a propósito: suponía que el 42 % de fallos a las 96 h era nucleación. Al escribir la cota con números (`20_cotas/cota_nucleacion_L41.py`) resultó que el nodo afirmaba **dos cosas distintas**:
- Un **valor** «ajustado» J ≈ 0.57 por L·h. Con φ = fracción de esos fallos que sí es nucleación, J(φ) = −ln(1 − 0.42φ)/(V·t) es **monótona creciente**, con máximo justo en φ = 1. ⇒ lo que dan los dos puntos de F85 **no es un valor ajustado: es una cota superior**. Corregido (patrón L33).
- Un **veredicto** de compatibilidad con la cota del riñón de cerdo. Ése **aguanta en todo φ ∈ [0,1] y en todas las esquinas de volumen** (rata 8–14 mL, cerdo 40–90 mL): holgura ×2.9, y romperlo exigiría **79 % de fallos por nucleación cuando F85 observa 42 % en total**. Cerrado por irrelevancia demostrada (patrón L43).
- **De paso, auditoría de los propios números:** la cota **reproduce desde cero** el 0.57 (0.567) y el ≤ 3 (3.05, regla de tres sobre los 5+5 animales de 5 h de F20) que el nodo tenía escritos a mano sin cálculo guardado.

### L13 cerrada con un dato que ya estaba en la red y nadie había cruzado (+0.11)
L13 tomaba la fila de «61 % EG solo» del preprint F52 y la de M22 del preprint F47. Pero **la información suplementaria del propio PNAS (F71, [V], PDF leído) dice que en el MISMO trabajo, mismo tejido y mismo protocolo probaron V3, EG al 61 % solo y EG 37.5 % + DMSO 12.5 %, y que V3 dio la mejor recuperación funcional.** Con F71 + F46 + F37b la serie queda entera con fuentes fuertes. F47 sale porque su fila es una **ausencia de dato** (M22: función no medida), que no puede ser base probatoria de nada; donde sí es apoyo es en X2, que lo conserva. Fuga declarada: «mejor recuperación funcional» es más vago que el «potenciación inestable» de F52; si F52 se publica, la fila gana precisión y el veredicto no cambia.

### L5 cerrada por dependencia innecesaria (+0.11)
Su veredicto («la congelación parcial no está limitada por el calor a LC 4 cm») es un resultado de **C6, que es mate**: geometría y calor latente, no experimento. F57 [P, preprint] lleva el dato a órgano grande y es la confirmación más bonita de la ley, pero la ley no la necesita.
- **Y la auditoría no es un rodillo: V06 SÍ conserva F57**, porque su casilla de escala afirma literalmente el dato del preprint («riñón de cerdo y humano, 10 días»). Un nodo que *cita* un preprint y un nodo que *se apoya* en él no son el mismo caso.

### La casilla del impostor vuelve a pillar uno: **F52 no está publicada, y ahora se sabe con certeza**
La tanda 45 dejó abierto si PNAS 123(24):e2605838123 era la versión publicada de F52. **No lo es:** es un **comentario** de Maya-Romero y Zoncu (UC Berkeley) sobre el artículo de German — otro título, otros autores. Verificado también que **F47** sigue preprint (bioRxiv v2, 5-feb-2026, sin revista) y que **F57** sigue preprint (su PMID 41646296 es el registro del preprint; lo único publicado del grupo a esa escala es un **resumen de congreso**). Y confirmado que la cita de F46 (PNAS 123(10):e2516848123) **es correcta**: título y los nueve autores coinciden.

### Lo que NO se cerró, con el motivo
- **X2 (+1.35): experimento, y no se intentó.** Pregunta si existe una química con función **y** escala. Su atajo (NADES) quedó refutado en la tanda 46 por su propia calorimetría. Proyectarla cerrada sería inventar el resultado.
- **L25 (+0.40): fuga real, y el motor la señala como sospechosa.** Sus tres dependencias son fuertes, así que la auditoría automática la marca — y **aun así se queda en [P]**, porque el ancla de que la carga en frío rescata la alta molaridad está medida en **riñón** (F65/L20), no en tejido neural. Ésa es exactamente la contradicción **I1** del marco. Test del patrón 2: si la carga en frío no rescata el tejido neural, el veredicto «la temperatura de carga es la variable decisiva» **se vuelve falso** ⇒ la incertidumbre sí cambia el veredicto ⇒ no es cerrable. Sí se corrigió su razón obsoleta: decía «queda [P] porque es preprint», y F72 dejó de serlo en la tanda 45.
- **F57 (+0.15), F47, F52: espera editorial.** Verificado hoy, ninguno publicado.
- **F6 (+0.15), F19 (+0.15), F82 (+0.11): lectura de primarias, imposible desde aquí.** Los dominios de revistas siguen bloqueados por la política de red de esta sesión. Se examinó quitar F6 de V16 por el patrón 4 y **se decidió que no**: el propio marco declara en el campo `cierra` de F6 que sostiene V16, y discutirlo con un fragmento de buscador no es método. F19 hace falta de verdad: es la única fuente del lémur *Cheirogaleus* en V09 y del pez pulmonado en V11.
- **L37: laguna declarada, y por eso no se cierra.** Sus tres longitudes de onda son reproducibles con λ = c/(f·√εr) y el veredicto «cuasiestático» es robusto en órdenes de magnitud de εr, **pero ni los 360 kHz del nanowarming ni la permitividad del tejido tienen fuente en esta red** (F41 ni siquiera está cableada como dependencia de nadie). Se examinó retirar F82 por el patrón 4 y se decidió que **no**: sin F82 la ley se quedaría sin ninguna fuente, que es peor que quedarse en [P]. Encontrar la laguna vale más que los 0.11 puntos.

**Progreso 92.1 → 94.5 %.** Quedan **5.5 puntos**: **1.35 de laboratorio** (X2), **~0.15 de espera editorial** (F57; F47 y F52 ya casi no mueven el total), **~0.4 de lectura de primarias** (F6, F19, F82) y el resto repartido en nodos que otro más débil sujeta. **La lección de la tanda:** en una red donde las aristas penalizan, un enlace mal dirigido cuesta puntos igual que un dato que falta — y auditar la dirección de las aristas es trabajo científico, no contable, porque obliga a preguntarse nodo a nodo *qué sostiene realmente a qué*.

## 2026-09-26: tanda 49 (el clúster de CAMPOS LEJANOS: el patrón de la tanda 48 aquí NO se repite, y eso es el hallazgo)

**Bloque auditado:** las siete fuentes de campo lejano (F74 tardígrado · F76 agua pura · F77 vidrios metálicos · F79 canal de vacuno · F81 foca de casco · F83 feto · F84 tanques de LNG) y las ocho leyes que sujetan (L29, L31, L32, L34, L35, L36, L38, L39). Progreso **94.5 → 94.6 %**.

### Lo primero, y es una corrección de expectativa: el clúster valía 1.40 puntos, no 3.6
`20_cotas/simul_campos_lejanos.py` replica la propagación y el COMP del motor en memoria (se autovalida contra el 94.5 % que el motor imprime) y mide **cuánto vale cada cierre de verdad**. Resultados que conviene tener escritos:
- Cerrar **todo** el clúster (7 fuentes + 8 leyes a [V]) da **+1.40**, no 3.6.
- Cerrar una ley sola da **+0.00** en los ocho casos: cada una tiene su fuente lejana [P] en `deps`, así que subir la declaración no mueve el efectivo. Y cerrar las **siete fuentes** solas también da **+0.00**, porque las declaraciones siguen en [P]. **Sólo cuentan los pares fuente+ley, +0.11 cada uno.**
- Dos pares no suben nada aunque se cierren: **F83+L39 (+0.00)** porque L39 depende además de L36, y **F84+L38 (+0.00)** porque L38 dependía de L34. Con las cuatro juntas, **+0.40**, y ahí entra **Q7** completa.
**Lección de método:** en esta red el valor de un cierre no es una propiedad del nodo, es una propiedad del camino. Medirlo antes de trabajar evita gastar la tanda en el nodo equivocado.

### El hallazgo: en este clúster la fuente secundaria **SÍ es el apoyo**, y por eso siete leyes se quedan en [P]
La tanda 48 ganó 1.83 puntos quitando aristas que eran marcas temáticas. Aquí se aplicó el mismo test nodo a nodo y **falla en siete de ocho**, por una razón estructural: en L29, L31, L32, L34, L36, L38 y L39 **la fuente lejana no es color, es el enunciado entero**. Quitar F74 de L29 dejaría a L29 sin las CAHS; quitar F76 de L31 la dejaría sin los 6.4 × 10⁶ K/s; quitar F84 de L38 la dejaría sin el límite de 9 °C/h. El test que lo decide es el que la tanda 48 ya usaba, aplicado al revés: **¿aparece el dato de la dependencia en alguna frase del nodo?** Si aparece, es apoyo. Si no aparece, es cableado. Esas siete leyes sólo suben leyendo las primarias, y **ningún dominio que las sirve es alcanzable desde esta sesión** (arxiv.org, journals.aps.org, ScienceDirect, PMC, PLOS y fao.org dan 403 al proxy). Declarado, no disimulado.

### L35 cerrada ([P] → [V], +0.11): un dato que llevaba cuatro tandas dentro de un PDF de la red
Al releer el PDF de **F80** (Jesus, Duarte & Paiva 2022, Sci Rep 12:8095, ya [V]) aparece en la Discusión la frase que a esta ley le faltaba, y la dicen los autores: «*The reason of using 50 % (w/v) instead of higher percentages of NADES is highly related to **their high toxicity at those concentrations**, as well as, their high viscosity...*». ⇒ El 50 % p/v **no es una elección de conveniencia: es el techo de toxicidad que declara la propia primaria**, y es exactamente la concentración a la que la CCR ya falla por un factor **≥ 70** (30 °C/min frente a 0.426; **1.85 décadas**, en `20_cotas/cota_campos_lejanos.py`). **Los dos lados del compromiso toxicidad↔vitrificación quedan medidos en el mismo artículo**, así que el veredicto deja de ser una inferencia nuestra sobre un solo lado.
- **Y se corrige una imprecisión propia (patrón L33):** la ley concluía que los NADES «siguen siendo interesantes por **baja toxicidad a concentración moderada**». F80 dice lo contrario justo donde importa. Lo que sí sostiene: mejor recuperación que el DMSO al 50 % p/v en dos líneas celulares, y que **el medio no hay que retirarlo, basta diluirlo**. Utilidad real: protocolos celulares, no volúmenes.
- **Arista retirada: L35 ya no depende de L29.** Test contrafáctico: con L29 cierta o falsa, los NADES cristalizan igual a 30 °C/min. L29 es un **hermano** (otra clase química, vitrificación **al secarse**), no un cimiento; la evidencia va de aquí a L29, no al revés. Era un nodo [P] arrastrando a [P] contenido cuya evidencia está entera en F80 [V] y G4 [V].
- El `cierra` («toxicidad comparada a igual concentración molar») **pasa a fuga declarada**: el veredicto no la necesita, porque la toxicidad que decide es la que hay **al máximo de concentración utilizable**, y ésa es la que F80 declara. No se convierte 50 % p/v a molaridad: los NADES son mezclas de masa molar variable y hacerlo exigiría suponer una composición (R5).

### Dos aristas más mal dirigidas, ninguna hacia X2 (patrón 2 de la tanda 48, ampliado)
- **L36 ya no depende de X1.** El contenido de X1 (los dos tramos de la zona gris) **no aparece en ninguna frase de L36**. Y la dirección es la contraria: la última frase de L36 («τ_eq no es una propiedad del tejido sino de su arquitectura metabólica») **aporta** a X1 y a G1. Se conserva G1, porque la ley sí habla de τ_eq.
- **L38 ya no depende de L34.** L34 corrobora **a C3**, que L38 ya tiene directamente **y es mate**. Colgar de un nodo al corroborador de su propia dependencia es el error de cableado de la tanda 41 en C10: el apoyo va un nivel más abajo. Efecto lateral declarado: ahora **F84 sola cierra L38 y con él Q7**, que antes exigía además cerrar F79.
- Ninguna de las dos sube nada hoy (ambas dependencias eran [V]/[M]): es **higiene de grafo**, y se hace porque un enlace falso miente sobre qué sostiene a qué aunque no cueste puntos.

### Datos sin explotar en los PDF ya descargados: uno bueno, y corrige una ley nuestra al alza
El PDF de **F6** (McKenzie 2024, leído en la tanda 46 sólo para lo que su cota pedía) trae en las págs. 8 y 13, citando a Studer et al. 2014, los números de la **criofijación de tejido** — que no son los de la rejilla de criomicroscopía de F76:
1. En tejido **sin crioprotector** se vitrifica por encima de **200 000 K/s**, que coincide **dentro de un factor 1.25** con el 2.5 × 10⁵ K/s al que F76 extrapola para < 1 % de hielo. Es una **corroboración independiente, de otro campo y otro autor, de la única cifra de F76 que el marco usa de verdad.**
2. La **profundidad de vitrificación** es de **10–20 µm** por inmersión, no ~3 µm, y sube a **~200 µm** con alta presión. **L31 subestimaba su propio techo en uno o dos órdenes de magnitud**; corregido (patrón L33). **Ningún veredicto cambia:** 200 µm siguen a un factor **200** de LC = 4 cm y a **4 × 10⁴** en velocidad.
3. **Una palanca que el marco no tenía catalogada:** a ~2000 bar el punto de congelación baja a −22 °C y **la CCR necesaria cae ×100**. La **presión** no es variable de diseño en ninguna magnitud del marco (G3 tiene forma, Tg y ΔT, no presión), y la vía isocórica de F22 la usa para **evitar** el hielo, no para bajar la CCR. Queda como **laguna declarada**, sin cablear, porque el dato llega vía una revisión [P] que cita a un tercero — igual que se hizo con L37 en la tanda 48.

### Verificación de estatus: metadatos confirmados en cuatro fuentes, ninguna sube, y una salvedad que va CONTRA el marco
- **F76:** «Direct measurement of the critical cooling rate for the vitrification of water», **Phys Rev Research 7:013095, 24-ene-2025**. Publicada con revisión por pares y el 6.4 × 10⁶ K/s está en su propio resumen. **Aun así se queda en [P]:** un fragmento de buscador confirma metadatos, no sustituye a leer la fuente.
- **F77:** **Lu & Liu 2002, Acta Mater 50:3501–3512**; confirmado también que el trabajo formula la CCR **y** el espesor crítico de sección a partir de γ. Sigue [P].
- **F81:** especie, los dos trabajos primarios y la localización glial confirmados. Añadido a la ficha y a L36, **marcado como nivel [P]**: las neuronas de foca siguen activas **hasta ~1 h en hipoxia severa frente a minutos en ratón**, con mecanismo propuesto de **«ANLS inversa»** (lanzadera de lactato neurona→astrocito). Ese «~1 h» es del orden del τ_cel de G1, **no del τ_org**: la foca no extiende la ventana del organismo, extiende la de la neurona.
- **F79, y esto rebaja a L34:** el artículo de revista es **Mallikarjunan & Mittal 1994, J Food Eng 23:277–292, «...— *modelling and simulation*»**. **Es un trabajo de modelo, no una campaña de medición.** Luego el lado «medido» de la razón medido/predicho de L34 **no se apoya en ese artículo**, sino en cifras de práctica industrial del manual de la FAO, **sin n ni desviación**. Comparar un modelo con otro modelo no sería validación. Anotado como tercera salvedad de L34; **ningún número se ha tocado**.
- **R4, casilla del impostor:** ninguna de las siete fuentes lejanas duplica a otra ya presente, y el script comprueba que no hay dos identificadores con la misma URL en las 84 fuentes.

### La tentación, dicha en voz alta porque señala dónde el marco es frágil
**F76 se quedó a un paso de [V] y la regla que lo impide no es la del propio marco.** El marco da [V] a F67 y F73 con «resumen primario verificado», y el dato que el marco usa de F76 **está en su resumen** y se confirmó palabra por palabra. Con el criterio interno F76 sería [V] (+0.11 con L31). No se subió porque la instrucción de esta tanda es más estricta que el marco: **un fragmento de buscador no es leer la fuente.** Queda escrito porque la fragilidad está en el propio criterio: **[V] mezcla dos cosas distintas — «es una primaria» y «alguien la ha leído» — y el marco debería separarlas** en vez de resolver caso por caso.

**Progreso 94.5 → 94.6 %.** Del clúster quedan **1.29 puntos**, y los siete son del mismo tipo: **lectura de primarias que esta sesión no puede alcanzar**. **La lección de la tanda:** la auditoría de aristas **no es un método que siempre rinda** — aquí rindió una vez de ocho, y las otras siete veces el resultado útil fue *saber por qué no se puede cerrar*. Una auditoría que siempre encuentra algo no está auditando.

## 2026-09-26: tanda 50 (barrido de aristas sobre TODO el grafo, y una colisión de nombres que era una mina; 94.5 → 94.9 %)
**Petición: generalizar el test de la tanda 48 a toda arista, no sólo a las que apuntaban a X2, y barrer las capas poco auditadas (preguntas, vías, ontología/magnitud/frontera).** Bloque de esta tanda: todo el grafo MENOS el clúster de campos lejanos (F74/F76/F77/F79/F81/F83/F84 y L29/L31/L32/L34/L35/L36/L38/L39), que trabajaba otro agente en paralelo.

### El barrido, y lo primero que dice es que había mucho menos de lo que parecía
`20_cotas/barrido_aristas_global.py` enumera las **382 aristas** del grafo (sin parámetros) y se queda con las que de verdad cuestan algo: las **PENALIZANTES**, las que por sí solas impiden que un nodo valga lo que su texto declara. Son **17**, y su techo teórico conjunto era **+1.93**. De ésas, 9 son del clúster ajeno o de X2 ⇒ **el ámbito propio eran 6 aristas y ~0.7 puntos**, no los ~1.9. Decirlo antes de empezar es parte del método: el barrido sirve igual, porque **acota** cuánto hay.

### Dos aristas pasan el test contrafáctico (+0.44)
- **L26 → L25 (+0.29, y arrastra Q22).** Las cuatro afirmaciones de L26 están en F69 [V] (objetivo 65 % p/v, TC al 83/97 %, 36 % de encogimiento) y en F72 [V] (respiración 80.4 frente a 173.3); la separación entre lesión osmótica y toxicidad química la da L20 [V]. Lo único que L25 añade por encima de F72 es su propia afirmación **abierta** («la temperatura de carga es la variable decisiva»), y el veredicto de L26 es cierto **en las dos ramas** de esa incógnita: si la carga en frío rescata la alta molaridad, P-19 no cargó a −22 °C y recibió igual la dosis tóxica; si no la rescata, con más razón. ⇒ referencia cruzada, no apoyo. **L25 sigue [P] y la contradicción I1 sigue abierta** (R1). Lo que deja de ocurrir es que una incógnita de MECANISMO rebaje una MEDIDA ya hecha.
- **V16 → F6 (+0.15), y es una arista FÓSIL.** F6 era el artículo de divulgación de Asterisk Mag, y por eso colgaba de la fila de criónica. En la **tanda 46 esa ficha se sustituyó** por la revisión de McKenzie 2024 sobre histología de estructura cerebral, y nadie volvió a comprobar la arista. Los cuatro campos de V16 los sostienen F16 [V] y F69 [V]; **ninguno procede de F6**. Verificado no con un fragmento de buscador (que es lo que hizo abortar esta misma auditoría en la tanda 48) sino **buscando cada afirmación de V16 en el texto completo del PDF de F6**: sus dos únicas menciones de la criónica son bibliográficas (citan a Best 2008, que en esta red es F5 y está huérfana). **Patrón nuevo, hermano del de la tanda 47: arista obsoleta por SUSTITUCIÓN DE FUENTE.** Si una ficha cambia de trabajo, hay que revisar sus aristas, no sólo su estatus.

### El hallazgo que no daba puntos y era el más serio: **el parámetro Q10 y la pregunta Q10 tenían el MISMO id**
El motor mete todos los nodos en un solo diccionario y **las preguntas entran al final**: la pregunta sobreescribía al parámetro. Consecuencia real, visible en `red/grafo.md`: **C2, C4, C9 y C10 — cuatro cotas MATE — dejaban de ver un parámetro** (cuya incertidumbre la propagación exime a propósito, porque entra por el rango) **y pasaban a depender de una PREGUNTA**, con un ciclo dibujado C2 → L12 → Q10 → C2. Hoy no cambiaba ningún estatus porque O3, G8 y L12 están fuertes, **pero si una de las tres bajara a [P] se caerían cuatro cotas mate y todo lo que cuelga de ellas** (L2, L18, L4, L7, L9, L42, G1, V01, V02...). Se renumera la **pregunta** a **Q23** (el parámetro no se puede renombrar sin editar `red/motor.py`, que no se toca). **Progreso idéntico, 94.9 %** — y el recuento de nodos pasa de 243 a 244 porque el parámetro deja de ser devorado. Higiene de paso: `deps` duplicadas en **G7** (F37b dos veces) y **V06** (F66 dos veces).

### Corrección de contenido en la capa de vías, que nadie había reauditado
**V16** decía «llegó al tanatorio ~90 min ⇒ **un orden de magnitud** por encima del <10 min». La tanda 45 ya había corregido eso **en L21**: lo que cuenta para τ_eq es el **inicio de la perfusión, 4 h 40 ⇒ ~28×**. La corrección se había aplicado a la ley y no a la vía. Barridas las 27 vías y las 22 preguntas buscando el mismo tipo de residuo: no hay más (los «94.65 %» y «sin perder músculo» que salen al grepear son **las correcciones ya escritas**, no los errores).

### Lo que NO se cerró, con el motivo
- **V06 → F57, V09 → F19, V11 → F19, L37 → F82:** las cuatro NO pasan el test y se quedan. V06 **afirma** el dato del preprint (riñón de cerdo y humano a 10 días) y es su mayor escala; F19 es la **única** fuente del lémur de V09 y de la fila entera de V11; sin F82, L37 se queda sin ninguna fuente. Buscado un sustituto en los **once PDF** de `10_fuentes/pdf/`: ninguno menciona lémures (la única coincidencia de «lemur» es un falso positivo dentro del apellido «Lebranth»), ninguno menciona kHz, MHz, permitividad ni dieléctrico salvo una **cita bibliográfica** en F6 a Wowk 2024 (27 MHz), que es otro trabajo y no está en la red. La laguna de L37 sigue exactamente donde la dejó la tanda 48.
- **V11: se examinó cerrarla por irrelevancia demostrada (patrón L43/V15) y se decidió que NO.** Su **veredicto** sí es cierto en todo el rango: que el pez pulmonado no sea mamífero es taxonómico y que la estivación no sea una pausa lo fija la propia ontología O1, y ningún valor de la ventana lo cambiaría. Pero la fila **afirma un dato propio**, los 3–4 años, y viene de un resumen: subirla a [V] sería declarar verificado lo que no se ha verificado. La diferencia con V15 es exacta: **V15 no afirma ningún dato** («escala: ninguna lograda») y su veredicto lo dan cotas mate. Anotado además que **ningún nodo depende de V11**: esos 0.15 puntos son el precio de catalogar honestamente una vía irrelevante.
- **Q5, Q6, Q7, Q11, Q20: se quedan TODAS, y aquí el test no aplica.** Una pregunta vale lo que su respuesta más débil, y eso es correcto: una pregunta con una respuesta floja **no está respondida**. Quitar la respuesta para subir la pregunta sería esconder la respuesta. X2 sigue siendo respuesta legítima de Q11.
- **X2: no se intentó**, por instrucción y por método: es empírica y su atajo se cayó en la tanda 46.

### Dos fragilidades del marco que conviene declarar (R4)
1. **El marco penaliza citar una revisión.** F6 queda sin sostener nada, y **no se puede recolocar** donde sí sería buen apoyo (G5, V17, capa E0) porque añadir una fuente [P] a un nodo [V] lo **rebaja**. Una revisión correcta no puede entrar en el grafo sin coste.
2. **La propagación exime a los parámetros, y eso deja cotas mate apoyadas en fuentes secundarias sin que el número lo note.** `turtle22_h` viene de F19 [P] y `tau_org_good` de F25b [P]; C4 y C7 siguen siendo [M]. Es **defendible por diseño** (la incertidumbre de un parámetro entra por su rango, y la cota se evalúa en las esquinas), pero hay que decirlo: el veredicto «×10 incluso a 22 °C» de L4 descansa en un rango tomado de un resumen. **No se toca** — mover un rango está prohibido (R2) y quitar la exención bajaría el número sin añadir conocimiento.

### Coordinación medida para el clúster de campos lejanos (simulado, no aplicado)
Subir **sólo** las ocho leyes vale **+0.00**; subir **sólo** sus siete fuentes vale **+0.00**. Hay que subir **cada ley junto con su fuente**: L29+F74, L31+F76, L32+F77, L34+F79 y L36+F81 valen **+0.11 cada par**, y L35, L38 y L39 sólo suben en cadena detrás de L29, L34 y L36. **Todo el clúster junto: +1.40** (hasta 96.3 %). Es el mismo tipo de efecto de par que la tanda 44 encontró en F47+F52: el ranking individual no lo ve.

**Progreso 94.5 → 94.9 %.** Scripts: `20_cotas/barrido_aristas_global.py` (enumera las penalizantes de todo el grafo), `20_cotas/auditoria_aristas_tanda49.py` (aplica el test una a una y deja escrito el veredicto, incluidas las que NO pasan) y `20_cotas/verificacion_tanda49.py` (seis bloques de `assert`: YAML válido, preregistro intacto, nadie por encima de su declaración, tensiones conservadas, `red/motor.py` idéntico al de HEAD y grafo acíclico). **La lección de la tanda:** el barrido rindió menos en puntos que la tanda 48 y encontró algo peor que una arista mal puesta — **dos nodos distintos con el mismo nombre**. Un marco que se audita a sí mismo tiene que auditar también sus identificadores, no sólo sus afirmaciones.

> **Nota de fusión (tandas 49 y 50).** Las dos tandas se ejecutaron **en paralelo y aisladas**, cada una en su copia del repositorio, y se fusionaron después. Por eso la 50 se escribió creyendo que L35 seguía en [P]: la 49 la había cerrado en su propia rama. Su script de verificación fallaba en esa única aserción y se actualizó al estado fusionado; las seis comprobaciones pasan. **Conjunto: 94.5 → 95.0 %.** Los bloques eran disjuntos (campos lejanos frente al resto del grafo) y el diff del YAML aplicó limpio en ambos sentidos.

## 2026-09-26: tanda 51 (una bibliografía del usuario destapa una laguna en el núcleo del marco)
**El usuario aportó ~80 referencias por bloque. El hallazgo con más alcance no está en ninguna fuente que íbamos a leer: está en un trabajo adyacente.**

- **LAGUNA EN `CCR_M22`, y toca el núcleo.** Existe literatura (carga de CPA en tejido renal) que informa que la CCR **medida en tejido** puede ser **hasta ×5 menor** que en solución libre. El marco **ya tenía la prueba de que el efecto existe y no la había generalizado**: `CCR_VS55` declara «tejido <1, solución 2.5» (factor >2.5) y `CCR_VMP` está etiquetada como tejido. **`CCR_M22` no está etiquetada**, y su fuente F2 vitrificó M22 en **bolsas**, no en tejido.
  - **Consecuencia calculada:** la tasa en el tronco es **0.0404 °C/min** y el veredicto «M22 falla en el centro del tronco» exige CCR_M22 > 0.0404. El mínimo del rango actual (0.05) lo sostiene por **×1.24**. Con un factor de tejido ×2.5 el rango sería **[0.020, 0.060]** y **el veredicto se da la vuelta**.
  - **Y eso alcanza a un cierre de esta misma sesión:** V15 se cerró en la tanda 47 por imposibilidad demostrada apoyándose en L43 («tronco y cuerpo entero fuera en el 100 % de las combinaciones»), y ese 100 % se calcula con el rango de CCR_M22. **El cierre de V15 queda declarado como CONDICIONADO a la etiqueta de ese parámetro.**
  - **NO se mueve el valor** (R2): la primaria no se ha leído. Se registra la laguna, la dirección del sesgo (si es de solución, el marco es **conservador** con M22) y de qué depende el cierre.
  - Nota: MARGENES.md ya marcaba estos veredictos como FRÁGILES y CONFIANZA.md les daba 3–4.7 % de error. Lo nuevo no es que sean frágiles: es que hay un **motivo para pensar que el sesgo va en la dirección que los rompe**.
- **Precisión en F81 (R4).** La ficha atribuye a **Mitz 2009** el dato de que las neuronas de foca aguantan más en hipoxia que las de ratón. Esa comparación, con registros intracelulares, es de **Folkow et al. 2008**, que **no está citado en la red**. Mitz sostiene el mecanismo glial, que es lo que L36 afirma. Declarado, no corregido: ninguna de las dos se ha leído entera.
- **Convergencia independiente sobre X2.** El análisis del usuario llega a la misma conclusión que `ESPACIO.md` había calculado horas antes: el valor de P19 ya no es demostrar que la vitrificación conserva función neural —eso lo demostró V3 y está publicado— sino **si la química M22 cruza el mismo puente funcional que cruzó V3**. Dos caminos distintos, misma frase.
- Progreso **95.0 %**, sin cambios: esta tanda no cierra nodos, **abre una laguna**. Que el número no suba al encontrar algo importante es el comportamiento correcto.

## 2026-09-26: tanda 52 (la cascada con TODO el marco, y el precio de contar dos veces el mismo experimento)
**Petición del usuario: no lanzar la cascada limitada a una cadena, sino hacer que todo el marco aporte su dato.** La crítica era correcta: `cascada.py` propagaba sólo la cadena de Arrhenius, cuando I1 ya tiene cuatro caminos y hay evidencia fuera de I1.

- **Caminos añadidos:** F47 (M22 en cerebro de conejo, cerdo y biopsia humana, sin hielo), F5 (riñón de conejo con M22 trasplantado, E3) y L13/F71 (V3 a 8.42 M conserva LTP y M22 sólo es un 10 % más concentrado).
- **ERROR PROPIO, detectado y corregido en la misma tanda.** La primera combinación usó 1−∏(1−p), que trata cada camino como una **oportunidad independiente de que P19 pase**, como billetes de lotería. Dio **99 % por las dos vías**, honesta e ingenua, lo que delató el fallo: un modelo que da lo mismo diga lo que diga cada camino no está midiendo nada. Los caminos son **observaciones ruidosas del MISMO hecho latente**, no oportunidades. Corregido a multiplicación de **razones de verosimilitud** sobre un prior de 0.5.
- **Resultado con el modelo correcto:**
  - sólo la cadena de Arrhenius: **78 %**
  - **todo el marco, combinación honesta: 89 %**
  - todo el marco, combinación ingenua: **95 %**
- **El agrupamiento por ancla es lo que separa 89 de 95.** Tres de los seis caminos leen el **mismo conjunto de datos de German** (F72/F46): la cadena de Arrhenius, la calibración daño↔LTP y el argumento de concentración V3↔M22. Si ese conjunto estuviera sesgado, los tres fallarían a la vez. Dentro de un grupo que comparte ancla **no se multiplican** las verosimilitudes: se toma la más fuerte. Sólo hay **3 anclas independientes** (German, Fahy renal/cerebral, conejo), no 6 caminos.
- **⇒ El usuario tenía razón en que todo el marco debía hablar: la creencia sube de 78 % a 89 %. Y tenía razón a medias en cuánto: contar los seis como independientes la habría inflado hasta 95 %.** La diferencia entre 89 y 95 es exactamente el precio de contar dos veces el mismo experimento, y ahora está cuantificado.
- **Lo que NO cambia, y es el motivo de que X2 siga abierta:** ninguno de los seis caminos mide **M22 sobre tejido neural con función**. Todos rodean el hueco; ninguno lo cruza. Por eso el número sube y no se cierra. El eslabón sin dato —que la energía de activación medida en **ovocitos** gobierne la LTP de CA1— sigue siendo el techo.
- Progreso **95.0 %**, sin cambios. Una creencia del 89 % no es una medición, y el historial sigue siendo 0 aciertos de 1 (I2 falló por un factor 100).

## 2026-09-27: tanda 52 (AUDITORÍA EN CONTRA de los cierres de hoy: 95.0 → 93.0 %, y el número baja porque tenía que bajar)
**Petición: no cerrar nada. Intentar TUMBAR cada cierre de las tandas 47–51 y reabrir los que no aguanten.** Seis nodos reabiertos, ningún valor movido (R2), `red/motor.py` intacto. **Que el progreso baje 2.0 puntos es el resultado, no el accidente:** dos de esos puntos estaban sostenidos por argumentos que nadie había revisado en contra.

### El hallazgo de la tanda, y no necesita ningún dato nuevo: **el «100 %» de L43 es un artefacto del muestreo**
La laguna de `CCR_M22` (tanda 51) se recorrió hasta el final en `20_cotas/cota_CCR_M22_tejido.py`, y de paso apareció algo peor que la laguna.
- **Lo que la tanda 51 no había recorrido: lo que se mueve es la FRONTERA, no un veredicto suelto.** `CCR_M22` entra en la derivada `b_CCR` y por ahí en `M_de_CCR`, `LC_viable` y `masa_viable`. Con un factor de tejido ×2.5 la masa viable pasa de **10.9 a 41.9 kg**; con ×5, a **115 kg**. El tronco entero entra en la región viable.
- **Y entonces la pregunta obvia: ¿aguanta L43 con los valores DECLARADOS?** `red/motor.py` dice en su cabecera que el criterio mate del marco son **las esquinas** («las esquinas acotan el rango completo sin Monte Carlo (R5: no hay teatro)»). L43 usa un **Monte Carlo triangular**, que concentra la masa en el centro y **nunca visita una esquina**. Recalculado en las 2⁶ = 64 esquinas de los seis parámetros de la frontera, **sin mover nada**: `LC_viable` va de **3.37 a 8.87 cm** (`masa_viable` de 4.3 a 78.9 kg), el **tronco (LC 7.5) cae DENTRO en 12 de las 64 esquinas** y el **cuerpo entero (LC 3.9) en 50 de 64**. Sólo el cerebro aguanta: **64/64**.
- **El propio motor ya lo estaba imprimiendo y nadie lo cruzó:** C3 da «M22 falla en el centro del tronco» como **✔~** (cierto en el centro, **NO robusto**). La cota y la ley se contradecían sobre el mismo rango.
- **Segundo defecto, independiente:** L43 juzga al «cuerpo entero» por **masa** (70 kg frente a `masa_viable`) mientras C3 lo juzga por **LC** (3.9 cm frente a `LC_viable`) y concluye **lo contrario** («M22 vitrifica el cuerpo medio»). `masa_viable` es la masa de la **esfera** equivalente a `LC_viable`, y un cuerpo no es una esfera. Dos reglas para el mismo objeto.
- **L43 → [A].** Queda cerrado el veredicto del cerebro; abiertos el del tronco y el del cuerpo entero.

### V15: el cierre «por imposibilidad demostrada» se cae, y encima le faltaba la arista
**V15 → [A].** Tres motivos que se suman: (1) se apoyaba entero en L43, hoy reabierta; (2) **la arista a L43 no existía** — la fila afirmaba el dato de L43 en su texto y `deps` era sólo `[C1, C3]`, así que el estatus de L43 nunca le llegaba (mismo error de cableado que la tanda 48 cazó en las ocho aristas a X2, pero al revés: aquí **faltaba** la arista que sí era apoyo; hoy se añade); (3) la condición que la tanda 51 escribió se cumple en la dirección que rompe el cierre. **Lo que sigue en pie:** C1 («M22 no se recalienta por superficie en el tronco») es mate y clave, y perfusión y bobina de MW siguen sin resolver ⇒ la vía sigue **no lograda**; lo que ya no se puede decir es **demostradamente imposible**.

### F13 era una REVISIÓN marcada [V], y sostenía dos cierres de la tanda 47 (−1.20)
Nordeen & Martin 2019, Physiology 34:101, es una **revisión** («*this review examines suspended animation...*»), y los dos datos que esta red le pide **nacen en otros trabajos que ella cita**: el caso clínico de hipotermia a 13.7 °C, y el ahorro de masa del **52–68 %**, que es de los estudios NIAC de **Bradford/SpaceWorks** («*mass reductions ranging from 52 % to 68 %*» frente al TransHab de referencia) y **no está en la red**. El marco ya aplica este criterio: **F6 es una revisión con revisión por pares y está en [P] con la razón escrita**, igual que F19 y F82. F13 en [V] era la **única excepción sin justificar**.
- **F13 → [P]**, y con ella **L7 → [P]** y **L8 → [P]**, cuyos cierres de la tanda 47 decían literalmente «hoy F13 es [V]». L8 además **atribuye a F13 un número que no es suyo**: el mismo patrón que la tanda 51 encontró en F81 (Mitz en vez de Folkow).
- **Efecto colateral que conviene ver:** C9, una cota **mate**, pasa a efectivo [P] porque F13 está en su `fuente_verif`. El cálculo de C9 no cambia; lo que cambia es que ya no hay una primaria detrás.
- **Lo que NO se hizo, y es la trampa de la tanda:** L33 queda rebajada por L8, y el test de aristas **habría licenciado quitar la arista L33 → L8** (los datos de L8 no aparecen en ninguna frase de L33). No se quitó: la tanda 48 ya avisó de que en una fila con varios ejemplos **el test premia borrar el ejemplo caro**, y usarlo aquí sería usarlo para proteger el número.

### L5: el marco usó DOS criterios distintos para la MISMA arista, y se quedó con el que le convenía (−0.11)
El test que la tanda 49 fijó y escribió es «**¿aparece el dato de la dependencia en alguna frase del nodo?**». El dato de F57 — **riñones de cerdo y humano, 10 días** — **aparece dos veces en el texto de L5**, y F57 se cita otra vez en su fuga (2). Con ese test la arista es apoyo. Para retirarla se usó **otro** criterio («el veredicto no la necesita, C6 es mate»), que la misma tanda **rechazó** para V06 con la frase al lado: «un nodo que *cita* un preprint y un nodo que *se apoya* en él no son el mismo caso». L5 cita y afirma igual que V06. **F57 vuelve a `deps` de L5 y L5 → [P]** mientras F57 siga preprint. El veredicto del nodo no cambia. Alternativa legítima para volver a [V]: **borrar del texto las dos frases**, no borrar la arista.

### Cierres que AGUANTAN, y uno que aguanta con una salvedad nueva
- **V27 [V] aguanta, verificado literal en el PDF de F85:** «*58 % long-term survival after 96 hours... while 100 % survival was limited to 72 hours*», trasplante ortotópico real. La vía no afirma nada más.
- **V17, L22, L23, L26, V16, Q22, L13, L30, L31, L32, L35, L29, L36, L38 y la renumeración Q10→Q23:** aguantan. **V16 ← F6 reverificado de forma independiente** en el texto completo del PDF: las dos únicas menciones de la criónica son bibliográficas (Best 2008), y «Alcor» y «Asterisk» no aparecen. Las ocho aristas a X2 aguantan por una razón estructural: **X2 es una pregunta empírica sin responder, y de una pregunta sin responder no se puede tomar un dato**.
- **L41 [V] aguanta CON SALVEDAD NUEVA, y es una asimetría de método: el lado de la rata no tiene n.** El PDF de F85 **no da el número de animales** en ningún sitio (buscado «n =» y «number of rats»), así que el 42 % es una **proporción puntual**, no una cota; el lado del cerdo **sí usa n** (regla de tres sobre 5+5). El veredicto de compatibilidad aguanta igual: con una cota binomial al 95 % y un n pequeño plausible (3/7 o 2/5) la J de la rata sube a ~1.4–1.6, todavía por debajo de la peor esquina del cerdo (2.04). Añadido también que **F85 es un artículo de PROTOCOLO** (Nat Protoc), no una campaña de medición — el mismo tipo de salvedad que la tanda 49 puso a F79.

### Los módulos nuevos, auditados uno a uno
- **`cruce.py`: la «brecha limpia» AGUANTA, y el confundido de ectotermia NO la invalida** — el punto que fija el suelo natural **es la ardilla ártica, un mamífero**: quitar la rana, la tortuga y el pez pulmonado deja el suelo exactamente en ×216. **Pero el documento afirmaba una cosa que no calculaba:** «las bandas no se solapan ni en sus extremos» se escribía a mano mientras `hay_brecha` comparaba **sólo los valores centrales**. Ahora se calcula (techo artificial ×79.9 frente a suelo natural ×123: **disjuntas de verdad**) y la frase se escribe desde el cálculo, con la rama contraria preparada. **Tercera salvedad añadida:** los dos lados de la brecha **no están al mismo nivel de éxito demostrado** — el techo artificial lo fija p07 (BrainEx, **E1**) frente a naturales todos en **E4**. Exigiendo el mismo nivel E, el techo artificial baja a ×12 y **la brecha crece a ×18**. La salvedad no rompe el hallazgo: lo agranda. Pero sin ella un lector lee «los protocolos humanos llegan a ×48 con un animal recuperado», y eso es falso.
- **`espacio.py`: tenía la CCR de M22 (0.10), de VS55 y de VMP ESCRITAS A MANO**, duplicando parámetros del YAML (R4, casilla del impostor). Si `CCR_M22` se etiquetara algún día —que es justo la laguna abierta— `ESPACIO.md` no se enteraría. **No se mueve ningún valor: ahora se comprueba que coinciden y el desfase se declararía en el propio documento.** Sus conclusiones aguantan: el requisito de 0.425 °C/min sale de C3 sola y la intersección sigue vacía en **todos** los escenarios de `CCR_M22`, porque lo que le falta a M22 es **función neural**, no CCR.
- **`confianza.py`, `rumbo.py`, `p21.py`:** los cálculos son correctos. Fragilidad declarada en `confianza.py`: el titular «P(falla algún veredicto clave) = 0 %» es un **0/20 000**, y el módulo da cota superior de Wilson por fila pero **no para el agregado**; la lectura pesimista (2.72 %) es la que hay que citar al lado. `p21.py` aplica literalmente los umbrales congelados y no tiene ningún parámetro ajustable.
- **Bug arreglado en `20_cotas/barrido_aristas_global.py`** (no en el motor): al simular la retirada de aristas podía dejar una pregunta **sin respuestas** y `min()` de secuencia vacía reventaba. Una pregunta sin respuestas no está respondida: vale [A], que es su suelo.

### Y una laguna nueva, que la tanda 51 dejó a medias
**La recta `b_CCR` ya mezcla etiquetas hoy, sea cual sea la de M22:** toma `CCR_VS55` en su valor de **solución** (2.5) y `CCR_VMP` etiquetado como **tejido**. Poniendo los tres puntos en tejido, y **sin tocar M22**, la pendiente pasa de −1.739 a −1.518 décadas/M. ⇒ La laguna no es sólo «de qué tipo es `CCR_M22`»: es que **la recta no declara de qué tipo es ninguno de sus tres puntos**.

**Progreso 95.0 → 93.0 %.** Scripts: `20_cotas/cota_CCR_M22_tejido.py` (+ `.out.txt`), y `20_cotas/verificacion_tanda49.py` con un bloque nuevo que **registra las seis reaperturas como expectativa**, para que ningún barrido posterior las vuelva a cerrar sin refutar el motivo escrito. Las seis comprobaciones pasan y el marcador no se ha tocado. **La lección de la tanda:** un marco que sólo se audita a favor sube de número y baja de verdad. **Y la fragilidad que queda señalada aunque no se haya tumbado: el marco tiene TRES criterios de robustez conviviendo** — las esquinas (motor), el Monte Carlo triangular (L43, `precision.py`) y los porcentajes (`confianza.py`) — y **no dicen lo mismo**. Mientras no se declare cuál manda, cualquier nodo puede cerrarse con el criterio que más le convenga.

## 2026-09-27: tanda 53 (L43 se cierra RETIRANDO lo que era falso, no refutando la auditoría)
**El usuario aportó URLs para los nodos pendientes y, en su punto 6, la salida correcta para L43: «o estrechas los parámetros hasta que el tronco falle en todas las esquinas, o rebajas el claim».** Se hace lo segundo, que es lo honesto: los parámetros no se tocan (R2).

- **Verificación independiente de las 64 esquinas**, con los valores declarados y sin mover nada:
  - **cerebro DENTRO de la región viable: 64/64** ⇒ cerrado por irrelevancia demostrada de la incertidumbre.
  - tronco fuera: **48/64**. Cuerpo entero fuera: **12/64**. **Nada que ver con el 100 % que L43 afirmaba.**
- **L43 → [V] con el enunciado rebajado.** Ya no afirma nada sobre el tronco ni sobre el cuerpo entero. Es el patrón de L33: corregir la exageración y entonces cerrar. **+0.58 puntos, 93.0 → 93.4 %.**
- **El assert de la tanda 52 frenó el cierre, y tenía razón en la forma.** Decía: «si se vuelve a cerrar, hay que refutar el motivo escrito». **No se refutó: se ACEPTÓ.** La expectativa se actualiza dejando escrita esa diferencia, y con dos asserts nuevos que impiden que L43 vuelva a [V] sin declarar el 48/64 y que V15 se cierre mientras la imposibilidad no esté demostrada.
- **V15 sigue en [A], y es la consecuencia que no se oculta:** la imposibilidad de vitrificar un tronco o un cuerpo entero **no está demostrada**. Lo que cerré en la tanda 47 era falso, y al rebajar L43 queda claro por qué.
- **Discrepancia de conteo declarada:** 48/12 aquí frente a 52/14 en la auditoría. Viene de juzgar el cuerpo por **LC** o por **masa**, los dos criterios que conviven en el marco sin declarar cuál manda. C3 usa LC y concluye lo contrario de lo que L43 afirmaba por masa. **Es la misma grieta de los tres criterios de robustez, en otra forma.**
- **Error propio en el camino:** el primer assert que escribí leía `N["L43"]["t"]` creyendo que era el texto, cuando en ese script `"t"` es el **tipo** de nodo. Corregido.
- **Las URLs aportadas no son accesibles desde este entorno**: nasa.gov, ntrs.nasa.gov, sei.aero, arxiv, wikipedia y la copia del Lancet dan 000 o 403. La lectura de F13, L8, F82 y F19 sigue bloqueada.

## 2026-09-27: tanda 54 (las primarias que faltaban, y una cifra del marco que su propia primaria no sostiene)
**El usuario descargó los PDF y pegó el contenido de la página de Alcor.** Tres resultados, y el tercero va contra el marco.

### Cerrado: L7 y L8 contra sus primarias (93.4 → 94.3 %)
La auditoría de la tanda 52 reabrió las dos porque se apoyaban en **F13, que es una revisión**, y sus datos nacían en trabajos que ella cita y que **no estaban en la red**. Ahora están:
- **F89 [V]** — informe **NIAC Phase I** (Bradford/SpaceWorks), leído entero. Cifra literal: «Compared to the current NASA reference **TransHab** design, the torpor-enabled habitats indicated **mass reductions ranging from 52 % to 68 %**». **L8 → [V]**, apoyada en C5 (mate) y F89.
- **F88 [V]** — **Gilbert et al. 2000, Lancet 355:375**, leído entero. Cronología de primera mano del caso de 13.7 °C. **L7 → [V]**, y **C9 recableada de F13 a F88**: el caso que C9 analiza es exactamente el del Lancet.
- **El assert del auditor frenó los dos cierres, y esta vez SÍ se refutó su motivo**, no se aceptó: el dato que él declaraba ausente está ahora en la red, leído. Las expectativas se actualizan con asserts nuevos que exigen que L7 y L8 dependan de las primarias y **no** de F13.
- **F13 sigue en [P]** —sigue siendo una revisión— pero ya no sostiene nada.

### DISCREPANCIA: la primaria no sostiene el valor que la red tenía
`hypo_case_min` = **412 min** («6 h 52 de parada»), heredado de F13. **El Lancet da otra cosa:** parada a las 19:00, flujo de bypass a las **21:50** (**170 min**) y ritmo con pulso hacia las 22:15 (**~195 min**). **La primaria NO sostiene los 412.**
- **El valor NO se mueve** (R2): no consta de dónde sale el 412 y corregirlo exige una fuente que lo explique. Se declara en la ficha.
- **Impacto calculado en C9:** el veredicto clave («razón > 3 ⇒ hubo bajo flujo») **se sostiene en todas las esquinas con los tres valores**, pero el margen cae de **×7.9–18.7** a **×3.26–7.71** sobre un umbral de 3. **El veredicto no cambia; la confianza sí.**
- Es el mismo patrón que F81/Mitz (tanda 51) y que F13 (tanda 52): **un dato atribuido a una fuente que no lo contiene.** Tercera vez esta semana.

### F87: la página de Alcor resuelve una laguna y abre otra
Fuente **organizacional, no revisada por pares ⇒ [P]**, mismo criterio que F36.
- **Resuelve la DIRECCIÓN de la laguna de `CCR_M22` (tanda 51).** A **81 % de la concentración de M22** un cerebro de conejo vitrificó **sin hielo**, y los autores declaran que esa concentración **no permanecería vitrificada como solución desnuda** ⇒ «el tejido cerebral puede ser más estable frente al hielo que la solución con la que se perfunde». **Confirma que un valor de solución es CONSERVADOR para tejido**, justo la dirección que la tanda 51 predijo. El sesgo **no** va hacia donde rompería los veredictos.
- **Abre una laguna nueva en `CWR_M22`, y ésta va en contra.** La fuente distingue lo que la red no distinguía: **~0.4 °C/min tras enfriamiento RÁPIDO** y **~1.0 °C/min tras enfriamiento LENTO**. Un objeto grande se enfría lento **por definición** (el centro de un cerebro humano va a 0.426 °C/min), así que la CWR relevante sería **~1.0, no 0.4**: recalentar es **×2.5 más difícil** de lo que el marco supone. **Efecto en C1:** el radio máximo recalentable por superficie pasa de **4.42 a 2.79 cm**; el veredicto clave del tronco (r ~15 cm) **se sostiene con ambos**. Valor sin mover (R2).

## 2026-09-27: tanda 55 (F82 y la fauna contra sus primarias; 94.3 → 94.7 %)
Siguen los PDF del usuario. **Dos cierres por primaria, uno por irrelevancia demostrada y una corrección que va en contra del marco.**

### F82 y L37 (+0.29 y +0.11)
- **F82 [P] → [V]** con **dos primarias leídas**, que sustituyen a las revisiones que la ficha citaba: *Investigative Radiology* («Ready for Routine…»), con medición **IN VIVO** en 10 voluntarios y mapas B1 de **82 sujetos en 3 centros**, que atribuye las inhomogeneidades a «**interferencias de radiofrecuencia y resonancias dieléctricas**» a **300 MHz**; y **arXiv 1911.05313**, que declara **εr = 64** para tejido a 7 T.
- **Verificada la aritmética de L37**: con λ = c/(f√εr) y εr = 64 salen **29.3 cm a 3 T y 12.5 cm a 7 T** (la ley afirmaba 30 y 13), y un cuerpo de 40 cm mide **1.37 y 3.20** longitudes de onda (afirmaba 1.3 y 3.1). Correcto.
- **L37 se cierra por IRRELEVANCIA DEMOSTRADA, no por encontrar el dato que faltaba.** La permitividad del tejido a 360 kHz **sigue sin fuente**, así que **se retira la cifra «λ ≈ 8.3 m»** que la ley afirmaba (exigía εr ≈ 1e4, que nadie aquí sostiene). Pero el **veredicto** no depende de ella: romper el régimen cuasiestático exigiría **εr ≥ 4.34e6**, es decir **×434** el valor supuesto. Con εr entre 64 y 1e5 el cuerpo mide entre **0.004 y 0.15** longitudes de onda. **Se sostiene el régimen, no la cifra.** Cálculo en `20_cotas/cota_L37_cuasiestatico.py`.

### Fauna: dos primarias y una corrección a la baja
- **F90 [V]** — Dausmann, Glos y Heldmaier 2009, *J Comp Physiol B* 179:345, **original paper**: consumo de O₂ y temperatura corporal de *Cheirogaleus medius* **en sus hibernáculos naturales**. **V09 → [V]**, apoyada ya en la primaria y no en los resúmenes de F19.
- **F91 [V]** — Niu et al., *Frontiers in Genetics*, **investigación original**: transcriptoma de *Protopterus annectens* tras 6 meses de estivación.
- **CORRECCIÓN QUE VA CONTRA EL MARCO:** V11 afirmaba una ventana de **3–4 AÑOS** para la estivación del pez pulmonado. **Ninguna de las dos primarias lo sostiene**: F91 dice que la estivación natural «lasts **seven or 8 months**, depending on the length of the dry season», y la revisión de estivación menciona episodios de 2 meses. La cifra venía de F19, que eran resúmenes. **Corregida a 7–8 meses: un orden de magnitud menos de lo que la red afirmaba.** Es el **cuarto** dato esta semana que no coincide con su fuente (tras F81/Mitz, F13 y hypo_case_min).
- **F19 sigue en [P]**: la parte de la **tortuga** no tiene primaria todavía, y F19 la sostiene vía `turtle22_h`.

### Dos asserts propios mal escritos, corregidos
- El primero prohibía la cadena «8.3 m» en L37 y saltó contra **la propia frase que retira la cifra**. Un assert que impide explicar por qué se retiró un dato es un mal assert.
- El segundo, de la tanda 49, exigía conservar F19 en V09 y V11. Su premisa era que F19 **era su única fuente**; ya no lo es. Sustituir un resumen por la primaria no es retirar una arista para subir el número, y así queda escrito.

### Leído y NO usado
`X_pnas_202423833.pdf` (PNAS 2025, origen evolutivo de los primates en ambientes fríos) menciona que los *Cheirogaleus* viven en climas fríos y que los primeros primates podrían haber entrado en torpor. **Es biogeografía evolutiva, no medición fisiológica: no cierra ningún nodo.**
