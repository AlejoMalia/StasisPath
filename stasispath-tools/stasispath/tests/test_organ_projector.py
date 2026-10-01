import unittest
from stasispath.organ_projector import (
    compute_bsa_dubois,
    estimate_organ_morphometry,
    project_multiorgan_constraints,
    format_multiorgan_markdown_report,
)


class TestOrganProjector(unittest.TestCase):
    def test_bsa_calculation(self):
        # 73 kg, 176 cm male standard reference (Du Bois BSA ~1.889 m²)
        bsa = compute_bsa_dubois(height_cm=176.0, weight_kg=73.0)
        self.assertAlmostEqual(bsa, 1.889, places=2)

    def test_organ_morphometry(self):
        organs = estimate_organ_morphometry(age_years=40, height_cm=175, weight_kg=73, sex="M")
        self.assertEqual(len(organs), 7)

        # Check liver and brain volumes are realistic
        liver = next(o for o in organs if "Liver" in o.name)
        brain = next(o for o in organs if "Brain" in o.name)
        kidney = next(o for o in organs if "Kidney" in o.name)

        self.assertGreater(liver.volume_liters, 1.2)
        self.assertLess(liver.volume_liters, 2.0)
        self.assertGreater(brain.volume_liters, 1.1)
        self.assertLess(brain.volume_liters, 1.6)
        self.assertGreater(kidney.volume_liters, 0.12)
        self.assertLess(kidney.volume_liters, 0.25)

    def test_multiorgan_projection_integrity(self):
        res = project_multiorgan_constraints(
            age_years=50,
            height_cm=175,
            weight_kg=75,
            sex="M",
            preperfusion_delay_min=15.0,
        )

        # Mandatory epistemic flags
        self.assertEqual(res["epistemic_boundary"]["whole_body_protocol"], "NOT_VALIDATED")
        self.assertEqual(res["epistemic_boundary"]["x2_frontier"], "OPEN")

        # Bottlenecks
        b = res["bottlenecks"]
        self.assertIn("Liver", b["nucleation_bottleneck_organ"])
        # Liver t_max at -2 °C should be ~35-45 minutes
        self.assertLess(b["nucleation_time_limit_min"], 50.0)
        self.assertGreater(b["nucleation_time_limit_min"], 30.0)

        # Markdown report generation
        md = format_multiorgan_markdown_report(res)
        self.assertIn("PROYECCIÓN DE RESTRICCIONES MULTI-ÓRGANO", md)
        self.assertIn("NOT_VALIDATED", md)
        self.assertIn("Liver (Hígado)", md)
        self.assertIn("Hipótesis del cálculo de tensión térmica", md)

    def test_custom_ct_volumes(self):
        # Pass direct segmentation volumes from CT/BOA
        custom_vols = {"liver": 1.75, "brain": 1.42}
        res = project_multiorgan_constraints(
            age_years=40,
            height_cm=175,
            weight_kg=73,
            sex="M",
            custom_organ_volumes_liters=custom_vols,
        )
        liver_row = next(r for r in res["organ_constraints"] if "Liver" in r["name"])
        self.assertEqual(liver_row["volume_L"], 1.75)
        self.assertIn("CT/BOA", liver_row["volume_source"])


if __name__ == "__main__":
    unittest.main()

