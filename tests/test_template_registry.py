"""Registry drift and unsupported-renderer negative NRT (#25)."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path
from jsonschema import ValidationError

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("registry", ROOT / "scripts/check_template_registry.py")
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads((ROOT / "templates/registry.json").read_text(encoding="utf-8"))

    def reject(self):
        with self.assertRaises((ValueError, ValidationError)):
            r.check_registry(self.registry)

    def test_real_registry_matches_repo(self):
        self.assertEqual(r.check_registry(self.registry)["profiles"], 4)
        preview = next(x for x in self.registry["templates"] if x["profile"] == "value-chain-preview")
        self.assertEqual(preview["capability"], "preview")
        self.assertFalse(preview["committee_authorized"])

    def test_audit_has_no_renderer(self):
        audit = next(x for x in self.registry["templates"] if x["profile"] == "audit")
        self.assertEqual(audit["capability"], "schema_only")
        self.assertIsNone(audit["renderer_ref"])

    def test_no_renderer_may_be_claimed_ready(self):
        self.registry["templates"][1]["capability"] = "ready"
        self.reject()

    def test_missing_renderer_rejected(self):
        self.registry["templates"][0]["renderer_ref"] = "renderers/missing.py"
        self.reject()

    def test_committee_authorization_not_implicit(self):
        self.registry["templates"][0]["committee_authorized"] = True
        self.reject()

    def test_duplicate_profile_rejected(self):
        self.registry["templates"].append(copy.deepcopy(self.registry["templates"][0]))
        self.reject()

    def test_missing_schema_rejected_for_demo(self):
        self.registry["templates"][0]["schema_ref"] = None
        self.reject()


if __name__ == "__main__":
    unittest.main()
