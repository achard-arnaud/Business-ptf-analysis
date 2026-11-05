"""Checkpoint shape, replay, optimistic lock and invalidation NRT."""
import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from jsonschema import ValidationError

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("checkpoint", ROOT / "scripts" / "session_checkpoint.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class CheckpointTests(unittest.TestCase):
    def setUp(self):
        self.p = json.loads((ROOT / "tests" / "fixtures" / "session_checkpoint_v01.json").read_text(encoding="utf-8"))

    def test_valid_fixture(self):
        self.assertTrue(m.validate_checkpoint(self.p))

    def test_invalid_stage(self):
        self.p["stage"] = "FAKE_DONE"
        with self.assertRaises(ValidationError): m.validate_checkpoint(self.p)

    def test_output_dependency_must_be_pinned(self):
        self.p["output_pins"][0]["depends_on"] = ["unseen.json"]
        with self.assertRaises(ValueError): m.validate_checkpoint(self.p)

    def test_only_descendant_is_invalidated(self):
        self.assertEqual(m.invalidate_outputs(self.p, ["evidence/claims.json"]), ["analysis/market.md"])
        self.assertEqual(m.invalidate_outputs(self.p, []), [])

    def test_unknown_mutation_is_not_silently_ignored(self):
        with self.assertRaises(ValueError): m.invalidate_outputs(self.p, ["evidence/unknown.json"])

    def test_replay_and_stale_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for pin in [self.p["run_context"], *self.p["input_pins"]]:
                path = root / pin["path"]
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(("fixture " + pin["path"]).encode())
                pin["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(m.verify_inputs(self.p, root, self.p["repo_sha"])["status"], "READY_TO_RESUME")
            (root / "evidence/claims.json").write_text("modified")
            self.assertEqual(m.verify_inputs(self.p, root, self.p["repo_sha"])["status"], "STALE")

    def test_concurrent_head_conflict(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(m.verify_inputs(self.p, tmp, "0"*64)["status"], "CONFLICT")

    def test_reference_does_not_approve(self):
        self.p["gate"] = "APPROVED_REF_ONLY"
        with self.assertRaises(ValueError): m.validate_checkpoint(self.p)
        self.p["human_decision_ref"] = "fixture://approval"
        self.assertTrue(m.validate_checkpoint(self.p))

    def test_path_escape_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError): m.safe_file(tmp, "../../secret")


if __name__ == "__main__":
    unittest.main()
