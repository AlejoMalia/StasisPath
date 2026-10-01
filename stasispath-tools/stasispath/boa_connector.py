"""
BOA / TotalSegmentator Connector Module: Ingestion of Radiological CT/MRI Organ Segmentations.
Seamlessly parses volumetric outputs from Body-and-Organ-Analysis (BOA) and TotalSegmentator
to feed patient-specific anatomy into the StasisPath Multi-Organ Projector.
"""

import json
import csv
import os
from typing import Dict, Any, Optional
from stasispath.organ_projector import project_multiorgan_constraints, format_multiorgan_markdown_report


def normalize_organ_volume_dict(raw_dict: Dict[str, float], input_unit: str = "auto") -> Dict[str, float]:
    """
    Normalizes a dictionary of organ volumes to Liters (L), consolidating left/right pairs.

    Args:
        raw_dict: Key-value mapping of organ name to volume.
        input_unit: 'auto', 'ml' (cm³), 'mm3', or 'l'.

    Returns:
        Dict with canonical keys ('liver', 'brain', 'kidney', 'heart', 'lung', 'pancreas', 'trunk') in Liters.
    """
    # Detect unit if auto
    max_val = max(raw_dict.values()) if raw_dict else 1.0
    if input_unit == "auto":
        if max_val > 50000.0:
            unit_factor = 1.0e-6  # mm³ to L
        elif max_val > 50.0:
            unit_factor = 1.0e-3  # mL / cm³ to L
        else:
            unit_factor = 1.0  # Already in Liters
    elif input_unit == "mm3":
        unit_factor = 1.0e-6
    elif input_unit in ["ml", "cm3"]:
        unit_factor = 1.0e-3
    else:
        unit_factor = 1.0

    normalized = {}
    kidney_vols = []
    lung_vols = []

    for raw_k, raw_v in raw_dict.items():
        k = raw_k.lower().strip()
        v_liters = float(raw_v) * unit_factor

        if "liver" in k or "higado" in k:
            normalized["liver"] = v_liters
        elif "brain" in k or "cerebro" in k or "enceph" in k:
            normalized["brain"] = v_liters
        elif "kidney" in k or "rinon" in k or "ren" in k:
            kidney_vols.append(v_liters)
        elif "heart" in k or "corazon" in k or "myocard" in k:
            normalized["heart"] = v_liters
        elif "lung" in k or "pulmon" in k:
            lung_vols.append(v_liters)
        elif "pancreas" in k:
            normalized["pancreas"] = v_liters
        elif "spleen" in k or "bazo" in k:
            normalized["spleen"] = v_liters
        elif "trunk" in k or "torso" in k or "body" in k or "abdomen" in k:
            normalized["trunk"] = v_liters

    # Handle paired kidneys: if multiple provided, use mean for single kidney
    if kidney_vols:
        normalized["kidney"] = sum(kidney_vols) / len(kidney_vols)

    # Handle lungs: combine left + right
    if lung_vols:
        normalized["lung"] = sum(lung_vols)

    return normalized


def load_boa_segmentation_file(filepath: str) -> Dict[str, float]:
    """
    Parses a JSON or CSV output file exported by Body-and-Organ-Analysis or TotalSegmentator.

    Args:
        filepath: Path to .json or .csv file.

    Returns:
        Dict of standardized organ volumes in Liters.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Segmentation file not found: {filepath}")

    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".json":
        with open(filepath, mode="r", encoding="utf-8") as f:
            data = json.load(f)
            # Handle nested formats (e.g. {'volumes': {...}} or {'structures': {...}})
            if "volumes" in data and isinstance(data["volumes"], dict):
                data = data["volumes"]
            elif "organs" in data and isinstance(data["organs"], dict):
                data = data["organs"]
            return normalize_organ_volume_dict(data)

    elif ext == ".csv":
        data = {}
        with open(filepath, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row_clean = {k.strip().lower(): v.strip() for k, v in row.items() if k}
                name = row_clean.get("organ") or row_clean.get("label") or row_clean.get("structure")
                val_str = (
                    row_clean.get("volume")
                    or row_clean.get("volume_ml")
                    or row_clean.get("volume_mm3")
                    or row_clean.get("volume_cm3")
                )
                if name and val_str:
                    try:
                        data[name] = float(val_str)
                    except ValueError:
                        continue
        return normalize_organ_volume_dict(data)

    else:
        raise ValueError(f"Unsupported file format '{ext}'. Expected .json or .csv.")


def project_from_boa_file(
    filepath: str,
    age_years: float,
    height_cm: float,
    weight_kg: float,
    sex: str = "M",
    preperfusion_delay_min: float = 15.0,
) -> Dict[str, Any]:
    """
    High-level pipeline: Loads CT/MRI segmentation file, computes personalized organ constraints,
    and returns full analysis with direct imaging volumetric provenance.
    """
    custom_volumes = load_boa_segmentation_file(filepath)
    return project_multiorgan_constraints(
        age_years=age_years,
        height_cm=height_cm,
        weight_kg=weight_kg,
        sex=sex,
        preperfusion_delay_min=preperfusion_delay_min,
        custom_organ_volumes_liters=custom_volumes,
    )
