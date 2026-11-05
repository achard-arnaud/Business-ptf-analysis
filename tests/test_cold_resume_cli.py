"""Cold-process checkpoint replay: independent invocation is not cross-model HITL."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "session_checkpoint.py"
FIXTURE = ROOT / "tests" / "fixtures" / "session_checkpoint_v01.json"


class ColdResume(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.record = json.loads(FIXTURE.read_text(encoding="utf-8"))
        for pin in [self.record["run_context"], *self.record["input_pins"]]:
            path = self.root / pin["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(("fixture:" + pin["path"]).encode("utf-8"))
            pin["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.file = self.root / "checkpoint.json"
        self.file.write_text(json.dumps(self.record), encoding="utf-8")

    def run_resume(self, sha=None):
        result = subprocess.run([sys.executable, str(SCRIPT), "resume", str(self.file),
                                 "--root", str(self.root), "--repo-sha", sha or self.record["repo_sha"]],
                                text=True, capture_output=True, check=False)
        return result.returncode, json.loads(result.stdout)

    def test_cold_session_receipt_has_bounded_context(self):
        rc, out = self.run_resume()
        self.assertEqual(rc, 0)
        self.assertEqual(out["status"], "READY_TO_RESUME")
        self.assertEqual(out["critical_claim_refs"], ["C-1"])
        self.assertFalse(out["human_approval_verified"])
        self.assertNotIn("input_pins", out)

    def test_concurrent_head_is_nonzero(self):
        rc, out = self.run_resume("0"*64)
        self.assertEqual(rc, 2)
        self.assertEqual(out["status"], "CONFLICT")

    def test_stale_evidence_is_nonzero(self):
        (self.root / self.record["input_pins"][0]["path"]).write_text("changed", encoding="utf-8")
        rc, out = self.run_resume()
        self.assertEqual(rc, 2)
        self.assertEqual(out["status"], "STALE")

    def test_missing_archive_is_nonzero(self):
        (self.root / self.record["input_pins"][0]["path"]).unlink()
        rc, out = self.run_resume()
        self.assertEqual(rc, 2)
        self.assertEqual(out["status"], "BLOCKED")


if __name__=="__main__":
    unittest.main()
