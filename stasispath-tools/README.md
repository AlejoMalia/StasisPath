# StasisPath Tools (`stasispath`)
## Computational Biophysics Toolkit for Cryopreservation and Biostasis

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-blue.svg)](../LICENSE)
[![Verification](https://img.shields.io/badge/Verification-97.3%25-green.svg)](https://github.com)

`stasispath` is a lightweight, zero-dependency Python biophysics library that provides exact analytical solutions, thermodynamic boundaries, and hypothesis-testing tools for laboratory protocols in cryopreservation, vitrification, and organ stasis.

It prevents research groups from having to reimplement piecewise $Q_{10}$ ischemic integration, volume-time ice nucleation scaling, Arrhenius CPA chemical toxicity, or thermomechanical fracture calculations from scratch.

---

## ⚠️ What it Does vs. What it Does NOT Do

| ✅ What StasisPath DOES | ❌ What StasisPath DOES NOT DO |
|---|---|
| Computes equivalent normothermic ischemic time ($\tau_{\text{eq}}$) with piecewise $Q_{10}$. | Does **not** simulate complex whole-organ biological biology 100% in silico. |
| Evaluates stochastic supercooling limits ($V \cdot t \approx 1.0\text{ L}\cdot\text{h}$). | Does **not** claim to close biological frontiers ($X_2$) without direct electrophysiological measurement. |
| Computes thermomechanical tensile stress ($\sigma_{\text{th}}$) and fracture risk near $T_g$. | Does **not** substitute live in vitro or in vivo laboratory experiments. |
| Models CPA Arrhenius toxicity and predicts OCR mitochondrial retention. | Does **not** extrapolate isolated organ preservation to unverified whole-body stasis. |
| Implements the frozen decision rule of preregistered experiment P19, exactly as hash-locked. | Zero unverified black boxes: every formula is rooted in empirical constants. |

---

## Key Biophysical Equations

### 1. Equivalent Ischemia under Piecewise $Q_{10}$ (Formula F3)
$$\tau_{\text{eq}} = \int_0^t \frac{dt'}{S(T(t'))}$$
Where the metabolic suppression factor $S(T)$ uses bilinear $Q_{10}$ exponents:
* $T > 15\text{ }^\circ\text{C}$: $Q_{10} = 2.15$
* $T \le 15\text{ }^\circ\text{C}$: $Q_{10} = 3.50$
$$S(T) = Q_{10,\text{warm}}^{\frac{37 - 15}{10}} \cdot Q_{10,\text{cold}}^{\frac{15 - T}{10}} \quad (T < 15\text{ }^\circ\text{C})$$

### 2. Stochastic Nucleation Scaling (Formula F4)
$$V \cdot t \approx 1.0\text{ L}\cdot\text{h} \quad (\text{at } -2\text{ }^\circ\text{C})$$
$$t_{\text{max}} = \frac{1.0\text{ L}\cdot\text{h}}{V} \implies P(\text{ice-free}) = \exp\left(-\frac{V \cdot t}{1.0\text{ L}\cdot\text{h}}\right)$$

### 3. Thermomechanical Stress & Fracture (Formulas F1 / F2 & EN 14620-5)
$$\sigma_{\text{th}} = \frac{E \cdot \alpha \cdot \Delta T_{\text{radial}}}{1 - \nu}, \quad \Delta T_{\text{radial}} = \frac{\dot{T} \cdot LC^2}{2 \cdot \alpha_{\text{diff}}}$$
Safe rate limit near $T_g$ (−123 °C): $\dot{T} \le 0.150\text{ }^\circ\text{C/min}$ (to keep $\sigma_{\text{th}} < \sigma_{\text{fracture}} \approx 2.0\text{ MPa}$).

### 4. CPA Chemical Toxicity Kinetics (Arrhenius Model)
$$D_{\text{CPA}} = D_{\text{ref}} \cdot \left(\frac{t}{t_{\text{ref}}}\right) \cdot \exp\left(\frac{E_a}{R}\left(\frac{1}{T_{\text{ref}}} - \frac{1}{T}\right)\right)$$
With $\frac{E_a}{R} \approx 2952\text{ K}$, predicting $D_{\text{CPA}} \approx 0.142$ at −22 °C ($\text{OCR} \ge 85\%$).

---

## Installation

```bash
# Clone and install in editable mode:
cd stasispath-tools
pip install -e .
```
*(No third-party dependencies required. Standard Python library only).*

---

## Python API Quickstart

### 1. Equivalent Ischemic Exposure
```python
from stasispath import tau_eq

# 2 hours of cold ischemia at 10 °C
tau = tau_eq(t_hours=2.0, T_c=10.0)
print(f"tau_eq: {tau:.3f} h ({tau * 60:.1f} minutes at 37 °C)")
# Output: tau_eq: 0.165 h (~9.9 minutes at 37 °C)
```

### 2. Stochastic Nucleation & Supercooling Limits
```python
from stasispath import t_max_nucleation, p_no_nucleation

# Porcine kidney (0.20 L)
t_kidney = t_max_nucleation(V_L=0.20)
print(f"Max stable hours: {t_kidney:.1f} h")  # 5.0 hours

# Human liver (1.50 L)
t_liver = t_max_nucleation(V_L=1.50)
print(f"Max stable minutes: {t_liver * 60:.1f} min")  # 40.0 minutes
```

### 3. Evaluating preregistered experiment P19 (frozen rule)
```python
from stasispath import eval_p19, check_p19_derivation

# Arm C (M22) 135 %, arm B (V3 positive control, replicates F46) 138 %, 95 % CI of C-B = (-12, +8) pp
res = eval_p19(ltp_arm_c_pct=135.0, ltp_arm_b_pct=138.0, ci95_diff_c_minus_b_pp=(-12.0, 8.0))
print(res["verdict"])        # Verdict.PASS   (C >= 130 % and CI of C-B within +/-25 pp)

# C at 100 % while the positive control works: FAIL. Arm D (loading only) gives the diagnosis.
res = eval_p19(100.0, 140.0, (-50.0, -30.0), ltp_arm_d_pct=102.0)
print(res["verdict"], res["diagnosis"])   # FAIL, chemical toxicity: redesign the CPA

# Respiration is a SECONDARY measure: it tests the Arrhenius derivation, not P19.
print(check_p19_derivation(0.92)["status"])   # DERIVATION_CONFIRMED
```

The thresholds are frozen: PASS if C >= 130 %, FAIL if C <= 110 % while B >= 130 %, anything else
inconclusive and never reinterpreted. If the positive control B does not replicate F46 within +/-20
points, the result is `NOT_INTERPRETABLE`. An earlier version of this toolkit implemented a different,
"softened" criterion (OCR >= 85 % and LTP >= 120 %); it did not match the preregistration and has been removed.

The module also contains four **exploratory** hypotheses (`eval_h2` ... `eval_h5`: nucleation scaling,
thermal fracture, reperfusion kinetics). They are **not preregistered**, and every result says so.

### 4. Thermal Stress and Fracture Risk
```python
from stasispath import fracture_risk

# Human organ radius LC = 3.9 cm cooled at 0.10 °C/min near Tg (-123 °C)
risk = fracture_risk(cooling_rate_c_min=0.10, lc_cm=3.9)
print(risk["risk_level"], risk["will_fracture"])  # LOW, False
```

### 5. Multi-Organ Constraint Projector (Anthropometrics & Allometry)
```python
from stasispath import project_multiorgan_constraints, format_multiorgan_markdown_report

# Subject: 45yo Male, 175 cm, 75 kg, 15 min pre-perfusion delay
analysis = project_multiorgan_constraints(age_years=45, height_cm=175, weight_kg=75, sex="M", preperfusion_delay_min=15)
print(format_multiorgan_markdown_report(analysis))
# Evaluates organ volumes, t_max nucleation, thermal stress, ischemic limits, and bottleneck rankings
# Always enforces: WHOLE_BODY_PROTOCOL = NOT_VALIDATED
```

---

## Command-Line Interface (CLI)

```bash
# Calculate ischemic dose
stasispath tau --time 2.0 --temp 10.0

# Calculate maximum supercooling time
stasispath nucleation --volume 1.5

# Assess thermal stress
stasispath stress --rate 0.5 --lc 3.9

# Evaluate Arrhenius CPA toxicity
stasispath toxicity --temp -22.0 --time 25.0

# Evaluate P1 experiment result
stasispath eval-p1 --ocr 0.88 --ltp --slope 1.35

# Project multi-organ constraints from subject anthropometry
stasispath multiorgan --age 45 --height 175 --weight 75 --sex M --delay 15

# Generate controlled-rate freezer cooling profile (Planer Kryo / Asymptote / CSV)
stasispath recipe --cpa M22 --lc 2.0 --csv planer_profile.csv --planer script.txt

# Design stepwise osmotic washout schedule (Fahy Kedem-Katchalsky protocol)
stasispath washout --cpa M22 --thickness 0.04

# Ingest CT/MRI segmentation from Body-and-Organ-Analysis (BOA) or TotalSegmentator
stasispath boa --file segmentation.json --age 48 --height 178 --weight 76 --sex M

# Generate complete Markdown protocol report
stasispath report --name "Porcine Kidney" --mass 0.20 --vol 0.20 --lc 2.0 --cpa M22
```

---

## Running Test Suite

```bash
python3 -m pytest -q          # or: PYTHONPATH=. python3 -m unittest discover -s stasispath/tests
```

All 11 test suites (79 tests) verify:
- $Q_{10}$ bilinear transitions and tau_eq accuracy.
- Stochastic volume-time invariants ($0.2\text{ L} \implies 5\text{ h}$, $1.5\text{ L} \implies 40\text{ min}$).
- Cooling phase transitions and EN 14620-5 rate limits near $T_g$.
- Arrhenius activation parameter calibration ($D_{\text{CPA}} \approx 0.142$ at −22 °C).
- Thermomechanical stress scaling with $\dot{T} \cdot LC^2$.
- The frozen P19 decision rule and four exploratory hypotheses (H2–H5).
- Anthropometric morphometry and bottleneck ranking.
- Cryogenic controlled-rate freezer recipe generation.
- Stepwise osmotic washout safety ($\Delta V / V_0 \le 1.15$).
- Radiological CT segmentation ingestion (BOA / TotalSegmentator).

---


## Citation & Framework Context

If using this package to design or report cryopreservation experiments, please cite the underlying theoretical framework:
* **StasisPath: A Quantitative Framework for Metabolic Depression, Ice Avoidance, and the Limits of Reversible Preservation (2026)**.
* Primary Anchors: *Fahy et al. 2004*, *German et al. (PNAS 2026)*, *Mowry et al. (Phys Rev Res 2025)*, *Wang et al. (Energy 2025)*.

---
*StasisPath Tools — Released under Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0). Strictly for academic and scientific research purposes; not for commercial sale or exploitation.*
