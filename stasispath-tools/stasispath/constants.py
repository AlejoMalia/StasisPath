"""
Physical, thermodynamic, and biological constants for the StasisPath framework.
All values are tied to empirical anchors in the StasisPath knowledge graph.
"""

from typing import Final, Dict

# --- Biological Reference Temperatures (°C) ---
T_NORMOTHERMIA_C: Final[float] = 37.0
T_DEEP_HYPOTHERMIA_DHCA_C: Final[float] = 18.0
T_HIBERNATION_MIN_C: Final[float] = -2.0
T_HIBERNATION_TORPOR_C: Final[float] = 4.0
T_SUBZERO_LOADING_M22_C: Final[float] = -22.0
T_SUBZERO_LOADING_VMP_C: Final[float] = -3.0

# --- Vitrification & Phase Transition Anchors (°C) ---
T_GLASS_M22_C: Final[float] = -123.0    # Tg for M22 (150.15 K)
T_FREEZING_M22_C: Final[float] = -55.0  # Tm for M22
T_LIQUID_NITROGEN_C: Final[float] = -196.0

# --- Piecewise Q10 Parameters (Mammalian non-hibernating) ---
Q10_WARM: Final[float] = 2.15           # T > 15 °C (range 2.0 - 2.3)
Q10_COLD: Final[float] = 3.50           # T <= 15 °C (range 3.0 - 4.0)
T_Q10_TRANSITION_C: Final[float] = 15.0

# --- Critical Cooling Rates (CCR) in °C/min ---
CCR_VALUES_C_MIN: Final[Dict[str, float]] = {
    "PURE_WATER": 3.84e8,
    # "V3": 147.0 is the cooling rate German et al. USED (> 2.45 C/s). The true CCR was not measured and is at most this value.
    "V3": 147.0,
    # "DP6": 40.0 has NO source in the StasisPath knowledge graph. Treat it as unverified.
    "DP6": 40.0,
    # "NADES": NOT A CONSTANT. No peer-reviewed CCR exists for any NADES formulation.
    # The framework measured the opposite behaviour: NADES at 50 % w/v CRYSTALLIZE
    # (Tc onset -26.6 C), i.e. they vitrify WORSE than DMSO. Use
    # design_spec.screen_candidate_cpa("NADES", None) -> UNMEASURED, and run a DSC.
    "VMP": 5.4,
    "VS55": 2.5,
    "M22": 0.10,
    "M22_HUMAN_CORTEX": 1.0,  # F47 DSC biopsy upper bound
}

# --- Critical Warming Rates (CWR) in °C/min ---
CWR_VALUES_C_MIN: Final[Dict[str, float]] = {
    "V3": 200.0,
    "DP6": 189.0,
    "VS55": 50.0,
    "VMP": 62.0,
    "M22": 0.43,
}

# --- Nucleation Stochastic Scaling Anchor (Formula F4) ---
# Empirical anchor: porcine/human organ scale at -2 °C
VT_STOCHASTIC_ANCHOR_L_H: Final[float] = 1.0  # V * t ≈ 1.0 L·h

# --- Thermomechanical Fracture Limits (Formulas F1 / F2 & EN 14620-5) ---
MAX_COOLING_RATE_NEAR_TG: Final[float] = 0.150  # °C/min around Tg (-123 °C)
SIGMA_FRACTURE_MPA: Final[float] = 2.0          # Critical tensile stress for cracking in vitreous tissue
YOUNG_MODULUS_VITREOUS_GPA: Final[float] = 1.2   # ~1.0-1.5 GPa below Tg
POISSON_RATIO_VITREOUS: Final[float] = 0.35
THERMAL_EXPANSION_COEFF_PER_K: Final[float] = 5.0e-5  # ~50 ppm/K

# --- CPA Chemical Toxicity Model (Arrhenius Ea/R) ---
ARRHENIUS_EA_R_K: Final[float] = 2952.0  # Derived activation parameter
D_CPA_P19_COLD_PREDICTED: Final[float] = 0.142  # Damage at -22 °C, 25 min
D_CPA_P19_WARM_PREDICTED: Final[float] = 0.540  # Damage at +10 °C, 25 min
