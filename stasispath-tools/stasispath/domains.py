"""
Domains & Boundaries Module: Epistemic Safeguards and Biological Disclaimers.
Prevents unphysical extrapolations from cells/organs to whole-body stasis.
"""

from enum import Enum
from typing import Dict, Any, Tuple


class WholeBodyStatus(str, Enum):
    UNRESOLVED_CONJECTURE = "WHOLE_BODY_OPEN: No verified functional protocols exist for adult non-hibernators."
    ISOLATED_ORGAN_ACOTADO = "ISOLATED_ORGAN: Bounded physically (Fourier C3 and CPA toxicity limit)."
    MICROSCALE_RESOLVED = "MICROSCALE: Verified electrophysiologically in slices/suspensions."


WHOLE_BODY_DISCLAIMER = (
    "EPISTEMIC BOUNDARY: The StasisPath framework strictly distinguishes between isolated organ "
    "cryopreservation (E3/TRL 3-5) and whole-body stasis (E0/TRL 1). "
    "Do NOT assume whole-body reversibility without whole-organ vascular rewiring and metabolic control."
)


def is_hibernator_exception(species: str, temperature_c: float) -> Tuple[bool, str]:
    """
    Checks if the organism falls under active metabolic regulation (non-Arrhenius).

    Args:
        species: Organism or model name.
        temperature_c: Core body temperature in °C.

    Returns:
        (is_exception, explanation)
    """
    s = species.lower()
    if any(h in s for h in ["hibernat", "ictidomys", "ground_squirrel", "cheirogaleus", "marmot"]):
        if temperature_c <= 12.0:
            return (
                True,
                "HIBERNATOR ACTIVE TORPOR: Metabolic rate is suppressed actively to 1-3% independent of Q10 slope.",
            )
    elif "trachemys" in s or "turtle" in s:
        return (
            True,
            "ECTOTHERM ANOXIA ARREST: Channel arrest and bone carbonate buffering enable extreme stasis.",
        )
    return (False, "Standard mammalian passive thermal kinetics apply.")


def check_domain_limits(
    mass_kg: float,
    temperature_c: float,
    species: str = "human",
) -> Dict[str, Any]:
    """
    Validates physical feasibility of cryopreservation / stasis based on mass and temperature.

    Args:
        mass_kg: Total biological mass in kilograms.
        temperature_c: Target temperature in °C.
        species: Biological species.

    Returns:
        Dict detailing domain validity, warnings, and required technology.
    """
    warnings = []
    is_valid = True

    # Check whole-body scale
    if mass_kg > 15.0:
        warnings.append(WHOLE_BODY_DISCLAIMER)
        whole_body_state = WholeBodyStatus.UNRESOLVED_CONJECTURE
    elif mass_kg > 0.05:
        whole_body_state = WholeBodyStatus.ISOLATED_ORGAN_ACOTADO
    else:
        whole_body_state = WholeBodyStatus.MICROSCALE_RESOLVED

    # Check thermal vs active suppression
    is_hib, hib_note = is_hibernator_exception(species, temperature_c)
    if is_hib:
        warnings.append(hib_note)

    # Check deep hypothermia without CPA
    if temperature_c < 0.0:
        warnings.append(
            "SUBZERO REGIME: Vitrification solution (CPA) or high-pressure supercooling mandatory to prevent freezing."
        )

    # Check thermal conduction limit in bulk tissue
    if mass_kg > 5.0 and temperature_c <= -100.0:
        warnings.append(
            "FOURIER LIMIT C3: Conductive cooling/warming will fail CCR/CWR limits; inductive nanowarming required."
        )

    return {
        "mass_kg": mass_kg,
        "temperature_c": temperature_c,
        "species": species,
        "whole_body_state": whole_body_state,
        "is_hibernator_exception": is_hib,
        "warnings": warnings,
        "pass_domain_check": is_valid,
    }
