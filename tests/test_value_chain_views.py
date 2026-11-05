"""Cross-sector value-chain shapes; no evidence truth or three-page rendering claim."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path
from jsonschema import ValidationError

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("value_chain", ROOT / "scripts/validate_value_chain_view.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)


class ValueChainViews(unittest.TestCase):
    def load(self, name):
        return json.loads((ROOT / "tests" / "fixtures" / name).read_text(encoding="utf-8"))

    def test_two_contrasting_business_models(self):
        manufacturer = self.load("value_chain_manufacturing_v01.json")
        assets = self.load("value_chain_asset_service_v01.json")
        self.assertEqual(m.check_view(manufacturer)["activities"], 9)
        self.assertEqual(m.check_view(assets)["activities"], 7)
        self.assertEqual(m.check_view(assets)["drivers"], 4)

    def test_dangling_driver_rejected(self):
        a = self.load("value_chain_asset_service_v01.json")
        a["activities"][0]["driver_refs"] = ["MISSING"]
        with self.assertRaises(ValueError): m.check_view(a)

    def test_false_factual_activity_rejected(self):
        a = self.load("value_chain_asset_service_v01.json")
        a["activities"][0]["epistemic_status"] = "fact"
        with self.assertRaises(ValueError): m.check_view(a)

    def test_no_ai_baseline_required(self):
        a = self.load("value_chain_asset_service_v01.json")
        del a["opportunities"][0]["baseline_no_ai"]
        with self.assertRaises(ValidationError): m.check_view(a)

    def test_dangling_use_case_activity_rejected(self):
        a = self.load("value_chain_asset_service_v01.json")
        a["opportunities"][0]["activity_id"] = "MISSING"
        with self.assertRaises(ValueError): m.check_view(a)

    def test_render_permission_cannot_be_inserted(self):
        a = self.load("value_chain_asset_service_v01.json")
        a["committee_authorized"] = True
        with self.assertRaises(ValidationError): m.check_view(a)


if __name__ == "__main__":
    unittest.main()
