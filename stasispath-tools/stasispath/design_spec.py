"""
Design specification: the CCR a given piece of tissue actually REQUIRES.

This is the StasisPath contribution that inverts the usual question. The field asks
"how good is M22?" (CCR 0.10 C/min). The useful question is the other way round:

    Given an organ of mass m, what is the slowest cooling rate that still vitrifies it?

The answer for a human brain is 0.426 C/min -- 4.3x more permissive than M22. Any
candidate chemistry that clears that bar is admissible, whether or not it matches M22.

Anchor: F2 (3 L vessel, LC 2.20 cm, 0.47 C/min centre), exponent n = 2 (conduction).
The exponent is PREREGISTERED BUT NOT YET MEASURED (P21). See assumptions.py.
"""
from __future__ import annotations
import math
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

ANCHOR_LC_CM: float = 2.20
ANCHOR_RATE_C_MIN: float = 0.47
EXPONENT_N: float = 2.0
A_CCR: float = 15.2          # log10(CCR) = A + B * molarity
B_CCR: float = -1.74
M_TOXIC_MOL_L: float = 9.28  # molarity at which basal respiration halves
LC_BIOT_CRIT_CM: float = 0.40


class Geometry(str, Enum):
    SPHERE = "sphere"        # LC = V/A = r/3
    CYLINDER = "cylinder"    # LC = V/A = r/2  (torso, limbs)
    SLAB = "slab"            # LC = half-thickness


_GEOM_FACTOR: Dict[Geometry, float] = {
    Geometry.SPHERE: 1.0,
    Geometry.CYLINDER: 1.5,
    Geometry.SLAB: 3.0,
}


class Admissibility(str, Enum):
    ADMISSIBLE = "ADMISSIBLE"
    REJECTED = "REJECTED"
    UNMEASURED = "UNMEASURED"


@dataclass
class DesignSpec:
    organ: str
    mass_g: float
    geometry: Geometry
    lc_cm: float
    achievable_rate_c_min: float
    required_ccr_c_min: float
    required_molarity_mol_l: float
    toxicity_margin_mol_l: float
    viable: bool
    permissiveness_vs_m22: float
    geometry_flip_factor: Optional[float]


def characteristic_length(mass_g: float, geometry: Geometry = Geometry.SPHERE,
                          density_g_cm3: float = 1.0) -> float:
    """LC = V/A in cm. Density is EXPLICIT here; the original framework assumed 1.0 silently."""
    volume_cm3 = mass_g / density_g_cm3
    r = (3.0 * volume_cm3 / (4.0 * math.pi)) ** (1.0 / 3.0)
    return (r / 3.0) * _GEOM_FACTOR[geometry]


def achievable_cooling_rate(lc_cm: float, n: float = EXPONENT_N) -> float:
    """Centre cooling rate by conduction, anchored on F2. Valid only above the Biot length."""
    if lc_cm <= 0:
        raise ValueError("lc_cm must be positive")
    return ANCHOR_RATE_C_MIN * (ANCHOR_LC_CM / lc_cm) ** n


def molarity_for_ccr(ccr_c_min: float) -> float:
    """Inverse of the local log10(CCR)-molarity line. Interpolation only, 8.4-9.3 M."""
    if ccr_c_min <= 0:
        raise ValueError("ccr_c_min must be positive")
    return (math.log10(ccr_c_min) - A_CCR) / B_CCR


def required_ccr(mass_g: float, geometry: Geometry = Geometry.SPHERE,
                 density_g_cm3: float = 1.0, n: float = EXPONENT_N) -> float:
    """THE HEADLINE NUMBER: slowest CCR that still vitrifies this piece."""
    return achievable_cooling_rate(characteristic_length(mass_g, geometry, density_g_cm3), n)


def geometry_flip_factor(mass_g: float, geometry: Geometry = Geometry.SPHERE,
                         density_g_cm3: float = 1.0, n: float = EXPONENT_N) -> Optional[float]:
    """
    How wrong would LC have to be, multiplicatively, to flip this organ from viable to not?
    Returns None if the organ is already non-viable. A cylinder error is 1.5x, so a flip
    factor above 1.5 means the verdict survives a geometry mistake.
    """
    lc0 = characteristic_length(mass_g, geometry, density_g_cm3)
    if molarity_for_ccr(achievable_cooling_rate(lc0, n)) >= M_TOXIC_MOL_L:
        return None
    lo, hi = 1.0, 8.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if molarity_for_ccr(achievable_cooling_rate(lc0 * mid, n)) < M_TOXIC_MOL_L:
            lo = mid
        else:
            hi = mid
    return lo


def design_spec(organ: str, mass_g: float, geometry: Geometry = Geometry.SPHERE,
                density_g_cm3: float = 1.0, n: float = EXPONENT_N) -> DesignSpec:
    lc = characteristic_length(mass_g, geometry, density_g_cm3)
    rate = achievable_cooling_rate(lc, n)
    m_req = molarity_for_ccr(rate)
    return DesignSpec(
        organ=organ, mass_g=mass_g, geometry=geometry, lc_cm=lc,
        achievable_rate_c_min=rate, required_ccr_c_min=rate,
        required_molarity_mol_l=m_req,
        toxicity_margin_mol_l=M_TOXIC_MOL_L - m_req,
        viable=m_req < M_TOXIC_MOL_L,
        permissiveness_vs_m22=rate / 0.10,
        geometry_flip_factor=geometry_flip_factor(mass_g, geometry, density_g_cm3, n),
    )


def screen_candidate_cpa(name: str, measured_ccr_c_min: Optional[float], organ: str = "brain",
                         mass_g: float = 1400.0,
                         geometry: Geometry = Geometry.SPHERE) -> Dict[str, object]:
    """
    Screen any candidate chemistry against the organ's requirement.

    measured_ccr_c_min=None means NOT MEASURED. The framework refuses to guess:
    an unmeasured CPA returns UNMEASURED, never a pass or a fail. This is deliberate --
    a hardcoded value for an unmeasured chemistry is how a framework fabricates progress.
    """
    spec = design_spec(organ, mass_g, geometry)
    if measured_ccr_c_min is None:
        return {"cpa": name, "organ": organ, "required_ccr_c_min": spec.required_ccr_c_min,
                "measured_ccr_c_min": None, "verdict": Admissibility.UNMEASURED,
                "rationale": f"No measured CCR for {name}. Run a DSC. The bar is "
                             f"{spec.required_ccr_c_min:.3f} C/min for {organ}."}
    ok = measured_ccr_c_min <= spec.required_ccr_c_min
    return {"cpa": name, "organ": organ, "required_ccr_c_min": spec.required_ccr_c_min,
            "measured_ccr_c_min": measured_ccr_c_min,
            "verdict": Admissibility.ADMISSIBLE if ok else Admissibility.REJECTED,
            "margin_factor": spec.required_ccr_c_min / measured_ccr_c_min,
            "rationale": f"{name} needs CCR <= {spec.required_ccr_c_min:.3f} C/min for {organ}; "
                         f"measured {measured_ccr_c_min:.3f} C/min "
                         f"({'clears' if ok else 'misses'} by "
                         f"x{max(spec.required_ccr_c_min, measured_ccr_c_min)/min(spec.required_ccr_c_min, measured_ccr_c_min):.1f}). "
                         f"NOTE: clearing the CCR bar says nothing about preserved FUNCTION (frontier X2)."}
