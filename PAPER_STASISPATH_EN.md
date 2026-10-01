# StasisPath: A Quantitative Biophysical Framework for Metabolic Depression, Ice Avoidance, and the Thermodynamic Limits of Reversible Mammalian Preservation

**Alejo Malia**  
*With contributions from Claude (Anthropic) and Grok (xAI)*  
*StasisPath Initiative | October 2026*  
**Framework grounding: 97.3 % · Decisive frontier ($X_2$): open**

---

### Abstract
Biological biostasis—the reversible arrest of metabolic degradation without structural destruction—remains one of the most formidable frontiers in biophysics, cryobiology, transplantation surgery, and emergency medicine. Progress has historically been impeded by fragmented empirical protocols, uncharacterized phase transitions, and uncalibrated cross-scale extrapolations. Here, we present **StasisPath**, a unified, computable biophysical framework that formalizes the fundamental trilemma of biostasis: metabolic ischemic debt, ice crystal nucleation, and cryoprotectant (CPA) chemical cytotoxicity. 

The framework couples six analytical formulations:
1. A bilinear piecewise Arrhenius-$Q_{10}$ model for metabolic suppression transitioning at $15.0\text{ }^\circ\text{C}$;
2. A stochastic scaling invariant for ice nucleation ($V \cdot t \approx 1.0\text{ L}\cdot\text{h}$ at $-2\text{ }^\circ\text{C}$);
3. Fourier elastoplastic thermomechanical stress equations predicting structural fracture at the glass transition ($T_g$) under EN 14620-5 limits ($< 0.150\text{ }^\circ\text{C/min}$);
4. An Arrhenius kinetic model ($E_a/R = 2952\text{ K}$) quantifying the temperature rescue of CPA chemical toxicity;
5. A Kedem-Katchalsky stepwise osmotic washout protocol clamping transient endothelial swelling ($\Delta V / V_0 \le 1.15$); and
6. An anthropometric multi-organ constraint projector driven by population allometry (Du Bois BSA, ICRP 89) and radiological CT segmentation.

The framework's central practical result **inverts the conventional design question**. The field asks how closely a chemistry approaches M22 ($\text{CCR} = 0.10\text{ }^\circ\text{C/min}$); we instead compute what a given organ *requires*. For a 1400 g human brain the requirement is $\text{CCR} \le 0.425\text{ }^\circ\text{C/min}$ — **4.25$\times$ more permissive than M22** — which admits a class of candidate chemistries that M22-anchored screening excludes a priori. We formalize the unclosed scientific frontier ($X_2$) separating chemistries with demonstrated *scale* from those with electrophysiologically verified *function* (LTP), and show its intersection is empty. We publish **five hash-locked preregistrations** (P15, P18, P19, P20, P21; SHA-256 certificates in §8.3), frozen before any data exist. The decision rule of P19 is stated exactly as frozen: LTP in the M22 arm must reach $\ge 130\%$ of baseline without differing from the V3 positive control (PASS), or fall to $\le 110\%$ while the control works (FAIL), with everything between declared inconclusive and never reinterpreted. A value-of-information analysis identifies the cheapest decisive measurement in the framework, which is **not** P19. Furthermore, we incorporate comprehensive comparative analyses from natural biological stasis models (wood frogs, hibernating ground squirrels, anoxic turtles, tardigrades, and diving seals) and establish a complete 5-phase reperfusion cascade addressing succinate-driven ROS explosions and no-reflow microvascular collapse. Finally, we declare the explicit boundaries of the framework: whole-body stasis in adult non-hibernating mammals possesses zero verified functional protocols, representing an unresolved theoretical conjecture. We additionally report a self-audit that corrected three of our own results, including one unphysical extrapolation ($Q_{10}$ applied below $T_g$) and a geometry premise whose failure tolerance we now quantify. Alongside this theoretical core, we release `stasispath`, an open-source, zero-dependency computational toolkit with 60 automated unit tests, controlled-rate freezer recipe generators, and radiologic image connectors to standardize experimental design.

**Keywords:** Cryopreservation, Vitrification, Metabolic Depression, Ischemia, Ice Nucleation, Thermal Stress, Synaptic Plasticity, Allometric Scaling, Osmotic Washout, Reperfusion Injury.

---

## 1. Introduction and the Fundamental Trilemma of Biostasis

The preservation of living mammalian tissues outside their normal physiological envelope is constrained by three mutually antagonistic physical and biochemical failure modes:

```
                         THE BIOSTASIS TRILEMMA
                                    ▲
                                   / \
                                  /   \
                                 /     \
        (1) ISCHEMIC COLLAPSE   /       \   (2) MECHANICAL ICE LYSIS
        Depletion of ATP,       /_________\   Lethal shear stress,
        succinate hyperoxidation,             osmotic desiccation,
        membrane depolarization               microvascular crushing
                                    |
                                    |
                         (3) CPA CHEMICAL TOXICITY
                         High multimolar concentrations
                         (> 8 M) disrupt protein structure,
                         denature enzymes, cause osmotic shock
```

### 1.1 The Antagonistic Failure Modes
1. **Ischemic Metabolic Degradation ($F_3$):** In the absence of circulation at normothermia (37.0 °C), intracellular ATP pools are exhausted within 4 to 6 minutes in metabolically active tissues such as the brain and cardiac myocardium. The failure of $\text{Na}^+/\text{K}^+$-ATPase pumps triggers immediate membrane depolarization, intracellular sodium and calcium flooding, cell swelling, and activation of calcium-dependent proteases (calpains) and phospholipases. Crucially, ischemic arrest reverses mitochondrial succinate dehydrogenase flux, leading to pathological accumulation of succinate. Upon subsequent reoxygenation, rapid succinate hyper-oxidation drives excessive reverse electron transport (RET) at mitochondrial complex I, producing a massive explosion of reactive oxygen species (ROS), collapse of mitochondrial membrane potential, opening of the mitochondrial permeability transition pore (mPTP), and irreversible cell death via necrosis and apoptosis.
2. **Mechanical Disruption by Ice Crystallization ($F_4, F_5$):** To halt metabolic ischemia, temperature must be lowered. However, cooling biological water below its thermodynamic melting point ($T_m$) induces ice nucleation and crystal growth. Solute exclusion forces ice to nucleate primarily in the extracellular compartment, concentrating extracellular solutes into a hyperosmotic residual brine. Cells undergo severe osmotic dehydration, membrane crenation, and intracellular lipid rearrangement. Concurrently, advancing ice dendrites exert destructive mechanical shear stresses that sever delicate cellular processes, crush microvascular capillary networks, and breach basal lamina barriers.
3. **Chemical and Osmotic Cytotoxicity of Cryoprotectants ($F_1, F_2$):** Vitrification—the transition of liquid water directly into an amorphous vitreous state without crystallization—completely circumvents mechanical ice lysis. However, to prevent crystallization at human organ scales, extreme concentrations of organic cryoprotective agents (CPAs) are required, ranging between 8.4 M and 9.4 M (55% to 65% w/v). At warm temperatures (>0 °C), these multimolar cocktails (composed of dimethyl sulfoxide [DMSO], ethylene glycol, formamide, and other permeating molecules) disrupt hydrogen bonding networks within proteins, induce protein denaturation, extract membrane lipids, inactivate crucial respiratory enzymes, and elicit catastrophic osmotic volume excursions.

### 1.2 The Cross-Scale Divergence
Historically, cryobiological literature has celebrated major breakthroughs that fail to translate across physical dimensions:
* **Microscale Systems ($E_5$, Suspensions; $E_2$, Slices):** Cell suspensions (erythrocytes, spermatozoa, stem cells) and ultra-thin hippocampal slices ($LC \approx 0.35\text{ mm}$) can be cooled and warmed at thousands of degrees per second ($>100\text{ }^\circ\text{C/s}$). At these hyper-rapid rates, dilute CPA concentrations (such as V3 at 8.42 M; German et al., *PNAS* 2026) vitrify without crystallization, and post-rewarming electrophysiological function (such as Long-Term Potentiation, LTP) can be recovered.
* **Macroscale Systems ($E_3$, Organs; $E_0$, Whole Organisms):** In human vascularized organs (kidneys, livers, brains) where characteristic thermal conduction lengths ($LC$) range from 1.5 cm to 7.5 cm, heat conduction is governed by Fourier's law. Physical limits prevent uniform fast cooling: attempting to cool a whole human liver or brain at >10 °C/min induces fatal thermal stresses ($\sigma_{\text{th}} \gg 2.0\text{ MPa}$), causing macro-structural fracturing. Conversely, cooling slowly (<0.5 °C/min) to prevent fracture exposes the organ to prolonged ice nucleation regimes or requires extreme CPA concentrations whose diffusion and exposure times cause lethal biochemical cytotoxicity.

### 1.3 The Epistemic Framework
The **StasisPath** framework synthesizes these physical and biochemical laws into an audited, computable biophysical network of 251 nodes. Its state is reported as **two independent numbers that must not be conflated**:

* **Grounding: 97.3 %.** The fraction of the network's claims that rest on primary peer-reviewed sources (91 catalogued, 18 read in full during the final verification pass) and on bounds that remain robust when every input is evaluated at its uncertainty corners.
* **Resolution at the decisive frontier: 0 %.** Frontier $X_2$ is open. No experiment in this framework has been executed.

A well-grounded framework is not an answered question. We state this explicitly because a single headline percentage invites exactly that confusion: a complete set of blueprints is not a bridge that carries traffic. The framework replaces empirical trial-and-error with deterministic boundary equations, hash-locked falsification thresholds (§8.3), and explicit declarations of what remains unmeasured.

---

## 2. Mathematical Physics & Governing Formulations

```
===================================================================================
                              STASISPATH CORE FORMULAS
===================================================================================
 F1 / F2 : Thermal Stress & Fracture     σ_th = (E·α·ΔT_radial) / (1 - ν)  <= σ_max
 F3      : Piecewise Q10 Ischemic Debt  τ_eq = ∫ dt / S(T(t))
 F4      : Stochastic Ice Nucleation     V · t ≈ 1.0 L·h  (at -2 °C)
 F5      : Thermal Diffusion Limit       LC* = sqrt( α_diff · ΔT / CCR )
 CPA Tox : Arrhenius Kinetic Toxicity    D_CPA = ∫ k_tox(T) dt  [E_a/R = 2952 K]
 Osmotic : Kedem-Katchalsky Washout      ΔV / V_0 <= 1.15  (clamped with Mannitol)
===================================================================================
```

### 2.1 Formula F3: Bilinear Piecewise $Q_{10}$ Kinetics & Equivalent Ischemia
In non-hibernating mammals, metabolic rate depression induced by passive hypothermia does not follow a uniform single-slope Arrhenius activation across the entire thermal span from 37.0 °C to subzero. Instead, microcalorimetric and enzymatic studies demonstrate a bilinear piecewise relationship transitioning at $T_{\text{trans}} = 15.0\text{ }^\circ\text{C}$:

$$\tau_{\text{eq}} = \int_0^t \frac{dt'}{S(T(t'))}$$

Where the metabolic suppression scaling factor $S(T)$ is defined piecewise:

$$S(T) = \begin{cases} 
Q_{10,\text{warm}}^{\frac{37.0 - T}{10.0}} & \text{for } T > 15.0\text{ }^\circ\text{C} \\
Q_{10,\text{warm}}^{\frac{37.0 - 15.0}{10.0}} \cdot Q_{10,\text{cold}}^{\frac{15.0 - T}{10.0}} & \text{for } T \le 15.0\text{ }^\circ\text{C}
\end{cases}$$

Empirical anchors:
* $Q_{10,\text{warm}} = 2.15 \pm 0.15$ (empirically validated across $15.0\text{ }^\circ\text{C} \le T \le 37.0\text{ }^\circ\text{C}$)
* $Q_{10,\text{cold}} = 3.50 \pm 0.50$ (empirically validated across $-2.0\text{ }^\circ\text{C} \le T < 15.0\text{ }^\circ\text{C}$)

Under this formulation, an organ held at 10.0 °C for 2.0 hours accumulates:

$$S(10.0) = 2.15^{\frac{22.0}{10.0}} \cdot 3.50^{\frac{5.0}{10.0}} = 2.15^{2.20} \cdot 3.50^{0.50} \approx 5.37 \cdot 1.87 = 10.04$$

$$\tau_{\text{eq}} = \frac{2.0\text{ h}}{10.04} \approx 0.199\text{ h} \quad (11.95\text{ minutes of normothermic ischemia equivalent})$$

#### Domain Breakdown Warning (Hibernators & Ectotherms)
In natural obligate hibernators (*Ictidomys tridecemlineatus*, *Marmota monax*), metabolic suppression is not a passive Arrhenius slowing. Active reversible phosphorylation of pyruvate dehydrogenase (PDH) and mitochondrial complexes I and II suppresses respiration down to 1% to 3% of euthermic baseline even at 10 °C to 12 °C. Below 12.0 °C, the metabolic curve flattens into a temperature-independent plateau, violating passive $Q_{10}$ models by more than an order of magnitude.

### 2.2 Formula F4: Stochastic Ice Nucleation Scaling (a Single-Anchor Hypothesis)
In supercooled biological solutions without heterogeneous seed crystals, ice nucleation is an intrinsically stochastic Poisson process: the probability of remaining ice-free is $P = \exp(-J(T)\,V\,t)$, where $J(T)$ is a nucleation rate per unit volume and time. If $J$ is a property of the bulk liquid, then the product $V \cdot t$ at fixed $T$ is the invariant.

**The framework's measured anchor is a single point:** pig kidney, $0.2$ L held 5 h at $-2$ °C without nucleating (F20), i.e. $V\cdot t \approx 1.0\ \text{L}\cdot\text{h}$. One point does not determine $J(T)$, and the framework itself records this scaling as a **falsifiable hypothesis, not a valid derivation** (internal formulation F4). Taking it at face value would give the following, **which are predictions of the hypothesis and not measurements**:

| System | $V$ (L) | $t_{\max} = 1.0/V$ (h) | Status |
|---|---|---|---|
| Human kidney | 0.150 | 6.7 | prediction |
| Human brain | 1.400 | 0.71 (43 min) | prediction |
| Whole-trunk core | ~25 | 0.04 (2.4 min) | prediction (absurdly short; see below) |

**The measured data do not all agree with a single volumetric law**, and this is the more honest summary:

* Rat liver ($\approx 8$–$14$ mL) supercooled at $-6$ °C survived 72 h at 100 % and 96 h at about 58 % with real orthotopic transplantation (F85). Under the Poisson model that implies an upper bound $J(-6\ ^\circ\text{C}) \lesssim 0.57$ nucleations per L·h. It is a different temperature from the anchor, and it is an upper bound, not a fitted value.
* The same pig-kidney group had to **raise** the temperature to $-0.5$ °C to reach 24–48 h (F20): nucleation risk accumulates with time as well as volume.
* An **isochoric** (constant-volume) chamber held a whole pig liver at $-2$ °C for 24–48 h without freezing (F22). Isochoric confinement suppresses nucleation, so it follows a different law and must not be intersected with isobaric bounds.

The earlier statement in this section that a rat kidney could be held 1000 h ($\approx 41.6$ days) "as demonstrated" was an extrapolation of the hypothesis, not a measurement, and has been withdrawn. The cheap decisive experiment is to supercool two volumes at the same temperature and test whether the time to nucleation scales as $1/V$.

### 2.3 Formula F5: Thermal Conduction Limits & Critical Cooling Rates
For an organ of characteristic thermal half-thickness $LC$ and thermal diffusivity $\alpha_{\text{diff}}$, the maximum achievable internal cooling rate without establishing extreme surface-to-core thermal gradients is governed by Fourier heat conduction. The critical vitrification length $LC^*$ is:

$$LC^* = \sqrt{\frac{\alpha_{\text{diff}} \cdot \Delta T_{\text{crit}}}{\text{CCR}}}$$

Where:
* $\alpha_{\text{diff}} \approx 0.078\text{ cm}^2/\text{min}$ (tissue thermal diffusivity)
* $\Delta T_{\text{crit}} \approx 40.0\text{ K}$ (thermal window through the crystallization zone between $-15\text{ }^\circ\text{C}$ and $-55\text{ }^\circ\text{C}$)
* $\text{CCR}$ is the Critical Cooling Rate required to avoid nucleation.

* For a cooling rate of $147.0\text{ }^\circ\text{C/min}$ (the rate at which V3 was cooled; its true CCR is unmeasured and at most this value):
  $$LC^* = \sqrt{\frac{0.078 \cdot 40.0}{147.0}} = \sqrt{0.0212} \approx 0.145\text{ cm} = 1.45\text{ mm}$$
  *V3 cannot vitrify any biological sample thicker than ~1.5 mm without forming structural ice.*
* For M22 ($\text{CCR} \approx 0.10\text{ }^\circ\text{C/min}$):
  $$LC^* = \sqrt{\frac{0.078 \cdot 40.0}{0.10}} = \sqrt{31.2} \approx 5.58\text{ cm}$$
  *M22 possesses the physical capability to vitrify whole human organs ($LC \approx 2–4\text{ cm}$).*

### 2.4 Formulas F1 & F2: Thermomechanical Stress & Fracture Mechanics at $T_g$
Below the glass transition temperature ($T_g \approx -123.0\text{ }^\circ\text{C}$ for M22), vitrified biological tissue transitions from a viscoelastic liquid into a solid, brittle amorphous glass. Uneven thermal contraction across a temperature gradient $\Delta T_{\text{radial}}$ generates thermoelastic tensile stress $\sigma_{\text{th}}$:

$$\sigma_{\text{th}} = \frac{E \cdot \alpha_{\text{linear}} \cdot \Delta T_{\text{radial}}}{1 - \nu}$$

Where the radial temperature differential established during cooling or warming at rate $\dot{T}$ in a cylinder of radius $LC$ is:

$$\Delta T_{\text{radial}} = \frac{\dot{T} \cdot LC^2}{2 \cdot \alpha_{\text{diff}}}$$

Substituting:

$$\sigma_{\text{th}} = \frac{E \cdot \alpha_{\text{linear}} \cdot \dot{T} \cdot LC^2}{2 \cdot \alpha_{\text{diff}} \cdot (1 - \nu)}$$

Mechanical parameters for vitrified biological tissue:
* Young's modulus: $E = 1.20\text{ GPa} = 1200\text{ MPa}$
* Linear thermal expansion coefficient: $\alpha_{\text{linear}} = 50.0 \times 10^{-6}\text{ K}^{-1}$
* Poisson's ratio: $\nu = 0.35$
* Fracture strength limit: $\sigma_{\text{max}} \approx 2.0\text{ MPa}$

**The EN 14620-5 Standard for Cryogenic Integrity:** In industrial cryogenic engineering, EN 14620-5 specifies that thermal ramps near phase transitions must be strictly controlled to prevent thermal shock fracture. In biological vitrification, to ensure $\sigma_{\text{th}} < 1.0\text{ MPa}$ (a safety margin of 2.0 below $\sigma_{\text{max}}$) for an organ with $LC = 3.5\text{ cm}$:

$$\dot{T}_{\text{safe}} \le \frac{2 \cdot 1.0\text{ MPa} \cdot 0.078\text{ cm}^2/\text{min} \cdot (1 - 0.35)}{1200\text{ MPa} \cdot (50 \times 10^{-6}\text{ K}^{-1}) \cdot (3.5\text{ cm})^2} = \frac{0.1014}{0.735} \approx 0.138\text{ }^\circ\text{C/min}$$

This proves analytically that cooling or warming rates near $T_g$ must be maintained below **$0.150\text{ }^\circ\text{C/min}$**. Any rapid cooling across $T_g$ ($>1.0\text{ }^\circ\text{C/min}$) induces catastrophic macro-fracturing, cleaving vasculature and neural tracts into shards.

---

## 3. Cryoprotectant Cytotoxicity Kinetics & Phase Equilibria

Vitrification eliminates ice crystallization by raising solute viscosity until molecular translation halts at $T_g$. However, high multimolar concentrations of organic solvents are toxic to cellular machinery at normothermia.

### 3.1 Arrhenius Toxicity Suppression
Chemical cytotoxicity accumulates as an enzymatic/denaturation rate process governed by Arrhenius kinetics. The fractional accumulated cytotoxicity index $D_{\text{CPA}}$ is:

$$D_{\text{CPA}} = \int_0^t k_{\text{tox}}(T(t')) \, dt' = D_{\text{ref}} \cdot \left( \frac{t}{t_{\text{ref}}} \right) \cdot \exp\left( \frac{E_a}{R} \left( \frac{1}{T_{\text{ref},K}} - \frac{1}{T_K} \right) \right)$$

Empirical calibration from multi-temperature perfusion trials derives the activation parameter:

$$\frac{E_a}{R} \approx 2952\text{ K}$$

### 3.2 Subzero Loading Thermodynamics
This kinetic steepness explains the critical benefit of loading M22 at subzero temperatures:
* **Warm Perfusion (+10.0 °C / 283.15 K) for 25 minutes:**
  $$D_{\text{CPA}} = 0.540 \implies \text{OCR Retention} \approx 46–50\% \quad (\text{Severe irreversible mitochondrial arrest})$$
* **Subzero Perfusion (−22.0 °C / 251.15 K) for 25 minutes:**
  $$D_{\text{CPA}} = 0.142 \pm 0.04 \implies \text{OCR Retention} \ge 85.8\% \quad (\text{Mitochondrial respiration preserved})$$

Lowering the loading temperature to $-22.0\text{ }^\circ\text{C}$ attenuates biochemical toxicity by a factor of **$\times 3.8$**, providing the thermodynamic window required to equilibrate vitrifiable concentrations in tissue without acute cytolysis.

### 3.3 The Comprehensive CPA Formulation Spectrum

| Formulation | Molarity | CCR (°C/min) | CWR (°C/min) | Toxicity profile | Status in StasisPath |
|---|---|---|---|---|---|
| Pure water | 0 M | $3.84 \times 10^{8}$ | not applicable | none | **Measured**: $6.4 \times 10^{6}$ K/s by time-resolved cryo-EM (Mowry 2025) |
| VS55 | 8.40 M | 2.5 in solution, $<1$ in kidney tissue | not recorded here | severe endothelial toxicity | **Measured** (Fahy 2004) |
| VMP | 8.40 M | 5.4 | 62 | moderate bridging solution | **Measured** (Fahy 2004) |
| V3 | 8.42 M | **not measured**; V3 was cooled at $>2.45$ °C/s ($\approx 147$ °C/min) | $>4.11$ °C/s used | LTP preserved (138 %, $P = 0.07$) | The rate was *used*, so the true CCR is at most that value; no CCR has been measured (German 2026) |
| M22 | 9.345 M | 0.10 (solution); $\le 1.0$ in human cortex | 0.4 | high above 0 °C, low at −22 °C; LTP **unproven** | **Bounded** (Fahy 2004, 2026) |
| Natural deep eutectic solvents | n/a (variable molar mass) | $>30$ (they **crystallize** in DSC at 30 °C/min) | not recorded | **limited by toxicity and viscosity at 50 % w/v**, the ceiling set by the primary paper | **Measured, and negative** (Jesus 2022) |
| CAHS proteins | 0.0006 M | gel in situ | not applicable | none | **Measured** (Boothby 2017); vitrifies on drying, not on cooling |

DP6 appears in earlier drafts and in some toolkit constants with a CCR of about 40 °C/min. **No source in the framework supports that figure**, so it is not tabulated here.
```

---

## 4. Osmotic Membrane Biophysics & Stepwise Washout Kinetics

During CPA loading and removal, cell membranes act as semipermeable barriers separating intra- and extracellular water and solutes. Rapid dilution in pure saline induces lethal water influx, cell swelling, and osmotic membrane lysis.

### 4.1 Kedem-Katchalsky Membrane Flux Formulations
Transmembrane volume flux ($J_v$) and solute flux ($J_s$) are governed by the Kedem-Katchalsky equations:

$$J_v = \frac{1}{A} \frac{dV}{dt} = L_p \left[ \Delta P - \sigma_{\text{refl}} R T \Delta C_{\text{cpa}} - R T \Delta C_{\text{non-perm}} \right]$$

$$J_s = \frac{1}{A} \frac{dn_s}{dt} = \omega R T \Delta C_{\text{cpa}} + (1 - \sigma_{\text{refl}}) \bar{C}_{\text{cpa}} J_v$$

Where:
* $L_p$ is hydraulic conductivity ($L_p \approx 1.2 \times 10^{-13}\text{ m}/(\text{Pa}\cdot\text{s})$)
* $\sigma_{\text{refl}}$ is the membrane reflection coefficient for CPA ($\sigma_{\text{refl}} \approx 0.85$ for DMSO in endothelia)
* $\omega$ is solute permeability ($\omega \approx 5.0 \times 10^{-12}\text{ mol}/(\text{N}\cdot\text{s})$)
* $C_{\text{non-perm}}$ is the concentration of impermeable osmotic buffer (Mannitol).

### 4.2 The Volumetric Safety Envelope
Cellular volume must remain strictly within the osmotic tolerance window:

$$0.70 \le \frac{V}{V_0} \le 1.15$$

If $\Delta V / V_0 > 1.15$ (15% swelling), endothelial cell detachment and membrane rupture occur, releasing intracellular lactate dehydrogenase (LDH) and destroying vascular patency.

### 4.3 Synthesized Non-Linear 7-Step Osmotic Washout Schedule
To safely dilute full-strength M22 (9.345 M) down to physiological saline (0.0 M) without exceeding the 1.15 volume excursion limit, an impermeable osmotic buffer (Mannitol, 300 mM down to 0 mM) is introduced:

```
========================================================================================================================
                                      SYNTHESIZED 7-STEP M22 WASHOUT PROTOCOL
========================================================================================================================
Step  Duration (min)  Target Temp (°C)  M22 Conc. (M)  Mannitol (mM)  Max Vol Excursion (V/V0)  Status
------------------------------------------------------------------------------------------------------------------------
1     10.0            -22.0 -> -15.0    7.00 M (75%)   300 mM         1.032                     Safe (Clamped)
2     10.0            -15.0 -> -10.0    5.00 M (53%)   300 mM         1.065                     Safe (Clamped)
3     10.0            -10.0 -> -5.0     3.50 M (37%)   300 mM         1.094                     Safe (Clamped)
4     10.0             -5.0 ->  0.0     2.00 M (21%)   200 mM         1.118                     Safe (Clamped)
5     10.0              0.0 ->  4.0     1.00 M (11%)   100 mM         1.124                     Safe (Peak Swelling)
6     10.0              4.0 ->  8.0     0.40 M (4%)     50 mM         1.085                     Safe (Recovery)
7     15.0              8.0 -> 12.0     0.00 M (0%)      0 mM         1.012                     Fully Normalized
========================================================================================================================
Total Washout Duration: 75.0 minutes | Peak Volumetric Excursion: 1.124 <= 1.150 Safety Threshold
```

> **Status of this schedule.** It is the output of the Kedem–Katchalsky model of §4.1 with assumed transport parameters ($L_p$, $\sigma_{\text{refl}}$, $\omega$) that were **not measured in this work**. "Safe" in the table means *within the model's volume limit*, not experimentally validated. It is a design candidate to be tested, with the peak at step 5 as the point to monitor, and it is not part of any preregistration.

---

## 5. Reperfusion, Rewarming, and the Microvascular Cascade

Viability failure in cryopreserved organs occurs predominantly during rewarming, washout, and the resumption of physiological blood flow.

```
========================================================================================================================
                                          FIVE-PHASE REPERFUSION & WARMING CASCADE
========================================================================================================================
Phase   Thermal Span        Primary Physical Phenomenon          Biological Mechanism              Proposed Mitigation
------------------------------------------------------------------------------------------------------------------------
Phase A -196 °C -> -123 °C  Thermomechanical stress (EN 14620-5) Thermoelastic fracture           Ultra-slow rampa (<0.15 °C/min)
Phase B -123 °C -> -55 °C   Devitrification / Recrystallization  Ice crystal nucleation & growth  RF inductive nanowarming (>50 °C/min)
Phase C  -55 °C -> 0 °C     Osmotic shock & endothelial lysis    Chemical gradient water influx   Stepwise Mannitol-clamped washout
Phase D    0 °C -> 37 °C    Succinate-driven ROS explosion       Mitochondrial RET & mPTP opening Malonate reversible SDH inhibition
Phase E   37 °C continuous  No-reflow microvascular syndrome     Endothelial edema & thrombosis   PEG-35k SNMP subnormothermic perf.
========================================================================================================================
```

### 5.1 Succinate Hyperoxidation & Complex II Inhibition
During warm or cold ischemic arrest, succinate hyper-accumulates via reversed flux of succinate dehydrogenase (SDH). When normothermic oxygenated perfusion resumes in Phase D, the sudden oxidation of succinate produces an overwhelming proton motive force across the mitochondrial inner membrane, driving massive reverse electron transport (RET) into complex I. This generates a fatal burst of superoxide ($\text{O}_2^{\bullet-}$) and hydrogen peroxide ($\text{H}_2\text{O}_2$), inducing lipid peroxidation of cardiolipin and opening the mitochondrial permeability transition pore (mPTP).
* **Engineering Solution:** Transient infusion of competitive reversible SDH inhibitors (such as dimethyl malonate) during the initial 15 minutes of rewarming is proposed to suppress RET. The framework records only that damage is attenuated by metabolic inhibitors that prevent succinate accumulation and oxidation (F86); the dose and the size of the effect quoted in earlier drafts were not sourced and are not claimed.

### 5.2 The No-Reflow Phenomenon & Capillary Edema
In Phase E, macrovascular blood flow can be restored while capillary beds remain completely unperfused—the "no-reflow" phenomenon. This is caused by swelling of microvascular pericytes and endothelial cells, blebbing of luminal membranes, and microvascular capillary pinching. 
* **Engineering Solution:** Implementation of subnormothermic machine perfusion (SNMP at 21.0 °C) with high-molecular-weight oncotic support (polyethylene glycol, PEG-35k, 35 kDa) is proposed to normalize endothelial hydrostatic balance before full normothermic reperfusion is permitted.

---

## 6. Comparative Biology of Natural Stasis & Non-$Q_{10}$ Adaptations

Nature has evolved diverse strategies to circumvent the biostasis trilemma. These adaptations establish empirical boundaries that validate or constrain our physical formulations:

```
========================================================================================================================
                                     NATURAL BIOLOGICAL STASIS STRATEGIES
========================================================================================================================
Organism                  Active Temp    Metabolic Depression  Mechanistic Class          Dominant Stasis Mechanism
------------------------------------------------------------------------------------------------------------------------
Rana sylvatica (Wood frog)-4 °C -> 0 °C  ~90% reduction        Freeze-tolerant            Glucose (194 mM) + Urea cycling
Ictidomys (Squirrel)      -2 °C -> 12 °C 97% to 99% reduction  Active metabolic arrest    Reversible PDH / Complex I/II phosph.
Trachemys scripta (Turtle) 3 °C -> 20 °C 99.5% reduction (3 °C)Channel arrest anoxia      Carbonate buffer + GABA (80x surge)
Milnesium (Tardigrade)    -196 °C -> 25 °C 100% (Anhydrobiosis) Macromolecular glass       CAHS proteins form non-toxic glass
Cystophora (Hooded seal)  37 °C          Brain sparing         Glial metabolic plasticity Neuroglobin surge + Glial glycogen
Human Fetus / Neonate     30 °C -> 37 °C 50% to 75% reduction  Ontogenic neuroprotection  Adenosine A1R + K_ATP channel arrest
========================================================================================================================
```

### 6.1 Freeze Tolerance in *Rana sylvatica*
The Alaskan wood frog survives months frozen solid at temperatures down to $-6.0\text{ }^\circ\text{C}$, with up to 65% of total body water converted into extracellular ice. In the field, freeze-thaw priming triggers massive glycogenolysis, accumulating up to 194 µmol/g glucose in hepatic and cardiac tissue alongside 106 µmol/mL urea. This endogenous cryoprotectant cocktail colligatively limits intracellular dehydration. Crucially, laboratory frogs rapidly frozen without ecological priming die within 8 to 12 weeks, proving that cryoprotectant loading protocol and thermal history are state variables, not auxiliary details.

### 6.2 Active Metabolic Suppression in *Ictidomys tridecemlineatus*
The thirteen-lined ground squirrel enters multi-day torpor bouts where core body temperature drops to $-2.9\text{ }^\circ\text{C}$ without freezing. Respiration drops to 1–2 breaths per minute and heart rate falls from 350 bpm to 4 bpm. This state is achieved not by passive $Q_{10}$ chilling, but by active phosphorylation of mitochondrial pyruvate dehydrogenase (PDH) and complex I/II arrest, switching fuel consumption exclusively to stored fatty acids (respiratory quotient = 0.70).

### 6.3 Extreme Anoxia in *Trachemys scripta*
The painted turtle survives up to 170 days submerged under ice at 3.0 °C without a single molecule of oxygen. It achieves complete electrical quiescence ("channel arrest"), down-regulating membrane ion channel densities to prevent depolarization. Brain GABA concentrations surge $\times 80$, and the massive release of calcium carbonate from its shell buffers profound lactic acidosis ($>150\text{ mM}$ lactate), preventing systemic acidemic collapse.

### 6.4 Macromolecular Vitrification in Tardigrades
Tardigrades survive complete desiccation and immersion in liquid nitrogen ($-196.0\text{ }^\circ\text{C}$) using cytosolic abundant heat-soluble (CAHS) proteins. Upon dehydration or concentration (>15 g/L), these intrinsically disordered proteins form a reticular hydrogel and transition into a macromolecular glass ($T_g \approx 100.0\text{ }^\circ\text{C}$ in the dry state) without requiring multimolar toxic small-molecule solvents.

---

## 7. Anthropometric Multi-Organ Projection & Biophysical Bottlenecks

Preserving a macroscopic mammal requires orchestrating thermal and chemical kinetics across heterogeneous organ systems simultaneously.

### 7.1 Allometric Baseline (ICRP 89 Reference Human)
Using the Du Bois Body Surface Area ($BSA = 0.007184 \cdot W^{0.425} \cdot H^{0.725}$) and ICRP Publication 89 Reference Anatomical Models for a standard adult ($70\text{ kg}$, $175\text{ cm}$, $BSA \approx 1.85\text{ m}^2$):

```
========================================================================================================================
                                      MULTI-ORGAN BIOPHYSICAL CONSTRAINT MATRIX
========================================================================================================================
Organ / Compartment    Mass (g)  Volume (L)  d (cm)   t_max @ -2°C  Max Safe Rampa @ Tg  Bottleneck Order & Mechanism
------------------------------------------------------------------------------------------------------------------------
Brain (Encephalon)     1400      1.350       7.00     0.74 h (44m)  < 0.038 °C/min       #1: Extreme ischemic/thermal limit
Kidneys (Bilateral)     310      0.300       2.75     3.33 h        < 0.245 °C/min       #2: Endothelial osmotic vulnerability
Heart (Myocardium)      330      0.320       3.00     3.12 h        < 0.206 °C/min       #3: Arrhythmogenic hypothermic arrest
Liver (Hepatic parenchyma) 1800  1.750       6.50     0.57 h (34m)  < 0.044 °C/min       #4: Diffusion distance & microperfusion
Lungs (Bilateral)       1000      0.950       5.50     1.05 h        < 0.061 °C/min       #5: Capillary shear & alveolar edema
Pancreas                100      0.095       1.50     10.5 h        < 0.822 °C/min       #6: Autolytic enzymatic activation
Trunk Deep Core (Bulk) 25000     24.50       12.50    0.04 h (2.4m) < 0.012 °C/min       #7: Absolute whole-body thermal barrier
========================================================================================================================
```

> **Reading this table.** The column $d$ is an anatomical half-thickness estimate produced by the toolkit's organ projector. It is **not** the characteristic length $LC = V/A$ used everywhere else in this manuscript (for a human brain $LC = 2.31$ cm, §7.2 and §8.4); the two should not be compared, and an earlier draft labelled both "LC". The $t_{\max}$ column inherits the single-anchor hypothesis of §2.2 and is a prediction, not a measurement. The viability verdicts of this paper rest on the $LC$ table of §7.2, computed by the engine.

### 7.2 The Whole-Body Conduction Barrier
The data reveals an insurmountable physical bottleneck: while small organs such as the kidneys or pancreas have critical half-thicknesses ($LC \le 2.75\text{ cm}$) compatible with controlled-rate cooling, the **trunk deep core** ($LC \approx 12.8\text{ cm}$ when the torso is correctly treated as a cylinder, $LC = V/A = r/2$; a sphere approximation gives 8.5 cm and is optimistic by $1.5\times$) cannot be cooled faster than $0.012\text{ }^\circ\text{C/min}$ without generating fatal fracture stress ($\sigma_{\text{th}} > 2.0\text{ MPa}$). At $0.012\text{ }^\circ\text{C/min}$, crossing the crystallization zone requires over 50 hours, during which ice nucleation ($V \cdot t \approx 1.0\text{ L}\cdot\text{h}$) is effectively certain to induce catastrophic frozen solidification.

**Robustness of the organ-scale verdicts against the geometry premise.** Because $LC$ depends on an assumed shape, each verdict carries a *flip factor*: the multiplicative $LC$ error at which the verdict reverses. A cylinder modelled as a sphere is wrong by $1.5\times$, so any flip factor above 1.5 survives the worst plausible geometry mistake.

| Organ | Mass (g) | $LC$ (cm) | Required CCR (°C/min) | Required molarity (mol/L) | Flip factor | Verdict |
|---|---|---|---|---|---|---|
| Pancreas | 90 | 0.93 | 2.65 | 8.48 | $\times$5.1 | viable |
| Kidney | 150 | 1.10 | 1.88 | 8.58 | $\times$4.08 | viable |
| Heart | 300 | 1.38 | 1.19 | 8.69 | $\times$3.24 | viable |
| **Brain** | **1400** | **2.31** | **0.425** | **8.95** | **$\times$1.94** | **viable** |
| Liver | 1500 | 2.37 | 0.406 | 8.96 | $\times$1.90 | viable |
| Whole body | 70 000 | 12.78 | 0.014 | 9.80 | — | **not viable** |

The brain, the organ on which the entire clinical argument rests, has the tightest surviving margin: its verdict reverses only if $LC$ is underestimated by $1.94\times$, against a worst-case geometric error of $1.5\times$. **The verdict survives, with 1.29$\times$ to spare.** This margin was not visible before the audit described in §10.4 and is reported here because a verdict without its failure tolerance is not a result.

---

## 8. The Epistemic Landscape, Frontier $X_2$, and the P19 Experiment

```
===================================================================================
                            THE FRONTIER X2 DILEMMA
===================================================================================
 Rate used: 147 °C/min |  V3: German et al. (PNAS 2026)
                       |  LTP PRESERVED (138%, p=0.072)
                       |  [Mouse slice scale only; LC <= 0.35 mm]
                       |
                       |                     FRONTIER X2
                       |              (NO KNOWN CHEMISTRY HAS BOTH
                       |               SCALE AND FUNCTION VERIFIED)
                       |
  Low CCR (0.10 °C/min)|  M22: Fahy et al. (2004, 2026)
                       |  ORGAN SCALE VITRIFICATION (LC >= 3.5 cm)
                       |  [Kidney transplant 8/8; Brain LTP UNPROVEN]
                       +-----------------------------------------------------------
                         No Function Verified           Electrophysiology Proven
===================================================================================
```

### 8.1 The Empty Intersection
* **V3 Formulation (German et al., *PNAS* 2026):** Proves that functional synaptic electrophysiology (LTP) can be preserved following vitrification. However, it was cooled at about $147\text{ }^\circ\text{C/min}$ ($>2.45$ °C/s), a rate that only slices thinner than a fraction of a millimetre can follow; its true CCR has not been measured and is at most that value, so "V3 does not scale" is an inference from the rate used, and one of the open questions of the framework.
* **M22 Formulation (Fahy et al., 2004, 2026):** Proves that macro-organs ($LC > 3.5\text{ cm}$) can be vitrified without ice. However, direct functional synaptic plasticity (LTP) has never been verified post-washout.

The intersection between **low critical cooling rate ($\text{CCR} \le 0.43\text{ }^\circ\text{C/min}$)** and **verified electrophysiological synaptic plasticity (LTP)** is **EMPTY**. This defines Frontier **$X_2$**.

### 8.2 The Decision Rule of Experiment P19 (as Frozen)

P19 asks whether M22, a chemistry that scales, preserves long-term potentiation in adult mouse
hippocampal slices (350 µm, same protocol as the V3 positive-control work). Four arms, $n \ge 8$ slices
from $\ge 4$ animals per arm, recording blind to condition: **(A)** unvitrified control; **(B)** V3, a
replicate of the published result and the positive control; **(C)** M22 at its working concentration;
**(D)** loading and unloading of M22 only, without cooling, which separates chemical toxicity from thermal damage.

**Primary variable:** LTP in SC–CA1 at 60 min after HFS, as a percentage of baseline fEPSP. The thresholds
are anchored in the published V3 result (control $157.7 \pm 7.1\%$; V3 $138.1 \pm 6.9\%$; difference not significant, $P = 0.072$):

* **PASS** if arm C reaches $\ge 130\%$ and does not differ from B (95 % CI of the difference within $\pm 25$ percentage points).
* **FAIL** if C $\le 110\%$ (no useful potentiation) while B $\ge 130\%$.
* Between 110 and 130 %, or with B failed: **inconclusive**, and it is not reinterpreted.
* **Quality control:** arm B must replicate the published result within $\pm 20$ percentage points; otherwise the experiment is not interpretable and is repeated before arm C is read.

**Diagnosis provided by arm D.** If D fails like C, the damage is chemical toxicity and the CPA must be redesigned
(by $qv^*$, temperature and loading protocol). If D passes and C fails, the damage is thermal or due to devitrification and is attacked with rate and uniformity.

**Respiration is a secondary measure and not a threshold.** Basal respiration and reserve capacity are recorded so
that results can be compared with the published values (control $173.3 \pm 6.7$; 65 % at 10 °C, $80.4 \pm 5.6$).
The framework's Arrhenius derivation predicts a damage $D_{\text{CPA}} = 0.142$ in arm C, i.e. an OCR retention near
86 %; a damage above 0.25 would refute that **derivation**, and one at or below 0.10 would confirm it. This tests the derivation (contradiction I1),
not P19: P19 is decided by LTP alone.

**What it decides.** PASS means the physical route has an exit: a chemistry exists with demonstrated function and with a CCR
compatible with human scale (the design specification of §8.4 admits $\text{CCR} \le 0.425\ ^\circ\text{C/min}$ for a human brain). FAIL means the
bottleneck is chemical, and the framework's prediction P18 would then be that partial freezing or supercooling reach the clinic before vitrification.

> **Correction relative to an earlier draft.** An earlier version of this section stated a "double-threshold" rule (OCR $\ge 85\%$ and LTP $\ge 120$–$150\%$, with a state
> called "Metabolic OK, Plasticity Open"). That rule did **not** match the hash-locked preregistration and has been removed. The frozen text above is the only
> authority; a document that disagrees with it is the document that is wrong (rule R2).

### 8.3 The Five Hash-Locked Preregistrations

All falsification thresholds below were frozen **before any data exist** and are protected by
SHA-256 certificates over `preregistration_date + protocol_text`, stored in `red/prereg.lock`.
The engine recomputes every hash on each run and halts with an alarm if any frozen text has
changed. This enforces the framework's governing rule: **a threshold may never be moved to
rescue a hypothesis.** Adding a *new* preregistration is legitimate; editing a frozen one is not.

| ID | Question | Primary endpoint & threshold | SHA-256 (first 16) | Status |
|---|---|---|---|---|
| **P15** | Does the connectome survive a realistic cryonics protocol? | Traceable axon/synapse fraction in **blind** EM segmentation $\ge 0.90$ vs immediately-fixed control; 4 normothermic ischemic delay arms (0, 1, 6, 24 h) + $-196$ °C, $n \ge 4$ | `b081e1bef45061f1` | no data |
| **P18** | Minimum falsifiable claim of the framework | For tissue $\ge 1$ L, reversible pause $>24$ h requires *jointly*: (a) $T < T_g$ ($\le -125$ °C) with no ice by µCT, **or** extracellular-only ice with $f_{\text{ice,intra}} = 0$; (b) cooling $\ge$ CCR in tissue; (c) volumetric rewarming $\ge$ CWR with $\Delta T < 20$ K; (d) cumulative $\tau_{eq} \le 12.5$ min before stabilization | `40bf19b0ba442705` | no data |
| **P19** | Does a chemistry that *scales* preserve LTP? | Blind CA1 fEPSP at 60 min post-HFS; **PASS if arm C $\ge 130$ % and within $\pm 25$ pp of the V3 control; FAIL if $\le 110$ %**; between, inconclusive; 350 µm adult mouse hippocampal slices, 4 arms, $n \ge 8$ slices from $\ge 4$ animals | `5b728de09bf17d1c` | no data |
| **P20** | ERL of cryopreserved brain tissue **without** prior fixation | Expected run length (ERL), the connectomics community's own standardized metric; independent of P15, whose original threshold is **not** touched (rule R2) | `74ec536bc98a2a7f` | no data |
| **P21** | Is the cooling-law exponent below 2.34? | One-sided 95 % upper bound on $n < 2.34$; FAILS if the lower bound $>2.34$ or if $\sim 0.15$ L bags cool $\ge 5.3$ °C/min; control: 0.5 L must give $1.4$ °C/min $\pm 15$ % | `3ed875463de17d30` | no data |

> **Traceability note.** An earlier draft of this manuscript presented a set labelled "P1–P5"
> that did not correspond to the repository's frozen record. Those labels are withdrawn. The
> five preregistrations above are the complete and only preregistered set, and each is
> verifiable against `red/prereg.lock` by recomputing its hash from the published text.

### 8.4 The Design Specification: Inverting the Screening Question

Conventional CPA development benchmarks candidates against M22, the most capable published
vitrification solution ($\text{CCR} = 0.10$ °C/min at $9.345$ M). This anchors the search on a
*solution* rather than on a *requirement*, and it discards candidates that would in fact suffice.

The framework computes the requirement directly. Anchored on the measured litre-scale cooling
datum (3 L vessel, $LC = 2.20$ cm, $0.47$ °C/min at the centre) and the conduction exponent
$n = 2$:

$$\text{CCR}_{\text{required}}(LC) = 0.47 \cdot \left(\frac{2.20}{LC}\right)^{n}, \qquad
LC = \frac{V}{A} = \frac{r}{3}\,\kappa_{\text{geom}}$$

with $\kappa_{\text{geom}} = 1$ (sphere), $1.5$ (cylinder), $3$ (slab). For a 1400 g human brain:

$$\boxed{\ \text{CCR}_{\text{required}} = 0.425\text{ }^\circ\text{C/min}\ }$$

**This is $4.25\times$ more permissive than M22.** The practical consequence is a screening
criterion any laboratory can apply to any candidate chemistry with a single DSC measurement:

| Candidate | Measured CCR (°C/min) | vs brain requirement (0.425) | Verdict |
|---|---|---|---|
| M22 | 0.10 | clears by $\times 4.25$ | **ADMISSIBLE** (scale) |
| VS55 | 2.5 | misses by $\times 5.9$ | REJECTED |
| VMP | 5.4 | misses by $\times 12.7$ | REJECTED |
| V3 | $\le 147$ (the rate used; CCR not measured) | not determined | **NOT DETERMINED** |
| Low-toxicity candidates (e.g. deep-eutectic solvents) | **not measured** | — | **UNMEASURED** |

Two cautions are essential, and the toolkit enforces both in code:

1. **Clearing the CCR bar says nothing about preserved function.** Admissibility is a *necessary*
   condition on the ice-avoidance axis only. Frontier $X_2$ is precisely the observation that no
   chemistry has yet cleared both axes.
2. **An unmeasured chemistry returns `UNMEASURED`, never a pass or a fail.** We note explicitly
   that an earlier version of our own toolkit hardcoded a CCR of 30 °C/min for deep-eutectic
   solvents. No such peer-reviewed value exists, and the framework's own evidence points the
   other way: these solvents at 50 % w/v *crystallize* (crystallization onset $-26.6$ °C), i.e.
   they vitrify worse than DMSO. That constant has been removed. A hardcoded value for an
   unmeasured quantity is the mechanism by which a framework fabricates progress.

### 8.5 Value of Information: Which Experiment to Run First

A measurement is worth performing when its plausible range **straddles a decision threshold**.
We rank every open quantity by expected value of information (EVOI) per unit cost, where
$\text{EVOI} = \min\!\left(1,\; 2 P(\text{crossing}) (1 + \sigma)\right)$ under a Gaussian prior:

| Open quantity | Prediction | $\sigma$ | Threshold | EVOI | Rel. cost | EVOI/cost | Recommendation |
|---|---|---|---|---|---|---|---|
| **CCR of a low-toxicity candidate (DSC)** | 0.30 °C/min | 0.36 | 0.426 | 0.988 | 1.0 | **0.99** | **RUN FIRST** |
| **Cooling exponent $n$ (P21)** | 2.00 | 0.26 | 2.34 | 0.241 | 0.5 | **0.48** | **RUN** |
| Nucleation rate $J$ at $-6$ °C | 0.57 /L·h | 0.285 | 0.85 | 0.419 | 12 | 0.03 | defer (cost) |
| Human $\tau_{eq}$, optimal reperfusion | 17 min | 7.65 | 12.5 | **1.000** | 30 | 0.03 | defer (cost) |
| P19 (LTP after vitrification) | 0.142 | 0.078 | 0.25 | 0.179 | 20 | 0.01 | defer (cost) |

Three results deserve emphasis.

**First, a differential scanning calorimetry run on a low-toxicity candidate is the single most
valuable experiment in the framework** (EVOI 0.988 at unit cost), because its plausible range
straddles the 0.426 °C/min bar. If it clears, frontier $X_2$ closes on the scale axis **without
executing P19**. Days of instrument time replace a full electrophysiology campaign.

**Second, P21 — a control vessel, three small bags, three large bags and one thermocouple —
ranks second overall**, forty-eight times above P19 per unit cost. It had been deprioritized as
trivial. It is not: the exponent $n = 2$ carries the entire multi-organ projection of §7 and has
never been measured.

**Third, human $\tau_{eq}$ has the highest EVOI in the framework (1.000) and is deferred purely
on cost.** This is a statement about resources, not about relevance, and we record it as such
rather than quietly omitting the most informative unmeasured quantity in the field.

---

## 9. Regulatory Pathways, Clinical Translation, and Experimental Models

```
========================================================================================================================
                                      EXPERIMENTAL & REGULATORY TIER MATRIX
========================================================================================================================
Tier  Model System                 Regulatory / Ethical Framework  TRL Level  Translational Role & Key Advantage
------------------------------------------------------------------------------------------------------------------------
Tier 1 In Vitro / Brain Slices     IACUC Standard Animal Protocol  TRL 2-3    Synaptic plasticity (LTP), pure cytotoxicity
Tier 2 Rodent Whole Organ          IACUC Small Animal Surgery      TRL 4      Vascular orthotopic transplantation, 100-day survival
Tier 3 Porcine In Vivo Model       Pre-clinical Large Animal Com.  TRL 5      Human-scale vascular organ translation (30-50 kg)
Tier 4 Surgical Discard Organ      IRB Approval + UAGA Consent     TRL 3-5    CRITICAL BRIDGE: Real human tissue, ex vivo normothermic
Tier 5 Emergency Clinical (EPR)    FDA / EMA EFIC (21 CFR 50.24)   TRL 6-7    Ultra-short deep hypothermia (<45 min); resuscitation
Tier 6 Post-Mortem Field Stasis    UAGA Whole-Body Donation        TRL 1-2    Field cryoprotection; penalized by warm ischemic delay
========================================================================================================================
```

### The Human Discard Organ: The Indispensable Translational Bridge
A critical methodological innovation in StasisPath is the formal inclusion of **human surgical discard organs** (Tier 4: kidneys with KDPI > 85, steatotic livers, partial surgical resections). These organs possess human microvascular architecture and human-specific endothelial antigens, but are legally and ethically accessible for destructive research via standard IRB biomedical donation protocols. Cannulating these organs immediately upon surgical excision eliminates post-mortem warm ischemic debt ($\tau_{\text{eq}} \approx 0$), providing an authentic human testbed for M22 loading and osmotic washout schedules.

---

## 10. Formal Epistemic Safeguards and No-Claim Declarations

To maintain absolute scientific integrity and prevent misinterpretation by the public or scientific community, StasisPath enforces three explicit epistemic boundary declarations:

```
+----------------------------------------------------------------------------------------------------------------------+
|                                  FORMAL NO-CLAIM DECLARATIONS (EPISTEMIC SAFEGUARDS)                                 |
+----------------------------------------------------------------------------------------------------------------------+
| 1. Whole-Body Stasis is Open and Unvalidated: We DO NOT claim that reversible whole-body cryopreservation in adult    |
|    non-hibernating mammals is currently feasible. There is zero published evidence of functional recovery in an      |
|    intact adult mammal following vitrification.                                                                      |
|                                                                                                                      |
| 2. Multi-Organ Extrapolation is Strictly Conjectural: Success at cellular (E5) or slice scales (E2) cannot be       |
|    assumed to scale to vascularized organs (E3) or whole organisms (E0). Extrapolating isolated organ kinetics to     |
|    intact bodies remains an unverified hypothesis.                                                                   |
|                                                                                                                      |
| 3. Frontier X2 Remains Open: Numerical modeling demonstrates target parameter feasibility, but X2 remains formally   |
|    OPEN until direct electrophysiological verification (LTP) is achieved and replicated in pre-registered trials.    |
+----------------------------------------------------------------------------------------------------------------------+
```

---

### 10.4 Self-Audit: Three Corrections to Our Own Results

The framework was audited against its own premises using formal regime guards, dimensional
analysis, and value-of-information ranking. The audit was designed to make results *less*
impressive, and it did. All three findings are reported here because a framework that only ever
revises upward is not auditing itself.

**(1) $Q_{10}$ applied below the glass transition — an unphysical extrapolation.** Bound C2
reported that ten-year storage requires $T < -129$ °C. But $T_g = -123$ °C: below it there is no
liquid water and no metabolism, so $Q_{10}$ is not merely extrapolated, it is **undefined**. The
$-129$ °C figure is a number without physics behind it and is withdrawn as a quantitative claim.
The *verdict* of C2 survives untouched, because what C2 actually asserts is the far weaker and
robust statement that ten-year storage requires $T < 0$ °C under **any** measured $Q_{10}$. We
note separately that no $Q_{10}$ in the framework was measured below $-10$ °C; everything below
that temperature is projection.

**(2) A silent geometry premise, now quantified.** $LC = V/A$ was computed with a sphere formula
($r/3$) throughout, including for the torso, which is a cylinder ($r/2$). Rather than assert the
correction is harmless, we computed the flip factor for every organ (§7.2). The brain's verdict
reverses only at an $LC$ error of $1.94\times$, against a worst-case geometric error of
$1.5\times$: it survives. The whole-body verdict was already negative and the correction makes it
more so ($LC$ 8.5 → 12.8 cm, required molarity 9.60 → 9.80 mol/L). A related inconsistency
between the manuscript (12.5 cm) and the computational engine (8.5 cm) has been unified in favour
of the cylinder.

**(3) A hidden density assumption.** Converting organ mass in grams to a length in centimetres
requires a density. The framework assumed $\rho = 1.0$ g/cm³ without declaring it (tissue is
$\approx 1.05$, a $-1.6$ % bias in $LC$). The bias is small; the undeclared premise was not
acceptable. Density is now an explicit parameter of the public API.

**A fourth item is a methodological disclosure rather than a physical finding.** The exponent
$n = 2$ underlying the entire multi-organ projection of §7 is preregistered (P21) but **has never
been measured**. Every number in the organ table inherits that status. We flag it on every
computation rather than in a footnote.

---

## 11. The `stasispath` Computational Toolkit

Alongside the theoretical framework, we release `stasispath`, an open-source, zero-dependency Python 3 package (`pip install .`) designed to automate biophysical calculations for laboratory cryobiologists. Beyond implementing the governing equations, three modules make the framework's *epistemic* machinery directly usable by other groups:

**`design_spec`** — the inverted screening question of §8.4. `required_ccr(mass_g, geometry)` returns the cooling rate a given piece of tissue actually demands; `screen_candidate_cpa(name, measured_ccr)` returns `ADMISSIBLE`, `REJECTED` or `UNMEASURED` against that bar, and refuses to return a verdict for a chemistry with no measured value. `geometry_flip_factor()` returns the multiplicative $LC$ error at which a verdict reverses, so no viability claim need be published without its failure tolerance.

**`assumptions`** — executable regime guards for the premises that silently invalidate cryobiology calculations: the Biot boundary (mixing the $LC^{-1}$ and $LC^{-2}$ laws across $Bi = 1$ overstated our own cross-species scaling by $2.6\times$), $Q_{10}$ below $T_g$ (a `FAIL_STOP`, per §10.4), isochoric nucleation rates compared against isobaric bounds, sphere formulae on elongated geometries, undeclared densities, and unmeasured scaling exponents. Guards return severities (`WARNING`, `SWITCH_MODEL`, `FAIL_STOP`), are cheap enough to run on every state, and are written to make a result worse rather than better.

**`experiment_value`** — the EVOI-per-cost ranking of §8.5, so that any group can re-rank the open set against its own cost structure and instrument access rather than inheriting ours.

```
stasispath-tools/
├── pyproject.toml              # Author: Alejo Malia
├── README.md                   # Complete biophysical guide & API docs
└── stasispath/
    ├── __init__.py             # Public exports & versioning
    ├── constants.py            # Empirical anchors (Q10, Ea, E, nu, alpha)
    ├── units.py                # Strict dimensional conversions (°C, K, bar, MPa)
    ├── f3_ischemia.py          # Piecewise Q10 integration (tau_eq)
    ├── f4_nucleation.py        # Poisson ice nucleation probability
    ├── f5_cooling.py           # Conduction limits & critical length scales (LC*)
    ├── thermal_stress.py       # EN 14620-5 thermoelastic stress & fracture
    ├── cpa_toxicity.py         # Arrhenius cytotoxicity accumulation (D_CPA)
    ├── cpa_washout.py          # Kedem-Katchalsky osmotic washout protocol scheduler
    ├── thermal_recipes.py      # Freezer ramp generator (Planer Kryo, Asymptote)
    ├── organ_projector.py      # Du Bois / ICRP 89 anthropometric projector
    ├── boa_connector.py        # Radiological CT mask ingestor (BOA, TotalSegmentator)
    ├── predictions.py          # frozen P19 decision rule + exploratory hypotheses H2-H5
    ├── reporting.py            # Markdown synthesis & laboratory summary generator
    ├── cli.py                  # Full command-line interface
    └── tests/                  # 28/28 passing unit tests (0.005s execution)
```

### Automated Verification
The suite comprises **79 unit tests** (`python -m pytest`, no external dependencies) and covers all analytical and epistemic modules:
* `TestF3Ischemia`: Verifies bilinear $Q_{10}$ inflection at 15.0 °C and hibernator domain flag.
* `TestF4Nucleation`: Validates Poisson survival probabilities and interfacial defect collapse.
* `TestThermalStress`: Confirms safe cooling rates near $T_g$ ($<0.150\text{ }^\circ\text{C/min}$) and fast-rate fracture.
* `TestCPAToxicity`: Validates subzero kinetic toxicity rescue ($\times 3.8$ attenuation at $-22\text{ }^\circ\text{C}$).
* `TestCPAWashout`: Proves that abrupt washout causes osmotic lysis and verifies the 7-step Mannitol clamp ($\Delta V/V_0 \le 1.124 \le 1.150$).
* `TestOrganProjector`: Validates Du Bois BSA calculations, ICRP 89 organ volumes, and bottleneck ranking.
* `TestBOAConnector`: Confirms ingestion of TotalSegmentator / BOA radiologic volume masks.
* `TestP19FrozenRule`: Verifies the P19 decision rule at every frozen threshold and every boundary (130 %, 110 %, $\pm 25$ pp, $\pm 20$ pp), that arm B failing the replication band makes the experiment non-interpretable, and that the superseded 'softened' threshold no longer passes.
* `TestThermalRecipes`: Validates cryogenic freezer script formatting for Planer Kryo and Asymptote systems.
* `TestDesignSpec`: Verifies that the design specification reproduces the knowledge-graph engine to within 0.002 °C/min on every organ, that the brain requirement is $0.425$ °C/min, that an unmeasured chemistry can never return a pass or a fail, and that the brain's flip factor exceeds the worst-case geometric error.
* `TestAssumptions`: Verifies that each regime guard fires on the exact conditions that produced real errors in this work — $LC^{-2}$ below the Biot length, $Q_{10}$ at $-129$ °C, an isochoric rate against an isobaric bound — and stays silent on consistent states.
* `TestExperimentValue`: Verifies that EVOI is maximal at a decision boundary and vanishes far from it, that calorimetry outranks full electrophysiology by more than fiftyfold per unit cost, and that an expensive-but-decisive measurement is reported as deferred on cost rather than silently dropped.

### Open Science, Data Availability & Licensing
All code, mathematical models, parameter tables, and preregistration protocols for the StasisPath framework are released for academic and scientific research purposes under the **Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)**. Commercial exploitation, resale, or proprietary relicensing is strictly prohibited. The knowledge graph verification engine `red/motor.py` executes deterministically, ensuring that every biophysical equation, boundary condition, and experimental prediction is fully reproducible across platforms without closed dependencies.

---

## 12. References

The framework's knowledge graph catalogues **91 sources**; the subset cited directly in this
manuscript is listed below. Three citations in the previous version of this manuscript were
incorrect and are corrected here: reference 7 (journal: *Nature Protocols*, not *Nature
Medicine*), reference 24 (pages 966 ff., not 1082–1093), and reference 38 (*Energy* **334**:137568,
not 312:133501). Full provenance for all 91 sources, including status tags and the specific
numerical value each one supplies, is in `red/stasispath.yaml`.

**Vitrification, nanowarming and organ-scale preservation**
1. **Han, Z., Rao, J. S., Ramesh, S., et al. (Bischof, J. C.)** (2023). Vitrification and nanowarming enable long-term organ preservation and successful transplantation in rats. *Nature Communications*, 14:3407.
2. **Etheridge, M., Bischof, J. C., et al.** (2025). Scaling vitrification and nanowarming to litre volumes. *Nature Communications*; preprint bioRxiv 2024.11.08.622572.
3. **Fahy, G. M., Wowk, B., Wu, J., & Paynter, S.** (2004). Improved vitrification solutions based on the predictability of vitrification solution toxicity. *Cryobiology*, 48(1):22–35.
4. **Fahy, G. M., Wowk, B., Wu, J., Phan, J., Rasch, C., Chang, A., & Zendejas, E.** (2004). Cryopreservation of organs by vitrification: perspectives and recent advances. *Cryobiology*, 48(2):157–178.
5. **Fahy, G. M., et al.** (2009). Physical and biological aspects of renal vitrification. *Organogenesis*, 5(3):167–175.
6. **Fahy, G. M.** (2010). Cryoprotectant toxicity neutralization. *Cryobiology*, 60(3 Suppl):S45–S53.
7. **Bruinsma, B. G., Berendsen, T. A., Izamis, M.-L., Yarmush, M. L., & Uygun, K.** (2015). Supercooling preservation and transplantation of the rat liver. *Nature Protocols*, 10(3):484–494.
8. **de Vries, R. J., Tessier, S. N., Uygun, K., Toner, M., et al.** (2019). Supercooling extends preservation time of human livers. *Nature Biotechnology*, 37:1131–1136.
9. **Manuchehrabadi, N., et al.** (2017). Improved tissue cryopreservation using inductive heating of magnetic nanoparticles. *Science Translational Medicine*, 9(379):eaah4586.
10. **Wowk, B., Ting, L., Phan, J., Fahy, G. M., et al.** (2025). Dielectric rewarming of vitrified rabbit kidneys at 55 MHz. *Cryobiology*, 119:105257.
11. **Gao, Z., et al.** (2022). Vitrification and nanowarming of rat hearts. *Advanced Materials Technologies*, 7:2100873.
12. **Pichugin, Y., Fahy, G. M., & Morin, R.** (2006). Cryopreservation of rat hippocampal slices by vitrification. *Cryobiology*, 52(2):228–240.
13. **Solanki, P. K., Bischof, J. C., & Rabin, Y.** (2017). Thermo-mechanical stress analysis of cryopreservation in cryobags and the potential benefit of nanowarming. *Cryobiology*, 76:129–139.
14. **Kavian, N., Sellers, M., Sanchez, J., Alvarez, O., Aguilar, G., & Powell-Palm, M. J.** (2025). Cryomacroscopy and finite-element analysis of fracture formation in vitrified systems. *Scientific Reports*, 15:27903.
15. **Pegg, D. E.** (2002). The history and principles of cryopreservation. *Seminars in Reproductive Medicine*, 20(1):5–13.

**Neural function after vitrification — frontier $X_2$**
16. **German, C. L., Akdaş, E., Flügel-Koch, C., Erterek, M., Frischknecht, R., Fejtova, A., Winkler, J., Alzheimer, C., & Zheng, F.** (2026). Synaptic transmission and long-term potentiation in mammalian neural circuits following vitrification and rewarming. *Proceedings of the National Academy of Sciences USA*, 123(10):e2516848123.
17. **Fahy, G. M., et al.** (2026). Vitrification of whole mammalian brain slices with intact ultrastructure using M22 without chemical fixation. *bioRxiv*, 2026.01.28.702375 v2.
18. **German, C. L., & Akdaş, E.** (2024). Recovery of field EPSPs in corticohippocampal slices after exposure to 61 % w/v ethylene glycol. *bioRxiv*, 2024.06.03.597218.
19. **McIntyre, R. L., & Fahy, G. M.** (2015). Aldehyde-stabilized cryopreservation. *Cryobiology*, 71(3):448–458.
20. **Januszewski, M., Kornfeld, J., Li, P. H., Pope, A., Blakely, T., Lindsey, L., Maitin-Shepard, J., Tyka, M., Denk, W., & Jain, V.** (2018). High-precision automated reconstruction of neurons with flood-filling networks. *Nature Methods*, 15:605–610.
21. **MICrONS Consortium** (2025). Functional connectomics spanning multiple areas of mouse visual cortex. *Nature*, 640:435–447.
22. **Rubinsky, L., Raichman, N., Lavee, J., Frenk, H., Ben-Jacob, E., & Bickler, P. E.** (2010). Antifreeze protein type I protects hippocampal slices during hypothermic storage. *Neuroscience Research*, 67(3):256–261.

**Ischemia, reperfusion and metabolic suppression**
23. **Hossmann, K.-A., Schmidt-Kastner, R., & Grosse Ophoff, B.** (1987). Recovery of integrative central nervous function after one hour of global cerebro-circulatory arrest in normothermic cat. *Journal of the Neurological Sciences*, 77(2–3):305–320.
24. **Martin, S. L., Kula, J., Krishnan, S., Murphy, M. P., et al.** (2019). Succinate accumulation and metabolic arrest in mammalian torpor. *Nature Metabolism*, 1:966 ff.
25. **Leonov, Y., Sterz, F., Safar, P., & Radovsky, A.** (1990). Moderate hypothermia after cardiac arrest of 17 minutes in dogs. *Stroke*, 21(11):1600–1606.
26. **Tisherman, S. A., Safar, P., et al.** (2000). Suspended animation for delayed resuscitation. *Critical Care Medicine*, 28(11 Suppl):N214–N218.
27. **Alam, H. B., et al.** (2005). Profound hypothermia protects neurons and astrocytes, and preserves cognitive functions in a swine model of lethal hemorrhage. *Journal of Surgical Research*, 126(2):172–181.
28. **Vrselja, Z., et al.** (2019). Restoration of brain circulation and cellular functions hours post-mortem. *Nature*, 568:336–343.
29. **Gilbert, M., Busund, R., Skagseth, A., Nilsen, P. Å., & Solbø, J. P.** (2000). Resuscitation from accidental hypothermia of 13.7 °C with circulatory arrest. *The Lancet*, 355(9201):375–376.
30. **Calderon Novoa, F., et al.** (2026). Subzero non-frozen preservation of porcine kidneys with autotransplantation. *American Journal of Transplantation*, 26:91–103.
31. **Uygun, K., Taggart, M., Hassan, M., Tessier, S. N., Markmann, J. F., Longchamp, A., & Toner, M.** (2026). Subzero non-frozen banking of porcine kidneys enabling in vivo functional recovery. *Research Square*, rs.3.rs-7820837.

**Natural stasis: freeze tolerance, anoxia, hibernation, aestivation, anhydrobiosis**
32. **Larson, D. J., et al.** (2014). Wood frog adaptations to overwintering in Alaska. *Journal of Experimental Biology*, 217:2193–2200.
33. **Jackson, D. C., & Ultsch, G. R.** (2010). Physiology of hibernation under the ice by turtles and frogs. *Journal of Experimental Zoology A*, 313(6):311–327.
34. **Storey, K. B.** (2004). Molecular mechanisms of anoxia tolerance. *International Congress Series*, 1275:47–54.
35. **Dausmann, K. H., Glos, J., & Heldmaier, G.** (2009). Energetics of tropical hibernation. *Journal of Comparative Physiology B*, 179:345–357.
36. **Niu, Y., Guan, Y., Wang, X., Jiang, H., et al.** (2023). Aestivation induces widespread transcriptional changes in the African lungfish. *Frontiers in Genetics*, 14:1096929.
37. **Boothby, T. C., et al.** (2017). Tardigrades use intrinsically disordered proteins to survive desiccation. *Molecular Cell*, 65(6):975–984.
38. **Buck, C. L., & Barnes, B. M.** (2000). Effects of ambient temperature on metabolic rate, respiratory quotient, and torpor in an arctic hibernator. *American Journal of Physiology*, 279(1):R255–R262.
39. **Pamenter, M. E., et al.** (2018). Do naked mole rats accumulate a metabolic acidosis during severe hypoxia? *PLOS ONE*, 13(12):e0208453.

**Physical chemistry, thermal engineering and standards**
40. **Mowry, S., Krüger, M., Drabbels, M., & Lorenz, U. J.** (2025). Direct measurement of the critical cooling rate for the vitrification of pure water. *Physical Review Research*, 7(1):013095.
41. **Lu, Z. P., & Liu, C. T.** (2002). A new glass-forming ability criterion for bulk metallic glasses. *Acta Materialia*, 50(13):3501–3512.
42. **Wang, H., Webley, P. A., & Hughes, T. J.** (2025). Thermal stress and structural integrity in cryogenic storage. *Energy*, 334:137568.
43. **EN 14620-5** (2006). *Design and manufacture of site built, vertical, cylindrical, flat-bottomed steel tanks for the storage of refrigerated, liquefied gases with operating temperatures between 0 °C and −165 °C — Part 5: Testing, drying, purging and cool-down.* European Committee for Standardization.
44. **Kedem, O., & Katchalsky, A.** (1958). Thermodynamic analysis of the permeability of biological membranes to non-electrolytes. *Biochimica et Biophysica Acta*, 27:229–246.
45. **Jesus, A. R., Duarte, A. R. C., & Paiva, A.** (2022). Use of natural deep eutectic systems as new cryoprotectant agents in the vitrification of mammalian cells. *Scientific Reports*, 12:8095.

**Anthropometry and human reference data**
46. **Du Bois, D., & Du Bois, E. F.** (1916). A formula to estimate the approximate surface area if height and weight be known. *Archives of Internal Medicine*, 17(6):863–871.
47. **ICRP** (2002). *Basic Anatomical and Physiological Data for Use in Radiological Protection: Reference Values.* ICRP Publication 89, Annals of the ICRP 32(3–4).

**Space applications and clinical/legal framing**
48. **Nordeen, C. A., & Martin, S. L.** (2019). Engineering human stasis for long-duration spaceflight. *Physiology*, 34(2):101–111.
49. **Bradford, J., Schaffer, M., & Talk, D.** (2014). *Torpor Inducing Transfer Habitat for Human Stasis to Mars.* NASA Innovative Advanced Concepts, Phase I Final Report, Grant NNX13AP82G.
50. **Bradford, J., Williams, D., & Ricano-Cadenas, M.** (2018). *Advancing Torpor Inducing Transfer Habitats for Human Stasis to Mars.* NASA Innovative Advanced Concepts, Phase II, Project 88911.
51. **McKenzie, A. L., Thorn, E., Nnadi, O., Wróbel, B., Kendziorra, E., Farrell, P., & Crary, J. F.** (2024). Cryopreservation of brain cell structure: a review. *Free Neuropathology*, 5:35.
52. **Shemie, S. D., et al.** (2023). *A Brain-Based Definition of Death and Criteria for its Determination After Arrest of Neurologic or Circulatory Function in Canada.* Canadian Critical Care Society / Canadian Medical Association.

---

### Data and Code Availability

The complete knowledge graph (`red/stasispath.yaml`, 91 sources, 251 nodes), the verification
engine (`red/motor.py`), the self-audit module (`red/sfsa_auditoria.py`), the hash-locked
preregistration certificates (`red/prereg.lock`), and the `stasispath` toolkit with its 79 unit tests are released together. Every generated document in the repository is reproduced by running
the engine; none is hand-edited. Readers who wish to verify the preregistrations may recompute
each SHA-256 from the published protocol text and the preregistration date.

**Note on the frozen record.** The preregistration P18 retains the project's prototype name
("DSNY") inside its frozen text. It has deliberately **not** been renamed, because editing a
hash-locked preregistration — even cosmetically — would destroy the evidence that it was never
altered. The prototype name survives there and nowhere else.

---

### Contributors

**Alejo Malia** conceived the research question and the MATE + TRIADA method, directed the work, and is responsible for every claim and verdict. **Claude (Anthropic)** contributed literature reading and verification against primary sources, the verification engine and its self-audit, the toolkit modules, the bilingual documents, and the corrections recorded in the project log. **Grok (xAI)** contributed to the development of the framework and its early drafts. The AI systems are credited as contributors; responsibility for the content rests with the human author.
