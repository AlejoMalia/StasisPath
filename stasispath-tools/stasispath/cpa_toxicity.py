"""
CPA Toxicity Module: Arrhenius Reaction Kinetics and Chemical Damage Modeling.
Implements the Arrhenius kinetic derivation calibrated from experiment P19.
"""

import math
from typing import Dict, Any
from stasispath.constants import (
    ARRHENIUS_EA_R_K,
    D_CPA_P19_COLD_PREDICTED,
    D_CPA_P19_WARM_PREDICTED,
)
from stasispath.units import celsius_to_kelvin, validate_positive


def arrhenius_factor(
    T_c: float,
    ref_T_c: float = 0.0,
    ea_r_k: float = ARRHENIUS_EA_R_K,
) -> float:
    """
    Computes the temperature acceleration/deceleration factor for CPA chemical toxicity:
        Factor = k(T) / k(T_ref) = exp( (Ea / R) * (1 / T_ref_K - 1 / T_K) )

    Args:
        T_c: Current tissue temperature in °C.
        ref_T_c: Reference temperature in °C (default: 0.0 °C).
        ea_r_k: Activation energy divided by gas constant (Ea / R in Kelvin).

    Returns:
        Relative kinetic rate factor (dimensionless).
    """
    t_k = celsius_to_kelvin(T_c)
    ref_k = celsius_to_kelvin(ref_T_c)

    exponent = ea_r_k * ((1.0 / ref_k) - (1.0 / t_k))
    return math.exp(exponent)


def d_cpa_predicted(
    T_c: float,
    t_exposure_min: float = 25.0,
    cpa: str = "M22",
    ea_r_k: float = ARRHENIUS_EA_R_K,
) -> float:
    """
    Predicts fractional metabolic/mitochondrial damage D_CPA accumulated
    during CPA exposure at temperature T_c.

    Calibration:
        - At -22 °C for 25 min: D_CPA ≈ 0.142 (OCR retention ≥ 85%)
        - At +10 °C for 25 min: D_CPA ≈ 0.540 (OCR drops to ~46-50%)

    Args:
        T_c: Exposure temperature in °C.
        t_exposure_min: Exposure time in minutes.
        cpa: Formulation name (default: M22).
        ea_r_k: Arrhenius activation parameter.

    Returns:
        Dimensionless damage index D_CPA (0.0 = zero damage, 1.0 = total mitochondrial arrest).
    """
    validate_positive(t_exposure_min, "t_exposure_min")

    # Baseline anchor: D_CPA at -22 °C for 25 min
    t_ref_c = -22.0
    t_ref_min = 25.0
    d_ref = D_CPA_P19_COLD_PREDICTED

    # Scale by Arrhenius factor and exposure duration
    rate_factor = arrhenius_factor(T_c, ref_T_c=t_ref_c, ea_r_k=ea_r_k)
    time_factor = t_exposure_min / t_ref_min

    d_pred = d_ref * rate_factor * time_factor
    return min(1.0, max(0.0, d_pred))


def predicted_ocr_retention(
    T_c: float,
    t_exposure_min: float = 25.0,
    cpa: str = "M22",
) -> Dict[str, Any]:
    """
    Computes expected mitochondrial Oxygen Consumption Rate (OCR) retention
    relative to fresh unfrozen tissue.

    Args:
        T_c: Temperature during loading (°C).
        t_exposure_min: Exposure duration (min).
        cpa: Formulation (default: M22).

    Returns:
        Dict with predicted OCR fraction, D_CPA, and protocol safety assessment.
    """
    d_cpa = d_cpa_predicted(T_c, t_exposure_min, cpa=cpa)
    ocr_retention = 1.0 - d_cpa

    is_safe = ocr_retention >= 0.85
    is_compromised = ocr_retention < 0.75

    status = (
        "SAFE_SUBZERO_PRESERVED"
        if is_safe
        else ("LETHAL_OR_COMPROMISED" if is_compromised else "MARGINAL_ACCEPTABLE")
    )

    return {
        "cpa": cpa,
        "temperature_c": T_c,
        "exposure_minutes": t_exposure_min,
        "d_cpa": d_cpa,
        "predicted_ocr_percent": ocr_retention * 100.0,
        "status": status,
        "meets_p19_metabolic_target": is_safe,
    }
