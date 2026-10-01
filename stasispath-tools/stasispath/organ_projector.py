"""
Organ Projector & Multi-Organ Constraints Module: Anthropometric Biophysical Profiling.
Translates age, height, weight, sex, and organ geometric scales into thermodynamic constraints.

IMPORTANT EPISTEMIC DISCLAIMER:
    This module IS NOT a validated whole-body stasis protocol generator.
    It is an anthropometric physical constraint projector. Whole-body reversible stasis
    in adult non-hibernating mammals remains an unverified scientific frontier.
"""

import math
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from stasispath.constants import (
    VT_STOCHASTIC_ANCHOR_L_H,
    SIGMA_FRACTURE_MPA,
    T_GLASS_M22_C,
)
from stasispath.f3_ischemia import tau_eq
from stasispath.f4_nucleation import t_max_nucleation
from stasispath.thermal_stress import sigma_thermal, fracture_risk
from stasispath.cpa_toxicity import predicted_ocr_retention

# Formal thermoelastic hypothesis disclosure for peer review defense
THERMOELASTIC_HYPOTHESIS_DISCLOSURE = (
    "Hipótesis del cálculo de tensión térmica (σ_th): Modelo de elasticidad lineal isotrópica vítrea "
    "por debajo de Tg (E = 1.2 GPa, ν = 0.35, α = 50 ppm/K, difusividad térmica α_diff = 0.078 cm²/min). "
    "Asume enfriamiento de sólido homogéneo sin relajación plástica ni microfisuración progresiva."
)


@dataclass
class OrganSpecification:
    name: str
    volume_liters: float
    characteristic_radius_cm: float  # LC
    primary_failure_mode: str
    epistemic_status: str
    cellular_ischemic_limit_min: float  # 37 °C warm ischemia limit
    is_parenchymal: bool = True
    volume_source: str = "Allometric ICRP 89 / Du Bois (Incertidumbre ±15-20%)"


def compute_bsa_dubois(height_cm: float, weight_kg: float) -> float:
    """
    Computes Body Surface Area (BSA) in m² using the classical Du Bois formula:
        BSA = 0.007184 * (weight^0.425) * (height^0.725)
    """
    return 0.007184 * (weight_kg ** 0.425) * (height_cm ** 0.725)


def estimate_organ_morphometry(
    age_years: float,
    height_cm: float,
    weight_kg: float,
    sex: str = "M",
    custom_organ_volumes_liters: Optional[Dict[str, float]] = None,
) -> List[OrganSpecification]:
    """
    Estimates organ volumes and characteristic conduction lengths based on
    allometric scaling (ICRP 89 reference man adjusted for BSA and age) or direct
    CT/BOA segmentation masks when provided.

    Args:
        age_years: Subject age in years.
        height_cm: Height in centimeters.
        weight_kg: Weight in kilograms.
        sex: 'M' or 'F' (case-insensitive).
        custom_organ_volumes_liters: Optional dict with direct CT/BOA measured volumes
                                     (e.g. {'liver': 1.55, 'brain': 1.30, 'kidney': 0.18}).

    Returns:
        List of OrganSpecification instances for major organ beds.
    """
    sex_clean = sex.upper()
    bsa = compute_bsa_dubois(height_cm, weight_kg)
    ref_bsa = 1.90 if sex_clean == "M" else 1.65

    # Scale factor for parenchymal organs relative to reference body size
    scale_factor = bsa / ref_bsa

    # Age attenuation factors (gradual organ atrophy in late decades)
    age_brain_factor = max(0.85, 1.0 - max(0.0, age_years - 50.0) * 0.004)
    age_kidney_factor = max(0.75, 1.0 - max(0.0, age_years - 40.0) * 0.006)
    age_liver_factor = max(0.80, 1.0 - max(0.0, age_years - 55.0) * 0.005)

    custom = custom_organ_volumes_liters or {}

    def get_vol(key: str, default_val: float) -> tuple:
        if key in custom:
            return (custom[key], "Segmentación Imagen CT/BOA (Incertidumbre ±5%)")
        for k, v in custom.items():
            if key in k.lower():
                return (v, "Segmentación Imagen CT/BOA (Incertidumbre ±5%)")
        return (default_val, "Alometría Poblacional ICRP 89 / Du Bois (Incertidumbre ±15-20%)")

    # 1. Liver (Hígado)
    v_liver_base = (1.60 if sex_clean == "M" else 1.40) * scale_factor * age_liver_factor
    v_liver, src_liver = get_vol("liver", v_liver_base)
    lc_liver = 4.2 * ((v_liver / 1.60) ** (1.0 / 3.0))

    # 2. Brain (Cerebro)
    v_brain_base = (1.35 if sex_clean == "M" else 1.25) * age_brain_factor
    v_brain, src_brain = get_vol("brain", v_brain_base)
    lc_brain = 3.8 * ((v_brain / 1.35) ** (1.0 / 3.0))

    # 3. Kidneys (Riñón individual)
    v_kidney_base = (0.18 if sex_clean == "M" else 0.15) * scale_factor * age_kidney_factor
    v_kidney_single, src_kidney = get_vol("kidney", v_kidney_base)
    lc_kidney = 2.2 * ((v_kidney_single / 0.18) ** (1.0 / 3.0))

    # 4. Heart (Corazón)
    v_heart_base = (0.33 if sex_clean == "M" else 0.28) * scale_factor
    v_heart, src_heart = get_vol("heart", v_heart_base)
    lc_heart = 2.6 * ((v_heart / 0.33) ** (1.0 / 3.0))

    # 5. Lungs (Pulmones, volumen parenquimal + vascular)
    v_lung_base = (0.90 if sex_clean == "M" else 0.75) * scale_factor
    v_lung, src_lung = get_vol("lung", v_lung_base)
    lc_lung = 3.2 * ((v_lung / 0.90) ** (1.0 / 3.0))

    # 6. Pancreas (Páncreas)
    v_pancreas_base = (0.10 if sex_clean == "M" else 0.08) * scale_factor
    v_pancreas, src_pancreas = get_vol("pancreas", v_pancreas_base)
    lc_pancreas = 1.4 * ((v_pancreas / 0.10) ** (1.0 / 3.0))

    # 7. Compartimento Térmico Equivalente: Tronco Profundo / Masa Esplácnica Central
    # Cota superior de masa térmica central (no es un órgano individual)
    v_trunk_base = (25.0 if sex_clean == "M" else 20.0) * (weight_kg / (73.0 if sex_clean == "M" else 60.0))
    v_trunk_core, src_trunk = get_vol("trunk", v_trunk_base)
    lc_trunk = 11.5 * ((v_trunk_core / 25.0) ** (1.0 / 3.0))

    return [
        OrganSpecification(
            name="Liver (Hígado)",
            volume_liters=round(v_liver, 3),
            characteristic_radius_cm=round(lc_liver, 2),
            primary_failure_mode="Bulk Ice Nucleation (F4) & Fourier Conduction Delay",
            epistemic_status="E3 Acotado (Trasplante porcino viable; humano subzero acotado)",
            cellular_ischemic_limit_min=30.0,
            is_parenchymal=True,
            volume_source=src_liver,
        ),
        OrganSpecification(
            name="Brain (Cerebro)",
            volume_liters=round(v_brain, 3),
            characteristic_radius_cm=round(lc_brain, 2),
            primary_failure_mode="Electrophysiological Gap (X2: LTP preservation) & CPA Osmotic Shock",
            epistemic_status="E2 en Lonchas (German 2026); E0 en Órgano Completo (Fahy 2026 bioRxiv)",
            cellular_ischemic_limit_min=10.0,
            is_parenchymal=True,
            volume_source=src_brain,
        ),
        OrganSpecification(
            name="Kidney Single (Riñón Individual)",
            volume_liters=round(v_kidney_single, 3),
            characteristic_radius_cm=round(lc_kidney, 2),
            primary_failure_mode="Devitrification during warming & Medullary osmotic perfusion",
            epistemic_status="E3 Verificado en Rata (Bischof 2023 100d); Porcino viable (Uygun 2026)",
            cellular_ischemic_limit_min=45.0,
            is_parenchymal=True,
            volume_source=src_kidney,
        ),
        OrganSpecification(
            name="Heart (Corazón)",
            volume_liters=round(v_heart, 3),
            characteristic_radius_cm=round(lc_heart, 2),
            primary_failure_mode="Microvascular No-Reflow & Acute Ischemic Arrhythmia",
            epistemic_status="E3 en Hipotermia corta; Vitrificación no demostrada",
            cellular_ischemic_limit_min=20.0,
            is_parenchymal=True,
            volume_source=src_heart,
        ),
        OrganSpecification(
            name="Lungs (Pulmones)",
            volume_liters=round(v_lung, 3),
            characteristic_radius_cm=round(lc_lung, 2),
            primary_failure_mode="Alveolar Capillary Leakage & Severe Washout Edema",
            epistemic_status="E1 Preservación estructural; E3 pendiente",
            cellular_ischemic_limit_min=60.0,
            is_parenchymal=True,
            volume_source=src_lung,
        ),
        OrganSpecification(
            name="Pancreas (Páncreas)",
            volume_liters=round(v_pancreas, 3),
            characteristic_radius_cm=round(lc_pancreas, 2),
            primary_failure_mode="Enzymatic Autolysis & Reperfusion Pancreatitis",
            epistemic_status="E3 Aislado en Isletas; Órgano vascularizado complejo",
            cellular_ischemic_limit_min=30.0,
            is_parenchymal=True,
            volume_source=src_pancreas,
        ),
        OrganSpecification(
            name="Trunk Deep Core [Compartimento Térmico Equivalente / Masa Central]",
            volume_liters=round(v_trunk_core, 2),
            characteristic_radius_cm=round(lc_trunk, 2),
            primary_failure_mode="Fourier Conduction Barrier (C3) & Severe Thermal Stress (C1)",
            epistemic_status="E0 ABIERTO / NO RESUELTO (Cota de masa no parenquimatosa)",
            cellular_ischemic_limit_min=15.0,
            is_parenchymal=False,
            volume_source=src_trunk,
        ),
    ]


def project_multiorgan_constraints(
    age_years: float,
    height_cm: float,
    weight_kg: float,
    sex: str = "M",
    preperfusion_delay_min: float = 15.0,
    preperfusion_temp_c: float = 25.0,
    subzero_loading_temp_c: float = -22.0,
    subzero_loading_time_min: float = 25.0,
    cooling_rate_near_tg: float = 0.10,
    custom_organ_volumes_liters: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """
    Generates a full biophysical constraint projection matrix for an individual subject.

    Args:
        age_years: Age of individual.
        height_cm: Height in cm.
        weight_kg: Body mass in kg.
        sex: 'M' or 'F'.
        preperfusion_delay_min: Minutes elapsed before cold flush/perfusion initiation.
        preperfusion_temp_c: Average body temperature during initial delay (°C).
        subzero_loading_temp_c: Intended CPA loading temperature (°C, default -22).
        subzero_loading_time_min: Minutes of subzero CPA exposure.
        cooling_rate_near_tg: Planned cooling rate near -123 °C (°C/min).
        custom_organ_volumes_liters: Optional direct CT/BOA volumes.

    Returns:
        Dict with anthropometrics, organ projection table, bottleneck rankings, and disclaimers.
    """
    bsa = compute_bsa_dubois(height_cm, weight_kg)
    organs = estimate_organ_morphometry(
        age_years=age_years,
        height_cm=height_cm,
        weight_kg=weight_kg,
        sex=sex,
        custom_organ_volumes_liters=custom_organ_volumes_liters,
    )

    # Accumulated ischemic burden during initial delay
    tau_initial_hours = tau_eq(t_hours=preperfusion_delay_min / 60.0, T_c=preperfusion_temp_c)
    tau_initial_min = tau_initial_hours * 60.0

    # Metabolic CPA damage estimate
    cpa_eval = predicted_ocr_retention(
        T_c=subzero_loading_temp_c,
        t_exposure_min=subzero_loading_time_min,
        cpa="M22",
    )

    organ_rows = []
    for org in organs:
        # Nucleation limit (Formula F4)
        t_nuc_h = t_max_nucleation(org.volume_liters)
        t_nuc_min = t_nuc_h * 60.0

        # Thermal stress at Tg
        stress_res = fracture_risk(cooling_rate_near_tg, org.characteristic_radius_cm)

        # Ischemic margin remaining
        ischemic_safety_margin_min = org.cellular_ischemic_limit_min - tau_initial_min

        organ_rows.append(
            {
                "name": org.name,
                "volume_L": org.volume_liters,
                "lc_cm": org.characteristic_radius_cm,
                "t_max_nucleation_min": round(t_nuc_min, 1),
                "t_max_nucleation_hours": round(t_nuc_h, 2),
                "sigma_thermal_mpa": round(stress_res["sigma_thermal_mpa"], 3),
                "fracture_risk": stress_res["risk_level"],
                "tau_initial_min": round(tau_initial_min, 1),
                "ischemic_margin_min": round(ischemic_safety_margin_min, 1),
                "primary_failure_mode": org.primary_failure_mode,
                "epistemic_status": org.epistemic_status,
                "is_parenchymal": org.is_parenchymal,
                "volume_source": org.volume_source,
            }
        )

    # Rank limiting parenchymal organs only (strictly parenchymal beds)
    parenchymal = [r for r in organ_rows if r["is_parenchymal"]]

    most_nucleation_limited = min(parenchymal, key=lambda x: x["t_max_nucleation_min"])
    most_conduction_limited = max(parenchymal, key=lambda x: x["lc_cm"])
    most_ischemia_threatened = min(parenchymal, key=lambda x: x["ischemic_margin_min"])

    return {
        "subject": {
            "age_years": age_years,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "sex": sex.upper(),
            "bsa_m2": round(bsa, 2),
        },
        "preperfusion_delay_min": preperfusion_delay_min,
        "tau_eq_accumulated_min": round(tau_initial_min, 1),
        "cpa_metabolic_retention": cpa_eval,
        "organ_constraints": organ_rows,
        "bottlenecks": {
            "nucleation_bottleneck_organ": most_nucleation_limited["name"],
            "nucleation_time_limit_min": most_nucleation_limited["t_max_nucleation_min"],
            "conduction_fracture_bottleneck_organ": most_conduction_limited["name"],
            "largest_parenchymal_lc_cm": most_conduction_limited["lc_cm"],
            "ischemia_bottleneck_organ": most_ischemia_threatened["name"],
            "ischemic_margin_min": most_ischemia_threatened["ischemic_margin_min"],
        },
        "thermoelastic_hypotheses": THERMOELASTIC_HYPOTHESIS_DISCLOSURE,
        "epistemic_boundary": {
            "whole_body_protocol": "NOT_VALIDATED",
            "x2_frontier": "OPEN",
            "warning": (
                "DISCLAIMER: This analysis maps physical and kinetic boundaries per organ bed. "
                "It DOES NOT constitute a validated whole-body stasis protocol. "
                "Reversible stasis of an intact adult human body remains an unresolved scientific frontier."
            ),
        },
    }


def format_multiorgan_markdown_report(analysis: Dict[str, Any]) -> str:
    """
    Formats the multiorgan projection dictionary into an executive Markdown table.
    """
    sub = analysis["subject"]
    b = analysis["bottlenecks"]
    epi = analysis["epistemic_boundary"]

    md = []
    md.append("# PROYECCIÓN DE RESTRICCIONES MULTI-ÓRGANO (STASISPATH)")
    md.append(f"**Sujeto Antropométrico:** {sub['sex']}, {sub['age_years']} años | {sub['height_cm']} cm | {sub['weight_kg']} kg (BSA: {sub['bsa_m2']} m²)")
    md.append(f"**Retraso Pre-perfusión asumido:** {analysis['preperfusion_delay_min']} min a temperatura ambiente ($\\tau_{{eq}} = {analysis['tau_eq_accumulated_min']}\\text{{ min}}$)")
    md.append("")

    md.append("> [!CAUTION]")
    md.append(f"> ### ESTADO DEL MARCO: `{epi['whole_body_protocol']}`")
    md.append(f"> * {epi['warning']}")
    md.append(f"> * **Frontera X2:** `{epi['x2_frontier']}` (la plasticidad sináptica con CPA macroscópico permanece abierta).")
    md.append("")

    md.append("## 1. Órganos Parenquimatosos Individuales")
    md.append("| Órgano | Volumen ($V$) | $LC$ (Radio) | $t_{\\max}$ a −2 °C ($F_4$) | $\\sigma_{\\text{th}}$ ($T_g$) | Margen Isquémico | Cuello de Botella Primario | Fuente de Volumen |")
    md.append("|---|---|---|---|---|---|---|---|")

    parenchymal_rows = [r for r in analysis["organ_constraints"] if r["is_parenchymal"]]
    for r in parenchymal_rows:
        md.append(
            f"| **{r['name']}** | {r['volume_L']:.2f} L | {r['lc_cm']:.1f} cm | "
            f"**{r['t_max_nucleation_min']:.0f} min** ({r['t_max_nucleation_hours']:.1f} h) | "
            f"{r['sigma_thermal_mpa']:.2f} MPa ({r['fracture_risk']}) | "
            f"{r['ischemic_margin_min']:.0f} min | {r['primary_failure_mode']} | {r['volume_source']} |"
        )
    md.append("")

    md.append("## 2. Compartimento Térmico Equivalente (Cota Superior de Masa Central)")
    md.append("*Nota: No constituye un órgano parenquimatoso individual; modela la barrera conductiva toraco-abdominal macroscópica.*")
    md.append("| Compartimento | Masa / Vol. Equiv. | $LC$ Efectivo | $t_{\\max}$ a −2 °C | $\\sigma_{\\text{th}}$ Teórica a $T_g$ | Dictamen Termomecánico |")
    md.append("|---|---|---|---|---|---|")
    compartment_rows = [r for r in analysis["organ_constraints"] if not r["is_parenchymal"]]
    for r in compartment_rows:
        md.append(
            f"| **{r['name']}** | {r['volume_L']:.1f} L (~{r['volume_L']:.0f} kg) | {r['lc_cm']:.1f} cm | "
            f"{r['t_max_nucleation_min']:.0f} min | **{r['sigma_thermal_mpa']:.2f} MPa** | "
            f"`{r['fracture_risk']}` |"
        )
    md.append("")

    md.append("> [!NOTE]")
    md.append(f"> **Fundamento y limitaciones del cálculo de tensión térmica ($\sigma_{{\\text{{th}}}}$):**")
    md.append(f"> {analysis['thermoelastic_hypotheses']}")
    md.append("")

    md.append("## 3. Jerarquía de Órganos Limitantes (Ranking de Cuellos de Botella)")
    md.append(f"1. **Limitante por Nucleación de Hielo (Fórmula F4):** `{b['nucleation_bottleneck_organ']}`")
    md.append(f"   * Dispone de tan solo **{b['nucleation_time_limit_min']} minutos** a −2 °C antes de que la probabilidad de nucleación supere la cota estocástica.")
    md.append(f"2. **Limitante por Conducción Térmica y Fractura ($LC$ máxima):** `{b['conduction_fracture_bottleneck_organ']}`")
    md.append(f"   * Espesor característico $LC = {b['largest_parenchymal_lc_cm']}\\text{{ cm}}$ exige calentamiento volumétrico inductivo (nanowarming); la conducción superficial fallará.")
    md.append(f"3. **Limitante por Vulnerabilidad Isquémica Inicial:** `{b['ischemia_bottleneck_organ']}`")
    md.append(f"   * Margen de seguridad restante tras retraso pre-perfusión: **{b['ischemic_margin_min']} min** antes de daño celular irreversible.")
    md.append(f"4. **Limitante Epistémico de Función Sináptica:** `Brain (Cerebro)`")
    md.append(f"   * Preservar la ultraestructura no garantiza la recuperación electrofisiológica (LTP). Requiere resolver $X_2$.")
    md.append("")

    md.append("---")
    md.append("*Generado por el módulo multi-órgano de StasisPath Toolkit v0.1.0 (StasisPath Framework 2026).*")
    return "\n".join(md)
