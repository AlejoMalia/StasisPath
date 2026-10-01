"""
Predictions module: the frozen P19 decision rule, and four exploratory laboratory hypotheses.

IMPORTANT — what is and is not preregistered
--------------------------------------------
The StasisPath framework freezes five preregistrations, protected by SHA-256 in `red/prereg.lock`:
P15, P18, P19, P20, P21. Of those, this module implements **P19** (`eval_p19`), exactly as frozen.
Thresholds are never "softened": a threshold is not moved to rescue a hypothesis (rule R2).

An earlier version of this module implemented a "softened double threshold" (OCR >= 85 % and
LTP >= 120 %) under the name P1, and four further hypotheses P2-P5 that were never preregistered.
That was a mismatch with the frozen text and it has been removed. The four exploratory hypotheses
below are renamed H2-H5 to make clear that they are **candidate laboratory tests, not
preregistrations**, and two of them rest on a single measured anchor (see `eval_h2`).
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Optional, Tuple

from stasispath.f4_nucleation import t_max_nucleation
from stasispath.thermal_stress import fracture_risk

# ---- Frozen P19 thresholds (verbatim from the preregistration; do not edit) ----
P19_PASS_LTP_PCT: float = 130.0          # arm C must reach >= 130 % of baseline fEPSP
P19_FAIL_LTP_PCT: float = 110.0          # FAIL if arm C <= 110 % while arm B >= 130 %
P19_CI_WINDOW_PP: float = 25.0           # 95 % CI of (C - B) must lie within +/-25 percentage points
P19_B_REPLICATION_PP: float = 20.0       # arm B must replicate F46 within +/-20 percentage points
F46_V3_LTP_PCT: float = 138.1            # German et al. 2026: V3 LTP, CA1 (control 157.7 +/- 7.1)

# ---- Derivation check (DERIVACION.md): predicted damage of the cold arm of P19 ----
DERIVATION_REFUTED_ABOVE: float = 0.25   # damage > 0.25 refutes the Arrhenius derivation
DERIVATION_CONFIRMED_BELOW: float = 0.10  # damage <= 0.10 confirms it


class Verdict(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"
    NOT_INTERPRETABLE = "NOT_INTERPRETABLE"


# Backwards-compatible alias for code that imported the old name.
PredictionVerdict = Verdict


def eval_p19(
    ltp_arm_c_pct: float,
    ltp_arm_b_pct: float,
    ci95_diff_c_minus_b_pp: Tuple[float, float],
    ltp_arm_d_pct: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Evaluate preregistered experiment P19 under its frozen rule.

    P19 asks whether M22 (a chemistry that scales) preserves LTP in adult mouse hippocampal slices.
    Arms: (A) unvitrified control, (B) V3 (positive control, replicates F46), (C) M22 at its working
    concentration, (D) M22 loading and unloading only, without cooling.

    Args:
        ltp_arm_c_pct: LTP in arm C at 60 min after HFS, % of baseline fEPSP.
        ltp_arm_b_pct: LTP in arm B (positive control), same units.
        ci95_diff_c_minus_b_pp: 95 % confidence interval of (C - B), in percentage points.
        ltp_arm_d_pct: optional arm D, used only for the diagnosis.

    Returns:
        dict with `verdict`, the checks that led to it, and the diagnosis provided by arm D.

    Rules (frozen):
        * Quality control: B must replicate F46 (138.1 %) within +/-20 pp, otherwise the experiment is
          not interpretable and is repeated before reading C.
        * PASS         if C >= 130 % and the 95 % CI of (C - B) lies within +/-25 pp.
        * FAIL         if C <= 110 % while B >= 130 %.
        * INCONCLUSIVE otherwise (between 110 and 130 %, or with B failed), and never reinterpreted.
    """
    lo, hi = ci95_diff_c_minus_b_pp
    if lo > hi:
        raise ValueError("ci95_diff_c_minus_b_pp must be (low, high)")

    b_replicates = abs(ltp_arm_b_pct - F46_V3_LTP_PCT) <= P19_B_REPLICATION_PP
    b_functional = ltp_arm_b_pct >= P19_PASS_LTP_PCT
    ci_inside = lo >= -P19_CI_WINDOW_PP and hi <= P19_CI_WINDOW_PP

    checks = {
        "quality_control_B_replicates_F46": b_replicates,
        "B_reaches_130": b_functional,
        "C_reaches_130": ltp_arm_c_pct >= P19_PASS_LTP_PCT,
        "CI_of_C_minus_B_within_25pp": ci_inside,
        "C_at_or_below_110": ltp_arm_c_pct <= P19_FAIL_LTP_PCT,
    }

    if not b_replicates:
        verdict = Verdict.NOT_INTERPRETABLE
        reading = ("Positive control (arm B) did not replicate F46 within +/-20 pp: the experiment is "
                   "not interpretable. Repeat it before reading arm C.")
    elif ltp_arm_c_pct >= P19_PASS_LTP_PCT and ci_inside and b_functional:
        verdict = Verdict.PASS
        reading = ("M22 preserves LTP: the physical route has an exit. A chemistry now exists with "
                   "function and with a CCR compatible with human scale (L3: <= 0.425 C/min for a human brain).")
    elif ltp_arm_c_pct <= P19_FAIL_LTP_PCT and b_functional:
        verdict = Verdict.FAIL
        reading = ("M22 does not preserve LTP while the positive control does: the bottleneck is chemical, "
                   "and P18 should predict that partial freezing or supercooling arrive before vitrification.")
    else:
        verdict = Verdict.INCONCLUSIVE
        reading = ("Between 110 and 130 %, or with arm B failed: inconclusive, and it is not reinterpreted "
                   "(rule R2).")

    diagnosis = None
    if ltp_arm_d_pct is not None and verdict in (Verdict.FAIL, Verdict.INCONCLUSIVE):
        if ltp_arm_d_pct <= P19_FAIL_LTP_PCT:
            diagnosis = "Arm D fails like C: the damage is CHEMICAL TOXICITY. Redesign the CPA (qv*, temperature, loading protocol)."
        elif ltp_arm_d_pct >= P19_PASS_LTP_PCT:
            diagnosis = "Arm D passes and C fails: the damage is THERMAL or from devitrification. Attack it with rate and uniformity."

    return {"verdict": verdict, "checks": checks, "reading": reading, "diagnosis": diagnosis,
            "frozen_thresholds": {"pass_pct": P19_PASS_LTP_PCT, "fail_pct": P19_FAIL_LTP_PCT,
                                  "ci_window_pp": P19_CI_WINDOW_PP, "b_replication_pp": P19_B_REPLICATION_PP}}


def check_p19_derivation(ocr_ratio: float) -> Dict[str, Any]:
    """
    SECONDARY measure of P19 (respiration), compared against the framework's own derivation.

    The framework predicts a damage D = 1 - OCR/control of 0.142 in the cold arm (Arrhenius, DERIVACION.md).
    This is a test of that **derivation**, not a P19 verdict: P19 is decided by LTP alone (`eval_p19`).
    D > 0.25 refutes the derivation; D <= 0.10 confirms it; in between it is undetermined.
    """
    damage = 1.0 - ocr_ratio
    if damage > DERIVATION_REFUTED_ABOVE:
        status = "DERIVATION_REFUTED"
    elif damage <= DERIVATION_CONFIRMED_BELOW:
        status = "DERIVATION_CONFIRMED"
    else:
        status = "UNDETERMINED"
    return {"damage": damage, "status": status, "predicted_damage": 0.142,
            "note": "Refutes or confirms the Arrhenius derivation (I1). It does not decide P19."}


# --------------------------------------------------------------------------------------
# Exploratory laboratory hypotheses H2-H5. NOT preregistered.
# --------------------------------------------------------------------------------------

def eval_h2(V_L: float, t_observed_hours: float, frozen: bool, n_trials: int = 10) -> Dict[str, Any]:
    """
    H2 (exploratory, not preregistered): stochastic supercooling limit V*t ~ 1.0 L.h at -2 C.

    CAUTION: the V*t invariant rests on a SINGLE measured anchor (pig kidney, 0.2 L, 5 h) and the
    framework itself records it as a falsifiable hypothesis, not a valid derivation (FORMULACION F4).
    """
    t_pred = t_max_nucleation(V_L)
    if not frozen and t_observed_hours > 3.0 * t_pred and n_trials >= 10:
        verdict = Verdict.FAIL
        conclusion = ("The V*t volume model is REFUTED: heterogeneous nucleation is container-dependent "
                      "or endogenous inhibitors suppress ice growth.")
    elif frozen and t_observed_hours <= 1.5 * t_pred:
        verdict = Verdict.PASS
        conclusion = "The V*t invariant is consistent with the observation (single-anchor hypothesis)."
    else:
        verdict = Verdict.INCONCLUSIVE
        conclusion = f"Observed {t_observed_hours:.2f} h vs predicted {t_pred:.2f} h. Requires more replicates."
    return {"verdict": verdict, "t_predicted_hours": t_pred, "t_observed_hours": t_observed_hours,
            "conclusion": conclusion, "preregistered": False}


def eval_h3(cooling_rate_c_min: float, lc_cm: float, fractures_detected: bool) -> Dict[str, Any]:
    """H3 (exploratory, not preregistered): thermomechanical fracture threshold near Tg."""
    risk = fracture_risk(cooling_rate_c_min, lc_cm)
    predicted = risk["will_fracture"]
    if predicted and fractures_detected:
        verdict, conclusion = Verdict.PASS, "Predicted thermal stress matches the physical fracture threshold (sigma_th >= 2.0 MPa)."
    elif not predicted and not fractures_detected:
        verdict, conclusion = Verdict.PASS, "Sub-threshold cooling verified without thermomechanical damage."
    elif not fractures_detected and cooling_rate_c_min > 1.0 and lc_cm >= 3.9:
        verdict = Verdict.FAIL
        conclusion = ("No fracture despite a severe gradient: the classical thermoelastic glass model is REFUTED "
                      "for this CPA-tissue matrix (higher compliance or plastic relaxation).")
    else:
        verdict, conclusion = Verdict.INCONCLUSIVE, "Stress near the critical threshold; needs acoustic-emission verification."
    return {"verdict": verdict, "calculated_stress_mpa": risk["sigma_thermal_mpa"],
            "critical_stress_mpa": risk["sigma_critical_mpa"], "conclusion": conclusion, "preregistered": False}


def eval_h4(ocr_retention_at_30min: float, fepsp_stable_to_60min: bool, ldh_massive_spike: bool = False) -> Dict[str, Any]:
    """H4 (exploratory, not preregistered): in vitro reperfusion kinetics after the P19 protocol."""
    passed_ocr = ocr_retention_at_30min >= 0.70
    passed_synaptic = fepsp_stable_to_60min and not ldh_massive_spike
    if passed_ocr and passed_synaptic:
        verdict, conclusion = Verdict.PASS, "Reperfusion recovery verified; the washout does not trigger secondary cytolysis."
    elif not passed_ocr or ldh_massive_spike:
        verdict, conclusion = Verdict.FAIL, "Reperfusion failure: massive cytolysis or ROS-mediated succinate collapse detected."
    else:
        verdict, conclusion = Verdict.INCONCLUSIVE, "Metabolic recovery acceptable, but electrophysiological stability failed."
    return {"verdict": verdict, "passed_ocr": passed_ocr, "passed_synaptic": passed_synaptic,
            "conclusion": conclusion, "preregistered": False}


def eval_h5(t_kidney_observed_hours: float, t_saline_control_hours: float, V_L: float = 0.20) -> Dict[str, Any]:
    """
    H5 (exploratory, not preregistered): organ-scale nucleation scaling in pig kidney.

    CAUTION: same single-anchor caveat as `eval_h2`. The anchor (0.2 L, 5 h at -2 C) is exactly the
    datum this hypothesis predicts, so a PASS here is a replication, not an independent test.
    """
    t_pred = t_max_nucleation(V_L)
    if abs(t_kidney_observed_hours - t_pred) <= 1.5:
        verdict, regime = Verdict.PASS, "VOLUME_STOCHASTIC_GOVERNED"
        conclusion = "Kidney stability matches the 1.0 L.h scaling (~5.0 h): a replication of the anchor."
    elif t_kidney_observed_hours < 1.0 and t_saline_control_hours >= 5.0:
        verdict, regime = Verdict.FAIL, "SURFACE_OR_CATHETER_DEFECT"
        conclusion = ("Premature nucleation (<1.0 h) despite stable saline: freezing is triggered by clamps, "
                      "cannula edges or capsule bubbles, not by bulk volume.")
    else:
        verdict, regime = Verdict.INCONCLUSIVE, "MARGINAL"
        conclusion = f"Observed {t_kidney_observed_hours:.2f} h vs predicted {t_pred:.2f} h."
    return {"verdict": verdict, "regime": regime, "t_predicted_hours": t_pred,
            "t_observed_hours": t_kidney_observed_hours, "conclusion": conclusion, "preregistered": False}
