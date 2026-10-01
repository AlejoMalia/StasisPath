import unittest
from stasispath.cpa_washout import (
    compute_peak_volume_excursion,
    design_washout_protocol,
)


class TestCPAWashout(unittest.TestCase):
    def test_volume_excursion_with_mannitol_clamp(self):
        # Step 1 washing from 9.35 M to 7.95 M (85%) with 300 mM mannitol clamps peak swelling <= 1.15
        v_safe = compute_peak_volume_excursion(
            internal_cpa_m=9.35,
            external_cpa_m=7.95,
            external_mannitol_mm=300.0,
        )
        self.assertLessEqual(v_safe, 1.15)
        self.assertGreaterEqual(v_safe, 1.0)

    def test_abrupt_washout_causes_lysis(self):
        # Abrupt washout into pure water (0 CPA, 0 mannitol) causes massive swelling > 1.50
        v_burst = compute_peak_volume_excursion(
            internal_cpa_m=9.35,
            external_cpa_m=0.0,
            external_mannitol_mm=0.0,
        )
        self.assertGreater(v_burst, 1.50)

    def test_protocol_synthesis_m22(self):
        res = design_washout_protocol(initial_cpa="M22", sample_thickness_or_lc_cm=0.04)
        self.assertEqual(len(res["steps"]), 7)
        self.assertTrue(res["all_steps_osmotically_safe"])
        self.assertGreater(res["total_duration_minutes"], 30.0)




if __name__ == "__main__":
    unittest.main()
