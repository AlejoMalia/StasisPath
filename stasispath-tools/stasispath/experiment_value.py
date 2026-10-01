"""
Which experiment to run next, by expected value of information per unit cost.

A measurement is worth doing when its plausible range STRADDLES a decision threshold.
A measurement whose outcome cannot change any verdict is expensive theatre, however
elegant. EVOI = 2 * P(prediction crosses the threshold) * (1 + sigma), capped at 1.

This ranking produced the one result the framework's own roadmap had missed: the
cheapest unmeasured quantity (the scaling exponent, P21) is the second most valuable.
"""
from __future__ import annotations
import math
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Candidate:
    name: str
    predicted_value: float
    sigma_absolute: float
    decision_threshold: float
    relative_cost: float
    description: str = ""


@dataclass
class Assessment:
    name: str
    evoi: float
    cost: float
    ratio: float
    recommendation: str
    rationale: str
    description: str = ""


def expected_value_of_information(predicted_value: float, sigma_absolute: float,
                                  decision_threshold: float) -> float:
    sigma = max(sigma_absolute, 1e-9)
    z = abs(predicted_value - decision_threshold) / sigma
    prob_flip = 0.5 * math.erfc(z / math.sqrt(2.0))
    return min(1.0, 2.0 * prob_flip * (1.0 + sigma_absolute))


def assess(c: Candidate, min_evoi: float = 0.15, min_ratio: float = 0.2) -> Assessment:
    evoi = expected_value_of_information(c.predicted_value, c.sigma_absolute, c.decision_threshold)
    ratio = evoi / max(c.relative_cost, 0.01)
    if evoi < min_evoi:
        rec = "SKIP_LOW_VALUE"
        why = (f"Outcome is {abs(c.predicted_value - c.decision_threshold)/max(c.sigma_absolute,1e-9):.1f} "
               f"sigma from the threshold: it is unlikely to change any verdict.")
    elif ratio < min_ratio:
        rec = "DEFER_COST"
        why = (f"Informative (EVOI {evoi:.2f}) but cost {c.relative_cost:.1f} dominates. "
               f"Find a cheaper proxy before committing.")
    else:
        rec = "RUN"
        why = f"EVOI {evoi:.2f} at cost {c.relative_cost:.1f}: plausibly decisive and affordable."
    return Assessment(c.name, evoi, c.relative_cost, ratio, rec, why, c.description)


def rank(candidates: List[Candidate], min_evoi: float = 0.15,
         min_ratio: float = 0.2) -> List[Assessment]:
    return sorted((assess(c, min_evoi, min_ratio) for c in candidates), key=lambda a: -a.ratio)


def stasispath_open_questions() -> List[Candidate]:
    """The framework's own open set as of 2026-10. Thresholds are preregistered."""
    return [
        Candidate("I2 CCR of a candidate low-toxicity CPA", 0.30, 0.36, 0.426, 1.0,
                  "DSC calorimetry. Days. Resolves frontier X2 without P19 if it clears."),
        Candidate("P21 scaling exponent n", 2.00, 0.26, 2.34, 0.5,
                  "One control vessel, three small and three large bags, one thermocouple."),
        Candidate("I5 nucleation rate J at -6 C", 0.57, 0.285, 0.85, 12.0,
                  "Liver nucleation series. Months."),
        Candidate("I4 human tau_eq with optimal reperfusion", 17.0, 7.65, 12.5, 30.0,
                  "Clinical series. Years. Highest EVOI, highest cost."),
        Candidate("P19 LTP after vitrification", 0.142, 0.078, 0.25, 20.0,
                  "Full electrophysiology. The direct assault on X2."),
    ]
