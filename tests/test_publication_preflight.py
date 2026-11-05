"""Fail-closed publication gate: never infer GO_DRAFT or committee approval from a PDF."""
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("preflight",ROOT/"scripts/publication_preflight.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
RECEIPT=json.loads((ROOT/"tests/fixtures/artifact_receipt_v01.json").read_text(encoding="utf-8"))


class PublicationPreflight(unittest.TestCase):
    def setUp(self):
        self.content=b"%PDF-1.7 synthetic"
        self.hash=hashlib.sha256(self.content).hexdigest()
        self.receipt={**RECEIPT,"sha256":self.hash}
        self.manifest={"render_profile":"value_chain_preview","visual_qa":"LAYOUT_PASS_MANUAL_PENDING",
                       "bundle_sha256":"b"*64,"payload_sha256":"c"*64}

    def call(self,**kwargs):
        return m.check_release(self.manifest,self.receipt,self.content,**kwargs)

    def test_preview_is_not_committee(self):
        r=self.call()
        self.assertIn("unsupported_render_profile",r["blockers"])
        self.assertFalse(r["committee_authorized"])

    def test_browser_qa_not_hitl(self):
        self.manifest["render_profile"]="exec"
        self.receipt["qa_state"]="PASS"
        self.assertIn("no_hitl_reference",self.call()["blockers"])
        self.assertIn("frozen_bundle_and_hitl_not_verified",self.call()["blockers"])

    def test_manipulated_pdf_rejected(self):
        self.receipt["sha256"]="0"*64
        self.assertIn("render_bytes_changed",self.call()["blockers"])

    def test_unverified_remote_not_published(self):
        self.receipt["publication_state"]="published_unverified"
        self.assertIn("artifact_not_durably_published",self.call()["blockers"])

    def test_stale_reader_review_rejected(self):
        self.assertIn("human_reader_review_stale",self.call(reader_verdict={
            "status":"READER_REVIEWED","pdf_sha256":"e"*64})["blockers"])

    def test_complete_claims_remain_unauthenticated(self):
        self.manifest["render_profile"]="exec"
        self.receipt["qa_state"]="PASS"
        self.receipt["authorization_state"]="HITL_REFERENCED"
        self.receipt["human_decision_ref"]="fixture://human"
        self.receipt["publication_state"]="published_verified"
        self.receipt["readback"]={"uri":"https://example.org/fixture","sha256":self.hash,
                                   "verified_at":"2026-11-04T20:00:00Z","method":"independent_readback"}
        frozen={"status":"VERIFIED_FROZEN_BUNDLE","bundle_sha256":"b"*64,"payload_sha256":"c"*64}
        reviewed={"status":"READER_REVIEWED","pdf_sha256":self.hash}
        result=self.call(independent_readback=self.content,freeze_verdict=frozen,reader_verdict=reviewed)
        self.assertEqual(result["status"],"AWAIT_AUTHENTICATED_HUMAN_RELEASE")
        self.assertFalse(result["committee_authorized"])
        self.assertFalse(result["human_authenticity_verified"])


if __name__=="__main__":
    unittest.main()
