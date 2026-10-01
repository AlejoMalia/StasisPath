# TABLAS DE DISEÑO, COTAS Y HUECOS EXPERIMENTALES
## Guía Biofísica para Laboratorios de Criopreservación y Biostasis (StasisPath 2026)

Este documento estructura el marco teórico StasisPath en **dimensiones operativas**, con coordenadas cuantitativas medidas, cotas termodinámicas, modelos de toxicidad y huecos experimentales rigurosamente acotados. Proporciona a los laboratorios de criobiología, biofísica y trasplante las especificaciones exactas para optimizar protocolos y ensayar la frontera sin redundancia computacional ni ambigüedad metodológica.

---

> [!CAUTION]
> ### LÍMITES NUMÉRICOS Y FRONTERA EPISTÉMICA: CAJA DE "NO AFIRMAMOS"
> * **No afirmamos** que la estasis reversible de cuerpo entero en mamíferos adultos no hibernantes sea viable hoy en día, ni que exista protocolo alguno publicado capaz de lograrla.
> * **No afirmamos** que los éxitos a escala de célula ($E_5$) o loncha/microtejido ($E_2$) se traduzcan de forma trivial a órganos vascularizados ($E_3$) o a organismos completos ($E_0$). Toda extrapolación de órgano aislado a cuerpo entero es en la actualidad **estrictamente una conjetura teórica** no resuelta.
> * **No cerramos la frontera $X_2$** mediante simulación: el cierre de $X_2$ exige contrastación electrofisiológica directa in vitro con doble umbral (metabólico + plasticidad sináptica durable).

---

## 1. Escala Biológica: De la Célula al Organismo Completo

| Escala / Nivel | Masa / $LC$ Típica | Nivel Ontológico | Estado en el Marco | Órgano o Tejido Limitante | Daño Físico/Biológico Dominante | Protocolo Líder Verificado | Hueco Experimental Abierto |
|---|---|---|---|---|---|---|---|
| **Célula / Suspensión** | $< 10^{-6}\text{ g}$<br>($LC < 10\text{ }\mu\text{m}$) | $E_5$<br>(Función completa, clonogénica) | **[MEDIDO]** | Membrana plasmática | Lisis osmótica y nucleación intracelular | Congelación lenta (1 °C/min) con 10% DMSO o vitrificación ultrarrápida | Ninguno conceptual. Dominio resuelto. |
| **Loncha / Microtejido** | $10^{-3} - 10^{-2}\text{ g}$<br>($LC \approx 0.1–0.4\text{ mm}$) | $E_2$<br>(LTP, sinapsis activa) | **[MEDIDO]** | Neurona piramidal (CA1, DG) | Toxicidad química mitocondrial a concentraciones $> 8.4\text{ M}$ | **V3 (59 % p/v)** con carga subcero (−10 °C) y enfriamiento direccional a 130 °C/s (German et al., *PNAS* 2026) | Enfriamiento rápido obligatorio; no escala a órganos gruesos. |
| **Órgano Pequeño** | $1 - 15\text{ g}$<br>($LC \approx 0.5–1.0\text{ cm}$) | $E_3$<br>(Viabilidad post-trasplante) | **[MEDIDO]** | Corteza y microvasculatura renal | Desvitrificación en recalentamiento conductivo lento | **Nanowarming inductivo** con sIONPs en riñón de rata (5/5 supervivencia a 100 días, Bischof 2023); sobreenfriamiento a −6 °C (Bruinsma 2015) | Distribución homogénea de nanopartículas y lavado vascular completo sin agregados. |
| **Órgano Grande** | $150 - 1500\text{ g}$<br>($LC \approx 1.5–3.9\text{ cm}$) | $E_3$ (parcial en cerdo)<br>$E_0$ (en humano) | **[ACOTADO]** | Médula interna renal / Endotelio vascular | Conducción térmica lenta (Fourier $C_3$), toxicidad de CPA por tiempo de difusión | **Congelación parcial a −15 °C** por 10 días (Uygun 2026, autotrasplante in vivo porcino con orina); **M22 a −22 °C/−45 °C** (Fahy 2004, 8/8 supervivencia) | **X2**: Demostrar electrofisiología activa (LTP durable) en tejido neural con CPA de baja CCR ($\le 0.43\text{ }^\circ\text{C/min}$). |
| **Multi-Órgano / Bloque** | $5 - 15\text{ kg}$<br>($LC \approx 4.0–6.0\text{ cm}$) | $E_1$<br>(Integridad histológica) | **[ACOTADO]** | Endotelio pulmonar y barrera hematoencefálica | Fenómeno de *no-reflow*, edema vasogénico, heterogeneidad de difusión entre parénquimas | Perfusión escalonada subnormotérmica (SNMP) y vehículos oncóticos (PEG 35k) | Perfusión simultánea de órganos con perfiles osmóticos dispares sin lisis endotelial. |
| **Organismo Completo** | $70\text{ kg}$<br>($LC \approx 7.5\text{ cm}$ en tronco) | $E_0$<br>(Preservación estructural) | **[ABIERTO]** | Centro del tronco / Masa esplácnica profunda | Imposibilidad de enfriar el centro sin cruzar la toxicidad de molécula pequeña ($F_2$ exige $>9.5\text{ M}$); fractura mecánica ($C_1$) | Crioprotección de campo post-mortem (de Wolf 2025; Alcor P-19) | **No existe ningún protocolo de estasis total reversible en mamífero adulto no hibernante.** |

---

## 2. Toxicidad Comparada de Crioprotectores (CPA)

Esta tabla resume el perfil operativo de los principales agentes vitrificantes evaluados en la literatura biofísica frente a la cota experimental pendiente de caracterización en laboratorio propio:

| Formulación CPA | Molaridad Típica (M) | Conc. (% p/v) | $\text{CCR}$ de Referencia | Toxicidad Relativa Observada | Nota Mecanística y Limitación | Dato Propio en Lab StasisPath |
|---|---|---|---|---|---|---|
| **DP6** | ~6.0 M | ~38.8 % w/w | ~40.0 °C/min | **Baja-Moderada** | Requiere calentamiento ultrarrápido (>180 °C/min) para evitar devitrificar. | Pendiente ensayo comparativo en loncha |
| **VS55 (VS41A)** | 8.4 M | 55.0 % | ~2.5 °C/min | **Severa** | Toxicidad endotelial y despolarización irreversible; no apto para perfusión normotérmica. | Registrado en nodo $F_3$ / $F_{65}$ |
| **VMP** | 8.4 M | 55.0 % | ~5.4 °C/min | **Moderada** | Solución puente con ice-blockers (X-1000/Z-1000); tolera perfusión rápida a −3 °C. | Registrado en nodo $F_1$ |
| **V3** | 8.42 M | 59.0 % | ~147.0 °C/min | **Tolerable a subcero** | Preserva LTP (German 2026), pero CCR inviable para órganos mayores a $0.5\text{ mm}$. | Validado en nodo $F_{46}$ / $F_{71}$ |
| **M22** | 9.345 M | 64.8 % | **0.10 °C/min** | **Alta a >0 °C / Baja a −22 °C** | Vitrifica a escala de órganos ($LC^* > 3.5\text{ cm}$); daño mitigado cinéticamente por frío. | **P19: Pendiente caracterización fEPSP/LTP** |
| **NADES** | n/d (mezclas de masa molar variable) | 50 % p/v | **> 30 °C/min (MEDIDA: cristalizan en DSC a 30 °C/min)** | **Limitada: el propio artículo fija el 50 % p/v como techo por toxicidad y viscosidad** | Eutécticos naturales: protegen líneas celulares por inmersión directa en N₂, pero cristalizan a 30 °C/min y no vitrifican volúmenes grandes. Su «vitrificación» es inmersión de un criovial. | Registrado en nodo $F_{80}$ |
| **Proteínas CAHS** | ~0.0006 M | 1.5 % (15 g/L) | Gel in situ | **Nula** | Vitrificación macromolecular por arresto estéreo-espacial; sin toxicidad osmótica. | Registrado en nodo $F_{74}$ |

---

## 3. Matriz de Reperfusión y Recalentamiento: Mecanismos por Fase Crítica

El fallo de viabilidad en criopreservación no solo ocurre durante el enfriamiento, sino predominantemente en las transiciones de fase y retorno fisiológico:

| Fase del Proceso | Rango Térmico | Fenómeno Crítico Dominante | Causa Biofísica / Bioquímica | Daño Celular / Fisiológico | Estrategia de Mitigación Validada |
|---|---|---|---|---|---|
| **Fase A: Recalentamiento Criogénico I** | $-196\text{ }^\circ\text{C} \rightarrow T_g$ (−123 °C) | **Fractura Termomecánica** | Contracción y dilatación diferencial volumétrica ($\sigma_{\text{th}} \approx \frac{E \cdot \alpha \cdot \Delta T}{1 - \nu}$) | Roturas macroscópicas y seccionamiento de lechos vasculares | Control de velocidad ultralento ($< 0.150\text{ }^\circ\text{C/min}$) en la vecindad de $T_g$ (Wang 2025; EN 14620-5) |
| **Fase B: Recalentamiento Criogénico II** | $T_g \rightarrow T_m$ (−123 °C a −55 °C) | **Desvitrificación y Recristalización** | Crecimiento descontrolado de núcleos de hielo metaestables por cinética térmica | Lisis celular mecánica completa del parénquima | **Nanowarming volumétrico inductivo** por radiofrecuencia con sIONPs (>50 °C/min homogéneo, Bischof 2023) |
| **Fase C: Lavado de CPA (Washout)** | −22 °C $\rightarrow$ 0 °C | **Shock Osmótico y Edema** | Retirada abrupta de solutos externos con salida/entrada rápida de agua por desequilibrio químico | Lisis osmótica de membrana y desprendimiento endotelial (elevación masiva de LDH) | Dilución escalonada no lineal mediada por solutos impermeables de soporte osmótico (**Manitol 300 mM**) |
| **Fase D: Reoxigenación y Flujo** | 0 °C $\rightarrow$ 37 °C | **Explosión de ROS por Succinato** | Acumulación de succinato durante la fase de parada; hiperoxidación súbita en complejo II mitocondrial al inducir flujo normotérmico | Estrés oxidativo fulminante, peroxidación de cardiolipina y apertura de poros mPTP | Infusión de inhibidores reversibles de la succinato deshidrogenasa (**Malonato de dimetilo**) en reperfusión temprana |
| **Fase E: Reperfusión Microvascular** | 37 °C continuo | **Síndrome de No-Reflow** | Edema de pericitos y endoteliocitos con colapso de la luz capilar microvascular e hiperadhesión plaquetaria | Necrosis isquémica post-reperfusión a pesar de perfusión macrovascular adecuada | Protocolo de perfusión subnormotérmica escalonada (SNMP a 21 °C $\rightarrow$ 37 °C) con coloides oncóticos (**PEG 35k**) |

---

## 4. Dominios de Regulación Metabólica (Más Allá del $Q_{10}$)

| Mecanismo de Supresión | Rango Térmico Activo | Depresión Metabólica Lograda | ¿Obedece a Arrhenius ($Q_{10}$)? | Mecanismo Molecular Clave | Límite Fisiológico de Ruptura |
|---|---|---|---|---|---|
| **Hipotermia Pasiva (Mamífero no hibernante)** | 37 °C $\rightarrow$ 10 °C | 50 % cada 10 °C ($Q_{10} = 2.0–2.3$ a $>15\text{ }^\circ\text{C}$; $Q_{10}=3.5$ a $<15\text{ }^\circ\text{C}$) | **SÍ** (cinética térmica enzimática) | Desaceleración pasiva de reacciones enzimáticas; colapso temprano del complejo V | Paro cardíaco por fibrilación ventricular a $<28\text{ }^\circ\text{C}$; $\tau_{\text{eq}} \le 45\text{ min}$ a 10 °C |
| **Torpor de Hibernante (*Ictidomys*, *Cheirogaleus*)** | 12 °C $\rightarrow$ −2 °C | Hasta el 1–3 % de la tasa basal de eotermia | **NO** (Dominio de ruptura de $F_3$: tasa plana entre 0 y 12 °C) | Inhibición activa por fosforilación reversible de complejos I/II; conmutación a sustrato puramente lipídico (CR = 0.70) | Límite fijado por disponibilidad de combustible no lipídico y nitrógeno ($L_{28}$); termogénesis reactiva si $T < 0\text{ }^\circ\text{C}$ |
| **Anoxia de Ectotermo (*Trachemys scripta*)** | 20 °C $\rightarrow$ 3 °C | 10–20 % a 20 °C;<br>**0.5 % a 3 °C** (<0.01 % de mamífero) | **NO** (Channel arrest regulado) | Despolarización suprimida, GABA cerebral aumentado $\times 80$, tamponamiento masivo de lactato por carbonato del caparazón | Capacidad tampón del esqueleto mineral; inviable en mamíferos sin caparazón por acidosis láctica letal |
| **Ahorro Cerebral Ontogénico (Feto/Neonato)** | 37 °C (feto)<br>30 °C (neonato) | Caída selectiva de demanda cerebral con bradicardia (25–60 %) | Parcialmente | Receptores de adenosina $A_1$, apertura de canales $K_{\text{ATP}}$, preservación selectiva de flujo carotídeo | Maduración postnatal de la excitotoxicidad por glutamato (se pierde en semanas tras nacer) |
| **Torpor Sintético Farmacológico** | 37 °C $\rightarrow$ 32–34 °C | Reducción de tasa metabólica del 30–50 % | Regulado farmacológicamente | Estimulación de neuronas Q hipotalámicas, agonistas de adenosina ($A_1R$, CHA) | Requiere soporte ventilatorio mecánico y nutrición parenteral continua (Bradford NASA NIAC) |

---

## 5. Matriz de Implementación Experimental y Regulatoria

| Nivel Experimental | Sujeto / Modelo | Marco Regulatorio y Legal | Nivel de Madurez (TRL) | Coste / Complejidad | Ventaja Clave y Qué Acredita |
|---|---|---|---|---|---|
| **In Vitro / Loncha** | Cultivo primario, cortes de hipocampo murino | Comités éticos de experimentación animal estándar (IACUC) | TRL 2–3 | Bajo / Rápido | Toxicidad molecular pura, viabilidad sináptica (LTP, fEPSP), respiración mitocondrial (OCR). |
| **Órgano de Roedor** | Riñón o hígado de rata | Comités IACUC estándar | TRL 4 | Medio | Trasplante vascular ortotópico real in vivo; supervivencia y función orgánica a 100 días. |
| **Órgano Porcino In Vivo** | Cerdo Yorkshire (30–50 kg) | Normativa preclínica mayor de trasplante animal | TRL 5 | Alto | Modelo traslacional idéntico en escala a órganos humanos; filtrado glomerular y producción de orina in vivo. |
| **Órgano Humano de Desecho Quirúrgico / Donante No Trasplantable** | Riñón / hígado / biopsias humanas no aptas para injerto (p. ej. KDPI > 85, esteatosis severa, tumorectomías parciales) | Aprobación de IRB local + Consentimiento de donación para investigación biomédica (UAGA / Ley de Trasplantes) | **TRL 3–5** | **Medio-Alto** / Acceso viable vía OPO/Banco | **Puente crítico entre roedor y clínica**: vasculatura humana real sin artefactos cadavéricos. $\tau_{\text{eq}}$ excelente si se canula inmediatamente en quirófano. Permite perfusión ex vivo en normotermia. |
| **Ensayos Clínicos de Emergencia** | Pacientes humanos de cirugía cardiovascular o trauma exanguinante | Aprobación FDA/EMA bajo excepción de consentimiento informado de emergencia (EFIC, 21 CFR 50.24) | TRL 6–7 | Extremo | Hipotermia terapéutica ultracorta (<45 min en DHCA; minutos en EPR). No apto para almacenamiento prolongado. |
| **Preservación Cadavérica de Campo** | Donación anatómica post-mortem legal de cuerpo entero | Uniform Anatomical Gift Act (UAGA) | TRL 1–2 | Logísticamente complejo | Perfusión de campo en cuerpo completo; penalizado por isquemia caliente post-paro ($\tau_{\text{eq}} \gg 10\text{ min}$) y retraso médico-legal. |

---

## 6. Predicciones Falsables Concretas para Laboratorio

**La Predicción 1 es P19, un preregistro congelado y protegido por hash** (`red/prereg.lock`). **Las Predicciones 2 a 5 son hipótesis de laboratorio exploratorias, NO preregistradas.** Todas llevan criterios cuantitativos de falsación:

### Predicción 1 (Experimento P19, preregistro congelado: ¿conserva la LTP un hipocampo vitrificado con una química que sí escala?)
* **Condición de ensayo**: lonchas de hipocampo de ratón adulto de 350 µm; cuatro brazos, $n \ge 8$ lonchas de $\ge 4$ animales por brazo, registro ciego: **(A)** control sin vitrificar · **(B)** V3 (réplica de F46, control positivo) · **(C)** M22 a su concentración de trabajo (precarga con VMP a 0 °C, M22 a −22 °C, lavado simultáneo al calentamiento) · **(D)** carga y descarga de M22 sin enfriar.
* **Variable primaria**: LTP en SC–CA1 a los 60 min tras HFS (100 Hz, 1 s), como % del fEPSP basal.
* **Regla de decisión (congelada, no se reinterpreta)**:
  1. **PASA** si el brazo C alcanza $\ge 130\ \%$ y no difiere de B (IC 95 % de la diferencia dentro de ±25 puntos porcentuales).
  2. **FALLA** si C $\le 110\ \%$ mientras B $\ge 130\ \%$.
  3. Entre 110 y 130 %, o con B fallido: **inconcluso**.
  4. **Control de calidad**: B debe replicar F46 (138.1 %) dentro de ±20 puntos porcentuales; si no, el experimento no es interpretable y se repite antes de leer C.
* **Diagnóstico del brazo D**: si D falla igual que C, el daño es **toxicidad química** y hay que rediseñar el CPA; si D pasa y C falla, el daño es **térmico o de desvitrificación**.
* **Medida secundaria (no es un umbral)**: la respiración basal (OCR). La derivación de Arrhenius predice daño $D_{\text{CPA}} = 0.142$ en el brazo C (retención de OCR ≈ 86 %); un daño $> 0.25$ refutaría esa **derivación** (contradicción I1), no P19.
* *Nota editorial*: una versión anterior de esta guía fijaba un «doble umbral» (OCR $\ge 85\ \%$ y LTP $\ge 120$–$150\ \%$). No coincidía con el preregistro congelado y se ha sustituido por la regla de arriba.

### Predicción 2 (exploratoria, no preregistrada; Fórmula F4: límite temporal de sobreenfriamiento por nucleación estocástica)
* **Condición de ensayo**: volumen biológico de $1.5\text{ L}$ (equivalente a hígado humano adulto) sometido a sobreenfriamiento a −2 °C sin agentes antinucleantes específicos.
* **Cálculo a partir de una hipótesis de un solo ancla ($V \cdot t \approx 1.0\text{ L}\cdot\text{h}$; el marco la registra como hipótesis falsable, no como derivación válida)**:
  $$t_{\text{máx sin nucleación}} \le 40\text{ minutos}$$
* **Criterio de falsación**: si el órgano permanece $> 3\text{ horas}$ a −2 °C en 10 repeticiones consecutivas sin congelarse, el invariante estocástico $V \cdot t$ queda **refutado** a favor de un régimen dominado por nucleación heterogénea interfacial del contenedor.

### Predicción 3 (exploratoria, no preregistrada; Fórmula F1/F2: umbral de fractura térmica en órgano grande)
* **Condición de ensayo**: enfriamiento pasivo por convección de un órgano con $LC \ge 3.9\text{ cm}$ perfundido con M22 al atravesar $T_g$ (−123 °C).
* **Cálculo analítico**: a velocidades $> 0.150\text{ }^\circ\text{C/min}$, el gradiente radial genera tensiones térmicas $\sigma_{\text{th}} > \sigma_{\text{fractura}} \approx 2.0\text{ MPa}$.
* **Criterio de falsación**: la ausencia reproducible de microfracturas vasculares/tisulares detectadas por tomografía computarizada criogénica o criomacroscopía a tasas $> 1.0\text{ }^\circ\text{C/min}$ refuta el límite termomecánico de Wang/EN 14620-5 para matrices vítreas tisulares.

### Predicción 4 (exploratoria, no preregistrada; reperfusión post-P19 in vitro: cinética de recuperación funcional)
* **Condición de ensayo**: lonchas de hipocampo expuestas al protocolo P19 completo (M22 a −22 °C, lavado con manitol) sometidas a superfusión continua con ACSF normotérmico oxigenado ($95\%\text{ O}_2 / 5\%\text{ CO}_2$) a 32 °C durante 60 minutos.
* **Cálculo analítico derivado**: la eliminación del CPA no debe inducir lisis secundaria por estrés osmótico residual ni cascada necrótica fulminante.
* **Criterio de falsación**:
  * A los 30 minutos de reperfusión normotérmica continua, el $\text{OCR}$ mitocondrial debe ser $\ge 70\text{ \%}$ del valor medido inmediatamente tras el lavado.
  * No debe observarse fallo progresivo o extinción de la amplitud del potencial de acción de población (fEPSP) entre el minuto 15 y el minuto 60 de registro continuo.
  * Una caída progresiva de fEPSP $> 50\text{ \%}$ en este intervalo con incremento continuo de LDH en el baño falsaría la viabilidad del protocolo de lavado escalonado.

### Predicción 5 (exploratoria, no preregistrada; escala de nucleación por volumen en órgano renal: $V \cdot t \approx 1.0\text{ L}\cdot\text{h}$)
* **Aviso**: el dato de 0.2 L y 5 h es exactamente el ancla de la hipótesis; un acierto aquí es una **réplica**, no una prueba independiente.
* **Condición de ensayo**: riñones de cerdo ($V \approx 0.15–0.20\text{ L}$) sobreenfriados a −2 °C en medio libre de núcleos de hielo exógenos.
* **Cálculo analítico derivado**:
  $$t_{\text{estabilidad teórica}} \approx \frac{1.0\text{ L}\cdot\text{h}}{0.20\text{ L}} = 5.0\text{ horas}$$
* **Criterio de falsación y diagnóstico interfacial**:
  * Si la estabilidad promedio observada en 5 ensayos consecutivos se sitúa en $5.0 \pm 1.5\text{ h}$, el modelo estocástico volumétrico queda verificado.
  * Si el riñón nuclea sistemáticamente en $t < 1.0\text{ hora}$ en el mismo contenedor donde volúmenes idénticos de solución salina permanecen sobreenfriados $> 6\text{ h}$, queda demostrado que la nucleación **no está gobernada por el volumen intrínseco**, sino por heterogeneidad de superficie (cápsula renal, catéteres o sellado vascular), orientando el diseño de lab hacia agentes de pasivación superficial.

---
*Documento biofísico de especificación de laboratorio integrado en el sistema analítico de la Red StasisPath — Versión 2.5 (2026).*
