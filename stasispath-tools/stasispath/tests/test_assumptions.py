"""Regime guards. Two of these encode errors StasisPath actually made."""
from stasispath.assumptions import (
    Severity, audit, guard_biot_regime, guard_q10_domain,
    guard_nucleation_regime, guard_geometry, guard_unmeasured_exponent,
    guard_density_declared,
)


def test_biot_boundary_violation_is_caught():
    """The x2.6 scaling error: LC^-2 applied below the Biot length."""
    v = guard_biot_regime(lc_cm=0.1, exponent_used=2.0)
    assert v is not None and v.severity is Severity.SWITCH_MODEL


def test_biot_consistent_case_passes():
    assert guard_biot_regime(lc_cm=2.31, exponent_used=2.0) is None
    assert guard_biot_regime(lc_cm=0.1, exponent_used=1.0) is None


def test_q10_below_glass_transition_is_fail_stop():
    v = guard_q10_domain(-129.0)
    assert v is not None and v.severity is Severity.FAIL_STOP


def test_q10_outside_measured_range_is_a_warning():
    v = guard_q10_domain(-73.7)
    assert v is not None and v.severity is Severity.WARNING


def test_q10_in_range_passes():
    assert guard_q10_domain(0.0) is None
    assert guard_q10_domain(37.0) is None


def test_isochoric_vs_isobaric_mismatch_is_caught():
    v = guard_nucleation_regime("isochoric")
    assert v is not None and v.severity is Severity.SWITCH_MODEL
    assert guard_nucleation_regime("isobaric") is None


def test_geometry_guard_distinguishes_survivable_from_fatal():
    survives = guard_geometry("cylinder", flip_factor=1.94)
    assert survives is not None and survives.severity is Severity.WARNING
    fatal = guard_geometry("cylinder", flip_factor=1.20)
    assert fatal is not None and fatal.severity is Severity.SWITCH_MODEL


def test_unmeasured_exponent_flagged_until_p21_runs():
    assert guard_unmeasured_exponent(2.0, p21_executed=False) is not None
    assert guard_unmeasured_exponent(2.0, p21_executed=True) is None


def test_silent_density_is_flagged():
    assert guard_density_declared(None) is not None
    assert guard_density_declared(1.05) is None


def test_audit_skips_guards_for_absent_keys():
    assert audit({}) == []


def test_audit_finds_the_two_historical_errors():
    out = audit({"temperature_c": -129.0, "nucleation_regime": "isochoric"})
    sev = {v.severity for v in out}
    assert Severity.FAIL_STOP in sev and Severity.SWITCH_MODEL in sev
