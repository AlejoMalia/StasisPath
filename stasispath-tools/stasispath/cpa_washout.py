"""
CPA Washout Module: Stepwise Osmotic Dilution and Endothelial Volume Control.
Calculates multi-step washout schedules to prevent osmotic lysis (ΔV/V₀ <= 1.15).
Based on the Kedem-Katchalsky membrane transport equations and Fahy et al. (2004).
"""

import math
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from stasispath.constants import CCR_VALUES_C_MIN
from stasispath.units import validate_positive


@dataclass
class WashoutStep:
    step_number: int
    temperature_c: float
    cpa_concentration_pct: float  # e.g. 85.0 %
    cpa_molarity_m: float
    osmotic_buffer_mannitol_mm: float  # Non-permeating support (mM)
    duration_minutes: float
    peak_relative_volume: float  # V_peak / V_0
    is_osmotically_safe: bool
    rationale: str


# Diffusion coefficient of small-molecule CPA (DMSO/EG/Formamide) in tissue:
DIFFUSION_COEFF_CPA_CM2_MIN_SUBZERO = 0.00020
DIFFUSION_COEFF_CPA_CM2_MIN_NORMOTHERMIC = 0.00060

# Critical swelling limit beyond which endothelial cell membranes rupture
CRITICAL_VOLUME_SWELLING_LIMIT = 1.15  # +15% expansion


def compute_peak_volume_excursion(
    internal_cpa_m: float,
    external_cpa_m: float,
    external_mannitol_mm: float,
    sigma_cpa: float = 0.80,
    sigma_buffer: float = 1.0,
    osmotic_inactive_fraction: float = 0.20,
    reference_osmolarity_m: float = 7.78,  # (0.30 + 0.80 * 9.35 M)
) -> float:
    """
    Computes transient peak relative cell volume (V_peak / V_0) during osmotic washout
    using the Kedem-Katchalsky osmotic flux boundary where water permeability (Lp)
    is orders of magnitude faster than solute permeation (Ps).

    Args:
        internal_cpa_m: Intracellular CPA concentration at start of step (Molar).
        external_cpa_m: Extracellular CPA concentration in the wash bath (Molar).
        external_mannitol_mm: Non-permeating osmotic buffer in bath (mM).
        sigma_cpa: Reflection coefficient of permeating CPA (typically 0.75 - 0.85).
        sigma_buffer: Reflection coefficient of impermeable buffer (1.0 for mannitol).
        osmotic_inactive_fraction: Osmotically inactive volume fraction (W_b ≈ 0.20).
        reference_osmolarity_m: Full-load reference osmolar capacity (0.30 + 0.80 * 9.35 M).

    Returns:
        Peak relative cell volume ratio (V_peak / V_0). Values <= 1.15 indicate safe washout.
    """
    mannitol_m = external_mannitol_mm / 1000.0

    # Net driving osmotic gradient pulling water INTO the cell:
    delta_osm = sigma_cpa * (internal_cpa_m - external_cpa_m) - sigma_buffer * mannitol_m

    if delta_osm <= 0.0:
        return 1.0

    # If pure water washout (external_cpa=0, mannitol=0, internal_cpa high), trigger massive lysis
    if external_cpa_m == 0.0 and external_mannitol_mm == 0.0 and internal_cpa_m > 3.0:
        return 1.85  # Osmotic membrane rupture

    relative_expansion = (1.0 - osmotic_inactive_fraction) * (delta_osm / reference_osmolarity_m)
    return 1.0 + relative_expansion


def design_washout_protocol(
    initial_cpa: str = "M22",
    sample_thickness_or_lc_cm: float = 0.04,  # Default: 400 µm brain slice (0.04 cm)
    max_allowed_swelling: float = CRITICAL_VOLUME_SWELLING_LIMIT,
    is_organ_vascularized: bool = False,
) -> Dict[str, Any]:
    """
    Synthesizes a stepwise non-linear osmotic washout protocol with mannitol support.

    Args:
        initial_cpa: 'M22' (~9.35 M) or 'V3' (~8.4 M).
        sample_thickness_or_lc_cm: Half-thickness or diffusion distance in cm.
        max_allowed_swelling: Maximum permissible transient swelling (default 1.15).
        is_organ_vascularized: If True, uses organ vascular perfusion kinetics rather than immersion diffusion.

    Returns:
        Dict containing step-by-step washout schedule, safety verification, and total duration.
    """
    initial_molarity = 9.35 if initial_cpa.upper() == "M22" else 8.42

    # Stepwise target percentages: non-linear 7-step schedule designed to clamp ΔV/V0 <= 1.15
    schedule_specs = [
        (85.0, -3.0, 300.0, "Subzero initial step (85%): high mannitol buffer clamps early water surge."),
        (70.0, -3.0, 300.0, "Secondary subzero step (70%): controlled egress of DMSO/EG."),
        (55.0, 0.0, 300.0, "Transition to 0 °C (55%): mannitol buffer preserves endothelial tight junctions."),
        (40.0, 5.0, 300.0, "Early hypothermic step (40%): core CPA egress."),
        (25.0, 10.0, 250.0, "Late hypothermic step (25%): gradual mannitol taper."),
        (10.0, 20.0, 200.0, "Subnormothermic rinse (10%): low-concentration CPA clearance."),
        (0.0, 32.0, 0.0, "Normothermic recovery (0%): isotonic physiological buffer (ACSF/saline)."),
    ]


    steps = []
    current_internal_m = initial_molarity
    total_time_min = 0.0
    all_safe = True

    # Diffusion characteristic time: tau_diff ≈ LC² / (2 * D_diff)
    d_diff = DIFFUSION_COEFF_CPA_CM2_MIN_SUBZERO if not is_organ_vascularized else 0.0010
    base_step_duration = max(7.0, (sample_thickness_or_lc_cm ** 2) / (2.0 * d_diff))

    for idx, (pct, temp_c, man_mm, rat) in enumerate(schedule_specs, 1):
        target_m = initial_molarity * (pct / 100.0)

        # Calculate peak osmotic volume excursion
        v_peak = compute_peak_volume_excursion(
            internal_cpa_m=current_internal_m,
            external_cpa_m=target_m,
            external_mannitol_mm=man_mm,
        )

        is_safe = v_peak <= max_allowed_swelling
        if not is_safe:
            all_safe = False

        duration = round(base_step_duration, 1)
        total_time_min += duration

        steps.append(
            WashoutStep(
                step_number=idx,
                temperature_c=temp_c,
                cpa_concentration_pct=pct,
                cpa_molarity_m=round(target_m, 2),
                osmotic_buffer_mannitol_mm=man_mm,
                duration_minutes=duration,
                peak_relative_volume=round(v_peak, 3),
                is_osmotically_safe=is_safe,
                rationale=rat,
            )
        )

        # Update internal concentration for next step assuming 80% equilibration during the step
        current_internal_m = target_m + 0.20 * (current_internal_m - target_m)

    return {
        "cpa": initial_cpa.upper(),
        "sample_lc_cm": sample_thickness_or_lc_cm,
        "is_organ_vascularized": is_organ_vascularized,
        "total_duration_minutes": round(total_time_min, 1),
        "all_steps_osmotically_safe": all_safe,
        "max_swelling_limit": max_allowed_swelling,
        "steps": steps,
        "summary": "Protocol maintains transient volume excursion below critical swelling limit (ΔV/V₀ <= 1.15)."
        if all_safe
        else "WARNING: Osmotic excursion exceeds safe membrane tolerance; increase mannitol buffer concentration.",
    }
