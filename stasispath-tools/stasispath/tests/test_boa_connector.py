import unittest
import os
import json
import tempfile
from stasispath.boa_connector import (
    normalize_organ_volume_dict,
    load_boa_segmentation_file,
    project_from_boa_file,
)


class TestBOAConnector(unittest.TestCase):
    def test_normalize_json_dict(self):
        raw = {
            "liver": 1540.0,  # mL
            "brain": 1320.0,
            "kidney_left": 160.0,
            "kidney_right": 170.0,
            "lung_left": 400.0,
            "lung_right": 450.0,
        }
        norm = normalize_organ_volume_dict(raw, input_unit="ml")
        self.assertAlmostEqual(norm["liver"], 1.54, places=2)
        self.assertAlmostEqual(norm["brain"], 1.32, places=2)
        self.assertAlmostEqual(norm["kidney"], 0.165, places=3)
        self.assertAlmostEqual(norm["lung"], 0.85, places=2)

    def test_load_and_project_from_file(self):
        sample_boa = {
            "volumes": {
                "liver": 1600.0,
                "brain": 1350.0,
                "kidney_left": 175.0,
                "kidney_right": 175.0,
                "heart": 320.0,
            }
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            fpath = os.path.join(tmpdir, "sample_boa.json")
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(sample_boa, f)

            res = project_from_boa_file(
                filepath=fpath,
                age_years=45,
                height_cm=175,
                weight_kg=73,
                sex="M",
            )
            self.assertEqual(res["epistemic_boundary"]["whole_body_protocol"], "NOT_VALIDATED")
            liver_row = next(r for r in res["organ_constraints"] if "Liver" in r["name"])
            self.assertAlmostEqual(liver_row["volume_L"], 1.60, places=2)
            self.assertIn("CT/BOA", liver_row["volume_source"])


if __name__ == "__main__":
    unittest.main()
