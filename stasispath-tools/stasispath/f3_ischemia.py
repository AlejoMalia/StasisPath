"""
F3 Ischemia Module: Piecewise Q10 Kinetics and Equivalent Ischemic Time.
Implements Formula F3 from the StasisPath Framework.
"""

from typing import List, Tuple, Optional
from stasispath.constants import (
    T_NORMOTHERMIA_C,
    T_Q10_TRANSITION_C,
    Q10_WARM,
    Q10_COLD,
)
from stasispath.units import validate_non_negative


def q10_for_T(T_c: float) -> float:
    """
    Returns the local empirical Q10 exponent for metabolic depression in non-hibernating mammals.

    Args:
        T_c: Temperature in degrees Celsius.

    Returns:
        Q10 factor (2.15 for T > 15 °C; 3.50 for T <= 15 °C).
    """
    if T_c > T_Q10_TRANSITION_C:
        return Q10_WARM
    return Q10_COLD


def metabolic_suppression_factor(T_c: float, piecewise: bool = True) -> float:
    """
    Calculates the ratio of normothermic metabolic rate (at 37 °C) to hypothermic rate at T_c.
    Rate(37°C) / Rate(T_c) >= 1.0 for T_c <= 37 °C.

    Args:
        T_c: Target tissue temperature in °C.
        piecewise: If True, uses the empirical bilinear Q10 (warm + cold regime).

    Returns:
        Slowing factor S >= 1.0. (An hour at T_c is equivalent to 1/S hours at 37 °C).
    """
    if T_c >= T_NORMOTHERMIA_C:
        # Hyperthermia or normothermia
        return Q10_WARM ** ((T_NORMOTHERMIA_C - T_c) / 10.0)

    if not piecewise:
        # Single-slope simplification
        return Q10_WARM ** ((T_NORMOTHERMIA_C - T_c) / 10.0)

    if T_c >= T_Q10_TRANSITION_C:
        # Warm hypothermia range: 37 °C -> 15 °C
        delta_warm = T_NORMOTHERMIA_C - T_c
        return Q10_WARM ** (delta_warm / 10.0)
    else:
        # Crosses transition: 37 °C -> 15 °C with Q10_WARM, and 15 °C -> T_c with Q10_COLD
        delta_warm = T_NORMOTHERMIA_C - T_Q10_TRANSITION_C  # 22.0 °C
        delta_cold = T_Q10_TRANSITION_C - T_c
        factor_warm = Q10_WARM ** (delta_warm / 10.0)
        factor_cold = Q10_COLD ** (delta_cold / 10.0)
        return factor_warm * factor_cold


def tau_eq(t_hours: float, T_c: float, piecewise: bool = True) -> float:
    """
    Calculates the equivalent normothermic ischemic time (tau_eq) in hours.
    An organ held at T_c for t_hours accumulates the metabolic ischemic damage
    equivalent to tau_eq hours at 37 °C under total circulatory arrest.

    Formula:
        tau_eq = t_hours / metabolic_suppression_factor(T_c)

    Args:
        t_hours: Duration of hypothermic exposure in hours.
        T_c: Temperature in degrees Celsius.
        piecewise: Whether to apply piecewise Q10 transition at 15 °C.

    Returns:
        Equivalent ischemic duration at 37 °C (hours).
    """
    validate_non_negative(t_hours, "t_hours")
    factor = metabolic_suppression_factor(T_c, piecewise=piecewise)
    return t_hours / factor


def equivalent_ischemic_dose(time_temp_profile: List[Tuple[float, float]]) -> float:
    """
    Integrates equivalent ischemic dose for a dynamic cooling or warming profile:
        tau_eq = sum( delta_t_i / factor(T_i) )

    Args:
        time_temp_profile: List of (delta_t_hours, T_c_midpoint) steps.

    Returns:
        Accumulated equivalent ischemic hours at 37 °C.
    """
    total_tau = 0.0
    for delta_t, t_c in time_temp_profile:
        validate_non_negative(delta_t, "delta_t")
        total_tau += tau_eq(delta_t, t_c, piecewise=True)
    return total_tau


def assert_domain(T_c: float, species: str = "mammal_non_hibernating") -> Tuple[bool, Optional[str]]:
    """
    Verifies physiological and thermodynamic domain validity for the Q10 ischemia model.

    Returns:
        (is_valid, warning_or_error_message)
    """
    species_lower = species.lower()

    if "hibernat" in species_lower or "ictidomys" in species_lower:
        if T_c < 12.0:
            return (
                False,
                "DOMAIN BREACH (F3): Hibernators exhibit active metabolic suppression (phosphorylation of complexes I/II) "
                "below 12 °C. The passive Arrhenius Q10 model severely underestimates suppression by a factor of >10.",
            )

    if species_lower == "mammal_non_hibernating":
        if T_c < 0.0:
            return (
                True,
                "NOTE: Subzero temperature in non-hibernating tissue requires chemical CPA or supercooling "
                "to prevent catastrophic ice nucleated injury.",
            )
        if T_c < 20.0 and T_c >= 0.0:
            return (
                True,
                "DOMAIN OK: Deep hypothermia regime. Requires artificial perfusion/ECMO to avoid spontaneous ventricular fibrillation.",
            )

    return (True, None)
