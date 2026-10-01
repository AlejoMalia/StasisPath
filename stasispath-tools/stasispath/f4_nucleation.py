"""
F4 Nucleation Module: Stochastic Ice Nucleation Kinetics and Volume-Time Scaling.
Implements Formula F4 from the StasisPath Framework: V * t ≈ 1.0 L·h anchor.
"""

import math
from typing import Optional, Dict, Any
from stasispath.constants import VT_STOCHASTIC_ANCHOR_L_H
from stasispath.units import validate_positive


def vt_product(V_L: float, t_hours: float) -> float:
    """
    Computes the Volume-Time product for supercooled liquid stability:
        VT = V * t  [L·h]

    Args:
        V_L: Sample or organ volume in Liters.
        t_hours: Duration of supercooling in hours.

    Returns:
        VT product in L·h.
    """
    validate_positive(V_L, "V_L")
    validate_positive(t_hours, "t_hours")
    return V_L * t_hours


def t_max_nucleation(V_L: float, vt_anchor: float = VT_STOCHASTIC_ANCHOR_L_H) -> float:
    """
    Computes the characteristic stochastic nucleation time limit:
        t_max = (V·t)_anchor / V

    At t = t_max, the cumulative probability of ice nucleation reaches ~63.2%
    (P_survival = exp(-1) ≈ 36.8%).

    Examples:
        - Porcine kidney (0.2 L): ~5.0 hours
        - Human liver (1.5 L): ~0.67 hours (40 minutes)

    Args:
        V_L: Volume in Liters.
        vt_anchor: Stochastic invariant anchor in L·h (default: 1.0 L·h at -2 °C).

    Returns:
        Maximum supercooling duration in hours before stochastic nucleation.
    """
    validate_positive(V_L, "V_L")
    validate_positive(vt_anchor, "vt_anchor")
    return vt_anchor / V_L


def p_no_nucleation(
    V_L: float,
    t_hours: float,
    vt_anchor: float = VT_STOCHASTIC_ANCHOR_L_H,
    J_rate: Optional[float] = None,
) -> float:
    """
    Calculates the Poisson survival probability of remaining completely ice-free:
        P(0 nuclei) = exp( - J * V * t ) = exp( - (V * t) / (V·t)_anchor )

    Args:
        V_L: Volume in Liters.
        t_hours: Exposure duration in hours.
        vt_anchor: Stochastic invariant anchor in L·h (default: 1.0).
        J_rate: Optional direct nucleation rate density in (L·h)^(-1).

    Returns:
        Probability between 0.0 and 1.0 of remaining free of ice nucleation.
    """
    validate_positive(V_L, "V_L")
    validate_positive(t_hours, "t_hours")

    if J_rate is not None:
        validate_positive(J_rate, "J_rate")
        exponent = J_rate * V_L * t_hours
    else:
        validate_positive(vt_anchor, "vt_anchor")
        exponent = (V_L * t_hours) / vt_anchor

    return math.exp(-exponent)


def heterogeneous_nucleation_rate(V_L: float, t_mean_observed_h: float) -> float:
    """
    Derives the effective empirical nucleation rate density J [L^-1 · h^-1]
    from measured mean time to freezing:
        J = 1 / (V * t_mean)

    Args:
        V_L: Volume in Liters.
        t_mean_observed_h: Mean time to freezing across experimental trials (hours).

    Returns:
        Nucleation rate density in (L·h)^(-1).
    """
    validate_positive(V_L, "V_L")
    validate_positive(t_mean_observed_h, "t_mean_observed_h")
    return 1.0 / (V_L * t_mean_observed_h)


def diagnose_nucleation_mechanism(
    V_L: float,
    t_observed_h: float,
    t_saline_control_h: float,
    vt_anchor: float = VT_STOCHASTIC_ANCHOR_L_H,
) -> Dict[str, Any]:
    """
    Diagnoses whether ice nucleation is governed by intrinsic volume kinetics
    or by container/interfacial artifacts (e.g. catheter edges, vessel clamps, wall defects).

    Args:
        V_L: Organ volume in Liters.
        t_observed_h: Measured time until freezing in the organ.
        t_saline_control_h: Measured time until freezing of pure saline in the identical container.
        vt_anchor: Theoretical volume anchor (default 1.0 L·h).

    Returns:
        Dict with diagnostic verdict, predicted time, and lab recommendations.
    """
    validate_positive(V_L, "V_L")
    validate_positive(t_observed_h, "t_observed_h")
    validate_positive(t_saline_control_h, "t_saline_control_h")

    t_pred = t_max_nucleation(V_L, vt_anchor=vt_anchor)
    ratio_to_pred = t_observed_h / t_pred

    if t_observed_h < 0.25 * t_pred and t_saline_control_h >= 2.0 * t_observed_h:
        verdict = "SURFACE_OR_CONTAINER_DOMINATED"
        recommendation = (
            "Premature nucleation observed. Nucleation is triggered by container interfaces, "
            "surface roughness, vascular clamps, or air-fluid bubbles. "
            "Passivate vessel walls and apply surfactant/oil sealing layers."
        )
    elif ratio_to_pred >= 0.6 and ratio_to_pred <= 1.6:
        verdict = "VOLUME_STOCHASTIC_CONFIRMED"
        recommendation = (
            "Observed nucleation aligns with the intrinsic stochastic volume limit (Formula F4). "
            "Scaling to larger volumes will strictly require ice blockers or higher CPA concentrations."
        )
    elif t_observed_h > 2.0 * t_pred:
        verdict = "INHIBITED_NUCLEATION_SUPERIOR"
        recommendation = (
            "Stability exceeds standard stochastic prediction. Biological tissue or carrier solution "
            "contains endogenous ice nucleation inhibitors or macromolecular stabilizers."
        )
    else:
        verdict = "INDETERMINATE"
        recommendation = "Replicate with N >= 8 trials to resolve interfacial vs volumetric regime."

    return {
        "verdict": verdict,
        "t_predicted_hours": t_pred,
        "t_observed_hours": t_observed_h,
        "ratio_obs_to_pred": ratio_to_pred,
        "recommendation": recommendation,
    }
