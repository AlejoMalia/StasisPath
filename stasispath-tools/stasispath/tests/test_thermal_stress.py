import unittest
from stasispath.thermal_stress import (
    radial_temperature_gradient,
    sigma_thermal,
    fracture_risk,
    critical_biot_length,
)


class TestThermalStress(unittest.TestCase):
    def test_slow_rate_safe(self):
        # 0.10 °C/min in LC = 2.0 cm should give low stress < 1.0 MPa (below 2.0 MPa limit)
        risk = fracture_risk(cooling_rate_c_min=0.10, lc_cm=2.0)
        self.assertFalse(risk["will_fracture"])
        self.assertEqual(risk["risk_level"], "LOW")

    def test_fast_rate_fracture(self):
        # 3.0 °C/min in LC = 3.9 cm (human organ radius) will severely exceed 2.0 MPa
        risk = fracture_risk(cooling_rate_c_min=3.0, lc_cm=3.9)
        self.assertTrue(risk["will_fracture"])
        self.assertIn("FRACTURE", risk["risk_level"])

    def test_biot_length(self):
        # Bi = 1 length should be around ~0.2 cm to 0.5 cm
        lc_star = critical_biot_length(h_heat_transfer=250.0, k_conductivity=0.5)
        self.assertAlmostEqual(lc_star, 0.20, places=2)


if __name__ == "__main__":
    unittest.main()
