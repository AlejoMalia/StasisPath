"""
Thermal Stress & Fracture Module: Thermomechanical Stress in Vitrified Matrices.
Implements Formulas F1 and F2 from the StasisPath Framework.
"""

from typing import Dict, Any
from stasispath.constants import (
    SIGMA_FRACTURE_MPA,
    YOUNG_MODULUS_VITREOUS_GPA,
    POISSON_RATIO_VITREOUS,
    THERMAL_EXPANSION_COEFF_PER_K,
)
from stasispath.units import validate_positive

# Thermal diffusivity of vitrified biological tissue: ~1.3e-7 m²/s = 0.078 cm²/min
DEFAULT_THERMAL_DIFFUSIVITY_CM2_MIN = 0.078


def radial_temperature_gradient(
    cooling_rate_c_min: float,
    lc_cm: float,
    thermal_diffusivity_cm2_min: float = DEFAULT_THERMAL_DIFFUSIVITY_CM2_MIN,
) -> float:
    """
    Computes the radial temperature difference (ΔT) between surface and core
    under steady cooling of a cylindrical/spherical organ mass:
        ΔT_radial = (dT/dt) * (LC^2) / (2 * α_diff)

    Args:
        cooling_rate_c_min: Cooling rate in °C/min (positive).
        lc_cm: Characteristic half-thickness or radius in cm.
        thermal_diffusivity_cm2_min: Thermal diffusivity in cm²/min.

    Returns:
        Radial temperature difference in °C (or K).
    """
    validate_positive(cooling_rate_c_min, "cooling_rate_c_min")
    validate_positive(lc_cm, "lc_cm")
    validate_positive(thermal_diffusivity_cm2_min, "thermal_diffusivity_cm2_min")

    return (cooling_rate_c_min * (lc_cm ** 2)) / (2.0 * thermal_diffusivity_cm2_min)


def sigma_thermal(
    cooling_rate_c_min: float,
    lc_cm: float,
    e_modulus_mpa: float = YOUNG_MODULUS_VITREOUS_GPA * 1000.0,
    nu_poisson: float = POISSON_RATIO_VITREOUS,
    alpha_thermal_per_k: float = THERMAL_EXPANSION_COEFF_PER_K,
    thermal_diffusivity_cm2_min: float = DEFAULT_THERMAL_DIFFUSIVITY_CM2_MIN,
) -> float:
    """
    Computes the peak thermomechanical tensile stress σ_th (in MPa)
    induced in a vitrified tissue mass crossing the glass transition:
        σ_th = (E * α * ΔT_radial) / (1 - ν)

    Args:
        cooling_rate_c_min: Cooling rate in °C/min.
        lc_cm: Characteristic dimension / radius in cm.
        e_modulus_mpa: Young's modulus in MPa (default: 1200 MPa).
        nu_poisson: Poisson's ratio (default: 0.35).
        alpha_thermal_per_k: Linear thermal expansion coefficient in K^-1.
        thermal_diffusivity_cm2_min: Thermal diffusivity in cm²/min.

    Returns:
        Peak tensile stress in MPa.
    """
    delta_t = radial_temperature_gradient(
        cooling_rate_c_min=cooling_rate_c_min,
        lc_cm=lc_cm,
        thermal_diffusivity_cm2_min=thermal_diffusivity_cm2_min,
    )

    stress_mpa = (e_modulus_mpa * alpha_thermal_per_k * delta_t) / (1.0 - nu_poisson)
    return stress_mpa


def fracture_risk(
    cooling_rate_c_min: float,
    lc_cm: float,
    sigma_crit_mpa: float = SIGMA_FRACTURE_MPA,
) -> Dict[str, Any]:
    """
    Assesses the risk of structural fracture during vitrification cooldown or warming.

    Args:
        cooling_rate_c_min: Rate in °C/min near Tg.
        lc_cm: Characteristic organ radius in cm.
        sigma_crit_mpa: Critical fracture stress threshold (default 2.0 MPa).

    Returns:
        Dict with stress, safety factor, and risk level.
    """
    stress = sigma_thermal(cooling_rate_c_min, lc_cm)
    safety_factor = sigma_crit_mpa / stress if stress > 0 else float("inf")

    if stress < 0.5 * sigma_crit_mpa:
        risk_level = "LOW"
    elif stress <= sigma_crit_mpa:
        risk_level = "MODERATE_ELEVATED"
    elif stress <= 2.0 * sigma_crit_mpa:
        risk_level = "HIGH_FRACTURE_LIKELY"
    else:
        risk_level = "CATASTROPHIC_FRACTURE_CERTAIN"

    return {
        "sigma_thermal_mpa": stress,
        "sigma_critical_mpa": sigma_crit_mpa,
        "safety_factor": safety_factor,
        "risk_level": risk_level,
        "will_fracture": stress >= sigma_crit_mpa,
    }


def critical_biot_length(
    h_heat_transfer: float = 250.0,
    k_conductivity: float = 0.5,
) -> float:
    """
    Computes the critical dimension LC* where Biot number Bi = (h * LC) / k = 1.0.
    For LC > LC*, internal thermal resistance dominates surface convective cooling.

    Args:
        h_heat_transfer: Convective heat transfer coefficient (W / m²·K).
        k_conductivity: Tissue thermal conductivity (W / m·K, ~0.5 for tissue).

    Returns:
        Critical LC in cm.
    """
    # Bi = 1 => LC = k / h (in meters)
    lc_m = k_conductivity / h_heat_transfer
    return lc_m * 100.0  # in cm
