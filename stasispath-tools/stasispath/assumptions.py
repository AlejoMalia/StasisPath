"""
Regime guards: the premises that silently break a cryobiology calculation.

Every finding below came from auditing StasisPath against itself, and two of them were
real errors in our own published numbers:

  * Applying the LC^-2 conduction law across the Biot boundary overestimated the
    mouse-to-human penalty by x2.6 (x231 reported, x88 correct).
  * A nucleation rate measured ISOCHORICALLY was compared against an isobaric bound.
    Isochoric confinement suppresses nucleation; the two are not interchangeable.

Guards return (ok, message). They are cheap, they run on every state, and they are
designed to make a result LESS impressive, not more.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

T_GLASS_C: float = -123.0
LC_BIOT_CRIT_CM: float = 0.40
Q10_MEASURED_MIN_C: float = -10.0
Q10_MEASURED_MAX_C: float = 37.0


class Severity(str, Enum):
    WARNING = "WARNING"
    SWITCH_MODEL = "SWITCH_MODEL"
    FAIL_STOP = "FAIL_STOP"


@dataclass
class Violation:
    guard_id: str
    name: str
    severity: Severity
    message: str


def guard_biot_regime(lc_cm: float, exponent_used: float) -> Optional[Violation]:
    """LC^-2 is conduction (Bi>1). LC^-1 is convection (Bi<1). Mixing them is the x2.6 error."""
    conduction_law = exponent_used > 1.5
    conduction_regime = lc_cm > LC_BIOT_CRIT_CM
    if conduction_law != conduction_regime:
        return Violation("BIOT", "Biot regime vs scaling exponent", Severity.SWITCH_MODEL,
            f"LC={lc_cm:.3f} cm is in the "
            f"{'conduction' if conduction_regime else 'convection'} regime "
            f"(Bi=1 at {LC_BIOT_CRIT_CM} cm) but exponent n={exponent_used} is the "
            f"{'conduction' if conduction_law else 'convection'} law. "
            f"Crossing this boundary with one exponent inflated our own scaling by x2.6.")
    return None


def guard_q10_domain(temperature_c: float) -> Optional[Violation]:
    """Q10 below Tg is not an extrapolation, it is a category error: no liquid, no metabolism."""
    if temperature_c < T_GLASS_C:
        return Violation("Q10_TG", "Q10 applied below the glass transition", Severity.FAIL_STOP,
            f"T={temperature_c:.1f} C is below Tg={T_GLASS_C} C. There is no liquid water and "
            f"no metabolism, so Q10 is undefined -- not merely extrapolated. Any ischemic dose "
            f"computed here is a number without physics behind it.")
    if temperature_c < Q10_MEASURED_MIN_C:
        return Violation("Q10_RANGE", "Q10 outside the measured range", Severity.WARNING,
            f"T={temperature_c:.1f} C: no Q10 in the framework was measured below "
            f"{Q10_MEASURED_MIN_C} C. This is projection, not measurement.")
    return None


def guard_nucleation_regime(measured_regime: str, bound_regime: str = "isobaric") -> Optional[Violation]:
    if measured_regime.lower() != bound_regime.lower():
        return Violation("NUCLEATION_P", "Pressure regime mismatch in nucleation", Severity.SWITCH_MODEL,
            f"Nucleation rate measured under '{measured_regime}' compared against a "
            f"'{bound_regime}' bound. Isochoric confinement suppresses nucleation; these are "
            f"different physics and must not be intersected.")
    return None


def guard_geometry(geometry: str, flip_factor: Optional[float]) -> Optional[Violation]:
    """A sphere formula on an elongated piece underestimates LC by 1.5x (cylinder) or 3x (slab)."""
    needed = {"cylinder": 1.5, "slab": 3.0}.get(geometry.lower())
    if needed is None:
        return None
    if flip_factor is None:
        return None
    if flip_factor < needed:
        return Violation("GEOMETRY", "Geometry error can flip the verdict", Severity.SWITCH_MODEL,
            f"Verdict flips at an LC error of x{flip_factor:.2f}, but a '{geometry}' treated as a "
            f"sphere is already off by x{needed}. The verdict does NOT survive the correction.")
    return Violation("GEOMETRY", "Geometry assumption noted (verdict survives)", Severity.WARNING,
        f"Sphere formula used on a '{geometry}' (x{needed} error), but the verdict only flips at "
        f"x{flip_factor:.2f}. Verdict survives with {flip_factor/needed:.2f}x to spare.")


def guard_unmeasured_exponent(exponent_used: float, p21_executed: bool = False) -> Optional[Violation]:
    if exponent_used == 2.0 and not p21_executed:
        return Violation("EXPONENT", "Scaling exponent preregistered but unmeasured", Severity.WARNING,
            "n=2 carries the entire multi-organ projection and has never been measured. "
            "P21 (a control vessel, three small and three large bags, one thermocouple) "
            "measures it for the cost of an afternoon.")
    return None


def guard_density_declared(density_g_cm3: Optional[float]) -> Optional[Violation]:
    if density_g_cm3 is None:
        return Violation("DENSITY", "Density assumed silently", Severity.WARNING,
            "Converting grams to centimetres requires a density. Assuming 1.0 g/cm3 without "
            "declaring it is a hidden premise (tissue is ~1.05, a -1.6 % bias in LC).")
    return None


def audit(state: Dict[str, Any]) -> List[Violation]:
    """Run every applicable guard over a state dict. Missing keys simply skip their guard."""
    out: List[Violation] = []
    if "lc_cm" in state and "exponent" in state:
        out.append(guard_biot_regime(state["lc_cm"], state["exponent"]))
    if "temperature_c" in state:
        out.append(guard_q10_domain(state["temperature_c"]))
    if "nucleation_regime" in state:
        out.append(guard_nucleation_regime(state["nucleation_regime"],
                                           state.get("bound_regime", "isobaric")))
    if "geometry" in state:
        out.append(guard_geometry(state["geometry"], state.get("flip_factor")))
    if "exponent" in state:
        out.append(guard_unmeasured_exponent(state["exponent"], state.get("p21_executed", False)))
    if "density_g_cm3" in state:
        out.append(guard_density_declared(state["density_g_cm3"]))
    return [v for v in out if v is not None]
