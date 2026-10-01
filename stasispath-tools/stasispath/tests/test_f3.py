import unittest
from stasispath.f3_ischemia import q10_for_T, tau_eq, assert_domain
from stasispath.constants import Q10_WARM, Q10_COLD


class TestF3Ischemia(unittest.TestCase):
    def test_q10_transition(self):
        self.assertEqual(q10_for_T(25.0), Q10_WARM)
        self.assertEqual(q10_for_T(10.0), Q10_COLD)

    def test_tau_eq_reduction(self):
        # At 37 °C, tau_eq equals physical time
        self.assertAlmostEqual(tau_eq(2.0, 37.0), 2.0, places=4)

        # At 10 °C, metabolic rate is strongly depressed
        t_hypo = 2.0
        tau = tau_eq(t_hypo, 10.0)
        # Factor should be > 5.0, so tau < 0.4 h
        self.assertLess(tau, 0.4)
        self.assertGreater(tau, 0.1)

    def test_domain_hibernator_flag(self):
        valid, warning = assert_domain(5.0, species="Ictidomys tridecemlineatus")
        self.assertFalse(valid)
        self.assertIn("DOMAIN BREACH", warning)


if __name__ == "__main__":
    unittest.main()
