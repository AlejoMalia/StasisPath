"""
stasispath: Computational Biophysics Toolkit for Cryopreservation and Biostasis
Based on the StasisPath Biophysical Framework (2026).

Primary Purpose:
    Provides verified physical and thermodynamic calculations (Q10 piecewise ischemia,
    Arrhenius chemical toxicity, stochastic nucleation limits, and phase transition
    thermal stress) to guide lab protocol design without redundant simulations.

Disclaimer:
    This library provides quantitative boundaries and falsifiable predictions.
    It DOES NOT substitute direct experimental measurement. Whole-body stasis in
    adult non-hibernating mammals remains an open biological frontier.
"""

from stasispath.constants import (
    T_NORMOTHERMIA_C,
    T_GLASS_M22_C,
    T_FREEZING_M22_C,
    VT_STOCHASTIC_ANCHOR_L_H,
    SIGMA_FRACTURE_MPA,
    MAX_COOLING_RATE_NEAR_TG,
)
from stasispath.f3_ischemia import (
    q10_for_T,
    tau_eq,
    equivalent_ischemic_dose,
    assert_domain as assert_ischemia_domain,
)
from stasispath.f4_nucleation import (
    vt_product,
    t_max_nucleation,
    p_no_nucleation,
    heterogeneous_nucleation_rate,
)
from stasispath.f5_cooling import (
    CoolingPhase,
    phase_for_T,
    recommended_cooling_rate,
    validate_cooling_profile,
)
from stasispath.thermal_stress import (
    sigma_thermal,
    fracture_risk,
    critical_biot_length,
)
from stasispath.cpa_toxicity import (
    arrhenius_factor,
    d_cpa_predicted,
    predicted_ocr_retention,
)
from stasispath.predictions import (
    eval_p19,
    check_p19_derivation,
    eval_h2,
    eval_h3,
    eval_h4,
    eval_h5,
    Verdict,
    PredictionVerdict,
)
from stasispath.domains import (
    check_domain_limits,
    is_hibernator_exception,
    WholeBodyStatus,
)
from stasispath.reporting import (
    generate_protocol_report,
    export_predictions_csv,
)
from stasispath.organ_projector import (
    compute_bsa_dubois,
    estimate_organ_morphometry,
    project_multiorgan_constraints,
    format_multiorgan_markdown_report,
    OrganSpecification,
)
from stasispath.thermal_recipes import (
    generate_vitrification_recipe,
    export_recipe_csv,
    export_planer_kryo_format,
    RecipeStep,
)
from stasispath.cpa_washout import (
    compute_peak_volume_excursion,
    design_washout_protocol,
    WashoutStep,
)
from stasispath.boa_connector import (
    normalize_organ_volume_dict,
    load_boa_segmentation_file,
    project_from_boa_file,
)

__version__ = "0.1.0"

__all__ = [
    "__version__",
    # Constants
    "T_NORMOTHERMIA_C",
    "T_GLASS_M22_C",
    "T_FREEZING_M22_C",
    "VT_STOCHASTIC_ANCHOR_L_H",
    "SIGMA_FRACTURE_MPA",
    "MAX_COOLING_RATE_NEAR_TG",
    # F3 Ischemia
    "q10_for_T",
    "tau_eq",
    "equivalent_ischemic_dose",
    "assert_ischemia_domain",
    # F4 Nucleation
    "vt_product",
    "t_max_nucleation",
    "p_no_nucleation",
    "heterogeneous_nucleation_rate",
    # F5 Cooling
    "CoolingPhase",
    "phase_for_T",
    "recommended_cooling_rate",
    "validate_cooling_profile",
    # Thermal stress
    "sigma_thermal",
    "fracture_risk",
    "critical_biot_length",
    # CPA toxicity
    "arrhenius_factor",
    "d_cpa_predicted",
    "predicted_ocr_retention",
    # Predictions
    "eval_p19",
    "check_p19_derivation",
    "eval_h2",
    "eval_h3",
    "eval_h4",
    "eval_h5",
    "Verdict",
    "PredictionVerdict",
    # Domains
    "check_domain_limits",
    "is_hibernator_exception",
    "WholeBodyStatus",
    # Reporting
    "generate_protocol_report",
    "export_predictions_csv",
    # Organ Projector
    "compute_bsa_dubois",
    "estimate_organ_morphometry",
    "project_multiorgan_constraints",
    "format_multiorgan_markdown_report",
    "OrganSpecification",
    # Thermal Recipes
    "generate_vitrification_recipe",
    "export_recipe_csv",
    "export_planer_kryo_format",
    "RecipeStep",
    # CPA Washout
    "compute_peak_volume_excursion",
    "design_washout_protocol",
    "WashoutStep",
    # BOA Connector
    "normalize_organ_volume_dict",
    "load_boa_segmentation_file",
    "project_from_boa_file",
]

# --- Design specification: what a given organ actually REQUIRES (StasisPath 2026) ---
from stasispath.design_spec import (
    Geometry,
    Admissibility,
    DesignSpec,
    characteristic_length,
    achievable_cooling_rate,
    molarity_for_ccr,
    required_ccr,
    geometry_flip_factor,
    design_spec,
    screen_candidate_cpa,
)

# --- Regime guards: the premises that silently break a calculation ---
from stasispath.assumptions import (
    Severity,
    Violation,
    audit as audit_assumptions,
    guard_biot_regime,
    guard_q10_domain,
    guard_nucleation_regime,
    guard_geometry,
    guard_unmeasured_exponent,
    guard_density_declared,
)

# --- Which experiment to run next, by value of information per unit cost ---
from stasispath.experiment_value import (
    Candidate,
    Assessment,
    expected_value_of_information,
    assess,
    rank,
    stasispath_open_questions,
)
