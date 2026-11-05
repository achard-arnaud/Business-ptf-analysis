"""Negative and positive handoff contracts; no external LLM/connector access required."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path
from jsonschema import ValidationError

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("handoff", ROOT / "scripts" / "validate_handoff.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class HandoffContract(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "tests" / "fixtures" / "research_handoff_v01.json").read_text(encoding="utf-8"))

    def reject(self):
        with self.assertRaises((ValueError, ValidationError)):
            m.validate_handoff(self.data)

    def test_valid_read_only(self):
        self.assertEqual(m.validate_handoff(self.data)["status"], "METADATA_VALID")

    def test_unavailable_required_capability_not_ready(self):
        self.data["capabilities"]["github_read"] = "unavailable"
        self.reject()

    def test_recoverable_verified_snapshot(self):
        self.data["capabilities"]["github_read"] = "unavailable"
        self.data["readiness"] = "RECOVERABLE"
        self.data["fallback"] = {"mode": "verified_snapshot", "reason": "Git unavailable",
                                  "snapshot": {"path": "snapshots/fixture.json", "sha256": "f"*64}}
        self.assertEqual(m.validate_handoff(self.data)["readiness"], "RECOVERABLE")

    def test_snapshot_fallback_not_invented(self):
        self.data["capabilities"]["github_read"] = "unavailable"
        self.data["readiness"] = "RECOVERABLE"
        self.data["fallback"] = {"mode": "verified_snapshot", "reason": "No verified snapshot"}
        self.reject()

    def test_duplicate_inputs_rejected(self):
        self.data["inputs"].append(copy.deepcopy(self.data["inputs"][0]))
        self.reject()

    def test_missing_sha_rejected(self):
        del self.data["run_context"]["sha256"]
        self.reject()

    def test_unknown_gate_field_cannot_approve(self):
        self.data["human_approval"] = True
        self.reject()

    def test_blocked_cannot_have_active_fallback(self):
        self.data["readiness"] = "BLOCKED"
        self.reject()


if __name__ == "__main__":
    unittest.main()
