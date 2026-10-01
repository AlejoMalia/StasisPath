"""P19 must follow its FROZEN rule exactly; H2-H5 are exploratory and must say so."""
import unittest
from stasispath.predictions import (
    eval_p19, check_p19_derivation, eval_h2, eval_h3, eval_h4, eval_h5, Verdict,
)


class TestP19FrozenRule(unittest.TestCase):
    """Thresholds: PASS C >= 130 %, FAIL C <= 110 % (with B >= 130 %), CI of C-B within +/-25 pp, B within +/-20 pp of 138.1."""

    def test_pass(self):
        r = eval_p19(ltp_arm_c_pct=135.0, ltp_arm_b_pct=138.0, ci95_diff_c_minus_b_pp=(-12.0, 8.0))
        self.assertIs(r["verdict"], Verdict.PASS)

    def test_pass_boundary_exactly_130(self):
        r = eval_p19(130.0, 138.0, (-25.0, 25.0))
        self.assertIs(r["verdict"], Verdict.PASS)          # >= 130 and CI exactly on the +/-25 edge

    def test_just_below_130_is_inconclusive_not_pass(self):
        r = eval_p19(129.9, 138.0, (-10.0, 10.0))
        self.assertIs(r["verdict"], Verdict.INCONCLUSIVE)

    def test_fail(self):
        r = eval_p19(ltp_arm_c_pct=105.0, ltp_arm_b_pct=140.0, ci95_diff_c_minus_b_pp=(-45.0, -25.0))
        self.assertIs(r["verdict"], Verdict.FAIL)

    def test_fail_boundary_exactly_110(self):
        self.assertIs(eval_p19(110.0, 140.0, (-40.0, -20.0))["verdict"], Verdict.FAIL)

    def test_just_above_110_is_inconclusive_not_fail(self):
        self.assertIs(eval_p19(110.1, 140.0, (-40.0, -20.0))["verdict"], Verdict.INCONCLUSIVE)

    def test_gray_zone_is_inconclusive_and_never_reinterpreted(self):
        for c in (115.0, 120.0, 125.0):
            self.assertIs(eval_p19(c, 138.0, (-30.0, -5.0))["verdict"], Verdict.INCONCLUSIVE)

    def test_pass_requires_ci_inside_25_points(self):
        r = eval_p19(140.0, 138.0, (-30.0, 20.0))          # C high, but CI too wide
        self.assertIs(r["verdict"], Verdict.INCONCLUSIVE)

    def test_positive_control_must_replicate_f46(self):
        """B outside 138.1 +/- 20 pp makes the whole experiment non-interpretable, whatever C says."""
        r = eval_p19(ltp_arm_c_pct=150.0, ltp_arm_b_pct=100.0, ci95_diff_c_minus_b_pp=(0.0, 5.0))
        self.assertIs(r["verdict"], Verdict.NOT_INTERPRETABLE)
        self.assertIs(eval_p19(150.0, 160.0, (-5.0, 5.0))["verdict"], Verdict.NOT_INTERPRETABLE)  # 21.9 pp above

    def test_b_failed_means_never_fail_verdict(self):
        """FAIL needs B >= 130. With B at 125 (inside the replication band) it is INCONCLUSIVE."""
        self.assertIs(eval_p19(100.0, 125.0, (-40.0, -10.0))["verdict"], Verdict.INCONCLUSIVE)

    def test_arm_d_diagnosis(self):
        chem = eval_p19(100.0, 140.0, (-50.0, -30.0), ltp_arm_d_pct=102.0)
        self.assertIn("CHEMICAL", chem["diagnosis"])
        therm = eval_p19(100.0, 140.0, (-50.0, -30.0), ltp_arm_d_pct=140.0)
        self.assertIn("THERMAL", therm["diagnosis"])

    def test_old_softened_threshold_is_gone(self):
        """OCR >= 85 % / LTP >= 120 % was NOT the frozen rule. 125 % must not pass."""
        self.assertIsNot(eval_p19(125.0, 138.0, (-5.0, 5.0))["verdict"], Verdict.PASS)

    def test_frozen_thresholds_are_published_in_the_result(self):
        t = eval_p19(135.0, 138.0, (-5.0, 5.0))["frozen_thresholds"]
        self.assertEqual((t["pass_pct"], t["fail_pct"], t["ci_window_pp"], t["b_replication_pp"]), (130.0, 110.0, 25.0, 20.0))

    def test_bad_ci_is_rejected(self):
        with self.assertRaises(ValueError):
            eval_p19(135.0, 138.0, (5.0, -5.0))


class TestDerivationCheck(unittest.TestCase):
    """Respiration is a secondary measure: it tests the Arrhenius derivation, not P19."""

    def test_confirmed(self):
        self.assertEqual(check_p19_derivation(0.92)["status"], "DERIVATION_CONFIRMED")

    def test_refuted_above_025_damage(self):
        self.assertEqual(check_p19_derivation(0.65)["status"], "DERIVATION_REFUTED")

    def test_undetermined_in_between(self):
        self.assertEqual(check_p19_derivation(0.85)["status"], "UNDETERMINED")

    def test_never_claims_to_decide_p19(self):
        self.assertIn("does not decide P19", check_p19_derivation(0.9)["note"])


class TestExploratoryHypotheses(unittest.TestCase):
    def test_none_is_marked_preregistered(self):
        for r in (eval_h2(1.5, 3.5, False, 10), eval_h3(2.0, 3.9, True), eval_h4(0.78, True), eval_h5(4.8, 5.5, 0.20)):
            self.assertFalse(r["preregistered"])

    def test_h2_refutation(self):
        self.assertIs(eval_h2(V_L=1.5, t_observed_hours=3.5, frozen=False, n_trials=10)["verdict"], Verdict.FAIL)

    def test_h4_reperfusion(self):
        self.assertIs(eval_h4(0.78, True)["verdict"], Verdict.PASS)
        self.assertIs(eval_h4(0.50, False, ldh_massive_spike=True)["verdict"], Verdict.FAIL)

    def test_h5_kidney_nucleation(self):
        self.assertIs(eval_h5(4.8, 5.5, 0.20)["verdict"], Verdict.PASS)
        d = eval_h5(0.4, 6.0, 0.20)
        self.assertIs(d["verdict"], Verdict.FAIL)
        self.assertEqual(d["regime"], "SURFACE_OR_CATHETER_DEFECT")

    def test_h5_pass_is_described_as_replication_not_independent_test(self):
        self.assertIn("replication", eval_h5(4.8, 5.5, 0.20)["conclusion"])


if __name__ == "__main__":
    unittest.main()
