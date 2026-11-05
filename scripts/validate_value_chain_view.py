"""Validate business model projections without activating or modifying the exec v0.3 renderer."""
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def check_view(view):
    schema = json.loads((ROOT / "contracts/value-chain-view.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(view)
    drivers = {d["id"] for d in view["drivers"]}
    activities = {a["id"] for a in view["activities"]}
    if len(drivers) != len(view["drivers"]) or len(activities) != len(view["activities"]):
        raise ValueError("duplicate driver or activity ID")
    opportunities = [u["id"] for u in view["opportunities"]]
    if len(set(opportunities)) != len(opportunities):
        raise ValueError("duplicate use case ID")
    for a in view["activities"]:
        if not set(a["driver_refs"]) <= drivers:
            raise ValueError("activity references missing driver")
        if a["epistemic_status"] == "fact" and not a["claim_refs"]:
            raise ValueError("fact activity without claims")
    for u in view["opportunities"]:
        if u["activity_id"] not in activities or not set(u["driver_refs"]) <= drivers:
            raise ValueError("opportunity dangling activity or driver")
    return {"status": "VIEW_STRUCTURALLY_VALID_UNAPPROVED", "activities": len(activities),
            "drivers": len(drivers), "evidence_integrity_verified": False,
            "render_authorized": False, "committee_authorized": False}


if __name__ == "__main__":
    try:
        view = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        print(json.dumps(check_view(view)))
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}))
        sys.exit(1)
