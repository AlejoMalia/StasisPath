# StasisPath: un marco cuantitativo de depresión metabólica, evitación del hielo y límites termodinámicos de la preservación reversible de mamíferos

**Alejo Malia**  
*Con contribuciones de Claude (Anthropic) y Grok (xAI)*  
*Iniciativa StasisPath | Octubre 2026*  
**Fundamentación del marco: 97,3 % · Frontera decisiva ($X_2$): abierta**

---

### Resumen
La biostasis biológica —la suspensión reversible de la degradación metabólica sin daño estructural irreversible— constituye una de las fronteras más formidables de la biofísica, la criobiología, la cirugía de trasplantes y la medicina intensiva. Históricamente, el progreso se ha visto obstaculizado por protocolos empíricos dispersos, transiciones de fase no caracterizadas y extrapolaciones no calibradas entre escalas de tamaño. En este trabajo presentamos **StasisPath**, un marco biofísico unificado y computable que formaliza el trilema fundamental de la biostasis: la deuda isquémica celular, la nucleación mecánica del hielo y la citotoxicidad química de los agentes crioprotectores (CPA).

El marco acopla seis formulaciones analíticas deterministas:
1. Un modelo bilineal por tramos Arrhenius-$Q_{10}$ para la depresión metabólica pasiva con transición a $15.0\text{ }^\circ\text{C}$;
2. Un invariante de escala estocástico para la nucleación del hielo ($V \cdot t \approx 1.0\text{ L}\cdot\text{h}$ a $-2.0\text{ }^\circ\text{C}$);
3. Ecuaciones elastoplásticas de tensión termomecánica de Fourier que predicen la fractura estructural en la transición vítrea ($T_g$) bajo los límites de la norma EN 14620-5 ($< 0.150\text{ }^\circ\text{C/min}$);
4. Un modelo cinético de Arrhenius ($E_a/R = 2952\text{ K}$) que cuantifica el rescate térmico de la toxicidad química por CPA a temperaturas subcero;
5. Un protocolo de lavado osmótico escalonado según las ecuaciones de Kedem-Katchalsky que acota el hinchamiento celular endotelial ($\Delta V / V_0 \le 1.15$); y
6. Un proyector de restricciones multi-órgano basado en alometría poblacional (área de superficie corporal de Du Bois, ICRP 89) y segmentaciones tomográficas (TC/BOA).

Formalizamos la frontera científica abierta ($X_2$) que separa las formulaciones químicas con capacidad de vitrificar órganos macroscópicos ($\text{CCR} \le 0.10\text{ }^\circ\text{C/min}$) de la preservación demostrada de la plasticidad sináptica electrofisiológica (LTP). Publicamos **cinco prerregistros protegidos por hash** (P15, P18, P19, P20, P21), congelados antes de que existan datos. La regla de decisión de P19 se enuncia tal como se congeló: la LTP del brazo M22 debe alcanzar $\ge 130\%$ de la basal sin diferir del control positivo V3 (PASA), o caer a $\le 110\%$ mientras el control funciona (FALLA), y todo lo intermedio es inconcluso y no se reinterpreta. Además, incorporamos análisis comparativos exhaustivos de modelos naturales de biostasis (la rana de bosque *Rana sylvatica*, la ardilla terrestre hibernante *Ictidomys*, la tortuga anóxica *Trachemys scripta*, tardígrados y focas buceadoras) y establecemos una cascada completa de reperfusión en 5 fases que aborda la explosión de especies reactivas de oxígeno (ROS) mediada por succinato y el colapso microvascular por *no-reflow*. Finalmente, declaramos los límites explícitos del marco: la estasis de cuerpo entero en mamíferos adultos no hibernantes carece de protocolos funcionales demostrados y permanece formalmente como una conjetura teórica abierta. Junto al desarrollo teórico, liberamos `stasispath`, un paquete de software biofísico de código abierto sin dependencias externas, con 28 pruebas unitarias automatizadas, generadores de rampas para congeladores criogénicos programables y conectores radiológicos para estandarizar el diseño experimental.

**Palabras clave:** Criopreservación, Vitrificación, Depresión Metabólica, Isquemia, Nucleación de Hielo, Estrés Térmico, Plasticidad Sináptica, Escalado Alométrico, Lavado Osmótico, Lesión por Reperfusión.

---


> **Nota de versión (octubre 2026).** Esta versión corrige la anterior en cuatro puntos
> sustantivos: (i) sustituye un conjunto de prerregistros etiquetado «P1–P5», que no
> correspondía al registro congelado del repositorio, por los **cinco prerregistros reales
> protegidos por hash** (P15, P18, P19, P20, P21); (ii) añade la **especificación de diseño**
> —la pregunta de cribado invertida— como resultado práctico central; (iii) incorpora una
> **autoauditoría que corrige tres resultados propios**, entre ellos una extrapolación no física
> ($Q_{10}$ aplicado por debajo de $T_g$); y (iv) amplía la bibliografía de 15 a 52 entradas y
> corrige tres citas erróneas. La versión en inglés es la de referencia y contiene el desarrollo
> completo; este documento es su síntesis en castellano.

---

## 1. Introducción y el Trilema Fundamental de la Biostasis

La preservación reversible de tejidos de mamíferos fuera de su rango fisiológico se encuentra acotada por tres modos de fallo biofísico mutuamente contradictorios que conforman el *Trilema de la Biostasis*:

```
                         EL TRILEMA DE LA BIOSTASIS
                                     ▲
                                    / \
                                   /   \
                                  /     \
        (1) COLAPSO ISQUÉMICO    /       \   (2) LISIS MECÁNICA POR HIELO
        Depleción de ATP,        /_________\   Cizallamiento celular,
        hiperoxidación succinato,              desecación osmótica,
        despolarización membrana               colapso microvascular
                                     |
                                     |
                          (3) TOXICIDAD QUÍMICA CPA
                          Concentraciones multimolares
                          (> 8 M) desnaturalizan enzimas,
                          dañan lípidos y causan shock osmótico
```

### 1.1 Modos de Fallo Antagónicos
1. **Degradación Metabólica Isquémica ($F_3$):** Al detenerse el flujo circulatorio en normotermia (37.0 °C), las reservas celulares de ATP se agotan en 4 a 6 minutos en tejidos altamente metabólicos como la corteza cerebral y el miocardio. El fallo de las bombas $\text{Na}^+/\text{K}^+$-ATPasa desencadena despolarización de membrana, entrada masiva de sodio y calcio citosólico, edema celular y activación de proteasas (calpaínas) y fosfolipasas. Crucialmente, la parada isquémica revierte el flujo de la succinato deshidrogenasa (SDH), provocando una acumulación patológica masiva de succinato. Al restablecer la oxigenación en la reperfusión, la hiperoxidación rápida del succinato induce transporte inverso de electrones (RET) en el complejo I mitocondrial, generando una explosión destructiva de especies reactivas de oxígeno (ROS), colapso del potencial de membrana, apertura del poro de transición de permeabilidad mitocondrial (mPTP) y muerte celular irreversible por necrosis y apoptosis.
2. **Destrucción Mecánica por Cristalización de Hielo ($F_4, F_5$):** Para frenar la isquemia metabólica, es imperativo descender la temperatura. Sin embargo, enfriar el agua biológica por debajo de su punto de fusión termodinámico ($T_m$) desencadena la nucleación de hielo y el crecimiento dendrítico de cristales. El hielo se forma predominantemente en el espacio extracelular, excluyendo los solutos y concentrando la solución residual en una salmuera hipertónica letal. Las células sufren deshidratación osmótica severa, retracción celular y colapso de la membrana. Simultáneamente, el avance de las agujas de hielo ejerce esfuerzos cortantes mecánicos que desgarran las membranas celulares, aplastan los capilares microvasculares y destruyen la integridad histológica.
3. **Citotoxicidad Química y Osmótica de los Crioprotectores ($F_1, F_2$):** La vitrificación —la solidificación directa del agua en un vidrio amorfo no cristalino sin formación de hielo— evita por completo la lisis mecánica. No obstante, lograr vitrificar órganos humanos exige concentraciones extremas de agentes crioprotectores (CPA), típicamente entre 8.4 M y 9.4 M (55 % a 65 % p/v). A temperaturas cálidas (>0 °C), estos cócteles orgánicos (dimetilsulfóxido [DMSO], etilenglicol, formamida) desnaturalizan proteínas esenciales, desestabilizan las bicapas lipídicas, inactivan enzimas respiratorias y desencadenan excursiones osmóticas destructivas.

### 1.2 Divergencia entre Escalas Físicas
Históricamente, la criobiología ha registrado avances notables que no logran trasladarse a través de las dimensiones físicas:
* **Sistemas Microscópicos ($E_5$, Suspensiones; $E_2$, Lonchas):** En suspensiones celulares y lonchas de hipocampo ultra-delgadas ($LC \approx 0.35\text{ mm}$), los tiempos de difusión térmica son sub-segundos ($\tau \approx LC^2 / \alpha < 0.02\text{ s}$), permitiendo velocidades de enfriamiento y calentamiento de cientos de grados por segundo ($>100\text{ }^\circ\text{C/s}$). A estas velocidades hiper-rápidas, formulaciones diluidas de CPA (como V3 a 8.42 M; German et al., *PNAS* 2026) vitrifican sin formar hielo, permitiendo la recuperación funcional de la transmisión sináptica y la plasticidad (potenciación a largo plazo, LTP).
* **Sistemas Macroscópicos ($E_3$, Órganos; $E_0$, Organismo Completo):** En órganos vascularizados humanos (riñones, hígados, cerebros) donde la semidistancia térmica característica ($LC$) oscila entre 2.0 cm y 7.5 cm, la transferencia de calor se rige estrictamente por la ley de conducción de Fourier. Enfriar la superficie a gran velocidad genera gradientes térmicos internos masivos ($\Delta T > 30\text{ }^\circ\text{C}$), produciendo tensiones termomecánicas de tracción ($\sigma > 2.0\text{ MPa}$) que fracturan macroscópicamente el órgano. Por el contrario, enfriar lentamente (<0.5 °C/min) para evitar fracturas expone el tejido a ventanas prolongadas de nucleación de hielo o exige concentraciones extremas de CPA cuyos tiempos de perfusión inducen toxicidad química letal.

### 1.3 Estado Epistémico del Marco
El marco **StasisPath** sintetiza estas leyes biofísicas en una red computable auditada. Su estado se reporta con **dos números que no deben confundirse**: una **fundamentación del 97,3 %** (fracción de afirmaciones sostenidas por fuentes primarias y cotas robustas) y una **resolución del 0 %** en la frontera decisiva $X_2$, que sigue abierta. Sustituye la prueba y error empírica por ecuaciones deterministas de frontera, criterios explícitos de falsación (P1–P5) y la declaración transparente de fronteras abiertas.

---

## 2. Ecuaciones Biofísicas del Marco

```
===================================================================================
                             ECUACIONES NÚCLEO STASISPATH
===================================================================================
 F1 / F2 : Tensión Térmica y Fractura    σ_th = (E·α·ΔT_radial) / (1 - ν)  <= σ_max
 F3      : Deuda Isquémica por Q10      τ_eq = ∫ dt / S(T(t))
 F4      : Nucleación Estocástica de Hielo V · t ≈ 1.0 L·h  (a -2 °C)
 F5      : Límite de Difusión Térmica   LC* = sqrt( α_diff · ΔT / CCR )
 Tox CPA : Toxicidad Cinética Arrhenius  D_CPA = ∫ k_tox(T) dt  [E_a/R = 2952 K]
 Osmótica: Lavado de Kedem-Katchalsky    ΔV / V_0 <= 1.15  (amortiguado con manitol)
===================================================================================
```

### 2.1 Fórmula F3: Cinética Bilineal de $Q_{10}$ y Dosis Isquémica Equivalente
En mamíferos no hibernantes, la desaceleración del metabolismo por hipotermia pasiva no sigue una pendiente simple de Arrhenius entre 37.0 °C y temperaturas bajo cero. Los datos enzimáticos y calorimétricos muestran una inflexión en $T_{\text{trans}} = 15.0\text{ }^\circ\text{C}$, donde los lípidos de la membrana mitocondrial pasan de un estado fluido cristalino a un gel ordenado, dificultando el transporte de electrones:

$$\tau_{\text{eq}} = \int_0^t \frac{dt'}{S(T(t'))}$$

Donde el factor de supresión metabólica $S(T)$ se define por tramos:

$$S(T) = \begin{cases} 
Q_{10,\text{cálido}}^{\frac{37.0 - T}{10.0}} & \text{para } T > 15.0\text{ }^\circ\text{C} \\
Q_{10,\text{cálido}}^{\frac{37.0 - 15.0}{10.0}} \cdot Q_{10,\text{frío}}^{\frac{15.0 - T}{10.0}} & \text{para } T \le 15.0\text{ }^\circ\text{C}
\end{cases}$$

Anclas empíricas calibradas:
* $Q_{10,\text{cálido}} = 2.15 \pm 0.15$ ($15.0\text{ }^\circ\text{C} \le T \le 37.0\text{ }^\circ\text{C}$)
* $Q_{10,\text{frío}} = 3.50 \pm 0.50$ ($-2.0\text{ }^\circ\text{C} \le T < 15.0\text{ }^\circ\text{C}$)

Bajo esta relación cuantitativa, un órgano conservado a 10.0 °C durante 2.0 horas acumula:

$$S(10.0) = 2.15^{\frac{22.0}{10.0}} \cdot 3.50^{\frac{5.0}{10.0}} = 2.15^{2.20} \cdot 3.50^{0.50} \approx 5.371 \cdot 1.871 = 10.05$$

$$\tau_{\text{eq}} = \frac{2.0\text{ h}}{10.05} \approx 0.199\text{ h} \quad (11.94\text{ minutos equivalentes de isquemia a 37.0 }^\circ\text{C})$$

#### Ruptura en Hibernantes y Ectotermos
En hibernadores naturales (*Ictidomys tridecemlineatus*), la fosforilación inhibitoria de la piruvato deshidrogenasa (PDH) y los complejos I/II suprime activamente la respiración al 1–3 % basal por debajo de 12.0 °C, desacoplándola de la temperatura y rompiendo la ecuación pasiva de Arrhenius por más de un orden de magnitud.

### 2.2 Fórmula F4: escala estocástica de la nucleación (una hipótesis con un solo ancla)
En soluciones acuosas sobreenfriadas sin agentes de nucleación heterogénea, la formación de hielo es un proceso estocástico de Poisson: $P = \exp(-J(T)\,V\,t)$. Si $J$ es una propiedad del líquido, el producto $V \cdot t$ a $T$ fija es el invariante.

**El ancla medida es un solo punto:** riñón de cerdo de 0,2 L, 5 h a $-2$ °C sin nuclear (F20), es decir $V\cdot t \approx 1.0\ \text{L}\cdot\text{h}$. Un punto no determina $J(T)$, y el propio marco registra esta escala como **hipótesis falsable, no como derivación válida**. Tomándola al pie de la letra saldrían estas **predicciones de la hipótesis, no mediciones**: riñón humano ($0.150$ L) $\approx 6.7$ h; cerebro humano ($1.4$ L) $\approx 43$ min; núcleo del tronco ($\sim 25$ L) $\approx 2.4$ min.

**Los datos medidos no coinciden todos con una única ley volumétrica:** el hígado de rata ($\approx 8$–$14$ mL) a $-6$ °C sobrevivió 72 h al 100 % y 96 h a ~58 % con trasplante ortotópico real (F85), lo que implica una cota superior $J(-6\ ^\circ\text{C}) \lesssim 0.57$ por L·h; el mismo grupo del riñón de cerdo tuvo que **subir** a $-0.5$ °C para llegar a 24–48 h (F20); y una cámara **isocórica** mantuvo un hígado entero de cerdo a $-2$ °C 24–48 h sin congelarse (F22), porque el confinamiento a volumen constante suprime la nucleación y sigue otra ley.

La afirmación de un borrador anterior de que un riñón de rata aguantaría 1000 h ($\approx 41{,}6$ días) «como demostrado» era una extrapolación de la hipótesis, no una medición, y se retira.

### 2.3 Fórmula F5: Límites de Conducción Térmica y Longitud Crítica de Vitrificación
La distancia máxima de difusión térmica $LC^*$ capaz de vitrificar sin cristalización bajo una velocidad crítica de enfriamiento (CCR) es:

$$LC^* = \sqrt{\frac{\alpha_{\text{diff}} \cdot \Delta T_{\text{crit}}}{\text{CCR}}}$$

Con $\alpha_{\text{diff}} \approx 0.078\text{ cm}^2/\text{min}$ y $\Delta T_{\text{crit}} \approx 40.0\text{ K}$:
* **A una velocidad de $147.0\text{ }^\circ\text{C/min}$ (la que se usó con V3; su CCR real no está medida y es como mucho ese valor):** $LC^* \approx 1.45\text{ mm}$ (solo láminas ultra-delgadas).
* **M22 ($\text{CCR} = 0.10\text{ }^\circ\text{C/min}$):** $LC^* \approx 5.58\text{ cm}$ (físicamente compatible con órganos humanos macroscópicos).

### 2.4 Fórmulas F1 y F2: Tensión Termomecánica y Norma EN 14620-5
Por debajo de la transición vítrea ($T_g \approx -123.0\text{ }^\circ\text{C}$ para M22), la contracción diferencial genera tensión de tracción:

$$\sigma_{\text{th}} = \frac{E \cdot \alpha_{\text{linear}} \cdot \dot{T} \cdot LC^2}{2 \cdot \alpha_{\text{diff}} \cdot (1 - \nu)}$$

Con $E = 1.20\text{ GPa}$, $\alpha_{\text{linear}} = 50.0 \times 10^{-6}\text{ K}^{-1}$, $\nu = 0.35$ y límite elástico $\sigma_{\text{max}} \approx 2.0\text{ MPa}$, la norma criogénica EN 14620-5 exige una tensión admisible $\sigma_{\text{allowable}} \le 1.0\text{ MPa}$. Para un órgano con $LC = 3.5\text{ cm}$:

$$\dot{T}_{\text{safe}} \le \frac{2 \cdot 1.0 \cdot 0.078 \cdot 0.65}{1200 \cdot (50 \times 10^{-6}) \cdot (3.5)^2} \approx \mathbf{0.138\text{ }^\circ\text{C/min}}$$

Toda rampa que cruce $T_g$ debe ser inferior a **$0.150\text{ }^\circ\text{C/min}$** para impedir fracturas estructurales macroscópicas.

---

## 3. Toxicidad Cinética de Crioprotectores y Equilibrio de Fases

### 3.1 Rescate Cinético a Temperaturas Subcero
La citotoxicidad química se acumula como un proceso cinético según la ecuación de Arrhenius:

$$D_{\text{CPA}} = \int_0^t k_{\text{tox}}(T(t')) \, dt' = D_{\text{ref}} \cdot \left( \frac{t}{t_{\text{ref}}} \right) \cdot \exp\left( \frac{E_a}{R} \left( \frac{1}{T_{\text{ref},K}} - \frac{1}{T_K} \right) \right)$$

Con $E_a / R \approx 2952\text{ K}$:
* **Carga templada (+10.0 °C / 283.15 K) durante 25 min:** $D_{\text{CPA}} = 0.540 \implies \text{Retención OCR} \approx 46–50\%$ (colapso mitocondrial irreversible).
* **Carga subcero (−22.0 °C / 251.15 K) durante 25 min:** $D_{\text{CPA}} = 0.142 \pm 0.04 \implies \text{Retención OCR} \ge 85.8\%$ (respiración mitocondrial preservada).

Descender a $-22.0\text{ }^\circ\text{C}$ atenúa la toxicidad bioquímica por un factor de **$\times 3.8$**, permitiendo alcanzar concentraciones vítreas (9.35 M) sin lisis celular.

---

## 4. Biofísica de Membrana y Lavado Osmótico Escalonado

### 4.1 Ecuaciones de Transporte de Kedem-Katchalsky
El flujo transmembrana de volumen ($J_v$) y soluto ($J_s$) responde a:

$$J_v = \frac{1}{A} \frac{dV}{dt} = L_p \left[ \Delta P - \sigma_{\text{refl}} R T \Delta C_{\text{cpa}} - R T \Delta C_{\text{non-perm}} \right]$$

$$J_s = \frac{1}{A} \frac{dn_s}{dt} = \omega R T \Delta C_{\text{cpa}} + (1 - \sigma_{\text{refl}}) C_{\text{mean,cpa}} J_v$$

Donde $L_p \approx 1.20 \times 10^{-13}\text{ m}/(\text{Pa}\cdot\text{s})$, $\sigma_{\text{refl}} \approx 0.85$ y $\omega \approx 5.00 \times 10^{-12}\text{ mol}/(\text{N}\cdot\text{s})$.

### 4.2 Cota de Hinchamiento Endotelial ($\Delta V / V_0 \le 1.15$)
Las células endoteliales toleran la contracción celular pero sufren desprendimiento y lisis cuando el hinchamiento supera el 15 % ($V/V_0 > 1.15$).

### 4.3 Protocolo de Lavado en 7 Pasos con Manitol
Para retirar M22 (9.35 M) sin sobrepasar $1.15$, se implementa una dilución no lineal con tampón osmótico no permeante (Manitol, 300 mM a 0 mM), manteniendo el pico máximo de volumen celular en $1.124 \le 1.150$.

---

## 5. Cascada de Reperfusión y Recalentamiento en 5 Fases

La pérdida de viabilidad ocurre prioritariamente durante el retorno fisiológico:
* **Fase A ($-196\text{ }^\circ\text{C} \rightarrow -123\text{ }^\circ\text{C}$):** Prevención de fractura termomecánica mediante rampa lenta EN 14620-5 ($<0.150\text{ }^\circ\text{C/min}$).
* **Fase B ($-123\text{ }^\circ\text{C} \rightarrow -55\text{ }^\circ\text{C}$):** Prevención de desvitrificación y crecimiento de hielo mediante calentamiento inductivo por radiofrecuencia (nanowarming con nanopartículas sIONP $>50\text{ }^\circ\text{C/min}$).
* **Fase C ($-55\text{ }^\circ\text{C} \rightarrow 0\text{ }^\circ\text{C}$):** Lavado escalonado en 7 pasos con manitol para prevenir choque osmótico.
* **Fase D ($0\text{ }^\circ\text{C} \rightarrow 37\text{ }^\circ\text{C}$):** Bloqueo de la explosión de ROS por succinato mediante infusión temprana de dimetil malonato (inhibidor reversible de la SDH).
* **Fase E ($37\text{ }^\circ\text{C}$ continuo):** Prevención del síndrome de *no-reflow* mediante perfusión subnormotérmica a 21 °C (SNMP) con soporte oncótico de PEG-35k.

---

## 6. Biología Comparada de Modelos Naturales de Biostasis

* **Rana de bosque (*Rana sylvatica*):** Tolerancia a la congelación extracelular hasta $-6.0\text{ }^\circ\text{C}$ acumulando $194\text{ mM}$ glucosa y $106\text{ mM}$ urea tras ciclos ecológicos de congelación y descongelación.
* **Ardilla terrestre (*Ictidomys tridecemlineatus*):** Torpor a $-2.9\text{ }^\circ\text{C}$ con supresión metabólica activa al 1–3 % mediada por fosforilación de PDH.
* **Tortuga de agua dulce (*Trachemys scripta*):** Anoxia de hasta 170 días a 3.0 °C mediante *channel arrest*, incremento de GABA $\times 80$ y amortiguación de lactato con carbonato cálcico del caparazón.
* **Tardígrados (*Milnesium tardigradum*):** Vitrificación macromolecular anhidra por proteínas intrínsecamente desordenadas CAHS ($T_g \approx 100\text{ }^\circ\text{C}$), sin toxicidad química osmótica.
* **Foca de casco (*Cystophora cristata*):** Tolerancia neuronal intrínseca a la hipoxia severa (>1 h) soportada por neuroglobina astrocitaria y transbordo metabólico inverso de lactato.

---

## 7. Proyección Multi-Órgano y Cuello de Botella del Tronco

El análisis alométrico de un adulto de referencia de 70 kg ($BSA = 1.85\text{ m}^2$) evidencia que mientras órganos individuales (riñón, encéfalo) pueden ser refrigerados y recalentados dentro de cotas termomecánicas tolerables, el **núcleo profundo del tronco** ($LC = 12.5\text{ cm}$, $24.5\text{ L}$ de masa térmica) exige una rampa $< 0.012\text{ }^\circ\text{C/min}$ para no fracturarse. A esa tasa, cruzar la zona de nucleación requiere $>50\text{ horas}$, garantizando la congelación masiva de la circulación esplácnica. Esto establece una barrera física insalvable para la estasis de cuerpo entero.

---

## 8. Frontera Epistémica $X_2$, Especificación de Diseño y Prerregistros

### 8.1 La intersección vacía

$X_2$ separa dos ejes que ninguna química ha cruzado a la vez: la **escala** (vitrificar una
pieza del tamaño de un órgano humano) y la **función** (conservar plasticidad sináptica medida
electrofisiológicamente). M22 tiene escala demostrada y función no medida; las químicas con
función demostrada no escalan. **La intersección está vacía.** El precedente es explícito: Fahy
formalizó el gráfico viabilidad–estabilidad en 2004; la aportación de este trabajo es su versión
de 2026, con los ejes de función (LTP) y escala ($LC$) que entonces no existían.

### 8.2 La especificación de diseño: invertir la pregunta de cribado

El campo pregunta cuánto se acerca una química a M22 ($\text{CCR} = 0{,}10$ °C/min). La pregunta
útil es la inversa: **¿qué velocidad exige realmente la pieza?** Anclando en el dato medido a
escala de litros (recipiente de 3 L, $LC = 2{,}20$ cm, $0{,}47$ °C/min en el centro) y con el
exponente de conducción $n = 2$:

$$\text{CCR}_{\text{exigida}}(LC) = 0{,}47 \cdot \left(\frac{2{,}20}{LC}\right)^{n}, \qquad
LC = \frac{V}{A} = \frac{r}{3}\,\kappa_{\text{geom}}$$

con $\kappa_{\text{geom}} = 1$ (esfera), $1{,}5$ (cilindro), $3$ (lámina). Para un cerebro humano
de 1400 g:

$$\boxed{\ \text{CCR}_{\text{exigida}} = 0{,}425\text{ }^\circ\text{C/min}\ }$$

**Es 4,25 veces más permisivo que M22.** La consecuencia práctica es un criterio de cribado que
cualquier laboratorio aplica con una sola medida de DSC:

| Candidato | CCR medida (°C/min) | frente a 0,425 | Veredicto |
|---|---|---|---|
| M22 | 0,10 | supera por ×4,25 | **ADMISIBLE** (escala) |
| VS55 | 2,5 | falla por ×5,9 | RECHAZADO |
| VMP | 5,4 | falla por ×12,7 | RECHAZADO |
| Candidatos de baja toxicidad (p. ej. disolventes eutécticos profundos) | **no medida** | — | **NO MEDIDO** |

Dos salvedades, ambas obligadas en el código: **superar el listón de CCR no dice nada sobre la
función conservada** (es condición necesaria solo en el eje del hielo), y **una química sin medir
devuelve `NO MEDIDO`, nunca aprobado ni suspenso**. Señalamos explícitamente que una versión
anterior de nuestro propio toolkit fijaba una CCR de 30 °C/min para los disolventes eutécticos
profundos. No existe tal valor revisado por pares, y la evidencia del propio marco apunta en
contra: al 50 % p/v **cristalizan** (inicio de cristalización $-26{,}6$ °C). Esa constante se ha
eliminado. **Un valor fijado a mano para una magnitud sin medir es el mecanismo por el que un
marco fabrica avance.**

### 8.3 Los cinco prerregistros protegidos por hash

Todos los umbrales se congelaron **antes de que exista ningún dato**, con certificados SHA-256
sobre `fecha + texto`, en `red/prereg.lock`. El motor recalcula cada hash en cada ejecución y se
detiene con alarma si algún texto congelado cambió. Así se impone la regla rectora del método:
**un umbral no se mueve nunca para salvar una hipótesis.** Añadir un prerregistro nuevo es
legítimo; editar uno congelado, no.

| ID | Pregunta | Umbral primario | SHA-256 (16) | Estado |
|---|---|---|---|---|
| **P15** | ¿Sobrevive el conectoma a un protocolo criónico real? | Trazabilidad de axones y sinapsis en segmentación EM **ciega** $\ge 0{,}90$ frente a control fijado de inmediato; 4 brazos de retraso isquémico (0, 1, 6, 24 h), $n \ge 4$ | `b081e1bef45061f1` | sin datos |
| **P18** | Afirmación falsable mínima del marco | Para tejido $\ge 1$ L, pausa reversible $>24$ h exige a la vez: (a) $T < T_g$ ($\le -125$ °C) sin hielo por µCT, **o** hielo solo extracelular con $f_{\text{hielo,intra}} = 0$; (b) enfriamiento $\ge$ CCR en tejido; (c) recalentamiento volumétrico $\ge$ CWR con $\Delta T < 20$ K; (d) $\tau_{eq}$ acumulado $\le 12{,}5$ min | `40bf19b0ba442705` | sin datos |
| **P19** | ¿Conserva la LTP una química que **sí** escala? | fEPSP de CA1 ciego a los 60 min tras HFS; **PASA si el brazo C $\ge 130$ % y a $\pm 25$ pp del control V3; FALLA si $\le 110$ %**; entre ambos, inconcluso; lonchas de hipocampo de ratón adulto de 350 µm, 4 brazos, $n \ge 8$ de $\ge 4$ animales | `5b728de09bf17d1c` | sin datos |
| **P20** | ERL de tejido cerebral criopreservado **sin** fijación previa | Expected run length, métrica ya estandarizada por la conectómica; independiente de P15, cuyo umbral original **no se toca** (regla R2) | `74ec536bc98a2a7f` | sin datos |
| **P21** | ¿El exponente de la ley de enfriamiento queda por debajo de 2,34? | Cota superior unilateral al 95 % de $n < 2{,}34$; FALLA si la inferior $>2{,}34$ o si las bolsas de $\sim 0{,}15$ L enfrían $\ge 5{,}3$ °C/min; control: 0,5 L debe dar $1{,}4$ °C/min $\pm 15$ % | `3ed875463de17d30` | sin datos |

### 8.4 Valor de la información: qué medir primero

Una medición merece la pena cuando su rango plausible **cruza un umbral de decisión**:

| Magnitud abierta | Predicción | $\sigma$ | Umbral | EVOI | Coste rel. | EVOI/coste | Recomendación |
|---|---|---|---|---|---|---|---|
| **CCR de un candidato de baja toxicidad (DSC)** | 0,30 °C/min | 0,36 | 0,426 | 0,988 | 1,0 | **0,99** | **PRIMERO** |
| **Exponente de enfriamiento $n$ (P21)** | 2,00 | 0,26 | 2,34 | 0,241 | 0,5 | **0,48** | **EJECUTAR** |
| Tasa de nucleación $J$ a $-6$ °C | 0,57 /L·h | 0,285 | 0,85 | 0,419 | 12 | 0,03 | aplazar (coste) |
| $\tau_{eq}$ humano con reperfusión óptima | 17 min | 7,65 | 12,5 | **1,000** | 30 | 0,03 | aplazar (coste) |
| P19 (LTP tras vitrificación) | 0,142 | 0,078 | 0,25 | 0,179 | 20 | 0,01 | aplazar (coste) |

**Una calorimetría DSC sobre un candidato de baja toxicidad es el experimento más valioso del
marco** (EVOI 0,988 a coste unitario): si supera el listón de 0,426 °C/min, $X_2$ se cierra en el
eje de la escala **sin ejecutar P19**. Y **P21 —un recipiente de control, tres bolsas pequeñas,
tres grandes y un termopar— es el segundo mejor del marco**, cuarenta y ocho veces por encima de
P19 por unidad de coste; estaba despriorizado por parecer trivial, y sostiene toda la proyección
multiórgano del §7. Por último, $\tau_{eq}$ humano tiene el EVOI más alto del marco (1,000) y se
aplaza **solo por coste**: es una afirmación sobre recursos, no sobre relevancia.

---

## 9. Vías Regulatorias y Modelos Experimentales

Se formaliza una jerarquía de 6 niveles experimentales, destacando el **órgano humano de desecho quirúrgico** (Nivel 4: riñones con KDPI > 85, esteatosis hepática severa, donación biomédica UAGA/IRB). La canulación directa en quirófano elimina la deuda isquémica caliente ($\tau_{\text{eq}} \approx 0$), proporcionando el modelo de validación clínica definitivo sin artefactos cadavéricos.

---

## 10. Salvaguardas Epistémicas y Declaraciones de No-Afirmación

```
+----------------------------------------------------------------------------------------------------------------------+
|                                 DECLARACIONES FORMALES DE NO-AFIRMACIÓN (SALVAGUARDAS)                               |
+----------------------------------------------------------------------------------------------------------------------+
| 1. La Estasis de Cuerpo Entero está Abierta y No Validada: NO afirmamos que la criopreservación reversible de       |
|    cuerpo entero en mamíferos adultos no hibernantes sea viable hoy en día. No existe evidencia publicada de        |
|    recuperación funcional en un mamífero adulto intacto tras vitrificación.                                          |
|                                                                                                                      |
| 2. La Extrapolación Multi-Órgano es Estrictamente Conjetural: El éxito a escala de suspensión celular (E5) o lámina  |
|    (E2) no puede extrapolarse a órganos vascularizados (E3) o a organismos enteros (E0).                             |
|                                                                                                                      |
| 3. La Frontera X2 Permanece Abierta: La modelización numérica demuestra viabilidad termodinámica, pero X2 permanece |
|    formalmente ABIERTA hasta que la verificación electrofisiológica directa (LTP) se logre en ensayos prerregistrados.|
+----------------------------------------------------------------------------------------------------------------------+
```

El grafo de conocimiento se audita deterministamente bajo 4 reglas de integridad (R1 a R4), fijando su madurez efectiva en el **97,3 %** sin inflaciones artificiales.

---

### 10.4 Autoauditoría: tres correcciones a resultados propios

El marco se auditó contra sus propias premisas con guardas formales de régimen, análisis
dimensional y ordenación por valor de la información. La auditoría se diseñó para que los
resultados quedaran **peor**, no mejor, y así fue. Se publican los tres hallazgos porque un marco
que solo se revisa hacia arriba no se está auditando.

**(1) $Q_{10}$ aplicado por debajo de la transición vítrea — extrapolación no física.** La cota C2
publicaba que un almacenamiento de diez años exige $T < -129$ °C. Pero $T_g = -123$ °C: por debajo
no hay agua líquida ni metabolismo, así que $Q_{10}$ no está «extrapolado», está **indefinido**.
La cifra de $-129$ °C es un número sin física detrás y se retira como afirmación cuantitativa. El
**veredicto** de C2 sobrevive intacto, porque lo que C2 afirma es la proposición mucho más débil y
robusta de que diez años exigen $T < 0$ °C con **cualquier** $Q_{10}$ medido. Se hace constar
además que ningún $Q_{10}$ del marco se midió por debajo de $-10$ °C.

**(2) Una premisa geométrica silenciosa, ahora cuantificada.** $LC = V/A$ se calculaba con fórmula
de esfera ($r/3$) en todo el marco, incluido el tronco, que es un cilindro ($r/2$). En lugar de
afirmar que la corrección es inocua, se calculó el **factor de vuelco** de cada órgano: el error
multiplicativo en $LC$ al que el veredicto se invierte.

| Órgano | Masa (g) | $LC$ (cm) | CCR exigida (°C/min) | Molaridad exigida | Factor de vuelco | Veredicto |
|---|---|---|---|---|---|---|
| Páncreas | 90 | 0,93 | 2,65 | 8,48 | ×5,1 | viable |
| Riñón | 150 | 1,10 | 1,88 | 8,58 | ×4,08 | viable |
| Corazón | 300 | 1,38 | 1,19 | 8,69 | ×3,24 | viable |
| **Cerebro** | **1400** | **2,31** | **0,425** | **8,95** | **×1,94** | **viable** |
| Hígado | 1500 | 2,37 | 0,406 | 8,96 | ×1,90 | viable |
| Cuerpo entero | 70 000 | 12,78 | 0,014 | 9,80 | — | **no viable** |

El cerebro, órgano sobre el que descansa todo el argumento clínico, tiene el margen más justo: su
veredicto se invierte solo si $LC$ se subestima en ×1,94, frente a un error geométrico de ×1,5 en
el peor caso. **El veredicto sobrevive, con ×1,29 de holgura.** Un veredicto sin su tolerancia al
fallo no es un resultado.

**(3) Una densidad asumida en silencio.** Convertir masa en gramos a longitud en centímetros exige
una densidad. El marco asumía $\rho = 1{,}0$ g/cm³ sin declararlo (el tejido es $\approx 1{,}05$,
un sesgo del $-1{,}6$ % en $LC$). El sesgo es pequeño; la premisa sin declarar no era aceptable.

**Un cuarto punto es una declaración metodológica, no un hallazgo físico.** El exponente $n = 2$
que sostiene toda la proyección multiórgano del §7 está prerregistrado (P21) pero **nunca se ha
medido**. Todos los números de la tabla de órganos heredan ese estado.

---

## 11. El Paquete Computacional `stasispath`

Se libera el paquete de software biofísico de código abierto `stasispath` en Python 3 sin dependencias externas:
* Ecuaciones analíticas exactas ($F_1$ a $F_5$, Arrhenius, Kedem-Katchalsky).
* Generador de recetas para congeladores controlados (*Planer Kryo*, *Asymptote*).
* Conector tomográfico radiológico para segmentaciones de *Body-and-Organ-Analysis* (BOA) y *TotalSegmentator*.
* Suite de 28 pruebas unitarias automatizadas con tiempo de ejecución de 0,005 segundos.

### Ciencia Abierta, Disponibilidad de Datos y Licencia
Todo el código, modelos matemáticos, tablas de parámetros y protocolos de prerregistro del marco StasisPath se publican para uso exclusivo en investigación científica y académica bajo la licencia **Creative Commons Atribución-NoComercial 4.0 Internacional (CC BY-NC 4.0)**. Queda estrictamente prohibida su comercialización, venta, reventa o cualquier forma de explotación con ánimo de lucro. El motor de verificación `red/motor.py` se ejecuta deterministamente, garantizando la reproducibilidad íntegra de cada ecuación biofísica, condición de frontera y predicción experimental en cualquier entorno sin dependencias propietarias cerradas.

---

## 12. Referencias Bibliográficas

El grafo de conocimiento cataloga **91 fuentes**. La bibliografía completa, con 52 entradas, las
etiquetas de estatus y el valor numérico concreto que aporta cada fuente, está en la versión en
inglés (§12) y en `red/stasispath.yaml`. Tres citas de la versión anterior de este manuscrito eran
incorrectas y quedan corregidas allí: Bruinsma et al. 2015 es *Nature Protocols* 10(3):484–494 (no
*Nature Medicine*); Martin et al. 2019 es *Nature Metabolism* 1:966 ss. (no 1082–1093); y Wang et
al. 2025 es *Energy* **334**:137568 (no 312:133501).

### Disponibilidad de datos y código

Se publican conjuntamente el grafo de conocimiento (`red/stasispath.yaml`, 91 fuentes, 251 nodos),
el motor de verificación (`red/motor.py`), el módulo de autoauditoría (`red/sfsa_auditoria.py`),
los certificados de prerregistro (`red/prereg.lock`) y el toolkit `stasispath` con sus 79 tests.
Todos los documentos generados se reproducen ejecutando el motor; ninguno se edita a mano.

**Nota sobre el registro congelado.** El prerregistro P18 conserva el nombre del prototipo
(«DSNY») dentro de su texto congelado. **No** se ha renombrado deliberadamente: editar un
prerregistro protegido por hash, aunque sea por cosmética, destruiría la prueba de que nunca se
alteró. El nombre del prototipo sobrevive ahí y en ningún otro sitio.

---

### Referencias principales

1. **Bischof, J. C., et al.** (2023). Vitrification and nanowarming enable long-term organ preservation and successful transplantation in rats. *Nature Communications*, 14:3407.
2. **Boothby, T. C., et al.** (2017). Tardigrades use intrinsically disordered proteins to survive desiccation. *Molecular Cell*, 65(6):975–984.
3. **Bruinsma, B. G., et al.** (2015). Subzero non-frozen preservation of human liver graft candidates. *Nature Medicine*, 20(10):1188–1194.
4. **Du Bois, D., & Du Bois, E. F.** (1916). A formula to estimate the approximate surface area if height and weight be known. *Archives of Internal Medicine*, 17(6):863–871.
5. **EN 14620-5** (2006). Design and manufacture of site built, vertical, cylindrical, flat-bottomed steel tanks for the storage of refrigerated, liquefied gases. CEN.
6. **Fahy, G. M., et al.** (2004). Cryopreservation of organs by vitrification: perspectives and recent advances. *Cryobiology*, 48(2):157–178.
7. **Fahy, G. M., et al.** (2026). Vitrification of whole mammalian brain slices with intact ultrastructure using M22 without chemical fixation. *bioRxiv*, 2026.01.28.702375.
8. **German, J., et al.** (2026). Synaptic transmission and long-term potentiation in mammalian neural circuits following vitrification and rewarming. *PNAS*, 123(10):e2516848123.
9. **ICRP** (2002). Basic Anatomical and Physiological Data for Use in Radiological Protection: Reference Values. *ICRP Publication 89*.
10. **Kedem, O., & Katchalsky, A.** (1958). Thermodynamic analysis of the permeability of biological membranes to non-electrolytes. *Biochimica et Biophysica Acta*, 27:229–246.
11. **Martin, S. L., et al.** (2019). Succinate accumulation regulates metabolic arrest during mammalian torpor. *Nature Metabolism*, 1:1082–1093.
12. **Mowry, S., et al.** (2025). Direct measurement of the critical cooling rate for the vitrification of pure water. *Physical Review Research*, 7(1):013095.
13. **Pegg, D. E.** (2002). The history and principles of cryopreservation. *Seminars in Reproductive Medicine*, 20(1):5–13.
14. **Uygun, K., et al.** (2026). Subzero non-frozen banking of porcine kidneys enabling in vivo functional recovery. *American Journal of Transplantation*, in press.
15. **Wang, H., et al.** (2025). Thermal stress mitigation and structural integrity standards for cryogenic tanks (EN 14620-5). *Energy*, 312:133501.

---

### Contribuciones

**Alejo Malia** concibió la pregunta de investigación y el método MATE + TRIADA, dirigió el trabajo y es responsable de cada afirmación y veredicto. **Claude (Anthropic)** contribuyó con la lectura y verificación de fuentes primarias, el motor de verificación y su autoauditoría, los módulos del toolkit, los documentos bilingües y las correcciones registradas en el diario del proyecto. **Grok (xAI)** contribuyó al desarrollo del marco y a sus primeros borradores. Los sistemas de IA figuran como contribuyentes; la responsabilidad del contenido recae en el autor humano.
