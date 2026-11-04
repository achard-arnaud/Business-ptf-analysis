"""RunContext stage compatibility tests (#45).

v0.1 snapshots remain readable; new research milestones require v0.2.
This is a shape check, not a state-transition engine or human approval.
"""
import copy
import json
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"


def sample(stage="RESEARCH", version="0.2.0"):
    return {
        "version": version,
        "entity_id": "synthetic-company",
        "stage": stage,
        "analysis_dimension": "business",
        "package_sha256": "a" * 64,
        "source_refs": [], "claim_refs": [], "contradictions": [],
        "unknowns": [], "rejected_alternatives": [], "hard_gates": [],
        "versions": {"workflow": "0.2.0", "template": "0.1.0", "fixture": "0.1.0"},
        "red_team_verdict": "NOT_RUN", "repair_count": 0,
        "hitl": None, "next_action": "Continue research on bounded scope",
    }


class RunContextStages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.external = json.loads((CONTRACTS / "run-context.schema.json").read_text(encoding="utf-8"))
        cls.embedded = json.loads((CONTRACTS / "three-pager.schema.json").read_text(encoding="utf-8"))["properties"]["run_context"]

    def validate_both(self, value):
        for contract in (self.external, self.embedded):
            Draft202012Validator(contract, format_checker=FormatChecker()).validate(value)

    def reject_both(self, value):
        for contract in (self.external, self.embedded):
            with self.assertRaises(ValidationError):
                Draft202012Validator(contract, format_checker=FormatChecker()).validate(value)

    def test_source_and_embedded_run_contract_are_equivalent(self):
        self.assertEqual(self.external["properties"], self.embedded["properties"])
        self.assertEqual(self.external["required"], self.embedded["required"])
        self.assertEqual(self.external["additionalProperties"], self.embedded["additionalProperties"])
        self.assertEqual(self.external["allOf"], self.embedded["allOf"])

    def test_v01_snapshot_remains_readable(self):
        self.validate_both(sample("ANALYSIS", "0.1.0"))
        self.validate_both(sample("FROZEN", "0.1.0"))

    def test_v01_does_not_silently_gain_new_milestones(self):
        for stage in ("MARKET_CONTEXT", "OPPORTUNITIES"):
            with self.subTest(stage=stage):
                self.reject_both(sample(stage, "0.1.0"))

    def test_v02_accepts_market_and_opportunities(self):
        for stage in ("RESEARCH", "MARKET_CONTEXT", "ANALYSIS", "OPPORTUNITIES", "RED_TEAM", "HITL_PENDING"):
            with self.subTest(stage=stage):
                self.validate_both(sample(stage, "0.2.0"))

    def test_no_unknown_or_future_stage(self):
        for stage in ("PUBLISH", "READY", "NOT_A_STAGE"):
            with self.subTest(stage=stage):
                self.reject_both(sample(stage))

    def test_post_hitl_stage_cannot_have_null_hitl_in_v02(self):
        for stage in ("GO_DRAFT", "FROZEN", "RENDERED", "DONE"):
            with self.subTest(stage=stage):
                self.reject_both(sample(stage))

    def test_post_hitl_requires_go_draft_metadata(self):
        value = sample("FROZEN")
        value["hitl"] = {"decision": "GO_DRAFT", "actor": "synthetic-reviewer",
                         "decided_at": "2026-09-23", "decision_ref": "fixture://approval",
                         "package_sha256": "a"*64}
        self.validate_both(value)
        value["hitl"]["decision"] = "NARROW_SCOPE"
        self.reject_both(value)

    def test_invalid_hash_remains_invalid(self):
        value = sample()
        value["package_sha256"] = "invalid"
        self.reject_both(value)


if __name__ == "__main__":
    unittest.main()
