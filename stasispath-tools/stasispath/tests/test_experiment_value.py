"""Value of information: which experiment is worth running."""
import pytest
from stasispath.experiment_value import (
    Candidate, assess, rank, expected_value_of_information, stasispath_open_questions,
)


def test_evoi_is_maximal_at_the_decision_boundary():
    on = expected_value_of_information(1.0, 0.1, 1.0)
    off = expected_value_of_information(1.0, 0.1, 5.0)
    assert on > off and off < 1e-6


def test_evoi_is_bounded():
    assert 0.0 <= expected_value_of_information(0.3, 10.0, 0.426) <= 1.0


def test_calorimetry_outranks_full_electrophysiology():
    ranked = rank(stasispath_open_questions())
    assert ranked[0].name.startswith("I2")
    assert ranked[0].ratio > ranked[-1].ratio * 50


def test_the_cheap_forgotten_experiment_ranks_second():
    """P21 is one afternoon of bags and a thermocouple, and it carries the whole projection."""
    ranked = rank(stasispath_open_questions())
    assert ranked[1].name.startswith("P21")
    assert ranked[1].recommendation == "RUN"


def test_expensive_but_decisive_is_deferred_not_skipped():
    """I4 has the highest EVOI of all and is still deferred: cost, not irrelevance."""
    by_name = {a.name: a for a in rank(stasispath_open_questions())}
    i4 = next(a for n, a in by_name.items() if n.startswith("I4"))
    assert i4.evoi == pytest.approx(1.0, abs=1e-3)
    assert i4.recommendation == "DEFER_COST"


def test_uninformative_measurement_is_skipped():
    c = Candidate("far from any threshold", 1.0, 0.01, 50.0, 0.1)
    assert assess(c).recommendation == "SKIP_LOW_VALUE"


def test_ranking_is_by_value_per_cost():
    ranked = rank(stasispath_open_questions())
    assert all(ranked[i].ratio >= ranked[i + 1].ratio for i in range(len(ranked) - 1))
