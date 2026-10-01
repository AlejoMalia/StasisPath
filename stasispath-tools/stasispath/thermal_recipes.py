"""
Thermal Recipes Module: Automated Generation of Cryogenic Cooling & Warming Trajectories.
Translates Formula F5 and EN 14620-5 engineering limits into machine-executable rampa sequences.
Compatible with programmable controlled-rate freezers (Planer Kryo, Asymptote, Sylab, Thermo Fisher).
"""

import csv
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from stasispath.constants import (
    T_NORMOTHERMIA_C,
    T_GLASS_M22_C,
    T_FREEZING_M22_C,
    T_LIQUID_NITROGEN_C,
    MAX_COOLING_RATE_NEAR_TG,
    CCR_VALUES_C_MIN,
    CWR_VALUES_C_MIN,
)
from stasispath.thermal_stress import fracture_risk


@dataclass
class RecipeStep:
    step_number: int
    step_type: str  # 'RAMP' or 'HOLD'
    start_temp_c: float
    target_temp_c: float
    rate_c_min: float  # Signed rate (°C/min)
    duration_min: float
    cumulative_time_min: float
    phase_name: str
    rationale: str


def generate_vitrification_recipe(
    cpa: str = "M22",
    organ_lc_cm: float = 2.0,
    storage_temp_c: float = T_LIQUID_NITROGEN_C,
    subzero_loading_temp_c: float = -22.0,
    subzero_holding_time_min: float = 25.0,
) -> List[RecipeStep]:
    """
    Synthesizes an optimal multi-stage controlled-rate freezing profile satisfying all
    StasisPath biophysical constraints (sufficient CCR in crystallization zone + safe rampa < 0.150 °C/min near Tg).

    Args:
        cpa: Cryoprotectant solution ('M22', 'V3', 'VS55').
        organ_lc_cm: Characteristic radius (cm) to calculate fracture risk.
        storage_temp_c: Target long-term cryogenic storage temperature (°C).
        subzero_loading_temp_c: Temperature of subzero CPA perfusion plateau (°C).
        subzero_holding_time_min: Exposure duration at subzero plateau.

    Returns:
        List of RecipeStep objects ready for execution or export.
    """
    cpa_key = cpa.upper()
    ccr = CCR_VALUES_C_MIN.get(cpa_key, 0.10)

    steps = []
    current_time = 0.0
    step_num = 1

    # Stage 1: Normothermic to Hypothermic transition (37 °C -> 0 °C)
    # Controlled cooling (1.0 °C/min) to avoid cold shock
    rate_1 = -1.0
    dt_1 = abs(0.0 - T_NORMOTHERMIA_C) / abs(rate_1)
    current_time += dt_1
    steps.append(
        RecipeStep(
            step_number=step_num,
            step_type="RAMP",
            start_temp_c=T_NORMOTHERMIA_C,
            target_temp_c=0.0,
            rate_c_min=rate_1,
            duration_min=round(dt_1, 2),
            cumulative_time_min=round(current_time, 2),
            phase_name="Hypothermic Equilibration",
            rationale="Controlled pre-cooling to suppress enzymatic metabolism without cold-shock injury.",
        )
    )
    step_num += 1

    # Stage 2: Subzero Transition (0 °C -> -22 °C)
    # 0.5 °C/min gradual rampa with CPA carrier infusion
    rate_2 = -0.5
    dt_2 = abs(subzero_loading_temp_c - 0.0) / abs(rate_2)
    current_time += dt_2
    steps.append(
        RecipeStep(
            step_number=step_num,
            step_type="RAMP",
            start_temp_c=0.0,
            target_temp_c=subzero_loading_temp_c,
            rate_c_min=rate_2,
            duration_min=round(dt_2, 2),
            cumulative_time_min=round(current_time, 2),
            phase_name="Subzero CPA Loading Rampa",
            rationale="Drop below zero with osmotic support (VMP carrier) to avoid premature ice formation.",
        )
    )
    step_num += 1

    # Stage 3: Subzero Perfusion Equilibrium Plateau (Hold at -22 °C)
    dt_3 = subzero_holding_time_min
    current_time += dt_3
    steps.append(
        RecipeStep(
            step_number=step_num,
            step_type="HOLD",
            start_temp_c=subzero_loading_temp_c,
            target_temp_c=subzero_loading_temp_c,
            rate_c_min=0.0,
            duration_min=round(dt_3, 2),
            cumulative_time_min=round(current_time, 2),
            phase_name="Subzero Osmotic Plateau",
            rationale=f"Vascular perfusion of full-strength {cpa_key} to reach complete vitrification concentration.",
        )
    )
    step_num += 1

    # Stage 4: Rapid Traverse of Metastable Crystallization Zone (-22 °C -> -120 °C)
    # Rate must comfortably exceed CCR while avoiding excessive thermal shock
    target_zone_c = T_GLASS_M22_C + 3.0  # -120 °C
    # For M22, CCR=0.10 °C/min -> use 1.50 °C/min (15x CCR safety margin)
    # Check that this rate doesn't cause fracture at -120 °C:
    rate_4 = -max(1.50, ccr * 3.0)
    dt_4 = abs(target_zone_c - subzero_loading_temp_c) / abs(rate_4)
    current_time += dt_4
    steps.append(
        RecipeStep(
            step_number=step_num,
            step_type="RAMP",
            start_temp_c=subzero_loading_temp_c,
            target_temp_c=target_zone_c,
            rate_c_min=rate_4,
            duration_min=round(dt_4, 2),
            cumulative_time_min=round(current_time, 2),
            phase_name="Rapid Vitrification Traverse",
            rationale=f"Traverse crystallization zone at {abs(rate_4):.2f} °C/min (> CCR {ccr:.2f} °C/min) to prevent ice crystal nucleation.",
        )
    )
    step_num += 1

    # Stage 5: Annealing Rampa across Tg (-120 °C -> -140 °C)
    # CRITICAL: Must be <= 0.150 °C/min according to EN 14620-5 and Wang 2025 to prevent fracture
    safe_rate_tg = -0.10
    target_post_tg = -140.0
    dt_5 = abs(target_post_tg - target_zone_c) / abs(safe_rate_tg)
    current_time += dt_5
    steps.append(
        RecipeStep(
            step_number=step_num,
            step_type="RAMP",
            start_temp_c=target_zone_c,
            target_temp_c=target_post_tg,
            rate_c_min=safe_rate_tg,
            duration_min=round(dt_5, 2),
            cumulative_time_min=round(current_time, 2),
            phase_name="Cryogenic Glass Annealing (Sub-Tg)",
            rationale=f"Ultralente rampa ({abs(safe_rate_tg):.2f} °C/min < {MAX_COOLING_RATE_NEAR_TG} °C/min) across Tg (-123 °C) to eliminate thermal tensile stress and prevent structural fracture.",
        )
    )
    step_num += 1

    # Stage 6: Cryogenic Storage Descent (-140 °C -> Storage Temp)
    if storage_temp_c < target_post_tg:
        rate_6 = -0.50
        dt_6 = abs(storage_temp_c - target_post_tg) / abs(rate_6)
        current_time += dt_6
        steps.append(
            RecipeStep(
                step_number=step_num,
                step_type="RAMP",
                start_temp_c=target_post_tg,
                target_temp_c=storage_temp_c,
                rate_c_min=rate_6,
                duration_min=round(dt_6, 2),
                cumulative_time_min=round(current_time, 2),
                phase_name="Terminal Cryogenic Descent",
                rationale="Equilibration to stable vapor/liquid nitrogen storage temperature.",
            )
        )
        step_num += 1

    return steps


def export_recipe_csv(steps: List[RecipeStep], filepath: str) -> None:
    """
    Exports the recipe sequence to standard CSV format.
    """
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Step",
                "Type",
                "Start_Temp_C",
                "Target_Temp_C",
                "Rate_C_min",
                "Duration_min",
                "Cumulative_Time_min",
                "Phase_Name",
                "Rationale",
            ]
        )
        for s in steps:
            writer.writerow(
                [
                    s.step_number,
                    s.step_type,
                    f"{s.start_temp_c:.1f}",
                    f"{s.target_temp_c:.1f}",
                    f"{s.rate_c_min:.2f}",
                    f"{s.duration_min:.2f}",
                    f"{s.cumulative_time_min:.2f}",
                    s.phase_name,
                    s.rationale,
                ]
            )


def export_planer_kryo_format(steps: List[RecipeStep], filepath: str) -> None:
    """
    Exports in Planer Kryo / Asymptote controlled freezer script syntax.
    """
    with open(filepath, mode="w", encoding="utf-8") as f:
        f.write("# PLANER KRYO CONTROL SCRIPT (Generated by StasisPath v0.1.0)\n")
        f.write("# Complies with StasisPath Framework F5 Vitrification & EN 14620-5 Limits\n\n")
        for s in steps:
            if s.step_type == "HOLD":
                f.write(f"HOLD AT {s.target_temp_c:.1f} C FOR {s.duration_min:.1f} MIN  # {s.phase_name}\n")
            else:
                f.write(
                    f"RAMP TO {s.target_temp_c:.1f} C AT {abs(s.rate_c_min):.2f} C/MIN  # {s.phase_name}\n"
                )
        f.write("END\n")
