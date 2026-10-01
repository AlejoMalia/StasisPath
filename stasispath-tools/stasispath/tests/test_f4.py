import unittest
from stasispath.f4_nucleation import (
    t_max_nucleation,
    vt_product,
    p_no_nucleation,
    diagnose_nucleation_mechanism,
)


class TestF4Nucleation(unittest.TestCase):
    def test_anchor_values(self):
        # Porcine kidney anchor: 0.20 L => ~5.0 h
        t_kidney = t_max_nucleation(0.20)
        self.assertAlmostEqual(t_kidney, 5.0, places=2)

        # Human liver anchor: 1.50 L => ~0.667 h (40 min)
        t_liver = t_max_nucleation(1.50)
        self.assertAlmostEqual(t_liver, 1.0 / 1.50, places=2)
        self.assertAlmostEqual(t_liver * 60.0, 40.0, places=1)

    def test_poisson_survival(self):
        # Exactly at t_max, P_survival = exp(-1) ≈ 0.367879
        p_surv = p_no_nucleation(0.20, 5.0)
        self.assertAlmostEqual(p_surv, 0.367879, places=4)

        # As time increases, probability drops monotonically
        self.assertLess(p_no_nucleation(0.20, 10.0), p_surv)

    def test_interfacial_defect_diagnosis(self):
        # If kidney nucleates in 0.5 h (< 1.0 h) while saline holds 6.0 h
        diag = diagnose_nucleation_mechanism(V_L=0.20, t_observed_h=0.5, t_saline_control_h=6.0)
        self.assertEqual(diag["verdict"], "SURFACE_OR_CONTAINER_DOMINATED")


if __name__ == "__main__":
    unittest.main()
