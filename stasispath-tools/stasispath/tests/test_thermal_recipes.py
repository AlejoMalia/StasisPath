import unittest
import os
import tempfile
from stasispath.thermal_recipes import (
     generate_vitrification_recipe,
     export_recipe_csv,
     export_planer_kryo_format,
 )
from stasispath.constants import MAX_COOLING_RATE_NEAR_TG


class TestThermalRecipes(unittest.TestCase):
    def test_recipe_generation_m22(self):
        steps = generate_vitrification_recipe(cpa="M22", organ_lc_cm=2.0)
        self.assertGreaterEqual(len(steps), 5)

        # Check sub-Tg annealing step strictly respects EN 14620-5 limit
        sub_tg_step = next(s for s in steps if "Annealing" in s.phase_name)
        self.assertLessEqual(abs(sub_tg_step.rate_c_min), MAX_COOLING_RATE_NEAR_TG)

        # Check rapid vitrification step exceeds M22 CCR (0.10 °C/min)
        vitrif_step = next(s for s in steps if "Vitrification" in s.phase_name)
        self.assertGreater(abs(vitrif_step.rate_c_min), 0.10)

    def test_recipe_exports(self):
        steps = generate_vitrification_recipe(cpa="M22")
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test_recipe.csv")
            planer_path = os.path.join(tmpdir, "test_planer.txt")

            export_recipe_csv(steps, csv_path)
            export_planer_kryo_format(steps, planer_path)

            self.assertTrue(os.path.exists(csv_path))
            self.assertTrue(os.path.exists(planer_path))

            with open(planer_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("PLANER KRYO CONTROL SCRIPT", content)
                self.assertIn("RAMP TO", content)


if __name__ == "__main__":
    unittest.main()
