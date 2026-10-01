import unittest
from stasispath.f5_cooling import (
    phase_for_T,
    CoolingPhase,
    recommended_cooling_rate,
    validate_cooling_profile,
)


class TestF5Cooling(unittest.TestCase):
    def test_phase_identification(self):
        self.assertEqual(phase_for_T(25.0), CoolingPhase.NORMOTHERMIC_PREPARATION)
        self.assertEqual(phase_for_T(5.0), CoolingPhase.HYPOTHERMIC_TRANSITION)
        self.assertEqual(phase_for_T(-10.0), CoolingPhase.SUBZERO_LOADING)
        self.assertEqual(phase_for_T(-60.0), CoolingPhase.RAPID_VITRIFICATION)
        self.assertEqual(phase_for_T(-150.0), CoolingPhase.CRYOGENIC_ANNEALING)

    def test_profile_validation_m22(self):
        # Good profile: rapid traverse between -22 and -123 (1.0 °C/min > 0.10 CCR), slow near Tg (0.10 °C/min < 0.15)
        times = [0.0, 30.0, 131.0, 431.0]
        temps = [0.0, -22.0, -123.0, -153.0]
        res = validate_cooling_profile(times, temps, cpa="M22")
        self.assertTrue(res["valid"])

        # Bad profile: too fast below Tg (-123 to -153 in 10 min = 3.0 °C/min > 0.15)
        times_bad = [0.0, 30.0, 131.0, 141.0]
        res_bad = validate_cooling_profile(times_bad, temps, cpa="M22")
        self.assertFalse(res_bad["valid"])
        self.assertTrue(any("FRACTURE" in v for v in res_bad["violations"]))


if __name__ == "__main__":
    unittest.main()
