"""Artifact receipt state machine negatives; no network or human approval."""
import copy
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path
from jsonschema import ValidationError

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("receipt", ROOT / "scripts/validate_artifact_receipt.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)


class ArtifactReceipts(unittest.TestCase):
    def setUp(self):
        self.p = json.loads((ROOT / "tests/fixtures/artifact_receipt_v01.json").read_text(encoding="utf-8"))

    def reject(self, **kwargs):
        with self.assertRaises((ValueError,ValidationError)):
            m.validate_receipt(self.p, **kwargs)

    def test_prepared_is_not_published(self):
        result=m.validate_receipt(self.p)
        self.assertEqual(result["publication_state"],"prepared_not_published")
        self.assertEqual(result["authorization_state"],"UNREVIEWED")

    def test_unverified_write_is_not_verified(self):
        self.p["publication_state"]="published_unverified"
        self.assertEqual(m.validate_receipt(self.p)["publication_state"],"published_unverified")

    def test_qa_pass_does_not_approve(self):
        self.p["qa_state"]="PASS"
        self.assertEqual(m.validate_receipt(self.p)["authorization_state"],"UNREVIEWED")

    def test_claimed_verified_without_bytes_fails(self):
        self.p["publication_state"]="published_verified"
        self.reject()

    def test_independent_byte_readback_required(self):
        content=b"synthetic receipt bytes"
        digest=hashlib.sha256(content).hexdigest()
        self.p["sha256"]=digest
        self.p["publication_state"]="published_verified"
        self.p["readback"]={"uri":"https://example.org/fixture","sha256":digest,
                            "verified_at":"2026-11-04T00:00:00Z","method":"independent_readback"}
        self.reject()
        self.assertEqual(m.validate_receipt(self.p,remote_readback_bytes=content)["publication_state"],"published_verified")
        self.reject(remote_readback_bytes=b"wrong")

    def test_cannot_forge_source_as_full_original(self):
        self.p["kind"]="source_capture"
        self.p["capture_kind"]="selected_excerpt"
        self.p["hash_scope"]="original_bytes"
        self.reject()

    def test_non_source_does_not_claim_capture_kind(self):
        self.p["capture_kind"]="full_original"
        self.reject()

    def test_hitl_ref_is_not_inferred(self):
        self.p["authorization_state"]="HITL_REFERENCED"
        self.reject()
        self.p["human_decision_ref"]="fixture://human"
        self.assertFalse(m.validate_receipt(self.p)["human_decision_authenticity_verified"])

    def test_readback_claim_with_unverified_state_fails(self):
        self.p["readback"]={"uri":"https://example.org/fixture","sha256":"a"*64,
                            "verified_at":"2026-11-04T00:00:00Z","method":"independent_readback"}
        self.reject()


if __name__=="__main__":
    unittest.main()
