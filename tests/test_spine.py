from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from h11_runtime.envelope import SchemaError
from h11_runtime.spine import HostInfectionSpine, assert_crossed


class SpineTests(unittest.IsolatedAsyncioTestCase):
    async def test_falciparum_case_crosses_all_six_agents(self):
        spine = HostInfectionSpine()
        result = await spine.run(
            {
                "patient_id": "P-1001",
                "travel_history": ["Kenya"],
                "symptoms": ["fever", "chills"],
                "blood_smear_density_per_ul": 5200.0,
                "entry_compartment": "skin",
            }
        )
        assert_crossed(result)
        payload = result.payload
        self.assertEqual(payload["diagnosis"]["identified_parasite"], "Plasmodium falciparum")
        self.assertEqual(payload["migration_path"], ["skin", "liver", "bloodstream"])
        self.assertTrue(payload["anatomy_ok"])
        self.assertIn("anemia", payload["systemic_effects"])
        self.assertGreater(payload["vitals"]["HeartRate"], 75.0)
        self.assertLess(payload["vitals"]["MeanArterialPressure"], 90.0)
        self.assertEqual(payload["recalled"][0]["payload"]["case_id"], payload["case_id"])
        self.assertGreater(payload["recall_scores"][0], 0.99)
        self.assertIn("Plasmodium falciparum", payload["reason"]["conclusion"])
        self.assertIn("Artemether-Lumefantrine", " ".join(payload["premises"]))
        self.assertTrue(payload["alignment"]["allowed"])
        self.assertIn("H11-ANATOMIA", result.hops)
        self.assertIn("H11-ALIGN", result.hops)

    async def test_missing_symptoms_rejected(self):
        spine = HostInfectionSpine()
        with self.assertRaises(SchemaError):
            await spine.run({"patient_id": "P-0", "travel_history": []})


if __name__ == "__main__":
    unittest.main()
