"""
F5 Cooling Module: Phase-Dependent Cooling Protocols and Transition Rate Limits.
Implements Formula F5 from the StasisPath Framework.
"""

from enum import Enum
from typing import List, Tuple, Dict, Any
from stasispath.constants import (
    T_GLASS_M22_C,
    T_FREEZING_M22_C,
    MAX_COOLING_RATE_NEAR_TG,
    CCR_VALUES_C_MIN,
    CWR_VALUES_C_MIN,
)


class CoolingPhase(str, Enum):
    NORMOTHERMIC_PREPARATION = "Phase 0: Normothermic perfusion (37 °C to 20 °C)"
    HYPOTHERMIC_TRANSITION = "Phase 1: Deep hypothermia & initial CPA perfusion (20 °C to 0 °C)"
    SUBZERO_LOADING = "Phase 2: Subzero full CPA loading (0 °C to -22 °C)"
    RAPID_VITRIFICATION = "Phase 3: Fast traverse of crystallization zone (-22 °C to -123 °C)"
    CRYOGENIC_ANNEALING = "Phase 4: Ultralow annealing below Tg (-123 °C to -196 °C)"


def phase_for_T(T_c: float) -> CoolingPhase:
    """
    Identifies the active cooling phase for a given tissue temperature.

    Args:
        T_c: Temperature in °C.

    Returns:
        CoolingPhase enum value.
    """
    if T_c > 20.0:
        return CoolingPhase.NORMOTHERMIC_PREPARATION
    elif T_c > 0.0:
        return CoolingPhase.HYPOTHERMIC_TRANSITION
    elif T_c > -22.0:
        return CoolingPhase.SUBZERO_LOADING
    elif T_c > T_GLASS_M22_C:
        return CoolingPhase.RAPID_VITRIFICATION
    else:
        return CoolingPhase.CRYOGENIC_ANNEALING


def recommended_cooling_rate(T_c: float, cpa: str = "M22") -> Dict[str, Any]:
    """
    Returns the recommended rate constraint (°C/min) depending on the active phase.

    Args:
        T_c: Current tissue temperature in °C.
        cpa: Name of the CPA formulation (e.g. 'M22', 'V3', 'VS55').

    Returns:
        Dict specifying min_rate, max_rate, and physical rationale.
    """
    cpa_key = cpa.upper()
    ccr = CCR_VALUES_C_MIN.get(cpa_key, 0.10)

    phase = phase_for_T(T_c)

    if phase == CoolingPhase.NORMOTHERMIC_PREPARATION:
        return {
            "phase": phase,
            "min_rate_c_min": 0.5,
            "max_rate_c_min": 5.0,
            "rationale": "Controlled cooling to avoid cold shock while maintaining membrane stability.",
        }
    elif phase == CoolingPhase.HYPOTHERMIC_TRANSITION:
        return {
            "phase": phase,
            "min_rate_c_min": 0.2,
            "max_rate_c_min": 2.0,
            "rationale": "Gradual equilibration of intermediate CPA carriers (e.g. VMP) before subzero drop.",
        }
    elif phase == CoolingPhase.SUBZERO_LOADING:
        return {
            "phase": phase,
            "min_rate_c_min": 0.1,
            "max_rate_c_min": 1.0,
            "rationale": "Osmotic equilibrium at subzero temperatures (-3 °C to -22 °C) to minimize chemical toxicity.",
        }
    elif phase == CoolingPhase.RAPID_VITRIFICATION:
        return {
            "phase": phase,
            "min_rate_c_min": ccr,
            "max_rate_c_min": 100.0,
            "rationale": f"Rate MUST exceed CCR ({ccr:.2f} °C/min) to prevent ice crystal nucleation.",
        }
    else:  # CRYOGENIC_ANNEALING
        return {
            "phase": phase,
            "min_rate_c_min": 0.01,
            "max_rate_c_min": MAX_COOLING_RATE_NEAR_TG,
            "rationale": f"Rate MUST stay below {MAX_COOLING_RATE_NEAR_TG:.3f} °C/min (EN 14620-5) to prevent catastrophic thermomechanical cracking.",
        }


def validate_cooling_profile(
    times_min: List[float],
    temps_c: List[float],
    cpa: str = "M22",
) -> Dict[str, Any]:
    """
    Validates a complete experimental cooling trajectory against physical bounds:
    1. Did it cool fast enough between -22 °C and Tg to exceed CCR?
    2. Did it cool slow enough below Tg to avoid thermal fracture?

    Args:
        times_min: Time coordinates in minutes (monotonic).
        temps_c: Temperature coordinates in °C.
        cpa: CPA formulation name.

    Returns:
        Dict with validation verdict, detected violations, and phase analysis.
    """
    if len(times_min) != len(temps_c) or len(times_min) < 2:
        raise ValueError("times_min and temps_c must be arrays of equal length >= 2.")

    cpa_key = cpa.upper()
    ccr = CCR_VALUES_C_MIN.get(cpa_key, 0.10)

    violations = []
    zone_ccr_passed = False
    fracture_risk_detected = False

    for i in range(len(times_min) - 1):
        dt = times_min[i + 1] - times_min[i]
        if dt <= 0:
            raise ValueError(f"times_min must be strictly monotonic at index {i}.")

        t1, t2 = temps_c[i], temps_c[i + 1]
        rate = abs(t2 - t1) / dt  # cooling rate in °C/min
        t_mid = (t1 + t2) / 2.0

        # Check crystallization traverse: -22 °C to -123 °C
        if t_mid <= -22.0 and t_mid >= T_GLASS_M22_C:
            if rate < ccr:
                violations.append(
                    f"CRYSTALLIZATION DANGER: Rate {rate:.3f} °C/min at {t_mid:.1f} °C is below CCR ({ccr:.3f} °C/min)."
                )
            else:
                zone_ccr_passed = True

        # Check fracture zone below Tg (-123 °C)
        if t_mid < T_GLASS_M22_C:
            if rate > MAX_COOLING_RATE_NEAR_TG:
                fracture_risk_detected = True
                violations.append(
                    f"THERMAL FRACTURE RISK: Rate {rate:.3f} °C/min below Tg ({t_mid:.1f} °C) exceeds safe limit ({MAX_COOLING_RATE_NEAR_TG} °C/min)."
                )

    passed = len(violations) == 0

    return {
        "valid": passed,
        "cpa": cpa_key,
        "ccr_required_c_min": ccr,
        "violations": violations,
        "summary": "Profile satisfies all thermodynamic vitrification and fracture constraints."
        if passed
        else f"Profile failed with {len(violations)} physical constraint violation(s).",
    }
