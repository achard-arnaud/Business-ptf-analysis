"""Producer-to-receipt checks against actual output bytes and QA report."""
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prepare_artifact_receipt import prepare


class ReceiptProducerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.artifact = Path(self.tmp.name)/"preview.pdf"
        self.artifact.write_bytes(b"%PDF-1.7 synthetic preview fixture\n")
        self.qa = Path(self.tmp.name)/"qa.json"
        self.qa.write_text(json.dumps({"pass": True, "page_count": 3}), encoding="utf-8")

    def make(self,qa=None):
        return prepare(self.artifact,entity_id="synthetic",run_id="fixture-run",
                       kind="render_pdf",producer="candidate-renderer",qa_report=qa,
                       visibility="public",input_refs=["synthetic-fixture"])

    def test_derived_sha_and_prepared_only(self):
        a=self.make(self.qa)
        self.assertEqual(a["sha256"],hashlib.sha256(self.artifact.read_bytes()).hexdigest())
        self.assertEqual(a["qa_state"],"PASS")
        self.assertEqual(a["publication_state"],"prepared_not_published")
        self.assertEqual(a["authorization_state"],"UNREVIEWED")

    def test_qa_failure_cannot_pretend_pass(self):
        self.qa.write_text(json.dumps({"pass": False, "page_count": 3}))
        with self.assertRaises(ValueError): self.make(self.qa)

    def test_missing_pdf_rejected(self):
        self.artifact.unlink()
        with self.assertRaises(FileNotFoundError): self.make()

    def test_output_modified_changes_digest(self):
        first=self.make()["sha256"]
        self.artifact.write_bytes(b"changed output")
        self.assertNotEqual(self.make()["sha256"],first)

    def test_no_browser_run_is_not_run(self):
        self.assertEqual(self.make()["qa_state"],"NOT_RUN")


if __name__=="__main__":
    unittest.main()
