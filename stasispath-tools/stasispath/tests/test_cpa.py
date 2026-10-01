import unittest
from stasispath.cpa_toxicity import (
    arrhenius_factor,
    d_cpa_predicted,
    predicted_ocr_retention,
)


class TestCPAToxicity(unittest.TestCase):
    def test_subzero_m22_loading(self):
        # Loading at -22 °C for 25 min should yield D_CPA ≈ 0.142 and OCR retention >= 85%
        res = predicted_ocr_retention(T_c=-22.0, t_exposure_min=25.0, cpa="M22")
        self.assertAlmostEqual(res["d_cpa"], 0.142, places=2)
        self.assertGreaterEqual(res["predicted_ocr_percent"], 85.0)
        self.assertTrue(res["meets_p19_metabolic_target"])

    def test_warm_loading_lethality(self):
        # Loading at +10 °C for 25 min yields high damage (D_CPA > 0.50)
        res = predicted_ocr_retention(T_c=10.0, t_exposure_min=25.0, cpa="M22")
        self.assertGreater(res["d_cpa"], 0.50)
        self.assertLess(res["predicted_ocr_percent"], 50.0)
        self.assertFalse(res["meets_p19_metabolic_target"])


if __name__ == "__main__":
    unittest.main()
