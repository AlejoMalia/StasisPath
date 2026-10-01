# DESIGN TABLES, BOUNDS AND EXPERIMENTAL GAPS
## A Biophysical Guide for Cryopreservation and Biostasis Laboratories (StasisPath 2026)

This document organizes the StasisPath framework into **operational dimensions**, with measured quantitative coordinates, thermodynamic bounds, toxicity models and tightly bounded experimental gaps. It gives cryobiology, biophysics and transplant laboratories the specifications needed to optimize protocols and test the frontier without computational redundancy or methodological ambiguity.

*Spanish original: [`es/TABLAS_DE_DISENO_Y_HUECOS_LAB.md`](../es/TABLAS_DE_DISENO_Y_HUECOS_LAB.md).*

---

> [!CAUTION]
> ### NUMERICAL LIMITS AND EPISTEMIC FRONTIER: THE "WE DO NOT CLAIM" BOX
> * We do **not** claim that reversible whole-body stasis in adult non-hibernating mammals is viable today, nor that any published protocol can achieve it.
> * We do **not** claim that successes at cell scale ($E_5$) or slice/microtissue scale ($E_2$) translate trivially to vascularized organs ($E_3$) or to whole organisms ($E_0$). Every extrapolation from isolated organ to whole body is currently **strictly an unresolved theoretical conjecture**.
> * We do **not** close frontier $X_2$ by simulation: closing $X_2$ requires direct in vitro electrophysiological testing under the frozen decision rule of preregistered experiment P19.

---

## 1. Biological Scale: From the Cell to the Whole Organism

| Scale / Level | Typical mass / $LC$ | Ontological level | State in the framework | Limiting organ or tissue | Dominant physical/biological damage | Leading verified protocol | Open experimental gap |
|---|---|---|---|---|---|---|---|
| **Cell / suspension** | $< 10^{-6}\text{ g}$<br>($LC < 10\text{ }\mu\text{m}$) | $E_5$<br>(full function, clonogenic) | **[MEASURED]** | Plasma membrane | Osmotic lysis and intracellular nucleation | Slow freezing (1 °C/min) with 10 % DMSO, or ultrafast vitrification | None conceptually. Solved domain. |
| **Slice / microtissue** | $10^{-3} - 10^{-2}\text{ g}$<br>($LC \approx 0.1–0.4\text{ mm}$) | $E_2$<br>(LTP, active synapse) | **[MEASURED]** | Pyramidal neuron (CA1, DG) | Mitochondrial chemical toxicity at concentrations $> 8.4\text{ M}$ | **V3 (59 % w/v)** with subzero loading and directional cooling at 130 °C/s (German et al., *PNAS* 2026) | Fast cooling is mandatory; does not scale to thick organs. |
| **Small organ** | $1 - 15\text{ g}$<br>($LC \approx 0.5–1.0\text{ cm}$) | $E_3$<br>(post-transplant viability) | **[MEASURED]** | Renal cortex and microvasculature | Devitrification during slow conductive rewarming | **Inductive nanowarming** with sIONPs in rat kidney (5/5 survival at 100 days, Han et al. 2023); supercooling at −6 °C (Bruinsma 2015) | Homogeneous nanoparticle distribution and complete vascular washout without aggregates. |
| **Large organ** | $150 - 1500\text{ g}$<br>($LC \approx 1.5–3.9\text{ cm}$) | $E_3$ (partial in pig)<br>$E_0$ (in human) | **[BOUNDED]** | Inner renal medulla / vascular endothelium | Slow thermal conduction (Fourier, $C_3$), CPA toxicity from diffusion time | **Partial freezing at −15 °C** for 10 days (Uygun 2026, porcine in vivo autotransplant with urine output); **M22 at −22 °C/−45 °C** (Fahy 2004, 8/8 survival) | **X2**: demonstrate active electrophysiology (durable LTP) in neural tissue with a low-CCR CPA ($\le 0.43\text{ }^\circ\text{C/min}$). |
| **Multi-organ / block** | $5 - 15\text{ kg}$<br>($LC \approx 4.0–6.0\text{ cm}$) | $E_1$<br>(histological integrity) | **[BOUNDED]** | Pulmonary endothelium and blood–brain barrier | *No-reflow*, vasogenic oedema, diffusion heterogeneity between parenchymas | Stepwise subnormothermic perfusion (SNMP) and oncotic vehicles (PEG 35k) | Simultaneous perfusion of organs with disparate osmotic profiles without endothelial lysis. |
| **Whole organism** | $70\text{ kg}$<br>($LC \approx 7.5\text{ cm}$ in trunk) | $E_0$<br>(structural preservation) | **[OPEN]** | Centre of the trunk / deep splanchnic mass | Impossibility of cooling the centre without crossing small-molecule toxicity ($F_2$ requires $>9.5\text{ M}$); mechanical fracture ($C_1$) | Post-mortem field cryoprotection (de Wolf 2025; Alcor P-19) | **No protocol exists for reversible total stasis in an adult non-hibernating mammal.** |

---

## 2. Comparative Cryoprotectant (CPA) Toxicity

This table summarizes the operational profile of the main vitrifying agents evaluated in the biophysical literature, against the experimental bound still pending characterization in our own laboratory:

| CPA formulation | Typical molarity (M) | Conc. (% w/v) | Reference $\text{CCR}$ | Observed relative toxicity | Mechanistic note and limitation | StasisPath laboratory datum |
|---|---|---|---|---|---|---|
| **DP6** | ~6.0 M | ~38.8 % w/w | ~40.0 °C/min | **Low–moderate** | Requires ultrafast warming (>180 °C/min) to avoid devitrification. | Comparative slice assay pending |
| **VS55 (VS41A)** | 8.4 M | 55.0 % | ~2.5 °C/min | **Severe** | Endothelial toxicity and irreversible depolarization; unsuited to normothermic perfusion. | Recorded at node $F_3$ / $F_{65}$ |
| **VMP** | 8.4 M | 55.0 % | ~5.4 °C/min | **Moderate** | Bridging solution with ice blockers (X-1000/Z-1000); tolerates fast perfusion at −3 °C. | Recorded at node $F_1$ |
| **V3** | 8.42 M | 59.0 % | ~147.0 °C/min | **Tolerable at subzero** | Preserves LTP (German 2026), but its CCR is unviable for organs thicker than $0.5\text{ mm}$. | Validated at node $F_{46}$ / $F_{71}$ |
| **M22** | 9.345 M | 64.8 % | **0.10 °C/min** | **High above 0 °C / low at −22 °C** | Vitrifies at organ scale ($LC^* > 3.5\text{ cm}$); damage kinetically mitigated by cold. | **P19: fEPSP/LTP characterization pending** |
| **NADES** | n/a (mixtures of variable molar mass) | 50 % w/v | **> 30 °C/min (MEASURED: they crystallize in DSC at 30 °C/min)** | **Limited: the primary source itself sets 50 % w/v as the ceiling because of toxicity and viscosity** | Natural eutectics protect cell lines by direct N₂ immersion, but they crystallize at 30 °C/min and do not vitrify large volumes. Their "vitrification" is the immersion of a cryovial. | Recorded at node $F_{80}$ |
| **CAHS proteins** | ~0.0006 M | 1.5 % (15 g/L) | In-situ gel | **None** | Macromolecular vitrification by steric arrest, on drying not on cooling; no osmotic toxicity. | Recorded at node $F_{74}$ |

---

## 3. Reperfusion and Rewarming Matrix: Mechanisms by Critical Phase

Failure of viability in cryopreservation occurs not only during cooling but predominantly at phase transitions and physiological return:

| Process phase | Thermal range | Dominant critical phenomenon | Biophysical / biochemical cause | Cellular / physiological damage | Validated mitigation strategy |
|---|---|---|---|---|---|
| **Phase A: Cryogenic rewarming I** | $-196\text{ }^\circ\text{C} \rightarrow T_g$ (−123 °C) | **Thermomechanical fracture** | Differential volumetric contraction and expansion ($\sigma_{\text{th}} \approx \frac{E \cdot \alpha \cdot \Delta T}{1 - \nu}$) | Macroscopic fractures and severing of vascular beds | Ultra-slow rate control ($< 0.150\text{ }^\circ\text{C/min}$) near $T_g$ (Wang 2025; EN 14620-5) |
| **Phase B: Cryogenic rewarming II** | $T_g \rightarrow T_m$ (−123 °C to −55 °C) | **Devitrification and recrystallization** | Uncontrolled growth of metastable ice nuclei by thermal kinetics | Complete mechanical cell lysis of the parenchyma | **Inductive volumetric nanowarming** by radiofrequency with sIONPs (>50 °C/min homogeneous, Han 2023) |
| **Phase C: CPA washout** | −22 °C $\rightarrow$ 0 °C | **Osmotic shock and oedema** | Abrupt removal of external solutes with rapid water efflux/influx from chemical imbalance | Osmotic membrane lysis and endothelial detachment (massive LDH rise) | Non-linear stepwise dilution mediated by impermeant osmotic-support solutes (**mannitol 300 mM**) |
| **Phase D: Reoxygenation and flow** | 0 °C $\rightarrow$ 37 °C | **Succinate ROS burst** | Succinate accumulation during arrest; sudden hyperoxidation at mitochondrial complex II when normothermic flow is induced | Fulminant oxidative stress, cardiolipin peroxidation and mPTP opening | Infusion of reversible succinate-dehydrogenase inhibitors (**dimethyl malonate**) in early reperfusion |
| **Phase E: Microvascular reperfusion** | 37 °C continuous | **No-reflow syndrome** | Pericyte and endothelial oedema with collapse of the capillary lumen and platelet hyperadhesion | Post-reperfusion ischemic necrosis despite adequate macrovascular perfusion | Stepwise subnormothermic perfusion (SNMP, 21 °C $\rightarrow$ 37 °C) with oncotic colloids (**PEG 35k**) |

---

## 4. Domains of Metabolic Regulation (Beyond $Q_{10}$)

| Suppression mechanism | Active thermal range | Metabolic depression achieved | Obeys Arrhenius ($Q_{10}$)? | Key molecular mechanism | Physiological breaking limit |
|---|---|---|---|---|---|
| **Passive hypothermia (non-hibernating mammal)** | 37 °C $\rightarrow$ 10 °C | 50 % per 10 °C ($Q_{10} = 2.0–2.3$ above $15\text{ }^\circ\text{C}$; $Q_{10}=3.5$ below $15\text{ }^\circ\text{C}$) | **YES** (enzymatic thermal kinetics) | Passive slowing of enzymatic reactions; early collapse of complex V | Cardiac arrest by ventricular fibrillation below $28\text{ }^\circ\text{C}$; $\tau_{\text{eq}} \le 45\text{ min}$ at 10 °C |
| **Hibernator torpor (*Ictidomys*, *Cheirogaleus*)** | 12 °C $\rightarrow$ −2 °C | Down to 1–3 % of the euthermic basal rate | **NO** (breaking domain of $F_3$: flat rate between 0 and 12 °C) | Active inhibition by reversible phosphorylation of complexes I/II; switch to purely lipid substrate (RQ = 0.70) | Limit set by availability of non-lipid fuel and nitrogen ($L_{28}$); reactive thermogenesis if $T < 0\text{ }^\circ\text{C}$ |
| **Ectotherm anoxia (*Trachemys scripta*)** | 20 °C $\rightarrow$ 3 °C | 10–20 % at 20 °C;<br>**0.5 % at 3 °C** (<0.01 % of a mammal) | **NO** (regulated channel arrest) | Suppressed depolarization, brain GABA raised $\times 80$, massive lactate buffering by shell carbonate | Buffering capacity of the mineral skeleton; unviable in mammals without a shell because of lethal lactic acidosis |
| **Ontogenic brain sparing (fetus/neonate)** | 37 °C (fetus)<br>30 °C (neonate) | Selective fall in cerebral demand with bradycardia (25–60 %) | Partially | Adenosine $A_1$ receptors, opening of $K_{\text{ATP}}$ channels, selective preservation of carotid flow | Postnatal maturation of glutamate excitotoxicity (lost within weeks of birth) |
| **Pharmacological synthetic torpor** | 37 °C $\rightarrow$ 32–34 °C | 30–50 % reduction in metabolic rate | Pharmacologically regulated | Stimulation of hypothalamic Q neurons, adenosine agonists ($A_1R$, CHA) | Requires mechanical ventilatory support and continuous parenteral nutrition (Bradford NASA NIAC) |

---

## 5. Experimental and Regulatory Implementation Matrix

| Experimental level | Subject / model | Regulatory and legal framework | Maturity (TRL) | Cost / complexity | Key advantage and what it establishes |
|---|---|---|---|---|---|
| **In vitro / slice** | Primary culture, murine hippocampal slices | Standard animal-experimentation ethics committees (IACUC) | TRL 2–3 | Low / fast | Pure molecular toxicity, synaptic viability (LTP, fEPSP), mitochondrial respiration (OCR). |
| **Rodent organ** | Rat kidney or liver | Standard IACUC committees | TRL 4 | Medium | Real orthotopic vascular transplantation in vivo; organ survival and function at 100 days. |
| **Porcine organ in vivo** | Yorkshire pig (30–50 kg) | Major preclinical animal-transplant regulation | TRL 5 | High | Translational model identical in scale to human organs; glomerular filtration and urine output in vivo. |
| **Discarded human surgical organ / non-transplantable donor** | Human kidney / liver / biopsies unsuitable for grafting (e.g. KDPI > 85, severe steatosis, partial tumour resections) | Local IRB approval + consent for donation to biomedical research (UAGA / transplant law) | **TRL 3–5** | **Medium–high** / access feasible via OPO/bank | **Critical bridge between rodent and clinic**: real human vasculature without cadaveric artefacts. Excellent $\tau_{\text{eq}}$ if cannulated immediately in the operating room. Allows ex vivo normothermic perfusion. |
| **Emergency clinical trials** | Human patients in cardiovascular surgery or exsanguinating trauma | FDA/EMA approval under emergency exception from informed consent (EFIC, 21 CFR 50.24) | TRL 6–7 | Extreme | Ultra-short therapeutic hypothermia (<45 min in DHCA; minutes in EPR). Not suitable for prolonged storage. |
| **Field cadaveric preservation** | Legal post-mortem whole-body anatomical donation | Uniform Anatomical Gift Act (UAGA) | TRL 1–2 | Logistically complex | Whole-body field perfusion; penalized by warm post-arrest ischemia ($\tau_{\text{eq}} \gg 10\text{ min}$) and medico-legal delay. |

---

## 6. Concrete Falsifiable Predictions for the Laboratory

**Prediction 1 is P19, a frozen, hash-protected preregistration** (`red/prereg.lock`). **Predictions 2 to 5 are exploratory laboratory hypotheses, NOT preregistered.** All carry quantitative falsification criteria:

### Prediction 1 (Experiment P19, frozen preregistration: does a hippocampus vitrified with a chemistry that scales preserve LTP?)
* **Test condition**: 350 µm adult mouse hippocampal slices; four arms, $n \ge 8$ slices from $\ge 4$ animals per arm, blind recording: **(A)** unvitrified control · **(B)** V3 (replicate of F46, positive control) · **(C)** M22 at its working concentration (VMP preload at 0 °C, M22 at −22 °C, washout simultaneous with warming) · **(D)** loading and unloading of M22 without cooling.
* **Primary variable**: LTP in SC–CA1 at 60 min after HFS (100 Hz, 1 s), as % of baseline fEPSP.
* **Decision rule (frozen, not reinterpreted)**:
  1. **PASS** if arm C reaches $\ge 130\ \%$ and does not differ from B (95 % CI of the difference within ±25 percentage points).
  2. **FAIL** if C $\le 110\ \%$ while B $\ge 130\ \%$.
  3. Between 110 and 130 %, or with B failed: **inconclusive**.
  4. **Quality control**: B must replicate F46 (138.1 %) within ±20 percentage points; otherwise the experiment is not interpretable and is repeated before reading C.
* **Diagnosis from arm D**: if D fails like C, the damage is **chemical toxicity** and the CPA must be redesigned; if D passes and C fails, the damage is **thermal or from devitrification**.
* **Secondary measure (not a threshold)**: basal respiration (OCR). The Arrhenius derivation predicts damage $D_{\text{CPA}} = 0.142$ in arm C (OCR retention ≈ 86 %); a damage $> 0.25$ would refute that **derivation** (contradiction I1), not P19.
* *Editorial note*: an earlier version of this guide set a "double threshold" (OCR $\ge 85\ \%$ and LTP $\ge 120$–$150\ \%$). It did not match the frozen preregistration and has been replaced by the rule above.

### Prediction 2 (exploratory, not preregistered; Formula F4: time limit of supercooling by stochastic nucleation)
* **Test condition**: biological volume of $1.5\text{ L}$ (equivalent to an adult human liver) supercooled at −2 °C without specific antinucleating agents.
* **Calculation from a single-anchor hypothesis ($V \cdot t \approx 1.0\text{ L}\cdot\text{h}$; the framework records it as a falsifiable hypothesis, not as a valid derivation)**:
  $$t_{\text{max without nucleation}} \le 40\text{ minutes}$$
* **Falsification criterion**: if the organ remains $> 3\text{ hours}$ at −2 °C in 10 consecutive repetitions without freezing, the stochastic invariant $V \cdot t$ is **refuted** in favour of a regime dominated by interfacial heterogeneous nucleation at the container.

### Prediction 3 (exploratory, not preregistered; Formula F1/F2: thermal fracture threshold in a large organ)
* **Test condition**: passive convective cooling of an organ with $LC \ge 3.9\text{ cm}$ perfused with M22 while crossing $T_g$ (−123 °C).
* **Analytical calculation**: at rates $> 0.150\text{ }^\circ\text{C/min}$, the radial gradient generates thermal stresses $\sigma_{\text{th}} > \sigma_{\text{fracture}} \approx 2.0\text{ MPa}$.
* **Falsification criterion**: the reproducible absence of vascular/tissue microfractures detected by cryogenic computed tomography or cryomacroscopy at rates $> 1.0\text{ }^\circ\text{C/min}$ refutes the thermomechanical limit of Wang/EN 14620-5 for vitreous tissue matrices.

### Prediction 4 (exploratory, not preregistered; in vitro post-P19 reperfusion: functional-recovery kinetics)
* **Test condition**: hippocampal slices exposed to the full P19 protocol (M22 at −22 °C, mannitol washout) subjected to continuous superfusion with oxygenated normothermic ACSF ($95\%\text{ O}_2 / 5\%\text{ CO}_2$) at 32 °C for 60 minutes.
* **Derived calculation**: removal of the CPA must not induce secondary lysis through residual osmotic stress nor a fulminant necrotic cascade.
* **Falsification criterion**:
  * At 30 minutes of continuous normothermic reperfusion, mitochondrial $\text{OCR}$ must be $\ge 70\text{ \%}$ of the value measured immediately after washout.
  * No progressive failure or extinction of the population-spike amplitude (fEPSP) may be observed between minute 15 and minute 60 of continuous recording.
  * A progressive fEPSP fall $> 50\text{ \%}$ over that interval with a continuous rise of LDH in the bath would falsify the viability of the stepwise washout protocol.

### Prediction 5 (exploratory, not preregistered; volumetric nucleation scaling in renal organ: $V \cdot t \approx 1.0\text{ L}\cdot\text{h}$)
* **Warning**: the 0.2 L and 5 h datum is exactly the anchor of the hypothesis; a success here is a **replication**, not an independent test.
* **Test condition**: pig kidneys ($V \approx 0.15–0.20\text{ L}$) supercooled at −2 °C in medium free of exogenous ice nuclei.
* **Derived calculation**:
  $$t_{\text{theoretical stability}} \approx \frac{1.0\text{ L}\cdot\text{h}}{0.20\text{ L}} = 5.0\text{ hours}$$
* **Falsification criterion and interfacial diagnosis**:
  * If the mean stability observed in 5 consecutive trials is $5.0 \pm 1.5\text{ h}$, the volumetric stochastic model is verified.
  * If the kidney systematically nucleates at $t < 1.0\text{ hour}$ in the same container where identical volumes of saline remain supercooled $> 6\text{ h}$, it is shown that nucleation **is not governed by intrinsic volume** but by surface heterogeneity (renal capsule, catheters or vascular seal), steering laboratory design toward surface-passivation agents.

---
*Biophysical laboratory specification document integrated into the StasisPath analytical system — Version 2.5 (2026), corrected 2026-10.*
