"""Optimistic session checkpoint verification and dependency invalidation (#39).

This module does not write state or verify the authenticity of human approval.
"""
import hashlib
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA = json.loads((Path(__file__).resolve().parents[1] / "contracts" / "session-checkpoint.schema.json").read_text(encoding="utf-8"))


def validate_checkpoint(record):
    Draft202012Validator(SCHEMA, format_checker=FormatChecker()).validate(record)
    sources = [p["path"] for p in record["input_pins"]]
    if len(sources) != len(set(sources)):
        raise ValueError("duplicate input paths")
    if len({p["path"] for p in record["output_pins"]}) != len(record["output_pins"]):
        raise ValueError("duplicate output paths")
    if any(not set(o["depends_on"]) <= set(sources) for o in record["output_pins"]):
        raise ValueError("output depends on unpinned input")
    if record["gate"] == "APPROVED_REF_ONLY" and not record.get("human_decision_ref"):
        raise ValueError("approved-reference checkpoint must carry a decision reference")
    return True


def safe_file(root, relative):
    root = Path(root).resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError("checkpoint path escapes root")
    return path


def verify_inputs(record, root, observed_repo_sha):
    validate_checkpoint(record)
    if observed_repo_sha != record["repo_sha"]:
        return {"status": "CONFLICT", "reason": "repo SHA changed; no write permitted"}
    pins = [record["run_context"], *record["input_pins"]]
    for item in pins:
        path = safe_file(root, item["path"])
        if not path.is_file():
            return {"status": "BLOCKED", "reason": "missing pinned file: " + item["path"]}
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != item["sha256"]:
            return {"status": "STALE", "reason": "input bytes changed: " + item["path"]}
    return {"status": "READY_TO_RESUME", "human_approval_verified": False, "outputs_promoted": False}


def invalidate_outputs(record, changed_input_paths):
    validate_checkpoint(record)
    pinned = {item["path"] for item in record["input_pins"]}
    changed = set(changed_input_paths)
    if not changed <= pinned:
        raise ValueError("unrecognized changed input must trigger targeted re-research")
    return sorted(o["path"] for o in record["output_pins"] if changed.intersection(o["depends_on"]))


if __name__ == "__main__":
    try:
        record = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        validate_checkpoint(record)
        print(json.dumps({"status":"CHECKPOINT_METADATA_VALID","human_approval_verified":False}))
    except Exception as exc:
        print(json.dumps({"status":"FAIL","reason":str(exc)}))
        sys.exit(1)
