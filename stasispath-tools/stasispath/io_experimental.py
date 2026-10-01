"""
IO Experimental Module: Loading Raw Lab CSV Data and Automated Threshold Verification.
Facilitates seamless ingestion of Seahorse OCR, electrophysiology fEPSP, and thermocouple traces.
"""

import csv
from typing import List, Dict, Any, Optional
from stasispath.predictions import check_p19_derivation


def load_ocr_seahorse_csv(filepath: str) -> Dict[str, Any]:
    """
    Parses a Seahorse/Oroboros OCR CSV file containing baseline and post-CPA respiration rates.
    Expected headers: 'condition', 'ocr_pmol_min' or similar.

    Returns:
        Dict with mean fresh control OCR, mean post-CPA OCR, the ratio, and the check of the Arrhenius
        derivation (secondary measure; it does NOT decide P19, which is decided by LTP alone).
    """
    fresh_vals = []
    cpa_vals = []

    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # normalize header keys
            row_clean = {k.strip().lower(): v.strip() for k, v in row.items() if k}
            cond = row_clean.get("group", "") or row_clean.get("condition", "")
            val_str = (
                row_clean.get("ocr", "")
                or row_clean.get("ocr_pmol_min", "")
                or row_clean.get("rate", "")
            )
            if not val_str:
                continue

            val = float(val_str)
            if "fresh" in cond.lower() or "control" in cond.lower():
                fresh_vals.append(val)
            elif "cpa" in cond.lower() or "m22" in cond.lower() or "v3" in cond.lower():
                cpa_vals.append(val)

    if not fresh_vals or not cpa_vals:
        raise ValueError(
            f"CSV must contain rows labeled as 'control'/'fresh' and 'cpa'/'m22'. "
            f"Found fresh: {len(fresh_vals)}, cpa: {len(cpa_vals)}."
        )

    mean_fresh = sum(fresh_vals) / len(fresh_vals)
    mean_cpa = sum(cpa_vals) / len(cpa_vals)
    ratio = mean_cpa / mean_fresh

    return {
        "n_fresh": len(fresh_vals),
        "mean_fresh_ocr": mean_fresh,
        "n_cpa": len(cpa_vals),
        "mean_cpa_ocr": mean_cpa,
        "ocr_retention_ratio": ratio,
        "ocr_percent": ratio * 100.0,
        "derivation_check": check_p19_derivation(ratio),
    }


def load_fepsp_recording_csv(filepath: str) -> Dict[str, Any]:
    """
    Parses electrophysiology LTP recording CSV.
    Expected headers: 'time_min', 'slope_mv_ms'.

    Computes baseline mean (first 15 min), post-tetanus mean (45-60 min), and induction ratio.
    """
    times = []
    slopes = []

    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_clean = {k.strip().lower(): v.strip() for k, v in row.items() if k}
            t_str = row_clean.get("time_min", "") or row_clean.get("time", "")
            s_str = row_clean.get("slope", "") or row_clean.get("fepsp_slope", "")
            if t_str and s_str:
                times.append(float(t_str))
                slopes.append(float(s_str))

    if not times:
        raise ValueError("Could not parse time and slope columns from CSV.")

    baseline = [s for t, s in zip(times, slopes) if t < 0.0]
    post_tetanus_late = [s for t, s in zip(times, slopes) if t >= 45.0]

    if not baseline or not post_tetanus_late:
        # Fallback to simple split if times not zeroed at tetanus
        n = len(slopes)
        baseline = slopes[: max(1, n // 4)]
        post_tetanus_late = slopes[-max(1, n // 4) :]

    mean_base = sum(baseline) / len(baseline)
    mean_late = sum(post_tetanus_late) / len(post_tetanus_late)
    ratio = mean_late / mean_base if mean_base > 0 else 0.0

    ltp_inducible = ratio >= 1.20

    return {
        "mean_baseline_slope": mean_base,
        "mean_late_slope": mean_late,
        "ltp_slope_ratio": ratio,
        "ltp_inducible": ltp_inducible,
    }
