"""The design specification must reproduce the StasisPath engine exactly."""
import math
import pytest
from stasispath.design_spec import (
    Geometry, Admissibility, characteristic_length, achievable_cooling_rate,
    molarity_for_ccr, required_ccr, geometry_flip_factor, design_spec,
    screen_candidate_cpa, M_TOXIC_MOL_L,
)


def test_headline_number_human_brain():
    """The contribution: a human brain needs CCR <= 0.426 C/min, not M22's 0.10."""
    assert required_ccr(1400.0) == pytest.approx(0.425, abs=0.002)


def test_brain_is_more_permissive_than_m22():
    spec = design_spec("brain", 1400.0)
    assert spec.permissiveness_vs_m22 == pytest.approx(4.25, abs=0.05)


def test_reproduces_engine_organ_table():
    expected = {150.0: 8.58, 300.0: 8.69, 1500.0: 8.96, 1400.0: 8.95}
    for mass, m_req in expected.items():
        assert design_spec("x", mass).required_molarity_mol_l == pytest.approx(m_req, abs=0.02)


def test_whole_body_is_not_viable():
    assert not design_spec("whole_body", 70000.0, Geometry.CYLINDER).viable


def test_geometry_scaling_factors():
    m = 1400.0
    assert characteristic_length(m, Geometry.CYLINDER) == pytest.approx(
        1.5 * characteristic_length(m, Geometry.SPHERE))
    assert characteristic_length(m, Geometry.SLAB) == pytest.approx(
        3.0 * characteristic_length(m, Geometry.SPHERE))


def test_brain_verdict_survives_a_cylinder_geometry_error():
    """Flip factor 1.94 > 1.5, so treating a brain as a sphere cannot flip its verdict."""
    flip = geometry_flip_factor(1400.0)
    assert flip == pytest.approx(1.94, abs=0.02)
    assert flip > 1.5


def test_flip_factor_is_none_when_already_non_viable():
    assert geometry_flip_factor(70000.0, Geometry.CYLINDER) is None


def test_density_is_explicit_not_assumed():
    assert characteristic_length(1000.0, density_g_cm3=1.05) < characteristic_length(1000.0)


def test_molarity_inverse_round_trip():
    for ccr in (0.1, 0.426, 2.5, 5.4):
        assert achievable_cooling_rate(
            characteristic_length(1400.0)) == pytest.approx(0.425, abs=0.002)
        assert molarity_for_ccr(ccr) == pytest.approx(
            (math.log10(ccr) - 15.2) / -1.74, abs=1e-9)


def test_unmeasured_cpa_never_passes_or_fails():
    """A chemistry with no measured CCR must come back UNMEASURED, never a verdict."""
    r = screen_candidate_cpa("some-candidate", None)
    assert r["verdict"] is Admissibility.UNMEASURED
    assert r["measured_ccr_c_min"] is None


def test_m22_clears_the_brain_bar():
    r = screen_candidate_cpa("M22", 0.10)
    assert r["verdict"] is Admissibility.ADMISSIBLE
    assert r["margin_factor"] == pytest.approx(4.25, abs=0.05)


def test_vs55_misses_the_brain_bar():
    assert screen_candidate_cpa("VS55", 2.5)["verdict"] is Admissibility.REJECTED


def test_screening_warns_that_ccr_is_not_function():
    assert "X2" in screen_candidate_cpa("M22", 0.10)["rationale"]


def test_rejects_nonsense_input():
    with pytest.raises(ValueError):
        achievable_cooling_rate(0.0)
    with pytest.raises(ValueError):
        molarity_for_ccr(-1.0)
